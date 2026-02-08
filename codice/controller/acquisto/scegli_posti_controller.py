from typing import Optional, override

from core.controller import AbstractVisualizzaController


from model.model import Model
from model.organizzazione.evento import Evento
from model.organizzazione.sezione import Sezione
from model.organizzazione.posto import Posto

from view.acquisto.pagine import ScegliPostiView


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
            self.__setup_posto_combobox
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __get_eventi_by_spettacolo(self, id_: int) -> list[Evento]:
        return self._model.get_eventi_by_spettacolo(id_)

    def __get_sezioni_disponibili_by_evento(
        self, id_: int
    ) -> list[Sezione]: ...  # - DA IMPLEMENTAR NEL MODEL

    def __get_posti_disponibili_by_sezione_ed_evento(
        self, id_sezione: int, id_evento: int
    ) -> list[Posto]: ...  # - DA IMPLEMENTAR NEL MODEL

    def __setup_evento_combobox(self, id_spettacolo: int) -> None:
        """Riempisce il `QComboBox` degli eventi della pagina."""
        self._view_page.evento.clear()

        lista_eventi = self.__get_eventi_by_spettacolo(id_spettacolo)

        self._view_page.evento.insertItem(0, "Scegliere evento...", -1)
        for i, e in enumerate(lista_eventi, start=1):
            self._view_page.evento.insertItem(
                i, e.get_data_ora().strftime("%d/%m/%y - %H:%M"), e.get_id()
            )

    def __setup_sezione_combobox(self, id_evento: int) -> None:
        self._view_page.sezione.clear()
        self._view_page.sezione.setEnabled(True)
        self._view_page.fila.setEnabled(False)
        self._view_page.numero.setEnabled(False)

        lista_sezioni = self.__get_sezioni_disponibili_by_evento(id_evento)
        if not lista_sezioni:
            self._view_page.sezione.setEnabled(False)
            return

        self._view_page.sezione.insertItem(0, "Scegliere sezione...", -1)
        for i, sezione in enumerate(lista_sezioni, start=1):
            self._view_page.sezione.insertItem(i, sezione.get_nome(), sezione.get_id())

    def __setup_fila_combobox(self, id_sezione: int, id_evento: int) -> None:
        self._view_page.fila.clear()
        self._view_page.numero.clear()
        self._view_page.fila.setEnabled(True)
        self._view_page.numero.setEnabled(False)

        self.__lista_posti = self.__get_posti_disponibili_by_sezione_ed_evento(
            id_sezione, id_evento
        )
        if not self.__lista_posti:
            self._view_page.fila.setEnabled(False)
            return

        self._view_page.fila.insertItem(0, "Scegliere fila...", None)
        for i, posto in enumerate(self.__lista_posti, start=1):
            if self._view_page.sezione.findText(posto.get_fila()) < 0:
                self._view_page.sezione.insertItem(
                    i, posto.get_fila(), posto.get_fila()
                )  # Salva il nome della fila come data

    def __setup_posto_combobox(self, txt_fila: Optional[str]) -> None:
        self._view_page.numero.clear()
        self._view_page.numero.setEnabled(True)

        posti = [p for p in self.__lista_posti if p.get_fila() == txt_fila]
        if not posti:
            self._view_page.numero.setEnabled(False)
            return

        self._view_page.numero.insertItem(0, "Scegliere numero...", -1)
        for i, posto in enumerate(posti, start=1):
            if self._view_page.numero.findData(posto.get_id()) < 0:
                self._view_page.numero.insertItem(
                    i, str(posto.get_numero()), posto.get_id()
                )
