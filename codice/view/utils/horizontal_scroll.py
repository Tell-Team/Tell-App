from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QWheelEvent
from typing import Optional

from view.style import QssStyle


class HorizontalWheelScrollArea(QScrollArea):
    def __init__(self):
        super().__init__()

        self.setWidgetResizable(True)
        self.setProperty(QssStyle.INVISIBLE_H_SCROLL, True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

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
