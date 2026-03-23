"""Color picker widget with SV area, hue slider, loupe, and mode inputs."""

from __future__ import annotations

from carina._qt.QtCore import (
    QPointF,
    QRectF,
    QRegularExpression,
    Qt,
    Signal,
)
from carina._qt.QtGui import (
    QBrush,
    QColor,
    QCursor,
    QFont,
    QImage,
    QKeyEvent,
    QLinearGradient,
    QMouseEvent,
    QPainter,
    QPainterPath,
    QPaintEvent,
    QPen,
    QPixmap,
    QRegularExpressionValidator,
    QResizeEvent,
)
from carina._qt.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLineEdit,
    QSpinBox,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_PICKER_WIDTH = 280
_SV_AREA_HEIGHT = 200
_HANDLE_RADIUS = 7
_HANDLE_BORDER = 2
_HUE_SLIDER_HEIGHT = 20
_HUE_HANDLE_RADIUS = 10
_SWATCH_SIZE = 32
_EYEDROPPER_SIZE = 28
_LOUPE_PIXEL_COUNT = 11  # odd, pixels sampled in each direction
_LOUPE_RADIUS = 70
_LOUPE_PIXEL_SIZE = -(-_LOUPE_RADIUS * 2 // _LOUPE_PIXEL_COUNT)  # ceil div
_CORNER_RADIUS = 8
_PAD = 12


# ---------------------------------------------------------------------------
# _SaturationValueArea
# ---------------------------------------------------------------------------


class _SaturationValueArea(QWidget):
    """Two-axis gradient: horizontal saturation, vertical value."""

    colorChanged = Signal(object)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._hue: float = 0.0
        self._sat: float = 1.0
        self._val: float = 1.0
        self._cache: QPixmap | None = None
        self.setFixedHeight(_SV_AREA_HEIGHT)

    # -- public --

    def setHue(self, hue: float) -> None:
        if self._hue != hue:
            self._hue = hue
            self._cache = None
            self.update()

    def setColor(self, color: QColor) -> None:
        h = color.hsvHueF() * 360
        if h < 0:
            h = self._hue
        self._hue = h
        self._sat = color.hsvSaturationF()
        self._val = color.valueF()
        self._cache = None
        self.update()

    # -- painting --

    def _rebuild_cache(self) -> None:
        w, h = self.width(), self.height()
        if w < 2 or h < 2:
            return
        pm = QPixmap(w, h)
        p = QPainter(pm)
        # Fill with pure hue
        p.fillRect(0, 0, w, h, QColor.fromHsvF(self._hue / 360.0, 1.0, 1.0))
        # White-to-transparent left-to-right (saturation)
        sat_grad = QLinearGradient(0, 0, w, 0)
        sat_grad.setColorAt(0, QColor(255, 255, 255))
        sat_grad.setColorAt(1, QColor(255, 255, 255, 0))
        p.fillRect(0, 0, w, h, QBrush(sat_grad))
        # Transparent-to-black top-to-bottom (value)
        val_grad = QLinearGradient(0, 0, 0, h)
        val_grad.setColorAt(0, QColor(0, 0, 0, 0))
        val_grad.setColorAt(1, QColor(0, 0, 0))
        p.fillRect(0, 0, w, h, QBrush(val_grad))
        p.end()
        self._cache = pm

    def paintEvent(self, event: QPaintEvent) -> None:
        if self._cache is None or self._cache.size() != self.size():
            self._rebuild_cache()

        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Clip to rounded top corners
        path = QPainterPath()
        r = QRectF(self.rect())
        path.moveTo(r.bottomLeft())
        path.lineTo(r.left(), r.top() + _CORNER_RADIUS)
        path.quadTo(r.topLeft(), QPointF(r.left() + _CORNER_RADIUS, r.top()))
        path.lineTo(r.right() - _CORNER_RADIUS, r.top())
        path.quadTo(r.topRight(), QPointF(r.right(), r.top() + _CORNER_RADIUS))
        path.lineTo(r.bottomRight())
        path.closeSubpath()
        p.setClipPath(path)

        if self._cache:
            p.drawPixmap(0, 0, self._cache)

        # Handle
        hx = self._sat * (self.width() - 1)
        hy = (1.0 - self._val) * (self.height() - 1)
        center = QPointF(hx, hy)

        p.setClipping(False)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(0, 0, 0, 60))
        p.drawEllipse(center, _HANDLE_RADIUS + 1, _HANDLE_RADIUS + 1)
        p.setPen(QPen(QColor(255, 255, 255), _HANDLE_BORDER))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawEllipse(center, _HANDLE_RADIUS, _HANDLE_RADIUS)
        p.end()

    def resizeEvent(self, event: QResizeEvent) -> None:
        self._cache = None
        super().resizeEvent(event)

    # -- mouse --

    def _update_from_pos(self, x: int, y: int) -> None:
        w, h = self.width(), self.height()
        if w < 2 or h < 2:
            return
        self._sat = max(0.0, min(1.0, x / (w - 1)))
        self._val = max(0.0, min(1.0, 1.0 - y / (h - 1)))
        self.update()
        self.colorChanged.emit(QColor.fromHsvF(self._hue / 360.0, self._sat, self._val))

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event and event.button() == Qt.MouseButton.LeftButton:
            self._update_from_pos(event.pos().x(), event.pos().y())

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event and event.buttons() & Qt.MouseButton.LeftButton:
            self._update_from_pos(event.pos().x(), event.pos().y())


