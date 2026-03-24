"""Look up pre-built Radix UI 12-step color scales.

Loads vendored scales from _radix_scales.json (pre-computed sRGB hex).
"""

from __future__ import annotations

import json
from functools import cache
from pathlib import Path

# ---------------------------------------------------------------------------
# Scale name constants
# ---------------------------------------------------------------------------

# Gray names must be listed explicitly since the JSON doesn't distinguish them.
GRAY_SCALE_NAMES = frozenset(("gray", "mauve", "slate", "sage", "olive", "sand"))

# Default pairings: each gray tint that best matches a chromatic family.
GRAY_FOR_SCALE: dict[str, str] = {
    "tomato": "mauve",
    "red": "mauve",
    "ruby": "mauve",
    "crimson": "mauve",
    "pink": "mauve",
    "plum": "mauve",
    "purple": "mauve",
    "violet": "mauve",
    "iris": "slate",
    "indigo": "slate",
    "blue": "slate",
    "cyan": "slate",
    "teal": "sage",
    "jade": "sage",
    "green": "sage",
    "grass": "olive",
    "brown": "sand",
    "orange": "sand",
    "sky": "slate",
    "mint": "sage",
    "lime": "olive",
    "yellow": "sand",
    "amber": "sand",
}

# Default backgrounds for dark mode, per gray tint.
DARK_BACKGROUNDS: dict[str, str] = {
    "gray": "#111111",
    "mauve": "#121113",
    "slate": "#111113",
    "sage": "#101211",
    "olive": "#111210",
    "sand": "#111110",
}

# Light mode always uses white.
LIGHT_BACKGROUND = "#ffffff"

# Pre-computed accent contrast colors (text color for step 9).
# Most scales use white; only the light-valued scales need a dark color.
_ACCENT_CONTRASTS: dict[str, str] = {
    "sky": "#05262e",
    "skyDark": "#05262e",
    "mint": "#062822",
    "mintDark": "#062822",
    "lime": "#1d250f",
    "limeDark": "#1d250f",
    "yellow": "#25220a",
    "yellowDark": "#25220a",
    "amber": "#2a2009",
    "amberDark": "#2a2009",
}


# ---------------------------------------------------------------------------
# Scale data
# ---------------------------------------------------------------------------


@cache
def _raw_scales() -> dict[str, list[str]]:
    data_path = Path(__file__).parent / "_radix_scales.json"
    return json.loads(data_path.read_bytes())


@cache
def scale_names() -> tuple[str, ...]:
    """Return all available scale names, derived from the JSON keys."""
    return tuple(k for k in _raw_scales() if not k.endswith("Dark"))


def get_scale(name: str, appearance: str) -> list[str]:
    """Return a 12-step Radix scale as sRGB hex strings.

    Parameters
    ----------
    name : str
        Scale name (e.g. "blue", "gray", "mauve").
    appearance : str
        "light" or "dark".
    """
    raw = _raw_scales()
    key = name if appearance == "light" else name + "Dark"
    if key not in raw:
        raise ValueError(
            f"Unknown scale {name!r} for appearance {appearance!r}. "
            f"Available: {', '.join(scale_names())}"
        )
    return raw[key]


def get_accent_contrast(name: str, appearance: str) -> str:
    """Return the contrast text color for step 9 of a named scale."""
    key = name if appearance == "light" else name + "Dark"
    return _ACCENT_CONTRASTS.get(key, "#ffffff")
