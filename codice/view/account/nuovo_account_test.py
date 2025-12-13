from PyQt6.QtWidgets import QLabel, QLineEdit, QComboBox, QFrame

from view.abstractView.creaAbstract import CreaAbstractView


# Si usa la stessa pagina per creare sia un account Amministratore che un Biglietteria.
#   Solo si modifica un QComboBox disabilitato per indicare il ruolo dell'account durante
#   la creazione. Nel caso di modifica, comunque, è abilitato per permettere aggiornare il
#   ruolo di qualunque account.
class NuovoAccountView(CreaAbstractView):
    """
    GUI di creazione di `Opera`.

    Contiene campi d'input per inserire le informazione anagrafiche dell'utente e del account.
    """

    def __init__(self):
        super().__init__()

        self._build_ui()

    def _build_ui(self):
        # Header
        self.header.setText("Nuovo account")

        # Form
        self._setup_form()

        # Layout
        self.main_layout.addWidget(self.header)
        self.main_layout.addWidget(self.form_content)
        self.main_layout.addWidget(self.input_error)
        self.main_layout.addWidget(self.pulsanti)
        self.main_layout.addStretch()

    def _setup_form(self):
        label_anagrafica_header = QLabel("Anagrafica")
        label_anagrafica_header.setObjectName("Header2")

        label_nome = QLabel("Nome :")
        label_nome.setObjectName("SubHeader")
        self.nome = QLineEdit()
        self.nome.setPlaceholderText("Inserire nome")

        label_cognome = QLabel("Cognome :")
        label_cognome.setObjectName("SubHeader")
        self.cognome = QLineEdit()
        self.cognome.setPlaceholderText("Inserire cognome")

        linea = QFrame()
        linea.setFrameShape(QFrame.Shape.HLine)

        label_account_header = QLabel("Accesso e Ruolo")
        label_account_header.setObjectName("Header2")

        label_username = QLabel("Username :")
        label_username.setObjectName("SubHeader")
        self.username = QLineEdit()
        self.username.setPlaceholderText("Inserire username")

        label_password = QLabel("Password :")
        label_password.setObjectName("SubHeader")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Inserire password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        label_ruolo = QLabel("Ruolo : ")
        label_ruolo.setObjectName("SubHeader")
        self.ruolo = QComboBox()
        # - Hard-coded options
        self.ruolo.insertItem(0, "Biglietteria")
        self.ruolo.insertItem(1, "Amministratore")
        self.ruolo.setEnabled(False)
        # - END

        self.add_row(label_anagrafica_header, None)
        self.add_row(label_nome, self.nome)
        self.add_row(label_cognome, self.cognome)
        self.add_row(linea, None)
        self.add_row(label_account_header, None)
        self.add_row(label_username, self.username)
        self.add_row(label_password, self.password)
        self.add_row(label_ruolo, self.ruolo)
