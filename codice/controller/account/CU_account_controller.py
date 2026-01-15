from core.controller import AbstractCUController

from model.model import Model

# from model.account import Account

from view.account.pagine import NuovoAccountView, ModificaAccountView

from typing import override


class CUAccountController(AbstractCUController):
    def __init__(
        self,
        model: Model,
        n_account_v: NuovoAccountView,
        m_account_v: ModificaAccountView,
    ):
        if type(n_account_v) is not NuovoAccountView:
            raise TypeError("Atteso NuovoAccountView per n_account_v.")

        if type(m_account_v) is not ModificaAccountView:
            raise TypeError("Atteso ModificaAccountView per m_account_v.")

        super().__init__(model, n_account_v, m_account_v)

    @override
    def _inizia_salvataggio(self, is_new: bool = True) -> None:
        print("# - DA CORRIGERE")
