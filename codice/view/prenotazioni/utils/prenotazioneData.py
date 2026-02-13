from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class PrenotazioneData:
    """Container immutabile per le pagine di `Prenotazione`."""

    id: int
    nominativo: str
    data_ora_registrazione: datetime
    is_pagata: bool
    ammontare: float  # Ottenuto chiamando un metodo del model
