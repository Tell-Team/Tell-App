from typing import override

from view.account.pagine.nuovo_account import NuovoAccountView


class ModificaAccountView(NuovoAccountView):
    """
    Sottoclasse di `NuovoAccountView`. Modifica alcuni label della pagina, abilita il
    QComboBox per scegliere un ruolo ed aggiunge un'attributo `cur_id_account` per
    indicare l'id dell'account da modificare.
    """

    def __init__(self) -> None:
        super().__init__()

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        # Il valore è assegnato quando si chiama AccountController.modifica_account(id_account)
        self.cur_id_account: int = -1

        # Aggiorna header
        self.header.setText("Modifica account")

        # Aggiorna btn_conferma
        self._btn_conferma.setText("Modifica")

        # - Una volta creato l'account, il nome e cognome vincolati all'account potrano esser modificati?

        # Abilita il QComboBox del ruolo
        self.ruolo.setEnabled(True)
