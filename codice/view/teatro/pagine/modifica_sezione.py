from typing import override

from view.teatro.pagine import NuovaSezioneView
from view.teatro.utils import SezionePageData


class ModificaSezioneView(NuovaSezioneView):
    """Pagina per la modifica di sezioni. Sottoclasse di `NuovaSezioneView`."""

    def __init__(self):
        super().__init__()

        self.id_current_sezione: int = -1

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        self._header.setText("Modifica sezione")

    # ------------------------- METODI DI VIEW -------------------------

    def set_data(self, data: SezionePageData) -> None:
        self.id_current_sezione = data.id

        self.nome.setText(data.nome)
        self.descrizione.setText(data.descrizione)

    @override
    def reset_pagina(self) -> None:
        super().reset_pagina()
        self.id_current_sezione = -1
