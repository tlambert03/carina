"""Radix-inspired theme playground for Qlementine.

A simplified theme configuration panel: pick an accent color, a gray tint,
light/dark appearance, border radius, and scaling.  The full Qlementine
palette is generated and applied live.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from carina._qlementine_mapper import generate_qlementine_theme
from carina._qt.Qlementine import Popover
from carina._qt.QtCore import QRectF, Qt, Signal
from carina._qt.QtGui import (
    QAction,
    QBrush,
    QColor,
    QFont,
    QPainter,
    QPen,
    QResizeEvent,
)
from carina._qt.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDockWidget,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSizePolicy,
    QSlider,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
from carina._theme import make_qlementine_theme

if TYPE_CHECKING:
    from carina._qt import Qlementine
    from carina._theme import ThemeDict

# ---------------------------------------------------------------------------
# Preset data
# ---------------------------------------------------------------------------

# Step-9 sRGB hex for each Radix scale (ordered by hue for the grid)
ACCENT_PRESETS: list[tuple[str, str]] = [
    ("Tomato", "#e54d2e"),
    ("Red", "#e5484d"),
    ("Ruby", "#e54666"),
    ("Crimson", "#e93d82"),
    ("Pink", "#d6409f"),
    ("Plum", "#ab4aba"),
    ("Purple", "#8e4ec6"),
    ("Violet", "#6e56cf"),
    ("Iris", "#5b5bd6"),
    ("Indigo", "#3e63dd"),
    ("Blue", "#0090ff"),
    ("Cyan", "#00a2c7"),
    ("Teal", "#12a594"),
    ("Jade", "#29a383"),
    ("Green", "#30a46c"),
    ("Grass", "#46a758"),
    ("Orange", "#f76b15"),
    ("Brown", "#ad7f58"),
    ("Sky", "#7ce2fe"),
    ("Mint", "#86ead4"),
    ("Lime", "#bdee63"),
    ("Yellow", "#ffe629"),
    ("Amber", "#ffc53d"),
]

GRAY_PRESETS: list[tuple[str, str]] = [
    ("Gray", "#8d8d8d"),
    ("Mauve", "#8e8c99"),
    ("Slate", "#8b8d98"),
    ("Sage", "#868e8b"),
    ("Olive", "#898e87"),
    ("Sand", "#8d8985"),
]


RADIUS_PRESETS: list[tuple[str, float]] = [
    ("None", 0.0),
    ("Small", 3.0),
    ("Medium", 6.0),
    ("Large", 10.0),
    ("Full", 14.0),  # half of default control height → pill-shaped buttons
]

SCALING_PRESETS: list[tuple[str, float]] = [
    ("90%", 0.90),
    ("95%", 0.95),
    ("100%", 1.00),
    ("105%", 1.05),
    ("110%", 1.10),
]

_SWATCH_SIZE = 30
_SWATCH_R = 11
_RING_R = 14
_GRID_COLS = 10

# Base Qlementine metrics (at 100% scaling)
_BASE_FONT_SIZE = 12
_BASE_HEIGHT_LARGE = 28
_BASE_HEIGHT_MEDIUM = 24
_BASE_HEIGHT_SMALL = 16
_BASE_SPACING = 6
_BASE_ICON = 16


# ---------------------------------------------------------------------------
# _ColorSwatch - clickable circle showing a single color
# ---------------------------------------------------------------------------


class _ColorSwatch(QWidget):
    """Small clickable color circle."""

    clicked = Signal()

    def __init__(self, color: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._color = QColor(color)
        self._hex = color
        self._selected = False
        self._hovered = False
        self.setFixedSize(_SWATCH_SIZE, _SWATCH_SIZE)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover)

    def hex(self) -> str:
        return self._hex

    def setSelected(self, selected: bool) -> None:
        if self._selected != selected:
            self._selected = selected
            self.update()

    def enterEvent(self, event: object) -> None:
        self._hovered = True
        self.update()

    def leaveEvent(self, event: object) -> None:
        self._hovered = False
        self.update()

    def mouseReleaseEvent(self, event: object) -> None:
        self.clicked.emit()

    def paintEvent(self, event: object) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        cx = self.width() / 2
        cy = self.height() / 2

        if self._selected:
            p.setPen(QPen(QColor(255, 255, 255, 220), 2.0))
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.drawEllipse(QRectF(cx - _RING_R, cy - _RING_R, 2 * _RING_R, 2 * _RING_R))

        r = _SWATCH_R + (1 if self._hovered and not self._selected else 0)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(self._color))
        p.drawEllipse(QRectF(cx - r, cy - r, 2 * r, 2 * r))
        p.end()




# ---------------------------------------------------------------------------
# _SwatchGrid - grid of swatches with single selection
# ---------------------------------------------------------------------------


class _SwatchGrid(QWidget):
    """Grid of color swatches with exclusive selection."""

    selectionChanged = Signal(str, str)  # (name, hex)

    def __init__(
        self,
        presets: list[tuple[str, str]],
        columns: int = _GRID_COLS,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._swatches: list[_ColorSwatch] = []
        self._selected_index: int = -1

        grid = QGridLayout(self)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(2)

        for i, (name, hex_color) in enumerate(presets):
            sw = _ColorSwatch(hex_color, self)
            sw.setToolTip(name)
            sw.clicked.connect(lambda idx=i: self._on_swatch_clicked(idx))
            row, col = divmod(i, columns)
            grid.addWidget(sw, row, col)
            self._swatches.append(sw)

    def _on_swatch_clicked(self, index: int) -> None:
        if 0 <= self._selected_index < len(self._swatches):
            self._swatches[self._selected_index].setSelected(False)
        self._selected_index = index
        sw = self._swatches[index]
        sw.setSelected(True)
        self.selectionChanged.emit(sw.toolTip(), sw.hex())

    def setCurrentIndex(self, index: int) -> None:
        self._on_swatch_clicked(index)


# ---------------------------------------------------------------------------
# _RadiusSelector - visual radius option buttons
# ---------------------------------------------------------------------------


class _RadiusButton(QPushButton):
    """Button showing a rounded-rect preview of a border radius."""

    def __init__(
        self, label: str, radius: float, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self._radius = radius
        self._label = label
        self.setCheckable(True)
        self.setFixedSize(56, 68)
        self.setToolTip(f"{label}: {radius}px")

    def paintEvent(self, event: object) -> None:
        super().paintEvent(event)
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        pal = self.palette()
        checked = self.isChecked()
        rect = QRectF(10, 6, 36, 32)
        r = min(self._radius, 16)

        # Fill
        fill = pal.highlight().color() if checked else pal.mid().color()
        p.setBrush(QBrush(fill))

        # Border — lighter stroke for contrast
        border = pal.light().color() if checked else pal.dark().color()
        p.setPen(QPen(border, 1.5))
        p.drawRoundedRect(rect, r, r)

        # Label text
        p.setPen(pal.text().color())
        font = p.font()
        font.setPointSize(8)
        p.setFont(font)
        p.drawText(
            QRectF(0, 42, self.width(), 20),
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
            self._label,
        )
        p.end()


# ---------------------------------------------------------------------------
# _SegmentedGroup - exclusive toggle button row (using QPushButtons)
# ---------------------------------------------------------------------------


class _SegmentedGroup(QWidget):
    """Row of exclusive toggle buttons."""

    currentIndexChanged = Signal(int)

    def __init__(
        self,
        options: list[str],
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(4)
        self._buttons: list[QPushButton] = []

        for i, text in enumerate(options):
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            btn.clicked.connect(lambda checked, idx=i: self._select(idx))
            lay.addWidget(btn)
            self._buttons.append(btn)

    def _select(self, index: int) -> None:
        for i, btn in enumerate(self._buttons):
            btn.setChecked(i == index)
        self.currentIndexChanged.emit(index)

    def setCurrentIndex(self, index: int) -> None:
        for i, btn in enumerate(self._buttons):
            btn.setChecked(i == index)


# ---------------------------------------------------------------------------
# ThemePanel - the configuration sidebar
# ---------------------------------------------------------------------------


class ThemePanel(QScrollArea):
    """Theme configuration panel inspired by the Radix playground."""

    themeChanged = Signal(object)  # ThemeDict
    useDefaultChanged = Signal(bool)  # True = use Qlementine default

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setMinimumWidth(340)
        self.setMaximumWidth(380)

        content = QWidget()
        lay = QVBoxLayout(content)
        lay.setSpacing(16)

        # ---------- heading + default toggle ----------
        head_row = QHBoxLayout()
        heading = QLabel("Theme")
        hfont = heading.font()
        hfont.setPointSize(18)
        hfont.setWeight(QFont.Weight.Bold)
        heading.setFont(hfont)
        head_row.addWidget(heading)
        head_row.addStretch()
        self._default_btn = QPushButton("Qlementine Default")
        self._default_btn.setCheckable(True)
        self._default_btn.clicked.connect(self._on_default_toggled)
        head_row.addWidget(self._default_btn)
        lay.addLayout(head_row)

        # ---------- accent color ----------
        lay.addWidget(self._section_label(
            "Accent color",
            "Your brand color. Used for primary buttons, active states, "
            "links, and focus rings. Uses a pre-built Radix 12-step scale.",
        ))
        self._accent_grid = _SwatchGrid(ACCENT_PRESETS, _GRID_COLS)
        self._accent_grid.selectionChanged.connect(self._on_accent_changed)
        lay.addWidget(self._accent_grid)

        # ---------- gray color ----------
        lay.addWidget(self._section_label(
            "Gray color",
            "Tints the neutral palette (backgrounds, borders, text). "
            "Pure Gray is neutral; Slate adds a cool blue tint, "
            "Mauve a purple tint, etc.",
        ))
        self._gray_grid = _SwatchGrid(GRAY_PRESETS, len(GRAY_PRESETS))
        self._gray_grid.selectionChanged.connect(self._on_gray_changed)
        lay.addWidget(self._gray_grid)

        # ---------- appearance ----------
        lay.addWidget(self._section_label("Appearance"))
        self._appearance = _SegmentedGroup(["Light", "Dark"])
        self._appearance.currentIndexChanged.connect(lambda _: self._on_any_change())
        lay.addWidget(self._appearance)

        # ---------- radius ----------
        lay.addWidget(self._section_label("Radius"))
        radius_row = QHBoxLayout()
        radius_row.setSpacing(4)
        self._radius_buttons: list[_RadiusButton] = []
        for i, (label, value) in enumerate(RADIUS_PRESETS):
            btn = _RadiusButton(label, value)
            btn.clicked.connect(lambda checked, idx=i: self._select_radius(idx))
            radius_row.addWidget(btn)
            self._radius_buttons.append(btn)
        lay.addLayout(radius_row)

        # ---------- scaling ----------
        lay.addWidget(self._section_label("Scaling"))
        self._scaling = _SegmentedGroup([s[0] for s in SCALING_PRESETS])
        self._scaling.currentIndexChanged.connect(lambda _: self._on_any_change())
        lay.addWidget(self._scaling)

        # ---------- copy theme button ----------
        lay.addSpacing(8)
        copy_btn = QPushButton("Copy Theme JSON")
        copy_btn.clicked.connect(self._copy_theme_json)
        lay.addWidget(copy_btn)

        lay.addStretch()
        self.setWidget(content)

        # ---------- defaults ----------
        self._accent_name = "blue"
        self._gray_name = "slate"
        self._appearance_mode = "light"
        self._radius = 6.0
        self._scaling_factor = 1.0

        # Set initial selections
        blue_idx = next(
            (i for i, (n, _) in enumerate(ACCENT_PRESETS) if n == "Blue"), 10
        )
        self._accent_grid.setCurrentIndex(blue_idx)
        slate_idx = next(
            (i for i, (n, _) in enumerate(GRAY_PRESETS) if n == "Slate"), 2
        )
        self._gray_grid.setCurrentIndex(slate_idx)
        self._appearance.setCurrentIndex(0)
        self._select_radius(2)  # Medium
        self._scaling.setCurrentIndex(2)  # 100%

    @staticmethod
    def _section_label(text: str, info: str = "") -> QWidget:
        if not info:
            lbl = QLabel(text)
            font = lbl.font()
            font.setWeight(QFont.Weight.DemiBold)
            lbl.setFont(font)
            return lbl

        row = QWidget()
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(4)
        lbl = QLabel(text)
        font = lbl.font()
        font.setWeight(QFont.Weight.DemiBold)
        lbl.setFont(font)
        lay.addWidget(lbl)

        info_btn = QPushButton("\u24d8")  # circled i: ⓘ
        info_btn.setFixedSize(20, 20)
        info_btn.setFlat(True)
        info_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        info_btn.setToolTip(info)

        popover_ref: list[Popover | None] = [None]

        def _toggle_info() -> None:
            if popover_ref[0] and popover_ref[0].isOpened():
                popover_ref[0].closePopover()
                return
            tip = QLabel(info)
            tip.setWordWrap(True)
            tip.setFixedWidth(260)
            tip.setContentsMargins(8, 8, 8, 8)
            p = Popover(info_btn)
            p.setAnchorWidget(info_btn)
            p.setContentWidget(tip)
            p.setPreferredPosition(Popover.Position.Bottom)
            p.setPreferredAlignment(Popover.Alignment.Begin)
            p.openPopover()
            popover_ref[0] = p

        info_btn.clicked.connect(_toggle_info)
        lay.addWidget(info_btn)
        lay.addStretch()
        return row

    def _select_radius(self, index: int) -> None:
        for i, btn in enumerate(self._radius_buttons):
            btn.setChecked(i == index)
        self._radius = RADIUS_PRESETS[index][1]
        self._on_any_change()

    def _on_default_toggled(self) -> None:
        use_default = self._default_btn.isChecked()
        self.useDefaultChanged.emit(use_default)
        if not use_default:
            self._emit_theme()

    def _on_accent_changed(self, name: str, _hex_color: str) -> None:
        self._accent_name = name.lower()
        self._emit_theme()

    def _on_gray_changed(self, name: str, _hex_color: str) -> None:
        self._gray_name = name.lower()
        self._emit_theme()

    def _on_any_change(self) -> None:
        app_idx = next(
            (i for i, btn in enumerate(self._appearance._buttons) if btn.isChecked()),
            0,
        )
        self._appearance_mode = "dark" if app_idx == 1 else "light"

        scale_idx = next(
            (i for i, btn in enumerate(self._scaling._buttons) if btn.isChecked()),
            2,
        )
        self._scaling_factor = SCALING_PRESETS[scale_idx][1]

        self._emit_theme()

    def _emit_theme(self) -> None:
        # Any custom change unchecks the default toggle
        if self._default_btn.isChecked():
            self._default_btn.setChecked(False)
            self.useDefaultChanged.emit(False)

        theme = generate_qlementine_theme(
            accent=self._accent_name,
            gray=self._gray_name,
            appearance=self._appearance_mode,
            name=f"{'Dark' if self._appearance_mode == 'dark' else 'Light'} Custom",
        )

        # Apply radius
        theme["border_radius"] = self._radius
        theme["check_box_border_radius"] = max(0, self._radius * 0.67)
        theme["menu_bar_item_border_radius"] = max(0, self._radius * 0.33)

        # Apply scaling
        f = self._scaling_factor
        theme["font_size"] = round(_BASE_FONT_SIZE * f)
        theme["control_height_large"] = round(_BASE_HEIGHT_LARGE * f)
        theme["control_height_medium"] = round(_BASE_HEIGHT_MEDIUM * f)
        theme["control_height_small"] = round(_BASE_HEIGHT_SMALL * f)
        theme["spacing"] = round(_BASE_SPACING * f)
        theme["icon_extent"] = round(_BASE_ICON * f)

        self.themeChanged.emit(theme)

    def _copy_theme_json(self) -> None:
        import json

        from carina._theme import _to_camel_case_dict

        theme = generate_qlementine_theme(
            accent=self._accent_name,
            gray=self._gray_name,
            appearance=self._appearance_mode,
        )
        theme["border_radius"] = self._radius
        f = self._scaling_factor
        theme["font_size"] = round(_BASE_FONT_SIZE * f)
        theme["control_height_large"] = round(_BASE_HEIGHT_LARGE * f)
        theme["control_height_medium"] = round(_BASE_HEIGHT_MEDIUM * f)
        theme["control_height_small"] = round(_BASE_HEIGHT_SMALL * f)
        theme["spacing"] = round(_BASE_SPACING * f)

        text = json.dumps(_to_camel_case_dict(theme), indent=2)
        clipboard = QApplication.clipboard()
        if clipboard is not None:
            clipboard.setText(text)


# ---------------------------------------------------------------------------
# DemoWidget - simple widget gallery for live preview
# ---------------------------------------------------------------------------


class _DemoControls(QWidget):
    """Widget gallery exercising the key theme colors."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setSpacing(12)
        lay.setContentsMargins(16, 16, 16, 16)

        # -- Buttons --
        btn_box = QGroupBox("Buttons")
        btn_lay = QHBoxLayout(btn_box)
        primary = QPushButton("Primary")
        primary.setDefault(True)
        btn_lay.addWidget(primary)
        btn_lay.addWidget(QPushButton("Secondary"))
        flat = QPushButton("Flat")
        flat.setFlat(True)
        btn_lay.addWidget(flat)
        disabled = QPushButton("Disabled")
        disabled.setEnabled(False)
        btn_lay.addWidget(disabled)
        lay.addWidget(btn_box)

        # -- Inputs --
        inp_box = QGroupBox("Inputs")
        inp_lay = QHBoxLayout(inp_box)
        inp_lay.addWidget(QLineEdit("Text input"))
        spin = QSpinBox()
        spin.setValue(42)
        inp_lay.addWidget(spin)
        combo = QComboBox()
        combo.addItems(["Option A", "Option B", "Option C"])
        inp_lay.addWidget(combo)
        lay.addWidget(inp_box)

        # -- Toggles --
        tog_box = QGroupBox("Toggles")
        tog_lay = QHBoxLayout(tog_box)
        cb = QCheckBox("Checkbox")
        cb.setChecked(True)
        tog_lay.addWidget(cb)
        tog_lay.addWidget(QCheckBox("Unchecked"))
        rb1 = QRadioButton("Radio A")
        rb1.setChecked(True)
        tog_lay.addWidget(rb1)
        tog_lay.addWidget(QRadioButton("Radio B"))
        lay.addWidget(tog_box)

        # -- Sliders & Progress --
        range_box = QGroupBox("Range")
        range_lay = QVBoxLayout(range_box)
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setValue(65)
        range_lay.addWidget(slider)
        progress = QProgressBar()
        progress.setValue(45)
        range_lay.addWidget(progress)
        lay.addWidget(range_box)

        # -- Labels --
        lbl_box = QGroupBox("Labels")
        lbl_lay = QVBoxLayout(lbl_box)
        lbl_lay.addWidget(QLabel("Normal label text"))
        disabled_lbl = QLabel("Disabled label")
        disabled_lbl.setEnabled(False)
        lbl_lay.addWidget(disabled_lbl)
        lay.addWidget(lbl_box)

        lay.addStretch()


