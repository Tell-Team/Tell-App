from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from typing import override

from core.view import AbstractSectionView

from view.utils.list_widgets import ListLayout, EmptyStateLabel
from view.style import QssStyle


class AccountSectionView(AbstractSectionView):
    """Sezione Account dell'app.

    Contiene le informazioni di tutti gli `Account` memorizzati. Non permette di modificare
    l'`Account` della sessione utente corrente.

    Segnali:
    - `logoutRequest()`: emesso quando si clicca il pulsante Logout;
    - `goToSpettacoli()`: emesso quando si clicca il pulsante Spettacoli;
    - `goToInfo()`: emesso quando si clicca il pulsante Info;
    - `nuovoAdminReques()`: emesso quando si clicca il pulsante Nuovo Amministratore;
    - `nuovoBiglietteriaRequest()`: emesso quando si clicca il pulsante Nuovo Biglietteria;
    - `displayAdminRequest(QVBoxLayout)`: emesso per caricare la lista di account
    Amministratore nella sezione Account;
    - `displayBiglietteriaRequest(QVBoxLayout)`: emesso per caricare la lista di
    account Biglietteria nella sezione Account.
    """

    nuovoAdminRequest = pyqtSignal()
    nuovoBiglietteriaRequest = pyqtSignal()
    displayAdminRequest = pyqtSignal(QVBoxLayout)
    displayBiglietteriaRequest = pyqtSignal(QVBoxLayout)

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        # Account Header
        header_account = QLabel("Account")
        header_account.setProperty(QssStyle.HEADER1, True)
        header_account.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # - Questo blocco posiziona il header Account della pagina all'altura degli header
        #   delle altre sezioni (Opere e Spettacoli). È una soluzione temporanea mentre non
        #   ci sia model per gli Account per testare la view.
        widget_header_account = QWidget()
        layout_header_account = QHBoxLayout(widget_header_account)
        layout_header_account.setContentsMargins(0, 0, 0, 0)
        layout_header_account.addWidget(header_account)

        top_header = QWidget()
        top_layout = QVBoxLayout(top_header)
        top_layout.addWidget(widget_header_account)
        # - END

        # Amministratore
        header_admin = QLabel("Amministratore")
        header_admin.setProperty(QssStyle.HEADER2, True)
        header_admin.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self._btn_nuovo_admin = QPushButton("Nuovo Amministratore")
        self._btn_nuovo_admin.setProperty(QssStyle.WHITE_BUTTON, True)

        widget_header_admin = QWidget()
        layout_header_admin = QHBoxLayout(widget_header_admin)
        layout_header_admin.addWidget(header_admin)
        layout_header_admin.addWidget(self._btn_nuovo_admin)
        layout_header_admin.addStretch()

        # Non è necessario, perché in prattica non vendrà mai visualizzato. Comunque
        #   lo lascio, in caso sia utile.
        label_lista_admin_vuota = EmptyStateLabel(
            "Non vi sono account Amministratore registrati."
        )
        label_lista_admin_vuota.setProperty(QssStyle.SECONDARY_TEXT, True)

        # Si usa 'admin' nei nomi delle variabili e 'amministratore' nei testi della UI.
        widget_lista_admin = QWidget()
        self.layout_lista_admin = ListLayout(
            widget_lista_admin, label_lista_admin_vuota
        )
        container_admin = QWidget()
        layout_admin = QVBoxLayout(container_admin)
        layout_admin.addWidget(widget_header_admin)
        layout_admin.addWidget(widget_lista_admin)

        # Biglietteria
        header_biglietteria = QLabel("Biglietteria")
        header_biglietteria.setProperty(QssStyle.HEADER2, True)
        header_biglietteria.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self._btn_nuovo_biglietteria = QPushButton("Nuovo Biglietteria")
        self._btn_nuovo_biglietteria.setProperty(QssStyle.WHITE_BUTTON, True)

        widget_header_biglietteria = QWidget()
        layout_header_biglietteria = QHBoxLayout(widget_header_biglietteria)
        layout_header_biglietteria.addWidget(header_biglietteria)
        layout_header_biglietteria.addWidget(self._btn_nuovo_biglietteria)
        layout_header_biglietteria.addStretch()

        label_lista_biglietteria_vuota = EmptyStateLabel(
            "Non vi sono account Biglietteria registrati."
        )
        label_lista_biglietteria_vuota.setProperty(QssStyle.SECONDARY_TEXT, True)

        # Viene usato 'biglietteria' in singolare per le variabili perché è il tipo di account.
        #   Quindi, è un nome proprio.
        widget_lista_biglietteria = QWidget()
        self.layout_lista_biglietteria = ListLayout(
            widget_lista_biglietteria, label_lista_biglietteria_vuota
        )

        container_biglietteria = QWidget()
        layout_biglietterie = QVBoxLayout(container_biglietteria)
        layout_biglietterie.addWidget(widget_header_biglietteria)
        layout_biglietterie.addWidget(widget_lista_biglietteria)

        # Scroll layout
        self.scroll_layout.addWidget(top_header)  # - DA CORRIGERE
        self.scroll_layout.addWidget(container_admin)
        self.scroll_layout.addWidget(container_biglietteria)
        self.scroll_layout.addStretch()

    @override
    def _connect_signals(self) -> None:
        super()._connect_signals()

        self._btn_sezione_account.setEnabled(False)

        self._btn_nuovo_admin.clicked.connect(  # type:ignore
            self.nuovoAdminRequest.emit
        )

        self._btn_nuovo_biglietteria.clicked.connect(  # type:ignore
            self.nuovoBiglietteriaRequest.emit
        )

        self.displayAdminRequest.emit(self.layout_lista_admin)

        self.displayBiglietteriaRequest.emit(self.layout_lista_biglietteria)

    # ------------------------- METODI DI VIEW -------------------------

    @override
    def aggiorna_pagina(self) -> None:
        self.layout_lista_admin.svuota_layout()
        self.displayAdminRequest.emit(self.layout_lista_admin)

        self.layout_lista_biglietteria.svuota_layout()
        self.displayBiglietteriaRequest.emit(self.layout_lista_biglietteria)

        vertical_scroll = self._scroll_area.verticalScrollBar()
        if not vertical_scroll:
            return
        vertical_scroll.setValue(0)
