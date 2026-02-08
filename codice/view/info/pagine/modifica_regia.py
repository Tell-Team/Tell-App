from typing import override

from view.info.pagine import NuovaRegiaView
from view.info.utils import RegiaPageData


class ModificaRegiaView(NuovaRegiaView):
    """Pagina per la modifica di regie. Sottoclasse di `NuovaRegiaView`."""

    def __init__(self):
        super().__init__()

        # Valore assegnato quando si chiama VisualizzaOperaController.modifica_regia
        self.id_current_regia: int = -1

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        self._header.setText("Modifica regia")

    # ------------------------- METODI DI VIEW -------------------------

    def set_data(self, data: RegiaPageData) -> None:
        """Carica i dati di una regia nella pagina.

        :param data: data salvata in una classe immutabile"""
        self.id_current_regia = data.id

        self.titolo.setText(data.titolo)
        self.note.setText(data.note)
        self.lista_interpreti = data.interpreti
        self.lista_musicisti_e_direttori_artistici = (
            data.musicisti_e_direttori_artistici
        )
        self.regista.setText(data.regista)
        self.anno.setValue(data.anno_produzione)

        current_id_opera = data.id_opera
        index = self.opera.findData(current_id_opera)
        if index >= 0:
            self.opera.setCurrentIndex(index)

    @override
    def reset_pagina(self) -> None:
        super().reset_pagina()
        self.id_current_regia = -1
