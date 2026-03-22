"""Port of Radix UI's generateRadixColors algorithm to Python.

Direct translation of radix-ui/website/components/generateRadixColors.tsx.
Uses coloraide for color space conversions (replacing colorjs.io).
"""

from __future__ import annotations

import json
import math
from collections.abc import Callable
from pathlib import Path
from typing import TypedDict

from coloraide import Color

# ---------------------------------------------------------------------------
# Scale name constants
# ---------------------------------------------------------------------------

GRAY_SCALE_NAMES = ("gray", "mauve", "slate", "sage", "olive", "sand")
SCALE_NAMES = (
    *GRAY_SCALE_NAMES,
    "tomato",
    "red",
    "ruby",
    "crimson",
    "pink",
    "plum",
    "purple",
    "violet",
    "iris",
    "indigo",
    "blue",
    "cyan",
    "teal",
    "jade",
    "green",
    "grass",
    "brown",
    "orange",
    "sky",
    "mint",
    "lime",
    "yellow",
    "amber",
)

# ---------------------------------------------------------------------------
# Bezier easing curves
# ---------------------------------------------------------------------------

_DARK_MODE_EASING: tuple[float, float, float, float] = (1.0, 0.0, 1.0, 0.0)
_LIGHT_MODE_EASING: tuple[float, float, float, float] = (0.0, 2.0, 0.0, 2.0)

# ---------------------------------------------------------------------------
# Lazy-loaded scale data (P3 → OKLCH)
# ---------------------------------------------------------------------------

_light_colors: dict[str, list[Color]] | None = None
_dark_colors: dict[str, list[Color]] | None = None
_light_gray_colors: dict[str, list[Color]] | None = None
_dark_gray_colors: dict[str, list[Color]] | None = None


def _ensure_scales() -> None:
    """Load vendored P3 color data and convert to OKLCH Color objects."""
    global _light_colors, _dark_colors, _light_gray_colors, _dark_gray_colors
    if _light_colors is not None:
        return

    data_path = Path(__file__).parent / "_radix_scales.json"
    with open(data_path) as f:
        raw: dict[str, list[str]] = json.load(f)

    _light_colors = {}
    _dark_colors = {}
    for name in SCALE_NAMES:
        _light_colors[name] = [Color(s).convert("oklch") for s in raw[name]]
        _dark_colors[name] = [Color(s).convert("oklch") for s in raw[name + "Dark"]]

    _light_gray_colors = {n: _light_colors[n] for n in GRAY_SCALE_NAMES}
    _dark_gray_colors = {n: _dark_colors[n] for n in GRAY_SCALE_NAMES}


# ---------------------------------------------------------------------------
# Bezier easing (port of npm bezier-easing)
# ---------------------------------------------------------------------------

_NEWTON_ITERATIONS = 4
_NEWTON_MIN_SLOPE = 0.001
_SUBDIVISION_PRECISION = 1e-7
_SUBDIVISION_MAX_ITERATIONS = 10
_SAMPLE_TABLE_SIZE = 11
_SAMPLE_STEP_SIZE = 1.0 / (_SAMPLE_TABLE_SIZE - 1)


def _bz_a(a1: float, a2: float) -> float:
    return 1.0 - 3.0 * a2 + 3.0 * a1


def _bz_b(a1: float, a2: float) -> float:
    return 3.0 * a2 - 6.0 * a1


def _bz_c(a1: float) -> float:
    return 3.0 * a1


def _calc_bezier(t: float, a1: float, a2: float) -> float:
    return ((_bz_a(a1, a2) * t + _bz_b(a1, a2)) * t + _bz_c(a1)) * t


def _get_slope(t: float, a1: float, a2: float) -> float:
    return 3.0 * _bz_a(a1, a2) * t * t + 2.0 * _bz_b(a1, a2) * t + _bz_c(a1)


def _binary_subdivide(
    x: float, a_start: float, a_end: float, mx1: float, mx2: float
) -> float:
    t = 0.0
    for _ in range(_SUBDIVISION_MAX_ITERATIONS):
        t = a_start + (a_end - a_start) / 2.0
        val = _calc_bezier(t, mx1, mx2) - x
        if val > 0:
            a_end = t
        else:
            a_start = t
        if abs(val) < _SUBDIVISION_PRECISION:
            break
    return t


