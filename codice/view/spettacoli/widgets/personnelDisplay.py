from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import pyqtSignal
from functools import partial


class PersonnelDisplay(QWidget):
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
        widget_key.setObjectName("Paragraph")

        widget_value = QLabel(value)
        widget_value.setObjectName("Paragraph")

        self.__btn_elimina = QPushButton("Elimina")
        self.__btn_elimina.setObjectName("WhiteButton")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(widget_key)
        layout.addWidget(widget_value)
        layout.addWidget(self.__btn_elimina)

    def _connect_signals(self) -> None:
        self.__btn_elimina.clicked.connect(  # type:ignore
            partial(self.eliminaRequest.emit, self.key)
        )
