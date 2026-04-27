from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QGridLayout,
)
from PyQt6.QtCore import Qt, pyqtSignal
from functools import partial

from model.pianificazione.regia import Regia

from view.utils.list_widgets import ItemDisplay
from view.utils.horizontal_scroll import HorizontalWheelScrollArea
from view.utils.custom_button import DefaultButton, ModificaButton, EliminaButton
from view.utils import make_vline

from view.style.ui_style import WidgetRole, WidgetColor


class RegiaDisplay(ItemDisplay):
    """View delle singole regia della Lista Regie dentro della pagina `VisualizzaOperaPage`.

    Segnali
    ---
    - `modificaRequest(int)`: emesso quando si clicca il pulsante Modifica;
    - `eliminaConfermata()`: emesso quando si clicca il pulsante Sì.
    """

    # In prattica, questo QWidget pottrebe essere nella pagina NuovaRegiaPage stessa, ma per
    #   tener il codice pulito preferisco creare un file dedicato a questa classe.
    modificaRequest = pyqtSignal(int)
    eliminaConfermata = pyqtSignal()

    def __init__(self, r: Regia, editable: bool):
        super().__init__()

        self.__editable = editable

        self.__setup_ui(r)
        self.__connect_signals(r)

    # ------------------------- SETUP INIT -------------------------

    def __setup_ui(self, r: Regia) -> None:
        # Labels
        # titolo = QLabel(r.get_titolo())
        # titolo.setProperty(WidgetRole.BODY_TEXT, True)
        # titolo.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)
        # scroll_titolo = HorizontalWheelScrollArea()
        # scroll_titolo.setWidget(titolo)

        regista_anno = QLabel(f"{r.get_regista()} ({r.get_anno_produzione()})")
        regista_anno.setProperty(WidgetRole.Label.BODY_TEXT, True)
        regista_anno.setProperty(WidgetColor.Label.PRIMARY_COLOR, True)
        scroll_regista_anno = HorizontalWheelScrollArea()
        scroll_regista_anno.setWidget(regista_anno)

        # Layout
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        # layout.addWidget(scroll_titolo, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        # layout.addWidget(make_vline(), 0, 0)
        layout.addWidget(
            scroll_regista_anno, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter
        )

        layout.setColumnStretch(0, 1)
        # layout.setColumnStretch(2, 1)

        if self.__editable:
            # Pulsanti
            self.__btn_modifica = ModificaButton("Modifica")
            self.__btn_modifica.setMinimumHeight(32)

            self.__btn_elimina = EliminaButton("Elimina")
            self.__btn_elimina.setMinimumHeight(32)

            self.__pulsanti = QWidget()
            layout_pulsanti = QHBoxLayout(self.__pulsanti)
            layout_pulsanti.setContentsMargins(1, 1, 1, 1)
            layout_pulsanti.addWidget(self.__btn_modifica)
            layout_pulsanti.addWidget(self.__btn_elimina)

            # Pannello di eliminazione
            domanda = QLabel("<b>Sicuro?</b>")
            domanda.setProperty(WidgetRole.Label.BODY_TEXT, True)
            domanda.setProperty(WidgetColor.Label.PRIMARY_COLOR, True)

            self.__btn_si = EliminaButton("Sì", has_icon=False)
            self.__btn_si.setMinimumSize(40, 32)

            self.__btn_no = DefaultButton("No")
            self.__btn_no.setMinimumSize(40, 32)

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

            layout.addWidget(make_vline(), 0, 1)
            layout.addWidget(dummy, 0, 2, alignment=Qt.AlignmentFlag.AlignCenter)

            layout.setColumnStretch(2, 1)

    def __connect_signals(self, r: Regia) -> None:
        if self.__editable:
            self.__id = r.get_id()

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
        """Mostra una richiesta di conferma per eliminare la regia."""
        self.__pulsanti.hide()
        self.__conferma_elimina.show()

    def annulla_elimina(self) -> None:
        """Annulla l'elimina, nascondendo la richiesta di conferma."""
        self.__conferma_elimina.hide()
        self.__pulsanti.show()
