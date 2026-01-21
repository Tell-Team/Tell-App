from model.account.account import Account, Ruolo
from model.exceptions import (
    IdOccupatoException,
    IdInesistenteException,
    PermessiInsufficientiException,
    AccountInesistenteException,
    CredenzialiErrateException,
    OccupatoException,
)
from typing import Optional
import copy


class GestoreAccounts:
    def __init__(self):
        self.__lista_accounts: list[Account] = []
        self.__lista_accounts.append(Account("admin", "00000000", Ruolo.AMMINISTRATORE))

    # Stato
    def ha_permessi_amministratore(self, id_: int) -> bool:
        """Throws: IdInesistenteException"""
        agent = self.get_account(id_)
        if agent is None:
            raise IdInesistenteException(f"Non è presente nessun account con id {id_}.")

        return agent.ha_permessi_amministratore()

    # Getters
    def get_max_id(self) -> int:
        ids = map(lambda x: x.get_id(), self.__lista_accounts)

        try:
            return max(ids)
        except ValueError:
            return -1

    def get_account(self, id_: int) -> Optional[Account]:
        for a in self.__lista_accounts:
            if a.get_id() == id_:
                return copy.copy(a)

        return None

    def get_accounts(self) -> list[Account]:
        return copy.deepcopy(self.__lista_accounts)

    # Permissions
    def __controlla_permessi_amministratore(self, agent_id: int, azione: str):
        """Throws: IdInesistenteException, PermessiInsufficientiException"""
        agent = self.get_account(agent_id)
        if agent is None:
            raise IdInesistenteException(
                f"Non è presente nessun account con id {agent_id} (id agent)."
            )

        if agent.get_ruolo() != Ruolo.AMMINISTRATORE:
            raise PermessiInsufficientiException(
                f"Solo un AMMINISTRATORE può {azione}."
            )

    # Validazione
    def __controllo_unique_key(self, primo: Account, secondo: Account):
        """Throws: OccupatoException"""
        if primo.get_username() == secondo.get_username():
            raise OccupatoException(
                f'E\' già presente un account con username "{primo.get_username()}".'
            )

    # Modificatori
    def aggiungi_account(self, account: Account, agent_id: int):
        """Throws: OccupatoException, PermessiInsufficientiException, IdOccupatoException, IdInesistenteException"""
        self.__controlla_permessi_amministratore(agent_id, "creare nuovi accounts")

        for a in self.__lista_accounts:
            if a.get_id() == account.get_id():
                raise IdOccupatoException(
                    f"E' già presente un account con id {a.get_id()}."
                )

            self.__controllo_unique_key(a, account)

        self.__lista_accounts.append(copy.copy(account))

    def elimina_account(self, id_: int, agent_id: int):
        """Throws: PermessiInsufficientiException, IdInesistenteException"""
        self.__controlla_permessi_amministratore(agent_id, "eliminare accounts")

        for i, a in enumerate(self.__lista_accounts):
            if a.get_id() == id_:
                self.__lista_accounts.pop(i)
                return

        raise IdInesistenteException(f"Non è presente nessun account con id {id_}.")

    def cambia_password(
        self, account_id: int, password_corrente: str, nuova_password: str
    ):
        """Throws: CredenzialiErrateException, DatoIncongruenteException, IdInesistenteException"""
        account = self.get_account(account_id)
        if account is None:
            raise IdInesistenteException(
                f"Non è presente nessun account con id {account_id}."
            )

        account.cambia_password(password_corrente, nuova_password)

    def cambia_ruolo(self, account_id: int, nuovo_ruolo: Ruolo, agent_id: int):
        """Throws: PermessiInsufficientiException, IdInesistenteException"""
        account = self.get_account(account_id)
        if account is None:
            raise IdInesistenteException(
                f"Non è presente nessun account con id {account_id}."
            )

        agent = self.get_account(agent_id)
        if agent is None:
            raise IdInesistenteException(
                f"Non è presente nessun account con id {agent_id}."
            )

        account.cambia_ruolo(nuovo_ruolo, agent)

    # Login
    def login(self, username: str, password: str) -> int:
        """Throws: CredenzialiErrateException, AccountInesistenteException"""
        for a in self.__lista_accounts:
            if a.get_username() == username:
                if not a.controlla_password(password):
                    raise CredenzialiErrateException(
                        "Le credenziali fornite sono errate."
                    )

                return a.get_id()

        raise AccountInesistenteException(
            f'Non esiste nessun account con username "{username}".'
        )
