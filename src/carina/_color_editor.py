"""Color swatch + hex line edit with inline color picker popup."""

from __future__ import annotations

from carina._color_picker import ColorPicker
from carina._qt.Qlementine import Popover
from carina._qt.QtCore import QMargins, Qt, Signal
from carina._qt.QtGui import QColor, QMouseEvent, QPainter
from carina._qt.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QSizePolicy,
    QWidget,
)

_SWATCH_SIZE = 24


class _ColorSwatch(QWidget):
    """Small button that displays a solid color."""

    clicked = Signal()

    def __init__(self, color: QColor, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._color = QColor(color)
        self.setFixedSize(_SWATCH_SIZE, _SWATCH_SIZE)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

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

    def mouseReleaseEvent(self, event: QMouseEvent | None) -> None:
        if event and event.button() == Qt.MouseButton.LeftButton:
            if self.rect().contains(event.pos()):
                self.clicked.emit()


def _color_to_hex(color: QColor) -> str:
    if color.alpha() < 255:
        return color.name(QColor.NameFormat.HexArgb)
    return color.name(QColor.NameFormat.HexRgb)


class ColorEditor(QWidget):
    """Color swatch + hex line edit with inline color picker."""

    colorChanged = Signal()

    def __init__(
        self, color: QColor | None = None, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        if color is None:
            color = QColor("black")
        self._color = QColor(color)
        self._updating = False
        self._popover: Popover | None = None

        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)

        self._swatch = _ColorSwatch(color, self)
        self._swatch.clicked.connect(self._toggle_picker)
        lay.addWidget(self._swatch)

        self._line_edit = QLineEdit(self)
        self._line_edit.setText(_color_to_hex(color))
        self._line_edit.editingFinished.connect(self._on_text_edited)
        lay.addWidget(self._line_edit)

        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

    def color(self) -> QColor:
        return QColor(self._color)

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
            self._line_edit.setText(_color_to_hex(candidate))
            self.colorChanged.emit()

    def _toggle_picker(self) -> None:
        if self._popover and self._popover.isOpened():
            self._popover.closePopover()
            return

        picker = ColorPicker(self._color)
        picker.colorChanged.connect(self._on_picker_color)

        self._popover = Popover(self)
        self._popover.setAnchorWidget(self._swatch)
        self._popover.setVerticalSpacing(6)
        self._popover.setContentWidget(picker)
        self._popover.setPadding(QMargins(0, 0, 0, 0))
        self._popover.setPreferredPosition(Popover.Position.Top)
        self._popover.setPreferredAlignment(Popover.Alignment.Center)
        self._popover.openPopover()

    def _on_picker_color(self, color: QColor) -> None:
        self.setColor(color)
