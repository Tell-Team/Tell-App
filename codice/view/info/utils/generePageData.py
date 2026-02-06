from dataclasses import dataclass


@dataclass(frozen=True)
class GenerePageData:
    """Container immutabile per le pagine di `Genere`."""

    id: int
    nome: str
    descrizione: str
