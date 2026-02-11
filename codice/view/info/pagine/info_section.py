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
from view.utils.custom_button import DefaultButton, RicercaButton

from view.style.ui_style import WidgetRole, WidgetColor


class InfoSectionView(AbstractSectionView):
    """Sezione Info dell'app.

    Contiene le informazioni sulle `Opera` e `Genere` memorizzati.

    Segnali
    ---
    - `nuovaOperaRequest()`: emesso quando si clicca il pulsante Nuova opera;
    - `nuovoGenereRequest()`: emesso quando si clicca il pulsante Nuovo genere;
    - `displayOpereRequest(ListLayout)`: emesso per mostrare a schermo la lista opere;
    - `displayGeneriRequest(ListLayout)`: emesso per mostrare a schermo la lista generi.
    """

    nuovaOperaRequest = pyqtSignal()
    nuovoGenereRequest = pyqtSignal()
    displayOpereRequest = pyqtSignal(ListLayout)
    displayGeneriRequest = pyqtSignal(ListLayout)

    def __init__(self, user_session: UserSession):
        self.is_biglietteria = user_session.ha_permessi_biglietteria()
        self.is_admin = user_session.ha_permessi_admin()

        super().__init__()

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        if not self.is_biglietteria:
            self._btn_sezione_spettacoli.hide()
            self._btn_sezione_prenotazioni.hide()
        if not self.is_admin:
            self._btn_sezione_teatro.hide()
            self._btn_sezione_account.hide()

        # Opere
        header_opere = QLabel("Opere")
        header_opere.setProperty(WidgetRole.HEADER1, True)
        header_opere.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.filtro_ricerca: str = ""

        self.ricerca_bar = QLineEdit()
        self.ricerca_bar.setPlaceholderText("Inserire nome...")
        self.ricerca_bar.setClearButtonEnabled(True)
        self.ricerca_bar.setProperty(WidgetRole.SEARCH_BAR, True)

        self.__btn_ricerca = RicercaButton()
        self.__btn_ricerca.setFixedHeight(self.ricerca_bar.sizeHint().height())

        widget_ricerca = QWidget()
        layout_ricerca = QHBoxLayout(widget_ricerca)
        layout_ricerca.setSpacing(0)
        layout_ricerca.setContentsMargins(0, 0, 0, 0)
        layout_ricerca.addWidget(self.ricerca_bar)
        layout_ricerca.addWidget(self.__btn_ricerca)

        widget_header_opere = QWidget()
        layout_header_opere = QHBoxLayout(widget_header_opere)
        layout_header_opere.setContentsMargins(0, 0, 0, 0)
        layout_header_opere.addWidget(header_opere)
        if self.is_admin:
            self._btn_nuova_opera = DefaultButton("Nuova opera")
            layout_header_opere.addWidget(self._btn_nuova_opera)
        layout_header_opere.addWidget(widget_ricerca)

        # Non è necessario salvare questa label come attributo perché il suo funzionamento
        #   viene gestito dal ListLayout a cui viene collegata.
        label_lista_opere_vuota = EmptyStateLabel("Non vi sono opere disponibili.")
        label_lista_opere_vuota.setProperty(WidgetRole.BODY_TEXT, True)
        label_lista_opere_vuota.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)

        widget_lista_opere = QWidget()
        self.layout_lista_opere = ListLayout(
            widget_lista_opere, label_lista_opere_vuota
        )

        container_opere = QWidget()
        layout_opere = QVBoxLayout(container_opere)
        layout_opere.addWidget(widget_header_opere)
        layout_opere.addWidget(widget_lista_opere)

        # Generi
        header_generi = QLabel("Generi")
        header_generi.setProperty(WidgetRole.HEADER1, True)
        header_generi.setAlignment(Qt.AlignmentFlag.AlignLeft)

        widget_header_generi = QWidget()
        layout_header_generi = QHBoxLayout(widget_header_generi)
        layout_header_generi.setContentsMargins(0, 0, 0, 0)
        layout_header_generi.addWidget(header_generi)
        if self.is_admin:
            self._btn_nuovo_genere = DefaultButton("Nuovo genere")
            layout_header_generi.addWidget(self._btn_nuovo_genere)
        layout_header_generi.addStretch()

        label_lista_generi_vuota = EmptyStateLabel("Non vi sono generi disponibili.")
        label_lista_generi_vuota.setProperty(WidgetRole.BODY_TEXT, True)
        label_lista_generi_vuota.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)

        widget_lista_generi = QWidget()
        self.layout_lista_generi = ListLayout(
            widget_lista_generi, label_lista_generi_vuota
        )

        container_generi = QWidget()
        layout_generi = QVBoxLayout(container_generi)
        layout_generi.addWidget(widget_header_generi)
        layout_generi.addWidget(widget_lista_generi)

        # # Teatro
        # header_teatro = QLabel("Teatro")
        # header_teatro.setProperty(WidgetRole.HEADER1, True)
        # header_teatro.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # teatro_nome = QLabel("Vitrifrigo Arena")
        # teatro_nome.setProperty(WidgetRole.HEADER2, True)

        # teatro_desc = HyphenatedLabel(
        #     "Inaugurato nel 1996\nVia R. Ripa, 1\nLa Vitrifrigo Arena è un'ampio "
        #     + "palazzetto che ospita numerosi eventi sportivi e musicali di "
        #     + "rilevanza mondiale. In occasione dello Rossini Opera Festival, "
        #     + "viene allestita una struttura in legno al suo interno per ricreare "
        #     + "l'esperienza acustica di un teatro tradizionale."
        # )
        # teatro_desc.setProperty(WidgetRole.BODY_TEXT, True)
        # teatro_desc.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)

        # info_teatro = QWidget()
        # info_teatro.setProperty(WidgetRole.ITEM_CARD, True)
        # layout_info_teatro = QVBoxLayout(info_teatro)
        # layout_info_teatro.addWidget(teatro_nome)
        # layout_info_teatro.addWidget(teatro_desc)

        # container_teatro = QWidget()
        # layout_teatro = QVBoxLayout(container_teatro)
        # layout_teatro.addWidget(header_teatro)
        # layout_teatro.addWidget(info_teatro)

        # Scroll layout
        self.scroll_layout.addWidget(container_opere)
        self.scroll_layout.addWidget(container_generi)
        # self.scroll_layout.addWidget(container_teatro)
        self.scroll_layout.addStretch()

    @override
    def _connect_signals(self) -> None:
        super()._connect_signals()

        self._btn_sezione_info.setEnabled(False)

        if self.is_admin:
            self._btn_nuova_opera.clicked.connect(  # type:ignore
                self.nuovaOperaRequest.emit
            )
            self._btn_nuovo_genere.clicked.connect(  # type:ignore
                self.nuovoGenereRequest.emit
            )

        self.__btn_ricerca.clicked.connect(  # type:ignore
            lambda: self.__filtra_opere(self.ricerca_bar.text())
        )

        self.displayOpereRequest.emit(self.layout_lista_opere)

        self.displayGeneriRequest.emit(self.layout_lista_generi)

    # ------------------------- METODI DI VIEW -------------------------

    def __filtra_opere(self, filtro: str) -> None:
        self.filtro_ricerca = filtro
        self.aggiorna_pagina()

    @override
    def aggiorna_pagina(self) -> None:
        super().aggiorna_pagina()

        self.layout_lista_opere.svuota_layout()
        self.displayOpereRequest.emit(self.layout_lista_opere)

        self.layout_lista_generi.svuota_layout()
        self.displayGeneriRequest.emit(self.layout_lista_generi)
