from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import pyqtSignal
from functools import partial

from model.pianificazione.spettacolo import Spettacolo
from model.pianificazione.regia import Regia  # - TESTING

from view.utils.list_widgets import ItemDisplay
from view.utils.hyphenate_text import HyphenatedLabel
from view.style import WidgetRole, WidgetColor


class SpettacoloDisplay(ItemDisplay):
    """View delle singole opere della Lista Opere.

    Segnali:
    - visualizzaRequest(int): emesso quando si clicca il pulsante Maggior info;
    - ScegliPostoRequest(int): emesso quando si clicca il pulsante Scegli posti;
    - modificaRequest(int): emesso quando si clicca il pulsante Modifica;
    - eliminaConfermata(int): emesso quando si clicca il pulsante Sì.
    """

    visualizzaRequest = pyqtSignal(int)
    scegliPostoRequest = pyqtSignal(int)
    modificaRequest = pyqtSignal(int)
    eliminaConfermata = pyqtSignal(int)

    def __init__(self, s: Spettacolo, editable: bool, dati: tuple[str, ...] = ()):
        super().__init__()

        self.__editable = editable

        self.__setup_ui(s, dati)
        self.__connect_signals(s)

    # ------------------------- SETUP INIT -------------------------

    def __setup_ui(self, s: Spettacolo, dati: tuple[str, ...] = ()) -> None:
        # Labels
        titolo = HyphenatedLabel(s.get_titolo())
        titolo.setProperty(WidgetRole.HEADER2, True)

        # Pulsanti
        self.__btn_visualizza = QPushButton("Maggior info")
        self.__btn_visualizza.setProperty(WidgetRole.DEFAULT_BUTTON, True)

        self.__btn_scegli_posti = QPushButton("Scegli posti")
        self.__btn_scegli_posti.setProperty(WidgetRole.DEFAULT_BUTTON, True)

        self.__pulsanti = QWidget()
        layout_pulsanti = QHBoxLayout(self.__pulsanti)
        layout_pulsanti.setContentsMargins(1, 1, 1, 1)
        layout_pulsanti.addWidget(self.__btn_visualizza)
        layout_pulsanti.addWidget(self.__btn_scegli_posti)

        # Layout
        self.__layout = QVBoxLayout(self)
        self.__layout.setContentsMargins(1, 1, 1, 1)
        self.__layout.addWidget(titolo)

        if isinstance(s, Regia):
            self.carica_dati_regia(dati)
        else:
            ...  # Nel caso ci siano altri sottoclassi di Spettacolo

        self.__layout.addWidget(self.__pulsanti)

        if self.__editable:
            self.__btn_modifica = QPushButton("Modifica")
            self.__btn_modifica.setProperty(WidgetRole.MODIFY_BUTTON, True)

            self.__btn_elimina = QPushButton("Elimina")
            self.__btn_elimina.setProperty(WidgetRole.DESTRUCTIVE_BUTTON, True)

            layout_pulsanti.addWidget(self.__btn_modifica)
            layout_pulsanti.addWidget(self.__btn_elimina)

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

            self.__layout.addWidget(self.__conferma_elimina)

        layout_pulsanti.addStretch()

    def __connect_signals(self, s: Spettacolo) -> None:
        self.__id = s.get_id()

        self.__btn_visualizza.clicked.connect(  # type:ignore
            partial(self.visualizzaRequest.emit, self.__id)
        )

        self.__btn_scegli_posti.clicked.connect(  # type:ignore
            partial(self.scegliPostoRequest.emit, self.__id)
        )

        if self.__editable:
            self.__btn_modifica.clicked.connect(  # type:ignore
                partial(self.modificaRequest.emit, self.__id)
            )

            self.__btn_elimina.clicked.connect(  # type:ignore
                self.__on_elimina
            )

            self.__btn_si.clicked.connect(  # type:ignore
                partial(self.eliminaConfermata.emit, self.__id)
            )

            self.__btn_no.clicked.connect(  # type:ignore
                self.annulla_elimina
            )

    # ------------------------- METODI DI VIEW -------------------------

    def __on_elimina(self) -> None:
        """Mostra una richiesta di conferma per eliminare l'opera."""
        self.__pulsanti.hide()
        self.__conferma_elimina.show()

    def annulla_elimina(self) -> None:
        """Annulla l'elimina, nascondendo la richiesta di conferma."""
        self.__conferma_elimina.hide()
        self.__pulsanti.show()

    # ------------------------- METODI PER CASI SPECIALI -------------------------

    def carica_dati_regia(self, dati: tuple[str, ...]) -> None:
        if not (len(dati) == 2):
            raise ValueError("dati deve essere un tuple di 2 string")

        compositore = HyphenatedLabel(f"Direttore d'orchestra: {dati[0]}")
        compositore.setProperty(WidgetRole.BODY_TEXT, True)
        compositore.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)
        self.__layout.addWidget(compositore)

        regista = HyphenatedLabel(f"Regista: {dati[1]}")
        regista.setProperty(WidgetRole.BODY_TEXT, True)
        regista.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)
        self.__layout.addWidget(regista)
