from typing import override

from view.info.pagine import NuovaRegiaView
from view.info.utils import RegiaPageData


class ModificaRegiaView(NuovaRegiaView):
    """Sottoclasse di `NuovaRegiaView`. Modifica alcuni label della pagina ed aggiunge
    un'attributo `cur_id_regia` per indicare l'id della regia da modificare."""

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        # Il valore è assegnato quando si chiama InfoController.modifica_regia(id_regia)
        self.cur_id_regia: int = -1

        # Aggiorna header
        self._header.setText("Modifica regia")

        # Aggiorna btn_conferma
        self._btn_conferma.setText("Modifica")

    # ------------------------- METODI DI VIEW -------------------------

    def set_data(self, data: RegiaPageData) -> None:
        """Carica i dati di una regia nella pagina.

        :param data: data salvata in una classe immutabile"""
        self.cur_id_regia = data.id

        self.titolo.setText(data.titolo)
        self.note.setText(data.note)
        self.lista_interpreti = data.interpreti
        self.lista_tecnici = data.tecnici
        self.regista.setText(data.regista)
        self.anno.setValue(data.anno_produzione)

        cur_id_opera = data.id_opera
        index = self.opera.findData(cur_id_opera)
        if index >= 0:
            self.opera.setCurrentIndex(index)

    @override
    def reset_pagina(self) -> None:
        super().reset_pagina()
        self.cur_id_regia = -1
