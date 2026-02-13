from dataclasses import dataclass


@dataclass(frozen=True)
class GenereData:
    """Container immutabile per le pagine di `Genere`."""

    id: int
    nome: str
    descrizione: str
