from typing import override

from view.info.pagine import NuovoGenerePage
from view.info.utils import GenereData


class ModificaGenerePage(NuovoGenerePage):
    """Pagina per la modifica di generi. Sottoclasse di `NuovoGenerePage`."""

    def __init__(self):
        super().__init__()

        # Valore assegnato quando si chiama InfoSectionController.modifica_genere
        self.id_current_genere: int = -1

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        self._header.setText("Modifica genere")

    # ------------------------- METODI DI VIEW -------------------------

    def set_data(self, data: GenereData) -> None:
        """Carica i dati di un genere nella pagina.

        :param data: data salvata in una classe immutabile"""
        self.id_current_genere = data.id

        self.nome.setText(data.nome)
        self.descrizione.setText(data.descrizione)

    @override
    def reset_pagina(self) -> None:
        super().reset_pagina()
        self.id_current_genere = -1
