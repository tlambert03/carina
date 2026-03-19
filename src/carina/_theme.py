# ruff: noqa: E501
from __future__ import annotations

from dataclasses import dataclass, fields
from typing import TYPE_CHECKING, TypedDict, overload

if TYPE_CHECKING:
    from collections.abc import Mapping

    from typing_extensions import Any, Required, Unpack

    from carina import Qlementine

    class ThemeMetaDict(TypedDict):
        name: str
        """Name of the theme (e.g. "Light", "Dark", "Solarized")."""
        version: str
        """Version string for the theme (e.g. "1.0", "2.1")."""
        author: str
        """Author or creator of the theme."""

    class ThemeDict(TypedDict, total=False):
        meta: Required[ThemeMetaDict]
        """Metadata for the theme (name, version, author)."""

        background_color_main1: str
        """Primary background for content areas, dialogs, menus, and text inputs."""
        background_color_main2: str
        """Secondary background for menu bars, toolbars, and status bars."""
        background_color_main3: str
        """Tertiary background for disabled/inactive states and hover effects."""
        background_color_main4: str
        """Darkest background for additional depth in the visual hierarchy."""
        background_color_workspace: str
        """Background for MDI workspace areas and external boundaries."""
        background_color_tab_bar: str
        """Background for tab bar containers."""

        neutral_color: str
        """Default fill for secondary buttons, separators, and slider grooves."""
        neutral_color_hovered: str
        """Hover state for neutral elements (menu bar items, tool buttons)."""
        neutral_color_pressed: str
        """Pressed state for neutral elements."""
        neutral_color_disabled: str
        """Disabled state for neutral elements (sliders, dials, list items)."""

        focus_color: str
        """Border color for keyboard focus indicators on interactive widgets."""

        primary_color: str
        """Accent color for primary buttons, active menu items, sliders, and progress bars."""
        primary_color_hovered: str
        """Hover state for primary-colored elements."""
        primary_color_pressed: str
        """Pressed state for primary-colored elements."""
        primary_color_disabled: str
        """Disabled state for primary-colored elements."""

        primary_color_foreground: str
        """Text/icon color on primary-colored backgrounds."""
        primary_color_foreground_hovered: str
        """Foreground hover state on primary-colored backgrounds."""
        primary_color_foreground_pressed: str
        """Foreground pressed state on primary-colored backgrounds."""
        primary_color_foreground_disabled: str
        """Foreground disabled state on primary-colored backgrounds."""

        primary_alternative_color: str
        """Alternative accent for selected checkboxes and active list items."""
        primary_alternative_color_hovered: str
        """Hover state for alternative primary elements."""
        primary_alternative_color_pressed: str
        """Pressed state for alternative primary elements."""
        primary_alternative_color_disabled: str
        """Disabled state for alternative primary elements."""

        secondary_color: str
        """Foreground color for regular text, labels, menu text, and tooltips."""
        secondary_color_hovered: str
        """Hover state for secondary-colored text elements."""
        secondary_color_pressed: str
        """Pressed state for secondary-colored text elements."""
        secondary_color_disabled: str
        """Disabled state for text and placeholder text."""

        secondary_color_foreground: str
        """Text/icon color on secondary (dark) backgrounds for contrast."""
        secondary_color_foreground_hovered: str
        """Foreground hover state on secondary backgrounds."""
        secondary_color_foreground_pressed: str
        """Foreground pressed state on secondary backgrounds."""
        secondary_color_foreground_disabled: str
        """Foreground disabled state on secondary backgrounds."""

        secondary_alternative_color: str
        """Lighter color for captions, labels, and menu shortcut text."""
        secondary_alternative_color_hovered: str
        """Hover state for alternative secondary elements."""
        secondary_alternative_color_pressed: str
        """Pressed state for alternative secondary elements."""
        secondary_alternative_color_disabled: str
        """Disabled state for alternative secondary elements."""

        status_color_success: str
        """Success state color for status indicators and buttons."""
        status_color_success_hovered: str
        """Hover state for success-colored elements."""
        status_color_success_pressed: str
        """Pressed state for success-colored elements."""
        status_color_success_disabled: str
        """Disabled state for success-colored elements."""

        status_color_info: str
        """Info state color for status indicators and buttons."""
        status_color_info_hovered: str
        """Hover state for info-colored elements."""
        status_color_info_pressed: str
        """Pressed state for info-colored elements."""
        status_color_info_disabled: str
        """Disabled state for info-colored elements."""

        status_color_warning: str
        """Warning state color for status indicators and buttons."""
        status_color_warning_hovered: str
        """Hover state for warning-colored elements."""
        status_color_warning_pressed: str
        """Pressed state for warning-colored elements."""
        status_color_warning_disabled: str
        """Disabled state for warning-colored elements."""

        status_color_error: str
        """Error state color for status indicators and buttons."""
        status_color_error_hovered: str
        """Hover state for error-colored elements."""
        status_color_error_pressed: str
        """Pressed state for error-colored elements."""
        status_color_error_disabled: str
        """Disabled state for error-colored elements."""

        status_color_foreground: str
        """Text/icon color on status-colored backgrounds."""
        status_color_foreground_hovered: str
        """Foreground hover state on status-colored backgrounds."""
        status_color_foreground_pressed: str
        """Foreground pressed state on status-colored backgrounds."""
        status_color_foreground_disabled: str
        """Foreground disabled state on status-colored backgrounds."""

        shadow_color1: str
        """Lightest shadow layer for subtle depth effects."""
        shadow_color2: str
        """Medium shadow layer for moderate depth effects."""
        shadow_color3: str
        """Darkest shadow layer for strong depth effects."""

        border_color: str
        """Default border color for controls (text fields, combo boxes)."""
        border_color_hovered: str
        """Hover state for control borders."""
        border_color_pressed: str
        """Pressed state for control borders."""
        border_color_disabled: str
        """Disabled state for control borders."""

        semi_transparent_color1: str
        """Lightest transparency overlay for subtle selection highlights."""
        semi_transparent_color2: str
        """Light transparency overlay for hover effects."""
        semi_transparent_color3: str
        """Medium transparency overlay for active selections."""
        semi_transparent_color4: str
        """Strongest transparency overlay for emphasized selections."""

        use_system_fonts: bool
        """Use OS system fonts instead of bundled Inter/Roboto fonts."""

        font_size: int
        """Base font size in pixels for regular text."""
        font_size_monospace: int
        """Font size in pixels for monospace/code text."""
        font_size_h1: int
        """Font size in pixels for h1 headings."""
        font_size_h2: int
        """Font size in pixels for h2 headings."""
        font_size_h3: int
        """Font size in pixels for h3 headings."""
        font_size_h4: int
        """Font size in pixels for h4 headings."""
        font_size_h5: int
        """Font size in pixels for h5 headings."""
        font_size_s1: int
        """Font size in pixels for small/caption text."""

        animation_duration: int
        """Duration in ms for standard color/state transitions."""
        focus_animation_duration: int
        """Duration in ms for focus border animations."""
        slider_animation_duration: int
        """Duration in ms for slider handle interactions."""

        border_radius: float
        """Default corner radius in pixels for buttons and containers."""
        check_box_border_radius: float
        """Corner radius in pixels for checkbox indicators."""
        menu_item_border_radius: float
        """Corner radius in pixels for menu item backgrounds."""
        menu_bar_item_border_radius: float
        """Corner radius in pixels for menu bar items."""
        border_width: int
        """Standard border thickness in pixels."""

        control_height_large: int
        """Height in pixels for large controls (prominent buttons/inputs)."""
        control_height_medium: int
        """Height in pixels for standard controls."""
        control_height_small: int
        """Height in pixels for compact controls."""
        control_default_width: int
        """Default width in pixels for combo boxes and similar controls."""

        dial_mark_length: int
        """Length in pixels of major tick marks on dial widgets."""
        dial_mark_thickness: int
        """Thickness in pixels of major tick marks on dial widgets."""
        dial_tick_length: int
        """Length in pixels of minor tick marks on dial widgets."""
        dial_tick_spacing: int
        """Spacing in pixels between dial tick marks."""
        dial_groove_thickness: int
        """Thickness in pixels of the dial groove track."""

        focus_border_width: int
        """Border thickness in pixels for focus ring indicators."""

        icon_extent: int
        """Base icon dimension in pixels (icons are square)."""

        slider_tick_size: int
        """Height in pixels of slider tick marks."""
        slider_tick_spacing: int
        """Horizontal spacing in pixels between slider ticks."""
        slider_tick_thickness: int
        """Width in pixels of slider tick marks."""
        slider_groove_height: int
        """Height in pixels of the slider track/groove."""

        progress_bar_groove_height: int
        """Height in pixels of the progress bar track."""
        spacing: int
        """Standard spacing unit in pixels used for padding and margins."""

        scroll_bar_thickness_full: int
        """Width in pixels of the scrollbar when fully visible."""
        scroll_bar_thickness_small: int
        """Width in pixels of the compact/mini scrollbar."""
        scroll_bar_margin: int
        """Margin in pixels between scrollbar and container edge."""

        tab_bar_padding_top: int
        """Top padding in pixels for tab bar items."""
        tab_bar_tab_max_width: int
        """Maximum tab width in pixels (0 = no limit)."""
        tab_bar_tab_min_width: int
        """Minimum tab width in pixels (0 = no minimum)."""


