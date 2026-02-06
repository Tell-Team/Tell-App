from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal, QObject
from functools import partial
from typing import Optional


from model.model import Model
from model.organizzazione.evento import Evento
from model.organizzazione.sezione import Sezione
from model.organizzazione.posto import Posto

from view.acquisto.pagine import ScegliPostiView

from view.utils.list_widgets import ListLayout
from view.utils import PopupMessage


class ScegliPostiController(QObject):
    """# - CORREGIR"""

    goBackRequest: pyqtSignal = pyqtSignal()

    def __init__(self, model: Model, scegli_posti_v: ScegliPostiView):
        super().__init__()
        self.__model = model
        self.__scegli_posti_view = scegli_posti_v

        self.__connect_signals()

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    def __connect_signals(self) -> None:
        self.__scegli_posti_view.tornaIndietroRequest.connect(  # type:ignore
            self.goBackRequest.emit
        )

        self.__scegli_posti_view.getSezioniPostiRequest.connect(  # type:ignore
            self.__carica_sezione_posto_comboboxes
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __get_sezioni_posti(self, id_evento: int) -> list[tuple[Sezione, list[Posto]]]:
        if id_evento == -1:
            return []
        lista: list[tuple[Sezione, list[Posto]]] = []
        sezioni = self.__model.get_sezioni()
        for s in sezioni:
            posti = self.__model.get_posti_by_sezione(s.get_id())
            lista.append((s, posti))
        return lista

    def __carica_sezione_posto_comboboxes(self, id_evento: int) -> None:
        couple = self.__get_sezioni_posti(id_evento)
        self.__scegli_posti_view.setup_sezione_combobox(couple)

    # def __display_eventi(self, layout_eventi: ListLayout) -> None:
    #     """Mostra a schermo le informazioni degli eventi salvati e associati ad
    #     uno spettacolo ed assegna a ciascuno dei pulsanti per modificarli o eliminarli.

    #     :param layout_eventi: layout dove saranno caricate tutti le regie
    #     """
    #     lista_eventi = self.__get_eventi_by_spettacolo(
    #         self.__scegli_posti_view.id_current_spettacolo
    #     )

    #     # Verifica che la lista non sia vuota
    #     if not lista_eventi:
    #         layout_eventi.mostra_msg_lista_vuota()
    #         return

    #     # Funzione di eliminazione per gli eventi
    #     def on_conferma(widget_evento: EventoDisplay, id_: int) -> None:
    #         """Prova ad eliminare l'istanza di Evento.

    #         :param widget_evento: widget associato all'Evento` da eliminare
    #         :param id_: id dell'evento da eliminare
    #         """
    #         try:
    #             self.__elimina_evento(id_)
    #         except OggettoInUsoException as exc:
    #             widget_evento.annulla_elimina()
    #             PopupMessage.mostra_errore(
    #                 self.__scegli_posti_view,
    #                 "Evento in uso",
    #                 f"Si è verificato un errore: {exc}",
    #             )
    #         else:
    #             self.__scegli_posti_view.aggiorna_pagina()

    #     for evento in lista_eventi:
    #         current_evento = EventoDisplay(evento)

    #         current_evento.modificaRequest.connect(  # type:ignore
    #             self.__modifica_evento
    #         )

    #         current_evento.eliminaConfermata.connect(  # type:ignore
    #             partial(on_conferma, current_evento, evento.get_id())
    #         )

    #         layout_eventi.aggiungi_list_item(current_evento)

    # def __nuovo_evento(self) -> None:
    #     """Carica la pagina `NuovoEventoView`, dove l'utente può inserire i dati
    #     necessari per creare un evento."""
    #     # Ottieni la pagina NuovoEventoView
    #     from view.spettacoli.pagine import NuovoEventoView

    #     cur_pagina_dict: dict[str, Optional[QWidget]] = {"value": None}
    #     pagina_nome = Pagina.NUOVO_EVENTO
    #     self.getPageRequest.emit(pagina_nome, cur_pagina_dict)
    #     current_pagina: Optional[QWidget] = cur_pagina_dict.get("value")

    #     if type(current_pagina) is not NuovoEventoView:
    #         PopupMessage.mostra_errore(
    #             self.__scegli_posti_view,
    #             "Pagina non trovata",
    #             f"Si è verificato un errore: Non è stato trovata la pagina '{pagina_nome}'. "
    #             + f"Type trovato: {type(current_pagina)}",
    #         )
    #         return

    #     # Setup pagina pulendo i campi
    #     current_pagina.reset_pagina()
    #     current_pagina.id_spettacolo = self.__scegli_posti_view.id_current_spettacolo

    #     # Apri la pagina
    #     self.goToPageRequest.emit(pagina_nome, True)

    # def __modifica_evento(self, id_: int) -> None:
    #     """Carica la pagina `ModificaEventoView`, con i dati del evento indicato
    #     inseriti nei campo di input.

    #     :param id_: id del evento da modificare
    #     """
    #     # Copia del evento da modificare
    #     current_evento = self.__get_evento(id_)
    #     if not current_evento:
    #         PopupMessage.mostra_errore(
    #             self.__scegli_posti_view,
    #             "Evento inesistente",
    #             f"Non è presente nessun evento con id {id_}.",
    #         )
    #         return

    #     # Ottieni la pagina ModificaEventoView
    #     from view.spettacoli.pagine import ModificaEventoView

    #     cur_pagina_dict: dict[str, Optional[QWidget]] = {"value": None}
    #     pagina_nome = Pagina.MODIFICA_EVENTO
    #     self.getPageRequest.emit(pagina_nome, cur_pagina_dict)
    #     current_pagina: Optional[QWidget] = cur_pagina_dict.get("value")

    #     if type(current_pagina) is not ModificaEventoView:
    #         PopupMessage.mostra_errore(
    #             self.__scegli_posti_view,
    #             "Pagina non trovata",
    #             f"Si è verificato un errore: Non è stato trovata la pagina '{pagina_nome}'. "
    #             + f"Type trovato: {type(current_pagina)}",
    #         )
    #         return

    #     # Salva i dati dentro di un container
    #     evento_data = EventoPageData(
    #         id=current_evento.get_id(),
    #         data_ora=current_evento.get_data_ora(),
    #         id_spettacolo=current_evento.get_id_spettacolo(),
    #     )

    #     # Setup pagina con i data del genere
    #     current_pagina.set_data(evento_data)

    #     # Apri la pagina
    #     self.goToPageRequest.emit(pagina_nome, True)
