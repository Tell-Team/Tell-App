from functools import partial

from core.controller import AbstractSectionController

from model.model import Model
from model.account.account import Ruolo

from view.account.pagine import AccountSectionView


class AccountSectionController(AbstractSectionController):
    """Gestice la sezione Account (`AccountSectionView`) dell'app."""

    _view_section: AccountSectionView

    def __init__(
        self,
        model: Model,
        account_s: AccountSectionView,
    ):
        if type(account_s) is not AccountSectionView:
            raise TypeError("Atteso AccountSectionView per account_s.")

        super().__init__(model, account_s)

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    def _connect_signals(self) -> None:
        super()._connect_signals()

        # Display della Lista Account
        self._view_section.displayAdminRequest.connect(  # type:ignore
            partial(self.__display_account, Ruolo.AMMINISTRATORE)
            # - UNIFICAR LA FUNCIÓN DE DISPLAY
        )
        self._view_section.displayBiglietteriaRequest.connect(  # type:ignore
            partial(self.__display_account, Ruolo.BIGLIETTERIA)
        )

        # Setup della pagina di creazione
        self._view_section.nuovoAdminRequest.connect(  # type:ignore
            partial(self.__nuovo_account, Ruolo.AMMINISTRATORE)
            # - UNIFICAR LA FUNCIÓN DE CREACIÓN??
        )
        self._view_section.nuovoBiglietteriaRequest.connect(  # type:ignore
            partial(self.__nuovo_account, Ruolo.BIGLIETTERIA)
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __display_account(self, ruolo: Ruolo) -> None: ...

    def __nuovo_account(self, ruolo: Ruolo) -> None: ...

    def modifica_account(self, id_: int) -> None: ...
