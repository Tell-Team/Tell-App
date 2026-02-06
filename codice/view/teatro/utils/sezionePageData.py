from dataclasses import dataclass


@dataclass(frozen=True)
class SezionePageData:
    """Container immutabile per le pagine di `Sezione`."""

    id: int
    nome: str
    descrizione: str
