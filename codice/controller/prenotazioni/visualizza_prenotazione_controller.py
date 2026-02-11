from PyQt6.QtWidgets import QWidget
from functools import partial
from typing import Optional, override

from core.controller import AbstractVisualizzaController

from controller.navigation import Pagina

from model.model.model import Model
from model.pianificazione.spettacolo import Spettacolo
from model.organizzazione.evento import Evento
from model.organizzazione.prenotazione import Prenotazione
from model.exceptions import OggettoInUsoException

from view.prenotazioni.pagine import VisualizzaPrenotazioneView

# - DEBE HABER LISTA POSTI

from view.utils.list_widgets import ListLayout
from view.utils import PopupMessage


class VisualizzaPrenotazioneController(AbstractVisualizzaController):
    """Gestice la pagina `VisualizzaPrenotazioneView` dell'app.

    Segnali
    ---
    - `goBackRequest()`: emesso per tornare alla pagina `SpettacoliSectionView`.
    # - CORREGIR
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

        self._view_page.aggiornaStatoPrenotazione.connect(  # type:ignore
            self.__aggiorna_stato_prenotazione
        )

        # self._view_page.displayEventiRequest.connect(  # type:ignore
        #     self.__display_eventi
        # )

        # self._view_page.nuovoEventoRequest.connect(  # type:ignore
        #     self.__nuovo_evento
        # )

        # self._view_page.visualizzaPrezziRequest.connect(  # type:ignore
        #     self.__visualizza_prezzi_associati
        # )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __get_prenotazione(self, id_: int) -> Optional[Prenotazione]:
        return self._model.get_prenotazione(id_)

    def __aggiorna_stato_prenotazione(self, is_pagata: bool) -> None:
        current_prenotazione = self.__get_prenotazione(
            self._view_page.id_current_prenotazione
        )
        assert isinstance(current_prenotazione, Prenotazione)

        if is_pagata:
            try:
                current_prenotazione.segna_come_pagata()
            except:
                return
        elif not is_pagata:
            try:
                current_prenotazione.segna_come_non_pagata()
            except:
                return

    # def __display_eventi(self, layout_eventi: ListLayout) -> None:
    #     """Mostra a schermo le informazioni degli eventi salvati e associati ad
    #     uno spettacolo ed assegna a ciascuno dei pulsanti per modificarli o eliminarli.

    #     :param layout_eventi: layout dove saranno caricate tutti le regie
    #     """
    #     lista_eventi = self.__get_eventi_by_spettacolo(
    #         self._view_page.id_current_spettacolo
    #     )

    #     # Verifica che la lista non sia vuota
    #     if not lista_eventi:
    #         layout_eventi.mostra_msg_lista_vuota()
    #         return

    #     lista_eventi = sorted(lista_eventi, key=lambda x: (x.get_data_ora()))

    #     # Funzione di eliminazione per gli eventi
    #     def on_conferma(widget_evento: EventoDisplay, id_: int) -> None:
    #         """Prova ad eliminare l'istanza di Evento.

    #         :param widget_evento: widget associato all'Evento` da eliminare
    #         :param id\\_: id dell'evento da eliminare
    #         """
    #         try:
    #             self.__elimina_evento(id_)
    #         except OggettoInUsoException as exc:
    #             widget_evento.annulla_elimina()
    #             PopupMessage.mostra_errore(
    #                 self._view_page,
    #                 "Evento in uso",
    #                 f"Si è verificato un errore: {exc}",
    #             )
    #         else:
    #             self._view_page.aggiorna_pagina()

    #     for evento in lista_eventi:
    #         current_evento = EventoDisplay(evento)

    #         current_evento.modificaRequest.connect(  # type:ignore
    #             self.__modifica_evento
    #         )

    #         current_evento.eliminaConfermata.connect(  # type:ignore
    #             partial(on_conferma, current_evento, evento.get_id())
    #         )

    #         layout_eventi.aggiungi_list_item(current_evento)
