from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import pyqtSignal
from functools import partial

from model.pianificazione.genere import Genere

from view.utils.list_widgets import ItemDisplay
from view.utils.hyphenate_text import HyphenatedLabel
from view.utils.custom_button import DefaultButton, ModificaButton, EliminaButton

from view.style.ui_style import WidgetRole, WidgetColor


class GenereDisplay(ItemDisplay):
    """View dei singoli generi della Lista Generi.

    Segnali
    ---
    - `modificaRequest(int)`: emesso quando si clicca il pulsante Modifica;
    - `eliminaConfermata()`: emesso quando si clicca il pulsante Sì.
    """

    modificaRequest = pyqtSignal(int)
    eliminaConfermata = pyqtSignal()

    def __init__(self, g: Genere, editable: bool):
        super().__init__()

        self.__editable = editable

        self.__setup_ui(g)
        self.__connect_signals(g)

    # ------------------------- SETUP INIT -------------------------

    def __setup_ui(self, g: Genere) -> None:
        # Labels
        nome = HyphenatedLabel(g.get_nome())
        nome.setProperty(WidgetRole.Label.HEADER2, True)

        descrizione = HyphenatedLabel(g.get_descrizione())
        descrizione.setProperty(WidgetRole.Label.BODY_TEXT, True)
        descrizione.setProperty(WidgetColor.Label.PRIMARY_COLOR, True)

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.addWidget(nome)
        layout.addWidget(descrizione)

        if self.__editable:
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
            domanda.setProperty(WidgetRole.Label.BODY_TEXT, True)
            domanda.setProperty(WidgetColor.Label.PRIMARY_COLOR, True)

            self.__btn_no = DefaultButton("No")
            self.__btn_si = EliminaButton("Sì", has_icon=False)

            self.__conferma_elimina = QWidget()
            layout_conferma = QHBoxLayout(self.__conferma_elimina)
            layout_conferma.setContentsMargins(1, 1, 1, 1)
            layout_conferma.addWidget(domanda)
            layout_conferma.addWidget(self.__btn_no)
            layout_conferma.addWidget(self.__btn_si)
            self.__conferma_elimina.hide()

            layout.addWidget(self.__pulsanti)
            layout.addWidget(self.__conferma_elimina)

    def __connect_signals(self, g: Genere) -> None:
        self.__id = g.get_id()

        if self.__editable:
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
        """Mostra una richiesta di conferma per eliminare il genere."""
        self.__pulsanti.hide()
        self.__conferma_elimina.show()

    def annulla_elimina(self) -> None:
        """Annulla l'elimina, nascondendo la richiesta di conferma."""
        self.__conferma_elimina.hide()
        self.__pulsanti.show()
