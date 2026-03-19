"""Stylesheet free theming for Qt applications."""

from importlib.metadata import PackageNotFoundError, version
from typing import TYPE_CHECKING

try:
    __version__ = version("carina")
except PackageNotFoundError:
    __version__ = "uninstalled"

__all__ = ["Theme", "ThemeMeta", "make_qlementine_theme"]

if TYPE_CHECKING:
    # only to be used for type checking
    from carina._theme import ThemeDict as ThemeDict
    from carina._theme import ThemeMetaDict as ThemeMetaDict

from carina._theme import Theme, ThemeMeta, make_qlementine_theme
