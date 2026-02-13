from typing import override

from view.spettacoli.pagine import NuovoEventoView
from view.spettacoli.utils import EventoData


class ModificaEventoView(NuovoEventoView):
    """Pagina per la modifica di eventi. Sottoclasse di `NuovoEventoView`."""

    def __init__(self):
        super().__init__()

        # Valore assegnato quando si chiama VisualizzaSpettacoloController.modifica_evento
        self.id_current_evento: int = -1

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        self._header.setText("Modifica evento")

    # ------------------------- METODI DI VIEW -------------------------

    def set_data(self, data: EventoData) -> None:
        """Carica i dati di un evento nella pagina.

        :param data: data salvata in una classe immutabile"""
        self.id_current_evento = data.id

        self.data.setDate(data.data_ora.date())
        self.ora.setTime(data.data_ora.time())

        self.id_spettacolo = data.id_spettacolo

    @override
    def reset_pagina(self) -> None:
        super().reset_pagina()
        self.id_current_evento = -1
