from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt, pyqtSignal


class AuthenticationPage(QWidget):
    """View per la autenticazione degli account `Biglietteria` e `Amministratore`.

    Permette di inserire un nome utente ed una password.

    Segnali:
    - tornaIndietroRequest(): emesso quando si clicca il pulsante Indietro;
    - authRequest(str, str): emesso quando si clicca il pulsante Login.
    """

    annullaRequest = pyqtSignal()
    authRequest = pyqtSignal(str, str)

    def __init__(self) -> None:
        super().__init__()

        self._setup_ui()
        self._connect_signals()

    # ------------------------- SETUP INIT -------------------------

    def _setup_ui(self) -> None:
        # Top widget
        self.__btn_indietro = QPushButton("Indietro")
        self.__btn_indietro.setObjectName("WhiteButton")

        pagina_header = QWidget()
        layout_header = QHBoxLayout(pagina_header)
        layout_header.addWidget(self.__btn_indietro)
        layout_header.addStretch()

        # Content
        label_header = QLabel("Login")
        label_header.setObjectName("Header1")
        label_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label_username = QLabel("Username")
        label_username.setObjectName("Paragraph")
        label_username.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        label_password = QLabel("Password")
        label_password.setObjectName("Paragraph")
        label_password.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        self.__btn_login = QPushButton("LOGIN")
        self.__btn_login.setObjectName("BlueButton")

        pagina_content = QWidget()
        layout_content = QVBoxLayout(pagina_content)
        layout_content.addWidget(label_header)
        layout_content.addWidget(label_username)
        layout_content.addWidget(self.username)
        layout_content.addWidget(label_password)
        layout_content.addWidget(self.password)
        layout_content.addStretch()
        layout_content.addWidget(self.__btn_login)

        # Layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        main_layout.addWidget(pagina_header)
        main_layout.addWidget(pagina_content)
        main_layout.addStretch()

    def _connect_signals(self):
        self.__btn_indietro.clicked.connect(  # type:ignore
            self.annullaRequest.emit
        )

        self.__btn_login.clicked.connect(  # type:ignore
            lambda: self.authRequest.emit(self.username.text(), self.password.text())
        )

    # ------------------------- METODI DI VIEW -------------------------

    def reset_pagina(self) -> None:
        """Reset della pagina allo stato default."""
        self.username.setText("")
        self.password.setText("")
