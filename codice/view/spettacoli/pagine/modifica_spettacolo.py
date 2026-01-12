from typing import override

from view.spettacoli.pagine import NuovoSpettacoloView
from view.spettacoli.utils import SpettacoloPageData

from view.utils.hyphenate_text import HyphenatedLabel
from view.style.uiStyle import QssStyle


class ModificaSpettacoloView(NuovoSpettacoloView):
    """Sottoclasse di `NuovoSpettacoloView`. Modifica alcune label della pagina ed aggiunge
    un'attributo `cur_id_spettacolo` per indicare l'id dello spettacolo da modificare.
    """

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        # Il valore è assegnato quando si chiama SpettacoliSectionController.modifica_spettacolo
        self.cur_id_spettacolo: int = -1

        # Aggiorna header
        self._header.setText("Modifica spettacolo")

        self.__tipo_spettacolo = HyphenatedLabel()
        self.__tipo_spettacolo.setProperty(QssStyle.SECONDARY_TEXT, True)

        self._form_layout.addWidget(self.__tipo_spettacolo)

    # ------------------------- METODI DI VIEW -------------------------

    def set_data(self, data: SpettacoloPageData, tipo_spettacolo: str = "") -> None:
        """Carica i dati di una regia nella pagina.

        :param data: data salvata in una classe immutabile"""
        self.cur_id_spettacolo = data.id

        self.titolo.setText(data.titolo)
        self.note.setText(data.note)
        self.lista_interpreti = data.interpreti
        self.lista_tecnici = data.tecnici

        if tipo_spettacolo:
            self.__tipo_spettacolo.setText(tipo_spettacolo)

    @override
    def reset_pagina(self) -> None:
        super().reset_pagina()
        self.cur_id_spettacolo = -1
        self.__tipo_spettacolo.setText("")
