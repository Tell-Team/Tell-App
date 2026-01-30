from functools import partial
from typing import Optional

from core.controller import AbstractSectionController

from controller.navigation import Pagina

from model.model import Model

from view.teatro.pagine import TeatroSectionView

from view.utils.list_widgets import ListLayout


class TeatroSectionController(AbstractSectionController):
    """Gestice la sezione Teatro (`TeatroSectionView`) dell'app."""

    _view_section: TeatroSectionView

    def __init__(self, model: Model, teatro_s: TeatroSectionView):
        if type(teatro_s) is not TeatroSectionView:
            raise TypeError("Atteso TeatroSectionView per info_s.")

        super().__init__(model, teatro_s)

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    def _connect_signals(self) -> None:
        super()._connect_signals()

        # Display delle istanze del model
        self._view_section.displaySezioniRequest.connect(  # type:ignore
            self.__display_sezioni
        )
        self._view_section.displayPostiRequest.connect(  # type:ignore
            self.__display_posti
        )

        # Setup delle pagine di creazione
        self._view_section.nuovaSezioneRequest.connect(  # type:ignore
            self.__nuova_sezione
        )
        self._view_section.nuovoPostoRequest.connect(  # type:ignore
            self.__nuovo_posto
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __display_sezioni(self, layout_sezioni: ListLayout) -> None: ...

    def __display_posti(self, layout_posti: ListLayout) -> None: ...

    def __nuova_sezione(self) -> None: ...

    def __nuovo_posto(self) -> None: ...
