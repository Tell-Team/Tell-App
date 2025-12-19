from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtCore import pyqtSignal
from functools import partial

from model.pianificazione.opera import Opera


class OperaDisplay(QWidget):
    """View delle singole opere della Lista Opere.

    Segnali:
    - visualizzaRequest(int): emesso quando si clicca il pulsante Maggior info;
    - modificaRequest(int): emesso quando si clicca il pulsante Modifica;
    - eliminaConfermata(int): emesso quando si clicca il pulsante Sì;
    """

    visualizzaRequest = pyqtSignal(int)
    modificaRequest = pyqtSignal(int)
    eliminaConfermata = pyqtSignal(int)

    def __init__(self, o: Opera) -> None:
        super().__init__()

        self._setup_ui(o)
        self._connect_signals(o)

    # ------------------------- SETUP INIT -------------------------

    def _setup_ui(self, o: Opera) -> None:
        # Labels
        nome = QLabel(f"{o.get_nome()}")
        nome.setObjectName("Header2")

        librettista = QLabel(f"Libretto di {o.get_librettista()}")
        librettista.setObjectName("Paragraph")

        compositore = QLabel(f"Musica di {o.get_compositore()}")
        compositore.setObjectName("Paragraph")

        # Pulsanti
        self._btn_visualizza = QPushButton("Maggior info")
        self._btn_visualizza.setObjectName("WhiteButton")

        self._btn_modifica = QPushButton("Modifica")
        self._btn_modifica.setObjectName("WhiteButton")

        self._btn_elimina = QPushButton("Elimina")
        self._btn_elimina.setObjectName("WhiteButton")

        self.pulsanti = QWidget()
        layout_btn = QHBoxLayout(self.pulsanti)
        layout_btn.addWidget(self._btn_visualizza)
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
        layout.addWidget(nome)
        layout.addWidget(librettista)
        layout.addWidget(compositore)
        layout.addWidget(self.pulsanti)
        layout.addWidget(self.conferma_elimina)

    def _connect_signals(self, o: Opera) -> None:
        self._id = o.get_id()

        self._btn_visualizza.clicked.connect(  # type:ignore
            partial(self.visualizzaRequest.emit, self._id)
        )

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
        """Mostra una richiesta di conferma per eliminare l'opera."""
        self.pulsanti.hide()
        self.conferma_elimina.show()

    def annulla_elimina(self) -> None:
        """Cancella l'elimina, nascondendo la richiesta di conferma."""
        self.conferma_elimina.hide()
        self.pulsanti.show()
