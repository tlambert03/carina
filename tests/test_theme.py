from __future__ import annotations

import importlib
import sys
import typing
from dataclasses import fields

from carina._theme import Theme, ThemeMeta

if typing.TYPE_CHECKING:
    from carina._theme import ThemeDict, ThemeMetaDict


def _get_typeddict_classes() -> tuple[type[ThemeMetaDict], type[ThemeDict]]:
    """Import _theme with TYPE_CHECKING=True to access TypedDicts."""
    mod_name = "carina._theme"
    saved = sys.modules.pop(mod_name, None)
    orig = typing.TYPE_CHECKING
    try:
        typing.TYPE_CHECKING = True
        mod = importlib.import_module(mod_name)
        importlib.reload(mod)
        return mod.ThemeMetaDict, mod.ThemeDict
    finally:
        typing.TYPE_CHECKING = orig
        if saved is not None:
            sys.modules[mod_name] = saved


def test_dataclasses_match_typeddicts() -> None:
    ThemeMetaDict, ThemeDict = _get_typeddict_classes()
    for dc, td in [(ThemeMeta, ThemeMetaDict), (Theme, ThemeDict)]:
        dc_fields = {f.name for f in fields(dc)}
        td_keys = set(td.__annotations__)
        assert dc_fields == td_keys, (
            f"{dc.__name__} / {td.__name__} mismatch: "
            f"extra in dc={dc_fields - td_keys}, "
            f"extra in td={td_keys - dc_fields}"
        )
