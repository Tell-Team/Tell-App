from PyQt6.QtWidgets import (
    QWidget,
    QLineEdit,
    QComboBox,
    QSpinBox,
    QTextEdit,
    QDateEdit,
    QTimeEdit,
)
from typing import Optional


def apply_fixed_size(widget: QWidget, w: Optional[int], h: Optional[int]):
    if w is None and h is None:
        raise ValueError("È necessario inserire almeno un valore tra width e height.")
    if w is not None:
        widget.setFixedWidth(w)
    if h is not None:
        widget.setFixedHeight(h)


class FixedSizeLineEdit(QLineEdit):
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ):
        super().__init__(parent)
        apply_fixed_size(self, width, height)


class FixedSizeComboBox(QComboBox):
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ):
        super().__init__(parent)
        apply_fixed_size(self, width, height)


class FixedSizeSpinBox(QSpinBox):
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ):
        super().__init__(parent)
        apply_fixed_size(self, width, height)


class FixedSizeTextEdit(QTextEdit):
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ):
        super().__init__(parent)
        apply_fixed_size(self, width, height)


class FixedSizeDateEdit(QDateEdit):
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ):
        super().__init__(parent)
        apply_fixed_size(self, width, height)


class FixedSizeTimeEdit(QTimeEdit):
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ):
        super().__init__(parent)
        apply_fixed_size(self, width, height)
