import dearpygui.dearpygui as dpg


def _rgba(rgb: tuple[int, int, int], a: int = 255) -> tuple[int, int, int, int]:
    return (rgb[0], rgb[1], rgb[2], a)


def _shift(rgb: tuple[int, int, int], delta: int) -> tuple[int, int, int]:
    return (
        max(0, min(255, rgb[0] + delta)),
        max(0, min(255, rgb[1] + delta)),
        max(0, min(255, rgb[2] + delta)),
    )


def _build_m3_palette(
    *,
    is_dark: bool,
    surface: tuple[int, int, int],
    container: tuple[int, int, int],
    frame: tuple[int, int, int],
    primary: tuple[int, int, int],
    button: tuple[int, int, int],
    button_hovered: tuple[int, int, int],
    tertiary: tuple[int, int, int],
) -> dict:
    if is_dark:
        text = (230, 224, 233)
        text_disabled = (147, 143, 153)
        border = (73, 69, 79)
        frame_hovered = _shift(frame, 12)
        frame_active = _shift(frame, 25)
        primary_active = _shift(primary, 26)
        button_active = _shift(button, -18)
        scroll_hovered = _shift(border, 28)
        header = _shift(container, 18)
        header_hovered = _shift(container, 36)
    else:
        text = (29, 27, 32)
        text_disabled = (121, 116, 126)
        border = (202, 196, 208)
        frame_hovered = _shift(frame, -12)
        frame_active = _shift(frame, -24)
        primary_active = _shift(primary, -22)
        button_active = _shift(button_hovered, -18)
        scroll_hovered = _shift(border, -34)
        header = _shift(button, -6)
        header_hovered = _shift(button_hovered, -6)

    return {
        dpg.mvThemeCol_Text: _rgba(text),
        dpg.mvThemeCol_TextDisabled: _rgba(text_disabled),
        dpg.mvThemeCol_WindowBg: _rgba(surface),
        dpg.mvThemeCol_ChildBg: _rgba(container),
        dpg.mvThemeCol_PopupBg: _rgba(frame if is_dark else container, 252),
        dpg.mvThemeCol_Border: _rgba(border),
        dpg.mvThemeCol_FrameBg: _rgba(frame),
        dpg.mvThemeCol_FrameBgHovered: _rgba(frame_hovered),
        dpg.mvThemeCol_FrameBgActive: _rgba(frame_active),
        dpg.mvThemeCol_TitleBg: _rgba(surface if is_dark else container),
        dpg.mvThemeCol_TitleBgActive: _rgba(container if is_dark else frame),
        dpg.mvThemeCol_MenuBarBg: _rgba(container),
        dpg.mvThemeCol_ScrollbarBg: _rgba(surface if is_dark else container),
        dpg.mvThemeCol_ScrollbarGrab: _rgba(border),
        dpg.mvThemeCol_ScrollbarGrabHovered: _rgba(scroll_hovered),
        dpg.mvThemeCol_CheckMark: _rgba(primary),
        dpg.mvThemeCol_SliderGrab: _rgba(primary),
        dpg.mvThemeCol_SliderGrabActive: _rgba(primary_active),
        dpg.mvThemeCol_Button: _rgba(button),
        dpg.mvThemeCol_ButtonHovered: _rgba(button_hovered),
        dpg.mvThemeCol_ButtonActive: _rgba(button_active),
        dpg.mvThemeCol_Header: _rgba(header),
        dpg.mvThemeCol_HeaderHovered: _rgba(header_hovered),
        dpg.mvThemeCol_HeaderActive: _rgba(button),
        dpg.mvThemeCol_Tab: _rgba(container if is_dark else frame),
        dpg.mvThemeCol_TabHovered: _rgba(button_hovered),
        dpg.mvThemeCol_TabActive: _rgba(button),
        dpg.mvThemeCol_PlotLines: _rgba(primary),
        dpg.mvThemeCol_PlotHistogram: _rgba(tertiary),
    }