def _newton_raphson(x: float, guess_t: float, mx1: float, mx2: float) -> float:
    for _ in range(_NEWTON_ITERATIONS):
        slope = _get_slope(guess_t, mx1, mx2)
        if slope == 0.0:
            return guess_t
        val = _calc_bezier(guess_t, mx1, mx2) - x
        guess_t -= val / slope
    return guess_t


def _bezier_easing(x1: float, y1: float, x2: float, y2: float) -> _BezierFn:
    """Create a cubic bezier easing function."""
    if x1 == y1 and x2 == y2:
        return lambda x: x

    samples = [
        _calc_bezier(i * _SAMPLE_STEP_SIZE, x1, x2) for i in range(_SAMPLE_TABLE_SIZE)
    ]

    def _get_t_for_x(x: float) -> float:
        interval_start = 0.0
        current_sample = 1
        last_sample = _SAMPLE_TABLE_SIZE - 1
        while current_sample != last_sample and samples[current_sample] <= x:
            interval_start += _SAMPLE_STEP_SIZE
            current_sample += 1
        current_sample -= 1

        denom = samples[current_sample + 1] - samples[current_sample]
        dist = (x - samples[current_sample]) / denom if denom else 0
        guess_t = interval_start + dist * _SAMPLE_STEP_SIZE
        initial_slope = _get_slope(guess_t, x1, x2)

        if initial_slope >= _NEWTON_MIN_SLOPE:
            return _newton_raphson(x, guess_t, x1, x2)
        if initial_slope == 0.0:
            return guess_t
        return _binary_subdivide(
            x, interval_start, interval_start + _SAMPLE_STEP_SIZE, x1, x2
        )

    def easing(x: float) -> float:
        if x == 0:
            return 0.0
        if x == 1:
            return 1.0
        return _calc_bezier(_get_t_for_x(x), y1, y2)

    return easing


_BezierFn = Callable[[float], float]


# ---------------------------------------------------------------------------
# APCA contrast (matching colorjs.io's contrastAPCA)
# ---------------------------------------------------------------------------


def _srgb_luminance(color: Color) -> float:
    """Compute relative luminance from an sRGB color."""
    srgb = color.convert("srgb")
    r, g, b = srgb.coords()

    def linearize(v: float) -> float:
        v = max(0.0, min(1.0, v))
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4

    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


def _contrast_apca(text: Color, background: Color) -> float:
    """APCA contrast matching colorjs.io's text.contrastAPCA(background)."""
    fg_y = _srgb_luminance(text)
    bg_y = _srgb_luminance(background)

    fg_yc = fg_y + (0.022 - fg_y) ** 1.414 if fg_y < 0.022 else fg_y
    bg_yc = bg_y + (0.022 - bg_y) ** 1.414 if bg_y < 0.022 else bg_y

    if bg_yc > fg_yc:
        # Normal polarity (dark text on light background)
        c = (bg_yc**0.56 - fg_yc**0.57) * 1.14
    else:
        # Reverse polarity (light text on dark background)
        c = (bg_yc**0.65 - fg_yc**0.62) * 1.14

    if abs(c) < 0.1:
        return 0.0
    return (c - 0.027) * 100.0 if c > 0 else (c + 0.027) * 100.0


# ---------------------------------------------------------------------------
# Helper: convert to hex
# ---------------------------------------------------------------------------


def _to_hex(color: Color) -> str:
    """Convert color to #rrggbb hex string."""
    return color.convert("srgb").clip().to_string(hex=True)


def _to_oklch_string(color: Color) -> str:
    """Convert to OKLCH string with percentage lightness."""
    oklch = color.convert("oklch")
    L = oklch["lightness"] * 100
    C = oklch["chroma"]
    H = oklch["hue"]
    h_str = "none" if math.isnan(H) else f"{H:.1f}"
    return f"oklch({L:.1f}% {C:.4f} {h_str})"


# ---------------------------------------------------------------------------
# Core algorithm helpers
# ---------------------------------------------------------------------------


def _get_text_color(background: Color) -> Color:
    """APCA check: white if contrast >= Lc 40, else a dark hue-matched color."""
    white = Color("oklch", [1, 0, 0])
    if abs(_contrast_apca(white, background)) < 40:
        _L, C, H = background["lightness"], background["chroma"], background["hue"]
        return Color("oklch", [0.25, max(0.08 * C, 0.04), H])
    return white


