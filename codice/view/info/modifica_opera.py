from typing import override

from view.info.nuova_opera import NuovaOperaView

from view.info.operaPageData import OperaPageData


class ModificaOperaView(NuovaOperaView):
    """
    Sottoclasse di `NuovaOperaView`. Modifica l'header della pagina ed aggiunge
    un'attributo `cur_id_opera` per indicare l'id dell'opera da modificare.
    """

    def __init__(self) -> None:
        super().__init__()

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        # Il valore è assegnato quando si chiama InfoController.modifica_opera(id_opera)
        self.cur_id_opera: int = -1

        # Header
        self.header.setText("Modifica opera")

    # ------------------------- METODI DI VIEW -------------------------

    def set_data(self, data: OperaPageData) -> None:
        """Carica i dati di un'opera nella pagina.

        :param data: data salvata in una classe immutabile"""
        self.cur_id_opera = data.id

        self.nome.setText(data.nome)
        self.trama.setText(data.trama)

        cur_id_genere = data.id_genere
        index = self.genere.findData(cur_id_genere)
        if index >= 0:
            self.genere.setCurrentIndex(index)

        self.compositore.setText(data.compositore)
        self.librettista.setText(data.librettista)
        self.atti.setValue(data.atti)
        self.data.setDate(data.data_rappresentazione)
        self.teatro.setText(data.teatro_rappresentazione)

    @override
    def reset_pagina(self) -> None:
        # Non è realmente necessario, ma serve per pulire la pagina dopo l'uso.
        super().reset_pagina()
        self.cur_id_genere = -1
