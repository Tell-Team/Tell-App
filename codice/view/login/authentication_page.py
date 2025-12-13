from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt


class AuthenticationPage(QWidget):
    """
    GUI di autenticazione degli account `Biglietteria` e `Amministratore`.

    Permette di inserire un nome utente ed una password.
    """

    def __init__(self):
        super().__init__()

        self._build_ui()

    def _build_ui(self):
        # Header
        self.header = QLabel("Login")
        self.header.setObjectName("Header1")
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Content
        self.label_username = QLabel("Username")
        self.label_username.setObjectName("Paragraph")
        self.label_username.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.label_password = QLabel("Password")
        self.label_password.setObjectName("Paragraph")
        self.label_password.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.addWidget(self.label_username)
        self.content_layout.addWidget(self.username)
        self.content_layout.addWidget(self.label_password)
        self.content_layout.addWidget(self.password)
        self.content_layout.addStretch()

        #
        #
        #

        # Pulsanti
        self.btn_indietro = QPushButton("Indietro")
        self.btn_indietro.setObjectName("SmallButton")

        self.box_btn_indietro = QWidget()
        self.box_layout = QHBoxLayout(self.box_btn_indietro)
        self.box_layout.addWidget(self.btn_indietro)
        self.box_layout.addStretch()

        self.btn_login = QPushButton("LOGIN")
        self.btn_login.setObjectName("BlueButton")
        # - Questo pulsante non è ancora collegato nel Controller

        #
        #
        #

        # Layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        main_layout.addWidget(self.box_btn_indietro)
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.content)
        main_layout.addWidget(self.btn_login)
        main_layout.addStretch()

    def refresh_page(self):
        self.username.setText("")
        self.password.setText("")
