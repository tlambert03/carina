"""Stylesheet free theming for Qt applications."""

from importlib.metadata import PackageNotFoundError, version
from typing import TYPE_CHECKING

try:
    __version__ = version("carina")
except PackageNotFoundError:
    __version__ = "uninstalled"

__all__ = [
    "Theme",
    "ThemeMeta",
    "ThemePlayground",
    "generate_qlementine_theme",
    "generate_radix_colors",
    "make_qlementine_theme",
]

if TYPE_CHECKING:
    # only to be used for type checking
    from carina._theme import ThemeDict as ThemeDict
    from carina._theme import ThemeMetaDict as ThemeMetaDict
    from carina._theme_playground import ThemePlayground as ThemePlayground

from carina._qlementine_mapper import generate_qlementine_theme
from carina._radix_generator import generate_radix_colors
from carina._theme import Theme, ThemeMeta, make_qlementine_theme


def __getattr__(name: str) -> object:
    if name == "ThemePlayground":
        from carina._theme_playground import ThemePlayground

        return ThemePlayground
    raise AttributeError(f"module 'carina' has no attribute {name!r}")
