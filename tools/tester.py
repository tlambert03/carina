import sys

from carina._editor import ThemeEditor
from carina._qt import QtWidgets as QtW
from carina._qt.Qlementine import QlementineStyle
from carina._qt.QtCore import Qt


class _Splitter(QtW.QSplitter):
    def __init__(self, parent: QtW.QWidget | None = None) -> None:
        super().__init__(parent)
        left = QtW.QLabel("Left")
        left.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right = QtW.QLabel("Right")
        right.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.addWidget(left)
        self.addWidget(right)


class _Slider(QtW.QSlider):
    def __init__(self, parent: QtW.QWidget | None = None) -> None:
        super().__init__(parent)
        self.setOrientation(Qt.Orientation.Horizontal)
        self.setValue(50)


def _add_widgets(layout: QtW.QVBoxLayout) -> None:
    layout.addWidget(QtW.QPushButton("QPushButton"))
    layout.addWidget(_Slider(None))
    layout.addWidget(_Splitter(None))


class _Group(QtW.QGroupBox):
    def __init__(self, parent: QtW.QWidget | None = None) -> None:
        super().__init__(parent)
        self.setTitle("QGroupBox")
        layout = QtW.QVBoxLayout(self)
        _add_widgets(layout)


class Tester(QtW.QMainWindow):
    """Basic tester window to test the Qlementine style."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Tester")

        layout = QtW.QVBoxLayout()
        _add_widgets(layout)
        layout.addWidget(_Group())

        tabs = QtW.QTabWidget()
        tab1 = QtW.QWidget()
        tab1_layout = QtW.QVBoxLayout(tab1)
        _add_widgets(tab1_layout)
        tabs.addTab(tab1, "Tab 1")
        # tab with a group box to test the style of the group box in a tab
        tab2 = QtW.QWidget()
        tab2_layout = QtW.QVBoxLayout(tab2)
        tab2_layout.addWidget(_Group())
        tabs.addTab(tab2, "Tab 2")
        layout.addWidget(tabs)

        central_widget = QtW.QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(layout)


if __name__ == "__main__":
    app = QtW.QApplication(sys.argv)
    if "--native" not in sys.argv:
        style = QlementineStyle(app)
        app.setStyle(style)

    tester = Tester()
    tester.resize(600, 400)
    tester.show()

    if "--native" not in sys.argv:
        editor = ThemeEditor(style.theme())
        editor.themeChanged.connect(style.setTheme)
        editor.setWindowTitle("Theme Editor")
        editor.resize(400, 600)
        editor.show()

    sys.exit(app.exec())
