"""QtAds-aware style extending QlementineStyle.

QtAds applies a global stylesheet to CDockManager, which creates a QStyleSheetStyle
proxy that intercepts painting for all descendant widgets — breaking custom QStyle
implementations like QlementineStyle. This module subclasses QlementineStyle directly
and renders QtAds dock tabs and title bars through the QStyle system, using
Qlementine's theme tokens for full theme awareness.

Usage::

    app.setStyle(AdsAwareQlementineStyle())
    dock_manager.setStyleSheet("")  # remove QtAds default CSS
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyconify import svg_path

from carina._qt.Qlementine import (
    AutoIconColor,
    MouseState,
    QlementineStyle,
    SelectionState,
)
from carina._qt.Qlementine import utils as qlem_utils
from carina._qt.QtGui import QColor, QPalette, QPen
from carina._qt.QtWidgets import QScrollArea, QStyle, QStyleOptionToolButton, QWidget

if TYPE_CHECKING:
    from carina._qt.QtGui import QPainter
    from carina._qt.QtWidgets import QStyleOption, QStyleOptionComplex

# QtAds widget objectNames
ADS_TAB_CLOSE = "tabCloseButton"
ADS_TAB_LABEL = "dockWidgetTabLabel"
ADS_TABS_MENU = "tabsMenuButton"
ADS_TABS_CONTAINER = "tabsContainerWidget"
ADS_TITLE_BAR = "dockAreaTitleBar"
ADS_AREA_CLOSE = "dockAreaCloseButton"
ADS_AUTO_HIDE = "dockAreaAutoHideButton"
ADS_DETACH = "detachGroupButton"

# QtAds dynamic property names
ADS_ACTIVE_TAB = "activeTab"

# Icon keys for QtAds buttons, resolved via pyconify at runtime.
_ADS_ICON_MAP = {
    ADS_TAB_CLOSE: "codicon:close",
    ADS_TABS_MENU: "codicon:chevron-down",
    ADS_DETACH: "tabler:queue-pop-out",
    ADS_AREA_CLOSE: "codicon:close",
    ADS_AUTO_HIDE: "codicon:pinned",
}


class AdsAwareQlementineStyle(QlementineStyle):
    """QlementineStyle subclass with QtAds dock widget awareness."""

    def __init__(self) -> None:
        super().__init__()
        self.setAutoIconColor(AutoIconColor.ForegroundColor)

    # ---- Drawing overrides ----

    def drawControl(
        self,
        element: QStyle.ControlElement,
        option: QStyleOption,
        painter: QPainter,
        widget: QWidget | None = None,
    ) -> None:
        if element == QStyle.ControlElement.CE_ShapedFrame and widget:
            if (active := widget.property(ADS_ACTIVE_TAB)) is not None:
                self._draw_dock_tab(option, painter, widget, bool(active))
                return
            if widget.objectName() == ADS_TITLE_BAR:
                self._draw_title_bar(option, painter, widget)
                return
        super().drawControl(element, option, painter, widget)

    def drawComplexControl(
        self,
        control: QStyle.ComplexControl,
        option: QStyleOptionComplex,
        painter: QPainter,
        widget: QWidget | None = None,
    ) -> None:
        # Suppress the double-chevron menu indicator on the tabs menu
        if (
            widget
            and widget.objectName() == ADS_TABS_MENU
            and control == QStyle.ComplexControl.CC_ToolButton
            and isinstance(option, QStyleOptionToolButton)
        ):
            option.features &= ~QStyleOptionToolButton.ToolButtonFeature.HasMenu
        super().drawComplexControl(control, option, painter, widget)

    # ---- Widget polishing ----

    def polish(self, obj: Any) -> None:
        result = super().polish(obj)
        if not isinstance(obj, QWidget):
            return result

        name = obj.objectName()

        # Set themed icons on QtAds buttons.
        # AutoIconColor (set in __init__) ensures Qlementine
        # re-colorizes them at paint time with the correct fg color.
        if name in _ADS_ICON_MAP and hasattr(obj, "setIcon"):
            obj.setIcon(self.makeThemedIcon(str(svg_path(_ADS_ICON_MAP[name]))))

        # Flat close buttons so Qlementine skips the button bevel
        if name == ADS_TAB_CLOSE and hasattr(obj, "setFlat"):
            obj.setFlat(True)

        # Set title bar background on intermediate widgets that would
        # otherwise auto-fill with palette(Window), covering the
        # darker title bar painted by _draw_title_bar.
        tb_bg = self.tabBarBackgroundColor(MouseState.Normal)
        if obj.property(ADS_ACTIVE_TAB) is not None or name == ADS_TABS_CONTAINER:
            _set_widget_bg(obj, tb_bg)
        elif name == ADS_TITLE_BAR:
            for child in obj.findChildren(QScrollArea):
                _set_widget_bg(child, tb_bg)
                _set_widget_bg(child.viewport(), tb_bg)

        return result

    # ---- Private drawing helpers ----

    def _draw_dock_tab(
        self,
        option: QStyleOption,
        painter: QPainter,
        widget: QWidget | None,
        is_active: bool,
    ) -> None:
        if widget is None:
            return
        mouse = qlem_utils.getMouseState(option.state)
        sel = SelectionState.Selected if is_active else SelectionState.NotSelected
        bg = self.tabBackgroundColor(mouse, sel)

        painter.save()

        if is_active:
            painter.fillRect(option.rect, bg)
        else:
            if bg.alpha() > 0:
                qlem_utils.drawRoundedRect(painter, option.rect, bg, 6.0)
            # Separator between inactive tabs
            pal = widget.palette()
            sep = qlem_utils.colorWithAlphaF(
                pal.color(QPalette.ColorRole.WindowText), 0.2
            )
            painter.setPen(QPen(sep, 1))
            x = int(option.rect.right())
            painter.drawLine(
                x,
                option.rect.top() + 5,
                x,
                option.rect.bottom() - 5,
            )

        painter.restore()
        if widget is not None:
            self._update_tab_label_color(widget, mouse, sel)

    def _update_tab_label_color(
        self, tab: QWidget, mouse: MouseState, sel: SelectionState
    ) -> None:
        target = self.tabForegroundColor(mouse, sel)
        for child in tab.children():
            if (
                isinstance(child, QWidget)
                and child.objectName() == ADS_TAB_LABEL
                and child.palette().color(QPalette.ColorRole.WindowText) != target
            ):
                pal = child.palette()
                pal.setColor(QPalette.ColorRole.WindowText, target)
                child.setPalette(pal)

    def _draw_title_bar(
        self, option: QStyleOption, painter: QPainter, widget: QWidget | None
    ) -> None:
        painter.save()
        painter.fillRect(option.rect, self.tabBarBackgroundColor(MouseState.Normal))
        painter.setPen(QPen(self.tabBarBottomShadowColor(), 1))
        painter.drawLine(
            option.rect.left(),
            option.rect.bottom(),
            option.rect.right(),
            option.rect.bottom(),
        )
        painter.restore()


def _set_widget_bg(widget: QWidget, color: QColor) -> None:
    pal = widget.palette()
    pal.setColor(QPalette.ColorRole.Window, color)
    widget.setPalette(pal)
    widget.setAutoFillBackground(True)
