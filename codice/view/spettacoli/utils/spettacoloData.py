from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SpettacoloData:
    """Container immutabile per le pagine di `Spettacolo`."""

    id: int
    titolo: str
    note: str
    # It's necessary to pass a copy of the dictionary to avoid modifying it by accident.
    # (en inglés sí me dio craneo pa verborrear)
    interpreti: dict[str, str]
    musicisti_e_direttori_artistici: dict[str, str]
