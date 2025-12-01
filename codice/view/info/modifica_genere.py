from functools import partial

from controller.info_controller import InfoController

from view.info.nuovo_genere import FormNuovoGenere


class FormModificaGenere(FormNuovoGenere):
    def __init__(self, info_controller: InfoController):
        super().__init__(info_controller)

        # I campi di input sono atributi di FormNuovoGenere

    def _build_ui(self):
        super()._build_ui()
        # # Inziare pagina come ModificaGenere

        # Il valore di cur_id_opera è assegnato quando si chiama .modifica_genere(id_genere)
        self.cur_id_genere: int = -1

        # ## Modifica il header del layout
        self.header.setText("Modifica genere")

        # ## Modifica il pulsanti Conferma
        self.btn_conferma.clicked.disconnect()  # type:ignore
        self.btn_conferma.clicked.connect(  # type:ignore
            partial(self.info_controller.salva_genere, is_new=False)
        )
