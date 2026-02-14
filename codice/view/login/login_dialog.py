from PyQt6.QtWidgets import QDialog, QStackedWidget, QVBoxLayout
from PyQt6.QtGui import QShowEvent, QKeyEvent
from PyQt6.QtCore import Qt, pyqtSignal
from functools import partial
from typing import Optional

from ._login_page import LoginPage
from ._credentials_page import CredentialsPage


class LoginDialog(QDialog):
    """Gestice la view della funzione di login dell'app.

    Segnali
    ---
    - `loginAsCliente()`: Emesso quando l'utente ingressa all'app come Cliente;
    - `authRequest(str, str)`: Emesso dopo inserire le credenziali richieste.
    """

    loginAsCliente = pyqtSignal()
    authRequest = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.__geometry_initialized = False

        self.__stack = QStackedWidget()

        self.setWindowTitle("Tell - Login")

        self.__login_page = LoginPage()
        self.__credentials_page = CredentialsPage()

        self.__stack.addWidget(self.__login_page)
        self.__stack.addWidget(self.__credentials_page)

        layout = QVBoxLayout(self)
        layout.addWidget(self.__stack)

        self._connect_signals()

    def _connect_signals(self) -> None:
        self.__login_page.btn_login_as_cliente.clicked.connect(  # type:ignore
            self.loginAsCliente.emit
        )

        self.__login_page.btn_login_with_credentials.clicked.connect(  # type:ignore
            partial(self.__stack.setCurrentWidget, self.__credentials_page)
        )

        self.__credentials_page.btn_indietro.clicked.connect(  # type:ignore
            self.reset_login_dialog
        )

        self.__credentials_page.btn_login.clicked.connect(  # type:ignore
            lambda: self.authRequest.emit(
                self.__credentials_page.username.text(),
                self.__credentials_page.password.text(),
            )
        )

    # ------------------------- SETUP QDialog -------------------------

    def showEvent(self, a0: Optional[QShowEvent]) -> None:
        super().showEvent(a0)

        if self.__geometry_initialized:
            return

        window = self.windowHandle()
        if not window:
            return

        screen = window.screen()
        if not screen:
            return

        screen_geom = screen.availableGeometry()
        self.setMinimumHeight(screen_geom.height() - 100)
        self.setMinimumWidth(int(screen_geom.width() / 1.8))

        fg = self.frameGeometry()
        fg.moveCenter(screen_geom.center())
        self.move(fg.topLeft())

        self.__geometry_initialized = True

    def keyPressEvent(self, a0: Optional[QKeyEvent]) -> None:
        if not isinstance(a0, QKeyEvent):
            raise TypeError(f"{type(QKeyEvent)} expect. Type recieved: {type(a0)}")
        if a0.key() == Qt.Key.Key_Escape:
            a0.ignore()
        else:
            super().keyPressEvent(a0)

    # ------------------------- METODI DELLA VIEW -------------------------

    def reset_login_dialog(self) -> None:
        """Annulla il tentativo di login."""
        self.__stack.setCurrentWidget(self.__login_page)
        self.reset_credentials_page()

    def reset_credentials_page(self) -> None:
        self.__credentials_page.reset_pagina()
