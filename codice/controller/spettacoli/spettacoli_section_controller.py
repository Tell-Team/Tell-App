from PyQt6.QtWidgets import QWidget
from functools import partial
from typing import Optional

from core.controller import AbstractSectionController

from controller.navigation import Pagina

from model.model import Model
from model.pianificazione.spettacolo import Spettacolo
from model.pianificazione.regia import Regia
from model.exceptions import OggettoInUsoException

from view.spettacoli.pagine import SpettacoliSectionView
from view.spettacoli.widgets import SpettacoloDisplay
from view.spettacoli.utils import SpettacoloPageData

from view.utils.list_widgets import ListLayout
from view.utils import PopupMessage
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
        ...
        # - self.__model.elimina_spettacolo(id_)

    def __display_spettacoli(self, layout_spettacoli: ListLayout) -> None:
        """Mostra a schermo alcune informazioni degli spettacoli salvati ed assegna a
        ciascuno pulsanti per visualizzarli in dettaglio, scegliere posti, modificarli
        o eliminarli.

        :param layout: layout dove saranno caricati tutti gli spettacoli
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
            layout_spettacoli.if_lista_vuota()
            return

        # Funzione di elimina per gli spettacoli
        def on_conferma(widget_spettacolo: SpettacoloDisplay, id_: int) -> None:
            """Prova di eliminare l'istanza di spettacolo.

            :param id_: id dello spettacolo da eliminare
            """
            try:
                self.__elimina_spettacolo(id_)
            except OggettoInUsoException as exc:
                widget_spettacolo.annulla_elimina()
                PopupMessage.mostra_errore(
                    self._view_section,
                    "Spettacolo in uso",
                    f"Si è verificato un errore: {exc}",
                )
            else:
                self._view_section.aggiorna_pagina()

        # Mostra tutti gli spettacoli della lista a schermo
        for spettacolo in lista_spettacoli:
            # Verifica che classe di Spettacolo è l'istanza
            if isinstance(spettacolo, Regia):
                compositore: str = ""
                if cur_opera := self._model.get_opera(spettacolo.get_id_opera()):
                    compositore = cur_opera.get_compositore()
                dati = (compositore, spettacolo.get_regista())
                cur_spettacolo = SpettacoloDisplay(
                    spettacolo,
                    dati=dati,
                )
            else:
                cur_spettacolo = SpettacoloDisplay(spettacolo)

            # Setup della pagina di visualizzazione delgli spettacoli
            cur_spettacolo.visualizzaRequest.connect(  # type:ignore
                self.__visualizza_spettacolo
            )

            # Setup della pagina di modifica degli spettacoli
            cur_spettacolo.modificaRequest.connect(  # type:ignore
                self.__modifica_spettacolo
            )

            cur_spettacolo.eliminaConfermata.connect(  # type:ignore
                partial(on_conferma, cur_spettacolo, spettacolo.get_id())
            )

            # Aggiungi cur_spettacolo al layout di ListaSpettacoli
            layout_spettacoli.aggiungi_list_item(cur_spettacolo, WidgetRole.ITEM_CARD)

    def __visualizza_spettacolo(self, id_: int) -> None: ...

    def __nuovo_spettacolo(self) -> None:
        """Carica la pagina `NuovoSpettacoloView`, dove l'utente può inserire i dati
        necessari per creare uno spettacolo."""
        # Ottieni la pagina NuovoSpettacoloView
        from view.spettacoli.pagine import NuovoSpettacoloView

        cur_pagina_dict: dict[str, Optional[QWidget]] = {"value": None}
        pagina_nome = Pagina.NUOVO_SPETTACOLO
        self.getPageRequest.emit(pagina_nome, cur_pagina_dict)
        cur_pagina: Optional[QWidget] = cur_pagina_dict.get("value")

        if type(cur_pagina) is not NuovoSpettacoloView:
            PopupMessage.mostra_errore(
                self._view_section,
                "Pagina non trovata",
                f"Si è verificato un errore: Non è stato trovata la pagina '{pagina_nome}'. "
                + f"Type trovato: {type(cur_pagina)}",
            )
            return

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)

    def __modifica_spettacolo(self, id_: int) -> None:
        """Carica la pagina `ModificaSpettacoloView`, con i dati dello spettacolo indicato
        inseriti nei campo di input.

        :param id_: id dello spettacolo da modificare
        """
        # Copia dello spettacolo da modificare
        cur_spettacolo = self.__get_spettacolo(id_)
        if not cur_spettacolo:
            PopupMessage.mostra_errore(
                self._view_section,
                "Spettacolo inesistente",
                f"Non è presente nessuno spettacolo con id {id_}.",
            )
            return

        # Ottieni la pagina ModificaSpettacoloView
        from view.spettacoli.pagine import ModificaSpettacoloView

        cur_pagina_dict: dict[str, Optional[QWidget]] = {"value": None}
        pagina_nome = Pagina.MODIFICA_SPETTACOLO
        self.getPageRequest.emit(pagina_nome, cur_pagina_dict)
        cur_pagina: Optional[QWidget] = cur_pagina_dict.get("value")

        if type(cur_pagina) is not ModificaSpettacoloView:
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
            tipo_spettacolo: str = ""
            if cur_opera := self._model.get_opera(cur_spettacolo.get_id_opera()):
                tipo_spettacolo = (
                    "**Questo spettacolo è una Regia associata "
                    + f'all\'opera "{cur_opera.get_nome()}".**'
                )
            cur_pagina.set_data(spettacolo_data, tipo_spettacolo)
        else:
            cur_pagina.set_data(spettacolo_data)

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)