class _DemoListTab(QWidget):
    """Tab with list and table widgets to show item-view backgrounds."""

    def __init__(self, parent: QWidget | None = None) -> None:
        from carina._qt.QtWidgets import QHeaderView, QTableWidget, QTableWidgetItem

        super().__init__(parent)
        lay = QVBoxLayout(self)

        # -- List --
        lw = QListWidget()
        for i in range(8):
            lw.addItem(f"List item {i + 1}")
        lw.setAlternatingRowColors(True)
        lay.addWidget(lw)

        # -- Table --
        table = QTableWidget(6, 4)
        table.setHorizontalHeaderLabels(["Name", "Status", "Value", "Notes"])
        table.setAlternatingRowColors(True)
        data = [
            ("Alpha", "Active", "42", "Primary component"),
            ("Beta", "Pending", "17", "Secondary path"),
            ("Gamma", "Complete", "93", "Verified"),
            ("Delta", "Error", "0", "Needs review"),
            ("Epsilon", "Active", "65", "In progress"),
            ("Zeta", "Disabled", "—", "Archived"),
        ]
        for row, (name, status, value, notes) in enumerate(data):
            table.setItem(row, 0, QTableWidgetItem(name))
            table.setItem(row, 1, QTableWidgetItem(status))
            table.setItem(row, 2, QTableWidgetItem(value))
            table.setItem(row, 3, QTableWidgetItem(notes))
        header = table.horizontalHeader()
        if header is not None:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        lay.addWidget(table)


