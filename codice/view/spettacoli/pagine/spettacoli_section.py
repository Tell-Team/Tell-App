from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import override

from core.view import AbstractSectionView

from view.utils.list_widgets import ListLayout, EmptyStateLabel
from view.style import QssStyle


class SpettacoliSectionView(AbstractSectionView):
    """View della sezione Spettacoli dell'app.

    Segnali:
    - logoutRequest(): emesso quando si clicca il pulsante Logout;
    - goToInfo(): emesso quando si clicca il pulsante Info;
    - goToAccount(): emesso quando si clicca il pulsante Account;
    - nuovoSpettacoloRequest(): emesso quando si clicca il pulsante Nuovo spettacolo;
    - displaySpettacoliRequest(QVBoxLayout): emesso per caricare la lista degli spettacoli
    nella sezione Spettacoli.
    """

    nuovoSpettacoloRequest = pyqtSignal()
    displaySpettacoliRequest = pyqtSignal(QVBoxLayout)

    # ------------------------- SETUP INIT -------------------------

    def _setup_ui(self):
        super()._setup_ui()

        # Spettacoli
        header_spettacoli = QLabel("Spettacoli")
        header_spettacoli.setProperty(QssStyle.HEADER1, True)
        header_spettacoli.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.__btn_nuovo_spettacolo = QPushButton("Nuovo spettacolo")
        self.__btn_nuovo_spettacolo.setProperty(QssStyle.WHITE_BUTTON, True)

        self.filtro_ricerca: str = ""

        self.ricerca_bar = QLineEdit()
        self.ricerca_bar.setPlaceholderText("Inserire titolo...")
        self.ricerca_bar.setClearButtonEnabled(True)
        self.ricerca_bar.setProperty(QssStyle.SEARCH_BAR, True)

        self._btn_ricerca = QPushButton()
        self._btn_ricerca.setProperty(QssStyle.SEARCH_BUTTON, True)
        self._btn_ricerca.setProperty(QssStyle.BLUE_BUTTON, True)
        self._btn_ricerca.setFixedHeight(self.ricerca_bar.sizeHint().height())

        widget_ricerca = QWidget()
        layout_ricerca = QHBoxLayout(widget_ricerca)
        layout_ricerca.setSpacing(0)
        layout_ricerca.setContentsMargins(0, 0, 0, 0)
        layout_ricerca.addWidget(self.ricerca_bar)
        layout_ricerca.addWidget(self._btn_ricerca)

        widget_header_spettacoli = QWidget()
        layout_header_spettacoli = QHBoxLayout(widget_header_spettacoli)
        layout_header_spettacoli.setContentsMargins(0, 0, 0, 0)
        layout_header_spettacoli.addWidget(header_spettacoli)
        layout_header_spettacoli.addWidget(self.__btn_nuovo_spettacolo)
        layout_header_spettacoli.addWidget(widget_ricerca)

        label_lista_spettacoli_vuota = EmptyStateLabel(
            "Non vi sono spettacoli registrati."
        )
        label_lista_spettacoli_vuota.setProperty(QssStyle.SECONDARY_TEXT, True)

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

        self._btn_sezione_spettacoli.setEnabled(False)

        self.__btn_nuovo_spettacolo.clicked.connect(  # type:ignore
            self.nuovoSpettacoloRequest.emit
        )

        self._btn_ricerca.clicked.connect(  # type:ignore
            lambda: self.__filtra_spettacoli(self.ricerca_bar.text())
        )

        self.displaySpettacoliRequest.emit(self.layout_lista_spettacoli)

    # ------------------------- METODI DI VIEW -------------------------

    def __filtra_spettacoli(self, filtro: str) -> None:
        self.filtro_ricerca = filtro
        self.aggiorna_pagina()

    @override
    def aggiorna_pagina(self) -> None:
        self.layout_lista_spettacoli.svuota_layout()
        self.displaySpettacoliRequest.emit(self.layout_lista_spettacoli)

        vertical_scroll = self._scroll_area.verticalScrollBar()
        if not vertical_scroll:
            return
        vertical_scroll.setValue(0)
