from PyQt6.QtWidgets import QLabel, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from functools import partial

from model.organizzazione.evento import Evento
from model.organizzazione.sezione import Sezione
from model.organizzazione.posto import Posto

from view.utils.list_widgets import ItemDisplay
from view.utils.horizontal_scroll import HorizontalWheelScrollArea
from view.utils.custom_button import EliminaButton
from view.utils import make_vline

from view.style.ui_style import WidgetRole, WidgetColor


class PostoSceltoDisplay(ItemDisplay):
    """View dei posti da prenotare per un evento.

    Segnali
    ---
    - `eliminaRequest(tuple[Evento, Sezione, Posto])`: emesso quando si clicca il
    pulsante di elimina [X].
    """

    eliminaRequest = pyqtSignal(tuple)

    def __init__(self, e: Evento, s: Sezione, p: Posto):
        super().__init__()

        self.__setup_ui(e, s, p)
        self.__connect_signals()

    def __setup_ui(self, e: Evento, s: Sezione, p: Posto) -> None:
        self.__prenotazione_key = (e, s, p)

        label_identificador = QLabel(
            f"<b>Data: </b> {e.get_data_ora().strftime("%d/%m/%y - %H:%M")}, "
            + f"<b>Sezione:</b> {s.get_nome()}, "
            + f"<b>Posto:</b> {p.get_fila()} #{p.get_numero()}"
        )
        label_identificador.setProperty(WidgetRole.BODY_TEXT, True)
        label_identificador.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)
        scroll_label = HorizontalWheelScrollArea()
        scroll_label.setWidget(label_identificador)
        # scroll_label.setMinimumWidth(250)

        self.__btn_rimuovi = EliminaButton()
        self.__btn_rimuovi.setFixedSize(32, 32)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 5, 0)
        layout.addWidget(
            scroll_label,
            alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
        )
        layout.addWidget(make_vline())
        layout.addWidget(self.__btn_rimuovi)

        layout.setStretch(0, 1)
        layout.setStretch(2, 2)

    def __connect_signals(self) -> None:
        self.__btn_rimuovi.clicked.connect(  # type:ignore
            partial(self.eliminaRequest.emit, self.__prenotazione_key)
        )
