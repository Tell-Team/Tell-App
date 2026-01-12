from PyQt6.QtCore import pyqtSignal, QObject
from functools import partial

from controller.navigation import Pagina

from model.model import Model
from model.account.account import Ruolo

from view.account.pagine import AccountSectionView

# from view.utils import PopupMessage


class AccountSectionController(QObject):
    """Gestice la sezione Account (`AccountSectionView`) dell'app.

    Segnali:
    - logoutRequest(): emesso per eseguire la funzione di logout dall'`AppContext`;
    - goToPageRequest(Pagina, bool): emesso per visualizzare un'altra pagina;
    - goToSectionRequest(Pagina): emesso per visualizzare un'altra pagina, senza salvarla
    nell'history del `NavigationController`;
    - getNavPageRequest(Pagina, dict): emesso per ottenere la pagina che vendrà visualizzata.
    """

    logoutRequest: pyqtSignal = pyqtSignal()
    goToPageRequest: pyqtSignal = pyqtSignal(Pagina, bool)
    goToSectionRequest: pyqtSignal = pyqtSignal(Pagina)
    getNavPageRequest: pyqtSignal = pyqtSignal(Pagina, dict)

    def __init__(
        self,
        model: Model,
        account_s: AccountSectionView,
    ) -> None:
        super().__init__()
        self.__model = model
        self.__account_section = account_s

        self.__connect_signals()

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    def __connect_signals(self) -> None:
        # Logout
        self.__account_section.logoutRequest.connect(  # type:ignore
            self.logoutRequest.emit
        )
        # Visualizza Sezione Spettacoli
        self.__account_section.goToSpettacoli.connect(  # type:ignore
            partial(self.goToSectionRequest.emit, Pagina.SEZIONE_SPETTACOLI)
        )
        # Visualizza Sezione Info
        self.__account_section.goToInfo.connect(  # type:ignore
            partial(self.goToSectionRequest.emit, Pagina.SEZIONE_INFO)
        )

        # Display della Lista Account
        self.__account_section.displayAdminRequest.connect(  # type:ignore
            partial(self.__display_account, Ruolo.AMMINISTRATORE)
        )
        self.__account_section.displayBiglietteriaRequest.connect(  # type:ignore
            partial(self.__display_account, Ruolo.BIGLIETTERIA)
        )

        # Setup della pagina di creazione di account
        self.__account_section.nuovoAdminRequest.connect(  # type:ignore
            partial(self.__nuovo_account, Ruolo.AMMINISTRATORE)
        )
        self.__account_section.nuovoBiglietteriaRequest.connect(  # type:ignore
            partial(self.__nuovo_account, Ruolo.BIGLIETTERIA)
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __display_account(self, ruolo: Ruolo) -> None: ...

    def __nuovo_account(self, ruolo: Ruolo) -> None: ...

    def modifica_account(self, id_: int) -> None: ...
