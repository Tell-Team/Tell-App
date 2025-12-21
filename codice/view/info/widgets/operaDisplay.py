from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
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
        nome = QLabel(o.get_nome())
        nome.setObjectName("header2")

        librettista = QLabel(f"Libretto di {o.get_librettista()}")
        librettista.setObjectName("paragraph")

        compositore = QLabel(f"Musica di {o.get_compositore()}")
        compositore.setObjectName("paragraph")

        # Pulsanti
        self.__btn_visualizza = QPushButton("Maggior info")
        self.__btn_visualizza.setObjectName("whiteButton")

        self.__btn_modifica = QPushButton("Modifica")
        self.__btn_modifica.setObjectName("whiteButton")

        self.__btn_elimina = QPushButton("Elimina")
        self.__btn_elimina.setObjectName("whiteButton")

        self.pulsanti = QWidget()
        layout_pulsanti = QHBoxLayout(self.pulsanti)
        layout_pulsanti.setContentsMargins(1, 1, 1, 1)
        layout_pulsanti.addWidget(self.__btn_visualizza)
        layout_pulsanti.addWidget(self.__btn_modifica)
        layout_pulsanti.addWidget(self.__btn_elimina)
        layout_pulsanti.addStretch()

        # Pannello di eliminazione
        domanda = QLabel("Sicuro di eliminare?")
        domanda.setObjectName("paragraph")

        self.__btn_si = QPushButton("Sì")
        self.__btn_si.setObjectName("whiteButton")

        self.__btn_no = QPushButton("No")
        self.__btn_no.setObjectName("whiteButton")

        self.conferma_elimina = QWidget()
        layout_conferma = QHBoxLayout(self.conferma_elimina)
        layout_conferma.setContentsMargins(1, 1, 1, 1)
        layout_conferma.addWidget(domanda)
        layout_conferma.addWidget(self.__btn_si)
        layout_conferma.addWidget(self.__btn_no)
        self.conferma_elimina.hide()

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.addWidget(nome)
        layout.addWidget(librettista)
        layout.addWidget(compositore)
        layout.addWidget(self.pulsanti)
        layout.addWidget(self.conferma_elimina)

    def _connect_signals(self, o: Opera) -> None:
        self._id = o.get_id()

        self.__btn_visualizza.clicked.connect(  # type:ignore
            partial(self.visualizzaRequest.emit, self._id)
        )

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
        """Mostra una richiesta di conferma per eliminare l'opera."""
        self.pulsanti.hide()
        self.conferma_elimina.show()

    def annulla_elimina(self) -> None:
        """Annulla l'elimina, nascondendo la richiesta di conferma."""
        self.conferma_elimina.hide()
        self.pulsanti.show()
