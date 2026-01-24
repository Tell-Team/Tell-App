from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import pyqtSignal
from functools import partial

from model.account.account import Account

from view.utils.list_widgets import ItemDisplay
from view.utils.hyphenate_text import HyphenatedLabel
from view.style.ui_style import WidgetRole, WidgetColor


class AccountDisplay(ItemDisplay):
    """View dei singoli account della Lista Account.

    Segnali
    ---
    - `modificaRequest(int)`: emesso quando si clicca il pulsante Modifica;
    - `eliminaConfermata()`: emesso quando si clicca il pulsante Sì.
    """

    modificaRequest = pyqtSignal(int)
    eliminaConfermata = pyqtSignal()

    def __init__(self, acc: Account, editable: bool):
        super().__init__()

        self.__editable = editable

        self.__setup_ui(acc)
        self.__connect_signals(acc)

    # ------------------------- SETUP INIT -------------------------

    def __setup_ui(self, acc: Account) -> None:
        # Labels
        self.__username = HyphenatedLabel(acc.get_username())
        self.__username.setProperty(WidgetRole.HEADER2, True)

        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.addWidget(self.__username)

        if self.__editable:
            # Pulsanti Modifica-Elimina
            self.__btn_modifica = QPushButton("Modifica")
            self.__btn_modifica.setProperty(WidgetRole.MODIFY_BUTTON, True)

            self.__btn_elimina = QPushButton("Elimina")
            self.__btn_elimina.setProperty(WidgetRole.DESTRUCTIVE_BUTTON, True)

            self.__pulsanti = QWidget()
            layout_pulsanti = QHBoxLayout(self.__pulsanti)
            layout_pulsanti.setContentsMargins(1, 1, 1, 1)
            layout_pulsanti.addWidget(self.__btn_modifica)
            layout_pulsanti.addWidget(self.__btn_elimina)

            # Pannello di eliminazione
            domanda = QLabel("<b>Sicuro di eliminare?</b>")
            domanda.setProperty(WidgetRole.HEADER3, True)
            domanda.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)

            self.__btn_si = QPushButton("Sì")
            self.__btn_si.setProperty(WidgetRole.DESTRUCTIVE_BUTTON, True)

            self.__btn_no = QPushButton("No")
            self.__btn_no.setProperty(WidgetRole.DEFAULT_BUTTON, True)

            self.__conferma_elimina = QWidget()
            layout_conferma = QHBoxLayout(self.__conferma_elimina)
            layout_conferma.setContentsMargins(1, 1, 1, 1)
            layout_conferma.addWidget(domanda)
            layout_conferma.addWidget(self.__btn_si)
            layout_conferma.addWidget(self.__btn_no)
            self.__conferma_elimina.hide()

            layout.addWidget(self.__pulsanti)
            layout.addWidget(self.__conferma_elimina)

    def __connect_signals(self, acc: Account) -> None:
        self.__id = acc.get_id()

        if self.__editable:
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
        """Mostra una richiesta di conferma per eliminare il genere."""
        self.__username.hide()
        self.__pulsanti.hide()
        self.__conferma_elimina.show()

    def annulla_elimina(self) -> None:
        """Annulla l'elimina, nascondendo la richiesta di conferma."""
        self.__conferma_elimina.hide()
        self.__username.show()
        self.__pulsanti.show()
