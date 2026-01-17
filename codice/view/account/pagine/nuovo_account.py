from PyQt6.QtWidgets import QLabel, QLineEdit, QComboBox
from typing import override

from core.view import AbstractCreaView

from model.account.account import Ruolo

from view.style import WidgetRole, WidgetColor


# Si usa la stessa pagina per creare sia un account Amministratore che un Biglietteria.
#   Solo si modifica un QComboBox disabilitato per indicare il ruolo dell'account durante
#   la creazione. Nel caso di modifica, comunque, è abilitato per permettere aggiornare il
#   ruolo di qualunque account.
class NuovoAccountView(AbstractCreaView):
    """Pagina per la creazione di un nuovo account utente.

    Segnali:
    - `annullaRequest(QWidget)`: emesso quando si clicca il pulsante Annulla;
    - `salvaRequest()`: emesso quando si clicca il pulsante Crea.
    """

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
        label_anagrafica_header = QLabel("Anagrafica")
        label_anagrafica_header.setProperty(WidgetRole.HEADER2, True)

        label_nome = QLabel('Nome<span style="color:red;">*</span> :')
        label_nome.setProperty(WidgetRole.BODY_TEXT, True)
        label_nome.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
        self.nome = QLineEdit()
        self.nome.setPlaceholderText("Inserire nome")

        label_cognome = QLabel('Cognome<span style="color:red;">*</span> :')
        label_cognome.setProperty(WidgetRole.BODY_TEXT, True)
        label_cognome.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
        self.cognome = QLineEdit()
        self.cognome.setPlaceholderText("Inserire cognome")

        label_account_header = QLabel("Accesso e Ruolo")
        label_account_header.setProperty(WidgetRole.HEADER2, True)

        label_username = QLabel('Username<span style="color:red;">*</span> :')
        label_username.setProperty(WidgetRole.BODY_TEXT, True)
        label_username.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
        self.username = QLineEdit()
        self.username.setPlaceholderText("Inserire username")

        label_password = QLabel('Password<span style="color:red;">*</span> :')
        label_password.setProperty(WidgetRole.BODY_TEXT, True)
        label_password.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
        self.password = QLineEdit()
        self.password.setPlaceholderText("Inserire password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        label_ruolo = QLabel('Ruolo<span style="color:red;">*</span> : ')
        label_ruolo.setProperty(WidgetRole.BODY_TEXT, True)
        label_ruolo.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
        self.ruolo = QComboBox()
        self.ruolo.insertItem(0, "Scegli ruolo", None)
        self.ruolo.insertItem(1, "Biglietteria", Ruolo.BIGLIETTERIA)
        self.ruolo.insertItem(2, "Amministratore", Ruolo.AMMINISTRATORE)
        self.ruolo.setEnabled(False)

        self._form_layout.addRow(label_anagrafica_header)
        self._form_layout.addRow(label_nome, self.nome)
        self._form_layout.addRow(label_cognome, self.cognome)
        self._form_layout.addRow(QLabel('<hr style="background-color:#b0b0b0;">'))
        self._form_layout.addRow(label_account_header)
        self._form_layout.addRow(label_username, self.username)
        self._form_layout.addRow(label_password, self.password)
        self._form_layout.addRow(label_ruolo, self.ruolo)

    # ------------------------- METODI DI VIEW -------------------------

    @override
    def reset_pagina(self) -> None:
        self.nome.setText("")
        self.password.setText("")
