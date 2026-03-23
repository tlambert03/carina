"""Tests for the Radix color generation algorithm."""

from __future__ import annotations

import math

from coloraide import Color

from carina._radix_generator import (
    _bezier_easing,
    _contrast_apca,
    _get_alpha_color_srgb,
    _srgb_luminance,
    _transpose_progression_start,
    generate_radix_colors,
)


def _delta_e(hex1: str, hex2: str) -> float:
    """Compute deltaE OK between two hex colors."""
    return Color(hex1).delta_e(Color(hex2), method="ok")


# ---------------------------------------------------------------------------
# Bezier easing tests
# ---------------------------------------------------------------------------


def test_bezier_linear() -> None:
    fn = _bezier_easing(0.5, 0.5, 0.5, 0.5)
    # Close to linear since control points are on the diagonal
    assert fn(0) == 0.0
    assert fn(1) == 1.0
    assert abs(fn(0.5) - 0.5) < 0.01


def test_bezier_endpoints() -> None:
    fn = _bezier_easing(0.0, 2.0, 0.0, 2.0)
    assert fn(0) == 0.0
    assert fn(1) == 1.0


def test_bezier_dark_mode_ease() -> None:
    fn = _bezier_easing(1.0, 0.0, 1.0, 0.0)
    assert fn(0) == 0.0
    assert fn(1) == 1.0
    # Should be an easing curve, monotonically increasing
    prev = 0.0
    for i in range(1, 10):
        x = i / 10
        y = fn(x)
        assert y >= prev
        prev = y


# ---------------------------------------------------------------------------
# APCA contrast tests
# ---------------------------------------------------------------------------


def test_apca_white_on_black() -> None:
    lc = _contrast_apca(Color("white"), Color("black"))
    # White text on black bg → reverse polarity, large negative Lc
    assert lc < -100


def test_apca_black_on_white() -> None:
    lc = _contrast_apca(Color("black"), Color("white"))
    # Black text on white bg → normal polarity, large positive Lc
    assert lc > 100


def test_apca_white_on_white() -> None:
    assert _contrast_apca(Color("white"), Color("white")) == 0.0


def test_apca_dark_text_on_white() -> None:
    # #404040 on white should give ~90 Lc (reference value)
    lc = _contrast_apca(Color("#404040"), Color("white"))
    assert 88 < lc < 93


def test_srgb_luminance_white() -> None:
    assert abs(_srgb_luminance(Color("white")) - 1.0) < 1e-6


def test_srgb_luminance_black() -> None:
    assert abs(_srgb_luminance(Color("black"))) < 1e-6


# ---------------------------------------------------------------------------
# Transpose progression tests
# ---------------------------------------------------------------------------


def test_transpose_no_change() -> None:
    arr = [1.0, 0.8, 0.6, 0.4, 0.2]
    result = _transpose_progression_start(1.0, arr, (0.0, 2.0, 0.0, 2.0))
    # When to == arr[0], diff=0, no shift
    for a, b in zip(arr, result, strict=False):
        assert abs(a - b) < 1e-10


# ---------------------------------------------------------------------------
# Alpha color tests
# ---------------------------------------------------------------------------


def test_alpha_color_srgb_identity() -> None:
    # White target on white background → should be fully transparent
    result = _get_alpha_color_srgb("#ffffff", "#ffffff")
    # Result should have alpha near 0 or be white
    c = Color(result)
    assert c.alpha() < 0.02 or result == "#ffffff"


def test_alpha_color_srgb_black_on_white() -> None:
    result = _get_alpha_color_srgb("#000000", "#ffffff")
    # Should be black with full alpha
    assert result == "#000000"


# ---------------------------------------------------------------------------
# Full generator tests
# ---------------------------------------------------------------------------


def test_generate_light_basic() -> None:
    result = generate_radix_colors(
        accent="#1890ff",
        gray="#8b8b8b",
        background="#ffffff",
        appearance="light",
    )
    assert len(result["accentScale"]) == 12
    assert len(result["grayScale"]) == 12
    assert len(result["accentScaleAlpha"]) == 12
    assert len(result["grayScaleAlpha"]) == 12
    assert result["background"] == "#ffffff"

    # Step 9 should be close to the accent input
    assert _delta_e(result["accentScale"][8], "#1890ff") < 0.01

    # Contrast should be white (blue on white has enough contrast)
    assert result["accentContrast"] == "#ffffff"


def test_generate_dark_basic() -> None:
    result = generate_radix_colors(
        accent="#5086ff",
        gray="#8b8d94",
        background="#1f2127",
        appearance="dark",
    )
    assert len(result["accentScale"]) == 12
    assert result["background"] == "#1f2127"
    assert _delta_e(result["accentScale"][8], "#5086ff") < 0.01
    assert result["accentContrast"] == "#ffffff"


def test_generate_scale_ordering_light() -> None:
    """Light mode: scale should go from light to dark (L decreasing)."""
    result = generate_radix_colors(
        accent="#1890ff",
        gray="#8b8b8b",
        background="#ffffff",
        appearance="light",
    )
    lightness = [Color(h).convert("oklch")["lightness"] for h in result["accentScale"]]
    # Overall trend should be decreasing (step 1 lightest, step 12 darkest)
    assert lightness[0] > lightness[11]


def test_generate_scale_ordering_dark() -> None:
    """Dark mode: scale should go from dark to light (L increasing)."""
    result = generate_radix_colors(
        accent="#5086ff",
        gray="#8b8d94",
        background="#1f2127",
        appearance="dark",
    )
    lightness = [Color(h).convert("oklch")["lightness"] for h in result["accentScale"]]
    # Overall trend should be increasing (step 1 darkest, step 12 lightest)
    assert lightness[0] < lightness[11]


def test_generate_gray_is_achromatic() -> None:
    """Gray scale should have very low chroma for a neutral gray input."""
    result = generate_radix_colors(
        accent="#1890ff",
        gray="#8b8b8b",
        background="#ffffff",
        appearance="light",
    )
    for h in result["grayScale"]:
        c = Color(h).convert("oklch")
        chroma = c["chroma"]
        if not math.isnan(chroma):
            assert chroma < 0.02


def test_generate_status_seeds() -> None:
    """Status color seeds should produce consistent results."""
    for seed in ("#2bb5a0", "#1ba8d5", "#fbc064", "#e96b72"):
        result = generate_radix_colors(
            accent=seed,
            gray="#8b8b8b",
            background="#ffffff",
            appearance="light",
        )
        assert len(result["accentScale"]) == 12
        # Light seeds like amber may snap to scale step 9 if too close
        # to the scale's step 1 background, so allow wider tolerance
        assert _delta_e(result["accentScale"][8], seed) < 0.1


def test_generate_wide_gamut_output() -> None:
    result = generate_radix_colors(
        accent="#1890ff",
        gray="#8b8b8b",
        background="#ffffff",
        appearance="light",
    )
    assert len(result["accentScaleWideGamut"]) == 12
    assert len(result["grayScaleWideGamut"]) == 12
    for s in result["accentScaleWideGamut"]:
        assert s.startswith("oklch(")
