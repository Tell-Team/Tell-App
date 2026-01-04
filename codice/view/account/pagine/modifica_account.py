from typing import override

from view.account.pagine import NuovoAccountView

# - from view.account.utils.accountPageData import AccountPageData


class ModificaAccountView(NuovoAccountView):
    """Sottoclasse di `NuovoAccountView`. Modifica alcune label della pagina, abilita
    il QComboBox per scegliere il ruolo ed aggiunge un'attributo `cur_id_account` per
    indicare l'id dell'account da modificare."""

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        # Il valore è assegnato quando si chiama AccountController.modifica_account(id_account)
        self.cur_id_account: int = -1

        # Aggiorna header
        self._header.setText("Modifica account")

        # - Una volta creato l'account, il nome e cognome vincolati all'account potrano esser modificati?

        # Abilita il QComboBox del ruolo
        self.ruolo.setEnabled(True)

    # ------------------------- METODI DI VIEW -------------------------

    # def set_data(self, data: AccountPageData) -> None:
    #     """Carica i dati di un'account nella pagina.

    #     :param data: data salvata in una classe immutabile"""
    #     self.cur_id_account = data.id
    #
    #     self.nome.setText(data.nome)
    #     self.cognome.setText(data.cognome)
    #     self.username.setText(data.username)
    #     self.password.setText(data.password) # - Fare il testo di self.password vissibile(?)

    @override
    def reset_pagina(self) -> None:
        super().reset_pagina()
        self.cur_id_account = -1
