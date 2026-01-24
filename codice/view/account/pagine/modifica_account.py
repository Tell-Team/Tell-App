from typing import override

from model.account.account import Ruolo

from view.account.pagine import NuovoAccountView
from view.account.utils import AccountPageData


class ModificaAccountView(NuovoAccountView):
    """Pagina per la modifica di account utente.

    Sottoclasse di `NuovoAccountView`. Modifica alcune label della pagina, abilita
    il QComboBox per scegliere il ruolo ed aggiunge un'attributo `cur_id_account` per
    indicare l'id dell'account da modificare."""

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        # Il valore è assegnato quando si chiama AccountSectionController.modifica_account(id_account)
        self.cur_id_account: int = -1

        # Aggiorna header
        self._header.setText("Modifica account")

        # Abilita il QComboBox del ruolo
        self.ruolo.setEnabled(True)

    # ------------------------- METODI DI VIEW -------------------------

    def set_data(self, data: AccountPageData) -> None:
        """Carica i dati di un'account nella pagina.

        :param data: data salvata in una classe immutabile"""
        self.cur_id_account = data.id

        self.username.setText(data.username)

        index = 0
        match data.ruolo:
            case Ruolo.BIGLIETTERIA:
                index = 1
            case Ruolo.AMMINISTRATORE:
                index = 2
        self.ruolo.setCurrentIndex(index)

    @override
    def reset_pagina(self) -> None:
        super().reset_pagina()
        self.cur_id_account = -1
