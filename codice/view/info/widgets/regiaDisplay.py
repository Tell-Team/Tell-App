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

    # In prattica, questo QWidget pottrebe essere nella pagina NuovaRegiaView stessa, ma per
    #   tener il codice pulito preferisco creare un file dedicato a questa classe.
    modificaRequest = pyqtSignal(int)
    eliminaConfermata = pyqtSignal(int)

    def __init__(self, r: Regia) -> None:
        super().__init__()

        self.__setup_ui(r)
        self.__connect_signals(r)

    # ------------------------- SETUP INIT -------------------------

    # - Il QWidget potrebbe essere una tabella. Per renderlo distinto dalle opere e generi.
    def __setup_ui(self, r: Regia) -> None:
        # Labels
        titolo = QLabel(r.get_titolo())
        titolo.setObjectName("header3")

        regista = QLabel(f"Regista: {r.get_regista()}")
        regista.setObjectName("paragraph")

        anno = QLabel(f"Anno di produzione: {r.get_anno_produzione()}")
        anno.setObjectName("paragraph")

        # Pulsanti
        self.__btn_modifica = QPushButton("Modifica")
        self.__btn_modifica.setObjectName("whiteButton")

        self.__btn_elimina = QPushButton("Elimina")
        self.__btn_elimina.setObjectName("whiteButton")

        self.__pulsanti = QWidget()
        layout_pulsanti = QHBoxLayout(self.__pulsanti)
        layout_pulsanti.setContentsMargins(1, 1, 1, 1)
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

        self.__conferma_elimina = QWidget()
        layout_conferma = QHBoxLayout(self.__conferma_elimina)
        layout_conferma.setContentsMargins(1, 1, 1, 1)
        layout_conferma.addWidget(domanda)
        layout_conferma.addWidget(self.__btn_si)
        layout_conferma.addWidget(self.__btn_no)
        self.__conferma_elimina.hide()

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.addWidget(titolo)
        layout.addWidget(regista)
        layout.addWidget(anno)
        layout.addWidget(self.__pulsanti)
        layout.addWidget(self.__conferma_elimina)

    def __connect_signals(self, r: Regia) -> None:
        self.__id = r.get_id()

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
        """Mostra una richiesta di conferma per eliminare la regia."""
        self.__pulsanti.hide()
        self.__conferma_elimina.show()

    def annulla_elimina(self) -> None:
        """Annulla l'elimina, nascondendo la richiesta di conferma."""
        self.__conferma_elimina.hide()
        self.__pulsanti.show()
