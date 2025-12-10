from view.info.nuovo_genere import NuovoGenereView


class ModificaGenereView(NuovoGenereView):
    """
    Sottoclasse di `NuovoGenereView`. Modifica l'header della pagina ed aggiunge
    un'attributo `cur_id_genere` per indicare l'id del genere da modificare.
    """

    def __init__(self):
        super().__init__()

    def _build_ui(self):
        super()._build_ui()

        # Il valore è assegnato quando si chiama InfoController.modifica_genere(id_genere)
        self.cur_id_genere: int = -1

        # Header
        self.header.setText("Modifica genere")
