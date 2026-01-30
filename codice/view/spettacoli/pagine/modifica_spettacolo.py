from typing import override

from view.spettacoli.pagine import NuovoSpettacoloView
from view.spettacoli.utils import SpettacoloPageData

from view.utils.hyphenate_text import HyphenatedLabel
from view.style.ui_style import WidgetRole, WidgetColor


class ModificaSpettacoloView(NuovoSpettacoloView):
    """Pagina per la modifica di spettacoli. Sottoclasse di `NuovoSpettacoloView`."""

    def __init__(self):
        super().__init__()

        # Valore assegnato quando si chiama SpettacoliSectionController.modifica_spettacolo
        self.id_current_spettacolo: int = -1

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        self._header.setText("Modifica spettacolo")

        self.__tipo_spettacolo = HyphenatedLabel()
        self.__tipo_spettacolo.setProperty(WidgetRole.BODY_TEXT, True)
        self.__tipo_spettacolo.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)

        self._form_layout.addWidget(self.__tipo_spettacolo)

    # ------------------------- METODI DI VIEW -------------------------

    def set_data(self, data: SpettacoloPageData, msg_tipo_spettacolo: str = "") -> None:
        """Carica i dati di una regia nella pagina.

        :param data: data salvata in una classe immutabile
        :param tipo_spettacolo: testo che chiarisce il tipo specifico dello `Spettacolo` e
        più informazioni rilevanti
        """
        self.id_current_spettacolo = data.id

        self.titolo.setText(data.titolo)
        self.note.setText(data.note)
        self.lista_interpreti = data.interpreti
        self.lista_tecnici = data.tecnici
        self.__tipo_spettacolo.setText(msg_tipo_spettacolo)

    @override
    def reset_pagina(self) -> None:
        super().reset_pagina()
        self.id_current_spettacolo = -1
        self.__tipo_spettacolo.setText("")
