from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QGridLayout,
    QStackedWidget,
)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Optional

from model.organizzazione.sezione import Sezione
from model.organizzazione.prezzo import Prezzo

from view.utils.list_widgets import ItemDisplay
from view.utils.custom_button import (
    ModificaButton,
    CreaButton,
    EliminaButton,
)
from view.utils import make_vline

from view.style.ui_style import WidgetRole, WidgetColor


class SezioniPrezziDisplay(ItemDisplay):
    """View della coppia sezione-prezzo della pagina `PrezziAssociatiPage`.

    Segnali
    ---
    - `creaRequest()`: emesso quando si clicca il pulsante Aggiungi;
    - `modificaRequest()`: emesso quando si clicca il pulsante Modifica;
    - `eliminaConfermata()`: emesso quando si clicca il pulsante Elimina.
    """

    creaRequest = pyqtSignal()
    modificaRequest = pyqtSignal()
    eliminaConfermata = pyqtSignal()

    def __init__(self, s: Sezione, p: Optional[Prezzo]):
        super().__init__()

        self.__setup_ui(s, p)
        self.__connect_signals()

    # ------------------------- SETUP INIT -------------------------

    def __setup_ui(self, s: Sezione, p: Optional[Prezzo]) -> None:
        # Labels
        self.label_sezione = QLabel(s.get_nome())
        self.label_sezione.setProperty(WidgetRole.Label.BODY_TEXT, True)
        self.label_sezione.setProperty(WidgetColor.Label.PRIMARY_COLOR, True)

        self.label_prezzo = QLabel(
            f"{p.get_ammontare():.2f}" if (p is not None) else "Non definito"
        )
        self.label_prezzo.setProperty(WidgetRole.Label.BODY_TEXT, True)
        self.label_prezzo.setProperty(WidgetColor.Label.PRIMARY_COLOR, True)

        # Layout
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(
            self.label_sezione, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(make_vline(), 0, 1)
        layout.addWidget(
            self.label_prezzo, 0, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(2, 1)

        # Pulsanti
        self.__btn_modifica = ModificaButton("")
        self.__btn_modifica.setMinimumHeight(32)

        self.__btn_crea = CreaButton("")
        self.__btn_crea.setMinimumHeight(32)

        self.stack_pulsanti = QStackedWidget()
        self.stack_pulsanti.addWidget(self.__btn_modifica)
        self.stack_pulsanti.addWidget(self.__btn_crea)
        self.stack_pulsanti.setCurrentWidget(
            self.__btn_modifica if (p is not None) else self.__btn_crea
        )

        self.__btn_elimina = EliminaButton("")
        self.__btn_elimina.setMinimumHeight(32)

        self.__pulsanti = QWidget()
        layout_pulsanti = QHBoxLayout(self.__pulsanti)
        layout_pulsanti.setContentsMargins(1, 1, 1, 1)
        layout_pulsanti.addWidget(self.stack_pulsanti)
        layout_pulsanti.addWidget(self.__btn_elimina)

        layout.addWidget(make_vline(), 0, 3)
        layout.addWidget(self.__pulsanti, 0, 4, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.setColumnStretch(4, 1)

    def __connect_signals(self) -> None:
        self.__btn_modifica.clicked.connect(  # type:ignore
            self.modificaRequest.emit
        )

        self.__btn_crea.clicked.connect(  # type:ignore
            self.creaRequest.emit
        )

        self.__btn_elimina.clicked.connect(  # type:ignore
            self.eliminaConfermata.emit
        )
