from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal, QObject
from typing import Optional

from core.metaclasses import ABCQObjectMeta
from core.view import AbstractSectionView

from controller.navigation import Pagina

from model.model.model import Model

from view.utils import mostra_error_popup


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
        self._view_page = section

        self._connect_signals()

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    def _connect_signals(self) -> None:
        # Logout
        self._view_page.logoutRequest.connect(  # type:ignore
            self.logoutRequest.emit
        )

        # Navigazione tra sezioni
        self._view_page.goToSection.connect(  # type:ignore
            self.goToSectionRequest.emit
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def _ottieni_pagina(self, pagina_nome: Pagina, tipo: type):
        """Ottiene la pagina indicata senza trasformarla in un `QWidget` generico.

        :param pagina_nome: nametag associato alla pagina
        :param tipo: tipo atteso della pagina

        :raise TypeError: il tipo atteso non è stato trovato
        """
        temp_dict: dict[str, Optional[QWidget]] = {"value": None}
        self.getPageRequest.emit(pagina_nome, temp_dict)
        pagina = temp_dict.get("value")

        if type(pagina) is not tipo:
            mostra_error_popup(
                self._view_page,
                "Pagina non trovata",
                f"Non è stato trovata la pagina '{pagina_nome}'. Type trovato: {tipo}",
            )
            raise TypeError("Pagina non trovata")
        return pagina
