from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import pyqtSignal
from functools import partial

from model.pianificazione.opera import Opera

from view.utils.list_widgets import ItemDisplay
from view.utils.hyphenate_text import HyphenatedLabel
from view.utils.custom_button import ModificaButton, EliminaButton

from view.style.ui_style import WidgetRole, WidgetColor


class OperaDisplay(ItemDisplay):
    """View delle singole opere della Lista Opere.

    Segnali
    ---
    - `visualizzaRequest(int)`: emesso quando si clicca il pulsante Maggior info;
    - `modificaRequest(int)`: emesso quando si clicca il pulsante Modifica;
    - `eliminaConfermata()`: emesso quando si clicca il pulsante Sì.
    """

    visualizzaRequest = pyqtSignal(int)
    modificaRequest = pyqtSignal(int)
    eliminaConfermata = pyqtSignal()

    def __init__(self, o: Opera, editable: bool):
        super().__init__()

        self.__editable = editable

        self.__setup_ui(o)
        self.__connect_signals(o)

    # ------------------------- SETUP INIT -------------------------

    def __setup_ui(self, o: Opera) -> None:
        # Labels
        nome = HyphenatedLabel(o.get_nome())
        nome.setProperty(WidgetRole.HEADER2, True)

        librettista = HyphenatedLabel(f"Librettista: {o.get_librettista()}")
        librettista.setProperty(WidgetRole.BODY_TEXT, True)
        librettista.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)

        compositore = HyphenatedLabel(f"Direttore d'orchestra: {o.get_compositore()}")
        compositore.setProperty(WidgetRole.BODY_TEXT, True)
        compositore.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)

        # Pulsanti
        self.__btn_visualizza = QPushButton("Maggior info")
        self.__btn_visualizza.setProperty(WidgetRole.DEFAULT_BUTTON, True)

        self.__pulsanti = QWidget()
        layout_pulsanti = QHBoxLayout(self.__pulsanti)
        layout_pulsanti.setContentsMargins(1, 1, 1, 1)
        layout_pulsanti.addWidget(self.__btn_visualizza)

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.addWidget(nome)
        layout.addWidget(librettista)
        layout.addWidget(compositore)

        layout.addWidget(self.__pulsanti)

        if self.__editable:
            self.__btn_modifica = ModificaButton("Modifica")

            self.__btn_elimina = EliminaButton("Elimina")

            layout_pulsanti.addWidget(self.__btn_modifica)
            layout_pulsanti.addWidget(self.__btn_elimina)

            # Pannello di eliminazione
            domanda = QLabel("<b>Sicuro di eliminare?</b>")
            domanda.setProperty(WidgetRole.BODY_TEXT, True)
            domanda.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)

            self.__btn_no = QPushButton("No")
            self.__btn_no.setProperty(WidgetRole.DEFAULT_BUTTON, True)

            self.__btn_si = QPushButton("Sì")
            self.__btn_si.setProperty(WidgetRole.DESTRUCTIVE_BUTTON, True)

            self.__conferma_elimina = QWidget()
            layout_conferma = QHBoxLayout(self.__conferma_elimina)
            layout_conferma.setContentsMargins(1, 1, 1, 1)
            layout_conferma.addWidget(domanda)
            layout_conferma.addWidget(self.__btn_no)
            layout_conferma.addWidget(self.__btn_si)
            self.__conferma_elimina.hide()

            layout.addWidget(self.__conferma_elimina)

        layout_pulsanti.addStretch()

    def __connect_signals(self, o: Opera) -> None:
        self.__id = o.get_id()

        self.__btn_visualizza.clicked.connect(  # type:ignore
            partial(self.visualizzaRequest.emit, self.__id)
        )

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
        """Mostra una richiesta di conferma per eliminare l'opera."""
        self.__pulsanti.hide()
        self.__conferma_elimina.show()

    def annulla_elimina(self) -> None:
        """Annulla l'elimina, nascondendo la richiesta di conferma."""
        self.__conferma_elimina.hide()
        self.__pulsanti.show()
