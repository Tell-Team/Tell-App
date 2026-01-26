from PyQt6.QtWidgets import QLabel, QLineEdit

from typing import override

from model.account.account import Ruolo

from view.account.pagine import NuovoAccountView
from view.account.utils import AccountPageData

from view.style.ui_style import WidgetRole, WidgetColor


class ModificaAccountView(NuovoAccountView):
    """Pagina per la modifica di account utente.

    Sottoclasse di `NuovoAccountView`. Modifica alcune label della pagina, abilita
    il QComboBox per scegliere il ruolo ed aggiunge un'attributo `cur_id_account` per
    indicare l'id dell'account da modificare."""

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        # Il valore è assegnato quando si chiama AccountSectionController.modifica_account
        self.cur_id_account: int = -1

        # Aggiorna ui della pagina
        self._header.setText("Modifica account")

        self.username.setEnabled(False)
        self._label_password.setText("Password originale :")
        self._label_conferma.setText("Conferma nuovo password :")

        self.ruolo.setEnabled(True)

        self._svuota_form_layout(self._form_layout)

        label_nuova_password = QLabel("Nuova password :")
        label_nuova_password.setProperty(WidgetRole.BODY_TEXT, True)
        label_nuova_password.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
        self.nuova_password = QLineEdit()
        self.nuova_password.setPlaceholderText("Inserire nuova password")
        self.nuova_password.setEchoMode(QLineEdit.EchoMode.Password)

        self._form_layout.addRow(self._label_username, self.username)
        self._form_layout.addRow(self._label_password, self.password)
        self._form_layout.addRow(label_nuova_password, self.nuova_password)
        self._form_layout.addRow(self._label_conferma, self.conferma)
        self._form_layout.addRow(self._label_ruolo, self.ruolo)

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
        self.nuova_password.setText("")
        self.cur_id_account = -1
