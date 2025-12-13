from view.account.nuovo_account import NuovoAccountView


class ModificaAccountView(NuovoAccountView):
    """
    Sottoclasse di `NuovoAccountView`. Modifica l'header della pagina, abilita il
    QComboBox per scegliere un ruolo ed aggiunge un'attributo `cur_id_account` per
    indicare l'id dell'account da modificare.
    """

    def __init__(self):
        super().__init__()

    def _build_ui(self):
        super()._build_ui()

        # Il valore è assegnato quando si chiama AccountController.modifica_account(id_account)
        self.cur_id_account: int = -1

        # Header
        self.header.setText("Modifica account")

        # - Una volta creato l'account, il nome e cognome vincolati all'account potrano esser modificati?

        # Abilita il QComboBox del ruolo
        self.ruolo.setEnabled(True)
