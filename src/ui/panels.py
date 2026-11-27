import dearpygui.dearpygui as dpg
from themes import ThemeManager

LINE_WEIGHT_OPTIONS: dict[str, float] = {
    "1.0 px (極細)": 1.0,
    "1.5 px (細め)": 1.5,
    "2.0 px (標準)": 2.0,
    "3.0 px (太め)": 3.0,
    "4.5 px (極太)": 4.5,
}


def build_controls_panel(theme_mgr: ThemeManager) -> None:
    """基本ウィジェット一覧の左カラム（入力と選択）を構築する。"""
    with dpg.child_window(
        tag="left_panel",
        width=360,
        height=-1,
        always_use_window_padding=True,
    ):
        dpg.add_text("入力と選択 (Input & Selection)")
        dpg.add_separator()
        dpg.add_input_text(label="テキスト入力", default_value="サンプルテキスト (Sample)")
        dpg.add_input_float(label="数値入力 (Float)", default_value=3.14, step=0.1)
        dpg.add_slider_float(
            tag="cpu_interval_slider",
            label="スライダー (Float)",
            default_value=0.20,
            min_value=0.05,
            max_value=2.00,
            format="%.2f s",
        )
        dpg.add_slider_int(
            tag="core_interval_slider",
            label="スライダー (Int)",
            default_value=200,
            min_value=50,
            max_value=2000,
            format="%d ms",
        )
        dpg.add_combo(
            tag="line_weight_combo",
            label="ドロップダウン",
            items=list(LINE_WEIGHT_OPTIONS.keys()),
            default_value="2.0 px (標準)",
            callback=lambda s, app_data: theme_mgr.set_plot_line_weight(
                LINE_WEIGHT_OPTIONS[app_data]
            ),
        )
        dpg.add_spacer(height=4)
        dpg.add_checkbox(label="機能を有効化 (Enable Feature)", default_value=True)
        dpg.add_radio_button(items=["モード 1", "モード 2", "モード 3"], horizontal=True)
        dpg.add_spacer(height=6)
        with dpg.group(horizontal=True):
            dpg.add_button(label="実行 (Primary)", width=140)
            dpg.add_button(label="キャンセル", width=110)


def build_table_tab() -> None:
    """テーブル表示タブを構築する。"""
    with dpg.tab(label="テーブル表示 (Table View)"):
        with dpg.table(
            header_row=True,
            row_background=True,
            borders_innerH=True,
            borders_outerH=True,
            borders_innerV=True,
            borders_outerV=True,
        ):
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
