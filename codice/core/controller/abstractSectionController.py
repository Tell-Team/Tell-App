from PyQt6.QtCore import pyqtSignal, QObject
from functools import partial

from core.metaclasses import ABCQObjectMeta
from core.view import AbstractSectionView

from controller.navigation import Pagina

from model.model import Model


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
        self._view_section.goToAcquisto.connect(  # type:ignore
            partial(self.goToSectionRequest.emit, Pagina.SEZIONE_ACQUISTO)
        )
        self._view_section.goToSpettacoli.connect(  # type:ignore
            partial(self.goToSectionRequest.emit, Pagina.SEZIONE_SPETTACOLI)
        )
        self._view_section.goToInfo.connect(  # type:ignore
            partial(self.goToSectionRequest.emit, Pagina.SEZIONE_INFO)
        )
        self._view_section.goToAccount.connect(  # type:ignore
            partial(self.goToSectionRequest.emit, Pagina.SEZIONE_ACCOUNT)
        )
