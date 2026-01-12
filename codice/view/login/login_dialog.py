from PyQt6.QtWidgets import QDialog, QStackedWidget, QVBoxLayout
from PyQt6.QtGui import QShowEvent
from PyQt6.QtCore import pyqtSignal
from functools import partial
from typing import Optional

from ._login_page import LoginPage
from ._credentials_page import CredentialsPage


class LoginDialog(QDialog):
    """Gestice la view della funzione di login dell'app.

    Segnali:
    - loginAsCliente(): Emesso quando l'utente ingressa all'app come Cliente;
    - authRequest(str, str): Emesso dopo inserire le credenziali richieste.
    """

    loginAsCliente = pyqtSignal()

    authRequest = pyqtSignal(str, str)

    def __init__(self) -> None:
        super().__init__()
        self._geometry_initialized = False

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
        self.__login_page.btn_cliente.clicked.connect(  # type:ignore
            self.loginAsCliente.emit
        )

        self.__login_page.btn_biglietteria.clicked.connect(  # type:ignore
            partial(self.__stack.setCurrentWidget, self.__credentials_page)
        )

        self.__login_page.btn_admin.clicked.connect(  # type:ignore
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

    def showEvent(self, a0: Optional[QShowEvent]) -> None:
        super().showEvent(a0)

        if self._geometry_initialized:
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

        self._geometry_initialized = True

    def reset_login_dialog(self):
        """Annulla il tentativo di login."""
        self.__stack.setCurrentWidget(self.__login_page)
        self.reset_credentials_page()

    def reset_credentials_page(self):
        self.__credentials_page.reset_pagina()
