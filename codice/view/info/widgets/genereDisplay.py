from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import pyqtSignal
from functools import partial

from model.pianificazione.genere import Genere


class GenereDisplay(QWidget):
    """View dei singoli generi della Lista Generi.

    Segnali:
    - modificaRequest(int): emesso quando si clicca il pulsante Modifica;
    - eliminaConfermata(int): emesso quando si clicca il pulsante Sì;
    """

    modificaRequest = pyqtSignal(int)
    eliminaConfermata = pyqtSignal(int)

    def __init__(self, g: Genere) -> None:
        super().__init__()

        self._setup_ui(g)
        self._connect_signals(g)

    # ------------------------- SETUP INIT -------------------------

    def _setup_ui(self, g: Genere) -> None:
        # Labels
        nome = QLabel(f"{g.get_nome()}")
        nome.setObjectName("Header2")

        descrizione = QLabel(f"{g.get_descrizione()}")
        descrizione.setObjectName("Paragraph")
        descrizione.setWordWrap(True)

        # Pulsanti Modifica-Elimina
        self.__btn_modifica = QPushButton("Modifica")
        self.__btn_modifica.setObjectName("WhiteButton")

        self.__btn_elimina = QPushButton("Elimina")
        self.__btn_elimina.setObjectName("WhiteButton")

        self.pulsanti = QWidget()
        layout_pulsanti = QHBoxLayout(self.pulsanti)
        layout_pulsanti.addWidget(self.__btn_modifica)
        layout_pulsanti.addWidget(self.__btn_elimina)
        layout_pulsanti.addStretch()

        # Pannello di eliminazione
        domanda = QLabel("Sicuro di eliminare?")
        domanda.setObjectName("Paragraph")

        self.__btn_si = QPushButton("Sì")
        self.__btn_si.setObjectName("WhiteButton")

        self.__btn_no = QPushButton("No")
        self.__btn_no.setObjectName("WhiteButton")

        self.conferma_elimina = QWidget()
        layout_conferma = QHBoxLayout(self.conferma_elimina)
        layout_conferma.addWidget(domanda)
        layout_conferma.addWidget(self.__btn_si)
        layout_conferma.addWidget(self.__btn_no)
        self.conferma_elimina.hide()

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(nome)
        layout.addWidget(descrizione)
        layout.addWidget(self.pulsanti)
        layout.addWidget(self.conferma_elimina)

    def _connect_signals(self, g: Genere) -> None:
        self._id = g.get_id()

        self.__btn_modifica.clicked.connect(  # type:ignore
            partial(self.modificaRequest.emit, self._id)
        )

        self.__btn_elimina.clicked.connect(  # type:ignore
            self._on_elimina
        )

        self.__btn_si.clicked.connect(  # type:ignore
            partial(self.eliminaConfermata.emit, self._id)
        )

        self.__btn_no.clicked.connect(  # type:ignore
            self.annulla_elimina
        )

    # ------------------------- METODI DI VIEW -------------------------

    def _on_elimina(self) -> None:
        """Mostra una richiesta di conferma per eliminare il genere."""
        self.pulsanti.hide()
        self.conferma_elimina.show()

    def annulla_elimina(self) -> None:
        """Annulla l'elimina, nascondendo la richiesta di conferma."""
        self.conferma_elimina.hide()
        self.pulsanti.show()
