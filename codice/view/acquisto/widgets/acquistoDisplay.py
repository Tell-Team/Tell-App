from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import pyqtSignal
from functools import partial

from model.pianificazione.spettacolo import Spettacolo
from model.pianificazione.regia import Regia

from view.utils.list_widgets import ItemDisplay
from view.utils.hyphenate_text import HyphenatedLabel
from view.utils.custom_button import DefaultButton

from view.style.ui_style import WidgetRole, WidgetColor


class AcquistoDisplay(ItemDisplay):
    """View dei singoli spettacoli della Lista Spettacoli per la sezione Acquisto.

    Segnali
    ---
    - `scegliPostoRequest(int)`: emesso quando si clicca il pulsante Scegli posti.
    """

    scegliPostoRequest = pyqtSignal(int)

    def __init__(self, s: Spettacolo, dati: tuple[str, ...] = ()):
        super().__init__()

        self.__setup_ui(s, dati)
        self.__connect_signals(s)

    # ------------------------- SETUP INIT -------------------------

    def __setup_ui(self, s: Spettacolo, dati: tuple[str, ...] = ()) -> None:
        # Labels
        titolo = HyphenatedLabel(s.get_titolo())
        titolo.setProperty(WidgetRole.Label.HEADER2, True)

        self.__btn_scegli_posti = DefaultButton("Scegli posti")

        self.__pulsanti = QWidget()
        layout_pulsanti = QHBoxLayout(self.__pulsanti)
        layout_pulsanti.setContentsMargins(1, 1, 1, 1)
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

        layout_pulsanti.addStretch()

    def __connect_signals(self, s: Spettacolo) -> None:
        self.__id = s.get_id()

        self.__btn_scegli_posti.clicked.connect(  # type:ignore
            partial(self.scegliPostoRequest.emit, self.__id)
        )

    # ------------------------- METODI PER CASI SPECIALI -------------------------

    def carica_dati_regia(self, dati: tuple[str, ...]) -> None:
        if not (len(dati) == 2):
            raise ValueError("dati deve essere un tuple[str, str]")

        compositore = HyphenatedLabel(f"Compositore: {dati[0]}")
        compositore.setProperty(WidgetRole.Label.BODY_TEXT, True)
        compositore.setProperty(WidgetColor.Label.PRIMARY_COLOR, True)
        self.__layout.addWidget(compositore)

        regista = HyphenatedLabel(f"Regista: {dati[1]}")
        regista.setProperty(WidgetRole.Label.BODY_TEXT, True)
        regista.setProperty(WidgetColor.Label.PRIMARY_COLOR, True)
        self.__layout.addWidget(regista)