PALETTES = {
    "Material 3 Dark": _build_m3_palette(
        is_dark=True,
        surface=(20, 18, 24),
        container=(29, 27, 32),
        frame=(43, 41, 48),
        primary=(208, 188, 255),
        button=(79, 55, 139),
        button_hovered=(103, 80, 164),
        tertiary=(239, 184, 200),
    ),
    "Material 3 Light": _build_m3_palette(
        is_dark=False,
        surface=(254, 247, 255),
        container=(243, 237, 247),
        frame=(230, 224, 233),
        primary=(103, 80, 164),
        button=(234, 221, 255),
        button_hovered=(216, 198, 250),
        tertiary=(125, 82, 96),
    ),
    "Material 3 Rose Dark": _build_m3_palette(
        is_dark=True,
        surface=(23, 18, 20),
        container=(32, 26, 29),
        frame=(46, 38, 42),
        primary=(255, 177, 200),
        button=(123, 41, 73),
        button_hovered=(152, 64, 97),
        tertiary=(239, 189, 148),
    ),
    "Material 3 Rose Light": _build_m3_palette(
        is_dark=False,
        surface=(255, 248, 249),
        container=(250, 238, 241),
        frame=(242, 226, 230),
        primary=(152, 64, 97),
        button=(255, 217, 226),
        button_hovered=(252, 195, 210),
        tertiary=(124, 86, 53),
    ),
    "Material 3 Amber Dark": _build_m3_palette(
        is_dark=True,
        surface=(23, 20, 16),
        container=(32, 28, 23),
        frame=(46, 41, 34),
        primary=(245, 191, 72),
        button=(108, 72, 0),
        button_hovered=(138, 94, 0),
        tertiary=(169, 209, 142),
    ),
    "Material 3 Amber Light": _build_m3_palette(
        is_dark=False,
        surface=(255, 249, 240),
        container=(250, 241, 227),
        frame=(242, 230, 212),
        primary=(125, 87, 0),
        button=(255, 222, 166),
        button_hovered=(248, 205, 134),
        tertiary=(68, 103, 50),
    ),
    "Material 3 Monochrome Dark": _build_m3_palette(
        is_dark=True,
        surface=(18, 18, 18),
        container=(27, 27, 27),
        frame=(40, 40, 40),
        primary=(212, 212, 212),
        button=(72, 72, 72),
        button_hovered=(92, 92, 92),
        tertiary=(170, 170, 170),
    ),
    "Material 3 Monochrome Light": _build_m3_palette(
        is_dark=False,
        surface=(250, 250, 250),
        container=(240, 240, 240),
        frame=(226, 226, 226),
        primary=(64, 64, 64),
        button=(216, 216, 216),
        button_hovered=(198, 198, 198),
        tertiary=(105, 105, 105),
    ),
}

DEFAULT_THEME = "Material 3 Dark"

PLOT_COLORMAPS: dict[str, list[tuple[int, int, int, int]]] = {
    "Material 3 Dark": [
        (208, 188, 255, 255),
        (239, 184, 200, 255),
        (136, 214, 204, 255),
        (168, 199, 250, 255),
        (245, 198, 120, 255),
        (166, 217, 148, 255),
    ],
    "Material 3 Light": [
        (103, 80, 164, 255),
        (125, 82, 96, 255),
        (0, 106, 102, 255),
        (43, 98, 184, 255),
        (140, 92, 16, 255),
        (56, 110, 44, 255),
    ],
    "Material 3 Rose Dark": [
        (255, 177, 200, 255),
        (239, 189, 148, 255),
        (208, 188, 255, 255),
        (146, 214, 196, 255),
        (164, 202, 245, 255),
        (235, 212, 134, 255),
    ],
    "Material 3 Rose Light": [
        (152, 64, 97, 255),
        (124, 86, 53, 255),
        (103, 80, 164, 255),
        (26, 108, 96, 255),
        (54, 96, 168, 255),
        (122, 102, 24, 255),
    ],
    "Material 3 Amber Dark": [
        (245, 191, 72, 255),
        (169, 209, 142, 255),
        (239, 184, 168, 255),
        (138, 210, 214, 255),
        (204, 186, 248, 255),
        (244, 168, 196, 255),
    ],
    "Material 3 Amber Light": [
        (125, 87, 0, 255),
        (68, 103, 50, 255),
        (156, 66, 52, 255),
        (12, 104, 114, 255),
        (102, 78, 158, 255),
        (148, 62, 96, 255),
    ],
    "Material 3 Monochrome Dark": [
        (242, 242, 242, 255),
        (208, 208, 208, 255),
        (176, 176, 176, 255),
        (144, 144, 144, 255),
        (116, 116, 116, 255),
        (88, 88, 88, 255),
    ],
    "Material 3 Monochrome Light": [
        (28, 28, 28, 255),
        (62, 62, 62, 255),
        (96, 96, 96, 255),
        (126, 126, 126, 255),
        (154, 154, 154, 255),
        (182, 182, 182, 255),
    ],
}
