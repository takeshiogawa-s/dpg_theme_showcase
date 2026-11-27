import collections
import math
import platform
import time
import dearpygui.dearpygui as dpg
import psutil
from themes import ThemeManager

APP_NAME = "Dear PyGui Theme Showcase"
APP_VERSION = "0.1.0"


def main():
    dpg.create_context()

    theme_mgr = ThemeManager()

    def show_about_modal():
        modal_w, modal_h = 360, 195
        vw = dpg.get_viewport_client_width()
        vh = dpg.get_viewport_client_height()
        if vw > 0 and vh > 0:
            dpg.set_item_pos("about_modal", [(vw - modal_w) // 2, (vh - modal_h) // 2])
        dpg.configure_item("about_modal", show=True)

    cpu_history = collections.deque([0.0] * 60, maxlen=60)
    psutil.cpu_percent(interval=None)
    initial_cores = psutil.cpu_percent(percpu=True)

    with dpg.window(tag="PrimaryWindow", label=APP_NAME):
        # 上部メニューバー
        with dpg.menu_bar():
            with dpg.menu(label="ファイル"):
                dpg.add_menu_item(label="スタイルエディタ", callback=lambda: dpg.show_style_editor())
                dpg.add_separator()
                dpg.add_menu_item(label="終了", callback=lambda: dpg.stop_dearpygui())
            with dpg.menu(label="ヘルプ"):
                dpg.add_menu_item(label="バージョン情報", callback=show_about_modal)

        # ヘッダー操作バー
        with dpg.group(horizontal=True):
            dpg.add_text("テーマ (Theme):")
            dpg.add_combo(
                tag="theme_selector",
                items=theme_mgr.names,
                default_value=theme_mgr.default_name,
                width=200,
                callback=lambda s, app_data: theme_mgr.apply(app_data),
            )
            dpg.add_spacer(width=12)
            dpg.add_button(
                label="スタイルエディタを開く (Style Editor)",
                callback=lambda: dpg.show_style_editor(),
            )

        dpg.add_separator()
        dpg.add_spacer(height=4)

        with dpg.tab_bar(tag="main_tabs"):
            # タブ1: 基本ウィジェット一覧
            with dpg.tab(label="基本ウィジェット (Widgets)"):
                with dpg.group(horizontal=True):
                    # 左カラム
                    with dpg.child_window(tag="left_panel", width=360, height=-1, always_use_window_padding=True):
                        dpg.add_text("入力と選択 (Input & Selection)")
                        dpg.add_separator()
                        dpg.add_input_text(label="テキスト入力", default_value="サンプルテキスト (Sample)")
                        dpg.add_input_float(label="数値入力 (Float)", default_value=3.14, step=0.1)
                        dpg.add_slider_float(label="スライダー (Float)", default_value=0.65, min_value=0.0, max_value=1.0)
                        dpg.add_slider_int(label="スライダー (Int)", default_value=42, min_value=0, max_value=100)
                        dpg.add_combo(label="ドロップダウン", items=["Option A (標準)", "Option B (拡張)", "Option C (カスタム)"], default_value="Option A (標準)")
                        dpg.add_spacer(height=4)
                        dpg.add_checkbox(label="機能を有効化 (Enable Feature)", default_value=True)
                        dpg.add_radio_button(items=["モード 1", "モード 2", "モード 3"], horizontal=True)
                        dpg.add_spacer(height=6)
                        with dpg.group(horizontal=True):
                            dpg.add_button(label="実行 (Primary)", width=140)
                            dpg.add_button(label="キャンセル", width=110)

                    # 右カラム
                    with dpg.child_window(tag="right_panel", width=-1, height=-1, always_use_window_padding=True):
                        dpg.add_text("リアルタイム PC モニタ (Live Stats)")
                        dpg.add_separator()
                        dpg.add_text("CPU: --.-%  |  RAM: --.-%", tag="pc_stats_text")
                        dpg.add_simple_plot(
                            tag="cpu_plot",
                            label="CPU (%)",
                            default_value=list(cpu_history),
                            min_scale=0.0,
                            max_scale=100.0,
                            height=85,
                            width=-1,
                        )
                        dpg.add_simple_plot(
                            tag="core_plot",
                            label="Cores (%)",
                            default_value=initial_cores,
                            min_scale=0.0,
                            max_scale=100.0,
                            height=85,
                            width=-1,
                            histogram=True,
                        )
                        dpg.add_spacer(height=4)
                        dpg.add_progress_bar(tag="mem_bar", default_value=0.0, overlay="RAM: --.-%", width=-1)
                        dpg.add_spacer(height=4)
                        with dpg.tree_node(label="詳細情報 (Collapsible Details)", default_open=True):
                            dpg.add_text("• 0.3 秒ごとに CPU・各コア・メモリ使用率を更新")
                            dpg.add_text("• themes.py で Material 3 配色や角丸を管理")

            # タブ2: テーブル表示確認
            with dpg.tab(label="テーブル表示 (Table View)"):
                with dpg.table(header_row=True, row_background=True, borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True):
                    dpg.add_table_column(label="ID")
                    dpg.add_table_column(label="項目 (Parameter)")
                    dpg.add_table_column(label="設定値 (Value)")
                    dpg.add_table_column(label="状態 (Status)")

                    rows = [
                        ("001", "サンプリング周波数 (Sampling Rate)", "48.0 kHz", "正常 (OK)"),
                        ("002", "バッファサイズ (Buffer Size)", "512 samples", "正常 (OK)"),
                        ("003", "ゲイン調整 (Gain Offset)", "+2.4 dB", "有効 (Active)"),
                        ("004", "スレッショルド (Threshold)", "-12.0 dB", "待機中 (Standby)"),
                    ]
                    for r in rows:
                        with dpg.table_row():
                            for cell in r:
                                dpg.add_text(cell)

            # タブ3: 拡張ウィジェット
            with dpg.tab(label="拡張ウィジェット (More)"):
                with dpg.group(horizontal=True):
                    # 左カラム
                    with dpg.child_window(tag="more_left_panel", width=360, height=-1, always_use_window_padding=True):
                        dpg.add_text("リストと選択 (List & Selectables)")
                        dpg.add_separator()
                        dpg.add_listbox(
                            label="リストボックス",
                            items=["Item 1 (標準)", "Item 2 (ハイライト)", "Item 3 (選択)", "Item 4", "Item 5"],
                            num_items=4,
                        )
                        dpg.add_spacer(height=4)
                        dpg.add_text("選択可能行 (Selectable):")
                        dpg.add_selectable(label="Selectable 項目 A (選択中)", default_value=True)
                        dpg.add_selectable(label="Selectable 項目 B", default_value=False)
                        dpg.add_selectable(label="Selectable 項目 C", default_value=False)
                        dpg.add_spacer(height=6)
                        dpg.add_color_edit(label="カラーピッカー (ColorEdit)", default_value=(103, 80, 164, 255))

                    # 右カラム
                    with dpg.child_window(tag="more_right_panel", width=-1, height=-1, always_use_window_padding=True):
                        dpg.add_text("テキストエリアと折りたたみ (Text & Headers)")
                        dpg.add_separator()
                        dpg.add_input_text(
                            label="##multiline",
                            multiline=True,
                            width=-1,
                            height=120,
                            default_value=(
                                "複数行テキストエリア (Multiline)\n"
                                "• スクロールバーや選択範囲の見た目を確認できます。\n"
                                "• 日本語と English の混在表示テスト。\n"
                                "4行目: サンプル行\n"
                                "5行目: サンプル行\n"
                                "6行目: サンプル行\n"
                                "7行目: サンプル行"
                            ),
                        )
                        dpg.add_spacer(height=6)
                        with dpg.collapsing_header(label="折りたたみヘッダー 1 (CollapsingHeader)", default_open=True):
                            dpg.add_text("Header / HeaderHovered / HeaderActive の配色確認用")
                            dpg.add_button(label="ツールチップ付きボタン (Hover me)", tag="tooltip_btn")
                            with dpg.tooltip("tooltip_btn"):
                                dpg.add_text("Tooltip: PopupBg と角丸の確認用メッセージ")
                        with dpg.collapsing_header(label="折りたたみヘッダー 2 (Collapsed)"):
                            dpg.add_text("展開時に表示されるコンテンツ")

            # タブ4: GPU 負荷テスト
            with dpg.tab(tag="gpu_tab", label="GPU 負荷テスト (Benchmark)"):
                with dpg.group(horizontal=True):
                    dpg.add_checkbox(tag="gpu_bench_enabled", label="負荷テストを実行", default_value=False)
                    dpg.add_spacer(width=8)
                    dpg.add_combo(
                        tag="gpu_bench_mode",
                        items=[
                            "半透明サークル (Fillrate)",
                            "高精細メッシュ (Vertices)",
                            "複合 (Heavy Mix)",
                        ],
                        default_value="半透明サークル (Fillrate)",
                        width=210,
                    )
                    dpg.add_spacer(width=8)
                    dpg.add_slider_int(
                        tag="gpu_bench_count",
                        label="描画数",
                        default_value=800,
                        min_value=100,
                        max_value=5000,
                        width=140,
                    )

                dpg.add_text("FPS: --.-  |  Frame Time: --.- ms  |  状態: 停止中", tag="gpu_stats_text")
                dpg.add_simple_plot(
                    tag="fps_plot",
                    label="FPS",
                    default_value=[60.0] * 60,
                    min_scale=0.0,
                    max_scale=165.0,
                    height=45,
                    width=-1,
                )
                with dpg.child_window(tag="gpu_canvas_wrap", width=-1, height=-1, no_scrollbar=True):
                    dpg.add_drawlist(tag="gpu_canvas", width=740, height=240)

    # バージョン情報モーダル
    with dpg.window(
        tag="about_modal",
        label="バージョン情報",
        modal=True,
        show=False,
        no_resize=True,
        width=360,
        height=195,
    ):
        dpg.add_text(APP_NAME)
        dpg.add_text(f"Version {APP_VERSION}")
        dpg.add_spacer(height=4)
        dpg.add_separator()
        dpg.add_spacer(height=4)
        dpg.add_text(f"Python {platform.python_version()}")
        dpg.add_text(f"Dear PyGui {dpg.get_dearpygui_version()}")
        dpg.add_spacer(height=10)
        dpg.add_button(
            label="閉じる",
            width=-1,
            callback=lambda: dpg.configure_item("about_modal", show=False),
        )

    def on_viewport_resize():
        client_w = dpg.get_viewport_client_width()
        client_h = dpg.get_viewport_client_height()
        if client_w > 0:
            # ウィンドウ左右パディング(32) + カラム間スペース(10) を差し引いた幅の約46%を左カラムに割り当てる
            avail_w = max(400, client_w - 42)
            left_w = max(280, int(avail_w * 0.46))
            for panel_tag in ("left_panel", "more_left_panel"):
                if dpg.does_item_exist(panel_tag):
                    dpg.configure_item(panel_tag, width=left_w)
            if dpg.does_item_exist("gpu_canvas"):
                dpg.configure_item(
                    "gpu_canvas",
                    width=max(300, client_w - 48),
                    height=max(140, client_h - 235),
                )

    def render_gpu_benchmark(phase: float):
        dpg.delete_item("gpu_canvas", children_only=True)
        cw = dpg.get_item_width("gpu_canvas") or 740
        ch = dpg.get_item_height("gpu_canvas") or 240
        count = dpg.get_value("gpu_bench_count")
        mode = dpg.get_value("gpu_bench_mode")

        for i in range(count):
            t = phase + i * 0.037
            cx = (0.5 + 0.42 * math.sin(t * 1.13 + i * 0.011)) * cw
            cy = (0.5 + 0.42 * math.cos(t * 0.87 + i * 0.017)) * ch
            r = (i * 53) % 180 + 75
            g = (i * 97) % 180 + 75
            b = (i * 151) % 180 + 75

            if mode == "半透明サークル (Fillrate)":
                dpg.draw_circle(
                    center=(cx, cy),
                    radius=45 + (i % 65),
                    color=(r, g, b, 60),
                    fill=(r, g, b, 24),
                    segments=48,
                    parent="gpu_canvas",
                )
            elif mode == "高精細メッシュ (Vertices)":
                rad = 28 + (i % 45)
                a1 = t * 1.5
                a2 = a1 + 2.094
                a3 = a1 + 4.188
                dpg.draw_triangle(
                    p1=(cx + math.cos(a1) * rad, cy + math.sin(a1) * rad),
                    p2=(cx + math.cos(a2) * rad, cy + math.sin(a2) * rad),
                    p3=(cx + math.cos(a3) * rad, cy + math.sin(a3) * rad),
                    color=(r, g, b, 190),
                    fill=(r, g, b, 45),
                    thickness=1.2,
                    parent="gpu_canvas",
                )
            else:
                if i % 2 == 0:
                    dpg.draw_circle(
                        center=(cx, cy),
                        radius=35 + (i % 55),
                        color=(r, g, b, 90),
                        fill=(r, g, b, 28),
                        segments=48,
                        parent="gpu_canvas",
                    )
                else:
                    rad = 32 + (i % 40)
                    a1 = t * 1.3
                    dpg.draw_triangle(
                        p1=(cx + math.cos(a1) * rad, cy + math.sin(a1) * rad),
                        p2=(cx + math.cos(a1 + 2.094) * rad, cy + math.sin(a1 + 2.094) * rad),
                        p3=(cx + math.cos(a1 + 4.188) * rad, cy + math.sin(a1 + 4.188) * rad),
                        color=(r, g, b, 170),
                        fill=(r, g, b, 40),
                        thickness=1.2,
                        parent="gpu_canvas",
                    )

    # 初期テーマ適用
    theme_mgr.apply()

    dpg.create_viewport(title="Dear PyGui Theme Showcase", width=800, height=520, min_width=620, min_height=420)
    dpg.set_viewport_resize_callback(on_viewport_resize)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("PrimaryWindow", True)
    on_viewport_resize()

    fps_history = collections.deque([60.0] * 60, maxlen=60)
    gpu_tab_id = dpg.get_alias_id("gpu_tab")
    last_update = 0.0
    prev_frame_time = time.perf_counter()
    phase = 0.0

    while dpg.is_dearpygui_running():
        now = time.monotonic()
        frame_now = time.perf_counter()
        dt = max(1e-6, frame_now - prev_frame_time)
        prev_frame_time = frame_now
        fps = 1.0 / dt

        if now - last_update >= 0.01:
            last_update = now
            cpu_total = psutil.cpu_percent(interval=None)
            cpu_cores = psutil.cpu_percent(percpu=True)
            mem = psutil.virtual_memory()

            cpu_history.append(cpu_total)
            dpg.set_value("cpu_plot", list(cpu_history))
            dpg.set_value("core_plot", cpu_cores)
            dpg.set_value("mem_bar", mem.percent / 100.0)
            dpg.configure_item(
                "mem_bar",
                overlay=f"RAM: {mem.percent:.1f}% ({mem.used / (1024**3):.1f} / {mem.total / (1024**3):.1f} GB)",
            )
            dpg.set_value(
                "pc_stats_text",
                f"CPU: {cpu_total:.1f}% ({len(cpu_cores)} cores)  |  RAM: {mem.percent:.1f}%",
            )

        is_gpu_tab = dpg.get_value("main_tabs") in ("gpu_tab", gpu_tab_id)
        if is_gpu_tab and dpg.get_value("gpu_bench_enabled"):
            phase += dt * 1.8
            render_gpu_benchmark(phase)
            fps_history.append(fps)
            dpg.set_value("fps_plot", list(fps_history))
            dpg.set_value(
                "gpu_stats_text",
                f"FPS: {fps:.1f}  |  Frame Time: {dt * 1000:.2f} ms  |  状態: 実行中",
            )
        elif is_gpu_tab:
            dpg.set_value(
                "gpu_stats_text",
                f"FPS: {fps:.1f}  |  Frame Time: {dt * 1000:.2f} ms  |  状態: 停止中",
            )

        dpg.render_dearpygui_frame()

    dpg.destroy_context()


if __name__ == "__main__":
    main()
