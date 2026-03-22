from __future__ import annotations

from typing import TYPE_CHECKING

from carina._qt.Qlementine import Theme
from carina._qt.QtCore import QEvent, QJsonDocument, QSize, Signal
from carina._qt.QtGui import QColor, QPainter
from carina._qt.QtWidgets import (
    QColorDialog,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
from carina._theme import make_qlementine_theme

if TYPE_CHECKING:
    from carina._theme import ThemeDict

# ---------------------------------------------------------------------------
# ColorEditor — color swatch + hex line edit with live dialog updates
# ---------------------------------------------------------------------------

_SWATCH_SIZE = 24


class _ColorSwatch(QPushButton):
    """Small button that displays a solid color."""

    def __init__(self, color: QColor, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._color = QColor(color)
        self.setFixedSize(_SWATCH_SIZE, _SWATCH_SIZE)

    def setColor(self, color: QColor) -> None:
        if self._color != color:
            self._color = QColor(color)
            self.update()

    def paintEvent(self, event: object) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(self.palette().mid().color())
        p.setBrush(self._color)
        p.drawEllipse(self.rect().adjusted(1, 1, -1, -1))
        p.end()


def _color_to_hex(color: QColor) -> str:
    if color.alpha() < 255:
        return color.name(QColor.NameFormat.HexArgb)
    return color.name(QColor.NameFormat.HexRgb)


class ColorEditor(QWidget):
    """Color swatch + hex line edit with two-way sync and live dialog."""

    colorChanged = Signal()

    def __init__(
        self, color: QColor | None = None, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        if color is None:
            color = QColor("black")
        self._color = QColor(color)
        self._updating = False

        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)

        self._swatch = _ColorSwatch(color, self)
        self._swatch.clicked.connect(self._open_dialog)
        lay.addWidget(self._swatch)

        self._line_edit = QLineEdit(self)
        self._line_edit.setText(_color_to_hex(color))
        self._line_edit.editingFinished.connect(self._on_text_edited)
        lay.addWidget(self._line_edit)

        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

    def color(self) -> QColor:
        return self._color

    def setColor(self, color: QColor) -> None:
        if self._color == color:
            return
        self._color = QColor(color)
        self._sync_widgets()
        self.colorChanged.emit()

    def _sync_widgets(self) -> None:
        """Push current color to swatch and line edit without re-emitting."""
        self._updating = True
        self._swatch.setColor(self._color)
        self._line_edit.setText(_color_to_hex(self._color))
        self._updating = False

    def _on_text_edited(self) -> None:
        if self._updating:
            return
        candidate = QColor(self._line_edit.text().strip())
        if candidate.isValid():
            self._color = candidate
            self._swatch.setColor(candidate)
            # Normalize display to hex
            self._line_edit.setText(_color_to_hex(candidate))
            self.colorChanged.emit()

    def _open_dialog(self) -> None:
        original = QColor(self._color)
        dlg = QColorDialog(self)
        dlg.setOption(QColorDialog.ColorDialogOption.DontUseNativeDialog)
        dlg.setOption(QColorDialog.ColorDialogOption.ShowAlphaChannel)
        dlg.setCurrentColor(self._color)
        # Block PaletteChange events on the dialog and all its children.
        # Our live colorChanged signal triggers style.setTheme() →
        # QApplication.setPalette(), which would corrupt the dialog's
        # internal color picker state without this filter.
        blocker = _PaletteChangeFilter(dlg)
        dlg.installEventFilter(blocker)
        for child in dlg.findChildren(QWidget):
            child.installEventFilter(blocker)
        dlg.currentColorChanged.connect(self._on_dialog_color)
        if dlg.exec():
            self.setColor(dlg.selectedColor())
        else:
            self.setColor(original)

    def _on_dialog_color(self, color: QColor) -> None:
        """Live update as user picks in the dialog."""
        self._color = QColor(color)
        self._sync_widgets()
        self.colorChanged.emit()


class _PaletteChangeFilter(QWidget):
    """Event filter that blocks PaletteChange on the color dialog."""

    def eventFilter(self, watched: object, event: object) -> bool:
        if isinstance(event, QEvent) and event.type() == QEvent.Type.PaletteChange:
            return True
        return super().eventFilter(watched, event)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Color / geometry data definitions
# ---------------------------------------------------------------------------

# Stateful color groups: (section_label, base_attr, has_transparent)
# Pattern: base, baseHovered, basePressed, baseDisabled[, baseTransparent]
_STATEFUL_COLORS: list[tuple[str, str, bool]] = [
    ("Neutral", "neutralColor", True),
    ("Primary", "primaryColor", True),
    ("Primary Foreground", "primaryColorForeground", True),
    ("Primary Alternative", "primaryAlternativeColor", True),
    ("Secondary", "secondaryColor", True),
    ("Secondary Foreground", "secondaryColorForeground", True),
    ("Secondary Alternative", "secondaryAlternativeColor", True),
    ("Border", "borderColor", True),
]

# Status color groups: (section_label, base_attr)
# Pattern: base, baseHovered, basePressed, baseDisabled (no Transparent)
_STATUS_COLORS: list[tuple[str, str]] = [
    ("Status Success", "statusColorSuccess"),
    ("Status Info", "statusColorInfo"),
    ("Status Warning", "statusColorWarning"),
    ("Status Error", "statusColorError"),
    ("Status Foreground", "statusColorForeground"),
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
            ("backgroundColorMainTransparent", "Main Transparent"),
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
            ("shadowColorTransparent", "Shadow Transparent"),
        ],
    ),
    (
        "Semi-transparent",
        [
            ("semiTransparentColor1", "Level 1"),
            ("semiTransparentColor2", "Level 2"),
            ("semiTransparentColor3", "Level 3"),
            ("semiTransparentColor4", "Level 4"),
            ("semiTransparentColorTransparent", "Transparent"),
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
            ("menuItemBorderRadius", "Menu Item Radius", "float", 0, 20),
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
            ("iconSizeMedium", "Medium", "size", 4, 64),
            ("iconSizeLarge", "Large", "size", 4, 64),
            ("iconSizeExtraSmall", "Extra Small", "size", 4, 64),
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
            for section, base, has_trans in _STATEFUL_COLORS:
                result.append((section, base, "Normal"))
                if has_trans:
                    result.append((section, f"{base}Transparent", "Transparent"))
            for section, base in _STATUS_COLORS:
                label = section.removeprefix("Status ")
                result.append(("Status", base, label))
        else:
            suffix = state  # "Hovered", "Pressed", or "Disabled"
            for section, base, _ in _STATEFUL_COLORS:
                result.append((section, f"{base}{suffix}", suffix))
            for section, base in _STATUS_COLORS:
                label = section.removeprefix("Status ")
                result.append(("Status", f"{base}{suffix}", label))

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

                    def _on_size(_, a=attr, ws=w_spin, hs=h_spin) -> None:
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

        layout = QVBoxLayout(self)

        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)
        for state in ("Active", "Hovered", "Pressed", "Disabled"):
            tab = Colors(self._theme, state)
            tab.changed.connect(self._on_changed)
            tab_widget.addTab(tab, state)
            self._tabs.append(tab)

        geo = Geometries(self._theme)
        geo.changed.connect(self._on_changed)
        tab_widget.addTab(geo, "Geometry")
        self._tabs.append(geo)

        dump_btn = QPushButton("Dump JSON to stdout")
        dump_btn.clicked.connect(self._dump_json)
        layout.addWidget(dump_btn)

    def _on_changed(self) -> None:
        # Roundtrip through JSON so the C++ Theme re-runs initializePalette()
        # (mutating attributes in-place leaves theme.palette stale).
        self._theme = Theme.fromJsonDoc(self._theme.toJson())
        for tab in self._tabs:
            tab._theme = self._theme
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

    # -- dump ---------------------------------------------------------------

    def _dump_json(self) -> None:
        doc = self._theme.toJson()
        print(bytes(doc.toJson(QJsonDocument.JsonFormat.Indented)).decode())
