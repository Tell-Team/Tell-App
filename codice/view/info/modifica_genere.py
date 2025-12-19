from typing import override

from view.info.nuovo_genere import NuovoGenereView

from view.info.generePageData import GenerePageData


class ModificaGenereView(NuovoGenereView):
    """
    Sottoclasse di `NuovoGenereView`. Modifica l'header della pagina ed aggiunge
    un'attributo `cur_id_genere` per indicare l'id del genere da modificare.
    """

    def __init__(self) -> None:
        super().__init__()

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        # Il valore è assegnato quando si chiama InfoController.modifica_genere(id_genere)
        self.cur_id_genere: int = -1

        # Header
        self.header.setText("Modifica genere")

    # ------------------------- METODI DI VIEW -------------------------

    def set_data(self, data: GenerePageData) -> None:
        """Carica i dati di un genere nella pagina.

        :param data: data salvata in una classe immutabile"""
        self.cur_id_genere = data.id

        self.nome.setText(data.nome)
        self.descrizione.setText(data.descrizione)

    @override
    def reset_pagina(self) -> None:
        # Non è realmente necessario, ma serve per pulire la pagina dopo l'uso.
        super().reset_pagina()
        self.cur_id_genere = -1
