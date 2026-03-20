"""
Complete Qlementine ThemeDict definitions for 12 modern design systems.

Each theme maps the full ~100-field ThemeDict schema, with geometry choices
that reflect the "spirit" of the originating design system.

Usage:
    from themes import THEMES, THEME_NAMES
    theme = THEMES["catppuccin_mocha"]
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Color utilities for computing interaction states
# ---------------------------------------------------------------------------
def _hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _rgb_to_hex(r: int, g: int, b: int) -> str:
    return (
        f"#{max(0, min(255, r)):02X}{max(0, min(255, g)):02X}{max(0, min(255, b)):02X}"
    )


def _blend(base: str, overlay: str, alpha: float) -> str:
    """Alpha-blend overlay onto base at given opacity."""
    br, bg, bb = _hex_to_rgb(base)
    or_, og, ob = _hex_to_rgb(overlay)
    return _rgb_to_hex(
        int(br * (1 - alpha) + or_ * alpha),
        int(bg * (1 - alpha) + og * alpha),
        int(bb * (1 - alpha) + ob * alpha),
    )


def _lighten(color: str, amount: float) -> str:
    """Lighten by blending with white."""
    return _blend(color, "#FFFFFF", amount)


def _darken(color: str, amount: float) -> str:
    """Darken by blending with black."""
    return _blend(color, "#000000", amount)


def _with_alpha(color: str, alpha: float) -> str:
    """Return hex color with alpha byte appended (Qt-compatible #AARRGGBB or #RRGGBBAA)."""
    h = color.lstrip("#")
    a = max(0, min(255, int(alpha * 255)))
    return f"#{h}{a:02X}"


def _hover(color: str, bg: str = "#FFFFFF") -> str:
    """M3-style hover: 8% content color overlay."""
    return _blend(color, bg, 0.08)


def _pressed(color: str, bg: str = "#FFFFFF") -> str:
    """M3-style press: 12% content color overlay."""
    return _blend(color, bg, 0.12)


def _disabled_color(color: str) -> str:
    """Disabled: 38% opacity (appended as alpha hex)."""
    return _with_alpha(color, 0.38)


# ---------------------------------------------------------------------------
# State variant helpers — generate the 4-state dict for a color
# ---------------------------------------------------------------------------
def _primary_states(base: str, bg: str) -> dict:
    """Primary color states: hover lightens, press darkens, disabled fades."""
    return {
        "primary_color": base,
        "primary_color_hovered": _lighten(base, 0.10),
        "primary_color_pressed": _darken(base, 0.12),
        "primary_color_disabled": _disabled_color(base),
    }


def _primary_fg_states(base: str) -> dict:
    return {
        "primary_color_foreground": base,
        "primary_color_foreground_hovered": base,
        "primary_color_foreground_pressed": base,
        "primary_color_foreground_disabled": _disabled_color(base),
    }


def _primary_alt_states(base: str) -> dict:
    return {
        "primary_alternative_color": base,
        "primary_alternative_color_hovered": _lighten(base, 0.10),
        "primary_alternative_color_pressed": _darken(base, 0.12),
        "primary_alternative_color_disabled": _disabled_color(base),
    }


def _secondary_states(base: str) -> dict:
    """Secondary = main text color."""
    return {
        "secondary_color": base,
        "secondary_color_hovered": _lighten(base, 0.05),
        "secondary_color_pressed": _darken(base, 0.05),
        "secondary_color_disabled": _disabled_color(base),
    }


def _secondary_fg_states(base: str) -> dict:
    """Text on secondary (dark text) backgrounds."""
    return {
        "secondary_color_foreground": base,
        "secondary_color_foreground_hovered": base,
        "secondary_color_foreground_pressed": base,
        "secondary_color_foreground_disabled": _disabled_color(base),
    }


def _secondary_alt_states(base: str) -> dict:
    """Muted/caption text."""
    return {
        "secondary_alternative_color": base,
        "secondary_alternative_color_hovered": _lighten(base, 0.08),
        "secondary_alternative_color_pressed": _darken(base, 0.05),
        "secondary_alternative_color_disabled": _disabled_color(base),
    }


def _neutral_states(base: str) -> dict:
    return {
        "neutral_color": base,
        "neutral_color_hovered": _lighten(base, 0.08),
        "neutral_color_pressed": _darken(base, 0.06),
        "neutral_color_disabled": _disabled_color(base),
    }


def _border_states(base: str) -> dict:
    return {
        "border_color": base,
        "border_color_hovered": _lighten(base, 0.12),
        "border_color_pressed": _lighten(base, 0.06),
        "border_color_disabled": _disabled_color(base),
    }


def _status_states(success: str, info: str, warning: str, error: str) -> dict:
    return {
        "status_color_success": success,
        "status_color_success_hovered": _lighten(success, 0.10),
        "status_color_success_pressed": _darken(success, 0.10),
        "status_color_success_disabled": _disabled_color(success),
        "status_color_info": info,
        "status_color_info_hovered": _lighten(info, 0.10),
        "status_color_info_pressed": _darken(info, 0.10),
        "status_color_info_disabled": _disabled_color(info),
        "status_color_warning": warning,
        "status_color_warning_hovered": _lighten(warning, 0.10),
        "status_color_warning_pressed": _darken(warning, 0.10),
        "status_color_warning_disabled": _disabled_color(warning),
        "status_color_error": error,
        "status_color_error_hovered": _lighten(error, 0.10),
        "status_color_error_pressed": _darken(error, 0.10),
        "status_color_error_disabled": _disabled_color(error),
    }


def _status_fg_states(base: str) -> dict:
    """Foreground on status-colored backgrounds (usually white or dark)."""
    return {
        "status_color_foreground": base,
        "status_color_foreground_hovered": base,
        "status_color_foreground_pressed": base,
        "status_color_foreground_disabled": _disabled_color(base),
    }


# ---------------------------------------------------------------------------
# Geometry presets
# ---------------------------------------------------------------------------

GEOMETRY_SHARP: dict = {
    # Typography — compact, developer-oriented
    "use_system_fonts": False,
    "font_size": 13,
    "font_size_monospace": 13,
    "font_size_h1": 26,
    "font_size_h2": 22,
    "font_size_h3": 18,
    "font_size_h4": 15,
    "font_size_h5": 13,
    "font_size_s1": 11,
    # Animation — snappy
    "animation_duration": 100,
    "focus_animation_duration": 150,
    "slider_animation_duration": 100,
    # Radii — minimal
    "border_radius": 4.0,
    "check_box_border_radius": 2.0,
    "menu_item_border_radius": 2.0,
    "menu_bar_item_border_radius": 2.0,
    "border_width": 1,
    # Control sizes — compact
    "control_height_large": 36,
    "control_height_medium": 28,
    "control_height_small": 22,
    "control_default_width": 120,
    # Dial — tight
    "dial_mark_length": 8,
    "dial_mark_thickness": 2,
    "dial_tick_length": 4,
    "dial_tick_spacing": 4,
    "dial_groove_thickness": 3,
    # Focus
    "focus_border_width": 2,
    # Icons
    "icon_extent": 16,
    # Slider — compact
    "slider_tick_size": 4,
    "slider_tick_spacing": 2,
    "slider_tick_thickness": 1,
    "slider_groove_height": 3,
    # Progress
    "progress_bar_groove_height": 4,
    # Spacing — tight
    "spacing": 6,
    # Scrollbar — thin
    "scroll_bar_thickness_full": 10,
    "scroll_bar_thickness_small": 4,
    "scroll_bar_margin": 1,
    # Tab bar
    "tab_bar_padding_top": 4,
    "tab_bar_tab_max_width": 0,
    "tab_bar_tab_min_width": 0,
}

GEOMETRY_SOFT: dict = {
    # Typography — comfortable, consumer-oriented
    "use_system_fonts": True,
    "font_size": 14,
    "font_size_monospace": 13,
    "font_size_h1": 28,
    "font_size_h2": 24,
    "font_size_h3": 20,
    "font_size_h4": 16,
    "font_size_h5": 14,
    "font_size_s1": 11,
    # Animation — smooth
    "animation_duration": 200,
    "focus_animation_duration": 250,
    "slider_animation_duration": 200,
    # Radii — generous
    "border_radius": 8.0,
    "check_box_border_radius": 4.0,
    "menu_item_border_radius": 6.0,
    "menu_bar_item_border_radius": 6.0,
    "border_width": 1,
    # Control sizes — comfortable
    "control_height_large": 44,
    "control_height_medium": 36,
    "control_height_small": 28,
    "control_default_width": 160,
    # Dial — standard
    "dial_mark_length": 10,
    "dial_mark_thickness": 2,
    "dial_tick_length": 5,
    "dial_tick_spacing": 5,
    "dial_groove_thickness": 4,
    # Focus
    "focus_border_width": 2,
    # Icons
    "icon_extent": 18,
    # Slider — standard
    "slider_tick_size": 5,
    "slider_tick_spacing": 3,
    "slider_tick_thickness": 1,
    "slider_groove_height": 4,
    # Progress
    "progress_bar_groove_height": 6,
    # Spacing — comfortable
    "spacing": 8,
    # Scrollbar — macOS-like
    "scroll_bar_thickness_full": 12,
    "scroll_bar_thickness_small": 6,
    "scroll_bar_margin": 2,
    # Tab bar
    "tab_bar_padding_top": 6,
    "tab_bar_tab_max_width": 0,
    "tab_bar_tab_min_width": 0,
}

GEOMETRY_MEDIUM: dict = {
    # Typography — balanced
    "use_system_fonts": False,
    "font_size": 13,
    "font_size_monospace": 13,
    "font_size_h1": 26,
    "font_size_h2": 22,
    "font_size_h3": 18,
    "font_size_h4": 15,
    "font_size_h5": 13,
    "font_size_s1": 11,
    # Animation — moderate
    "animation_duration": 150,
    "focus_animation_duration": 200,
    "slider_animation_duration": 150,
    # Radii — moderate
    "border_radius": 6.0,
    "check_box_border_radius": 3.0,
    "menu_item_border_radius": 4.0,
    "menu_bar_item_border_radius": 4.0,
    "border_width": 1,
    # Control sizes — standard
    "control_height_large": 40,
    "control_height_medium": 32,
    "control_height_small": 24,
    "control_default_width": 140,
    # Dial
    "dial_mark_length": 8,
    "dial_mark_thickness": 2,
    "dial_tick_length": 4,
    "dial_tick_spacing": 4,
    "dial_groove_thickness": 3,
    # Focus
    "focus_border_width": 2,
    # Icons
    "icon_extent": 16,
    # Slider
    "slider_tick_size": 4,
    "slider_tick_spacing": 2,
    "slider_tick_thickness": 1,
    "slider_groove_height": 4,
    # Progress
    "progress_bar_groove_height": 4,
    # Spacing
    "spacing": 7,
    # Scrollbar
    "scroll_bar_thickness_full": 11,
    "scroll_bar_thickness_small": 5,
    "scroll_bar_margin": 2,
    # Tab bar
    "tab_bar_padding_top": 5,
    "tab_bar_tab_max_width": 0,
    "tab_bar_tab_min_width": 0,
}


# ---------------------------------------------------------------------------
# Theme builder
# ---------------------------------------------------------------------------
def _build_theme(
    meta: dict,
    backgrounds: dict,
    primary: str,
    primary_fg: str,
    primary_alt: str,
    text_primary: str,
    text_secondary: str,
    text_on_dark_bg: str,
    neutral_fill: str,
    focus: str,
    border: str,
    success: str,
    info: str,
    warning: str,
    error: str,
    status_fg: str,
    shadow_base: str,
    semi_base: str,
    geometry: dict,
) -> dict:
    """Assemble a full ThemeDict from high-level palette choices."""
    theme: dict = {}
    theme["meta"] = meta

    # Backgrounds
    theme["background_color_main1"] = backgrounds["main1"]
    theme["background_color_main2"] = backgrounds["main2"]
    theme["background_color_main3"] = backgrounds["main3"]
    theme["background_color_main4"] = backgrounds["main4"]
    theme["background_color_workspace"] = backgrounds.get(
        "workspace", backgrounds["main1"]
    )
    theme["background_color_tab_bar"] = backgrounds.get("tab_bar", backgrounds["main2"])

    # Neutral (separator/button fills)
    theme.update(_neutral_states(neutral_fill))

    # Focus ring
    theme["focus_color"] = focus

    # Primary accent
    theme.update(_primary_states(primary, backgrounds["main3"]))
    theme.update(_primary_fg_states(primary_fg))

    # Primary alternative (checkboxes, active list items)
    theme.update(_primary_alt_states(primary_alt))

    # Secondary = main text color
    theme.update(_secondary_states(text_primary))

    # Secondary foreground = text on dark/secondary backgrounds
    theme.update(_secondary_fg_states(text_on_dark_bg))

    # Secondary alternative = muted/caption text
    theme.update(_secondary_alt_states(text_secondary))

    # Status colors
    theme.update(_status_states(success, info, warning, error))
    theme.update(_status_fg_states(status_fg))

    # Shadows (3 graduated layers)
    sr, sg, sb = _hex_to_rgb(shadow_base)
    theme["shadow_color1"] = f"#{sr:02X}{sg:02X}{sb:02X}18"  # ~10%
    theme["shadow_color2"] = f"#{sr:02X}{sg:02X}{sb:02X}30"  # ~19%
    theme["shadow_color3"] = f"#{sr:02X}{sg:02X}{sb:02X}60"  # ~38%

    # Borders
    theme.update(_border_states(border))

    # Semi-transparent overlays (using primary or white tints)
    tr, tg, tb = _hex_to_rgb(semi_base)
    theme["semi_transparent_color1"] = f"#{tr:02X}{tg:02X}{tb:02X}0D"  # ~5%
    theme["semi_transparent_color2"] = f"#{tr:02X}{tg:02X}{tb:02X}1A"  # ~10%
    theme["semi_transparent_color3"] = f"#{tr:02X}{tg:02X}{tb:02X}33"  # ~20%
    theme["semi_transparent_color4"] = f"#{tr:02X}{tg:02X}{tb:02X}4D"  # ~30%

    # Geometry
    theme.update(geometry)

    return theme


# ===================================================================
# THEME DEFINITIONS
# ===================================================================

# -------------------------------------------------------------------
# 1. Material Design 3 — Dark baseline
#    Cool purple tint. Sharp/material geometry.
#    As Google's own team would ship it.
# -------------------------------------------------------------------
MATERIAL_DESIGN_3 = _build_theme(
    meta={
        "name": "Material Design 3 Dark",
        "version": "1.0.0",
        "author": "Google (adapted)",
    },
    backgrounds={
        "main1": "#0F0D13",  # surface-container-lowest (tone 4)
        "main2": "#1D1B20",  # surface-container-low (tone 10)
        "main3": "#211F26",  # surface-container (tone 12)
        "main4": "#36343B",  # surface-container-high (tone 17)
        "workspace": "#0F0D13",
        "tab_bar": "#1D1B20",
    },
    primary="#D0BCFF",  # M3 primary (pastel purple)
    primary_fg="#381E72",  # on-primary (deep purple)
    primary_alt="#CCC2DC",  # secondary (lavender)
    text_primary="#E6E0E9",  # on-surface
    text_secondary="#CAC4D0",  # on-surface-variant
    text_on_dark_bg="#E6E0E9",
    neutral_fill="#49454F",  # surface-container-highest / outline-variant
    focus="#D0BCFF",
    border="#49454F",  # outline-variant
    success="#A8DAB5",
    info="#D0BCFF",
    warning="#FFB4AB",
    error="#F2B8B5",  # M3 error container
    status_fg="#1D1B20",
    shadow_base="#000000",
    semi_base="#D0BCFF",  # primary tint for selections
    geometry={
        **GEOMETRY_SHARP,
        # M3-specific overrides: slightly larger radii than pure sharp
        "border_radius": 8.0,  # M3 uses 8dp for buttons
        "check_box_border_radius": 2.0,
        "menu_item_border_radius": 4.0,
        "menu_bar_item_border_radius": 4.0,
        "control_height_large": 40,  # M3 FAB = 56, button = 40
        "control_height_medium": 32,
        "control_height_small": 24,
        "animation_duration": 200,  # M3 standard: 200ms
        "focus_animation_duration": 200,
    },
)

# -------------------------------------------------------------------
# 2. Catppuccin Mocha — Darkest flavor
#    Warm blue-violet tint. Soft, rounded geometry.
#    The coziest theme — generous spacing, smooth animations.
# -------------------------------------------------------------------
CATPPUCCIN_MOCHA = _build_theme(
    meta={
        "name": "Catppuccin Mocha",
        "version": "1.0.0",
        "author": "Catppuccin (adapted)",
    },
    backgrounds={
        "main1": "#11111B",  # crust
        "main2": "#181825",  # mantle
        "main3": "#1E1E2E",  # base
        "main4": "#313244",  # surface0
        "workspace": "#11111B",
        "tab_bar": "#181825",
    },
    primary="#89B4FA",  # blue
    primary_fg="#1E1E2E",  # base (dark on bright)
    primary_alt="#CBA6F7",  # mauve — checkboxes, active items
    text_primary="#CDD6F4",  # text
    text_secondary="#A6ADC8",  # subtext0
    text_on_dark_bg="#CDD6F4",
    neutral_fill="#45475A",  # surface1
    focus="#89B4FA",  # blue
    border="#45475A",  # surface1
    success="#A6E3A1",  # green
    info="#89DCEB",  # sky
    warning="#F9E2AF",  # yellow
    error="#F38BA8",  # red
    status_fg="#1E1E2E",
    shadow_base="#000000",
    semi_base="#89B4FA",  # blue tint for selections
    geometry={
        **GEOMETRY_SOFT,
        "border_radius": 10.0,  # catppuccin UIs tend to be very rounded
        "check_box_border_radius": 4.0,
        "menu_item_border_radius": 8.0,
        "menu_bar_item_border_radius": 6.0,
    },
)

# -------------------------------------------------------------------
# 3. Catppuccin Macchiato — Medium-dark flavor
#    Slightly warmer/lighter. Soft geometry.
# -------------------------------------------------------------------
CATPPUCCIN_MACCHIATO = _build_theme(
    meta={
        "name": "Catppuccin Macchiato",
        "version": "1.0.0",
        "author": "Catppuccin (adapted)",
    },
    backgrounds={
        "main1": "#181926",  # crust
        "main2": "#1E2030",  # mantle
        "main3": "#24273A",  # base
        "main4": "#363A4F",  # surface0
        "workspace": "#181926",
        "tab_bar": "#1E2030",
    },
    primary="#8AADF4",
    primary_fg="#24273A",
    primary_alt="#C6A0F6",  # mauve
    text_primary="#CAD3F5",
    text_secondary="#A5ADCB",
    text_on_dark_bg="#CAD3F5",
    neutral_fill="#494D64",  # surface1
    focus="#8AADF4",
    border="#494D64",
    success="#A6DA95",
    info="#91D7E3",
    warning="#EED49F",
    error="#ED8796",
    status_fg="#24273A",
    shadow_base="#000000",
    semi_base="#8AADF4",
    geometry={
        **GEOMETRY_SOFT,
        "border_radius": 10.0,
        "check_box_border_radius": 4.0,
        "menu_item_border_radius": 8.0,
        "menu_bar_item_border_radius": 6.0,
    },
)

# -------------------------------------------------------------------
# 4. Nord — Arctic blue
#    Cool teal-blue neutrals. Medium geometry.
#    Restrained, coherent, not too sharp not too soft.
# -------------------------------------------------------------------
NORD = _build_theme(
    meta={"name": "Nord", "version": "1.0.0", "author": "Arctic Ice Studio (adapted)"},
    backgrounds={
        "main1": "#2E3440",  # nord0 polar night
        "main2": "#2E3440",  # nord0 (nord uses same bg for most panels)
        "main3": "#3B4252",  # nord1
        "main4": "#434C5E",  # nord2
        "workspace": "#2E3440",
        "tab_bar": "#2E3440",
    },
    primary="#88C0D0",  # frost[1] — signature teal
    primary_fg="#2E3440",
    primary_alt="#81A1C1",  # frost[2] — steel blue for checkboxes
    text_primary="#ECEFF4",  # snow storm 2
    text_secondary="#D8DEE9",  # snow storm 0
    text_on_dark_bg="#ECEFF4",
    neutral_fill="#4C566A",  # nord3
    focus="#88C0D0",
    border="#4C566A",  # nord3
    success="#A3BE8C",  # aurora green
    info="#88C0D0",  # frost teal
    warning="#EBCB8B",  # aurora yellow
    error="#BF616A",  # aurora red
    status_fg="#2E3440",
    shadow_base="#000000",
    semi_base="#88C0D0",  # frost tint
    geometry={
        **GEOMETRY_MEDIUM,
        "border_radius": 4.0,  # Nord UIs tend to be clean and minimal
        "check_box_border_radius": 2.0,
        "menu_item_border_radius": 4.0,
        "menu_bar_item_border_radius": 3.0,
    },
)

# -------------------------------------------------------------------
# 5. Dracula — Saturated neon purple
#    High-contrast, saturated accents. Medium-sharp geometry.
#    Bold, opinionated, slightly playful.
# -------------------------------------------------------------------
DRACULA = _build_theme(
    meta={"name": "Dracula", "version": "1.0.0", "author": "Zeno Rocha (adapted)"},
    backgrounds={
        "main1": "#191A21",
        "main2": "#21222C",
        "main3": "#282A36",  # background
        "main4": "#44475A",  # current line
        "workspace": "#191A21",
        "tab_bar": "#21222C",
    },
    primary="#BD93F9",  # purple — THE dracula color
    primary_fg="#282A36",
    primary_alt="#FF79C6",  # pink — for checkboxes/active
    text_primary="#F8F8F2",  # foreground
    text_secondary="#6272A4",  # comment
    text_on_dark_bg="#F8F8F2",
    neutral_fill="#44475A",  # current line
    focus="#BD93F9",
    border="#44475A",
    success="#50FA7B",
    info="#8BE9FD",  # cyan
    warning="#F1FA8C",  # yellow
    error="#FF5555",
    status_fg="#282A36",
    shadow_base="#000000",
    semi_base="#BD93F9",
    geometry={
        **GEOMETRY_MEDIUM,
        "border_radius": 4.0,
        "check_box_border_radius": 3.0,
        "menu_item_border_radius": 4.0,
        "animation_duration": 120,  # Dracula feels snappy
    },
)

# -------------------------------------------------------------------
# 6. shadcn/ui — Pure achromatic neutral
#    Zero-hue. Soft/modern geometry.
#    The blank canvas — no opinion on hue, strong opinion on spacing.
# -------------------------------------------------------------------
SHADCN_NEUTRAL = _build_theme(
    meta={
        "name": "shadcn/ui Neutral Dark",
        "version": "1.0.0",
        "author": "shadcn (adapted)",
    },
    backgrounds={
        "main1": "#09090B",  # zinc-950
        "main2": "#18181B",  # zinc-900
        "main3": "#27272A",  # zinc-800
        "main4": "#3F3F46",  # zinc-700
        "workspace": "#09090B",
        "tab_bar": "#18181B",
    },
    primary="#FAFAFA",  # shadcn dark uses white-ish primary
    primary_fg="#18181B",
    primary_alt="#A1A1AA",  # zinc-400
    text_primary="#FAFAFA",  # zinc-50
    text_secondary="#A1A1AA",  # zinc-400
    text_on_dark_bg="#FAFAFA",
    neutral_fill="#3F3F46",  # zinc-700
    focus="#A1A1AA",  # zinc-400 (muted ring)
    border="#27272A",  # zinc-800
    success="#4ADE80",  # green-400
    info="#60A5FA",  # blue-400
    warning="#FBBF24",  # amber-400
    error="#F87171",  # red-400
    status_fg="#09090B",
    shadow_base="#000000",
    semi_base="#FAFAFA",  # white tints
    geometry={
        **GEOMETRY_SOFT,
        "border_radius": 8.0,  # shadcn default ~0.5rem
        "check_box_border_radius": 4.0,
        "menu_item_border_radius": 4.0,
        "menu_bar_item_border_radius": 6.0,
        "spacing": 8,
    },
)

# -------------------------------------------------------------------
# 7. GitHub Dark (Primer)
#    Deep blue-black. Sharp/dense developer geometry.
#    Green primary (the GitHub button), very functional.
# -------------------------------------------------------------------
GITHUB_DARK = _build_theme(
    meta={
        "name": "GitHub Dark",
        "version": "1.0.0",
        "author": "GitHub/Primer (adapted)",
    },
    backgrounds={
        "main1": "#010409",
        "main2": "#0D1117",  # default bg
        "main3": "#161B22",  # canvas-subtle
        "main4": "#21262D",  # canvas-inset
        "workspace": "#010409",
        "tab_bar": "#0D1117",
    },
    primary="#238636",  # green (the button color)
    primary_fg="#FFFFFF",
    primary_alt="#1F6FEB",  # blue accent (links, focus)
    text_primary="#E6EDF3",  # fg-default
    text_secondary="#7D8590",  # fg-muted
    text_on_dark_bg="#E6EDF3",
    neutral_fill="#21262D",  # btn-bg
    focus="#1F6FEB",  # blue accent
    border="#30363D",  # border-default
    success="#3FB950",
    info="#4493F8",
    warning="#D29922",
    error="#F85149",
    status_fg="#FFFFFF",
    shadow_base="#010409",
    semi_base="#388BFD",  # blue tint for selections
    geometry={
        **GEOMETRY_SHARP,
        "border_radius": 6.0,  # GitHub uses 6px
        "check_box_border_radius": 3.0,
        "menu_item_border_radius": 6.0,
        "menu_bar_item_border_radius": 6.0,
        "control_height_medium": 32,
        "control_height_small": 24,
        "spacing": 8,
    },
)

# -------------------------------------------------------------------
# 8. Tokyo Night — Deep indigo
#    The most "blue" dark theme. Soft, atmospheric geometry.
#    Neon-inspired but elegant.
# -------------------------------------------------------------------
TOKYO_NIGHT = _build_theme(
    meta={"name": "Tokyo Night", "version": "1.0.0", "author": "enkia (adapted)"},
    backgrounds={
        "main1": "#16161E",  # terminal bg (deeper)
        "main2": "#1A1B26",  # bg
        "main3": "#1F2335",  # bg_highlight
        "main4": "#292E42",  # bg_visual
        "workspace": "#16161E",
        "tab_bar": "#1A1B26",
    },
    primary="#7AA2F7",  # blue
    primary_fg="#1A1B26",
    primary_alt="#BB9AF7",  # magenta/purple
    text_primary="#C0CAF5",  # fg
    text_secondary="#565F89",  # comment
    text_on_dark_bg="#C0CAF5",
    neutral_fill="#3B4261",  # bg_highlight border
    focus="#7AA2F7",
    border="#3B4261",
    success="#9ECE6A",  # green
    info="#7DCFFF",  # cyan
    warning="#E0AF68",  # yellow
    error="#F7768E",  # red
    status_fg="#1A1B26",
    shadow_base="#000000",
    semi_base="#7AA2F7",
    geometry={
        **GEOMETRY_SOFT,
        "border_radius": 8.0,
        "check_box_border_radius": 4.0,
        "menu_item_border_radius": 6.0,
        "menu_bar_item_border_radius": 6.0,
        "animation_duration": 200,
    },
)

# -------------------------------------------------------------------
# 9. One Dark Pro — Warm blue-gray
#    THE classic Atom dark. Medium geometry.
#    Comfortable for code, not too sharp, not too bubbly.
# -------------------------------------------------------------------
ONE_DARK_PRO = _build_theme(
    meta={
        "name": "One Dark Pro",
        "version": "1.0.0",
        "author": "Atom/Binaryify (adapted)",
    },
    backgrounds={
        "main1": "#1B1D23",
        "main2": "#21252B",  # sidebar
        "main3": "#282C34",  # editor
        "main4": "#2C313A",  # highlight
        "workspace": "#1B1D23",
        "tab_bar": "#21252B",
    },
    primary="#61AFEF",  # blue
    primary_fg="#282C34",
    primary_alt="#C678DD",  # magenta/purple
    text_primary="#ABB2BF",  # fg
    text_secondary="#5C6370",  # comment
    text_on_dark_bg="#ABB2BF",
    neutral_fill="#3E4451",  # gutter
    focus="#528BFF",  # cursor/focus blue
    border="#3E4451",
    success="#98C379",
    info="#56B6C2",  # cyan
    warning="#E5C07B",
    error="#E06C75",
    status_fg="#282C34",
    shadow_base="#000000",
    semi_base="#61AFEF",
    geometry={
        **GEOMETRY_MEDIUM,
        "border_radius": 4.0,
        "check_box_border_radius": 2.0,
        "menu_item_border_radius": 3.0,
        "menu_bar_item_border_radius": 3.0,
    },
)

# -------------------------------------------------------------------
# 10. Gruvbox Dark — Warm retro
#     THE warm theme. Earthy tones, high saturation accents.
#     Slightly sharp/retro geometry — no frills.
# -------------------------------------------------------------------
GRUVBOX_DARK = _build_theme(
    meta={"name": "Gruvbox Dark", "version": "1.0.0", "author": "morhetz (adapted)"},
    backgrounds={
        "main1": "#1D2021",  # bg0_h (hard contrast)
        "main2": "#282828",  # bg0
        "main3": "#3C3836",  # bg1
        "main4": "#504945",  # bg2
        "workspace": "#1D2021",
        "tab_bar": "#282828",
    },
    primary="#83A598",  # aqua — less aggressive than bright green
    primary_fg="#282828",
    primary_alt="#D3869B",  # purple
    text_primary="#EBDBB2",  # fg1
    text_secondary="#A89984",  # gray (fg4)
    text_on_dark_bg="#EBDBB2",
    neutral_fill="#504945",  # bg2
    focus="#83A598",
    border="#504945",
    success="#B8BB26",  # bright green
    info="#83A598",  # aqua
    warning="#FABD2F",  # bright yellow
    error="#FB4934",  # bright red
    status_fg="#282828",
    shadow_base="#000000",
    semi_base="#EBDBB2",  # warm fg tint for selections
    geometry={
        **GEOMETRY_SHARP,
        "border_radius": 2.0,  # Gruvbox aesthetic is flat/minimal
        "check_box_border_radius": 1.0,
        "menu_item_border_radius": 2.0,
        "menu_bar_item_border_radius": 2.0,
        "font_size": 13,
        "animation_duration": 80,  # Retro = instant
        "focus_animation_duration": 100,
    },
)

# -------------------------------------------------------------------
# 11. Fluent Design 2 — Microsoft neutral
#     Pure zero-hue gray + Teams blue accent. Medium geometry.
#     Systematic, accessible, functional.
# -------------------------------------------------------------------
FLUENT_2 = _build_theme(
    meta={
        "name": "Fluent Design 2 Dark",
        "version": "1.0.0",
        "author": "Microsoft (adapted)",
    },
    backgrounds={
        "main1": "#0A0A0A",
        "main2": "#141414",
        "main3": "#1F1F1F",  # layer/card bg
        "main4": "#292929",
        "workspace": "#0A0A0A",
        "tab_bar": "#141414",
    },
    primary="#479EF5",  # brand blue (dark mode)
    primary_fg="#FFFFFF",
    primary_alt="#479EF5",  # Fluent uses same brand blue
    text_primary="#FFFFFF",
    text_secondary="#ADADAD",
    text_on_dark_bg="#FFFFFF",
    neutral_fill="#333333",  # subtle bg
    focus="#FFFFFF",  # Fluent uses white double-ring focus
    border="#666666",
    success="#54B054",
    info="#96C6FA",
    warning="#F98845",
    error="#DC626D",
    status_fg="#FFFFFF",
    shadow_base="#000000",
    semi_base="#479EF5",
    geometry={
        **GEOMETRY_MEDIUM,
        "border_radius": 4.0,  # Fluent 2 default: 4px
        "check_box_border_radius": 2.0,
        "menu_item_border_radius": 4.0,
        "menu_bar_item_border_radius": 4.0,
        "control_height_large": 40,
        "control_height_medium": 32,
        "control_height_small": 24,
        "focus_border_width": 2,  # Fluent double-ring: 1px black + 1px white
        "spacing": 8,
        "animation_duration": 167,  # Fluent standard: 167ms
        "focus_animation_duration": 167,
    },
)

# -------------------------------------------------------------------
# 12. Radix Slate + Blue — Methodical 12-step
#     Cool gray base, vivid blue accent. Soft/modern geometry.
#     Radix is shadcn's color foundation — very polished.
# -------------------------------------------------------------------
RADIX_SLATE_BLUE = _build_theme(
    meta={
        "name": "Radix Slate Blue",
        "version": "1.0.0",
        "author": "WorkOS/Radix (adapted)",
    },
    backgrounds={
        "main1": "#111113",  # slate-dark-1
        "main2": "#18191B",  # slate-dark-2
        "main3": "#212225",  # slate-dark-3
        "main4": "#272A2D",  # slate-dark-4
        "workspace": "#111113",
        "tab_bar": "#18191B",
    },
    primary="#0090FF",  # blue-dark-9 (solid accent)
    primary_fg="#FFFFFF",
    primary_alt="#3E63DD",  # indigo-dark-9
    text_primary="#EDEEF0",  # slate-dark-12
    text_secondary="#B0B4BA",  # slate-dark-11
    text_on_dark_bg="#EDEEF0",
    neutral_fill="#2E3135",  # slate-dark-5
    focus="#0090FF",
    border="#43484E",  # slate-dark-7
    success="#30A46C",  # green-dark-9
    info="#0090FF",
    warning="#F5D90A",  # yellow-dark-9
    error="#E5484D",  # red-dark-9
    status_fg="#FFFFFF",
    shadow_base="#000000",
    semi_base="#0090FF",
    geometry={
        **GEOMETRY_SOFT,
        "border_radius": 8.0,  # Radix Themes default radius
        "check_box_border_radius": 4.0,
        "menu_item_border_radius": 4.0,
        "menu_bar_item_border_radius": 6.0,
        "control_height_large": 44,
        "control_height_medium": 36,
        "control_height_small": 28,
    },
)

# -------------------------------------------------------------------
# BONUS 13. Warm Stone Dark — Custom warm neutral
#   Based on Tailwind Stone scale. A warm-but-not-brown dark theme
#   for users who want "slightly brownish" neutrals.
#   Paired with a warm amber accent.
# -------------------------------------------------------------------
WARM_STONE = _build_theme(
    meta={
        "name": "Warm Stone Dark",
        "version": "1.0.0",
        "author": "Custom (Tailwind Stone-based)",
    },
    backgrounds={
        "main1": "#0C0A09",  # stone-950
        "main2": "#1C1917",  # stone-900
        "main3": "#292524",  # stone-800
        "main4": "#44403C",  # stone-700
        "workspace": "#0C0A09",
        "tab_bar": "#1C1917",
    },
    primary="#F59E0B",  # amber-500
    primary_fg="#0C0A09",
    primary_alt="#D97706",  # amber-600
    text_primary="#FAFAF9",  # stone-50
    text_secondary="#A8A29E",  # stone-400
    text_on_dark_bg="#FAFAF9",
    neutral_fill="#44403C",  # stone-700
    focus="#F59E0B",
    border="#44403C",  # stone-700
    success="#4ADE80",  # green-400
    info="#38BDF8",  # sky-400
    warning="#FBBF24",  # amber-400
    error="#F87171",  # red-400
    status_fg="#0C0A09",
    shadow_base="#000000",
    semi_base="#F59E0B",  # warm amber tint
    geometry={
        **GEOMETRY_SOFT,
        "border_radius": 8.0,
        "check_box_border_radius": 4.0,
        "menu_item_border_radius": 6.0,
        "menu_bar_item_border_radius": 6.0,
    },
)

# -------------------------------------------------------------------
# BONUS 14. Slate Cool Dark — Custom cool blue-gray
#   Based on Tailwind Slate scale. The "blue tint" dark neutral
#   without a strong accent opinion — blue-gray everywhere.
# -------------------------------------------------------------------
SLATE_COOL = _build_theme(
    meta={
        "name": "Slate Cool Dark",
        "version": "1.0.0",
        "author": "Custom (Tailwind Slate-based)",
    },
    backgrounds={
        "main1": "#020617",  # slate-950
        "main2": "#0F172A",  # slate-900
        "main3": "#1E293B",  # slate-800
        "main4": "#334155",  # slate-700
        "workspace": "#020617",
        "tab_bar": "#0F172A",
    },
    primary="#3B82F6",  # blue-500
    primary_fg="#FFFFFF",
    primary_alt="#8B5CF6",  # violet-500
    text_primary="#F8FAFC",  # slate-50
    text_secondary="#94A3B8",  # slate-400
    text_on_dark_bg="#F8FAFC",
    neutral_fill="#334155",  # slate-700
    focus="#3B82F6",
    border="#334155",
    success="#4ADE80",
    info="#38BDF8",
    warning="#FBBF24",
    error="#F87171",
    status_fg="#020617",
    shadow_base="#000000",
    semi_base="#3B82F6",
    geometry={
        **GEOMETRY_MEDIUM,
        "border_radius": 6.0,
        "check_box_border_radius": 3.0,
        "menu_item_border_radius": 4.0,
        "menu_bar_item_border_radius": 4.0,
    },
)


# ===================================================================
# Registry
# ===================================================================

THEMES: dict[str, dict] = {
    "material_design_3": MATERIAL_DESIGN_3,
    "catppuccin_mocha": CATPPUCCIN_MOCHA,
    "catppuccin_macchiato": CATPPUCCIN_MACCHIATO,
    "nord": NORD,
    "dracula": DRACULA,
    "shadcn_neutral": SHADCN_NEUTRAL,
    "github_dark": GITHUB_DARK,
    "tokyo_night": TOKYO_NIGHT,
    "one_dark_pro": ONE_DARK_PRO,
    "gruvbox_dark": GRUVBOX_DARK,
    "fluent_2": FLUENT_2,
    "radix_slate_blue": RADIX_SLATE_BLUE,
    "warm_stone": WARM_STONE,
    "slate_cool": SLATE_COOL,
}

THEME_NAMES: list[str] = list(THEMES.keys())


# ===================================================================
# CLI: dump all themes as JSON
# ===================================================================
if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        for name in THEME_NAMES:
            meta = THEMES[name]["meta"]
            print(f"  {name:30s}  {meta['name']}")
        sys.exit(0)

    if len(sys.argv) > 1 and sys.argv[1] in THEMES:
        print(json.dumps(THEMES[sys.argv[1]], indent=2))
        sys.exit(0)

    # Dump all themes
    output = {name: theme for name, theme in THEMES.items()}
    print(json.dumps(output, indent=2))
