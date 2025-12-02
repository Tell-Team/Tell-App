from view.info.nuova_opera import NuovaOperaView


class ModificaOperaView(NuovaOperaView):
    """
    Sottoclasse di `NuovaOperaView` che solo modifica il header della pagina.
    """

    def __init__(self):
        super().__init__()

    def _build_ui(self):
        super()._build_ui()

        # Il valore è assegnato quando si chiama .modifica_opera(id_opera)
        self.cur_id_opera: int = -1

        # Header
        self.header.setText("Modifica opera")
