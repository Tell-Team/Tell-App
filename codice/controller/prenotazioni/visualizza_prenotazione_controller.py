from typing import override

from core.controller import AbstractVisualizzaController

from model.model.model import Model, SezionePostiInfo
from model.organizzazione.prezzo import Prezzo
from model.exceptions import AzioneIncongruenteException

from view.prenotazioni.pagine import VisualizzaPrenotazioneView
from view.acquisto.widgets import EventoPostiDisplay

from view.utils.list_widgets import ListLayout


class VisualizzaPrenotazioneController(AbstractVisualizzaController):
    """Gestice la pagina `VisualizzaPrenotazioneView` dell'app.

    Segnali
    ---
    - `goBackRequest()`: emesso per tornare alla pagina `SpettacoliSectionView`.
    """

    _view_page: VisualizzaPrenotazioneView

    def __init__(self, model: Model, prenotazione_v: VisualizzaPrenotazioneView):
        if type(prenotazione_v) is not VisualizzaPrenotazioneView:
            raise TypeError("Atteso VisualizzaPrenotazioneView per prenotazione_v.")

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

    def __get_prezzo_by_spettacolo_e_sezione(self, id_spettacolo: int, id_sezione: int):
        return self._model.get_prezzo_by_spettacolo_e_sezione(id_spettacolo, id_sezione)

    def __display_posti_prenotati(self, layout_posti: ListLayout) -> None:
        """Mostra a schermo le informazioni degli posti prenotati.

        :param layout_posti: layout dove saranno caricate tutti i posti"""
        lista_posti = self._view_page.lista_evento_posti

        # Verifica che la lista non sia vuota
        if not lista_posti:
            layout_posti.mostra_msg_lista_vuota()
            return

        e, sp = lista_posti

        sezione_posti: list[SezionePostiInfo] = []
        for sezione, posti in sp:
            prezzo: Prezzo = self.__get_prezzo_by_spettacolo_e_sezione(
                e.get_id_spettacolo(), sezione.get_id()
            )  # type:ignore

            sezione_posti.append(
                SezionePostiInfo(
                    sezione_nome=sezione.get_nome(),
                    prezzo_ammontare=prezzo.get_ammontare(),
                    posti=posti,
                )
            )

        current_evento = EventoPostiDisplay(e.get_data_ora(), sezione_posti)

        layout_posti.aggiungi_list_item(current_evento)

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
