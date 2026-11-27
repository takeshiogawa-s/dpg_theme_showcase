import dearpygui.dearpygui as dpg
from themes import ThemeManager
from ui import (
    LiveMonitor,
    build_about_modal,
    build_controls_panel,
    build_header,
    build_menu_bar,
    build_table_tab,
)

APP_NAME = "Dear PyGui Theme Showcase"
APP_VERSION = "0.1.0"


def main():
    dpg.create_context()

    theme_mgr = ThemeManager()
    monitor = LiveMonitor()

    with dpg.window(tag="PrimaryWindow", label=APP_NAME):
        build_menu_bar()
        build_header(theme_mgr)

        dpg.add_separator()
        dpg.add_spacer(height=4)

        with dpg.tab_bar():
            with dpg.tab(label="基本ウィジェット (Widgets)"):
                with dpg.group(horizontal=True):
                    build_controls_panel(theme_mgr)
                    monitor.build()
            build_table_tab()

    build_about_modal(APP_NAME, APP_VERSION)

    def on_viewport_resize():
        client_w = dpg.get_viewport_client_width()
        if client_w > 0 and dpg.does_item_exist("left_panel"):
            avail_w = max(400, client_w - 42)
            left_w = max(280, int(avail_w * 0.46))
            dpg.configure_item("left_panel", width=left_w)

    theme_mgr.register_plot("cpu_plot")
    theme_mgr.apply()

    dpg.create_viewport(title=APP_NAME, width=1280, height=720, min_width=620, min_height=420)
    dpg.set_viewport_resize_callback(on_viewport_resize)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.maximize_viewport()
    dpg.set_primary_window("PrimaryWindow", True)
    on_viewport_resize()

    while dpg.is_dearpygui_running():
        cpu_interval = float(dpg.get_value("cpu_interval_slider"))
        core_interval = float(dpg.get_value("core_interval_slider")) / 1000.0
        monitor.update(cpu_interval, core_interval)
        dpg.render_dearpygui_frame()

    dpg.destroy_context()


if __name__ == "__main__":
    main()
