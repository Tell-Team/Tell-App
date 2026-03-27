from PyQt6.QtWidgets import QLabel
from typing import override

from core.view import AbstractCreaView

from model.account.account import Ruolo

from view.utils.fixed_size_widget import FixedSizeLineEdit, FixedSizeComboBox

from view.style.ui_style import WidgetRole, WidgetColor


class NuovoAccountPage(AbstractCreaView):
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
        self._label_username.setProperty(WidgetRole.Label.BODY_TEXT, True)
        self._label_username.setProperty(WidgetColor.Label.SECONDARY_COLOR, True)
        self.username = FixedSizeLineEdit(width=230)
        self.username.setPlaceholderText("Inserire username")

        self._label_password = QLabel('Password<span style="color:red;">*</span> :')
        self._label_password.setProperty(WidgetRole.Label.BODY_TEXT, True)
        self._label_password.setProperty(WidgetColor.Label.SECONDARY_COLOR, True)
        self.password = FixedSizeLineEdit(width=230)
        self.password.setPlaceholderText("Inserire password")
        self.password.setEchoMode(FixedSizeLineEdit.EchoMode.Password)

        self._label_conferma = QLabel(
            'Conferma password<span style="color:red;">*</span> :'
        )
        self._label_conferma.setProperty(WidgetRole.Label.BODY_TEXT, True)
        self._label_conferma.setProperty(WidgetColor.Label.SECONDARY_COLOR, True)
        self.conferma = FixedSizeLineEdit(width=230)
        self.conferma.setPlaceholderText("Confermare password")
        self.conferma.setEchoMode(FixedSizeLineEdit.EchoMode.Password)

        self._label_ruolo = QLabel('Ruolo<span style="color:red;">*</span> : ')
        self._label_ruolo.setProperty(WidgetRole.Label.BODY_TEXT, True)
        self._label_ruolo.setProperty(WidgetColor.Label.SECONDARY_COLOR, True)
        self.ruolo = FixedSizeComboBox(width=230)
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