# ---------------------------------------------------------------------------
# _HueSlider
# ---------------------------------------------------------------------------


class _HueSlider(QWidget):
    """Horizontal hue slider with rainbow groove and colored handle."""

    hueChanged = Signal(float)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._hue: float = 0.0
        self.setFixedHeight(_HUE_HANDLE_RADIUS * 2 + 8)
        self.setMinimumWidth(80)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def hue(self) -> float:
        return self._hue

    def setHue(self, hue: float) -> None:
        hue = max(0.0, min(360.0, hue))
        if self._hue != hue:
            self._hue = hue
            self.update()

    def paintEvent(self, event: QPaintEvent | None) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        margin = _HUE_HANDLE_RADIUS
        gy = (self.height() - _HUE_SLIDER_HEIGHT) / 2
        groove = QRectF(0, gy, self.width(), _HUE_SLIDER_HEIGHT)

        # Rainbow gradient
        grad = QLinearGradient(groove.left(), 0, groove.right(), 0)
        for i in range(7):
            grad.setColorAt(i / 6.0, QColor.fromHsvF(i * 60 / 360.0, 1.0, 1.0))

        path = QPainterPath()
        path.addRoundedRect(groove, groove.height() / 2, groove.height() / 2)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(grad))
        p.drawPath(path)

        # Handle
        usable = self.width() - 2 * margin
        hx = margin + (self._hue / 360.0) * usable
        hy = self.height() / 2.0
        center = QPointF(hx, hy)

        p.setBrush(QColor(0, 0, 0, 50))
        p.drawEllipse(center, _HUE_HANDLE_RADIUS + 1, _HUE_HANDLE_RADIUS + 1)
        p.setPen(QPen(QColor(255, 255, 255), 2))
        p.setBrush(QColor.fromHsvF(self._hue / 360.0, 1.0, 1.0))
        p.drawEllipse(center, _HUE_HANDLE_RADIUS, _HUE_HANDLE_RADIUS)
        p.end()

    def _update_from_x(self, x: int) -> None:
        margin = _HUE_HANDLE_RADIUS
        usable = self.width() - 2 * margin
        self._hue = max(0.0, min(1.0, (x - margin) / usable)) * 359.0
        self.update()
        self.hueChanged.emit(self._hue)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event and event.button() == Qt.MouseButton.LeftButton:
            self._update_from_x(event.pos().x())

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event and event.buttons() & Qt.MouseButton.LeftButton:
            self._update_from_x(event.pos().x())


# ---------------------------------------------------------------------------
# _ColorSwatch
# ---------------------------------------------------------------------------


