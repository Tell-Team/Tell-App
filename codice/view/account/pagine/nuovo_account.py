from PyQt6.QtWidgets import QLabel, QLineEdit, QComboBox
from typing import override

from core.view import AbstractCreaView

from model.account.account import Ruolo

from view.style.ui_style import WidgetRole, WidgetColor


class NuovoAccountView(AbstractCreaView):
    """Pagina per la creazione di un nuovo account utente."""

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        # Header
        self._header.setText("Aggiungi nuovo account")

        # Layout
        self._main_layout.addWidget(self._header)
        self._main_layout.addWidget(self._scroll_area)
        self._main_layout.addWidget(self._input_error)
        self._main_layout.addWidget(self._pulsanti)
        self._main_layout.addStretch()

    @override
    def _setup_form(self) -> None:
        self._label_username = QLabel('Username<span style="color:red;">*</span> :')
        self._label_username.setProperty(WidgetRole.BODY_TEXT, True)
        self._label_username.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
        self.username = QLineEdit()
        self.username.setPlaceholderText("Inserire username")

        self._label_password = QLabel('Password<span style="color:red;">*</span> :')
        self._label_password.setProperty(WidgetRole.BODY_TEXT, True)
        self._label_password.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
        self.password = QLineEdit()
        self.password.setPlaceholderText("Inserire password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        self._label_conferma = QLabel(
            'Conferma password<span style="color:red;">*</span> :'
        )
        self._label_conferma.setProperty(WidgetRole.BODY_TEXT, True)
        self._label_conferma.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
        self.conferma = QLineEdit()
        self.conferma.setPlaceholderText("Confermare password")
        self.conferma.setEchoMode(QLineEdit.EchoMode.Password)

        self._label_ruolo = QLabel('Ruolo<span style="color:red;">*</span> : ')
        self._label_ruolo.setProperty(WidgetRole.BODY_TEXT, True)
        self._label_ruolo.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
        self.ruolo = QComboBox()
        self.ruolo.insertItem(0, "Scegli ruolo", None)
        self.ruolo.insertItem(1, "Biglietteria", Ruolo.BIGLIETTERIA)
        self.ruolo.insertItem(2, "Amministratore", Ruolo.AMMINISTRATORE)

        self._form_layout.addRow(self._label_username, self.username)
        self._form_layout.addRow(self._label_password, self.password)
        self._form_layout.addRow(self._label_conferma, self.conferma)
        self._form_layout.addRow(self._label_ruolo, self.ruolo)

    # ------------------------- METODI DI VIEW -------------------------

    @override
    def reset_pagina(self) -> None:
        super().reset_pagina()

        self.username.setText("")
        self.password.setText("")
        self.conferma.setText("")
        self.ruolo.setCurrentIndex(0)
