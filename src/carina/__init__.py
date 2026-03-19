"""Stylesheet free theming for Qt applications."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("carina")
except PackageNotFoundError:
    __version__ = "uninstalled"
__author__ = "Talley Lambert"
__email__ = "talley.lambert@gmail.com"
