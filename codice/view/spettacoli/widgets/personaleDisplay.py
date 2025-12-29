from PyQt6.QtWidgets import QLabel, QPushButton, QGridLayout
from PyQt6.QtCore import Qt, pyqtSignal
from functools import partial

from view.utils.list_widgets import ItemDisplay
from view.utils import make_vline
from view.style import QssStyle


class PersonaleDisplay(ItemDisplay):
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
        widget_key.setProperty(QssStyle.PARAGRAPH.style_role, True)

        widget_value = QLabel(value)
        widget_value.setProperty(QssStyle.PARAGRAPH.style_role, True)

        self.__btn_rimuovi = QPushButton("X")
        # - Quitar el texto del botón para cuando pueda usar icons
        self.__btn_rimuovi.setFixedSize(32, 32)
        self.__btn_rimuovi.setProperty(QssStyle.DESTRUCTIVE_BUTTON.style_role, True)

        layout = QGridLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.addWidget(widget_key, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(make_vline(), 0, 1)
        layout.addWidget(widget_value, 0, 2, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(make_vline(), 0, 3)
        layout.addWidget(self.__btn_rimuovi, 0, 4)

    def __connect_signals(self) -> None:
        self.__btn_rimuovi.clicked.connect(  # type:ignore
            partial(self.eliminaRequest.emit, self.__key)
        )
