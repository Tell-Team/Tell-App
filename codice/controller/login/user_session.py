from dataclasses import dataclass
from typing import Optional

from model.account.account import Ruolo


@dataclass(frozen=True)
class UserSession:
    """Container immutabile per la creazioni di sessioni utente."""

    id: int
    username: str
    ruolo: Optional[Ruolo]

    @classmethod
    def guest(cls) -> "UserSession":
        return cls(id=-1, username="Cliente", ruolo=None)

    def ha_permessi_admin(self) -> bool:
        return self.ruolo == Ruolo.AMMINISTRATORE

    def ha_permessi_biglietteria(self) -> bool:
        return self.ruolo == Ruolo.AMMINISTRATORE or self.ruolo == Ruolo.BIGLIETTERIA
