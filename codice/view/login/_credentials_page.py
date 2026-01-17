from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt

from view.style import WidgetRole, WidgetColor


class CredentialsPage(QWidget):
    """View per la autenticazione degli account `Biglietteria` e `Amministratore`.

    Permette di inserire un nome utente ed una password.
    """

    def __init__(self):
        super().__init__()

        self._setup_ui()

    # ------------------------- SETUP INIT -------------------------

    def _setup_ui(self) -> None:
        # Top widget
        self.btn_indietro = QPushButton("Indietro")
        self.btn_indietro.setProperty(WidgetRole.DEFAULT_BUTTON, True)

        pagina_header = QWidget()
        layout_header = QHBoxLayout(pagina_header)
        layout_header.addWidget(self.btn_indietro)
        layout_header.addStretch()

        # Content
        label_header = QLabel("Login")
        label_header.setProperty(WidgetRole.HEADER1, True)
        label_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label_username = QLabel("Username")
        label_username.setProperty(WidgetRole.BODY_TEXT, True)
        label_username.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)
        label_username.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        label_password = QLabel("Password")
        label_password.setProperty(WidgetRole.BODY_TEXT, True)
        label_password.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)
        label_password.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        self.btn_login = QPushButton("LOGIN")
        self.btn_login.setProperty(WidgetColor.Button.BLUE_BUTTON, True)
        self.btn_login.setProperty(WidgetRole.MAIN_BUTTON, True)

        pagina_content = QWidget()
        layout_content = QVBoxLayout(pagina_content)
        layout_content.addWidget(label_header)
        layout_content.addWidget(label_username)
        layout_content.addWidget(self.username)
        layout_content.addWidget(label_password)
        layout_content.addWidget(self.password)
        layout_content.addStretch()
        layout_content.addWidget(self.btn_login)

        # Layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        main_layout.addWidget(pagina_header)
        main_layout.addWidget(pagina_content)
        main_layout.addStretch()

    # ------------------------- METODI DI VIEW -------------------------

    def reset_pagina(self) -> None:
        """Reset della pagina allo stato default."""
        self.username.setText("")
        self.password.setText("")
