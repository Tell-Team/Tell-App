from typing import override

from model.pianificazione.spettacolo import Spettacolo
from model.organizzazione.sezione import Sezione

from view.spettacoli.pagine import NuovoPrezzoView
from view.spettacoli.utils import PrezzoPageData


class ModificaPrezzoView(NuovoPrezzoView):
    """Pagina per la modifica di prezzi. Sottoclasse di `NuovoPrezzoView`."""

    def __init__(self) -> None:
        super().__init__()

        self.id_current_prezzo = -1

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        # Header
        self._header.setText("Modifica prezzo")

    # ------------------------- METODI DI VIEW -------------------------

    @override
    def reset_pagina(self) -> None:
        super().reset_pagina()

        self._input_error.setText("")
        self.id_current_prezzo = -1

    def set_data_modifica(
        self, data: PrezzoPageData, spettacolo: Spettacolo, sezione: Sezione
    ) -> None:
        super().set_data(spettacolo, sezione)

        self.id_current_prezzo = data.id
        self.prezzo.setText(f"{data.ammontare:.2f}")
