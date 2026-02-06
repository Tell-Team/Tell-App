from PyQt6.QtCore import pyqtSignal, QObject

from core.metaclasses import ABCQObjectMeta
from core.view import AbstractVisualizzaView

from controller.navigation import Pagina

from model.model import Model


class AbstractVisualizzaController(QObject, metaclass=ABCQObjectMeta):
    """Classe astratta per la creazione di controller per gestire pagine
    `AbstractVisualizzaView`.

    Segnali
    ---
    - `goBackRequest()`: emesso per tornare all'ultima pagina visualizzata;
    - `goToPageRequest(Pagina, bool)`: emesso per visualizzare un'altra pagina;
    - `getPageRequest(Pagina, dict)`: emesso per ottenere la pagina che vendrà visualizzata.
    """

    goBackRequest: pyqtSignal = pyqtSignal()
    goToPageRequest: pyqtSignal = pyqtSignal(Pagina, bool)
    getPageRequest: pyqtSignal = pyqtSignal(Pagina, dict)

    def __init__(self, model: Model, pagina: AbstractVisualizzaView):
        super().__init__()
        self._model = model
        self._view_page = pagina

        self._connect_signals()

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    def _connect_signals(self) -> None:
        self._view_page.tornaIndietroRequest.connect(  # type:ignore
            self.goBackRequest.emit
        )
