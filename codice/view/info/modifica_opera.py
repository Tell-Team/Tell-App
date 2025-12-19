from view.info.nuova_opera import NuovaOperaView


class ModificaOperaView(NuovaOperaView):
    """
    Sottoclasse di `NuovaOperaView`. Modifica l'header della pagina ed aggiunge
    un'attributo `cur_id_opera` per indicare l'id dell'opera da modificare.
    """

    def __init__(self) -> None:
        super().__init__()

    # ------------------------- SETUP INIT -------------------------

    def _setup_ui(self) -> None:
        super()._setup_ui()

        # Il valore è assegnato quando si chiama InfoController.modifica_opera(id_opera)
        self.cur_id_opera: int = -1

        # Header
        self.header.setText("Modifica opera")