def _get_step9_colors(scale: list[Color], accent_base: Color) -> tuple[Color, Color]:
    """Get step 9 color and its contrast text color."""
    ref_bg = scale[0]
    distance = accent_base.delta_e(ref_bg, method="ok") * 100
    if distance < 25:
        return scale[8], _get_text_color(scale[8])
    return accent_base, _get_text_color(accent_base)


def _get_button_hover_color(source: Color, scales: list[list[Color]]) -> Color:
    """Compute hover color for step 10."""
    L = source["lightness"]
    C = source["chroma"]
    H = source["hue"]

    new_L = L - 0.03 / (L + 0.1) if L > 0.4 else L + 0.03 / (L + 0.1)
    new_C = C * 0.93 if L > 0.4 and not math.isnan(H) else C
    hover = Color("oklch", [new_L, new_C, H])

    # Find closest in-scale color to donate chroma and hue
    closest = hover
    min_dist = float("inf")
    for scale in scales:
        for color in scale:
            d = hover.delta_e(color, method="ok")
            if d < min_dist:
                min_dist = d
                closest = color

    hover["chroma"] = closest["chroma"]
    hover["hue"] = closest["hue"]
    return hover


def _transpose_progression_start(
    to: float, arr: list[float], curve: tuple[float, float, float, float]
) -> list[float]:
    """Shift lightness progression so the first step matches `to`."""
    fn = _bezier_easing(*curve)
    last_index = len(arr) - 1
    diff = arr[0] - to
    return [
        n - diff * fn(1 - i / last_index) if last_index > 0 else n
        for i, n in enumerate(arr)
    ]


def _get_scale_from_color(
    source: Color,
    scales: dict[str, list[Color]],
    background_color: Color,
) -> list[Color]:
    """Find and blend the two closest reference scales to match source."""
    # Collect all individual color distances
    all_colors: list[tuple[str, float, Color]] = []
    for name, scale in scales.items():
        for color in scale:
            d = source.delta_e(color, method="ok")
            all_colors.append((name, d, color))
    all_colors.sort(key=lambda x: x[1])

    # Deduplicate to one entry per scale (closest color from each)
    seen: set[str] = set()
    closest: list[tuple[str, float, Color]] = []
    for name, d, color in all_colors:
        if name not in seen:
            seen.add(name)
            closest.append((name, d, color))

    # If top two are both grays (and not ALL are grays), skip extra grays
    all_are_grays = all(n in GRAY_SCALE_NAMES for n, _, _ in closest)
    if not all_are_grays and closest[0][0] in GRAY_SCALE_NAMES:
        while len(closest) > 1 and closest[1][0] in GRAY_SCALE_NAMES:
            closest.pop(1)

    color_a = closest[0]
    color_b = closest[1]

    # Trigonometry to determine blend ratio
    a = color_b[1]  # distance from source to B
    b = color_a[1]  # distance from source to A
    c = color_a[2].delta_e(color_b[2], method="ok")  # distance A to B

    ratio = 0.0
    if b > 1e-10 and c > 1e-10:
        cos_a_val = max(-1.0, min(1.0, (b**2 + c**2 - a**2) / (2 * b * c)))
        cos_b_val = max(-1.0, min(1.0, (a**2 + c**2 - b**2) / (2 * a * c)))
        rad_a = math.acos(cos_a_val)
        rad_b = math.acos(cos_b_val)
        sin_a = math.sin(rad_a)
        sin_b = math.sin(rad_b)

        if sin_a > 1e-10 and sin_b > 1e-10:
            tan_c1 = cos_a_val / sin_a
            tan_c2 = cos_b_val / sin_b
            if tan_c2 != 0:
                ratio = max(0.0, tan_c1 / tan_c2) * 0.5

    # Mix the two closest scales
    scale_a = scales[color_a[0]]
    scale_b = scales[color_b[0]]
    scale = [scale_a[i].mix(scale_b[i], ratio, space="oklch") for i in range(12)]

    # Find closest color in the blended scale
    base_color = min(scale, key=lambda c: source.delta_e(c, method="ok"))

    # Chroma ratio
    base_chroma = base_color["chroma"]
    source_chroma = source["chroma"]
    ratio_c = source_chroma / base_chroma if base_chroma > 1e-10 else 1.0

    # Adjust hue and chroma of every step
    source_hue = source["hue"]
    for color in scale:
        color["chroma"] = min(source_chroma * 1.5, color["chroma"] * ratio_c)
        color["hue"] = source_hue

    # --- Lightness transposition ---

    # Light mode
    if scale[0]["lightness"] > 0.5:
        lightness_scale = [c["lightness"] for c in scale]
        bg_L = max(0.0, min(1.0, background_color["lightness"]))
        new_L = _transpose_progression_start(
            bg_L, [1.0, *lightness_scale], _LIGHT_MODE_EASING
        )
        new_L.pop(0)  # remove the prepended white step
        for i, L in enumerate(new_L):
            scale[i]["lightness"] = L
        return scale

    # Dark mode
    ease = list(_DARK_MODE_EASING)
    ref_bg_L = scale[0]["lightness"]
    bg_L = max(0.0, min(1.0, background_color["lightness"]))

    if ref_bg_L > 1e-10:
        ratio_L = bg_L / ref_bg_L
        if ratio_L > 1:
            max_ratio = 1.5
            for i in range(len(ease)):
                meta_ratio = (ratio_L - 1) * (max_ratio / (max_ratio - 1))
                ease[i] = (
                    0.0 if ratio_L > max_ratio else max(0.0, ease[i] * (1 - meta_ratio))
                )

    lightness_scale = [c["lightness"] for c in scale]
    new_L = _transpose_progression_start(
        bg_L,
        lightness_scale,
        tuple(ease),  # type: ignore[arg-type]
    )
    for i, L in enumerate(new_L):
        scale[i]["lightness"] = L
    return scale