@dataclass(slots=True)
class ThemeMeta:
    """Metadata for a theme (name, version, author)."""

    name: str
    """Name of the theme (e.g. "Light", "Dark", "Solarized")."""
    version: str
    """Version string for the theme (e.g. "1.0", "2.1")."""
    author: str
    """Author or creator of the theme."""

    def asdict(self) -> ThemeMetaDict:
        return {"name": self.name, "version": self.version, "author": self.author}


@dataclass(slots=True)
class Theme:
    """Complete theme configuration for a Qt application.

    All color fields accept CSS-style hex strings (e.g. ``"#RRGGBB"`` or
    ``"#AARRGGBB"``).  Fields left as ``None`` use the Qlementine defaults.
    """

    meta: ThemeMeta
    """Metadata for the theme (name, version, author)."""

    background_color_main1: str | None = None
    """Primary background for content areas, dialogs, menus, and text inputs."""
    background_color_main2: str | None = None
    """Secondary background for menu bars, toolbars, and status bars."""
    background_color_main3: str | None = None
    """Tertiary background for disabled/inactive states and hover effects."""
    background_color_main4: str | None = None
    """Darkest background for additional depth in the visual hierarchy."""
    background_color_workspace: str | None = None
    """Background for MDI workspace areas and external boundaries."""
    background_color_tab_bar: str | None = None
    """Background for tab bar containers."""

    neutral_color: str | None = None
    """Default fill for secondary buttons, separators, and slider grooves."""
    neutral_color_hovered: str | None = None
    """Hover state for neutral elements (menu bar items, tool buttons)."""
    neutral_color_pressed: str | None = None
    """Pressed state for neutral elements."""
    neutral_color_disabled: str | None = None
    """Disabled state for neutral elements (sliders, dials, list items)."""

    focus_color: str | None = None
    """Border color for keyboard focus indicators on interactive widgets."""

    primary_color: str | None = None
    """Accent color for primary buttons, active menu items, sliders, and progress bars."""
    primary_color_hovered: str | None = None
    """Hover state for primary-colored elements."""
    primary_color_pressed: str | None = None
    """Pressed state for primary-colored elements."""
    primary_color_disabled: str | None = None
    """Disabled state for primary-colored elements."""

    primary_color_foreground: str | None = None
    """Text/icon color on primary-colored backgrounds."""
    primary_color_foreground_hovered: str | None = None
    """Foreground hover state on primary-colored backgrounds."""
    primary_color_foreground_pressed: str | None = None
    """Foreground pressed state on primary-colored backgrounds."""
    primary_color_foreground_disabled: str | None = None
    """Foreground disabled state on primary-colored backgrounds."""

    primary_alternative_color: str | None = None
    """Alternative accent for selected checkboxes and active list items."""
    primary_alternative_color_hovered: str | None = None
    """Hover state for alternative primary elements."""
    primary_alternative_color_pressed: str | None = None
    """Pressed state for alternative primary elements."""
    primary_alternative_color_disabled: str | None = None
    """Disabled state for alternative primary elements."""

    secondary_color: str | None = None
    """Foreground color for regular text, labels, menu text, and tooltips."""
    secondary_color_hovered: str | None = None
    """Hover state for secondary-colored text elements."""
    secondary_color_pressed: str | None = None
    """Pressed state for secondary-colored text elements."""
    secondary_color_disabled: str | None = None
    """Disabled state for text and placeholder text."""

    secondary_color_foreground: str | None = None
    """Text/icon color on secondary (dark) backgrounds for contrast."""
    secondary_color_foreground_hovered: str | None = None
    """Foreground hover state on secondary backgrounds."""
    secondary_color_foreground_pressed: str | None = None
    """Foreground pressed state on secondary backgrounds."""
    secondary_color_foreground_disabled: str | None = None
    """Foreground disabled state on secondary backgrounds."""

    secondary_alternative_color: str | None = None
    """Lighter color for captions, labels, and menu shortcut text."""
    secondary_alternative_color_hovered: str | None = None
    """Hover state for alternative secondary elements."""
    secondary_alternative_color_pressed: str | None = None
    """Pressed state for alternative secondary elements."""
    secondary_alternative_color_disabled: str | None = None
    """Disabled state for alternative secondary elements."""

    status_color_success: str | None = None
    """Success state color for status indicators and buttons."""
    status_color_success_hovered: str | None = None
    """Hover state for success-colored elements."""
    status_color_success_pressed: str | None = None
    """Pressed state for success-colored elements."""
    status_color_success_disabled: str | None = None
    """Disabled state for success-colored elements."""

    status_color_info: str | None = None
    """Info state color for status indicators and buttons."""
    status_color_info_hovered: str | None = None
    """Hover state for info-colored elements."""
    status_color_info_pressed: str | None = None
    """Pressed state for info-colored elements."""
    status_color_info_disabled: str | None = None
    """Disabled state for info-colored elements."""

    status_color_warning: str | None = None
    """Warning state color for status indicators and buttons."""
    status_color_warning_hovered: str | None = None
    """Hover state for warning-colored elements."""
    status_color_warning_pressed: str | None = None
    """Pressed state for warning-colored elements."""
    status_color_warning_disabled: str | None = None
    """Disabled state for warning-colored elements."""

    status_color_error: str | None = None
    """Error state color for status indicators and buttons."""
    status_color_error_hovered: str | None = None
    """Hover state for error-colored elements."""
    status_color_error_pressed: str | None = None
    """Pressed state for error-colored elements."""
    status_color_error_disabled: str | None = None
    """Disabled state for error-colored elements."""

    status_color_foreground: str | None = None
    """Text/icon color on status-colored backgrounds."""
    status_color_foreground_hovered: str | None = None
    """Foreground hover state on status-colored backgrounds."""
    status_color_foreground_pressed: str | None = None
    """Foreground pressed state on status-colored backgrounds."""
    status_color_foreground_disabled: str | None = None
    """Foreground disabled state on status-colored backgrounds."""

    shadow_color1: str | None = None
    """Lightest shadow layer for subtle depth effects."""
    shadow_color2: str | None = None
    """Medium shadow layer for moderate depth effects."""
    shadow_color3: str | None = None
    """Darkest shadow layer for strong depth effects."""

    border_color: str | None = None
    """Default border color for controls (text fields, combo boxes)."""
    border_color_hovered: str | None = None
    """Hover state for control borders."""
    border_color_pressed: str | None = None
    """Pressed state for control borders."""
    border_color_disabled: str | None = None
    """Disabled state for control borders."""

    semi_transparent_color1: str | None = None
    """Lightest transparency overlay for subtle selection highlights."""
    semi_transparent_color2: str | None = None
    """Light transparency overlay for hover effects."""
    semi_transparent_color3: str | None = None
    """Medium transparency overlay for active selections."""
    semi_transparent_color4: str | None = None
    """Strongest transparency overlay for emphasized selections."""

    use_system_fonts: bool | None = None
    """Use OS system fonts instead of bundled Inter/Roboto fonts."""

    font_size: int | None = None
    """Base font size in pixels for regular text."""
    font_size_monospace: int | None = None
    """Font size in pixels for monospace/code text."""
    font_size_h1: int | None = None
    """Font size in pixels for h1 headings."""
    font_size_h2: int | None = None
    """Font size in pixels for h2 headings."""
    font_size_h3: int | None = None
    """Font size in pixels for h3 headings."""
    font_size_h4: int | None = None
    """Font size in pixels for h4 headings."""
    font_size_h5: int | None = None
    """Font size in pixels for h5 headings."""
    font_size_s1: int | None = None
    """Font size in pixels for small/caption text."""

    animation_duration: int | None = None
    """Duration in ms for standard color/state transitions."""
    focus_animation_duration: int | None = None
    """Duration in ms for focus border animations."""
    slider_animation_duration: int | None = None
    """Duration in ms for slider handle interactions."""

    border_radius: float | None = None
    """Default corner radius in pixels for buttons and containers."""
    check_box_border_radius: float | None = None
    """Corner radius in pixels for checkbox indicators."""
    menu_item_border_radius: float | None = None
    """Corner radius in pixels for menu item backgrounds."""
    menu_bar_item_border_radius: float | None = None
    """Corner radius in pixels for menu bar items."""
    border_width: int | None = None
    """Standard border thickness in pixels."""

    control_height_large: int | None = None
    """Height in pixels for large controls (prominent buttons/inputs)."""
    control_height_medium: int | None = None
    """Height in pixels for standard controls."""
    control_height_small: int | None = None
    """Height in pixels for compact controls."""
    control_default_width: int | None = None
    """Default width in pixels for combo boxes and similar controls."""

    dial_mark_length: int | None = None
    """Length in pixels of major tick marks on dial widgets."""
    dial_mark_thickness: int | None = None
    """Thickness in pixels of major tick marks on dial widgets."""
    dial_tick_length: int | None = None
    """Length in pixels of minor tick marks on dial widgets."""
    dial_tick_spacing: int | None = None
    """Spacing in pixels between dial tick marks."""
    dial_groove_thickness: int | None = None
    """Thickness in pixels of the dial groove track."""

    focus_border_width: int | None = None
    """Border thickness in pixels for focus ring indicators."""

    icon_extent: int | None = None
    """Base icon dimension in pixels (icons are square)."""

    slider_tick_size: int | None = None
    """Height in pixels of slider tick marks."""
    slider_tick_spacing: int | None = None
    """Horizontal spacing in pixels between slider ticks."""
    slider_tick_thickness: int | None = None
    """Width in pixels of slider tick marks."""
    slider_groove_height: int | None = None
    """Height in pixels of the slider track/groove."""

    progress_bar_groove_height: int | None = None
    """Height in pixels of the progress bar track."""
    spacing: int | None = None
    """Standard spacing unit in pixels used for padding and margins."""

    scroll_bar_thickness_full: int | None = None
    """Width in pixels of the scrollbar when fully visible."""
    scroll_bar_thickness_small: int | None = None
    """Width in pixels of the compact/mini scrollbar."""
    scroll_bar_margin: int | None = None
    """Margin in pixels between scrollbar and container edge."""

    tab_bar_padding_top: int | None = None
    """Top padding in pixels for tab bar items."""
    tab_bar_tab_max_width: int | None = None
    """Maximum tab width in pixels (0 = no limit)."""
    tab_bar_tab_min_width: int | None = None
    """Minimum tab width in pixels (0 = no minimum)."""

    def asdict(self) -> ThemeDict:
        d: dict[str, Any] = {"meta": self.meta.asdict()}
        for f in fields(self):
            if f.name == "meta":
                continue
            val = getattr(self, f.name)
            if val is not None:
                d[f.name] = val
        return d  # type: ignore[return-value]

    def to_qlementine(self) -> Qlementine.Theme:
        return make_qlementine_theme(self.asdict())


