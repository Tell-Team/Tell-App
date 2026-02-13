from dataclasses import dataclass

from view.spettacoli.utils import SpettacoloData


@dataclass(frozen=True)
class RegiaData(SpettacoloData):
    """Container immutabile per i widget di `Regia`."""

    regista: str
    anno_produzione: int
    id_opera: int