# ---------------------------------------------------------------------------
# Alpha color computation (sRGB only)
# ---------------------------------------------------------------------------


def _get_alpha_color(
    target_rgb: list[float],
    background_rgb: list[float],
    rgb_precision: int,
    alpha_precision: int,
    target_alpha: float | None = None,
) -> tuple[float, float, float, float]:
    """Back-solve alpha color from a target solid color over a background."""
    tr = round(target_rgb[0] * rgb_precision)
    tg = round(target_rgb[1] * rgb_precision)
    tb = round(target_rgb[2] * rgb_precision)
    br = round(background_rgb[0] * rgb_precision)
    bg = round(background_rgb[1] * rgb_precision)
    bb = round(background_rgb[2] * rgb_precision)

    # Decide whether to lighten or darken
    desired_rgb = rgb_precision if (tr > br or tg > bg or tb > bb) else 0

    def safe_div(num: float, den: float) -> float:
        return num / den if den != 0 else 0.0

    alpha_r = safe_div(tr - br, desired_rgb - br)
    alpha_g = safe_div(tg - bg, desired_rgb - bg)
    alpha_b = safe_div(tb - bb, desired_rgb - bb)

    is_pure_gray = alpha_r == alpha_g == alpha_b

    if target_alpha is None and is_pure_gray:
        v = desired_rgb / rgb_precision
        return (v, v, v, alpha_r)

    def clamp_rgb(n: float) -> float:
        return 0.0 if math.isnan(n) else min(rgb_precision, max(0, n))

    def clamp_a(n: float) -> float:
        return 0.0 if math.isnan(n) else min(alpha_precision, max(0, n))

    max_alpha = (
        target_alpha if target_alpha is not None else max(alpha_r, alpha_g, alpha_b)
    )
    A = clamp_a(math.ceil(max_alpha * alpha_precision)) / alpha_precision
    if A == 0:
        return (0.0, 0.0, 0.0, 0.0)

    R = clamp_rgb(((br * (1 - A) - tr) / A) * -1)
    G = clamp_rgb(((bg * (1 - A) - tg) / A) * -1)
    B = clamp_rgb(((bb * (1 - A) - tb) / A) * -1)

    R = math.ceil(R)
    G = math.ceil(G)
    B = math.ceil(B)

    def blend_alpha(fg: float, alpha: float, bkg: float) -> float:
        return round(bkg * (1 - alpha)) + round(fg * alpha)

    blended_r = blend_alpha(R, A, br)
    blended_g = blend_alpha(G, A, bg)
    blended_b = blend_alpha(B, A, bb)

    # Correct for rounding errors (light mode)
    if desired_rgb == 0:
        if tr <= br and tr != blended_r:
            R += 1 if tr > blended_r else -1
        if tg <= bg and tg != blended_g:
            G += 1 if tg > blended_g else -1
        if tb <= bb and tb != blended_b:
            B += 1 if tb > blended_b else -1

    # Correct for rounding errors (dark mode)
    if desired_rgb == rgb_precision:
        if tr >= br and tr != blended_r:
            R += 1 if tr > blended_r else -1
        if tg >= bg and tg != blended_g:
            G += 1 if tg > blended_g else -1
        if tb >= bb and tb != blended_b:
            B += 1 if tb > blended_b else -1

    return (R / rgb_precision, G / rgb_precision, B / rgb_precision, A)


