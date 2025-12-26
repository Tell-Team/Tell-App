from typing import override

from view.info.pagine import NuovoGenereView
from view.info.utils import GenerePageData


class ModificaGenereView(NuovoGenereView):
    """Sottoclasse di `NuovoGenereView`. Modifica alcuni label della pagina ed aggiunge
    un'attributo `cur_id_genere` per indicare l'id del genere da modificare."""

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        # Il valore è assegnato quando si chiama InfoController.modifica_genere(id_genere)
        self.cur_id_genere: int = -1

        # Aggiorna header
        self._header.setText("Modifica genere")

        # Aggiorna btn_conferma
        self._btn_conferma.setText("Modifica")

    # ------------------------- METODI DI VIEW -------------------------

    def set_data(self, data: GenerePageData) -> None:
        """Carica i dati di un genere nella pagina.

        :param data: data salvata in una classe immutabile"""
        self.cur_id_genere = data.id

        self.nome.setText(data.nome)
        self.descrizione.setText(data.descrizione)

    @override
    def reset_pagina(self) -> None:
        super().reset_pagina()
        self.cur_id_genere = -1
