from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout
from PyQt6.QtCore import pyqtSignal
from functools import partial

from view.style import QssStyle


class PersonaleDisplay(QWidget):
    """View degli interpreti e tecnici degli spettacoli.

    Segnali:
    - eliminaRequest(str): emesso quando si clicca il pulsante di elimina [X].
    """

    eliminaRequest = pyqtSignal(str)

    def __init__(self, key: str, value: str) -> None:
        super().__init__()

        self.__setup_ui(key, value)
        self.__connect_signals()

    def __setup_ui(self, key: str, value: str) -> None:
        self.__key = key

        widget_key = QLabel(self.__key)
        widget_key.setObjectName(QssStyle.PARAGRAPH.style_name)

        widget_value = QLabel(value)
        widget_value.setObjectName(QssStyle.PARAGRAPH.style_name)

        self.__btn_rimuovi = QPushButton("X")
        self.__btn_rimuovi.setFixedSize(25, 25)
        self.__btn_rimuovi.setObjectName(QssStyle.REMOVE_BUTTON.style_name)

        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(widget_key, 0, 0)
        layout.addWidget(widget_value, 0, 1)
        layout.addWidget(self.__btn_rimuovi, 0, 2)

    def __connect_signals(self) -> None:
        self.__btn_rimuovi.clicked.connect(  # type:ignore
            partial(self.eliminaRequest.emit, self.__key)
        )
