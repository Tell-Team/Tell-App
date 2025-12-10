from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt


class LoginPage(QWidget):
    """
    GUI iniziale dell'app.

    Permette di scegliere il tipo d'account con cui si utilizzerà l'app:
    - Se scelto Cliente, semplicemente viene inviato alla sezione Info;
    - Se scelto Biglietteria o Amministratore, chiede un'autenticazione.
    """

    def __init__(self):
        super().__init__()

        self._build_ui()

    def _build_ui(self):
        # Header
        self.header = QLabel("Login")
        self.header.setObjectName("Header1")
        self.header.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Subheader
        self.subheader = QLabel("Scegliere il tipo di account:")
        self.subheader.setObjectName("Paragraph")
        self.subheader.setAlignment(Qt.AlignmentFlag.AlignLeft)

        #
        #
        #

        # Pulsanti
        self.btn_cliente = QPushButton("Cliente")
        self.btn_cliente.setObjectName("BlueButton")

        self.btn_biglietteria = QPushButton("Biglietteria")
        self.btn_biglietteria.setObjectName("BlueButton")

        self.btn_amministratore = QPushButton("Amministratore")
        self.btn_amministratore.setObjectName("BlueButton")

        self.pulsanti_utente = QWidget()
        layout_pulsanti_utente = QVBoxLayout(self.pulsanti_utente)
        layout_pulsanti_utente.addWidget(self.btn_cliente)
        layout_pulsanti_utente.addWidget(self.btn_biglietteria)
        layout_pulsanti_utente.addWidget(self.btn_amministratore)

        #
        #
        #

        # Layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        main_layout.addWidget(self.header)
        main_layout.addWidget(self.subheader)
        main_layout.addWidget(self.pulsanti_utente)
        main_layout.addStretch()
