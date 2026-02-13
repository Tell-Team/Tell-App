from dataclasses import dataclass


@dataclass(frozen=True)
class PostoData:
    """Container immutabile per le pagine di `Posto`."""

    id: int
    fila: str
    numero: int
    id_sezione: int
