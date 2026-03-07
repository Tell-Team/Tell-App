from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import override

from core.view import AbstractSectionView

from controller.login.user_session import UserSession

from view.utils.list_widgets import ListLayout, EmptyStateLabel
from view.utils.custom_button import RicercaButton

from view.style.ui_style import WidgetRole, WidgetColor


class AcquistoSection(AbstractSectionView):
    """Sezione Acquisto dell'app.

    Contiene le informazioni su tutti gli `Spettacolo` memorizzati con almeno un `Evento`
    non scaduto (detto "evento corrente").

    Segnali
    ---
    - `displaySpettacoliRequest(ListLayout)`: emesso per mostrare a schermo la lista spettacoli,
    tale che tutti gli `Spettacolo` ottenuti hanno almeno un evento corrente associato.
    """

    displaySpettacoliRequest = pyqtSignal(ListLayout)

    def __init__(self, user_session: UserSession):
        self.is_biglietteria = user_session.ha_permessi_biglietteria()
        self.is_admin = user_session.ha_permessi_admin()

        super().__init__()

    # ------------------------- SETUP INIT -------------------------

    def _setup_ui(self):
        super()._setup_ui()

        if not self.is_biglietteria:
            self._btn_sezione_spettacoli.hide()
            self._btn_sezione_prenotazioni.hide()
        if not self.is_admin:
            self._btn_sezione_teatro.hide()
            self._btn_sezione_account.hide()

        # Acquisto
        header_spettacoli = QLabel("Acquisto")
        header_spettacoli.setProperty(WidgetRole.Label.HEADER1, True)
        header_spettacoli.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.filtro_ricerca: str = ""

        self.ricerca_bar = QLineEdit()
        self.ricerca_bar.setPlaceholderText("Inserire titolo")
        self.ricerca_bar.setFixedWidth(201)
        self.ricerca_bar.setClearButtonEnabled(True)
        self.ricerca_bar.setProperty(WidgetRole.LineEdit.SEARCH_BAR, True)

        self.__btn_ricerca = RicercaButton()
        self.__btn_ricerca.setFixedWidth(40)
        self.__btn_ricerca.setFixedHeight(self.ricerca_bar.sizeHint().height())

        widget_ricerca = QWidget()
        layout_ricerca = QHBoxLayout(widget_ricerca)
        layout_ricerca.setSpacing(0)
        layout_ricerca.setContentsMargins(0, 0, 0, 0)
        layout_ricerca.addStretch()
        layout_ricerca.addWidget(self.ricerca_bar)
        layout_ricerca.addWidget(self.__btn_ricerca)

        widget_header_spettacoli = QWidget()
        layout_header_spettacoli = QHBoxLayout(widget_header_spettacoli)
        layout_header_spettacoli.setContentsMargins(0, 0, 0, 0)
        layout_header_spettacoli.addWidget(header_spettacoli)
        layout_header_spettacoli.addWidget(widget_ricerca)

        label_lista_spettacoli_vuota = EmptyStateLabel(
            "Non vi sono spettacoli disponibili."
        )
        label_lista_spettacoli_vuota.setProperty(WidgetRole.Label.BODY_TEXT, True)
        label_lista_spettacoli_vuota.setProperty(
            WidgetColor.Label.SECONDARY_COLOR, True
        )

        widget_lista_spettacoli = QWidget()
        self.layout_lista_spettacoli = ListLayout(
            widget_lista_spettacoli, label_lista_spettacoli_vuota
        )

        container_spettacoli = QWidget()
        layout_spettacoli = QVBoxLayout(container_spettacoli)
        layout_spettacoli.addWidget(widget_header_spettacoli)
        layout_spettacoli.addWidget(widget_lista_spettacoli)

        # Scroll layout
        self.scroll_layout.addWidget(container_spettacoli)
        self.scroll_layout.addStretch()

    @override
    def _connect_signals(self) -> None:
        super()._connect_signals()

        self._btn_sezione_acquisto.setEnabled(False)

        self.__btn_ricerca.clicked.connect(  # type:ignore
            lambda: self.__filtra_spettacoli(self.ricerca_bar.text())
        )

        self.displaySpettacoliRequest.emit(self.layout_lista_spettacoli)

    # ------------------------- METODI DI VIEW -------------------------

    def __filtra_spettacoli(self, filtro: str) -> None:
        self.filtro_ricerca = filtro
        self.aggiorna_pagina()

    @override
    def aggiorna_pagina(self) -> None:
        super().aggiorna_pagina()

        self.layout_lista_spettacoli.svuota_layout()
        self.displaySpettacoliRequest.emit(self.layout_lista_spettacoli)
