from functools import partial
from typing import Optional

from core.controller import AbstractSectionController

from controller.navigation import Pagina

from model.model.model import Model
from model.pianificazione.spettacolo import Spettacolo
from model.pianificazione.regia import Regia
from model.exceptions import OggettoInUsoException

from view.spettacoli.pagine import SpettacoliSectionView
from view.spettacoli.widgets import SpettacoloDisplay
from view.spettacoli.utils import SpettacoloData
from view.info.utils import RegiaData

from view.utils.list_widgets import ListLayout
from view.utils import mostra_error_popup
from view.style.ui_style import WidgetRole


class SpettacoliSectionController(AbstractSectionController):
    """Gestice la sezione Spettacoli (`SpettacoliSectionView`) dell'app."""

    _view_section: SpettacoliSectionView

    def __init__(self, model: Model, spettacoli_s: SpettacoliSectionView):
        if type(spettacoli_s) is not SpettacoliSectionView:
            raise TypeError("Atteso AcquistoSectionView per spettacoli_s.")

        super().__init__(model, spettacoli_s)

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    def _connect_signals(self) -> None:
        super()._connect_signals()

        # Display della Lista Spettacoli
        self._view_section.displaySpettacoliRequest.connect(  # type:ignore
            self.__display_spettacoli
        )

        # Setup della pagina di creazione di spettacoli
        self._view_section.nuovoSpettacoloRequest.connect(  # type:ignore
            self.__nuovo_spettacolo
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __get_spettacolo(self, id_: int) -> Optional[Spettacolo]:
        return self._model.get_spettacolo(id_)

    def __get_spettacoli(self) -> list[Spettacolo]:
        return self._model.get_spettacoli()

    def __get_spettacoli_by_titolo(self, titolo: str) -> list[Spettacolo]:
        return self._model.get_spettacoli_by_titolo(titolo)

    def __elimina_spettacolo(self, id_: int) -> None:
        self._model.elimina_spettacolo(id_)

    def __display_spettacoli(self, layout_spettacoli: ListLayout) -> None:
        """Mostra a schermo alcune informazioni degli spettacoli salvati ed assegna a
        ciascuno dei pulsanti per visualizzarli in dettaglio, scegliere posti, modificarli
        o eliminarli.

        :param layout_spettacoli: layout dove saranno caricati tutti gli spettacoli
        """
        # Verifica se c'è un filtro di ricerca
        filtro = self._view_section.filtro_ricerca

        lista_spettacoli = (
            self.__get_spettacoli()
            if not filtro
            else self.__get_spettacoli_by_titolo(filtro)
        )

        # Verifica che la lista non sia vuota
        if not lista_spettacoli:
            layout_spettacoli.mostra_msg_lista_vuota()
            return

        # Funzione di eliminazione per gli spettacoli
        def on_conferma(widget_spettacolo: SpettacoloDisplay, id_: int) -> None:
            """Prova ad eliminare l'istanza di Spettacolo.

            :param widget_spettacolo: widget associato allo `Spettacolo` da eliminare
            :param id\\_: id dello spettacolo da eliminare
            """
            try:
                self.__elimina_spettacolo(id_)
            except OggettoInUsoException as exc:
                widget_spettacolo.annulla_elimina()
                mostra_error_popup(self._view_section, "Spettacolo in uso", str(exc))
            else:
                self._view_section.aggiorna_pagina()

        # Mostra tutti gli spettacoli della lista a schermo
        for spettacolo in lista_spettacoli:
            # Verifica che classe di Spettacolo è l'istanza
            dati: tuple[str, ...] = ()
            if isinstance(spettacolo, Regia):
                if opera_associata := self._model.get_opera(spettacolo.get_id_opera()):
                    dati = (opera_associata.get_compositore(), spettacolo.get_regista())
            else:
                ...  # Nel caso ci siano altri sottoclassi di Spettacolo
            current_spettacolo = SpettacoloDisplay(spettacolo, dati)

            current_spettacolo.visualizzaRequest.connect(  # type:ignore
                self.__visualizza_spettacolo
            )

            current_spettacolo.modificaRequest.connect(  # type:ignore
                self.__modifica_spettacolo
            )

            current_spettacolo.eliminaConfermata.connect(  # type:ignore
                partial(on_conferma, current_spettacolo, spettacolo.get_id())
            )

            layout_spettacoli.aggiungi_list_item(
                current_spettacolo, WidgetRole.Item.CARD
            )

    def __visualizza_spettacolo(self, id_: int) -> None:
        """Carica la pagina `VisualizzaSpettacoloView` con i dati relativi allo spettacolo
        indicato.

        :param id\\_: id dello spettacolo da visualizzare
        """
        # Copia dello spettacolo da visualizzare
        current_spettacolo = self.__get_spettacolo(id_)
        if not current_spettacolo:
            mostra_error_popup(
                self._view_section,
                "Spettacolo inesistente",
                f"Non è presente nessuno spettacolo con id {id_}.",
            )
            return

        # Ottieni la pagina VisualizzaSpettacoloView
        from view.spettacoli.pagine import VisualizzaSpettacoloView

        pagina_nome = Pagina.VISUALIZZA_SPETTACOLO
        try:
            pagina: VisualizzaSpettacoloView = self._ottieni_pagina(  # type:ignore
                pagina_nome, VisualizzaSpettacoloView
            )
        except TypeError:
            return

        if isinstance(current_spettacolo, Regia):
            spettacolo_data = RegiaData(
                id=current_spettacolo.get_id(),
                titolo=current_spettacolo.get_titolo(),
                note=current_spettacolo.get_note(),
                interpreti=current_spettacolo.get_interpreti(),
                musicisti_e_direttori_artistici=current_spettacolo.get_musicisti_e_direttori_artistici(),
                regista=current_spettacolo.get_regista(),
                anno_produzione=current_spettacolo.get_anno_produzione(),
                id_opera=current_spettacolo.get_id_opera(),
            )
        else:  # Caso Spettacolo generico
            spettacolo_data = SpettacoloData(
                id=current_spettacolo.get_id(),
                titolo=current_spettacolo.get_titolo(),
                note=current_spettacolo.get_note(),
                interpreti=current_spettacolo.get_interpreti(),
                musicisti_e_direttori_artistici=current_spettacolo.get_musicisti_e_direttori_artistici(),
            )

        pagina.set_data(spettacolo_data)

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)

    def __nuovo_spettacolo(self) -> None:
        """Carica la pagina `NuovoSpettacoloView`, dove l'utente può inserire i dati
        necessari per creare uno spettacolo."""
        # Ottieni la pagina NuovoSpettacoloView
        from view.spettacoli.pagine import NuovoSpettacoloView

        pagina_nome = Pagina.NUOVO_SPETTACOLO
        try:
            pagina: NuovoSpettacoloView = self._ottieni_pagina(  # type:ignore
                pagina_nome, NuovoSpettacoloView
            )
        except TypeError:
            return

        # Setup pagina pulendo i campi
        pagina.reset_pagina()

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)

    def __modifica_spettacolo(self, id_: int) -> None:
        """Carica la pagina `ModificaSpettacoloView`, con i dati dello spettacolo indicato
        inseriti nei campo di input.

        :param id_: id dello spettacolo da modificare
        """
        # Copia dello spettacolo da modificare
        current_spettacolo = self.__get_spettacolo(id_)
        if not current_spettacolo:
            mostra_error_popup(
                self._view_section,
                "Spettacolo inesistente",
                f"Non è presente nessuno spettacolo con id {id_}.",
            )
            return

        # Ottieni la pagina ModificaSpettacoloView
        from view.spettacoli.pagine import ModificaSpettacoloView

        pagina_nome = Pagina.MODIFICA_SPETTACOLO
        try:
            pagina: ModificaSpettacoloView = self._ottieni_pagina(  # type:ignore
                pagina_nome, ModificaSpettacoloView
            )
        except TypeError:
            return

        # Salva i dati dentro di un container
        if isinstance(current_spettacolo, Regia):
            spettacolo_data = RegiaData(
                id=current_spettacolo.get_id(),
                titolo=current_spettacolo.get_titolo(),
                note=current_spettacolo.get_note(),
                interpreti=current_spettacolo.get_interpreti(),
                musicisti_e_direttori_artistici=current_spettacolo.get_musicisti_e_direttori_artistici(),
                regista=current_spettacolo.get_regista(),
                anno_produzione=current_spettacolo.get_anno_produzione(),
                id_opera=current_spettacolo.get_id_opera(),
            )
        else:
            spettacolo_data = SpettacoloData(
                id=current_spettacolo.get_id(),
                titolo=current_spettacolo.get_titolo(),
                note=current_spettacolo.get_note(),
                interpreti=current_spettacolo.get_interpreti(),
                musicisti_e_direttori_artistici=current_spettacolo.get_musicisti_e_direttori_artistici(),
            )

        pagina.set_data(spettacolo_data)

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)