class _DemoQlementineTab(QWidget):
    """Tab showing Qlementine-specific custom widgets."""

    def __init__(self, parent: QWidget | None = None) -> None:
        from carina._qt.Qlementine import (
            NavigationBar,
            SegmentedControl,
            StatusBadge,
            StatusBadgeSize,
            StatusBadgeWidget,
            Switch,
        )

        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setSpacing(16)
        lay.setContentsMargins(16, 16, 16, 16)

        # -- NavigationBar (top-level, no groupbox) --
        nav = NavigationBar()
        nav.addItem("Home", badge="3")
        nav.addItem("Search")
        nav.addItem("Notifications", badge="12")
        nav.addItem("Profile")
        nav.setCurrentIndex(0)
        lay.addWidget(nav)

        # -- SegmentedControl --
        seg_box = QGroupBox("SegmentedControl")
        seg_lay = QVBoxLayout(seg_box)
        seg = SegmentedControl()
        seg.addItem("Overview")
        seg.addItem("Details")
        seg.addItem("Settings")
        seg.setCurrentIndex(0)
        seg_lay.addWidget(seg)
        lay.addWidget(seg_box)

        # -- Switch --
        switch_box = QGroupBox("Switch")
        switch_lay = QHBoxLayout(switch_box)
        sw_on = Switch()
        sw_on.setChecked(True)
        switch_lay.addWidget(QLabel("On"))
        switch_lay.addWidget(sw_on)
        sw_off = Switch()
        switch_lay.addWidget(QLabel("Off"))
        switch_lay.addWidget(sw_off)
        sw_disabled = Switch()
        sw_disabled.setChecked(True)
        sw_disabled.setEnabled(False)
        switch_lay.addWidget(QLabel("Disabled"))
        switch_lay.addWidget(sw_disabled)
        switch_lay.addStretch()
        lay.addWidget(switch_box)

        # -- StatusBadgeWidget --
        badge_box = QGroupBox("StatusBadge")
        badge_lay = QHBoxLayout(badge_box)
        for badge_type in (
            StatusBadge.Success,
            StatusBadge.Info,
            StatusBadge.Warning,
            StatusBadge.Error,
        ):
            for size in (StatusBadgeSize.Medium, StatusBadgeSize.Small):
                badge_lay.addWidget(StatusBadgeWidget(badge_type, size))
        badge_lay.addStretch()
        lay.addWidget(badge_box)

        lay.addStretch()


