from PyQt6.QtCore import pyqtSignal, QObject
from typing import Optional

from model.model import Model
from model.account.account import Account
from model.exceptions import CredenzialiErrateException, AccountInesistenteException

from view.login import LoginDialog

from view.utils import PopupMessage


class LoginController(QObject):
    """Gestisce la funzione di login dell'app.

    Segnali:
    - loginSucceeded(): emesso quando viene verificato un login riuscito."""

    loginSucceeded = pyqtSignal()

    def __init__(self, model: Model, login_d: LoginDialog) -> None:
        super().__init__()
        self.__model = model
        self.__login_dialog = login_d

        self._connect_signals()

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    def _connect_signals(self) -> None:
        self.__login_dialog.loginAsCliente.connect(  # type:ignore
            self.loginSucceeded.emit  # - RUOLO ANCORA NON IMPLEMENTATO
        )

        self.__login_dialog.authRequest.connect(  # type:ignore
            self.__login
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __get_account(self, id_: int) -> Optional[Account]:
        return self.__model.get_account(id_)

    def __login(self, username: str, password: str) -> None:
        try:
            id_account = self.__model.login(username, password)
            # Non viene usato hashing
        except CredenzialiErrateException as exc:
            PopupMessage.mostra_errore(
                self.__login_dialog,
                "Credenziali errate",
                f"Si è verificato un errore: {exc}",
            )
            return
        except AccountInesistenteException as exc:
            PopupMessage.mostra_errore(
                self.__login_dialog,
                "Account inesistente",
                f"Si è verificato un errore: {exc}",
            )
        else:
            if user := self.__get_account(id_account):
                ruolo = user.get_ruolo()
                # - DOVREI USARE user COME PARAMETRO DI loginSucceeded
            self.__login_dialog.reset_credentials_page()
            self.loginSucceeded.emit()  # - RUOLO ANCORA NON IMPLEMENTATO
            self.__login_dialog.reset_login_dialog()
