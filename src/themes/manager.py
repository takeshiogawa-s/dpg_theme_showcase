import os
from pathlib import Path
import dearpygui.dearpygui as dpg
from .palettes import DEFAULT_THEME, PALETTES, PLOT_COLORMAPS

DEFAULT_FONT_SIZE = 15


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

    dpg.add_theme_style(dpg.mvPlotStyleVar_PlotBorderSize, 0, category=dpg.mvThemeCat_Plots)
    dpg.add_theme_style(dpg.mvPlotStyleVar_PlotPadding, 8, 8, category=dpg.mvThemeCat_Plots)
    return dpg.add_theme_style(dpg.mvPlotStyleVar_LineWeight, 2.0, category=dpg.mvThemeCat_Plots)


def create_theme_from_palette(
    palette: dict,
    line_weight_items: list[int | str] | None = None,
) -> int:
    with dpg.theme() as theme_id:
        with dpg.theme_component(dpg.mvAll):
            for col_const, rgba in palette.items():
                dpg.add_theme_color(col_const, rgba)

            child_bg = palette[dpg.mvThemeCol_ChildBg]
            frame_bg = palette[dpg.mvThemeCol_FrameBg]
            border = palette[dpg.mvThemeCol_Border]
            text = palette[dpg.mvThemeCol_Text]
            text_disabled = palette[dpg.mvThemeCol_TextDisabled]

            plot_colors = {
                dpg.mvPlotCol_FrameBg: child_bg,
                dpg.mvPlotCol_PlotBg: frame_bg,
                dpg.mvPlotCol_PlotBorder: border,
                dpg.mvPlotCol_AxisText: text_disabled,
                dpg.mvPlotCol_AxisTick: text_disabled,
                dpg.mvPlotCol_AxisGrid: (border[0], border[1], border[2], 90),
                dpg.mvPlotCol_LegendBg: (child_bg[0], child_bg[1], child_bg[2], 215),
                dpg.mvPlotCol_LegendBorder: (border[0], border[1], border[2], 120),
                dpg.mvPlotCol_LegendText: text,
            }
            for col_const, rgba in plot_colors.items():
                dpg.add_theme_color(col_const, rgba, category=dpg.mvThemeCat_Plots)

            lw_id = _apply_material3_style()
            if line_weight_items is not None:
                line_weight_items.append(lw_id)
    return theme_id


def _load_default_font(size: int = DEFAULT_FONT_SIZE) -> int | str | None:
    """テーマ標準の合成フォント（未存在時はシステムフォント）を登録して返す。"""
    project_root = Path(__file__).resolve().parents[2]
    merged_font_path = project_root / "fonts" / "RobotoNotoJP-Regular.ttf"
    system_font_path = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts" / "Roboto-Regular.ttf"
    font_path = merged_font_path if merged_font_path.exists() else system_font_path
    if not font_path.exists():
        return None
    with dpg.font_registry():
        return dpg.add_font(str(font_path), size)


class ThemeManager:
    """Material 3 テーマ（配色・スタイル・フォント）の生成・切り替えを管理するクラス。"""

    def __init__(self, default_name: str = DEFAULT_THEME, font_size: int = DEFAULT_FONT_SIZE):
        self._font = _load_default_font(font_size)
        if self._font is not None:
            dpg.bind_font(self._font)

        self._line_weight_items: list[int | str] = []
        self._themes: dict[str, int] = {
            name: create_theme_from_palette(palette, line_weight_items=self._line_weight_items)
            for name, palette in PALETTES.items()
        }
        with dpg.colormap_registry():
            self._colormaps: dict[str, int | str] = {
                name: dpg.add_colormap(colors, True)
                for name, colors in PLOT_COLORMAPS.items()
            }
        self._plots: list[int | str] = []
        self.default_name = (
            default_name if default_name in self._themes else next(iter(self._themes))
        )
        self.current_name = self.default_name

    @property
    def names(self) -> list[str]:
        return list(self._themes.keys())

    def register_plot(self, plot_tag: int | str) -> None:
        """テーマ切り替え時にカラーマップを連動させるプロットを登録する。"""
        if plot_tag not in self._plots:
            self._plots.append(plot_tag)
        cm_id = self._colormaps.get(self.current_name)
        if cm_id is not None and dpg.does_item_exist(plot_tag):
            dpg.bind_colormap(plot_tag, cm_id)

    def set_plot_line_weight(self, weight: float) -> None:
        """全テーマのグラフ線の太さを動的に変更する。"""
        value = [float(weight), -1.0]
        for item_id in self._line_weight_items:
            if dpg.does_item_exist(item_id):
                dpg.set_value(item_id, value)

    def apply(self, name: str | None = None) -> None:
        """指定したテーマ（未指定時はデフォルトテーマ）を適用する。"""
        target = name or self.default_name
        theme_id = self._themes.get(target, 0)
        if theme_id != 0:
            self.current_name = target
        dpg.bind_theme(theme_id)
        cm_id = self._colormaps.get(self.current_name)
        if cm_id is not None:
            for plot_tag in self._plots:
                if dpg.does_item_exist(plot_tag):
                    dpg.bind_colormap(plot_tag, cm_id)
