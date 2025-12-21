from PyQt6.QtWidgets import QLabel, QLineEdit, QComboBox, QFrame
from PyQt6.QtCore import pyqtSignal
from typing import override

from view.abstractView.creaAbstract import CreaAbstractView


# Si usa la stessa pagina per creare sia un account Amministratore che un Biglietteria.
#   Solo si modifica un QComboBox disabilitato per indicare il ruolo dell'account durante
#   la creazione. Nel caso di modifica, comunque, è abilitato per permettere aggiornare il
#   ruolo di qualunque account.
class NuovoAccountView(CreaAbstractView):
    """
    View per la creazione di un nuovo account utente.

    Segnali:
    - annullaRequest(): emesso quando si clicca il pulsante Annulla;
    - salvaRequest(): emesso quando si clicca il pulsante Conferma.
    """

    annullaRequest = pyqtSignal()
    salvaRequest = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

        self._setup_ui()
        self._connect_signals()

    # ------------------------- SETUP INIT -------------------------

    def _setup_ui(self) -> None:
        # Header
        self.header.setText("Aggiungi nuovo account")

        # Form
        self._setup_form()

        # Layout
        self.main_layout.addWidget(self.header)
        self.main_layout.addWidget(self.form_content)
        self.main_layout.addWidget(self.input_error)
        self.main_layout.addWidget(self.pulsanti)
        self.main_layout.addStretch()

    @override
    def _setup_form(self) -> None:
        label_anagrafica_header = QLabel("Anagrafica")
        label_anagrafica_header.setObjectName("header2")

        label_nome = QLabel("Nome :")
        label_nome.setObjectName("subheader")
        self.nome = QLineEdit()
        self.nome.setPlaceholderText("Inserire nome")

        label_cognome = QLabel("Cognome :")
        label_cognome.setObjectName("subheader")
        self.cognome = QLineEdit()
        self.cognome.setPlaceholderText("Inserire cognome")

        linea = QFrame()
        linea.setFrameShape(QFrame.Shape.HLine)

        label_account_header = QLabel("Accesso e Ruolo")
        label_account_header.setObjectName("header2")

        label_username = QLabel("Username :")
        label_username.setObjectName("subheader")
        self.username = QLineEdit()
        self.username.setPlaceholderText("Inserire username")

        label_password = QLabel("Password :")
        label_password.setObjectName("subheader")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Inserire password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        label_ruolo = QLabel("Ruolo : ")
        label_ruolo.setObjectName("subheader")
        self.ruolo = QComboBox()
        # - Hard-coded options
        self.ruolo.insertItem(0, "Scegli ruolo")
        self.ruolo.insertItem(1, "Biglietteria")
        self.ruolo.insertItem(2, "Amministratore")
        self.ruolo.setEnabled(False)
        # - END

        self.form_layout.addRow(label_anagrafica_header, None)
        self.form_layout.addRow(label_nome, self.nome)
        self.form_layout.addRow(label_cognome, self.cognome)
        self.form_layout.addRow(linea, None)
        self.form_layout.addRow(label_account_header, None)
        self.form_layout.addRow(label_username, self.username)
        self.form_layout.addRow(label_password, self.password)
        self.form_layout.addRow(label_ruolo, self.ruolo)

    def _connect_signals(self) -> None:
        self._btn_annulla.clicked.connect(  # type:ignore
            self.annullaRequest.emit
        )

        self._btn_conferma.clicked.connect(  # type:ignore
            self.salvaRequest.emit
        )
