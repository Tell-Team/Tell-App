from PyQt6.QtWidgets import QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from functools import partial

from view.utils.list_widgets import ItemDisplay
from view.utils.horizontal_scroll import HorizontalWheelScrollArea
from view.utils import make_vline
from view.style import WidgetRole, WidgetColor


class PersonaleDisplay(ItemDisplay):
    """View degli interpreti e tecnici degli spettacoli.

    Segnali
    ---
    - `eliminaRequest(str)`: emesso quando si clicca il pulsante di elimina [X].
    """

    eliminaRequest = pyqtSignal(str)

    def __init__(self, key: str, value: str):
        super().__init__()

        self.__setup_ui(key, value)
        self.__connect_signals()

    def __setup_ui(self, key: str, value: str) -> None:
        self.__key = key

        widget_key = QLabel(self.__key)
        widget_key.setProperty(WidgetRole.BODY_TEXT, True)
        widget_key.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)
        scroll_key = HorizontalWheelScrollArea()
        scroll_key.setWidget(widget_key)
        scroll_key.setMinimumWidth(250)  # - DA CORRIGERE

        widget_value = QLabel(value)
        widget_value.setProperty(WidgetRole.BODY_TEXT, True)
        widget_value.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)
        scroll_value = HorizontalWheelScrollArea()
        scroll_value.setWidget(widget_value)
        scroll_value.setMinimumWidth(200)  # - DA CORRIGERE

        self.__btn_rimuovi = QPushButton("X")
        # - Quitar el texto del botón para cuando pueda usar icons
        self.__btn_rimuovi.setFixedSize(32, 32)
        self.__btn_rimuovi.setProperty(WidgetRole.DESTRUCTIVE_BUTTON, True)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 5, 0)
        layout.addWidget(
            scroll_key,
            alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
        )
        layout.addWidget(make_vline())
        layout.addWidget(
            scroll_value,
            alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
        )
        layout.addWidget(make_vline())
        layout.addWidget(self.__btn_rimuovi)

        layout.setStretch(0, 1)
        layout.setStretch(2, 2)
        layout.setStretch(4, 0)

    def __connect_signals(self) -> None:
        self.__btn_rimuovi.clicked.connect(  # type:ignore
            partial(self.eliminaRequest.emit, self.__key)
        )
