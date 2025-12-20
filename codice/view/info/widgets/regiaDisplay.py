from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import pyqtSignal
from functools import partial

from model.pianificazione.regia import Regia


class RegiaDisplay(QWidget):
    """View delle singole regia della Lista Regie dentro della pagina `VisualizzaOperaView`.

    Segnali:
    - modificaRequest(int): emesso quando si clicca il pulsante Modifica;
    - eliminaConfermata(int): emesso quando si clicca il pulsante Sì;
    """

    modificaRequest = pyqtSignal(int)
    eliminaConfermata = pyqtSignal(int)

    def __init__(self, r: Regia) -> None:
        super().__init__()

        self._setup_ui(r)
        self._connect_signals(r)

    # ------------------------- SETUP INIT -------------------------

    def _setup_ui(self, r: Regia) -> None:
        # Labels
        titolo = QLabel(f"{r.get_titolo()}")
        titolo.setObjectName("Header2")

        regista = QLabel(f"Regista: {r.get_regista()}")
        regista.setObjectName("Paragraph")

        anno = QLabel(f"Anno di produzione: {r.get_anno_produzione()}")
        anno.setObjectName("Paragraph")

        # Pulsanti
        self._btn_modifica = QPushButton("Modifica")
        self._btn_modifica.setObjectName("WhiteButton")

        self._btn_elimina = QPushButton("Elimina")
        self._btn_elimina.setObjectName("WhiteButton")

        self.pulsanti = QWidget()
        layout_btn = QHBoxLayout(self.pulsanti)
        layout_btn.addWidget(self._btn_modifica)
        layout_btn.addWidget(self._btn_elimina)
        layout_btn.addStretch()

        # Pannello di eliminazione
        domanda = QLabel("Sicuro di eliminare?")
        domanda.setObjectName("Paragraph")

        self._btn_si = QPushButton("Sì")
        self._btn_si.setObjectName("WhiteButton")

        self._btn_no = QPushButton("No")
        self._btn_no.setObjectName("WhiteButton")

        self.conferma_elimina = QWidget()
        layout_conferma = QHBoxLayout(self.conferma_elimina)
        layout_conferma.addWidget(domanda)
        layout_conferma.addWidget(self._btn_si)
        layout_conferma.addWidget(self._btn_no)
        self.conferma_elimina.hide()

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(titolo)
        layout.addWidget(regista)
        layout.addWidget(anno)
        layout.addWidget(self.pulsanti)
        layout.addWidget(self.conferma_elimina)

    def _connect_signals(self, r: Regia) -> None:
        self._id = r.get_id()

        self._btn_modifica.clicked.connect(  # type:ignore
            partial(self.modificaRequest.emit, self._id)
        )

        self._btn_elimina.clicked.connect(  # type:ignore
            self._on_elimina
        )

        self._btn_si.clicked.connect(  # type:ignore
            partial(self.eliminaConfermata.emit, self._id)
        )

        self._btn_no.clicked.connect(  # type:ignore
            self.annulla_elimina
        )

    # ------------------------- METODI DI VIEW -------------------------

    def _on_elimina(self) -> None:
        """Mostra una richiesta di conferma per eliminare la regia."""
        self.pulsanti.hide()
        self.conferma_elimina.show()

    def annulla_elimina(self) -> None:
        """Annulla l'elimina, nascondendo la richiesta di conferma."""
        self.conferma_elimina.hide()
        self.pulsanti.show()
