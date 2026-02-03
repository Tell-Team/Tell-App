from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import pyqtSignal
from functools import partial

from model.organizzazione.sezione import Sezione

from view.utils.list_widgets import ItemDisplay
from view.utils.hyphenate_text import HyphenatedLabel
from view.utils.custom_button import ModificaButton, EliminaButton

from view.style.ui_style import WidgetRole, WidgetColor


class SezioneDisplay(ItemDisplay):
    """View delle singole sezioni della Lista Sezioni.

    Segnali
    ---
    - `modificaRequest(int)`: emesso quando si clicca il pulsante Modifica;
    - `eliminaConfermata()`: emesso quando si clicca il pulsante Sì.
    """

    modificaRequest = pyqtSignal(int)
    eliminaConfermata = pyqtSignal()

    def __init__(self, s: Sezione):
        super().__init__()

        self.__setup_ui(s)
        self.__connect_signals(s)

    # ------------------------- SETUP INIT -------------------------

    def __setup_ui(self, s: Sezione) -> None:
        # Labels
        nome = HyphenatedLabel(s.get_nome())
        nome.setProperty(WidgetRole.HEADER2, True)

        descrizione = HyphenatedLabel(s.get_descrizione())
        descrizione.setProperty(WidgetRole.BODY_TEXT, True)
        descrizione.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.addWidget(nome)
        layout.addWidget(descrizione)

        # Pulsanti Modifica-Elimina
        self.__btn_modifica = ModificaButton("Modifica")

        self.__btn_elimina = EliminaButton("Elimina")

        self.__pulsanti = QWidget()
        layout_pulsanti = QHBoxLayout(self.__pulsanti)
        layout_pulsanti.setContentsMargins(1, 1, 1, 1)
        layout_pulsanti.addWidget(self.__btn_modifica)
        layout_pulsanti.addWidget(self.__btn_elimina)
        layout_pulsanti.addStretch()

        # Pannello di eliminazione
        domanda = QLabel("<b>Sicuro di eliminare?</b>")
        domanda.setProperty(WidgetRole.BODY_TEXT, True)
        domanda.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)

        self.__btn_no = QPushButton("No")
        self.__btn_no.setProperty(WidgetRole.DEFAULT_BUTTON, True)

        self.__btn_si = QPushButton("Sì")
        self.__btn_si.setProperty(WidgetRole.DESTRUCTIVE_BUTTON, True)

        self.__conferma_elimina = QWidget()
        layout_conferma = QHBoxLayout(self.__conferma_elimina)
        layout_conferma.setContentsMargins(1, 1, 1, 1)
        layout_conferma.addWidget(domanda)
        layout_conferma.addWidget(self.__btn_no)
        layout_conferma.addWidget(self.__btn_si)
        self.__conferma_elimina.hide()

        layout.addWidget(self.__pulsanti)
        layout.addWidget(self.__conferma_elimina)

    def __connect_signals(self, s: Sezione) -> None:
        self.__id = s.get_id()

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
        """Mostra una richiesta di conferma per eliminare la sezione."""
        self.__pulsanti.hide()
        self.__conferma_elimina.show()

    def annulla_elimina(self) -> None:
        """Annulla l'elimina, nascondendo la richiesta di conferma."""
        self.__conferma_elimina.hide()
        self.__pulsanti.show()
