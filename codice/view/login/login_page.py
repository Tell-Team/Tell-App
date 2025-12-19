from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal


class LoginPage(QWidget):
    """
    View della prima pagina dell'app.

    Segnali:
    - loginAsCliente(): emesso quando si clicca il pulsante Cliente;
    - loginAsBiglietteria(): emesso quando si clicca il pulsante Biglietteria;
    - loginAsAdmin(): emesso quando si clicca il pulsante Amministratore;
    """

    loginAsCliente = pyqtSignal()
    loginAsBiglietteria = pyqtSignal()
    loginAsAdmin = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

        self._setup_ui()
        self._connect_signals()

    # ------------------------- SETUP INIT -------------------------

    def _setup_ui(self) -> None:
        # Header
        self.header = QLabel("Login")
        self.header.setObjectName("Header1")
        self.header.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Subheader
        self.subheader = QLabel("Scegliere il tipo di account:")
        self.subheader.setObjectName("Paragraph")
        self.subheader.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Pulsanti
        self._btn_cliente = QPushButton("Cliente")
        self._btn_cliente.setObjectName("BlueButton")

        self._btn_biglietteria = QPushButton("Biglietteria")
        self._btn_biglietteria.setObjectName("BlueButton")

        self._btn_admin = QPushButton("Amministratore")
        self._btn_admin.setObjectName("BlueButton")

        self.pulsanti_utente = QWidget()
        layout_pulsanti_utente = QVBoxLayout(self.pulsanti_utente)
        layout_pulsanti_utente.addWidget(self._btn_cliente)
        layout_pulsanti_utente.addWidget(self._btn_biglietteria)
        layout_pulsanti_utente.addWidget(self._btn_admin)

        # Layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        main_layout.addWidget(self.header)
        main_layout.addWidget(self.subheader)
        main_layout.addWidget(self.pulsanti_utente)
        main_layout.addStretch()

    def _connect_signals(self) -> None:
        self._btn_cliente.clicked.connect(  # type:ignore
            self.loginAsCliente.emit
        )

        self._btn_biglietteria.clicked.connect(  # type:ignore
            self.loginAsBiglietteria.emit
        )

        self._btn_admin.clicked.connect(  # type:ignore
            self.loginAsAdmin.emit
        )
