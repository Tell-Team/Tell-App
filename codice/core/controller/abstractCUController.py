from abc import abstractmethod
from PyQt6.QtCore import pyqtSignal, QObject
from functools import partial

from core.metaclasses import ABCQObjectMeta
from core.view import AbstractCreaView

from model.model import Model


class AbstractCUController(QObject, metaclass=ABCQObjectMeta):
    """Classe astratta per la creazione di controller per la creazione o modifica
    di oggetti del model.

    Segnali:
    - `goBackRequest()`: emesso per tornare all'ultima pagina visualizzata.
    """

    goBackRequest: pyqtSignal = pyqtSignal()

    def __init__(
        self, model: Model, nuova: AbstractCreaView, modifica: AbstractCreaView
    ):
        super().__init__()

        self._model = model
        self._view_nuova = nuova
        self._view_modifica = modifica

        self._connect_signals()

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    def _connect_signals(self) -> None:
        # # Annulla creazione
        self._view_nuova.annullaRequest.connect(  # type:ignore
            self._annulla_salvataggio
        )
        # Conferma creazione
        self._view_nuova.salvaRequest.connect(  # type:ignore
            partial(self._inizia_salvataggio, is_new=True)
        )

        # Annulla modifica
        self._view_modifica.annullaRequest.connect(  # type:ignore
            self._annulla_salvataggio
        )
        # Conferma modifica
        self._view_modifica.salvaRequest.connect(  # type:ignore
            partial(self._inizia_salvataggio, is_new=False)
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def _annulla_salvataggio(self, cur_pagina: AbstractCreaView) -> None:
        """Annulla l'operazione di creazione o modifica.

        :param cur_pagina: pagina dove fare il reset dopo ritornare alla pagina dove
        l'operazione è stata iniziata
        """
        self.goBackRequest.emit()
        cur_pagina.reset_pagina()

    @abstractmethod
    def _inizia_salvataggio(self, is_new: bool) -> None:
        """Salva l'istanza creata o modificata nel gestore dedicato.

        :param is_new: verifica se si deve creare un'instanza o modificare una esistente
        """
        ...
