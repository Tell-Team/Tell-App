from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import override

from core.view import AbstractSectionView

from view.utils.list_widgets import ListLayout, EmptyStateLabel
from view.style.ui_style import WidgetRole, WidgetColor


class TeatroSectionView(AbstractSectionView):
    """Sezione Teatro dell'app.

    Contiene le informazioni sulle `Sezione` e `Posto` memorizzati.


    Segnali
    ---
    - `nuovaSezioneRequest()`: emesso quando si clicca il pulsante Nuova sezione;
    - `displaySezioniRequest(QVBoxLayout)`: emesso per mostrare a schermo la lista sezioni.
    """

    nuovaSezioneRequest = pyqtSignal()
    # nuovoPostoRequest = pyqtSignal()
    displaySezioniRequest = pyqtSignal(QVBoxLayout)
    # displayPostiRequest = pyqtSignal(QVBoxLayout)

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        # Sezioni
        header_sezioni = QLabel("Sezioni")
        header_sezioni.setProperty(WidgetRole.HEADER1, True)
        header_sezioni.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self._btn_nuova_sezione = QPushButton("Nuova sezione")
        self._btn_nuova_sezione.setProperty(WidgetRole.DEFAULT_BUTTON, True)

        widget_header_sezioni = QWidget()
        layout_header_sezioni = QHBoxLayout(widget_header_sezioni)
        layout_header_sezioni.setContentsMargins(0, 0, 0, 0)
        layout_header_sezioni.addWidget(header_sezioni)
        layout_header_sezioni.addWidget(self._btn_nuova_sezione)
        layout_header_sezioni.addStretch()

        label_lista_sezioni_vuota = EmptyStateLabel("Non vi sono sezioni disponibili.")
        label_lista_sezioni_vuota.setProperty(WidgetRole.BODY_TEXT, True)
        label_lista_sezioni_vuota.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)

        widget_lista_sezioni = QWidget()
        self.layout_lista_sezioni = ListLayout(
            widget_lista_sezioni, label_lista_sezioni_vuota
        )

        container_sezioni = QWidget()
        layout_sezioni = QVBoxLayout(container_sezioni)
        layout_sezioni.addWidget(widget_header_sezioni)
        layout_sezioni.addWidget(widget_lista_sezioni)

        # # Posti
        # header_posti = QLabel("Posti")
        # header_posti.setProperty(WidgetRole.HEADER1, True)
        # header_posti.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # self._btn_nuovo_posto = QPushButton("Nuovo posto")
        # self._btn_nuovo_posto.setProperty(WidgetRole.DEFAULT_BUTTON, True)

        # widget_header_posti = QWidget()
        # layout_header_posti = QHBoxLayout(widget_header_posti)
        # layout_header_posti.setContentsMargins(0, 0, 0, 0)
        # layout_header_posti.addWidget(header_posti)
        # layout_header_posti.addWidget(self._btn_nuovo_posto)
        # layout_header_posti.addStretch()

        # label_lista_posti_vuota = EmptyStateLabel("Non vi sono posti disponibili.")
        # label_lista_posti_vuota.setProperty(WidgetRole.BODY_TEXT, True)
        # label_lista_posti_vuota.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)

        # widget_lista_posti = QWidget()
        # self.layout_lista_posti = ListLayout(
        #     widget_lista_posti, label_lista_posti_vuota
        # )

        # container_posti = QWidget()
        # layout_posti = QVBoxLayout(container_posti)
        # layout_posti.addWidget(widget_header_posti)
        # layout_posti.addWidget(widget_lista_posti)

        # Scroll layout
        self.scroll_layout.addWidget(container_sezioni)
        # self.scroll_layout.addWidget(container_posti)
        self.scroll_layout.addStretch()

    @override
    def _connect_signals(self) -> None:
        super()._connect_signals()

        self._btn_sezione_teatro.setEnabled(False)

        self._btn_nuova_sezione.clicked.connect(  # type:ignore
            self.nuovaSezioneRequest.emit
        )
        # self._btn_nuovo_posto.clicked.connect(  # type:ignore
        #     self.nuovoPostoRequest.emit
        # )

        self.displaySezioniRequest.emit(self.layout_lista_sezioni)

        # self.displayPostiRequest.emit(self.layout_lista_posti)

    # ------------------------- METODI DI VIEW -------------------------

    @override
    def aggiorna_pagina(self) -> None:
        self.layout_lista_sezioni.svuota_layout()
        self.displaySezioniRequest.emit(self.layout_lista_sezioni)

        # self.layout_lista_posti.svuota_layout()
        # self.displayPostiRequest.emit(self.layout_lista_posti)

        if vertical_scroll := self._scroll_area.verticalScrollBar():
            vertical_scroll.setValue(0)
