from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal, QObject
from functools import partial
from typing import Optional, override

from core.controller import AbstractVisualizzaController


from model.model import Model
from model.organizzazione.evento import Evento
from model.organizzazione.sezione import Sezione
from model.organizzazione.posto import Posto

from view.acquisto.pagine import ScegliPostiView

from view.utils.list_widgets import ListLayout
from view.utils import PopupMessage


class ScegliPostiController(AbstractVisualizzaController):
    """# - CORREGIR"""

    _view_page: ScegliPostiView

    def __init__(self, model: Model, scegli_posti_v: ScegliPostiView):
        if type(scegli_posti_v) is not ScegliPostiView:
            raise TypeError("Atteso ScegliPostiView per scegli_posti_v.")

        super().__init__(model, scegli_posti_v)

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    @override
    def _connect_signals(self) -> None:
        super()._connect_signals()

        self._view_page.getSezioniPostiRequest.connect(  # type:ignore
            self.__carica_sezione_e_posti_data
        )

        self._view_page.sezione.currentIndexChanged.connect(  # type:ignore
            lambda: self.__setup_fila_combobox(self._view_page.sezione.currentData())
        )

        self._view_page.fila.currentIndexChanged.connect(  # type:ignore
            lambda: self.__setup_posto_combobox(self._view_page.sezione.currentData())
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __get_sezioni_e_file_e_posti_disponibili(self, id_evento: int):
        if id_evento == -1:
            return None
        return self._model.get_sezioni_e_file_e_posti_disponibili(id_evento)

    def __carica_sezione_e_posti_data(self, id_evento: int) -> None:
        couple = self.__get_sezioni_e_file_e_posti_disponibili(id_evento)
        self.setup_sezione_combobox(couple)

    def setup_sezione_combobox(
        self,
        sezioni_file_e_posti: Optional[
            list[tuple[Sezione, list[tuple[str, list[Posto]]]]]
        ],
    ) -> None:
        self.__lista_sezioni_file_e_posti = sezioni_file_e_posti

        self._view_page.sezione.clear()

        if (
            self.__lista_sezioni_file_e_posti is None
            or not self.__lista_sezioni_file_e_posti
        ):
            return

        self._view_page.sezione.insertItem(0, "Scegliere sezione...", -1)
        for i, couple in enumerate(self.__lista_sezioni_file_e_posti, start=1):
            s, fila_posti = couple
            self._view_page.sezione.insertItem(i, s.get_nome(), s.get_id())

    def __setup_fila_combobox(self, id_sezione: int) -> None:
        self._view_page.fila.clear()

        if id_sezione == -1:
            return

        self._view_page.fila.insertItem(0, "Scegliere fila...", -1)
        for s, fila_posti in self.__lista_sezioni_file_e_posti:
            if s.get_id() != id_sezione:
                continue

            for i, couple in enumerate(fila_posti, start=1):
                f, posti = couple
                self._view_page.fila.insertItem(i, f, f)
                print(f)

    def __setup_posto_combobox(self, nome_fila: str | int) -> None:
        self._view_page.numero.clear()

        if nome_fila == -1:
            return

        self._view_page.numero.insertItem(0, "Scegliere posto...", -1)
        for s, fila_posti in self.__lista_sezioni_file_e_posti:
            for f, posti in fila_posti:
                if f != nome_fila:
                    continue

                for i, p in enumerate(posti, start=1):
                    self._view_page.numero.insertItem(
                        i, str(p.get_numero()), p.get_id()
                    )
