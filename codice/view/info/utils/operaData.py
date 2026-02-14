from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class OperaData:
    """Container immutabile per le pagine di `Opera`."""

    id: int
    nome: str
    trama: str
    id_genere: int
    compositore: str
    librettista: str
    atti: int
    data_rappresentazione: date
    teatro_rappresentazione: str
