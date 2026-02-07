from PyQt6.QtWidgets import QWidget
from functools import partial
from typing import Optional, override

from core.controller import AbstractVisualizzaController

from controller.navigation import Pagina

from model.model import Model
from model.pianificazione.spettacolo import Spettacolo
from model.organizzazione.evento import Evento
from model.exceptions import OggettoInUsoException

from view.spettacoli.pagine import VisualizzaSpettacoloView
from view.spettacoli.widgets import EventoDisplay
from view.spettacoli.utils import EventoPageData

from view.utils.list_widgets import ListLayout
from view.utils import PopupMessage


class VisualizzaSpettacoloController(AbstractVisualizzaController):
    """Gestice la pagina `VisualizzaSpettacoloView` dell'app.

    Segnali
    ---
    - `goBackRequest()`: emesso per tornare alla pagina `SpettacoliSectionView`.
    """

    _view_page: VisualizzaSpettacoloView

    def __init__(self, model: Model, spettacolo_v: VisualizzaSpettacoloView):
        if type(spettacolo_v) is not VisualizzaSpettacoloView:
            raise TypeError("Atteso VisualizzaSpettacoloView per spettacolo_v.")

        super().__init__(model, spettacolo_v)

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    @override
    def _connect_signals(self) -> None:
        super()._connect_signals()

        self._view_page.displayEventiRequest.connect(  # type:ignore
            self.__display_eventi
        )

        self._view_page.nuovoEventoRequest.connect(  # type:ignore
            self.__nuovo_evento
        )

        self._view_page.visualizzaPrezziRequest.connect(  # type:ignore
            self.__visualizza_prezzi_associati
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __get_spettacolo(self, id_: int) -> Optional[Spettacolo]:
        return self._model.get_spettacolo(id_)

    def __get_evento(self, id_: int) -> Optional[Evento]:
        return self._model.get_evento(id_)

    def __get_eventi_by_spettacolo(self, id_: int) -> list[Evento]:
        return self._model.get_eventi_by_spettacolo(id_)

    def __elimina_evento(self, id_: int) -> None:
        self._model.elimina_evento(id_)

    def __visualizza_prezzi_associati(self, id_spettacolo: int) -> None:
        """Carica la pagina `PrezziAssociatiView` con i dati relativi allo spettacolo
        indicato.

        :param id\\_: id dello spettacolo da visualizzare
        """
        # Copia dello spettacolo da visualizzare
        current_spettacolo = self.__get_spettacolo(id_spettacolo)
        if not current_spettacolo:
            PopupMessage.mostra_errore(
                self._view_page,
                "Spettacolo inesistente",
                f"Non è presente nessuno spettacolo con id {id_spettacolo}.",
            )
            return

        # Ottieni la pagina PrezziAssociatiView
        from view.spettacoli.pagine import PrezziAssociatiView

        pagina_nome = Pagina.PREZZI_ASSOCIATI
        current_pagina = self._ottieni_pagina(pagina_nome)
        if type(current_pagina) is not PrezziAssociatiView:
            self._mostra_msg_pagina_non_trovata(pagina_nome, type(current_pagina))
            return

        current_pagina.set_data(current_spettacolo.get_id())

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)

    def __display_eventi(self, layout_eventi: ListLayout) -> None:
        """Mostra a schermo le informazioni degli eventi salvati e associati ad
        uno spettacolo ed assegna a ciascuno dei pulsanti per modificarli o eliminarli.

        :param layout_eventi: layout dove saranno caricate tutti le regie
        """
        lista_eventi = self.__get_eventi_by_spettacolo(
            self._view_page.id_current_spettacolo
        )

        # Verifica che la lista non sia vuota
        if not lista_eventi:
            layout_eventi.mostra_msg_lista_vuota()
            return

        lista_eventi = sorted(lista_eventi, key=lambda x: (x.get_data_ora()))

        # Funzione di eliminazione per gli eventi
        def on_conferma(widget_evento: EventoDisplay, id_: int) -> None:
            """Prova ad eliminare l'istanza di Evento.

            :param widget_evento: widget associato all'Evento` da eliminare
            :param id\\_: id dell'evento da eliminare
            """
            try:
                self.__elimina_evento(id_)
            except OggettoInUsoException as exc:
                widget_evento.annulla_elimina()
                PopupMessage.mostra_errore(
                    self._view_page,
                    "Evento in uso",
                    f"Si è verificato un errore: {exc}",
                )
            else:
                self._view_page.aggiorna_pagina()

        for evento in lista_eventi:
            current_evento = EventoDisplay(evento)

            current_evento.modificaRequest.connect(  # type:ignore
                self.__modifica_evento
            )

            current_evento.eliminaConfermata.connect(  # type:ignore
                partial(on_conferma, current_evento, evento.get_id())
            )

            layout_eventi.aggiungi_list_item(current_evento)

    def __nuovo_evento(self) -> None:
        """Carica la pagina `NuovoEventoView`, dove l'utente può inserire i dati
        necessari per creare un evento."""
        # Ottieni la pagina NuovoEventoView
        from view.spettacoli.pagine import NuovoEventoView

        cur_pagina_dict: dict[str, Optional[QWidget]] = {"value": None}
        pagina_nome = Pagina.NUOVO_EVENTO
        self.getPageRequest.emit(pagina_nome, cur_pagina_dict)
        current_pagina: Optional[QWidget] = cur_pagina_dict.get("value")

        if type(current_pagina) is not NuovoEventoView:
            PopupMessage.mostra_errore(
                self._view_page,
                "Pagina non trovata",
                f"Si è verificato un errore: Non è stato trovata la pagina '{pagina_nome}'. "
                + f"Type trovato: {type(current_pagina)}",
            )
            return

        # Setup pagina pulendo i campi
        current_pagina.reset_pagina()
        current_pagina.id_spettacolo = self._view_page.id_current_spettacolo

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)

    def __modifica_evento(self, id_: int) -> None:
        """Carica la pagina `ModificaEventoView`, con i dati del evento indicato
        inseriti nei campo di input.

        :param id_: id del evento da modificare
        """
        # Copia del evento da modificare
        current_evento = self.__get_evento(id_)
        if not current_evento:
            PopupMessage.mostra_errore(
                self._view_page,
                "Evento inesistente",
                f"Non è presente nessun evento con id {id_}.",
            )
            return

        # Ottieni la pagina ModificaEventoView
        from view.spettacoli.pagine import ModificaEventoView

        cur_pagina_dict: dict[str, Optional[QWidget]] = {"value": None}
        pagina_nome = Pagina.MODIFICA_EVENTO
        self.getPageRequest.emit(pagina_nome, cur_pagina_dict)
        current_pagina: Optional[QWidget] = cur_pagina_dict.get("value")

        if type(current_pagina) is not ModificaEventoView:
            PopupMessage.mostra_errore(
                self._view_page,
                "Pagina non trovata",
                f"Si è verificato un errore: Non è stato trovata la pagina '{pagina_nome}'. "
                + f"Type trovato: {type(current_pagina)}",
            )
            return

        # Salva i dati dentro di un container
        evento_data = EventoPageData(
            id=current_evento.get_id(),
            data_ora=current_evento.get_data_ora(),
            id_spettacolo=current_evento.get_id_spettacolo(),
        )

        # Setup pagina con i data dell'evento
        current_pagina.set_data(evento_data)

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)
