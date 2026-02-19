from functools import partial
from typing import Optional

from core.controller import AbstractSectionController

from controller.navigation import Pagina

from model.model.model import Model
from model.organizzazione.sezione import Sezione
from model.exceptions import OggettoInUsoException

from view.teatro.pagine import TeatroSectionView
from view.teatro.utils import SezioneData
from view.teatro.widgets import SezioneDisplay

from view.utils.list_widgets import ListLayout
from view.utils import mostra_error_popup
from view.style.ui_style import WidgetRole


class TeatroSectionController(AbstractSectionController):
    """Gestice la sezione Teatro (`TeatroSectionView`) dell'app."""

    _view_section: TeatroSectionView

    def __init__(self, model: Model, teatro_s: TeatroSectionView):
        if type(teatro_s) is not TeatroSectionView:
            raise TypeError("Atteso TeatroSectionView per teatro_s.")

        super().__init__(model, teatro_s)

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    def _connect_signals(self) -> None:
        super()._connect_signals()

        self._view_section.displaySezioniRequest.connect(  # type:ignore
            self.__display_sezioni
        )

        self._view_section.nuovaSezioneRequest.connect(  # type:ignore
            self.__nuova_sezione
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __get_sezione(self, id_: int) -> Optional[Sezione]:
        return self._model.get_sezione(id_)

    def __get_sezioni(self) -> list[Sezione]:
        return self._model.get_sezioni()

    def __elimina_sezione(self, id_: int) -> None:
        self._model.elimina_sezione(id_)

    def __display_sezioni(self, layout_sezioni: ListLayout) -> None:
        """Mostra a schermo le informazioni delle sezioni salvate ed assegna a
        ciascuna dei pulsanti per accedere alle loro liste posti, modificarle o eliminarle.

        :param layout_sezioni: layout dove saranno caricati tutte le sezioni
        """
        lista_sezioni = self.__get_sezioni()

        # Verifica che la lista non sia vuota
        if not lista_sezioni:
            layout_sezioni.mostra_msg_lista_vuota()
            return

        # Funzione di eliminazione per le sezioni
        def on_conferma(widget_sezione: SezioneDisplay, id_: int) -> None:
            """Prova ad eliminare l'istanza di `Sezione`.

            :param widget_sezione: widget associato alla `Sezione` da eliminare
            :param id\\_: id della sezione da eliminare
            """
            try:
                self.__elimina_sezione(id_)
            except OggettoInUsoException as exc:
                widget_sezione.annulla_elimina()
                mostra_error_popup(self._view_section, "Sezione in uso", str(exc))
            else:
                self._view_section.aggiorna_pagina()

        # Mostra tutte le sezioni salvati a schermo
        for sezione in lista_sezioni:
            current_sezione = SezioneDisplay(sezione)

            current_sezione.visualizzaRequest.connect(  # type:ignore
                self.__visualizza_sezione
            )

            current_sezione.modificaRequest.connect(  # type:ignore
                self.__modifica_sezione
            )

            current_sezione.eliminaConfermata.connect(  # type:ignore
                partial(on_conferma, current_sezione, sezione.get_id())
            )

            layout_sezioni.aggiungi_list_item(current_sezione, WidgetRole.Item.CARD)

    def __visualizza_sezione(self, id_: int) -> None:
        # Copia della sezione da visualizzare
        current_sezione = self.__get_sezione(id_)
        if not current_sezione:
            mostra_error_popup(
                self._view_section,
                "Sezione inesistente",
                f"Non è presente nessuna sezione con id {id_}.",
            )
            return

        # Ottieni la pagina ListaPostiView
        from view.teatro.pagine import VisualizzaSezioneView

        pagina_nome = Pagina.VISUALIZZA_SEZIONE
        try:
            pagina: VisualizzaSezioneView = self._ottieni_pagina(  # type:ignore
                pagina_nome, VisualizzaSezioneView
            )
        except TypeError:
            return

        sezione_data = SezioneData(
            id=current_sezione.get_id(),
            nome=current_sezione.get_nome(),
            descrizione=current_sezione.get_descrizione(),
        )

        pagina.reset_pagina()
        pagina.set_data(sezione_data)

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)

    def __nuova_sezione(self) -> None:
        """Carica la pagina `NuovaSezioneView`, dove l'utente può inserire i dati
        necessari per creare una sezione."""
        # Ottieni la pagina NuovaSezioneView
        from view.teatro.pagine import NuovaSezioneView

        pagina_nome = Pagina.NUOVA_SEZIONE
        try:
            pagina: NuovaSezioneView = self._ottieni_pagina(  # type:ignore
                pagina_nome, NuovaSezioneView
            )
        except TypeError:
            return

        # Setup pagina pulendo i campi
        pagina.reset_pagina()

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)

    def __modifica_sezione(self, id_: int) -> None:
        """Carica la pagina `ModificaSezioneView`, con i dati della sezione indicata
        inseriti nei campo di input.

        :param id_: id della sezione da modificare
        """
        # Copia della sezione da modificare
        current_sezione = self.__get_sezione(id_)
        if not current_sezione:
            mostra_error_popup(
                self._view_section,
                "Sezione inesistente",
                f"Non è presente nessuna sezione con id {id_}.",
            )
            return

        # Ottieni la pagina ModificaSezioneView
        from view.teatro.pagine import ModificaSezioneView

        pagina_nome = Pagina.MODIFICA_SEZIONE
        try:
            pagina: ModificaSezioneView = self._ottieni_pagina(  # type:ignore
                pagina_nome, ModificaSezioneView
            )
        except TypeError:
            return

        # Salva i dati dentro di un container
        sezione_data = SezioneData(
            id=current_sezione.get_id(),
            nome=current_sezione.get_nome(),
            descrizione=current_sezione.get_descrizione(),
        )

        # Setup pagina con i data della sezione
        pagina.set_data(sezione_data)

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)