def _get_alpha_color_srgb(
    target_hex: str,
    background_hex: str,
    target_alpha: float | None = None,
) -> str:
    """Compute alpha-composited sRGB hex color."""
    target = Color(target_hex).convert("srgb")
    bg = Color(background_hex).convert("srgb")
    r, g, b, a = _get_alpha_color(
        list(target.coords()), list(bg.coords()), 255, 255, target_alpha
    )
    return Color("srgb", [r, g, b], a).clip().to_string(hex=True)


# ---------------------------------------------------------------------------
# Output type
# ---------------------------------------------------------------------------


class RadixColorOutput(TypedDict):
    """Output from the Radix color generation algorithm."""

    accentScale: list[str]
    accentScaleAlpha: list[str]
    accentScaleWideGamut: list[str]
    accentScaleAlphaWideGamut: list[str]
    accentContrast: str
    grayScale: list[str]
    grayScaleAlpha: list[str]
    grayScaleWideGamut: list[str]
    grayScaleAlphaWideGamut: list[str]
    background: str


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def generate_radix_colors(
    accent: str,
    gray: str,
    background: str,
    appearance: str,
) -> RadixColorOutput:
    """Generate Radix color scales from accent, gray, and background inputs.

    Parameters
    ----------
    accent : str
        Hex color for the accent/brand color.
    gray : str
        Hex color for the gray tint base.
    background : str
        Hex color for the page background.
    appearance : str
        Either "light" or "dark".

    Returns
    -------
    RadixColorOutput
        Dictionary containing 12-step accent and gray scales in multiple
        formats, plus the accent contrast color and background hex.
    """
    _ensure_scales()
    assert _light_colors is not None
    assert _dark_colors is not None
    assert _light_gray_colors is not None
    assert _dark_gray_colors is not None

    all_scales = _light_colors if appearance == "light" else _dark_colors
    gray_scales = _light_gray_colors if appearance == "light" else _dark_gray_colors

    background_color = Color(background).convert("oklch")
    gray_base = Color(gray).convert("oklch")
    gray_scale = _get_scale_from_color(gray_base, gray_scales, background_color)

    accent_base = Color(accent).convert("oklch")
    accent_scale = _get_scale_from_color(accent_base, all_scales, background_color)

    # Enforce sRGB for the background
    background_hex = Color(background).convert("srgb").clip().to_string(hex=True)

    # Pure black/white accent → use gray scale
    accent_base_hex = accent_base.convert("srgb").clip().to_string(hex=True)
    if accent_base_hex in ("#000000", "#ffffff"):
        accent_scale = [c.clone() for c in gray_scale]

    # Step 9 and contrast
    accent9, accent_contrast = _get_step9_colors(accent_scale, accent_base)
    accent_scale[8] = accent9
    accent_scale[9] = _get_button_hover_color(accent9, [accent_scale])

    # Limit saturation of text colors (steps 11, 12)
    max_c = max(accent_scale[8]["chroma"], accent_scale[7]["chroma"])
    accent_scale[10]["chroma"] = min(max_c, accent_scale[10]["chroma"])
    accent_scale[11]["chroma"] = min(max_c, accent_scale[11]["chroma"])

    # Convert to output formats
    accent_hex = [_to_hex(c) for c in accent_scale]
    accent_wg = [_to_oklch_string(c) for c in accent_scale]
    accent_alpha_hex = [_get_alpha_color_srgb(h, background_hex) for h in accent_hex]

    gray_hex = [_to_hex(c) for c in gray_scale]
    gray_wg = [_to_oklch_string(c) for c in gray_scale]
    gray_alpha_hex = [_get_alpha_color_srgb(h, background_hex) for h in gray_hex]

    contrast_hex = _to_hex(accent_contrast)

    return {
        "accentScale": accent_hex,
        "accentScaleAlpha": accent_alpha_hex,
        "accentScaleWideGamut": accent_wg,
        "accentScaleAlphaWideGamut": [],
        "accentContrast": contrast_hex,
        "grayScale": gray_hex,
        "grayScaleAlpha": gray_alpha_hex,
        "grayScaleWideGamut": gray_wg,
        "grayScaleAlphaWideGamut": [],
        "background": background_hex,
    }