class _ColorSwatch(QWidget):
    """Readonly circle showing the current color."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._color = QColor(0, 0, 0)
        self.setFixedSize(_SWATCH_SIZE, _SWATCH_SIZE)

    def setColor(self, color: QColor) -> None:
        if self._color != color:
            self._color = QColor(color)
            self.update()

    def paintEvent(self, event: QPaintEvent | None) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRectF(self.rect()).adjusted(1, 1, -1, -1)
        p.setPen(QPen(QColor(255, 255, 255, 80), 1.5))
        p.setBrush(self._color)
        p.drawEllipse(rect)
        p.end()


# ---------------------------------------------------------------------------
# _EyeDropperButton
# ---------------------------------------------------------------------------


class _EyeDropperButton(QWidget):
    """Button that triggers screen-wide color picking with a loupe."""

    colorPicked = Signal(object)
    clicked = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedSize(_EYEDROPPER_SIZE, _EYEDROPPER_SIZE)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(self._start_pick)

    def paintEvent(self, event: QPaintEvent | None) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(QPen(QColor(200, 200, 200), 1.5))
        p.setBrush(Qt.BrushStyle.NoBrush)

        cx, cy = self.width() / 2, self.height() / 2
        path = QPainterPath()
        path.addEllipse(QPointF(cx - 1, cy - 4), 5, 5)
        path.moveTo(cx - 4, cy + 1)
        path.lineTo(cx - 1, cy + 8)
        path.lineTo(cx + 2, cy + 1)
        p.drawPath(path)
        p.end()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event and event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()

    def _start_pick(self) -> None:
        self._overlay = _LoupeOverlay(self)
        self._overlay.colorPicked.connect(self._on_picked)
        self._overlay.show()
        self._overlay.raise_()
        self._overlay.activateWindow()

    def _on_picked(self, color: QColor) -> None:
        self.colorPicked.emit(color)
        self._overlay = None


# ---------------------------------------------------------------------------
# _LoupeOverlay
# ---------------------------------------------------------------------------


class _LoupeOverlay(QWidget):
    """Fullscreen overlay with magnifying loupe for pixel-precise picking."""

    colorPicked = Signal(object)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(None)
        self._parent_ref = parent
        self.setWindowFlags(Qt.WindowType.Popup)
        self.setCursor(Qt.CursorShape.CrossCursor)
        self.setMouseTracking(True)

        self._grab: QPixmap | None = None
        self._grab_image: QImage | None = None
        self._cursor_pos = QCursor.pos()
        self._grab_screen()

    def _grab_screen(self) -> None:
        screen = QApplication.screenAt(self._cursor_pos)
        if screen is None:
            screen = QApplication.primaryScreen()
        if screen:
            self._grab = screen.grabWindow(0)
            self._grab_image = self._grab.toImage()
            self.setGeometry(screen.geometry())

    def paintEvent(self, event: QPaintEvent | None) -> None:
        if not self._grab or not self._grab_image:
            return

        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Screenshot background + dim
        p.drawPixmap(0, 0, self._grab)
        p.fillRect(self.rect(), QColor(0, 0, 0, 30))

        # Loupe
        cursor = self.mapFromGlobal(self._cursor_pos)
        cx, cy = cursor.x(), cursor.y()
        half = _LOUPE_PIXEL_COUNT // 2
        center = QPointF(cx, cy)
        img = self._grab_image
        dpr = self._grab.devicePixelRatio()

        # Clip to circle
        clip = QPainterPath()
        clip.addEllipse(center, _LOUPE_RADIUS, _LOUPE_RADIUS)
        p.setClipPath(clip)

        # Magnified pixels
        for dy in range(-half, half + 1):
            for dx in range(-half, half + 1):
                sx = int((cx + dx) * dpr)
                sy = int((cy + dy) * dpr)
                if 0 <= sx < img.width() and 0 <= sy < img.height():
                    pc = img.pixelColor(sx, sy)
                else:
                    pc = QColor(0, 0, 0)
                p.fillRect(
                    QRectF(
                        cx + dx * _LOUPE_PIXEL_SIZE - _LOUPE_PIXEL_SIZE / 2,
                        cy + dy * _LOUPE_PIXEL_SIZE - _LOUPE_PIXEL_SIZE / 2,
                        _LOUPE_PIXEL_SIZE,
                        _LOUPE_PIXEL_SIZE,
                    ),
                    pc,
                )

        # Grid
        p.setPen(QPen(QColor(255, 255, 255, 40), 0.5))
        for i in range(-half, half + 2):
            gy = cy + i * _LOUPE_PIXEL_SIZE - _LOUPE_PIXEL_SIZE / 2
            p.drawLine(
                QPointF(cx - _LOUPE_RADIUS, gy),
                QPointF(cx + _LOUPE_RADIUS, gy),
            )
            gx = cx + i * _LOUPE_PIXEL_SIZE - _LOUPE_PIXEL_SIZE / 2
            p.drawLine(
                QPointF(gx, cy - _LOUPE_RADIUS),
                QPointF(gx, cy + _LOUPE_RADIUS),
            )

        p.setClipping(False)

        # Loupe border
        p.setPen(QPen(QColor(0, 0, 0, 120), 3))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawEllipse(center, _LOUPE_RADIUS + 1, _LOUPE_RADIUS + 1)
        p.setPen(QPen(QColor(255, 255, 255), 2))
        p.drawEllipse(center, _LOUPE_RADIUS, _LOUPE_RADIUS)

        # Center pixel highlight
        p.setPen(QPen(QColor(255, 255, 255), 1.5))
        p.drawRect(
            QRectF(
                cx - _LOUPE_PIXEL_SIZE / 2,
                cy - _LOUPE_PIXEL_SIZE / 2,
                _LOUPE_PIXEL_SIZE,
                _LOUPE_PIXEL_SIZE,
            )
        )

        # Hex label below loupe
        sx = int(cx * dpr)
        sy = int(cy * dpr)
        if 0 <= sx < img.width() and 0 <= sy < img.height():
            center_color = img.pixelColor(sx, sy)
        else:
            center_color = QColor(0, 0, 0)
        hex_text = center_color.name().upper().lstrip("#")
        font = QFont()
        font.setStyleHint(QFont.StyleHint.Monospace)
        font.setPointSize(12)
        p.setFont(font)
        label_rect = QRectF(cx - 46, cy + _LOUPE_RADIUS + 10, 92, 26)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(30, 30, 30, 200))
        p.drawRoundedRect(label_rect, 6, 6)
        p.setPen(QPen(QColor(255, 255, 255, 220)))
        p.drawText(label_rect, Qt.AlignmentFlag.AlignCenter, hex_text)
        p.end()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        self._cursor_pos = QCursor.pos()
        self.update()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if not (event and event.button() == Qt.MouseButton.LeftButton):
            return
        if not self._grab_image or not self._grab:
            return
        pos = self.mapFromGlobal(self._cursor_pos)
        dpr = self._grab.devicePixelRatio()
        px = int(pos.x() * dpr)
        py = int(pos.y() * dpr)
        img = self._grab_image
        if 0 <= px < img.width() and 0 <= py < img.height():
            self.colorPicked.emit(img.pixelColor(px, py))
        self.close()
        self.deleteLater()

    def keyPressEvent(self, event: QKeyEvent | None) -> None:
        if event and event.key() == Qt.Key.Key_Escape:
            self.close()
            self.deleteLater()
        elif event:
            super().keyPressEvent(event)


# ---------------------------------------------------------------------------
# _ColorInputs
# ---------------------------------------------------------------------------


class _ColorInputs(QWidget):
    """Mode-switchable color value inputs."""

    colorEdited = Signal(object)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._updating = False
        self._hue: float = 0.0  # preserve hue for achromatic colors

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self._stack = QStackedWidget()
        layout.addWidget(self._stack)

        # RGB page
        rgb_page = QWidget()
        rgb_lay = QHBoxLayout(rgb_page)
        rgb_lay.setContentsMargins(0, 0, 0, 0)
        rgb_lay.setSpacing(6)
        self._r_spin = self._make_spin(0, 255)
        self._g_spin = self._make_spin(0, 255)
        self._b_spin = self._make_spin(0, 255)
        rgb_lay.addWidget(self._r_spin)
        rgb_lay.addWidget(self._g_spin)
        rgb_lay.addWidget(self._b_spin)
        self._stack.addWidget(rgb_page)

        # HSL page
        hsl_page = QWidget()
        hsl_lay = QHBoxLayout(hsl_page)
        hsl_lay.setContentsMargins(0, 0, 0, 0)
        hsl_lay.setSpacing(6)
        self._h_spin = self._make_spin(0, 360)
        self._s_spin = self._make_spin(0, 100, suffix="%")
        self._l_spin = self._make_spin(0, 100, suffix="%")
        hsl_lay.addWidget(self._h_spin)
        hsl_lay.addWidget(self._s_spin)
        hsl_lay.addWidget(self._l_spin)
        self._stack.addWidget(hsl_page)

        # HEX page
        hex_page = QWidget()
        hex_lay = QHBoxLayout(hex_page)
        hex_lay.setContentsMargins(0, 0, 0, 0)
        hex_lay.setSpacing(6)
        self._hex_edit = QLineEdit()
        self._hex_edit.setValidator(
            QRegularExpressionValidator(QRegularExpression(r"#[0-9A-Fa-f]{0,6}"))
        )
        self._hex_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._hex_edit.editingFinished.connect(self._on_hex_edited)
        hex_lay.addWidget(self._hex_edit)
        self._stack.addWidget(hex_page)

        # Mode combo
        self._combo = QComboBox()
        self._combo.addItems(["R   G   B", "H   S   L", "HEX"])
        self._combo.currentIndexChanged.connect(self._stack.setCurrentIndex)
        layout.addWidget(self._combo)

    def _make_spin(self, lo: int, hi: int, suffix: str = "") -> QSpinBox:
        spin = QSpinBox()
        spin.setRange(lo, hi)
        spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if suffix:
            spin.setSuffix(suffix)
        spin.valueChanged.connect(self._on_spin_changed)
        return spin

    def setMode(self, index: int) -> None:
        self._combo.setCurrentIndex(index)

    def setColor(self, color: QColor, hue: float = -1.0) -> None:
        self._updating = True
        self._r_spin.setValue(color.red())
        self._g_spin.setValue(color.green())
        self._b_spin.setValue(color.blue())

        h = color.hslHueF()
        if h >= 0:
            self._hue = h * 360
        elif hue >= 0:
            self._hue = hue
        self._h_spin.setValue(round(self._hue))
        self._s_spin.setValue(round(color.hslSaturationF() * 100))
        self._l_spin.setValue(round(color.lightnessF() * 100))

        self._hex_edit.setText(color.name(QColor.NameFormat.HexRgb).upper())
        self._updating = False

    def _on_spin_changed(self) -> None:
        if self._updating:
            return
        page = self._stack.currentIndex()
        if page == 0:
            color = QColor(
                self._r_spin.value(), self._g_spin.value(), self._b_spin.value()
            )
        elif page == 1:
            color = QColor.fromHslF(
                self._h_spin.value() / 360.0,
                self._s_spin.value() / 100.0,
                self._l_spin.value() / 100.0,
            )
        else:
            return
        self.colorEdited.emit(color)

    def _on_hex_edited(self) -> None:
        if self._updating:
            return
        color = QColor(self._hex_edit.text().strip())
        if color.isValid():
            self.colorEdited.emit(color)


# ---------------------------------------------------------------------------
# ColorPicker
# ---------------------------------------------------------------------------


class ColorPicker(QWidget):
    """Color picker with SV area, hue slider, and mode inputs."""

    colorChanged = Signal(object)

    def __init__(
        self, color: QColor | None = None, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self._updating = False
        self._color = QColor(color) if color else QColor(0, 120, 215)

        self.setFixedWidth(_PICKER_WIDTH)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Row 1: SV area
        self._sv_area = _SaturationValueArea()
        self._sv_area.colorChanged.connect(self._on_sv_changed)
        layout.addWidget(self._sv_area)

        # Padded bottom section
        bottom = QWidget()
        bottom_lay = QVBoxLayout(bottom)
        bottom_lay.setContentsMargins(_PAD, _PAD, _PAD, _PAD)
        bottom_lay.setSpacing(10)

        # Row 2: eyedropper + swatch + hue slider
        row2 = QHBoxLayout()
        row2.setSpacing(10)
        self._eyedropper = _EyeDropperButton()
        self._eyedropper.colorPicked.connect(self._on_picked)
        row2.addWidget(self._eyedropper)
        self._swatch = _ColorSwatch()
        row2.addWidget(self._swatch)
        self._hue_slider = _HueSlider()
        self._hue_slider.hueChanged.connect(self._on_hue_changed)
        row2.addWidget(self._hue_slider, 1)
        bottom_lay.addLayout(row2)

        # Rows 3-4: inputs + mode combo
        self._inputs = _ColorInputs()
        self._inputs.colorEdited.connect(self._on_input_edited)
        bottom_lay.addWidget(self._inputs)

        layout.addWidget(bottom)
        self._apply(self._color)

    # -- public API --

    def color(self) -> QColor:
        return QColor(self._color)

    def setColor(self, color: QColor) -> None:
        if self._color != color:
            self._apply(color)

    # -- internal --

    def _apply(
        self, color: QColor, *, update_sv: bool = True, update_hue: bool = True
    ) -> None:
        """Push color to all widgets and emit. Skips if already updating."""
        if self._updating:
            return
        self._updating = True
        if update_sv:
            self._sv_area.setColor(color)
        if update_hue:
            h = color.hsvHueF()
            if h >= 0:
                self._hue_slider.setHue(h * 360)
        self._swatch.setColor(color)
        self._inputs.setColor(color, self._hue_slider.hue())
        self._updating = False
        self._color = QColor(color)
        self.colorChanged.emit(QColor(color))

    def _on_sv_changed(self, color: QColor) -> None:
        self._apply(color, update_sv=False, update_hue=False)

    def _on_hue_changed(self, hue: float) -> None:
        if self._updating:
            return
        self._sv_area.setHue(hue)
        color = QColor.fromHsvF(hue / 360.0, self._sv_area._sat, self._sv_area._val)
        self._apply(color, update_sv=False)

    def _on_input_edited(self, color: QColor) -> None:
        self._apply(color)

    def _on_picked(self, color: QColor) -> None:
        self._apply(color)


# ---------------------------------------------------------------------------
# Quick test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    app = QApplication.instance() or QApplication(sys.argv)
    picker = ColorPicker(QColor(7, 176, 233))
    picker.colorChanged.connect(lambda c: print(f"Color: {c.name()}"))
    picker.setWindowTitle("Color Picker")
    picker.show()
    app.exec()
