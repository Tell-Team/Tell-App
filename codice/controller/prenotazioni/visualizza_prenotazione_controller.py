from typing import override

from core.controller import AbstractVisualizzaController

from model.model.model import Model
from model.exceptions import AzioneIncongruenteException

from view.prenotazioni.pagine import VisualizzaPrenotazionePage
from view.acquisto.widgets import EventoPostiDisplay

from view.utils.list_widgets import ListLayout

from view.style.ui_style import WidgetRole


class VisualizzaPrenotazioneController(AbstractVisualizzaController):
    """Gestice la pagina `VisualizzaPrenotazionePage` dell'app.

    Segnali
    ---
    - `goBackRequest()`: emesso per tornare alla pagina `SpettacoliSection`.
    """

    _view_page: VisualizzaPrenotazionePage

    def __init__(self, model: Model, prenotazione_v: VisualizzaPrenotazionePage):
        if type(prenotazione_v) is not VisualizzaPrenotazionePage:
            raise TypeError("Atteso VisualizzaPrenotazionePage per prenotazione_v.")

        super().__init__(model, prenotazione_v)

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    @override
    def _connect_signals(self) -> None:
        super()._connect_signals()

        self._view_page.displayPostiRequest.connect(  # type:ignore
            self.__display_posti_prenotati
        )

        self._view_page.aggiornaStatoPrenotazione.connect(  # type:ignore
            self.__aggiorna_stato_prenotazione
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __display_posti_prenotati(self, layout_posti_prenotati: ListLayout) -> None:
        """Mostra a schermo le informazioni degli posti prenotati.

        :param layout_posti_prenotati: layout dove saranno caricate tutti i posti"""
        evento_dataora, lista_sezione_posti = self._view_page.lista_evento_posti

        # Verifica che la lista non sia vuota
        if evento_dataora is None or not lista_sezione_posti:
            layout_posti_prenotati.mostra_msg_lista_vuota()
            return

        current_evento_posti = EventoPostiDisplay(evento_dataora, lista_sezione_posti)

        layout_posti_prenotati.aggiungi_list_item(
            current_evento_posti, WidgetRole.Item.CARD
        )

    def __aggiorna_stato_prenotazione(self, is_pagata: bool) -> None:
        try:
            id_ = self._view_page.id_current_prenotazione
            (
                self._model.segna_prenotazione_come_pagata(id_)
                if is_pagata
                else self._model.segna_prenotazione_come_non_pagata(id_)
            )
        except AzioneIncongruenteException:
            return
