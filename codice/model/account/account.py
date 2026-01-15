from enum import Enum, auto
from typing import Self

from model.exceptions import (
    CredenzialiErrateException,
    DatoIncongruenteException,
    PermessiInsufficientiException,
)

LUNGHEZZA_MIN_PASSWORD = 8


class Ruolo(Enum):
    BIGLIETTERIA = auto()
    AMMINISTRATORE = auto()


class Account:
    __next_id = 0

    def __init__(self, username: str, password: str, ruolo: Ruolo):
        """Throws: DatoIncongruenteException"""
        self.__id = Account.__next_id
        Account.__next_id += 1

        self.set_username(username)
        self.__set_password(password)

        self.__ruolo = ruolo

    # Getters
    def get_id(self) -> int:
        return self.__id

    def get_username(self) -> str:
        return self.__username

    def get_ruolo(self) -> Ruolo:
        return self.__ruolo

    # Setters
    @staticmethod
    def set_next_id(next_id: int):
        """Throws: DatoIncongruenteException"""
        if next_id < 0:
            raise DatoIncongruenteException("Il next_id non può essere minore di 0.")

        Account.__next_id = next_id

    def set_username(self, username: str):
        """Throws: DatoIncongruenteException"""
        username_stripped = username.strip()
        if username_stripped == "":
            raise DatoIncongruenteException("Lo username non può essere vuoto.")

        self.__username = username_stripped

    def __set_password(self, password: str):
        """Throws: DatoIncongruenteException"""
        if password == "":
            raise DatoIncongruenteException("La password non può essere vuota.")

        if len(password) < LUNGHEZZA_MIN_PASSWORD:
            raise DatoIncongruenteException(
                f"La password deve essere lunga almeno {LUNGHEZZA_MIN_PASSWORD} caratteri."
            )

        self.__password = password

    # Controlli
    def controlla_password(self, password: str) -> bool:
        if password != self.__password:
            return False

        return True

    # Modifiche
    def cambia_password(self, password_corrente: str, nuova_password: str):
        """Throws: CredenzialiErrateException, DatoIncongruenteException"""
        if not self.controlla_password(password_corrente):
            raise CredenzialiErrateException("La password corrente inserita è errata.")

        self.__set_password(nuova_password)

    def cambia_ruolo(self, nuovo_ruolo: Ruolo, agent: Self):
        """Throws: PermessiInsufficientiException"""
        if agent.get_ruolo() != Ruolo.AMMINISTRATORE:
            raise PermessiInsufficientiException(
                "Solo un AMMINISTRATORE può modificare i ruoli di un account."
            )

        self.__ruolo = nuovo_ruolo

    # Magics
    def __eq__(self, other: object) -> bool:
        if (
            self.get_username() == other.get_username()  # type: ignore
            and self.__password == other.__password  # type: ignore
            and self.get_ruolo() == other.get_ruolo()  # type: ignore
        ):
            return True

        return False
