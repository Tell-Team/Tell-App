from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QGridLayout,
)
from PyQt6.QtCore import Qt, pyqtSignal
from functools import partial

from model.organizzazione.posto import Posto

from view.utils.list_widgets import ItemDisplay
from view.utils.custom_button import ModificaButton, EliminaButton
from view.utils import make_vline

from view.style.ui_style import WidgetRole, WidgetColor


class PostoDisplay(ItemDisplay):
    """View dei singoli posti della pagina `ListaPostiView`.

    Segnali
    ---
    - `modificaRequest(int)`: emesso quando si clicca il pulsante Modifica;
    - `eliminaConfermata()`: emesso quando si clicca il pulsante Elimina.
    """

    modificaRequest = pyqtSignal(int)
    eliminaConfermata = pyqtSignal()

    def __init__(self, p: Posto):
        super().__init__()

        self.__setup_ui(p)
        self.__connect_signals(p)

    # ------------------------- SETUP INIT -------------------------

    def __setup_ui(self, p: Posto) -> None:
        # Labels
        data = QLabel(str(p.get_numero()))
        data.setProperty(WidgetRole.BODY_TEXT, True)
        data.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)

        # Pulsanti
        self.__btn_modifica = ModificaButton("")
        self.__btn_modifica.setMinimumHeight(32)

        self.__btn_elimina = EliminaButton("")
        self.__btn_elimina.setMinimumHeight(32)

        self.__pulsanti = QWidget()
        layout_pulsanti = QHBoxLayout(self.__pulsanti)
        layout_pulsanti.setContentsMargins(1, 1, 1, 1)
        layout_pulsanti.addWidget(self.__btn_modifica)
        layout_pulsanti.addWidget(self.__btn_elimina)

        dummy = QWidget()
        dummy_layout = QHBoxLayout(dummy)
        dummy_layout.addWidget(self.__pulsanti)

        # Layout
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(data, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(make_vline(), 0, 1)
        layout.addWidget(dummy, 0, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(2, 1)

    def __connect_signals(self, p: Posto) -> None:
        self.__id = p.get_id()

        # if self.__editable:
        self.__btn_modifica.clicked.connect(  # type:ignore
            partial(self.modificaRequest.emit, self.__id)
        )

        self.__btn_elimina.clicked.connect(  # type:ignore
            self.eliminaConfermata.emit
        )
