"""Map Radix color generation output to a Qlementine ThemeDict."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from coloraide import Color

from carina._radix_generator import (
    RadixColorOutput,
    generate_radix_colors,
)

if TYPE_CHECKING:
    from carina._theme import ThemeDict

# ---------------------------------------------------------------------------
# Status color seeds (fixed accent inputs for the 4 status groups)
# ---------------------------------------------------------------------------

STATUS_SEEDS: dict[str, str] = {
    "success": "#2bb5a0",
    "info": "#1ba8d5",
    "warning": "#fbc064",
    "error": "#e96b72",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _hex_with_alpha(hex_color: str, alpha: float) -> str:
    """Apply alpha (0-1) to a #rrggbb hex color, returning #rrggbbaa."""
    c = Color(hex_color).convert("srgb")
    c.set("alpha", alpha)
    return c.clip().to_string(hex=True)



# ---------------------------------------------------------------------------
# Main mapper
# ---------------------------------------------------------------------------


def generate_qlementine_theme(
    accent: str,
    gray: str,
    background: str,
    appearance: str,
    name: str = "Custom",
    author: str = "Generated",
    version: str = "1.0",
) -> ThemeDict:
    """Generate a complete Qlementine theme from 3 color inputs + appearance.

    Parameters
    ----------
    accent : str
        Hex color for the accent/brand color (e.g. "#1890ff").
    gray : str
        Hex color for the gray tint base (e.g. "#8b8d94").
    background : str
        Hex color for the page background (e.g. "#ffffff").
    appearance : str
        "light" or "dark".
    name : str
        Theme display name.
    author : str
        Theme author.
    version : str
        Theme version string.
    """
    is_dark = appearance == "dark"

    # --- Generate main scales ---
    main = generate_radix_colors(accent, gray, background, appearance)
    acc = main["accentScale"]  # 12 sRGB hex values, 0-indexed
    gry = main["grayScale"]
    gry_a = main["grayScaleAlpha"]
    contrast = main["accentContrast"]
    bg_hex = main["background"]

    # Gray hue for derivations
    gray_oklch = Color(gry[8]).convert("oklch")
    gray_hue = gray_oklch["hue"]
    if math.isnan(gray_hue):
        gray_hue = 0.0

    # --- Generate status scales ---
    status_scales: dict[str, RadixColorOutput] = {}
    for status_name, seed in STATUS_SEEDS.items():
        status_scales[status_name] = generate_radix_colors(
            accent=seed, gray=gray, background=background, appearance=appearance
        )

    # --- Build the theme dict ---
    theme: ThemeDict = {"meta": {"name": name, "version": version, "author": author}}

    # =====================================================================
    # Background colors (from gray scale)
    # =====================================================================
    theme["background_color_main1"] = bg_hex  # QPalette::Base (item views)
    theme["background_color_main2"] = bg_hex  # QPalette::Window — match user bg
    theme["background_color_main3"] = gry[1]
    theme["background_color_main4"] = gry[1]
    # Workspace: darkest area (MDI background, external edges)
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
    theme["primary_color"] = acc[8]       # Radix step 9: solid accent
    theme["primary_color_hovered"] = acc[9]  # Radix step 10: hover on solid
    theme["primary_color_pressed"] = acc[10]  # Radix step 11: pressed
    theme["primary_color_disabled"] = acc[3]  # Radix step 4: subtle disabled

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
        theme["secondary_color"] = gry[11]       # Radix step 12: high-contrast text
        theme["secondary_color_hovered"] = gry[10]  # Radix step 11: slightly lighter
        theme["secondary_color_pressed"] = gry[9]   # Radix step 10
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
    theme["border_color_disabled"] = gry[3]  # Radix step 4
    theme["border_color"] = gry[6]          # Radix step 7: borders
    theme["border_color_hovered"] = gry[7]  # Radix step 8: hover border
    theme["border_color_pressed"] = gry[8]  # Radix step 9: pressed border

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
    # Status colors (4 groups, each generated from fixed seeds)
    # =====================================================================
    for status_name in ("success", "info", "warning", "error"):
        s = status_scales[status_name]["accentScale"]
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
