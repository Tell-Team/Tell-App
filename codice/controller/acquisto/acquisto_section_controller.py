from PyQt6.QtWidgets import QWidget
from typing import Optional

from core.controller import AbstractSectionController

from controller.navigation import Pagina

from model.model import Model
from model.pianificazione.spettacolo import Spettacolo
from model.pianificazione.regia import Regia

from view.acquisto.pagine import AcquistoSectionView
from view.acquisto.widgets import AcquistoDisplay
from view.spettacoli.utils import SpettacoloPageData

from view.utils.list_widgets import ListLayout
from view.utils import PopupMessage
from view.style import WidgetRole

import copy  # - DA TOGLIERE: C'è una definizione che dovrebbe stare nel model


class AcquistoSectionController(AbstractSectionController):
    """Gestice la sezione Acquisto (`AcquistoSectionView`) dell'app."""

    _view_section: AcquistoSectionView

    def __init__(self, model: Model, acquisto_s: AcquistoSectionView):
        if type(acquisto_s) is not AcquistoSectionView:
            raise TypeError("Atteso AcquistoSectionView per acquisto_v.")

        super().__init__(model, acquisto_s)

        self._view_section.aggiorna_pagina()
        # Serve per aggiornare la pagina con i dati del model. Siccome questa è la prima pagina
        #   caricata nella MainWindow, non si chiama nessun metodo del NavigationController al
        #   momento di visualizzarla e non viene aggiornata automanticamente.

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    def _connect_signals(self) -> None:
        super()._connect_signals()

        # Display della Lista Spettacoli
        self._view_section.displaySpettacoliRequest.connect(  # type:ignore
            self.__display_spettacoli
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __get_spettacolo(self, id_: int) -> Optional[Spettacolo]:
        return self._model.get_spettacolo(id_)

    def __get_spettacoli_in_programa(self) -> list[Spettacolo]:
        return self._model.get_spettacoli_in_programma()

    def __get_spettacoli_by_titolo(self, titolo: str) -> list[Spettacolo]:
        return copy.deepcopy(  # - DA AGGIUNGERE AL MODEL
            list(
                filter(
                    lambda o: titolo.lower() in o.get_titolo().lower(),
                    self.__get_spettacoli_in_programa(),
                )
            )
        )

    def __display_spettacoli(self, layout_spettacoli: ListLayout) -> None:
        """Mostra a schermo alcune informazioni degli spettacoli salvati ed assegna a
        ciascuno pulsanti per visualizzarli in dettaglio, scegliere posti, modificarli
        o eliminarli.

        :param layout: layout dove saranno caricati tutti gli spettacoli
        """
        # Verifica se c'è un filtro di ricerca
        filtro = self._view_section.filtro_ricerca

        lista_spettacoli = (
            self.__get_spettacoli_in_programa()
            if not filtro
            else self.__get_spettacoli_by_titolo(filtro)
        )

        # Verifica che la lista non sia vuota
        if not lista_spettacoli:
            layout_spettacoli.if_lista_vuota()
            return

        # Mostra tutti gli spettacoli della lista a schermo
        for spettacolo in lista_spettacoli:
            # Verifica che classe di Spettacolo è l'istanza
            if isinstance(spettacolo, Regia):
                compositore: str = ""
                if cur_opera := self._model.get_opera(spettacolo.get_id_opera()):
                    compositore = cur_opera.get_compositore()
                dati = (compositore, spettacolo.get_regista())
                cur_spettacolo = AcquistoDisplay(
                    spettacolo,
                    dati=dati,
                )
            else:
                cur_spettacolo = AcquistoDisplay(spettacolo)

            cur_spettacolo.scegliPostoRequest.connect(  # type:ignore
                self.__scegli_posti
            )

            # - CREA UN DISPLAY PARA SPETTACOLI DISPONIBILI

            # Aggiungi cur_spettacolo al layout di ListaSpettacoli
            layout_spettacoli.aggiungi_list_item(cur_spettacolo, WidgetRole.ITEM_CARD)

    def __scegli_posti(self, id_: int) -> None:
        """Carica la pagina `ScegliPostiView`, dove l'utente può inserire i dati
        necessari per creare una prenotazione."""
        # Copia dello spettacolo per iniziare la prenotazione
        cur_spettacolo = self.__get_spettacolo(id_)
        if not cur_spettacolo:
            PopupMessage.mostra_errore(
                self._view_section,
                "Spettacolo inesistente",
                f"Non è presente nessuno spettacolo con id {id_}.",
            )
            return

        # Ottieni la pagina ModificaSpettacoloView
        from view.acquisto.pagine import ScegliPostiView

        cur_pagina_dict: dict[str, Optional[QWidget]] = {"value": None}
        pagina_nome = Pagina.SCEGLI_POSTI
        self.getPageRequest.emit(pagina_nome, cur_pagina_dict)
        cur_pagina: Optional[QWidget] = cur_pagina_dict.get("value")

        if type(cur_pagina) is not ScegliPostiView:
            PopupMessage.mostra_errore(
                self._view_section,
                "Pagina non trovata",
                f"Si è verificato un errore: Non è stato trovata la pagina '{pagina_nome}'. "
                + f"Type trovato: {type(cur_pagina)}",
            )
            return

        # Salva i dati dentro di un container
        spettacolo_data = SpettacoloPageData(
            id=cur_spettacolo.get_id(),
            titolo=cur_spettacolo.get_titolo(),
            note=cur_spettacolo.get_note(),
            interpreti=cur_spettacolo.get_interpreti(),
            tecnici=cur_spettacolo.get_tecnici(),
        )

        # Setup pagina con i data dello spettacolo
        if isinstance(cur_spettacolo, Regia):
            tipo_spettacolo: tuple[str, str] = ("", "")
            if cur_opera := self._model.get_opera(cur_spettacolo.get_id_opera()):
                compositore = cur_opera.get_compositore()
                regista = cur_spettacolo.get_regista()
                tipo_spettacolo = (compositore, regista)
            cur_pagina.set_data(spettacolo_data, tipo_spettacolo)
        else:
            cur_pagina.set_data(spettacolo_data)

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)
