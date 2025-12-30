from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import pyqtSignal
from functools import partial

from model.pianificazione.genere import Genere

from view.utils.list_widgets import ItemDisplay
from view.style import QssStyle


class GenereDisplay(ItemDisplay):
    """View dei singoli generi della Lista Generi.

    Segnali:
    - modificaRequest(int): emesso quando si clicca il pulsante Modifica;
    - eliminaConfermata(int): emesso quando si clicca il pulsante Sì.
    """

    modificaRequest = pyqtSignal(int)
    eliminaConfermata = pyqtSignal(int)

    def __init__(self, g: Genere) -> None:
        super().__init__()

        self.__setup_ui(g)
        self.__connect_signals(g)

    # ------------------------- SETUP INIT -------------------------

    def __setup_ui(self, g: Genere) -> None:
        # Labels
        nome = QLabel(g.get_nome())
        nome.setProperty(QssStyle.HEADER2.style_role, True)

        descrizione = QLabel(g.get_descrizione())
        descrizione.setProperty(QssStyle.PARAGRAPH.style_role, True)
        descrizione.setWordWrap(True)

        # Pulsanti Modifica-Elimina
        self.__btn_modifica = QPushButton("Modifica")
        self.__btn_modifica.setProperty(QssStyle.MODIFY_BUTTON.style_role, True)

        self.__btn_elimina = QPushButton("Elimina")
        self.__btn_elimina.setProperty(QssStyle.DESTRUCTIVE_BUTTON.style_role, True)

        self.__pulsanti = QWidget()
        layout_pulsanti = QHBoxLayout(self.__pulsanti)
        layout_pulsanti.setContentsMargins(1, 1, 1, 1)
        layout_pulsanti.addWidget(self.__btn_modifica)
        layout_pulsanti.addWidget(self.__btn_elimina)
        layout_pulsanti.addStretch()

        # Pannello di eliminazione
        domanda = QLabel("<b>Sicuro di eliminare?</b>")
        domanda.setProperty(QssStyle.PARAGRAPH.style_role, True)

        self.__btn_no = QPushButton("No")
        self.__btn_no.setProperty(QssStyle.WHITE_BUTTON.style_role, True)

        self.__btn_si = QPushButton("Sì")
        self.__btn_si.setProperty(QssStyle.DESTRUCTIVE_BUTTON.style_role, True)

        self.__conferma_elimina = QWidget()
        layout_conferma = QHBoxLayout(self.__conferma_elimina)
        layout_conferma.setContentsMargins(1, 1, 1, 1)
        layout_conferma.addWidget(domanda)
        layout_conferma.addWidget(self.__btn_no)
        layout_conferma.addWidget(self.__btn_si)
        self.__conferma_elimina.hide()

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.addWidget(nome)
        layout.addWidget(descrizione)
        layout.addWidget(self.__pulsanti)
        layout.addWidget(self.__conferma_elimina)

    def __connect_signals(self, g: Genere) -> None:
        self.__id = g.get_id()

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
        """Mostra una richiesta di conferma per eliminare il genere."""
        self.__pulsanti.hide()
        self.__conferma_elimina.show()

    def annulla_elimina(self) -> None:
        """Annulla l'elimina, nascondendo la richiesta di conferma."""
        self.__conferma_elimina.hide()
        self.__pulsanti.show()
