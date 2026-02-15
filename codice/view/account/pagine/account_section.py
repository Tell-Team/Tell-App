from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from typing import override

from controller.login.user_session import UserSession

from core.view import AbstractSectionView

from view.utils.list_widgets import ListLayout, EmptyStateLabel
from view.utils.custom_button import DefaultButton

from view.style.ui_style import WidgetRole, WidgetColor


class AccountSectionView(AbstractSectionView):
    """Sezione Account dell'app.

    Contiene le informazioni di tutti gli `Account` memorizzati. Non permette di modificare
    l'`Account` della sessione utente corrente.

    Segnali
    ---
    - `nuovoAccountRequest()`: emesso quando si clicca il pulsante Nuovo Account;
    - `displayAccountRequest(ListLayout)`: emesso per caricare la lista di account
    nella sezione Account;
    """

    # Si usa 'admin' nei nomi delle variabili e 'amministratore' nei testi della UI.

    # Viene usato 'biglietteria' in singolare per le variabili perché è il tipo di account.
    #   Quindi, è un nome proprio.

    nuovoAccountRequest = pyqtSignal()
    displayAccountRequest = pyqtSignal(ListLayout)

    def __init__(self, user_session: UserSession):
        self.user_session_id = user_session.id

        super().__init__()

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        # Account Header
        header_account = QLabel("Account")
        header_account.setProperty(WidgetRole.Label.HEADER1, True)
        header_account.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self._btn_nuovo_account = DefaultButton("Nuovo Account")

        widget_header_account = QWidget()
        layout_header_account = QHBoxLayout(widget_header_account)
        layout_header_account.setContentsMargins(0, 0, 0, 0)
        layout_header_account.addWidget(header_account)
        layout_header_account.addWidget(self._btn_nuovo_account)
        layout_header_account.addStretch()

        # Non è necessario, perché in prattica non vendrà mai visualizzato. Comunque
        #   lo lascio, in caso sia utile.
        label_lista_account_vuota = EmptyStateLabel("Non vi sono account registrati.")
        label_lista_account_vuota.setProperty(WidgetRole.Label.BODY_TEXT, True)
        label_lista_account_vuota.setProperty(WidgetColor.Label.SECONDARY_COLOR, True)

        widget_lista_account = QWidget()
        self.layout_lista_account = ListLayout(
            widget_lista_account, label_lista_account_vuota
        )
        container_account = QWidget()
        layout_account = QVBoxLayout(container_account)
        layout_account.addWidget(widget_header_account)
        layout_account.addWidget(widget_lista_account)

        # Scroll layout
        self.scroll_layout.addWidget(container_account)
        self.scroll_layout.addStretch()

    @override
    def _connect_signals(self) -> None:
        super()._connect_signals()

        self._btn_sezione_account.setEnabled(False)

        self._btn_nuovo_account.clicked.connect(  # type:ignore
            self.nuovoAccountRequest.emit
        )

        self.displayAccountRequest.emit(self.layout_lista_account)

    # ------------------------- METODI DI VIEW -------------------------

    @override
    def aggiorna_pagina(self) -> None:
        super().aggiorna_pagina()

        self.layout_lista_account.svuota_layout()
        self.displayAccountRequest.emit(self.layout_lista_account)
