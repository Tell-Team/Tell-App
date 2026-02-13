from dataclasses import dataclass

from model.account.account import Ruolo


@dataclass(frozen=True)
class AccountData:
    """Container immutabile per le pagine di `Account`."""

    id: int
    username: str
    ruolo: Ruolo
