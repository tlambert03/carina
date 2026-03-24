"""Tests for the Qlementine theme mapper."""

from __future__ import annotations

from carina._qlementine_mapper import generate_qlementine_theme
from carina._radix_generator import get_scale


def _parse_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")[:6]
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _relative_luminance(hex_color: str) -> float:
    r, g, b = _parse_rgb(hex_color)

    def lin(v: int) -> float:
        s = v / 255
        return s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4

    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


# ---------------------------------------------------------------------------
# Light theme tests
# ---------------------------------------------------------------------------


def test_light_theme_structure() -> None:
    theme = generate_qlementine_theme(accent="blue", appearance="light")
    assert theme["meta"]["name"] == "Custom"
    for key, value in theme.items():
        if key == "meta":
            continue
        assert isinstance(value, str), f"{key} should be str, got {type(value)}"


def test_light_primary_matches_scale_step9() -> None:
    theme = generate_qlementine_theme(accent="blue", appearance="light")
    scale = get_scale("blue", "light")
    assert theme["primary_color"] == scale[8]
    assert theme["primary_color_foreground"] == "#ffffff"


def test_light_background_is_white() -> None:
    theme = generate_qlementine_theme(accent="blue", appearance="light")
    assert theme["background_color_main1"] == "#ffffff"


def test_light_hover_press_differs() -> None:
    theme = generate_qlementine_theme(accent="blue", appearance="light")
    primary = theme["primary_color"]
    assert theme["primary_color_hovered"] != primary
    assert theme["primary_color_pressed"] != primary
    assert theme["primary_color_hovered"] != theme["primary_color_pressed"]


def test_light_secondary_color_contrast() -> None:
    """Secondary color (main text) should have high contrast on background."""
    theme = generate_qlementine_theme(accent="blue", appearance="light")
    text_lum = _relative_luminance(theme["secondary_color"])
    bg_lum = _relative_luminance(theme["background_color_main1"])
    # WCAG contrast ratio: (lighter + 0.05) / (darker + 0.05)
    ratio = (bg_lum + 0.05) / (text_lum + 0.05)
    assert ratio > 7, f"Expected contrast ratio > 7, got {ratio:.1f}"


def test_light_status_colors() -> None:
    theme = generate_qlementine_theme(accent="blue", appearance="light")
    teal_scale = get_scale("teal", "light")
    blue_scale = get_scale("blue", "light")
    red_scale = get_scale("red", "light")
    assert theme["status_color_success"] == teal_scale[8]
    assert theme["status_color_info"] == blue_scale[8]
    assert theme["status_color_error"] == red_scale[8]
    assert theme["status_color_foreground"] == "#ffffff"


def test_light_hardcoded_values() -> None:
    theme = generate_qlementine_theme(accent="blue", appearance="light")
    assert theme["semi_transparent_color1"] == "#0000000a"
    assert theme["shadow_color1"] == "#0000001f"


# ---------------------------------------------------------------------------
# Dark theme tests
# ---------------------------------------------------------------------------


def test_dark_theme_structure() -> None:
    theme = generate_qlementine_theme(accent="blue", appearance="dark")
    assert theme["meta"]["name"] == "Custom"
    for key, value in theme.items():
        if key == "meta":
            continue
        assert isinstance(value, str), f"{key} should be str"


def test_dark_primary_matches_scale_step9() -> None:
    theme = generate_qlementine_theme(accent="blue", appearance="dark")
    scale = get_scale("blue", "dark")
    assert theme["primary_color"] == scale[8]


def test_dark_secondary_is_white() -> None:
    theme = generate_qlementine_theme(accent="blue", appearance="dark")
    assert theme["secondary_color"] == "#ffffff"


def test_dark_background_is_dark() -> None:
    theme = generate_qlementine_theme(accent="blue", appearance="dark")
    bg_lum = _relative_luminance(theme["background_color_main1"])
    assert bg_lum < 0.03


def test_dark_tab_bar_is_dark() -> None:
    theme = generate_qlementine_theme(accent="blue", appearance="dark")
    tab_lum = _relative_luminance(theme["background_color_tab_bar"])
    assert tab_lum < 0.05


def test_dark_semi_transparent_uses_accent_tint() -> None:
    theme = generate_qlementine_theme(accent="blue", appearance="dark")
    r, g, b = _parse_rgb(theme["semi_transparent_color1"])
    # Should have some blue tint, not pure black
    assert max(r, g, b) > 80


def test_dark_hover_press_differs() -> None:
    theme = generate_qlementine_theme(accent="blue", appearance="dark")
    primary = theme["primary_color"]
    assert theme["primary_color_hovered"] != primary
    assert theme["primary_color_pressed"] != primary


# ---------------------------------------------------------------------------
# General / cross-mode tests
# ---------------------------------------------------------------------------


def test_different_accent_scales() -> None:
    for accent in ("red", "green", "purple", "orange", "teal"):
        theme = generate_qlementine_theme(accent=accent, appearance="light")
        scale = get_scale(accent, "light")
        assert theme["primary_color"] == scale[8]


def test_default_gray_pairing() -> None:
    """When gray is not specified, it uses the default pairing."""
    theme = generate_qlementine_theme(accent="blue", appearance="light")
    slate_scale = get_scale("slate", "light")
    assert theme["neutral_color"] == slate_scale[6]


def test_explicit_gray() -> None:
    theme = generate_qlementine_theme(accent="blue", gray="mauve", appearance="light")
    mauve_scale = get_scale("mauve", "light")
    assert theme["neutral_color"] == mauve_scale[6]


def test_theme_round_trip() -> None:
    from carina._theme import Theme, ThemeMeta

    td = generate_qlementine_theme(accent="blue", appearance="light")
    meta_dict = td["meta"]
    meta = ThemeMeta(
        name=meta_dict["name"],
        version=meta_dict["version"],
        author=meta_dict["author"],
    )
    theme = Theme(meta=meta)
    for key, value in td.items():
        if key == "meta":
            continue
        if hasattr(theme, key):
            setattr(theme, key, value)

    d = theme.asdict()
    scale = get_scale("blue", "light")
    assert d["primary_color"] == scale[8]
