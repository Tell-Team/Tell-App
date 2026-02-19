from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from typing import override

from core.view import AbstractSectionView

from controller.login.user_session import UserSession

from view.utils.list_widgets import ListLayout, EmptyStateLabel
from view.utils.custom_button import RicercaButton

from view.style.ui_style import WidgetRole, WidgetColor


class PrenotazioniSection(AbstractSectionView):
    """Sezione Prenotazioni dell'app.

    Contiene le informazioni su tutti i `Prenotazione` memorizzati.

    Segnali
    ---
    - `displayPrenotazioniRequest(ListLayout)`: emesso per mostrare a schermo la lista
    prenotazioni.
    """

    displayPrenotazioniRequest = pyqtSignal(ListLayout)

    def __init__(self, user_session: UserSession):
        self.is_admin = user_session.ha_permessi_admin()

        super().__init__()

    # ------------------------- SETUP INIT -------------------------

    def _setup_ui(self):
        super()._setup_ui()

        if not self.is_admin:
            self._btn_sezione_teatro.hide()
            self._btn_sezione_account.hide()

        # Prenotazioni
        header_prenotazioni = QLabel("Prenotazioni")
        header_prenotazioni.setProperty(WidgetRole.Label.HEADER1, True)
        header_prenotazioni.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.filtro_ricerca: str = ""

        self.ricerca_bar = QLineEdit()
        self.ricerca_bar.setPlaceholderText("Inserire nominativo...")
        self.ricerca_bar.setClearButtonEnabled(True)
        self.ricerca_bar.setProperty(WidgetRole.LineEdit.SEARCH_BAR, True)

        self.__btn_ricerca = RicercaButton()
        self.__btn_ricerca.setFixedHeight(self.ricerca_bar.sizeHint().height())

        widget_ricerca = QWidget()
        layout_ricerca = QHBoxLayout(widget_ricerca)
        layout_ricerca.setSpacing(0)
        layout_ricerca.setContentsMargins(0, 0, 0, 0)
        layout_ricerca.addWidget(self.ricerca_bar)
        layout_ricerca.addWidget(self.__btn_ricerca)

        widget_header_prenotazioni = QWidget()
        layout_header_prenotazioni = QHBoxLayout(widget_header_prenotazioni)
        layout_header_prenotazioni.setContentsMargins(0, 0, 0, 0)
        layout_header_prenotazioni.addWidget(header_prenotazioni)
        # self.__btn_nuovo_spettacolo = DefaultButton("Nuovo spettacolo")
        # layout_header_prenotazioni.addWidget(self.__btn_nuovo_spettacolo)
        layout_header_prenotazioni.addWidget(widget_ricerca)

        label_lista_prenotazioni_vuota = EmptyStateLabel(
            "Non vi sono prenotazioni registrate."
        )
        label_lista_prenotazioni_vuota.setProperty(WidgetRole.Label.BODY_TEXT, True)
        label_lista_prenotazioni_vuota.setProperty(
            WidgetColor.Label.SECONDARY_COLOR, True
        )

        widget_lista_prenotazioni = QWidget()
        self.layout_lista_prenotazioni = ListLayout(
            widget_lista_prenotazioni, label_lista_prenotazioni_vuota
        )

        container_prenotazioni = QWidget()
        layout_prenotazioni = QVBoxLayout(container_prenotazioni)
        layout_prenotazioni.addWidget(widget_header_prenotazioni)
        layout_prenotazioni.addWidget(widget_lista_prenotazioni)

        # Scroll layout
        self.scroll_layout.addWidget(container_prenotazioni)
        self.scroll_layout.addStretch()

    @override
    def _connect_signals(self) -> None:
        super()._connect_signals()

        self._btn_sezione_prenotazioni.setEnabled(False)

        self.__btn_ricerca.clicked.connect(  # type:ignore
            lambda: self.__filtra_prenotazioni(self.ricerca_bar.text())
        )

        self.displayPrenotazioniRequest.emit(self.layout_lista_prenotazioni)

    # ------------------------- METODI DI VIEW -------------------------

    def __filtra_prenotazioni(self, filtro: str) -> None:
        self.filtro_ricerca = filtro
        self.aggiorna_pagina()

    @override
    def aggiorna_pagina(self) -> None:
        super().aggiorna_pagina()

        self.layout_lista_prenotazioni.svuota_layout()
        self.displayPrenotazioniRequest.emit(self.layout_lista_prenotazioni)
