import platform
import dearpygui.dearpygui as dpg
from themes import ThemeManager


def show_about_modal() -> None:
    """バージョン情報モーダルをビューポート中央に表示する。"""
    modal_w, modal_h = 360, 195
    vw = dpg.get_viewport_client_width()
    vh = dpg.get_viewport_client_height()
    if vw > 0 and vh > 0:
        dpg.set_item_pos("about_modal", [(vw - modal_w) // 2, (vh - modal_h) // 2])
    dpg.configure_item("about_modal", show=True)


def build_menu_bar() -> None:
    """上部メニューバーを構築する。"""
    with dpg.menu_bar():
        with dpg.menu(label="ファイル"):
            dpg.add_menu_item(label="終了", callback=lambda: dpg.stop_dearpygui())
        with dpg.menu(label="ヘルプ"):
            dpg.add_menu_item(label="バージョン情報", callback=show_about_modal)


def build_header(theme_mgr: ThemeManager) -> None:
    """テーマ切り替え用のヘッダー操作バーを構築する。"""
    with dpg.group(horizontal=True):
        dpg.add_text("テーマ (Theme):")
        dpg.add_combo(
            tag="theme_selector",
            items=theme_mgr.names,
            default_value=theme_mgr.default_name,
            width=220,
            callback=lambda s, app_data: theme_mgr.apply(app_data),
        )


def build_about_modal(app_name: str, app_version: str) -> None:
    """バージョン情報モーダルウィンドウを構築する。"""
    with dpg.window(
        tag="about_modal",
        label="バージョン情報",
        modal=True,
        show=False,
        no_resize=True,
        width=360,
        height=195,
    ):
        dpg.add_text(app_name)
        dpg.add_text(f"Version {app_version}")
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
