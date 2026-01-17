from typing import Optional

# from .session_context import SessionContext

from model.model import Model
from model.account.account import Ruolo  # , Permission, UserSession
from model.exceptions import AccountInesistenteException


class AuthenticationService:
    """Servizio per la gestione della autenticazione e autorizazioni degli utenti. Gestisce
    il login (con autenticazione o come Cliente), il logout ed espone metodi per verificare
    i permessi dell'utente, tenendo la logica di sessione separata dai controller e la view.
    """

    def __init__(self):
        self.__id_account: Optional[int] = None
        self.__ruolo: Optional[Ruolo] = None

    # def __init__(self, session: SessionContext):
    #     self.__session = session

    # ------------------------- LIFECYCLE DELLE SESSIONI -------------------------

    def login(self, id_account: int, model: Model) -> None:
        if account := model.get_account(id_account):
            self.__id_account = id_account
            self.__ruolo = account.get_ruolo()
            return
        raise AccountInesistenteException("Impossibile effetuare login.")

    def login_as_cliente(self) -> None:
        self.__id_account = None
        self.__ruolo = None

    def logout(self) -> None:
        self.__id_account = None
        self.__ruolo = None

    # ------------------------- GESTIONE DI PERMESSI -------------------------

    def get_id(self) -> Optional[int]:
        return self.__id_account

    def is_biglietteria(self) -> bool:
        if self.__ruolo is Ruolo.AMMINISTRATORE:
            return True
        return self.__ruolo is Ruolo.BIGLIETTERIA

    def is_admin(self) -> bool:
        return self.__ruolo is Ruolo.AMMINISTRATORE
