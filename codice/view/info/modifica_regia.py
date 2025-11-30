from controller.info_controller import InfoController

from view.info.nuova_regia import FormNuovaRegia


class FormModificaRegia(FormNuovaRegia):
    def __init__(self, info_controller: InfoController):
        super().__init__(info_controller)

        self._build_ui()

        # I campi di input sono atributi di FormNuovaRegia

    def _build_ui(self):
        super()._build_ui()
        # # Inziare pagina come ModificaRegia

        # Il valore di cur_id_opera è assegnato quando si chiama .modifica_regia(id_regia)
        self.cur_id_regia: int = -1

        # ## Modifica il header del layout
        self.header.setText("Modifica regia")

        # ## Modifica il pulsanti Conferma
        self.btn_conferma.clicked.connect(  # type:ignore
            lambda: print(
                "self.info_controller.salva_regia(is_new=False)"
            )  # - self.info_controller.salva_regia(is_new=False)
        )
