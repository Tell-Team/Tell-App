from PyQt6.QtCore import pyqtSignal, QObject
from functools import partial
from typing import Optional

from controller.navigation import Pagina

from model.model import Model
from model.pianificazione.spettacolo import Spettacolo

from view.spettacoli.pagine.spettacoli_section import SpettacoliSectionView

# from view.messageView import MessageView


class SpettacoliController(QObject):
    """Gestice la sezione Spettacoli (`SpettacoliSectionView`) dell'app.

    Segnali:
    - logoutRequest(): emesso per eseguire la funzione di logout dall`AppContext`;
    - goToPageRequest(Pagina, bool): emesso per visualizzare un'altra pagina;
    - goToSectionRequest(Pagina): emesso per visualizzare un'altra pagina, senza salvarla
    nell'history del `NavigationController`;
    - getNavPageRequest(Pagina, dict): emesso per ottenere la pagina che vendrà visualizzata.
    """

    logoutRequest: pyqtSignal = pyqtSignal()
    goToPageRequest: pyqtSignal = pyqtSignal(Pagina, bool)
    goToSectionRequest: pyqtSignal = pyqtSignal(Pagina)
    getNavPageRequest: pyqtSignal = pyqtSignal(Pagina, dict)

    def __init__(self, model: Model, spettacoli_s: SpettacoliSectionView) -> None:
        super().__init__()
        self.__model = model
        self.__spettacoli_section = spettacoli_s

        self.__connect_signals()

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    def __connect_signals(self) -> None:
        # Logout
        self.__spettacoli_section.logoutRequest.connect(  # type:ignore
            self.logoutRequest.emit  # - CORRIGGERE: Account ancora non implementato
        )
        # Visualizza Sezione Info
        self.__spettacoli_section.goToInfo.connect(  # type:ignore
            partial(self.goToSectionRequest.emit, Pagina.SEZIONE_INFO)
        )
        # Visualizza Sezione Account
        self.__spettacoli_section.goToAccount.connect(  # type:ignore
            partial(self.goToSectionRequest.emit, Pagina.SEZIONE_ACCOUNT)
        )

        # Display della Lista Spettacoli
        self.__spettacoli_section.displaySpettacoliRequest.connect(  # type:ignore
            self.display_spettacoli
        )

        # Setup della pagina di creazione di spettacoli
        self.__spettacoli_section.nuovoSpettacoloRequest.connect(  # type:ignore
            self.nuovo_spettacolo
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def get_spettacolo(self, id_: int) -> Optional[Spettacolo]:
        return self.__model.get_spettacolo(id_)

    def get_spettacoli(self) -> list[Spettacolo]:
        return self.__model.get_spettacoli()

    def get_spettacoli_by_titolo(self, titolo: str) -> list[Spettacolo]:
        return self.__model.get_spettacoli_by_titolo(titolo)

    def elimina_spettacolo(self, id_: int) -> None:
        self.__model.elimina_spettacolo(id_)
        # - Implementare elimina_spettacolo nel model

    def display_spettacoli(self) -> None: ...

    def nuovo_spettacolo(self) -> None: ...

    def modifica_spettacolo(self, id_: int) -> None: ...

    def scegli_posti(self, id_: int) -> None: ...
