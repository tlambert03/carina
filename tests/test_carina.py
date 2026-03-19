import carina
from carina._qt.QtWidgets import QApplication, QTabWidget
from carina.demo import DemoWindow


def test_imports_with_version() -> None:
    assert isinstance(carina.__version__, str)


def test_demo_widget(qapp: QApplication) -> None:
    window = DemoWindow()
    window.show()
    qapp.processEvents()

    tabs = window.findChild(QTabWidget)
    assert tabs is not None
    for i in range(tabs.count() + 1):
        tabs.setCurrentIndex(i)
        qapp.processEvents()

    window.close()
