from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from carina._qt.QtWidgets import QApplication

if TYPE_CHECKING:
    from carina._qt.QtCore import QCoreApplication


@pytest.fixture(scope="session")
def qapp() -> QCoreApplication:
    """Provide a shared QApplication instance for the test session."""
    app = QApplication.instance() or QApplication([])
    return app
