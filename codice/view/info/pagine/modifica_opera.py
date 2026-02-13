from typing import override

from view.info.pagine import NuovaOperaView
from view.info.utils import OperaData


class ModificaOperaView(NuovaOperaView):
    """Pagina per la modifica di opere. Sottoclasse di `NuovaOperaView`."""

    def __init__(self):
        super().__init__()

        # Valore assegnato quando si chiama InfoSectionController.modifica_opera
        self.id_current_opera: int = -1

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        self._header.setText("Modifica opera")

    # ------------------------- METODI DI VIEW -------------------------

    def set_data(self, data: OperaData) -> None:
        """Carica i dati di un'opera nella pagina.

        :param data: data salvata in una classe immutabile"""
        self.id_current_opera = data.id

        self.nome.setText(data.nome)
        self.trama.setText(data.trama)

        current_id_genere = data.id_genere
        index = self.genere.findData(current_id_genere)
        if index >= 0:
            self.genere.setCurrentIndex(index)

        self.compositore.setText(data.compositore)
        self.librettista.setText(data.librettista)
        self.atti.setValue(data.atti)
        self.data.setDate(data.data_rappresentazione)
        self.teatro.setText(data.teatro_rappresentazione)

    @override
    def reset_pagina(self) -> None:
        super().reset_pagina()
        self.id_current_opera = -1
