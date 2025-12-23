from PyQt6.QtCore import pyqtSignal, QObject
from functools import partial

from controller.navigation import Pagina

from model.model import Model

from view.login.login_page import LoginPage
from view.login.authentication_page import AuthenticationPage


class LoginController(QObject):
    """# - ancora non so come funzionerà sto controller."""

    goBackRequest = pyqtSignal()
    goToPageRequest = pyqtSignal(Pagina, bool)

    def __init__(
        self, model: Model, login_v: LoginPage, auth_v: AuthenticationPage
    ) -> None:
        super().__init__()
        self.__model = model
        self.__login_page = login_v
        self.__authentication_page = auth_v

        self._connect_signals()

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    def _connect_signals(self) -> None:
        self.__login_page.loginAsCliente.connect(  # type:ignore
            partial(self.goToPageRequest.emit, Pagina.SEZIONE_SPETTACOLI, True)
        )

        # - Il ruolo dell'utente non è ancora implementato
        self.__login_page.loginAsBiglietteria.connect(  # type:ignore
            partial(self.goToPageRequest.emit, Pagina.PAGINA_AUTENTICAZIONE, True)
        )

        # - Il ruolo dell'utente non è ancora implementato
        self.__login_page.loginAsAdmin.connect(  # type:ignore
            partial(self.goToPageRequest.emit, Pagina.PAGINA_AUTENTICAZIONE, True)
        )

        self.__authentication_page.annullaRequest.connect(  # type:ignore
            self.annulla_login
        )

        self.__authentication_page.authRequest.connect(  # type:ignore
            self.login_attempt
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def annulla_login(self) -> None:
        """Annulla il tentativo di login."""
        self.goBackRequest.emit()
        self.__authentication_page.reset_pagina()

    def login_attempt(self, username: str, password: str) -> None:
        ...  # - Da definere
        self.goToPageRequest.emit(Pagina.SEZIONE_SPETTACOLI, True)
