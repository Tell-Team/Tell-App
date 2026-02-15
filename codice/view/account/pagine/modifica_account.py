from PyQt6.QtWidgets import QLabel, QLineEdit

from typing import override

from model.account.account import Ruolo

from view.account.pagine import NuovoAccountView
from view.account.utils import AccountData

from view.style.ui_style import WidgetRole, WidgetColor


class ModificaAccountView(NuovoAccountView):
    """Pagina per la modifica di account utente. Sottoclasse di `NuovoAccountView`."""

    def __init__(self):
        super().__init__()

        # Valore assegnato quando si chiama AccountSectionController.modifica_account
        self.id_current_account: int = -1

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        self._header.setText("Modifica account")

        self.username.setEnabled(False)
        self._label_password.setText("Password originale :")
        self._label_conferma.setText("Conferma nuovo password :")

        self.ruolo.setEnabled(True)

        self._svuota_form_layout(self._form_layout)

        label_nuova_password = QLabel("Nuova password :")
        label_nuova_password.setProperty(WidgetRole.Label.BODY_TEXT, True)
        label_nuova_password.setProperty(WidgetColor.Label.SECONDARY_COLOR, True)
        self.nuova_password = QLineEdit()
        self.nuova_password.setPlaceholderText("Inserire nuova password")
        self.nuova_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.conferma.setEnabled(False)
        self.password.setEnabled(False)

        self._form_layout.addRow(self._label_username, self.username)
        self._form_layout.addRow(label_nuova_password, self.nuova_password)
        self._form_layout.addRow(self._label_conferma, self.conferma)
        self._form_layout.addRow(self._label_password, self.password)
        self._form_layout.addRow(self._label_ruolo, self.ruolo)

    # ------------------------- METODI DI VIEW -------------------------

    def set_modifica_password_enabled(self, enabled: bool):
        self.conferma.setEnabled(enabled)
        self.password.setEnabled(enabled)

    def set_data(self, data: AccountData) -> None:
        """Carica i dati di un'account nella pagina.

        :param data: data salvata in una classe immutabile"""
        self.reset_pagina()

        self.id_current_account = data.id

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
        self.id_current_account = -1
        self.nuova_password.setText("")
        self.set_modifica_password_enabled(False)
