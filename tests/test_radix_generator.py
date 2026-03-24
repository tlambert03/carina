"""Tests for the Radix scale lookup."""

from __future__ import annotations

import pytest

from carina._radix_generator import (
    GRAY_SCALE_NAMES,
    get_accent_contrast,
    get_scale,
    scale_names,
)


def _parse_rgb(hex_color: str) -> tuple[int, int, int]:
    """Parse #rrggbb to (r, g, b) ints."""
    h = hex_color.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _relative_luminance(hex_color: str) -> float:
    """Approximate relative luminance from hex."""
    r, g, b = _parse_rgb(hex_color)

    def lin(v: int) -> float:
        s = v / 255
        return s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4

    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


# ---------------------------------------------------------------------------
# get_scale tests
# ---------------------------------------------------------------------------


def test_get_scale_returns_12_steps() -> None:
    scale = get_scale("blue", "light")
    assert len(scale) == 12
    assert all(s.startswith("#") for s in scale)


def test_get_scale_dark() -> None:
    scale = get_scale("blue", "dark")
    assert len(scale) == 12


def test_get_scale_all_names() -> None:
    for name in scale_names():
        light = get_scale(name, "light")
        dark = get_scale(name, "dark")
        assert len(light) == 12, f"{name} light"
        assert len(dark) == 12, f"{name} dark"


def test_get_scale_invalid_name() -> None:
    with pytest.raises(ValueError, match="Unknown scale"):
        get_scale("nonexistent", "light")


def test_light_scale_lightness_decreasing() -> None:
    """Light mode: step 1 should be lighter than step 12."""
    scale = get_scale("blue", "light")
    assert _relative_luminance(scale[0]) > _relative_luminance(scale[11])


def test_dark_scale_lightness_increasing() -> None:
    """Dark mode: step 1 should be darker than step 12."""
    scale = get_scale("blue", "dark")
    assert _relative_luminance(scale[0]) < _relative_luminance(scale[11])


def test_gray_scale_low_chroma() -> None:
    """Gray scales should be nearly achromatic."""
    for name in GRAY_SCALE_NAMES:
        scale = get_scale(name, "light")
        for i, hex_color in enumerate(scale):
            r, g, b = _parse_rgb(hex_color)
            spread = max(r, g, b) - min(r, g, b)
            assert spread <= 15, f"{name} step {i}: spread={spread}"


# ---------------------------------------------------------------------------
# Contrast tests
# ---------------------------------------------------------------------------


def test_get_accent_contrast_blue() -> None:
    assert get_accent_contrast("blue", "light") == "#ffffff"


def test_get_accent_contrast_yellow() -> None:
    """Yellow step 9 is light, so contrast should be dark."""
    contrast = get_accent_contrast("yellow", "light")
    assert contrast != "#ffffff"
    assert _relative_luminance(contrast) < 0.1


# ---------------------------------------------------------------------------
# scale_names tests
# ---------------------------------------------------------------------------


def test_scale_names_derived_from_json() -> None:
    names = scale_names()
    assert "blue" in names
    assert "gray" in names
    assert len(names) >= 29  # 6 grays + 23 chromatics


def test_gray_names_are_subset_of_scale_names() -> None:
    assert GRAY_SCALE_NAMES.issubset(scale_names())
