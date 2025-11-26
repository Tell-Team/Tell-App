from model.model import Model
from controller.navigation import NavigationController

from view.info.nuova_regia import FormularioNuovaRegia


class FormularioModificaRegia(FormularioNuovaRegia):
    def __init__(self, model: Model, nav: NavigationController):
        super().__init__(model, nav)
        # I campi di input sono atributi di FormularioNuovaRegia

        # # Inziare pagina come ModificaRegia
        # ## Modifica il header del layout
        self.header.setText("Modifica regia")

        # ## Modifica il pulsanti Conferma
        self.btn_conferma.clicked.connect(  # type:ignore
            nav.go_back  # - DA CORRIGERE: Un trigger per verificare dati e salvare la regia modificata
        )
