import os
import dearpygui.dearpygui as dpg


def _apply_material3_style():
    dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 10)
    dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 12)
    dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6)
    dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, 8)
    dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 8)
    dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 8)
    dpg.add_theme_style(dpg.mvStyleVar_TabRounding, 8)

    dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 16, 16)
    dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 12, 7)
    dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 10, 8)
    dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, 10)
    dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 0)
    dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0)
    dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0)
    dpg.add_theme_style(dpg.mvStyleVar_PopupBorderSize, 0)
    dpg.add_theme_style(dpg.mvStyleVar_TabBarBorderSize, 0)


def create_theme_from_palette(palette: dict) -> int:
    with dpg.theme() as theme_id:
        with dpg.theme_component(dpg.mvAll):
            for col_const, rgba in palette.items():
                dpg.add_theme_color(col_const, rgba)
            _apply_material3_style()
    return theme_id


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
    "Material 3 Blue Dark": _build_m3_palette(
        is_dark=True,
        surface=(18, 20, 24),
        container=(26, 29, 35),
        frame=(38, 42, 50),
        primary=(168, 199, 250),
        button=(8, 66, 160),
        button_hovered=(11, 87, 208),
        tertiary=(127, 213, 198),
    ),
    "Material 3 Blue Light": _build_m3_palette(
        is_dark=False,
        surface=(248, 250, 255),
        container=(238, 243, 252),
        frame=(225, 232, 245),
        primary=(11, 87, 208),
        button=(211, 227, 253),
        button_hovered=(184, 210, 250),
        tertiary=(20, 108, 46),
    ),
    "Material 3 Green Dark": _build_m3_palette(
        is_dark=True,
        surface=(18, 21, 18),
        container=(26, 30, 26),
        frame=(38, 44, 38),
        primary=(156, 214, 125),
        button=(32, 81, 22),
        button_hovered=(56, 106, 32),
        tertiary=(160, 207, 208),
    ),
    "Material 3 Green Light": _build_m3_palette(
        is_dark=False,
        surface=(248, 251, 244),
        container=(238, 244, 233),
        frame=(225, 234, 219),
        primary=(56, 106, 32),
        button=(183, 243, 151),
        button_hovered=(162, 228, 130),
        tertiary=(25, 104, 106),
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
DEFAULT_FONT_SIZE = 15


def _load_default_font(size: int = DEFAULT_FONT_SIZE) -> int | str | None:
    """テーマ標準の合成フォント（未存在時はシステムフォント）を登録して返す。"""
    merged_font_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "fonts", "RobotoNotoJP-Regular.ttf"
    )
    system_font_path = os.path.join(
        os.environ.get("WINDIR", r"C:\Windows"), "Fonts", "Roboto-Regular.ttf"
    )
    font_path = merged_font_path if os.path.exists(merged_font_path) else system_font_path
    if not os.path.exists(font_path):
        return None
    with dpg.font_registry():
        return dpg.add_font(font_path, size)


class ThemeManager:
    """Material 3 テーマ（配色・スタイル・フォント）の生成・切り替えを管理するクラス。"""

    def __init__(self, default_name: str = DEFAULT_THEME, font_size: int = DEFAULT_FONT_SIZE):
        self._font = _load_default_font(font_size)
        if self._font is not None:
            dpg.bind_font(self._font)

        self._themes: dict[str, int] = {
            name: create_theme_from_palette(palette)
            for name, palette in PALETTES.items()
        }
        self.default_name = (
            default_name if default_name in self._themes else next(iter(self._themes))
        )
        self.current_name = self.default_name

    @property
    def names(self) -> list[str]:
        return list(self._themes.keys())

    def apply(self, name: str | None = None) -> None:
        """指定したテーマ（未指定時はデフォルトテーマ）を適用する。"""
        target = name or self.default_name
        theme_id = self._themes.get(target, 0)
        if theme_id != 0:
            self.current_name = target
        dpg.bind_theme(theme_id)
