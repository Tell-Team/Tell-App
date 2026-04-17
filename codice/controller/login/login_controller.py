from PyQt6.QtCore import pyqtSignal, QObject
from functools import partial
from typing import Optional

from controller.login.user_session import UserSession

from model.model.model import Model
from model.account.account import Account

from model.exceptions import CredenzialiErrateException

from view.login import LoginDialog

from view.utils import mostra_error_popup


class LoginController(QObject):
    """Controller dedicato alla gestione del `LoginDialog`. Emette un segnale dopo verifica
    la correttezza delle credenziali inserite durante un tentativo di login oppure dopo
    accedere all'app come Cliente.

    Segnali
    ---
    - `loginSucceeded(UserSession)`: emesso quando viene verificato un login riuscito.
    """

    loginSucceeded = pyqtSignal(UserSession)

    def __init__(self, model: Model):
        super().__init__()
        self.__model = model
        self.__login_dialog = LoginDialog()

        self._connect_signals()

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    def _connect_signals(self) -> None:
        self.__login_dialog.loginAsCliente.connect(  # type:ignore
            partial(self.loginSucceeded.emit, UserSession.guest())
        )

        self.__login_dialog.authRequest.connect(  # type:ignore
            self.__login
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def get_dialog(self) -> LoginDialog:
        return self.__login_dialog

    def get_account(self, id_: int) -> Optional[Account]:
        return self.__model.get_account(id_)

    def __login(self, username: str, password: str) -> None:
        """Verifica la correttezza delle credenziali inserite durante un tentativo di login."""
        try:
            id_account = self.__model.login(username, password)
            # Non viene usato hashing
        except CredenzialiErrateException as exc:
            mostra_error_popup(self.__login_dialog, "Credenziali errate", str(exc))
            return
        else:
            if account := self.__model.get_account(id_account):
                user_session = UserSession(
                    id=account.get_id(),
                    username=account.get_username(),
                    ruolo=account.get_ruolo(),
                )
                self.loginSucceeded.emit(user_session)
            self.__login_dialog.reset_login_dialog()
