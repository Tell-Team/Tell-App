from typing import Optional

# from .session_context import SessionContext

from model.model import Model
from model.account import Ruolo  # , Permission, UserSession


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
        self.__id_account = None
        self.__ruolo = None

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
        return self.__ruolo is Ruolo.BIGLIETTERIA

    def is_admin(self) -> bool:
        return self.__ruolo is Ruolo.AMMINISTRATORE

    # def can_cud_spettacoli(self) -> bool:
    #     return self.__has_permission(Permission.CUD_SPETTACOLI)

    # def can_cud_eventi(self) -> bool:
    #     return self.__has_permission(Permission.CUD_EVENTI)

    # def can_gestire_prenotazioni(self) -> bool:
    #     return self.__has_permission(Permission.GESTIRE_PRENOTAZIONI)

    # def can_cud_opere(self) -> bool:
    #     return self.__has_permission(Permission.CUD_OPERE)

    # def can_cud_generi(self) -> bool:
    #     return self.__has_permission(Permission.CUD_GENERI)

    # def can_cud_regie(self) -> bool:
    #     return self.__has_permission(Permission.CUD_REGIE)

    # def can_cud_sezioni(self) -> bool:
    #     return self.__has_permission(Permission.CUD_SEZIONI)

    # def can_cud_posti(self) -> bool:
    #     return self.__has_permission(Permission.CUD_POSTI)

    # def can_crud_account(self) -> bool:
    #     return self.__has_permission(Permission.CRUD_ACCOUNT)

    # def __has_permission(self, permission: Permission) -> bool:
    #     user = self.__session.get_user()
    #     if user is None:
    #         return False
    #     return permission in user.get_permissions()
