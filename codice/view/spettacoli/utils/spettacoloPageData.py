from dataclasses import dataclass


@dataclass(frozen=True)
class SpettacoloPageData:
    """Container immutabile per le pagine di `Spettacolo`."""

    id: int
    titolo: str
    note: str
    interpreti: dict[str, str]
    musicisti_e_direttori_artistici: dict[str, str]
