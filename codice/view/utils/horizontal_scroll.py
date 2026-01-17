from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QWheelEvent
from typing import Optional

from view.style import WidgetRole


class HorizontalWheelScrollArea(QScrollArea):
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
