from functools import partial
from typing import Optional

from core.controller import AbstractSectionController

from controller.navigation import Pagina

from model.model.model import Model, DettagliPrenotazione
from model.organizzazione.prenotazione import Prenotazione
from model.exceptions import OggettoInUsoException

from view.prenotazioni.pagine import PrenotazioniSectionView
from view.prenotazioni.utils import PrenotazioneData
from view.prenotazioni.widgets import PrenotazioneDisplay

from view.utils.list_widgets import ListLayout
from view.utils import mostra_error_popup

from view.style.ui_style import WidgetRole


class PrenotazioniSectionController(AbstractSectionController):
    """Gestice la sezione Prenotazioni (`PrenotazioniSectionView`) dell'app."""

    _view_section: PrenotazioniSectionView

    def __init__(self, model: Model, prenotazioni_s: PrenotazioniSectionView):
        if type(prenotazioni_s) is not PrenotazioniSectionView:
            raise TypeError("Atteso PrenotazioniSectionView per prenotazioni_s.")

        super().__init__(model, prenotazioni_s)

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    def _connect_signals(self) -> None:
        super()._connect_signals()

        # Display della Lista Prenotazioni
        self._view_section.displayPrenotazioniRequest.connect(  # type:ignore
            self.__display_prenotazioni
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __get_prenotazione(self, id_: int) -> Optional[Prenotazione]:
        return self._model.get_prenotazione(id_)

    def __get_prenotazioni(self) -> list[Prenotazione]:
        return self._model.get_prenotazioni()

    def __get_prenotazioni_by_nominativo(self, filtro: str) -> list[Prenotazione]:
        return self._model.get_prenotazioni_by_nominativo(filtro)

    def __get_dettagli_prenotazione(self, id_: int) -> DettagliPrenotazione:
        return self._model.get_dettagli_prenotazione(id_)

    def __elimina_prenotazione(self, id_: int) -> None:
        self._model.elimina_prenotazione(id_)

    def __ammontare_totale_prenotazione(self, id_: int) -> float:
        return self._model.ammontare_totale_prenotazione(id_)

    def __display_prenotazioni(self, layout_prenotazioni: ListLayout) -> None:
        """Mostra a schermo alcune informazioni delle prenotazioni salvate ed assegna a
        ciascuna dei pulsanti per visualizzarle in dettaglio o eliminarle.

        :param layout_prenotazioni: layout dove saranno caricate tutte le prenotazioni
        """
        # Verifica se c'è un filtro di ricerca
        filtro = self._view_section.filtro_ricerca

        lista_prenotazioni = (
            self.__get_prenotazioni()
            if not filtro
            else self.__get_prenotazioni_by_nominativo(filtro)
        )

        # Verifica che la lista non sia vuota
        if not lista_prenotazioni:
            layout_prenotazioni.mostra_msg_lista_vuota()
            return

        # Funzione di eliminazione per le prenotazioni
        def on_conferma(widget_prenotazione: PrenotazioneDisplay, id_: int) -> None:
            """Prova ad eliminare l'istanza di `Prenotazione`.

            :param widget_prenotazione: widget associato alla `Prenotazione` da eliminare
            :param id\\_: id della prenotazione da eliminare
            """
            try:
                self.__elimina_prenotazione(id_)
            except OggettoInUsoException as exc:
                widget_prenotazione.annulla_elimina()
                mostra_error_popup(self._view_section, "Prenotazione in uso", str(exc))
            else:
                self._view_section.aggiorna_pagina()

        # Mostra tutte le prenotazioni della lista a schermo
        for prenotazione in lista_prenotazioni:
            current_prenotazione = PrenotazioneDisplay(prenotazione)

            current_prenotazione.visualizzaRequest.connect(  # type:ignore
                self.__visualizza_prenotazione
            )

            current_prenotazione.eliminaConfermata.connect(  # type:ignore
                partial(on_conferma, current_prenotazione, prenotazione.get_id())
            )

            layout_prenotazioni.aggiungi_list_item(
                current_prenotazione, WidgetRole.ITEM_CARD
            )

    def __visualizza_prenotazione(self, id_: int) -> None:
        """Carica la pagina `VisualizzaPrenotazioneView` con i dati relativi alla prenotazione
        indicati.

        :param id\\_: id della prenotazione da visualizzare
        """
        # Copia della prenotazione da visualizzare
        current_prenotazione = self.__get_prenotazione(id_)
        if not current_prenotazione:
            mostra_error_popup(
                self._view_section,
                "Prenotazione inesistente",
                f"Non è presente nessuna prenotazione con id {id_}.",
            )
            return

        # Ottieni la pagina VisualizzaPrenotazioneView
        from view.prenotazioni.pagine import VisualizzaPrenotazioneView

        pagina_nome = Pagina.VISUALIZZA_PRENOTAZIONE
        current_pagina = self._ottieni_pagina(pagina_nome)
        if type(current_pagina) is not VisualizzaPrenotazioneView:
            self._mostra_msg_pagina_non_trovata(pagina_nome, type(current_pagina))
            return

        # Ottieni i dati della prenotazione
        prenotazione_data = PrenotazioneData(
            id=current_prenotazione.get_id(),
            nominativo=current_prenotazione.get_nominativo(),
            data_ora_registrazione=current_prenotazione.get_data_ora_registrazione(),
            is_pagata=current_prenotazione.pagata(),
            ammontare=self.__ammontare_totale_prenotazione(
                current_prenotazione.get_id()
            ),
        )

        dettagli = self.__get_dettagli_prenotazione(current_prenotazione.get_id())

        current_pagina.set_data(prenotazione_data, dettagli)

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)
