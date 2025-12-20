from dataclasses import dataclass


@dataclass(frozen=True)
class RegiaPageData:
    """Container immutabile per le pagine di Regia."""

    id: int
    regista: str
    anno_produzione: int
    id_opera: int
    titolo: str
    note: str
    interpreti: dict[str, str]
    tecnici: dict[str, str]
