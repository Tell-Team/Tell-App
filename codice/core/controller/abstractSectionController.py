from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal, QObject
from typing import Optional

from core.metaclasses import ABCQObjectMeta
from core.view import AbstractSectionView

from controller.navigation import Pagina

from model.model.model import Model

from view.utils import PopupMessage


class AbstractSectionController(QObject, metaclass=ABCQObjectMeta):
    """Classe astratta per la creazione di controller per gestire le sezioni dell'app.

    Segnali
    ---
    - `logoutRequest()`: emesso per eseguire la funzione di logout dall'`AppContext`;
    - `goToPageRequest(Pagina, bool)`: emesso per visualizzare un'altra pagina;
    - `goToSectionRequest(Pagina)`: emesso per visualizzare un'altra pagina, senza salvarla
    nell'history del `NavigationController`;
    - `getPageRequest(Pagina, dict)`: emesso per ottenere la pagina che vendrà visualizzata.
    """

    logoutRequest: pyqtSignal = pyqtSignal()
    goToPageRequest: pyqtSignal = pyqtSignal(Pagina, bool)
    goToSectionRequest: pyqtSignal = pyqtSignal(Pagina)
    getPageRequest: pyqtSignal = pyqtSignal(Pagina, dict)

    def __init__(self, model: Model, section: AbstractSectionView):
        super().__init__()
        self._model = model
        self._view_section = section

        self._connect_signals()

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    def _connect_signals(self) -> None:
        # Logout
        self._view_section.logoutRequest.connect(  # type:ignore
            self.logoutRequest.emit
        )

        # Navigazione tra sezioni
        self._view_section.goToSection.connect(  # type:ignore
            self.goToSectionRequest.emit
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def _ottieni_pagina(self, pagina_nome: Pagina):
        """Ottiene la pagina indicata senza trasformarla in un `QWidget` generico.

        :param pagina_nome: nametag associato alla pagina
        """
        temp_dict: dict[str, Optional[QWidget]] = {"value": None}
        self.getPageRequest.emit(pagina_nome, temp_dict)
        return temp_dict.get("value")

    def _mostra_msg_pagina_non_trovata(self, pagina_nome: Pagina, tipo: type) -> None:
        """Metodo associato a `_ottieni_pagina`. È chiamato se la pagina ottenuta non è corretta.

        :param pagina_nome: nametag associato alla pagina attesa
        :param tipo: tipo ottenuto al chiamare `_ottiene_pagina`"""
        PopupMessage.mostra_errore(
            self._view_section,
            "Pagina non trovata",
            f"Si è verificato un errore: Non è stato trovata la pagina '{pagina_nome}'. "
            + f"Type trovato: {tipo}",
        )
