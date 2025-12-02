from view.spettacoli.nuova_regia import NuovaRegiaView


# - QUIZÁ DEBA QUITAR LA OPCIÓN PARA ELEGIR EL TIPO DE Spettacolo DEL QFormLayout. ASÍ
#   SIMPLIFICA LA CREACIÓN.
class ModificaRegiaView(NuovaRegiaView):
    def __init__(self):
        super().__init__()

    def _build_ui(self):
        super()._build_ui()

        # Il valore è assegnato quando si chiama .modifica_regia(id_regia)
        self.cur_id_regia: int = -1

        # Header
        self.header.setText("Modifica regia")
