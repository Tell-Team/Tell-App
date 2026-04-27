from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PrezzoData:
    """Container immutabile per le pagine di `Prezzo`."""

    id: int
    ammontare: float
    id_spettacolo: int
    id_sezione: int
