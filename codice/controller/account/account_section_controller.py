from functools import partial
from typing import Optional

from core.controller import AbstractSectionController

from controller.login.user_session import UserSession
from controller.navigation import Pagina

from model.model import Model
from model.account.account import Account, Ruolo
from model.exceptions import OggettoInUsoException

from view.account.pagine import AccountSectionView
from view.account.utils import AccountPageData
from view.account.widgets import AccountDisplay

from view.utils.list_widgets import ListLayout
from view.utils import PopupMessage
from view.style.ui_style import WidgetRole, WidgetColor


class AccountSectionController(AbstractSectionController):
    """Gestice la sezione Account ('AccountSectionView') dell'app."""

    _view_section: AccountSectionView

    def __init__(
        self, model: Model, account_s: AccountSectionView, session: UserSession
    ):
        if type(account_s) is not AccountSectionView:
            raise TypeError("Atteso AccountSectionView per account_s.")

        self.__user_session_id = session.id

        super().__init__(model, account_s)

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    def _connect_signals(self) -> None:
        super()._connect_signals()

        # Display della Lista Account
        self._view_section.displayAccountRequest.connect(  # type:ignore
            self.__display_account
        )

        # Setup della pagina di creazione
        self._view_section.nuovoAccountRequest.connect(  # type:ignore
            self.__nuovo_account
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __get_account(self, id_: int) -> Optional[Account]:
        return self._model.get_account(id_)

    def __get_accounts(self) -> list[Account]:
        return self._model.get_accounts()

    def __elimina_account(self, id_: int) -> None:
        self._model.elimina_account(id_, self.__user_session_id)

    def __display_account(self, layout_accounts: ListLayout) -> None:
        """Mostra a schermo la lista degli account salvati
        e assegna a ciascuno dei pulsanti per modificarli o eliminarli

        :param layout_accounts: layout dove saranno caricati tutti gli account
        """
        accounts = self.__get_accounts()

        # Verifica che la lista non sia vuota
        if not accounts:
            layout_accounts.mostra_msg_lista_vuota()
            return

        accounts = sorted(accounts, key=lambda x: (x.get_ruolo()), reverse=True)

        # Funzione di eliminazione per gli account
        def on_conferma(id_: int) -> None:
            """Prova ad eliminare l'istanza di Account.

            :param id_: id dell'account da elimina
            """
            try:
                self.__elimina_account(id_)
            except OggettoInUsoException as e:
                current_account.annulla_elimina()
                PopupMessage.mostra_errore(
                    self._view_section,
                    "Account in uso",
                    f"Si è verificato un errore: {e}",
                )
            else:
                self._view_section.aggiorna_pagina()

        # Mostra tutti gli account salvati a schermo
        for acc in accounts:
            current_account = AccountDisplay(
                acc, (acc.get_id() != self.__user_session_id)
            )

            # Setup della pagina di modifica degli account
            current_account.modificaRequest.connect(  # type: ignore
                self.__modifica_account
            )

            current_account.eliminaConfermata.connect(  # type:ignore
                partial(on_conferma, acc.get_id())
            )

            COLORE = (
                WidgetColor.Item.RED_ITEM
                if acc.get_ruolo() == Ruolo.AMMINISTRATORE
                else WidgetColor.Item.BLUE_ITEM
            )
            layout_accounts.aggiungi_list_item(
                current_account, WidgetRole.ITEM_LIST, COLORE
            )

    def __nuovo_account(self) -> None:
        """Carica la pagina 'NuovoAccountView',
        dove l'utente può inserire i dati necessari per creare un account."""
        # Ottieni la pagina NuovoAccountView
        from view.account.pagine import NuovoAccountView

        pagina_nome = Pagina.NUOVO_ACCOUNT
        current_pagina = self._ottieni_pagina(pagina_nome)
        if type(current_pagina) is not NuovoAccountView:
            self._mostra_msg_pagina_non_trovata(pagina_nome, type(current_pagina))
            return

        # Setup pagina pulendo i campi
        current_pagina.reset_pagina()

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)

    def __modifica_account(self, id_: int) -> None:
        """Carica la pagina 'ModificaAccountView',
        con i dati del account indicato inseriti nei campo di input.

        :param id_: id del account da modificare
        """

        # Copia dell'account da modificare
        current_account = self.__get_account(id_)
        if not current_account:
            PopupMessage.mostra_errore(
                self._view_section,
                "Account insesitente",
                f"Non è presente nessun account con id {id_}",
            )
            return

        # Ottieni la pagina ModificaAccountView
        from view.account.pagine import ModificaAccountView

        pagina_nome = Pagina.MODIFICA_ACCOUNT
        current_pagina = self._ottieni_pagina(pagina_nome)
        if type(current_pagina) is not ModificaAccountView:
            self._mostra_msg_pagina_non_trovata(pagina_nome, type(current_pagina))
            return

        # Salva i dati dentro di un container
        account_dato = AccountPageData(
            id=current_account.get_id(),
            username=current_account.get_username(),
            ruolo=current_account.get_ruolo(),
        )

        # Setup pagina con i data dell'account
        current_pagina.set_data(account_dato)

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)
