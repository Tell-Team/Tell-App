from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal


class LoginPage(QWidget):
    """View della prima pagina dell'app.

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
        # Content
        header = QLabel("Login")
        header.setObjectName("header1")
        header.setAlignment(Qt.AlignmentFlag.AlignLeft)

        subheader = QLabel("Scegliere il tipo di account:")
        subheader.setObjectName("paragraph")
        subheader.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Pulsanti
        self.__btn_cliente = QPushButton("Cliente")
        self.__btn_cliente.setObjectName("blueButton")

        self.__btn_biglietteria = QPushButton("Biglietteria")
        self.__btn_biglietteria.setObjectName("blueButton")

        self.__btn_admin = QPushButton("Amministratore")
        self.__btn_admin.setObjectName("blueButton")

        self.pulsanti_utente = QWidget()
        layout_pulsanti_utente = QVBoxLayout(self.pulsanti_utente)
        layout_pulsanti_utente.addWidget(self.__btn_cliente)
        layout_pulsanti_utente.addWidget(self.__btn_biglietteria)
        layout_pulsanti_utente.addWidget(self.__btn_admin)

        # Layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        main_layout.addWidget(header)
        main_layout.addWidget(subheader)
        main_layout.addWidget(self.pulsanti_utente)
        main_layout.addStretch()

    def _connect_signals(self) -> None:
        self.__btn_cliente.clicked.connect(  # type:ignore
            self.loginAsCliente.emit
        )

        self.__btn_biglietteria.clicked.connect(  # type:ignore
            self.loginAsBiglietteria.emit
        )

        self.__btn_admin.clicked.connect(  # type:ignore
            self.loginAsAdmin.emit
        )
