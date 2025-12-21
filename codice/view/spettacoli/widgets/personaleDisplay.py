from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout
from PyQt6.QtCore import pyqtSignal
from functools import partial


class PersonaleDisplay(QWidget):
    """View degli interpreti e tecnici degli spettacoli.

    Segnali:
    - eliminaRequest(str): emesso quando si clicca il pulsante Elimina.
    """

    eliminaRequest = pyqtSignal(str)

    def __init__(self, key: str, value: str) -> None:
        super().__init__()

        self._setup_ui(key, value)
        self._connect_signals()

    def _setup_ui(self, key: str, value: str) -> None:
        self.key = key

        widget_key = QLabel(self.key)
        widget_key.setObjectName("paragraph")

        widget_value = QLabel(value)
        widget_value.setObjectName("paragraph")

        self.__btn_rimuovi = QPushButton("X")
        self.__btn_rimuovi.setFixedSize(25, 25)
        self.__btn_rimuovi.setObjectName("removeButton")

        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(widget_key, 0, 0)
        layout.addWidget(widget_value, 0, 1)
        layout.addWidget(self.__btn_rimuovi, 0, 2)

    def _connect_signals(self) -> None:
        self.__btn_rimuovi.clicked.connect(  # type:ignore
            partial(self.eliminaRequest.emit, self.key)
        )
