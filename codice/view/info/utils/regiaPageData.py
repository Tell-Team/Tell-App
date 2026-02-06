from dataclasses import dataclass

from view.spettacoli.utils import SpettacoloPageData


@dataclass(frozen=True)
class RegiaPageData(SpettacoloPageData):
    """Container immutabile per i widget di `Regia`."""

    regista: str
    anno_produzione: int
    id_opera: int
