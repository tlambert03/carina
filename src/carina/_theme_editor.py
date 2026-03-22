from __future__ import annotations

from typing import TYPE_CHECKING, Any

from carina._color_editor import ColorEditor
from carina._qt.Qlementine import Theme
from carina._qt.QtCore import QEvent, QJsonDocument, QSize, Signal
from carina._qt.QtGui import QKeySequence
from carina._qt.QtWidgets import (
    QApplication,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
from carina._theme import make_qlementine_theme

if TYPE_CHECKING:
    from carina._theme import ThemeDict

# ---------------------------------------------------------------------------
# Color / geometry data definitions
# ---------------------------------------------------------------------------

# Color groups with interaction-state variants: (section, base_attr, label)
# Each base_attr expands to: base, baseHovered, basePressed, baseDisabled
# NOTE: *Transparent variants are derived by qlementine, not editable.
_VARIANT_COLORS: list[tuple[str, str, str]] = [
    ("Neutral", "neutralColor", "Neutral"),
    ("Primary", "primaryColor", "Primary"),
    ("Primary Foreground", "primaryColorForeground", "Foreground"),
    ("Primary Alternative", "primaryAlternativeColor", "Alternative"),
    ("Secondary", "secondaryColor", "Secondary"),
    ("Secondary Foreground", "secondaryColorForeground", "Foreground"),
    ("Secondary Alternative", "secondaryAlternativeColor", "Alternative"),
    ("Border", "borderColor", "Border"),
    ("Status", "statusColorSuccess", "Success"),
    ("Status", "statusColorInfo", "Info"),
    ("Status", "statusColorWarning", "Warning"),
    ("Status", "statusColorError", "Error"),
    # ("Status", "statusColorForeground", "Foreground"),  # not serialized by qlementine toJson()
]

# Standalone colors (Active tab only): (section_label, [(attr, label), ...])
_STANDALONE_COLORS: list[tuple[str, list[tuple[str, str]]]] = [
    (
        "Background",
        [
            ("backgroundColorMain1", "Main 1"),
            ("backgroundColorMain2", "Main 2"),
            ("backgroundColorMain3", "Main 3"),
            ("backgroundColorMain4", "Main 4"),
            # ("backgroundColorMainTransparent", "Main Transparent"),  # derived by qlementine
            ("backgroundColorWorkspace", "Workspace"),
            ("backgroundColorTabBar", "Tab Bar"),
        ],
    ),
    ("Focus", [("focusColor", "Focus")]),
    (
        "Shadow",
        [
            ("shadowColor1", "Shadow 1"),
            ("shadowColor2", "Shadow 2"),
            ("shadowColor3", "Shadow 3"),
            # ("shadowColorTransparent", "Shadow Transparent"),  # derived by qlementine
        ],
    ),
    (
        "Semi-transparent",
        [
            ("semiTransparentColor1", "Level 1"),
            ("semiTransparentColor2", "Level 2"),
            ("semiTransparentColor3", "Level 3"),
            ("semiTransparentColor4", "Level 4"),
            # ("semiTransparentColorTransparent", "Transparent"),  # derived by qlementine
        ],
    ),
]

# Geometry properties: (section, [(attr, label, type, min, max), ...])
_GEOMETRY_PROPS: list[tuple[str, list[tuple[str, str, str, int, int]]]] = [
    (
        "Border & Radius",
        [
            ("borderRadius", "Border Radius", "float", 0, 30),
            ("checkBoxBorderRadius", "Checkbox Radius", "float", 0, 20),
            # ("menuItemBorderRadius", ...),  # not serialized by qlementine
            ("menuBarItemBorderRadius", "MenuBar Item Radius", "float", 0, 20),
            ("borderWidth", "Border Width", "int", 0, 10),
            ("focusBorderWidth", "Focus Border Width", "int", 0, 10),
        ],
    ),
    (
        "Control Sizes",
        [
            ("controlHeightLarge", "Height Large", "int", 8, 64),
            ("controlHeightMedium", "Height Medium", "int", 8, 64),
            ("controlHeightSmall", "Height Small", "int", 4, 32),
            ("controlDefaultWidth", "Default Width", "int", 32, 256),
        ],
    ),
    (
        "Spacing",
        [
            ("spacing", "Spacing", "int", 0, 32),
            ("scrollBarMargin", "Scrollbar Margin", "int", 0, 16),
        ],
    ),
    (
        "Slider",
        [
            ("sliderTickSize", "Tick Size", "int", 0, 16),
            ("sliderTickSpacing", "Tick Spacing", "int", 0, 16),
            ("sliderTickThickness", "Tick Thickness", "int", 0, 8),
            ("sliderGrooveHeight", "Groove Height", "int", 1, 16),
        ],
    ),
    (
        "Dial",
        [
            ("dialMarkLength", "Mark Length", "int", 0, 20),
            ("dialMarkThickness", "Mark Thickness", "int", 0, 10),
            ("dialTickLength", "Tick Length", "int", 0, 16),
            ("dialTickSpacing", "Tick Spacing", "int", 0, 16),
            ("dialGrooveThickness", "Groove Thickness", "int", 1, 16),
        ],
    ),
    ("Progress Bar", [("progressBarGrooveHeight", "Groove Height", "int", 1, 16)]),
    (
        "Scroll Bar",
        [
            ("scrollBarThicknessFull", "Thickness Full", "int", 4, 32),
            ("scrollBarThicknessSmall", "Thickness Small", "int", 2, 16),
        ],
    ),
    (
        "Tab Bar",
        [
            ("tabBarPaddingTop", "Padding Top", "int", 0, 20),
            ("tabBarTabMaxWidth", "Tab Max Width", "int", 0, 500),
            ("tabBarTabMinWidth", "Tab Min Width", "int", 0, 200),
        ],
    ),
    (
        "Icon Sizes",
        [
            ("iconSize", "Default", "size", 4, 64),
            # ("iconSizeMedium", ...),  # derived from iconSize
            # ("iconSizeLarge", ...),  # derived from iconSize
            # ("iconSizeExtraSmall", ...),  # derived from iconSize
        ],
    ),
    (
        "Animation",
        [
            ("animationDuration", "Duration (ms)", "int", 0, 1000),
            ("focusAnimationDuration", "Focus (ms)", "int", 0, 1000),
            ("sliderAnimationDuration", "Slider (ms)", "int", 0, 1000),
        ],
    ),
]


# ---------------------------------------------------------------------------
# Colors - one scroll-area per interaction state
# ---------------------------------------------------------------------------


class Colors(QScrollArea):
    """Color editors for a single interaction state (Active/Hovered/…)."""

    changed = Signal()
    batchStarted = Signal()
    batchFinished = Signal()

    def __init__(self, theme: Theme, state: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._theme = theme
        self._state = state
        self._editors: dict[str, ColorEditor] = {}
        self._updating = False

        self.setWidgetResizable(True)
        content = QWidget()
        lay = QVBoxLayout(content)

        colors = self._colors_for_state(state)
        current_section: str | None = None
        form: QFormLayout | None = None

        for section, attr, label in colors:
            if section != current_section:
                box = QGroupBox(section)
                form = QFormLayout(box)
                lay.addWidget(box)
                current_section = section

            color = getattr(theme, attr)
            editor = ColorEditor(color, content)
            editor.colorChanged.connect(
                lambda *, a=attr, e=editor: self._on_color_changed(a, e)
            )
            editor.editingStarted.connect(self.batchStarted)
            editor.editingFinished.connect(self.batchFinished)
            self._editors[attr] = editor
            assert form is not None
            form.addRow(label, editor)

        lay.addStretch()
        self.setWidget(content)

    @staticmethod
    def _colors_for_state(
        state: str,
    ) -> list[tuple[str, str, str]]:
        """Return (section, attr_name, label) triples for *state*."""
        result: list[tuple[str, str, str]] = []

        if state == "Active":
            for section, attrs in _STANDALONE_COLORS:
                for attr, label in attrs:
                    result.append((section, attr, label))
            for section, base, label in _VARIANT_COLORS:
                result.append((section, base, label))
        else:
            for section, base, label in _VARIANT_COLORS:
                result.append((section, f"{base}{state}", label))

        return result

    def _on_color_changed(self, attr: str, editor: ColorEditor) -> None:
        if self._updating:
            return
        setattr(self._theme, attr, editor.color())
        self.changed.emit()

    def setTheme(self, theme: Theme) -> None:
        """Update the theme reference and refresh all editors."""
        self._theme = theme
        self._updating = True
        try:
            for attr, editor in self._editors.items():
                editor.setColor(getattr(theme, attr))
        finally:
            self._updating = False


# ---------------------------------------------------------------------------
# Geometries - single scroll-area for all geometry properties
# ---------------------------------------------------------------------------


class Geometries(QScrollArea):
    """Editors for theme geometry / sizing properties."""

    changed = Signal()

    def __init__(self, theme: Theme, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._theme = theme
        self._editors: dict[str, QSpinBox | QDoubleSpinBox | tuple] = {}
        self._updating = False

        self.setWidgetResizable(True)
        content = QWidget()
        lay = QVBoxLayout(content)

        for section, props in _GEOMETRY_PROPS:
            box = QGroupBox(section)
            form = QFormLayout(box)
            lay.addWidget(box)

            for attr, label, ptype, pmin, pmax in props:
                if ptype in ("int", "float"):
                    if ptype == "float":
                        editor = QDoubleSpinBox(content)
                        editor.setSingleStep(0.5)
                    else:
                        editor = QSpinBox(content)
                    editor.setRange(pmin, pmax)
                    editor.setValue(getattr(theme, attr))
                    editor.valueChanged.connect(
                        lambda v, a=attr: self._on_changed(a, v)
                    )
                    self._editors[attr] = editor
                    form.addRow(label, editor)

                elif ptype == "size":
                    size_val: QSize = getattr(theme, attr)
                    w_spin = QSpinBox(content)
                    w_spin.setRange(pmin, pmax)
                    w_spin.setValue(size_val.width())
                    w_spin.setPrefix("W:")
                    h_spin = QSpinBox(content)
                    h_spin.setRange(pmin, pmax)
                    h_spin.setValue(size_val.height())
                    h_spin.setPrefix("H:")

                    def _on_size(
                        _: Any,
                        a: str = attr,
                        ws: QSpinBox = w_spin,
                        hs: QSpinBox = h_spin,
                    ) -> None:
                        self._on_changed(a, QSize(ws.value(), hs.value()))

                    w_spin.valueChanged.connect(_on_size)
                    h_spin.valueChanged.connect(_on_size)
                    self._editors[attr] = (w_spin, h_spin)

                    row_w = QWidget(content)
                    row_lay = QHBoxLayout(row_w)
                    row_lay.setContentsMargins(0, 0, 0, 0)
                    row_lay.addWidget(w_spin)
                    row_lay.addWidget(h_spin)
                    form.addRow(label, row_w)

        lay.addStretch()
        self.setWidget(content)

    def _on_changed(self, attr: str, value: object) -> None:
        if self._updating:
            return
        setattr(self._theme, attr, value)
        self.changed.emit()

    def setTheme(self, theme: Theme) -> None:
        """Update the theme reference and refresh all editors."""
        self._theme = theme
        self._updating = True
        try:
            for attr, editor in self._editors.items():
                if isinstance(editor, tuple):
                    size_val: QSize = getattr(theme, attr)
                    editor[0].setValue(size_val.width())
                    editor[1].setValue(size_val.height())
                else:
                    editor.setValue(getattr(theme, attr))
        finally:
            self._updating = False


# ---------------------------------------------------------------------------
# ThemeEditor
# ---------------------------------------------------------------------------


class ThemeEditor(QWidget):
    """Editor for all theme color and geometry properties."""

    themeChanged = Signal(Theme)

    def __init__(
        self, theme: Theme | None = None, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self._theme = Theme(theme) if theme is not None else Theme()
        self._tabs: list[Colors | Geometries] = []

        # undo/redo state: list of JSON snapshots, cursor points at current
        self._undo_stack: list[QJsonDocument] = [self._theme.toJson()]
        self._undo_cursor: int = 0
        self._macro_depth: int = 0
        self._macro_changed: bool = False

        layout = QVBoxLayout(self)

        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)
        for state in ("Active", "Hovered", "Pressed", "Disabled"):
            tab = Colors(self._theme, state)
            tab.changed.connect(self._on_changed)
            tab.batchStarted.connect(self.beginMacro)
            tab.batchFinished.connect(self.endMacro)
            tab_widget.addTab(tab, state)
            self._tabs.append(tab)

        geo = Geometries(self._theme)
        geo.changed.connect(self._on_changed)
        tab_widget.addTab(geo, "Geometry")
        self._tabs.append(geo)

        dump_btn = QPushButton("Dump JSON to stdout")
        dump_btn.clicked.connect(self._dump_json)
        layout.addWidget(dump_btn)

        # Install event filter on QApp to intercept undo/redo before child
        # widgets (QSpinBox, QLineEdit) consume them as their own text undo.
        app = QApplication.instance()
        if app is not None:
            app.installEventFilter(self)

    def eventFilter(self, obj: object, event: QEvent) -> bool:
        if event.type() == QEvent.Type.KeyPress:
            w = QApplication.focusWidget()
            if w is not None and self.isAncestorOf(w):
                if event.matches(QKeySequence.StandardKey.Undo):  # type: ignore[union-attr]
                    self.undo()
                    return True
                if event.matches(QKeySequence.StandardKey.Redo):  # type: ignore[union-attr]
                    self.redo()
                    return True
        return super().eventFilter(obj, event)

    def _on_changed(self) -> None:
        # Roundtrip through JSON so the C++ Theme re-runs initializePalette()
        # (mutating attributes in-place leaves theme.palette stale).
        self._theme = Theme.fromJsonDoc(self._theme.toJson())
        for tab in self._tabs:
            tab._theme = self._theme
        self.themeChanged.emit(self._theme)

        if self._macro_depth > 0:
            # Inside a macro: live-update but defer the undo push.
            self._macro_changed = True
            return

        # push snapshot, discard any redo history
        self._push_snapshot()

    def _push_snapshot(self) -> None:
        self._undo_cursor += 1
        del self._undo_stack[self._undo_cursor :]
        self._undo_stack.append(self._theme.toJson())

    def _apply_snapshot(self, doc: QJsonDocument) -> None:
        """Restore theme from a JSON snapshot and refresh all editors."""
        self._theme = Theme.fromJsonDoc(doc)
        for tab in self._tabs:
            tab.setTheme(self._theme)
        self.themeChanged.emit(self._theme)

    # -- public API ---------------------------------------------------------

    def theme(self) -> Theme:
        """Return the current theme."""
        return self._theme

    def setTheme(self, theme: Theme | ThemeDict) -> None:
        """Replace the current theme and refresh all editors."""
        if isinstance(theme, dict):
            theme = make_qlementine_theme(theme)

        self._theme = Theme(theme)
        for tab in self._tabs:
            tab.setTheme(self._theme)

        # reset undo history to this new baseline
        self._undo_stack = [self._theme.toJson()]
        self._undo_cursor = 0

    def beginMacro(self) -> None:
        """Begin batching changes into a single undo entry."""
        self._macro_depth += 1
        self._macro_changed = False

    def endMacro(self) -> None:
        """End macro; push one undo entry if anything changed."""
        if self._macro_depth > 0:
            self._macro_depth -= 1
        if self._macro_depth == 0 and self._macro_changed:
            self._push_snapshot()
            self._macro_changed = False

    def undo(self) -> None:
        """Restore the previous theme state."""
        if self._undo_cursor > 0:
            self._undo_cursor -= 1
            self._apply_snapshot(self._undo_stack[self._undo_cursor])

    def redo(self) -> None:
        """Re-apply the next theme state."""
        if self._undo_cursor < len(self._undo_stack) - 1:
            self._undo_cursor += 1
            self._apply_snapshot(self._undo_stack[self._undo_cursor])

    def canUndo(self) -> bool:
        return self._undo_cursor > 0

    def canRedo(self) -> bool:
        return self._undo_cursor < len(self._undo_stack) - 1

    # -- dump ---------------------------------------------------------------

    def _dump_json(self) -> None:
        doc = self._theme.toJson()
        print(bytes(doc.toJson(QJsonDocument.JsonFormat.Indented)).decode())
