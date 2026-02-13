from dataclasses import dataclass


@dataclass(frozen=True)
class SezioneData:
    """Container immutabile per le pagine di `Sezione`."""

    id: int
    nome: str
    descrizione: str
