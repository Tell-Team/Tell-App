from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class EventoPageData:
    """Container immutabile per le pagine di `Evento`."""

    id: int
    data_ora: datetime
    id_spettacolo: int
