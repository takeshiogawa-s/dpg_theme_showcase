import collections
import random
import time
import dearpygui.dearpygui as dpg


class LiveMonitor:
    """ダミーデータを用いたリアルタイム PC モニタの UI と更新を管理するクラス。"""

    def __init__(self, num_cores: int = 8, total_ram_gb: float = 16.0):
        self.num_cores = num_cores
        self.total_ram_gb = total_ram_gb
        self.mem_val = 52.0
        self.x_vals: list[float] = [float(i) for i in range(60)]
        self.series_specs = [
            ("cpu_series_total", "Total"),
            ("cpu_series_core1", "Core 1"),
            ("cpu_series_core2", "Core 2"),
            ("cpu_series_core3", "Core 3"),
            ("cpu_series_core4", "Core 4"),
            ("cpu_series_core5", "Core 5"),
        ]
        self.series_vals = [20.0 + i * 11.0 for i in range(len(self.series_specs))]
        self.series_histories = [
            collections.deque([v] * 60, maxlen=60) for v in self.series_vals
        ]
        self.core_vals = [random.uniform(15.0, 55.0) for _ in range(num_cores)]
        self._last_cpu_update = 0.0
        self._last_core_update = 0.0

    def build(self) -> None:
        """リアルタイムモニタ用の右カラム UI を構築する。"""
        with dpg.child_window(
            tag="right_panel",
            width=-1,
            height=-1,
            always_use_window_padding=True,
        ):
            dpg.add_text("リアルタイム PC モニタ (Sample Data)")
            dpg.add_separator()
            dpg.add_text("CPU: --.-%  |  RAM: --.-%", tag="pc_stats_text")
            dpg.add_spacer(height=2)
            dpg.add_text("CPU (%)")
            with dpg.plot(
                tag="cpu_plot",
                no_title=True,
                no_menus=True,
                no_box_select=True,
                no_mouse_pos=True,
                height=150,
                width=-1,
            ):
                dpg.add_plot_legend(
                    location=dpg.mvPlot_Location_NorthWest,
                    horizontal=True,
                    no_menus=True,
                )
                dpg.add_plot_axis(
                    dpg.mvXAxis,
                    tag="cpu_x_axis",
                    no_tick_labels=True,
                    no_tick_marks=True,
                    no_menus=True,
                )
                dpg.set_axis_limits("cpu_x_axis", 0, 59)
                with dpg.plot_axis(dpg.mvYAxis, tag="cpu_y_axis", no_menus=True):
                    dpg.set_axis_limits("cpu_y_axis", 0, 100)
                    for (tag, label), history in zip(self.series_specs, self.series_histories):
                        dpg.add_line_series(self.x_vals, list(history), label=label, tag=tag)

            dpg.add_text("Cores (%)")
            dpg.add_simple_plot(
                tag="core_plot",
                label="",
                default_value=self.core_vals,
                min_scale=0.0,
                max_scale=100.0,
                height=85,
                width=-1,
                histogram=True,
            )
            dpg.add_spacer(height=4)
            dpg.add_progress_bar(
                tag="mem_bar",
                default_value=self.mem_val / 100.0,
                overlay="RAM: --.-%",
                width=-1,
            )
            dpg.add_spacer(height=4)
            with dpg.tree_node(label="詳細情報 (Collapsible Details)", default_open=True):
                dpg.add_text("• ランダム生成したダミー数値をリアルタイム表示")
                dpg.add_text("• src/themes/ の ThemeManager で配色・角丸・フォントを一括管理")

    def update(self, cpu_interval: float, core_interval: float) -> None:
        """指定された更新間隔に従って CPU・Core・RAM 表示を更新する。"""
        now = time.monotonic()
        safe_cpu_interval = max(0.05, cpu_interval)
        safe_core_interval = max(0.05, core_interval)

        if now - self._last_cpu_update >= safe_cpu_interval:
            self._last_cpu_update = now
            self.series_vals = [
                max(2.0, min(98.0, v + random.uniform(-12.0, 12.0)))
                for v in self.series_vals
            ]
            self.mem_val = max(25.0, min(88.0, self.mem_val + random.uniform(-1.5, 1.5)))
            used_gb = self.total_ram_gb * (self.mem_val / 100.0)

            for (tag, _), val, history in zip(
                self.series_specs, self.series_vals, self.series_histories
            ):
                history.append(val)
                dpg.set_value(tag, [self.x_vals, list(history)])

            dpg.set_value("mem_bar", self.mem_val / 100.0)
            dpg.configure_item(
                "mem_bar",
                overlay=f"RAM: {self.mem_val:.1f}% ({used_gb:.1f} / {self.total_ram_gb:.1f} GB)",
            )
            dpg.set_value(
                "pc_stats_text",
                f"CPU: {self.series_vals[0]:.1f}% ({self.num_cores} cores)  |  RAM: {self.mem_val:.1f}%",
            )

        if now - self._last_core_update >= safe_core_interval:
            self._last_core_update = now
            self.core_vals = [
                max(2.0, min(98.0, v + random.uniform(-14.0, 14.0)))
                for v in self.core_vals
            ]
            dpg.set_value("core_plot", self.core_vals)
