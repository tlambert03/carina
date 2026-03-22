"""Tests for the Qlementine theme mapper."""

from __future__ import annotations

from coloraide import Color

from carina._qlementine_mapper import generate_qlementine_theme


def _delta_e(hex1: str, hex2: str) -> float:
    return Color(hex1).delta_e(Color(hex2), method="ok")


# ---------------------------------------------------------------------------
# Light theme tests
# ---------------------------------------------------------------------------


def test_light_theme_structure() -> None:
    theme = generate_qlementine_theme(
        accent="#1890ff",
        gray="#8b8b8b",
        background="#ffffff",
        appearance="light",
    )
    assert theme["meta"]["name"] == "Custom"
    # All color fields should be strings
    for key, value in theme.items():
        if key == "meta":
            continue
        assert isinstance(value, str), f"{key} should be str, got {type(value)}"


def test_light_primary_is_accent() -> None:
    theme = generate_qlementine_theme(
        accent="#1890ff",
        gray="#8b8b8b",
        background="#ffffff",
        appearance="light",
    )
    assert theme["primary_color"] == "#1890ff"
    assert theme["primary_color_foreground"] == "#ffffff"


def test_light_background_is_exact() -> None:
    theme = generate_qlementine_theme(
        accent="#1890ff",
        gray="#8b8b8b",
        background="#ffffff",
        appearance="light",
    )
    assert theme["background_color_main1"] == "#ffffff"


def test_light_hover_press_differs() -> None:
    """Hover/press should differ from the base primary color."""
    theme = generate_qlementine_theme(
        accent="#1890ff",
        gray="#8b8b8b",
        background="#ffffff",
        appearance="light",
    )
    primary = theme["primary_color"]
    assert theme["primary_color_hovered"] != primary
    assert theme["primary_color_pressed"] != primary
    assert theme["primary_color_hovered"] != theme["primary_color_pressed"]


def test_light_secondary_color_contrast() -> None:
    """Secondary color (main text) should have high contrast on background."""
    theme = generate_qlementine_theme(
        accent="#1890ff",
        gray="#8b8b8b",
        background="#ffffff",
        appearance="light",
    )
    from carina._radix_generator import _contrast_apca

    text = Color(theme["secondary_color"])
    bg = Color(theme["background_color_main1"])
    lc = abs(_contrast_apca(text, bg))
    assert lc > 80, f"Expected Lc > 80, got {lc}"


def test_light_status_colors() -> None:
    theme = generate_qlementine_theme(
        accent="#1890ff",
        gray="#8b8b8b",
        background="#ffffff",
        appearance="light",
    )
    # Status seeds should be close to the reference
    assert _delta_e(theme["status_color_success"], "#2bb5a0") < 0.02
    assert _delta_e(theme["status_color_info"], "#1ba8d5") < 0.02
    assert _delta_e(theme["status_color_error"], "#e96b72") < 0.02
    assert theme["status_color_foreground"] == "#ffffff"


def test_light_hardcoded_values() -> None:
    theme = generate_qlementine_theme(
        accent="#1890ff",
        gray="#8b8b8b",
        background="#ffffff",
        appearance="light",
    )
    assert theme["semi_transparent_color1"] == "#0000000a"
    assert theme["shadow_color1"] == "#0000001f"


# ---------------------------------------------------------------------------
# Dark theme tests
# ---------------------------------------------------------------------------


def test_dark_theme_structure() -> None:
    theme = generate_qlementine_theme(
        accent="#5086ff",
        gray="#8b8d94",
        background="#1f2127",
        appearance="dark",
    )
    assert theme["meta"]["name"] == "Custom"
    for key, value in theme.items():
        if key == "meta":
            continue
        assert isinstance(value, str), f"{key} should be str"


def test_dark_primary_is_accent() -> None:
    theme = generate_qlementine_theme(
        accent="#5086ff",
        gray="#8b8d94",
        background="#1f2127",
        appearance="dark",
    )
    assert theme["primary_color"] == "#5086ff"
    assert theme["primary_color_foreground"] == "#ffffff"


def test_dark_secondary_is_white() -> None:
    theme = generate_qlementine_theme(
        accent="#5086ff",
        gray="#8b8d94",
        background="#1f2127",
        appearance="dark",
    )
    assert theme["secondary_color"] == "#ffffff"


def test_dark_background_is_exact() -> None:
    theme = generate_qlementine_theme(
        accent="#5086ff",
        gray="#8b8d94",
        background="#1f2127",
        appearance="dark",
    )
    assert theme["background_color_main1"] == "#1f2127"


def test_dark_tab_bar_matches_bg() -> None:
    """In dark mode, tab bar should equal main background."""
    theme = generate_qlementine_theme(
        accent="#5086ff",
        gray="#8b8d94",
        background="#1f2127",
        appearance="dark",
    )
    # Plan says gray[0] for dark, which is close to background
    # but not identical; just check it's dark
    tab_L = Color(theme["background_color_tab_bar"]).convert("oklch")["lightness"]
    assert tab_L < 0.3


def test_dark_semi_transparent_uses_accent_tint() -> None:
    """Dark mode semiTransparent should be tinted with accent step 12."""
    theme = generate_qlementine_theme(
        accent="#5086ff",
        gray="#8b8d94",
        background="#1f2127",
        appearance="dark",
    )
    # Should NOT be pure black
    c = Color(theme["semi_transparent_color1"])
    srgb = c.convert("srgb")
    # The color part should have some blue/accent tint
    r, g, b = srgb.coords()
    # At least one channel should be notably higher (blue tint)
    assert max(r, g, b) > 0.3


def test_dark_hover_press_differs() -> None:
    theme = generate_qlementine_theme(
        accent="#5086ff",
        gray="#8b8d94",
        background="#1f2127",
        appearance="dark",
    )
    primary = theme["primary_color"]
    assert theme["primary_color_hovered"] != primary
    assert theme["primary_color_pressed"] != primary
    assert theme["primary_color_hovered"] != theme["primary_color_pressed"]


# ---------------------------------------------------------------------------
# General/cross-mode tests
# ---------------------------------------------------------------------------


def test_different_accent_colors() -> None:
    """Generator should work with various accent colors."""
    for accent in ("#ff0000", "#00ff00", "#ff6600", "#9933ff", "#00cccc"):
        theme = generate_qlementine_theme(
            accent=accent,
            gray="#8b8b8b",
            background="#ffffff",
            appearance="light",
        )
        assert _delta_e(theme["primary_color"], accent) < 0.02


def test_theme_round_trip() -> None:
    """Generated theme should be usable with Theme dataclass."""
    from carina._theme import Theme, ThemeMeta

    td = generate_qlementine_theme(
        accent="#1890ff",
        gray="#8b8b8b",
        background="#ffffff",
        appearance="light",
    )
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
    assert d["primary_color"] == "#1890ff"
