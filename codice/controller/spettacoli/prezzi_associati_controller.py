from functools import partial
from typing import Optional, override

from core.controller import AbstractVisualizzaController

from controller.navigation import Pagina

from model.model.model import Model
from model.pianificazione.spettacolo import Spettacolo
from model.organizzazione.sezione import Sezione
from model.organizzazione.prezzo import Prezzo
from model.exceptions import IdInesistenteException

from view.spettacoli.pagine import PrezziAssociatiView
from view.spettacoli.utils import PrezzoData
from view.spettacoli.widgets import SezioniPrezziDisplay

from view.utils.list_widgets import ListLayout
from view.utils import mostra_error_popup


class PrezziAssociatiController(AbstractVisualizzaController):
    """Gestice la pagina `PrezziAssociatiView` dell'app.

    Segnali
    ---
    - `goBackRequest()`: emesso per tornare alla pagina `SpettacoliSectionView`.
    """

    _view_page: PrezziAssociatiView

    def __init__(self, model: Model, prezzi_v: PrezziAssociatiView):
        if type(prezzi_v) is not PrezziAssociatiView:
            raise TypeError("Atteso PrezziAssociatiView per prezzi_v.")

        super().__init__(model, prezzi_v)

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    @override
    def _connect_signals(self) -> None:
        super()._connect_signals()

        self._view_page.displaySezioniPrezziRequest.connect(  # type:ignore
            self.__display_sezioni
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __get_spettacolo(self, id_: int) -> Optional[Spettacolo]:
        return self._model.get_spettacolo(id_)

    def __get_sezioni(self) -> list[Sezione]:
        return self._model.get_sezioni()

    def __get_prezzo_by_spettacolo_e_sezione(
        self, id_spettacolo: int, id_sezione: int
    ) -> Optional[Prezzo]:
        return self._model.get_prezzo_by_spettacolo_e_sezione(id_spettacolo, id_sezione)

    def __elimina_prezzo(self, id_: int) -> None:
        self._model.elimina_prezzo(id_)

    def __display_sezioni(self, layout_sezioni_prezzi: ListLayout) -> None:
        """Mostra a schermo le informazioni delle coppie sezione-prezzo salvate e
        associate ad uno `Spettacolo` ed assegna a ciascuna dei pulsanti per creare,
        modificare o eliminare i prezzi.

        :param layout_sezioni_prezzi: layout dove saranno caricate tutte le coppie
        sezione-prezzo
        """
        lista_sezioni = self.__get_sezioni()

        # Verifica che la lista non sia vuota
        if not lista_sezioni:
            layout_sezioni_prezzi.mostra_msg_lista_vuota()
            return

        # Funzione di eliminazione per i prezzi
        def on_conferma(id_prezzo: int) -> None:
            """Prova ad eliminare un prezzo associato ad una sezione.

            :param id_prezzo: id del prezzo da eliminare"""
            try:
                self.__elimina_prezzo(id_prezzo)
            except IdInesistenteException as exc:
                mostra_error_popup(self._view_page, "ID Prezzo inesistente", str(exc))
            else:
                self._view_page.aggiorna_pagina()

        id_current_spettacolo = self._view_page.id_current_spettacolo
        for sezione in lista_sezioni:
            prezzo = self.__get_prezzo_by_spettacolo_e_sezione(
                id_current_spettacolo, sezione.get_id()
            )

            current_sezione_prezzo = SezioniPrezziDisplay(sezione, prezzo)

            if not Prezzo:
                current_sezione_prezzo.creaRequest.connect(  # type:ignore
                    partial(self.__nuovo_prezzo, sezione)
                )
            else:
                current_sezione_prezzo.modificaRequest.connect(  # type:ignore
                    partial(self.__modifica_prezzo, sezione)
                )
                current_sezione_prezzo.eliminaConfermata.connect(  # type:ignore
                    partial(on_conferma, prezzo.get_id())
                )

            layout_sezioni_prezzi.aggiungi_list_item(current_sezione_prezzo)

    def __nuovo_prezzo(self, sezione: Sezione) -> None:
        """Carica la pagina `NuovoPrezzoView`, creare un prezzo associato ad uno spettacolo
        ed una sezione.

        :param sezione: `Sezione` a cui il prezzo sarà associato"""
        current_spettacolo = self.__get_spettacolo(
            self._view_page.id_current_spettacolo
        )
        if not current_spettacolo:
            mostra_error_popup(
                self._view_page,
                "Spettacolo inesistente",
                f"Non è presente nessuno spettacolo con id {self._view_page.id_current_spettacolo}.",
            )
            return

        # Ottieni la pagina NuovoPrezzoView
        from view.spettacoli.pagine import NuovoPrezzoView

        pagina_nome = Pagina.NUOVO_PREZZO
        current_pagina = self._ottieni_pagina(pagina_nome)
        if type(current_pagina) is not NuovoPrezzoView:
            self._mostra_msg_pagina_non_trovata(pagina_nome, type(current_pagina))
            return

        # Setup dati nella pagina
        current_pagina.set_data(current_spettacolo, sezione)

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)

    def __modifica_prezzo(self, sezione: Sezione) -> None:
        """Carica la pagina `ModificaPrezzoView`, con i dati del prezzo indicato
        inseriti nei campo di input.

        :param sezione: `Sezione` a cui il prezzo è associato
        :param id_prezzo: id del prezzo da modificare
        """
        # Copia del prezzo da modificare
        current_spettacolo = self.__get_spettacolo(
            self._view_page.id_current_spettacolo
        )
        if not current_spettacolo:
            mostra_error_popup(
                self._view_page,
                "Spettacolo inesistente",
                f"Non è presente nessuno spettacolo con id {self._view_page.id_current_spettacolo}.",
            )
            return

        current_prezzo = self.__get_prezzo_by_spettacolo_e_sezione(
            current_spettacolo.get_id(), sezione.get_id()
        )
        if not current_prezzo:
            mostra_error_popup(
                self._view_page,
                "Prezzo inesistente",
                f"Non è presente nessun prezzo per la sezione con id {sezione.get_id()} "
                + f"per lo spettacolo con id {current_spettacolo.get_id()}.",
            )
            return

        # Ottieni la pagina ModificaPrezzoView
        from view.spettacoli.pagine import ModificaPrezzoView

        pagina_nome = Pagina.MODIFICA_PREZZO
        current_pagina = self._ottieni_pagina(pagina_nome)
        if type(current_pagina) is not ModificaPrezzoView:
            self._mostra_msg_pagina_non_trovata(pagina_nome, type(current_pagina))
            return

        # Salva i dati dentro di un container
        prezzo_data = PrezzoData(
            id=current_prezzo.get_id(),
            ammontare=current_prezzo.get_ammontare(),
            id_spettacolo=current_prezzo.get_id_spettacolo(),
            id_sezione=current_prezzo.get_id_sezione(),
        )

        current_pagina.set_data_modifica(prezzo_data, current_spettacolo, sezione)

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)