# ---------------------------------------------------------------------------
# ThemePlayground - QMainWindow with toolbar, menubar, statusbar, dock
# ---------------------------------------------------------------------------


class ThemePlayground(QMainWindow):
    """Main playground: QMainWindow with full chrome + theme panel dock."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Qlementine Theme Playground")

        # -- Menu bar --
        menu_bar = self.menuBar()
        assert menu_bar is not None
        file_menu = menu_bar.addMenu("&File")
        assert file_menu is not None
        file_menu.addAction("&New")
        file_menu.addAction("&Open...")
        file_menu.addAction("&Save")
        file_menu.addSeparator()
        quit_action = file_menu.addAction("&Quit")
        assert quit_action is not None
        quit_action.setMenuRole(QAction.MenuRole.QuitRole)
        quit_action.triggered.connect(QApplication.quit)

        edit_menu = menu_bar.addMenu("&Edit")
        assert edit_menu is not None
        edit_menu.addAction("&Undo")
        edit_menu.addAction("&Redo")
        edit_menu.addSeparator()
        edit_menu.addAction("Cu&t")
        edit_menu.addAction("&Copy")
        edit_menu.addAction("&Paste")

        view_menu = menu_bar.addMenu("&View")
        assert view_menu is not None
        view_menu.addAction("Zoom &In")
        view_menu.addAction("Zoom &Out")

        help_menu = menu_bar.addMenu("&Help")
        assert help_menu is not None
        help_menu.addAction("&About")

        # -- Tool bar --
        toolbar = self.addToolBar("Main")
        assert toolbar is not None
        toolbar.addAction("New")
        toolbar.addAction("Open")
        toolbar.addAction("Save")
        toolbar.addSeparator()
        toolbar.addAction("Undo")
        toolbar.addAction("Redo")

        # -- Status bar --
        status_bar = self.statusBar()
        assert status_bar is not None
        status_bar.showMessage("Ready")

        # -- Central: tabbed demo area --
        tabs = QTabWidget()
        controls_scroll = QScrollArea()
        controls_scroll.setWidgetResizable(True)
        controls_scroll.setWidget(_DemoControls())
        tabs.addTab(controls_scroll, "Controls")
        tabs.addTab(_DemoListTab(), "List View")
        tabs.addTab(_DemoQlementineTab(), "Qlementine")
        self.setCentralWidget(tabs)

        # -- Dock: theme panel --
        dock = QDockWidget("Theme", self)
        dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable
            | QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )
        self._panel = ThemePanel()
        dock.setWidget(self._panel)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

        # Connect panel → style
        self._style: Qlementine.QlementineStyle | None = None
        self._panel.themeChanged.connect(self._apply_theme)
        self._panel.useDefaultChanged.connect(self._on_use_default)

    def setStyle(self, style: Qlementine.QlementineStyle) -> None:
        """Set the QlementineStyle instance to apply themes to."""
        self._style = style
        self._panel._emit_theme()

    def _apply_theme(self, theme_dict: ThemeDict) -> None:
        if self._style is not None:
            qt_theme = make_qlementine_theme(theme_dict)
            self._style.setTheme(qt_theme)
            self._refresh_all_widgets()

    def _on_use_default(self, use_default: bool) -> None:
        if use_default and self._style is not None:
            from carina._qt.Qlementine import Theme as QlemTheme

            self._style.setTheme(QlemTheme())
            self._refresh_all_widgets()

    @staticmethod
    def _refresh_all_widgets() -> None:
        from carina._qt.QtCore import QSize
        from carina._qt.QtWidgets import QTabBar

        for w in QApplication.allWidgets():
            if isinstance(w, QTabBar):
                # Tab bars cache tab sizes; send a resize event to force relayout
                evt = QResizeEvent(w.size(), QSize(0, 0))
                QApplication.sendEvent(w, evt)
            w.updateGeometry()
            w.update()

    def panel(self) -> ThemePanel:
        return self._panel


# ---------------------------------------------------------------------------
# Standalone entry point
# ---------------------------------------------------------------------------


def main() -> None:
    """Run the theme playground as a standalone application."""
    import sys

    from carina._qt.Qlementine import AutoIconColor, QlementineStyle

    app = QApplication(sys.argv)
    style = QlementineStyle(app)
    style.setAutoIconColor(AutoIconColor.TextColor)
    style.setAnimationsEnabled(True)
    app.setStyle(style)

    playground = ThemePlayground()
    playground.setStyle(style)
    playground.resize(1100, 800)
    playground.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
