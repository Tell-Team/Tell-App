from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import override

from view.abstractView.sectionAbstract import AbstractSectionView


class AccountSectionView(AbstractSectionView):
    """
    View della sezione Account dell'app.

    Segnali:
    - logoutRequest(): emesso quando si clicca il pulsante Logout;
    - goToSpettacoli(): emesso quando si clicca il pulsante Spettacoli;
    - goToInfo(): emesso quando si clicca il pulsante Info;
    - nuovaoAdminReques(): emesso quando si clicca il pulsante Nuovo Amministratore;
    - nuovoBiglietteriaRequest(): emesso quando si clicca il pulsante Nuovo Biglietteria;
    - displayAdminRequest(QVBoxLayout): emesso per caricare la lista di account
    Amministratore nella sezione Account;
    - displayBiglietteriaRequest(QVBoxLayout): emesso per caricare la lista di
    account Biglietteria nella sezione Account.
    """

    logoutRequest = pyqtSignal()
    goToSpettacoli = pyqtSignal()
    goToInfo = pyqtSignal()

    nuovaoAdminRequest = pyqtSignal()
    nuovoBiglietteriaRequest = pyqtSignal()
    displayAdminRequest = pyqtSignal(QVBoxLayout)
    displayBiglietteriaRequest = pyqtSignal(QVBoxLayout)

    def __init__(self) -> None:
        super().__init__()

        self._setup_ui()
        self._connect_signals()

    # ------------------------- SETUP INIT -------------------------

    def _setup_ui(self) -> None:
        # Account Header
        header_account = QLabel("Account")
        header_account.setObjectName("Header1")
        header_account.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Amministratore
        header_admin = QLabel("Amministratore")
        header_admin.setObjectName("Header2")
        header_admin.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self._btn_nuovo_admin = QPushButton("Nuovo Amministratore")
        self._btn_nuovo_admin.setObjectName("SmallButton")

        layout_header_admin = QHBoxLayout()
        layout_header_admin.addWidget(header_admin)
        layout_header_admin.addWidget(self._btn_nuovo_admin)
        layout_header_admin.addStretch()

        # Si usa 'admin' nei nomi delle variabili e 'amministratore' nei testi della UI.
        self.layout_lista_admin = QVBoxLayout()

        # Non è necessario, perché in prattica non vendrà mai visualizzato. Comunque
        #   lo lascio, in caso sia utile.
        self.label_lista_admin_vuota = QLabel(
            "Non vi sono account Amministratore registrati."
        )
        self.label_lista_admin_vuota.setObjectName("SubHeader")
        self.label_lista_admin_vuota.hide()

        container_admin = QWidget()
        layout_admin = QVBoxLayout(container_admin)
        layout_admin.addLayout(layout_header_admin)
        layout_admin.addLayout(self.layout_lista_admin)

        # Biglietteria
        header_biglietteria = QLabel("Biglietteria")
        header_biglietteria.setObjectName("Header2")
        header_biglietteria.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self._btn_nuovo_biglietteria = QPushButton("Nuovo Biglietteria")
        self._btn_nuovo_biglietteria.setObjectName("SmallButton")

        layout_header_biglietteria = QHBoxLayout()
        layout_header_biglietteria.addWidget(header_biglietteria)
        layout_header_biglietteria.addWidget(self._btn_nuovo_biglietteria)
        layout_header_biglietteria.addStretch()

        # Viene usata 'biglietteria' in singolare per le variabili perché è il tipo di account.
        #   Quindi, un nome proprio.
        self.layout_lista_biglietteria = QVBoxLayout()

        self.label_lista_biglietteria_vuota = QLabel(
            "Non vi sono account Biglietteria registrati."
        )
        self.label_lista_biglietteria_vuota.setObjectName("SubHeader")
        self.label_lista_biglietteria_vuota.hide()

        container_biglietteria = QWidget()
        layout_biglietterie = QVBoxLayout(container_biglietteria)
        layout_biglietterie.addLayout(layout_header_biglietteria)
        layout_biglietterie.addLayout(self.layout_lista_biglietteria)

        # Scroll layout
        self.scroll_layout.addWidget(header_account)
        self.scroll_layout.addWidget(container_admin)
        self.scroll_layout.addWidget(container_biglietteria)
        self.scroll_layout.addStretch()

    def _connect_signals(self) -> None:
        self._btn_logout.clicked.connect(  # type:ignore
            self.logoutRequest.emit
        )

        self._btn_sezione_spettacoli.clicked.connect(  # type:ignore
            self.goToSpettacoli.emit
        )

        self._btn_sezione_info.clicked.connect(  # type:ignore
            self.goToInfo.emit
        )

        self._btn_sezione_account.setEnabled(False)

        self._btn_nuovo_admin.clicked.connect(  # type:ignore
            self.nuovaoAdminRequest.emit
        )

        self._btn_nuovo_biglietteria.clicked.connect(  # type:ignore
            self.nuovoBiglietteriaRequest.emit
        )

        self.displayAdminRequest.emit(self.layout_lista_admin)

        self.displayBiglietteriaRequest.emit(self.layout_lista_biglietteria)

    # ------------------------- METODI DI VIEW -------------------------

    @override
    def refresh_page(self) -> None:
        self.clear_layout(self.layout_lista_admin)
        self.layout_lista_admin.addWidget(self.label_lista_admin_vuota)
        self.label_lista_admin_vuota.hide()
        self.displayAdminRequest.emit(self.layout_lista_admin)

        self.clear_layout(self.layout_lista_biglietteria)
        self.layout_lista_biglietteria.addWidget(self.label_lista_biglietteria_vuota)
        self.label_lista_biglietteria_vuota.hide()
        self.displayBiglietteriaRequest.emit(self.layout_lista_biglietteria)
