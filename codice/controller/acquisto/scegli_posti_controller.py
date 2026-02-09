from PyQt6.QtWidgets import QWidget
from collections import defaultdict
from typing import Optional, override

from core.controller import AbstractVisualizzaController

from controller.navigation import Pagina

from model.model import Model
from model.organizzazione.evento import Evento
from model.organizzazione.sezione import Sezione
from model.organizzazione.posto import Posto
from model.exceptions import IdInesistenteException

from view.acquisto.pagine import ScegliPostiView
from view.acquisto.widgets import PostoSceltoDisplay

from view.utils.list_widgets import ListLayout

from view.utils import PopupMessage


class ScegliPostiController(AbstractVisualizzaController):
    """Gestice la pagina `ScegliPostiView` dell'app."""

    _view_page: ScegliPostiView

    def __init__(self, model: Model, scegli_posti_v: ScegliPostiView):
        if type(scegli_posti_v) is not ScegliPostiView:
            raise TypeError("Atteso ScegliPostiView per scegli_posti_v.")

        super().__init__(model, scegli_posti_v)

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    @override
    def _connect_signals(self) -> None:
        super()._connect_signals()

        self._view_page.setupEventoCombobox.connect(  # type:ignore
            self.__setup_evento_combobox
        )

        self._view_page.setupSezioneCombobox.connect(  # type:ignore
            self.__setup_sezione_combobox
        )

        self._view_page.setupFilaCombobox.connect(  # type:ignore
            self.__setup_fila_combobox
        )

        self._view_page.setupPostoCombobox.connect(  # type:ignore
            self.__setup_numero_posto_combobox
        )

        self._view_page.aggiungiPostoScelto.connect(  # type:ignore
            self.__aggiungi_posto_scelto
        )

        self._view_page.displayPostiSceltiRequest.connect(  # type:ignore
            self.__display_posti_scelti
        )

        self._view_page.iniziaCreazionePrenotazione.connect(  # type:ignore
            self.__inizia_creazione_prenotazione
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __get_evento(self, id_: int) -> Optional[Evento]:
        return self._model.get_evento(id_)

    def __get_eventi_by_spettacolo(self, id_: int) -> list[Evento]:
        return self._model.get_eventi_by_spettacolo(id_)

    def __get_sezione(self, id_: int) -> Optional[Sezione]:
        return self._model.get_sezione(id_)

    def __get_sezioni_e_file_e_posti_disponibili(self, id_evento: int):
        # -> list[tuple[Sezione, list[tuple[str, list[Posto]]]]]
        return self._model.get_sezioni_e_file_e_posti_disponibili(id_evento)

    def __get_posto(self, id_: int) -> Optional[Posto]:
        return self._model.get_posto(id_)

    def __setup_evento_combobox(self, id_spettacolo: int) -> None:
        """Riempisce il `QComboBox` degli eventi della pagina.

        :param id_spettacolo: id dello spettacolo per cui si vuole far una prenotazione
        """
        self._view_page.evento.clear()

        self.__eventi = self.__get_eventi_by_spettacolo(id_spettacolo)

        self._view_page.evento.insertItem(0, "Scegliere evento...", -1)
        for i, e in enumerate(self.__eventi, start=1):
            self._view_page.evento.insertItem(
                i, e.get_data_ora().strftime("%d/%m/%y - %H:%M"), e.get_id()
            )

    def __setup_sezione_combobox(self, id_evento: int) -> None:
        """Riempisce il `QComboBox` delle sezioni della pagina.

        :param id_evento: id dell'evento per cui si vuole prendere posti"""
        self._view_page.sezione.clear()
        self._view_page.sezione.setEnabled(True)
        self._view_page.fila.setEnabled(False)
        self._view_page.numero.setEnabled(False)

        try:
            self.__lista_completa = self.__get_sezioni_e_file_e_posti_disponibili(
                id_evento
            )
        except IdInesistenteException:
            self.__lista_completa = []

        self.__sezioni = [s for s, _ in self.__lista_completa]
        if not self.__sezioni:
            self._view_page.sezione.setEnabled(False)
            return
        self.__sezioni = sorted(self.__sezioni, key=lambda x: x.get_nome())

        self._view_page.sezione.insertItem(0, "Scegliere sezione...", -1)
        for i, sezione in enumerate(self.__sezioni, start=1):
            self._view_page.sezione.insertItem(i, sezione.get_nome(), sezione.get_id())

    def __setup_fila_combobox(self, id_sezione: int) -> None:
        """Riempisce il `QComboBox` delle file della pagina.

        :param id_sezione: id della sezione da è posizionato il posto da scegliere"""
        self._view_page.fila.clear()
        self._view_page.fila.setEnabled(True)
        self._view_page.numero.setEnabled(False)

        self.__lista_fila_posti = next(
            (fp for s, fp in self.__lista_completa if s.get_id() == id_sezione), None
        )
        if not self.__lista_fila_posti:
            self._view_page.fila.setEnabled(False)
            return
        self.__lista_fila_posti = sorted(self.__lista_fila_posti, key=lambda x: (x[0]))

        self._view_page.fila.insertItem(0, "Scegliere fila...", None)
        for i, couple in enumerate(self.__lista_fila_posti, start=1):
            fila, _ = couple
            if self._view_page.fila.findText(fila) < 0:
                self._view_page.fila.insertItem(i, fila, fila)
                # Salva il nome della fila come data

    def __setup_numero_posto_combobox(self, txt_fila: Optional[str]) -> None:
        """Riempisce il `QComboBox` dei posti della pagina.

        :param txt_fila: nome della fila in cui si trova il posto"""
        self._view_page.numero.clear()
        self._view_page.numero.insertItem(0, "", -1)
        self._view_page.numero.setEnabled(True)

        assert self.__lista_fila_posti is not None
        self.__posti = next(
            (p for f, p in self.__lista_fila_posti if f == txt_fila), None
        )
        if not self.__posti:
            self._view_page.numero.setEnabled(False)
            return
        self.__posti = sorted(self.__posti, key=lambda x: x.get_numero())

        self._view_page.numero.setItemText(0, "Scegliere numero...")
        for i, posto in enumerate(self.__posti, start=1):
            if self._view_page.numero.findData(posto.get_id()) < 0:
                self._view_page.numero.insertItem(
                    i, str(posto.get_numero()), posto.get_id()
                )

    def __aggiungi_posto_scelto(
        self, id_evento: int, id_sezione: int, id_posto: int
    ) -> None:
        # Verifica che tutti i campi sono compilati
        if id_evento == -1 or id_sezione == -1 or id_posto == -1:
            return

        evento = self.__get_evento(id_evento)
        assert isinstance(evento, Evento)

        sezione = self.__get_sezione(id_sezione)
        assert isinstance(sezione, Sezione)

        posto = self.__get_posto(id_posto)
        assert isinstance(posto, Posto)

        # Verifica che la tuple non è già presente nella lista
        if (evento, sezione, posto) in self._view_page.lista_posti_scelti:
            return
        self._view_page.lista_posti_scelti.append((evento, sezione, posto))
        # Ordina la lista per il display dei posti
        self._view_page.lista_posti_scelti = sorted(
            self._view_page.lista_posti_scelti,
            key=lambda x: (
                x[0].get_data_ora(),
                x[1].get_nome(),
                x[2].get_fila(),
                x[2].get_numero(),
            ),
        )
        self._view_page.aggiorna_pagina()

    def __display_posti_scelti(self, layout_posti_scelti: ListLayout) -> None:
        """Mostra a schermo le informazioni del posto da prenotare.

        :param layout_posti_scelti: layout dove saranno caricati tutti i posti scelti
        """
        pagina = self._view_page
        lista_posti_scelti = pagina.lista_posti_scelti

        if not lista_posti_scelti:
            layout_posti_scelti.mostra_msg_lista_vuota()
            return

        for e, s, p in lista_posti_scelti:
            current_posto_scelto = PostoSceltoDisplay(e, s, p)

            def elimina_posto_scelto(t: tuple[Evento, Sezione, Posto]) -> None:
                pagina.lista_posti_scelti.remove(t)
                pagina.aggiorna_pagina()

            current_posto_scelto.eliminaRequest.connect(  # type:ignore
                elimina_posto_scelto
            )

            layout_posti_scelti.aggiungi_list_item(current_posto_scelto)

    def __inizia_creazione_prenotazione(self) -> None:
        lista_posti_scelti = self._view_page.lista_posti_scelti

        tree: dict[Evento, dict[Sezione, set[Posto]]] = defaultdict(
            lambda: defaultdict(set)
        )

        for e, s, p in lista_posti_scelti:
            tree[e][s].add(p)

        from view.acquisto.pagine import RicevutaView

        cur_pagina_dict: dict[str, Optional[QWidget]] = {"value": None}
        pagina_nome = Pagina.RICEVUTA
        self.getPageRequest.emit(pagina_nome, cur_pagina_dict)
        current_pagina: Optional[QWidget] = cur_pagina_dict.get("value")

        if type(current_pagina) is not RicevutaView:
            PopupMessage.mostra_errore(
                self._view_page,
                "Pagina non trovata",
                f"Si è verificato un errore: Non è stato trovata la pagina '{pagina_nome}'. "
                + f"Type trovato: {type(current_pagina)}",
            )
            return
