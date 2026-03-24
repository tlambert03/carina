"""Map Radix 12-step color scales to a Qlementine ThemeDict."""

from __future__ import annotations

from typing import TYPE_CHECKING

from carina._radix_generator import (
    DARK_BACKGROUNDS,
    GRAY_FOR_SCALE,
    LIGHT_BACKGROUND,
    get_accent_contrast,
    get_scale,
)

if TYPE_CHECKING:
    from carina._theme import ThemeDict

# ---------------------------------------------------------------------------
# Status scale names (fixed Radix scales for the 4 status groups)
# ---------------------------------------------------------------------------

STATUS_SCALES: dict[str, str] = {
    "success": "teal",
    "info": "blue",
    "warning": "amber",
    "error": "red",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _hex_with_alpha(hex_color: str, alpha: float) -> str:
    """Apply alpha (0-1) to a #rrggbb hex color, returning #rrggbbaa."""
    hex_color = hex_color.lstrip("#")
    aa = f"{round(alpha * 255):02x}"
    return f"#{hex_color[:6]}{aa}"


# ---------------------------------------------------------------------------
# Main mapper
# ---------------------------------------------------------------------------


def generate_qlementine_theme(
    accent: str,
    gray: str | None = None,
    appearance: str = "light",
    name: str = "Custom",
    author: str = "Generated",
    version: str = "1.0",
) -> ThemeDict:
    """Generate a Qlementine theme from named Radix scales.

    Parameters
    ----------
    accent : str
        Radix chromatic scale name (e.g. "blue", "crimson").
    gray : str, optional
        Radix gray scale name (e.g. "slate", "mauve"). If not provided,
        uses the default gray pairing for the accent.
    appearance : str
        "light" or "dark".
    name : str
        Theme display name.
    author : str
        Theme author.
    version : str
        Theme version string.
    """
    if gray is None:
        gray = GRAY_FOR_SCALE.get(accent, "gray")

    is_dark = appearance == "dark"

    # --- Look up scales ---
    acc = get_scale(accent, appearance)
    gry = get_scale(gray, appearance)
    contrast = get_accent_contrast(accent, appearance)
    bg_hex = DARK_BACKGROUNDS.get(gray, "#111111") if is_dark else LIGHT_BACKGROUND

    # Alpha variants of gray for semi-transparent uses
    gry_a = [_hex_with_alpha(c, 0.5) for c in gry]

    # --- Build the theme dict ---
    theme: ThemeDict = {"meta": {"name": name, "version": version, "author": author}}

    # =====================================================================
    # Background colors (from gray scale)
    # =====================================================================
    theme["background_color_main1"] = bg_hex
    theme["background_color_main2"] = bg_hex
    theme["background_color_main3"] = gry[1]
    theme["background_color_main4"] = gry[1]
    theme["background_color_workspace"] = bg_hex if is_dark else gry[7]
    theme["background_color_tab_bar"] = gry[2] if not is_dark else gry[1]

    # =====================================================================
    # Neutral colors
    # =====================================================================
    theme["neutral_color_disabled"] = gry[2]
    theme["neutral_color"] = gry[6]
    theme["neutral_color_hovered"] = gry[7]
    theme["neutral_color_pressed"] = gry[8]

    # =====================================================================
    # Focus color
    # =====================================================================
    theme["focus_color"] = _hex_with_alpha(acc[8], 0.40)

    # =====================================================================
    # Primary colors (from accent scale)
    # =====================================================================
    theme["primary_color"] = acc[8]
    theme["primary_color_hovered"] = acc[9]
    theme["primary_color_pressed"] = acc[10]
    theme["primary_color_disabled"] = acc[3]

    # Primary foreground
    theme["primary_color_foreground"] = contrast
    theme["primary_color_foreground_hovered"] = contrast
    theme["primary_color_foreground_pressed"] = contrast
    if is_dark:
        theme["primary_color_foreground_disabled"] = gry[6]
    else:
        theme["primary_color_foreground_disabled"] = acc[4]

    # Primary alternative
    if is_dark:
        theme["primary_alternative_color"] = acc[7]
        theme["primary_alternative_color_disabled"] = acc[3]
    else:
        theme["primary_alternative_color"] = acc[10]
        theme["primary_alternative_color_disabled"] = acc[5]
    theme["primary_alternative_color_hovered"] = acc[9]
    theme["primary_alternative_color_pressed"] = acc[8]

    # =====================================================================
    # Secondary colors (text / foreground)
    # =====================================================================
    if is_dark:
        theme["secondary_color"] = "#ffffff"
        theme["secondary_color_hovered"] = gry[11]
        theme["secondary_color_pressed"] = gry[11]
        theme["secondary_color_disabled"] = _hex_with_alpha("#ffffff", 0.20)
    else:
        theme["secondary_color"] = gry[11]
        theme["secondary_color_hovered"] = gry[10]
        theme["secondary_color_pressed"] = gry[9]
        theme["secondary_color_disabled"] = gry[5]

    # Secondary foreground (text on dark tooltip surfaces)
    if is_dark:
        theme["secondary_color_foreground"] = gry[2]
        theme["secondary_color_foreground_hovered"] = gry[2]
        theme["secondary_color_foreground_pressed"] = gry[2]
        theme["secondary_color_foreground_disabled"] = _hex_with_alpha(gry[2], 0.25)
    else:
        theme["secondary_color_foreground"] = "#ffffff"
        theme["secondary_color_foreground_hovered"] = "#ffffff"
        theme["secondary_color_foreground_pressed"] = "#ffffff"
        theme["secondary_color_foreground_disabled"] = gry[2]

    # Secondary alternative (muted/placeholder text)
    theme["secondary_alternative_color"] = gry[8]
    if is_dark:
        theme["secondary_alternative_color_hovered"] = gry[9]
        theme["secondary_alternative_color_pressed"] = gry[9]
        theme["secondary_alternative_color_disabled"] = gry_a[8]
    else:
        theme["secondary_alternative_color_hovered"] = gry[9]
        theme["secondary_alternative_color_pressed"] = gry[9]
        theme["secondary_alternative_color_disabled"] = gry[3]

    # =====================================================================
    # Border colors
    # =====================================================================
    theme["border_color_disabled"] = gry[3]
    theme["border_color"] = gry[6]
    theme["border_color_hovered"] = gry[7]
    theme["border_color_pressed"] = gry[8]

    # =====================================================================
    # Shadow colors
    # =====================================================================
    if is_dark:
        theme["shadow_color1"] = _hex_with_alpha("#000000", 0.40)
        theme["shadow_color2"] = _hex_with_alpha("#000000", 0.73)
        theme["shadow_color3"] = _hex_with_alpha("#000000", 1.00)
    else:
        theme["shadow_color1"] = _hex_with_alpha("#000000", 0.12)
        theme["shadow_color2"] = _hex_with_alpha("#000000", 0.25)
        theme["shadow_color3"] = _hex_with_alpha("#000000", 0.38)

    # =====================================================================
    # Semi-transparent colors
    # =====================================================================
    if is_dark:
        tint_base = acc[11]
        theme["semi_transparent_color1"] = _hex_with_alpha(tint_base, 0.09)
        theme["semi_transparent_color2"] = _hex_with_alpha(tint_base, 0.14)
        theme["semi_transparent_color3"] = _hex_with_alpha(tint_base, 0.16)
        theme["semi_transparent_color4"] = _hex_with_alpha(tint_base, 0.18)
    else:
        theme["semi_transparent_color1"] = _hex_with_alpha("#000000", 0.04)
        theme["semi_transparent_color2"] = _hex_with_alpha("#000000", 0.10)
        theme["semi_transparent_color3"] = _hex_with_alpha("#000000", 0.13)
        theme["semi_transparent_color4"] = _hex_with_alpha("#000000", 0.16)

    # =====================================================================
    # Status colors (4 groups from named Radix scales)
    # =====================================================================
    for status_name, scale_name in STATUS_SCALES.items():
        s = get_scale(scale_name, appearance)
        prefix = f"status_color_{status_name}"
        theme[prefix] = s[8]  # type: ignore[literal-required]
        theme[f"{prefix}_hovered"] = s[9]  # type: ignore[literal-required]
        theme[f"{prefix}_pressed"] = s[10]  # type: ignore[literal-required]
        theme[f"{prefix}_disabled"] = s[3]  # type: ignore[literal-required]

    theme["status_color_foreground"] = "#ffffff"
    theme["status_color_foreground_hovered"] = "#ffffff"
    theme["status_color_foreground_pressed"] = "#ffffff"
    theme["status_color_foreground_disabled"] = _hex_with_alpha(
        "#ffffff", 0.60 if not is_dark else 0.15
    )

    return theme
