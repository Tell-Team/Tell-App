from PyQt6.QtWidgets import QLabel, QLineEdit, QComboBox
from typing import override

from view.abstractView.abstractCreaView import AbstractCreaView
from view.style import QssStyle


# Si usa la stessa pagina per creare sia un account Amministratore che un Biglietteria.
#   Solo si modifica un QComboBox disabilitato per indicare il ruolo dell'account durante
#   la creazione. Nel caso di modifica, comunque, è abilitato per permettere aggiornare il
#   ruolo di qualunque account.
class NuovoAccountView(AbstractCreaView):
    """View per la creazione di un nuovo account utente.

    Segnali:
    - annullaRequest(QWidget): emesso quando si clicca il pulsante Annulla;
    - salvaRequest(): emesso quando si clicca il pulsante Crea.
    """

    def __init__(self) -> None:
        super().__init__()

        self._setup_ui()
        self._connect_signals()

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        # Header
        self._header.setText("Aggiungi nuovo account")

        # Form
        self._setup_form()

        # Layout
        self._main_layout.addWidget(self._header)
        self._main_layout.addWidget(self._scroll_area)
        self._main_layout.addWidget(self._input_error)
        self._main_layout.addWidget(self._pulsanti)
        self._main_layout.addStretch()

    @override
    def _setup_form(self) -> None:
        label_anagrafica_header = QLabel("Anagrafica")
        label_anagrafica_header.setObjectName(QssStyle.HEADER2.style_name)

        label_nome = QLabel('Nome<span style="color:red;">*</span> :')
        label_nome.setObjectName(QssStyle.SECONDARY_TEXT.style_name)
        self.nome = QLineEdit()
        self.nome.setPlaceholderText("Inserire nome")

        label_cognome = QLabel('Cognome<span style="color:red;">*</span> :')
        label_cognome.setObjectName(QssStyle.SECONDARY_TEXT.style_name)
        self.cognome = QLineEdit()
        self.cognome.setPlaceholderText("Inserire cognome")

        label_account_header = QLabel("Accesso e Ruolo")
        label_account_header.setObjectName(QssStyle.HEADER2.style_name)

        label_username = QLabel('Username<span style="color:red;">*</span> :')
        label_username.setObjectName(QssStyle.SECONDARY_TEXT.style_name)
        self.username = QLineEdit()
        self.username.setPlaceholderText("Inserire username")

        label_password = QLabel('Password<span style="color:red;">*</span> :')
        label_password.setObjectName(QssStyle.SECONDARY_TEXT.style_name)
        self.password = QLineEdit()
        self.password.setPlaceholderText("Inserire password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        label_ruolo = QLabel('Ruolo<span style="color:red;">*</span> : ')
        label_ruolo.setObjectName(QssStyle.SECONDARY_TEXT.style_name)
        self.ruolo = QComboBox()
        # - Hard-coded options
        self.ruolo.insertItem(0, "Scegli ruolo")
        self.ruolo.insertItem(1, "Biglietteria")
        self.ruolo.insertItem(2, "Amministratore")
        self.ruolo.setEnabled(False)
        # - END

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
