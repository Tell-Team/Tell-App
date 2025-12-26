from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QGridLayout,
    QFrame,
)
from PyQt6.QtCore import Qt, pyqtSignal
from functools import partial

from model.pianificazione.regia import Regia

from view.utils.list_widgets import ItemDisplay
from view.style import QssStyle


class RegiaDisplay(ItemDisplay):
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

    def __setup_ui(self, r: Regia) -> None:
        # Labels
        titolo = QLabel(r.get_titolo())
        titolo.setProperty(QssStyle.PARAGRAPH.style_role, True)

        regista_anno = QLabel(f"{r.get_regista()} ({r.get_anno_produzione()})")
        regista_anno.setProperty(QssStyle.PARAGRAPH.style_role, True)

        # Pulsanti
        self.__btn_modifica = QPushButton("Modifica")
        self.__btn_modifica.setProperty(QssStyle.WHITE_BUTTON.style_role, True)

        self.__btn_elimina = QPushButton("Elimina")
        self.__btn_elimina.setProperty(QssStyle.DESTRUCTIVE_BUTTON.style_role, True)

        self.__pulsanti = QWidget()
        layout_pulsanti = QHBoxLayout(self.__pulsanti)
        layout_pulsanti.setContentsMargins(1, 1, 1, 1)
        layout_pulsanti.addWidget(self.__btn_modifica)
        layout_pulsanti.addWidget(self.__btn_elimina)

        # Pannello di eliminazione
        domanda = QLabel("Sicuro di eliminare?")
        domanda.setProperty(QssStyle.PARAGRAPH.style_role, True)

        self.__btn_si = QPushButton("Sì")
        self.__btn_si.setProperty(QssStyle.WHITE_BUTTON.style_role, True)

        self.__btn_no = QPushButton("No")
        self.__btn_no.setProperty(QssStyle.WHITE_BUTTON.style_role, True)

        self.__conferma_elimina = QWidget()
        layout_conferma = QHBoxLayout(self.__conferma_elimina)
        layout_conferma.setContentsMargins(1, 1, 1, 1)
        layout_conferma.addWidget(domanda)
        layout_conferma.addWidget(self.__btn_si)
        layout_conferma.addWidget(self.__btn_no)
        self.__conferma_elimina.hide()

        dummy = QWidget()
        dummy_layout = QHBoxLayout(dummy)
        dummy_layout.addWidget(self.__pulsanti)
        dummy_layout.addWidget(self.__conferma_elimina)

        def make_vline() -> QFrame:
            line = QFrame()
            line.setFrameShape(QFrame.Shape.VLine)
            line.setFrameShadow(QFrame.Shadow.Sunken)
            return line

        # Layout
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(titolo, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(make_vline(), 0, 1)
        layout.addWidget(regista_anno, 0, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(make_vline(), 0, 3)
        layout.addWidget(dummy, 0, 4, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(4, 1)

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
