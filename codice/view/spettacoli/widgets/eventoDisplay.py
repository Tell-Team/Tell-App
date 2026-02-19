from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QGridLayout,
)
from PyQt6.QtCore import Qt, pyqtSignal
from functools import partial

from model.organizzazione.evento import Evento

from view.utils.list_widgets import ItemDisplay
from view.utils.custom_button import DefaultButton, ModificaButton, EliminaButton
from view.utils import make_vline

from view.style.ui_style import WidgetRole, WidgetColor


class EventoDisplay(ItemDisplay):
    """View dei singoli eventi della Lista Eventi dentro della pagina
    `VisualizzaSpettacoloPage`.

    Segnali
    ---
    - `scegliPostiRequest(int)`: emesso quando si clicca il pulsante Scegli posti;
    - `modificaRequest(int)`: emesso quando si clicca il pulsante Modifica;
    - `eliminaConfermata()`: emesso quando si clicca il pulsante Sì.
    """

    scegliPostiRequest = pyqtSignal(int)
    modificaRequest = pyqtSignal(int)
    eliminaConfermata = pyqtSignal()

    def __init__(self, ev: Evento):
        super().__init__()

        self.__setup_ui(ev)
        self.__connect_signals(ev)

    # ------------------------- SETUP INIT -------------------------

    def __setup_ui(self, ev: Evento) -> None:
        # Labels
        data = QLabel(ev.get_data_ora().strftime("%d-%m-%Y"))
        data.setProperty(WidgetRole.Label.BODY_TEXT, True)
        data.setProperty(WidgetColor.Label.PRIMARY_COLOR, True)

        ora = QLabel(ev.get_data_ora().strftime("%H:%M"))
        ora.setProperty(WidgetRole.Label.BODY_TEXT, True)
        ora.setProperty(WidgetColor.Label.PRIMARY_COLOR, True)

        # Layout
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(data, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(make_vline(), 0, 1)
        layout.addWidget(ora, 0, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(2, 1)

        # if self.__editable:
        # Pulsanti
        self.__btn_modifica = ModificaButton("Modifica")
        self.__btn_modifica.setMinimumHeight(32)

        self.__btn_elimina = EliminaButton("Elimina")
        self.__btn_elimina.setMinimumHeight(32)

        self.__pulsanti = QWidget()
        layout_pulsanti = QHBoxLayout(self.__pulsanti)
        layout_pulsanti.setContentsMargins(1, 1, 1, 1)
        layout_pulsanti.addWidget(self.__btn_modifica)
        layout_pulsanti.addWidget(self.__btn_elimina)

        # Pannello di eliminazione
        domanda = QLabel("<b>Sicuro?</b>")
        domanda.setProperty(WidgetRole.Label.BODY_TEXT, True)
        domanda.setProperty(WidgetColor.Label.PRIMARY_COLOR, True)

        self.__btn_si = EliminaButton("Sì", has_icon=False)
        self.__btn_si.setMinimumSize(40, 32)

        self.__btn_no = DefaultButton("No")
        self.__btn_no.setMinimumSize(40, 32)

        self.__conferma_elimina = QWidget()
        layout_conferma = QHBoxLayout(self.__conferma_elimina)
        layout_conferma.setContentsMargins(1, 1, 1, 1)
        layout_conferma.addWidget(domanda)
        layout_conferma.addWidget(self.__btn_si)
        layout_conferma.addWidget(self.__btn_no)
        self.__conferma_elimina.hide()

        dummy = QWidget()
        dummy_layout = QHBoxLayout(dummy)
        dummy_layout.addWidget(self.__pulsanti)
        dummy_layout.addWidget(self.__conferma_elimina)

        layout.addWidget(make_vline(), 0, 3)
        layout.addWidget(dummy, 0, 4, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.setColumnStretch(4, 1)

    def __connect_signals(self, ev: Evento) -> None:
        self.__id = ev.get_id()

        # if self.__editable:
        self.__btn_modifica.clicked.connect(  # type:ignore
            partial(self.modificaRequest.emit, self.__id)
        )

        self.__btn_elimina.clicked.connect(  # type:ignore
            self.__on_elimina
        )

        self.__btn_si.clicked.connect(  # type:ignore
            self.eliminaConfermata.emit
        )

        self.__btn_no.clicked.connect(  # type:ignore
            self.annulla_elimina
        )

    # ------------------------- METODI DI VIEW -------------------------

    def __on_elimina(self) -> None:
        """Mostra una richiesta di conferma per eliminare la regia."""
        self.__pulsanti.hide()
        self.__conferma_elimina.show()

    def annulla_elimina(self) -> None:
        """Annulla l'elimina, nascondendo la richiesta di conferma."""
        self.__conferma_elimina.hide()
        self.__pulsanti.show()
