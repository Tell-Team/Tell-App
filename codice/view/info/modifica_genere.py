from model.model import Model
from controller.navigation import NavigationController

from view.info.nuovo_genere import FormularioNuovoGenere


class FormularioModificaGenere(FormularioNuovoGenere):
    def __init__(self, model: Model, nav: NavigationController):
        super().__init__(model, nav)
        # I campi di input sono atributi di FormularioNuovoGenere

        # # Inziare pagina come ModificaGenere
        # ## Modifica il header del layout
        self.header.setText("Modifica genere")

        # ## Modifica il pulsanti Conferma
        self.btn_conferma.clicked.connect(  # type:ignore
            info_controller.salva_genere(is_new=False)
        )
