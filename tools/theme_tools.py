"""Theme tester and editor for Qlementine themes."""

from __future__ import annotations

import sys

from carina._editor import ThemeEditor
from carina._qt.Qlementine import (
    AutoIconColor,
    CommandLinkButton,
    Label,
    LineEdit,
    QlementineStyle,
    Status,
    StatusBadge,
    StatusBadgeWidget,
    Switch,
    TextRole,
)
from carina._qt.QtCore import Qt
from carina._qt.QtGui import QAction
from carina._qt.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDial,
    QDockWidget,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMenu,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSlider,
    QSpinBox,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

# ---------------------------------------------------------------------------
# ThemeTester
# ---------------------------------------------------------------------------


class ThemeTester(QWidget):
    """Minimal set of QWidgets that exercises every theme color."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        tabs = QTabWidget()
        tabs.setTabsClosable(True)
        tabs.setMovable(True)
        layout.addWidget(tabs)

        tabs.addTab(self._build_controls_tab(), "Controls")
        tabs.addTab(self._build_data_tab(), "Data Views")

    # -- Controls tab -------------------------------------------------------

    def _build_controls_tab(self) -> QWidget:
        page = QScrollArea()
        page.setWidgetResizable(True)
        widget = QWidget()
        columns = QHBoxLayout(widget)
        left = QVBoxLayout()
        right = QVBoxLayout()
        columns.addLayout(left, 1)
        columns.addLayout(right, 1)

        left.addWidget(self._build_buttons())
        left.addWidget(self._build_inputs())
        left.addStretch()

        right.addWidget(self._build_toggles())
        right.addWidget(self._build_range())
        right.addWidget(self._build_status())
        right.addWidget(self._build_labels())
        right.addWidget(self._build_group_boxes())
        right.addStretch()

        page.setWidget(widget)
        return page

    def _build_buttons(self) -> QGroupBox:
        box = QGroupBox("Buttons")
        lay = QVBoxLayout(box)

        row1 = QHBoxLayout()
        primary = QPushButton("Primary")
        primary.setDefault(True)
        row1.addWidget(primary)
        dis = QPushButton("Primary Disabled")
        dis.setDefault(True)
        dis.setEnabled(False)
        row1.addWidget(dis)
        lay.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QPushButton("Secondary"))
        sec_dis = QPushButton("Sec. Disabled")
        sec_dis.setEnabled(False)
        row2.addWidget(sec_dis)
        lay.addLayout(row2)

        row3 = QHBoxLayout()
        flat = QPushButton("Flat")
        flat.setFlat(True)
        row3.addWidget(flat)
        menu_btn = QPushButton("With Menu")
        menu = QMenu(menu_btn)
        menu.addAction(QAction("Action 1", menu))
        menu.addAction(QAction("Action 2", menu))
        menu.addSeparator()
        menu.addAction(QAction("Action 3", menu))
        menu_btn.setMenu(menu)
        row3.addWidget(menu_btn)
        lay.addLayout(row3)

        row4 = QHBoxLayout()
        cmd = CommandLinkButton(box)
        cmd.setText("Command Link")
        cmd.setDescription("Description text underneath")
        row4.addWidget(cmd)
        cmd_dis = CommandLinkButton(box)
        cmd_dis.setText("Disabled")
        cmd_dis.setDescription("Disabled description")
        cmd_dis.setEnabled(False)
        row4.addWidget(cmd_dis)
        lay.addLayout(row4)

        return box

    def _build_toggles(self) -> QGroupBox:
        box = QGroupBox("Toggles")
        lay = QVBoxLayout(box)

        row1 = QHBoxLayout()
        cb_on = QCheckBox("Checked")
        cb_on.setChecked(True)
        row1.addWidget(cb_on)
        row1.addWidget(QCheckBox("Unchecked"))
        cb_dis = QCheckBox("Disabled")
        cb_dis.setChecked(True)
        cb_dis.setEnabled(False)
        row1.addWidget(cb_dis)
        lay.addLayout(row1)

        row2 = QHBoxLayout()
        rb1 = QRadioButton("Selected")
        rb1.setChecked(True)
        row2.addWidget(rb1)
        row2.addWidget(QRadioButton("Unselected"))
        rb_dis = QRadioButton("Disabled")
        rb_dis.setEnabled(False)
        row2.addWidget(rb_dis)
        lay.addLayout(row2)

        row3 = QHBoxLayout()
        sw_on = Switch(box)
        sw_on.setText("On")
        sw_on.setChecked(True)
        row3.addWidget(sw_on)
        sw_off = Switch(box)
        sw_off.setText("Off")
        row3.addWidget(sw_off)
        sw_dis = Switch(box)
        sw_dis.setText("Disabled")
        sw_dis.setChecked(True)
        sw_dis.setEnabled(False)
        row3.addWidget(sw_dis)
        lay.addLayout(row3)

        return box

    def _build_inputs(self) -> QGroupBox:
        box = QGroupBox("Inputs")
        lay = QVBoxLayout(box)

        le = LineEdit(box)
        le.setPlaceholderText("Normal input")
        le.setClearButtonEnabled(True)
        lay.addWidget(le)

        for status, text in [
            (Status.Error, "Error status"),
            (Status.Warning, "Warning status"),
            (Status.Success, "Success status"),
        ]:
            sle = LineEdit(box)
            sle.setPlaceholderText(text)
            sle.setStatus(status)
            lay.addWidget(sle)

        le_dis = LineEdit(box)
        le_dis.setPlaceholderText("Disabled input")
        le_dis.setEnabled(False)
        lay.addWidget(le_dis)

        row = QHBoxLayout()
        spin = QSpinBox(box)
        spin.setRange(0, 100)
        spin.setValue(42)
        row.addWidget(spin)
        spin_dis = QSpinBox(box)
        spin_dis.setEnabled(False)
        row.addWidget(spin_dis)
        lay.addLayout(row)

        row2 = QHBoxLayout()
        combo = QComboBox(box)
        combo.addItems(["Option 1", "Option 2", "Option 3"])
        row2.addWidget(combo)
        combo_dis = QComboBox(box)
        combo_dis.addItems(["Disabled"])
        combo_dis.setEnabled(False)
        row2.addWidget(combo_dis)
        lay.addLayout(row2)

        return box

    def _build_range(self) -> QGroupBox:
        box = QGroupBox("Range")
        lay = QVBoxLayout(box)

        slider = QSlider(Qt.Orientation.Horizontal, box)
        slider.setRange(0, 100)
        slider.setValue(40)
        slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        slider.setTickInterval(10)
        lay.addWidget(slider)

        slider_dis = QSlider(Qt.Orientation.Horizontal, box)
        slider_dis.setRange(0, 100)
        slider_dis.setValue(40)
        slider_dis.setTickPosition(QSlider.TickPosition.TicksBelow)
        slider_dis.setTickInterval(10)
        slider_dis.setEnabled(False)
        lay.addWidget(slider_dis)

        progress = QProgressBar(box)
        progress.setRange(0, 100)
        progress.setValue(60)
        lay.addWidget(progress)

        prog_dis = QProgressBar(box)
        prog_dis.setRange(0, 100)
        prog_dis.setValue(60)
        prog_dis.setEnabled(False)
        lay.addWidget(prog_dis)

        dial_row = QHBoxLayout()
        dial = QDial(box)
        dial.setRange(0, 100)
        dial.setValue(50)
        dial.setNotchesVisible(True)
        dial.setFixedSize(64, 64)
        dial_row.addWidget(dial)
        dial_dis = QDial(box)
        dial_dis.setRange(0, 100)
        dial_dis.setValue(50)
        dial_dis.setNotchesVisible(True)
        dial_dis.setFixedSize(64, 64)
        dial_dis.setEnabled(False)
        dial_row.addWidget(dial_dis)
        dial_row.addStretch()
        lay.addLayout(dial_row)

        return box

    def _build_status(self) -> QGroupBox:
        box = QGroupBox("Status Badges")
        lay = QHBoxLayout(box)
        for badge in (
            StatusBadge.Success,
            StatusBadge.Info,
            StatusBadge.Warning,
            StatusBadge.Error,
        ):
            w = StatusBadgeWidget(badge, box)
            lay.addWidget(w)
            lay.addWidget(QLabel(badge.name))
        lay.addStretch()
        return box

    def _build_labels(self) -> QGroupBox:
        box = QGroupBox("Labels")
        grid = QHBoxLayout(box)

        left = QVBoxLayout()
        lbl = Label(box)
        lbl.setText("Normal label")
        left.addWidget(lbl)
        cap = Label(box)
        cap.setText("Caption text")
        cap.setRole(TextRole.Caption)
        left.addWidget(cap)

        right = QVBoxLayout()
        lbl_dis = Label(box)
        lbl_dis.setText("Disabled label")
        lbl_dis.setEnabled(False)
        right.addWidget(lbl_dis)
        cap_dis = Label(box)
        cap_dis.setText("Disabled caption")
        cap_dis.setRole(TextRole.Caption)
        cap_dis.setEnabled(False)
        right.addWidget(cap_dis)

        grid.addLayout(left)
        grid.addLayout(right)
        grid.addStretch()
        return box

    def _build_group_boxes(self) -> QWidget:
        outer = QWidget()
        lay = QHBoxLayout(outer)
        lay.setContentsMargins(0, 0, 0, 0)

        active = QGroupBox("Active GroupBox")
        al = QVBoxLayout(active)
        al.addWidget(QLabel("Content inside"))
        lay.addWidget(active)

        disabled = QGroupBox("Disabled GroupBox")
        dl = QVBoxLayout(disabled)
        dl.addWidget(QLabel("Content inside"))
        disabled.setEnabled(False)
        lay.addWidget(disabled)

        return outer

    # -- Data Views tab -----------------------------------------------------

    def _build_data_tab(self) -> QWidget:
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # List with checkable items  →  primaryAlternativeColor, scrollbar colors
        list_w = QListWidget()
        list_w.setAlternatingRowColors(True)
        for i in range(20):
            item = QListWidgetItem(f"Item {i + 1}")
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(
                Qt.CheckState.Checked if i % 3 == 0 else Qt.CheckState.Unchecked
            )
            list_w.addItem(item)
        list_w.setCurrentRow(0)
        splitter.addWidget(list_w)

        # Table  →  header bg/fg, grid lines
        table = QTableWidget(8, 3)
        table.setHorizontalHeaderLabels(["Name", "Value", "Type"])
        for r in range(8):
            for c in range(3):
                table.setItem(r, c, QTableWidgetItem(f"Cell {r},{c}"))
        table.horizontalHeader().setStretchLastSection(True)
        splitter.addWidget(table)

        return splitter


# ---------------------------------------------------------------------------
# Main window
# ---------------------------------------------------------------------------


class ThemeToolsWindow(QMainWindow):
    """Main window with ThemeTester as central widget and ThemeEditor in dock."""

    def __init__(self, style: QlementineStyle) -> None:
        super().__init__()
        self.setWindowTitle("Qlementine Theme Tools")

        # Menu bar
        file_menu = self.menuBar().addMenu("File")
        file_menu.addAction(QAction("Open", self))
        file_menu.addAction(QAction("Save", self))
        file_menu.addSeparator()
        quit_act = QAction("Quit", self)
        quit_act.triggered.connect(self.close)
        file_menu.addAction(quit_act)

        edit_menu = self.menuBar().addMenu("Edit")
        edit_menu.addAction(QAction("Undo", self))
        edit_menu.addAction(QAction("Redo", self))

        # Tool bar
        toolbar = QToolBar("Main", self)
        toolbar.addAction(QAction("New", self))
        toolbar.addAction(QAction("Open", self))
        toolbar.addSeparator()
        toolbar.addAction(QAction("Save", self))
        self.addToolBar(toolbar)

        # Status bar with tooltip
        tip_label = QLabel("Hover here for tooltip")
        tip_label.setToolTip("This is a tooltip \u2014 demonstrates tooltip colors")
        self.statusBar().addWidget(tip_label)

        # Central widget
        self.setCentralWidget(ThemeTester(self))

        # Dock: ThemeEditor
        dock = QDockWidget("Theme Editor", self)
        editor = ThemeEditor(style.theme(), dock)
        editor.themeChanged.connect(style.setTheme)
        dock.setWidget(editor)
        dock.setMinimumWidth(380)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

        self.resize(1250, 850)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Qlementine Theme Tools")

    style = QlementineStyle(app)
    style.setAutoIconColor(AutoIconColor.TextColor)
    style.setAnimationsEnabled(True)
    app.setStyle(style)

    window = ThemeToolsWindow(style)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