@overload
def make_qlementine_theme(theme: ThemeDict | Theme, /) -> Qlementine.Theme: ...
@overload
def make_qlementine_theme(
    theme: ThemeDict | Theme | None = None, /, **kwargs: Unpack[ThemeDict]
) -> Qlementine.Theme: ...
def make_qlementine_theme(
    theme: ThemeDict | Theme | None = None, /, **kwargs: Any
) -> Qlementine.Theme:
    """Convert a ThemeDict or Theme configuration into a Qlementine.Theme instance."""
    from carina import Qlementine
    from carina._qt.QtCore import QJsonDocument

    if isinstance(theme, Theme):
        theme = theme.asdict()

    camel_dict = _to_camel_case_dict({**(theme or {}), **kwargs})
    json_doc = QJsonDocument.fromVariant(camel_dict)
    return Qlementine.Theme.fromJsonDoc(json_doc)


def _to_camel_case_dict(d: Mapping[str, Any]) -> dict[str, Any]:
    """Recursively convert all dict keys from snake_case to camelCase."""
    out: dict[str, Any] = {}
    for key, value in d.items():
        part0, *rest = key.split("_")
        camel_key = part0 + "".join(p.capitalize() for p in rest)
        if isinstance(value, dict):
            value = _to_camel_case_dict(value)
        out[camel_key] = value
    return out
