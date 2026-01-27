from PyQt6.QtWidgets import QScrollArea, QWidget
from PyQt6.QtCore import Qt, QEvent, QObject
from PyQt6.QtGui import (
    QWheelEvent,
    QPaintEvent,
    QPainter,
    QLinearGradient,
    QColor,
    QResizeEvent,
)
from typing import Optional

from view.style.ui_style import WidgetRole
from view.style import rileva_tema_os


class HorizontalWheelScrollArea(QScrollArea):
    """Scroll area speciale per la visualizzazione di label con testo potenzialmente lungo.

    Permette all'utente di scorrere il suo contenuto con la rotellina."""

    def __init__(self):
        super().__init__()

        self.setWidgetResizable(True)
        self.setProperty(WidgetRole.INVISIBLE_H_SCROLL, True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setAutoFillBackground(False)
        viewport = self.viewport()
        assert viewport is not None
        viewport.setAutoFillBackground(False)
        viewport.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Funzione di fade
        fade = ScrollFadeOverlay(self)
        viewport.installEventFilter(fade)
        fade.resize(viewport.size())

    def wheelEvent(self, a0: Optional[QWheelEvent]) -> None:
        if a0 is None:
            return

        delta = a0.angleDelta().y()

        if delta:
            if bar := self.horizontalScrollBar():
                bar.setValue(bar.value() - delta)
                a0.accept()
        else:
            super().wheelEvent(a0)


class ScrollFadeOverlay(QWidget):

    __colored = (
        QColor(192, 192, 192, 125)
        if rileva_tema_os() == "dark.qss"
        else QColor(128, 128, 128, 125)
    )

    def __init__(self, scroll_area: HorizontalWheelScrollArea, fade_width: int = 40):
        super().__init__(scroll_area.viewport())

        self.__scroll_area = scroll_area
        self.__fade_width = fade_width

        self.__h_scroll_bar = self.__scroll_area.horizontalScrollBar()
        assert self.__h_scroll_bar is not None
        self.__h_scroll_bar.valueChanged.connect(  # type:ignore
            self.update
        )

        self.setAttribute(Qt.WidgetAttribute.WA_AlwaysStackOnTop)
        self.raise_()

    def eventFilter(self, a0: Optional[QObject], a1: Optional[QEvent]):
        if a0 is self.__scroll_area.viewport() and isinstance(a1, QResizeEvent):
            self.resize(a1.size())
        return super().eventFilter(a0, a1)

    def paintEvent(self, a0: Optional[QPaintEvent]):
        painter = QPainter(self)

        assert self.__h_scroll_bar is not None
        value = self.__h_scroll_bar.value()
        maximum = self.__h_scroll_bar.maximum()

        h = self.height()
        w = self.width()

        colored = self.__colored
        empty = QColor(0, 0, 0, 0)

        # Fade sinistra
        if value > 0:
            grad = QLinearGradient(0, 0, self.__fade_width, 0)
            grad.setColorAt(0.0, colored)
            grad.setColorAt(1.0, empty)
            painter.fillRect(0, 0, self.__fade_width, h, grad)

        # Fade destra
        if value < maximum:
            grad = QLinearGradient(w - self.__fade_width, 0, w, 0)
            grad.setColorAt(0.0, empty)
            grad.setColorAt(1.0, colored)
            painter.fillRect(w - self.__fade_width, 0, self.__fade_width, h, grad)
