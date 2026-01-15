from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt

from view.style import QssStyle


class LoginPage(QWidget):
    """View della pagina per scegliere il tipo d'account con cui ingressare all'app."""

    def __init__(self):
        super().__init__()

        self._setup_ui()

    # ------------------------- SETUP INIT -------------------------

    def _setup_ui(self) -> None:
        # Content
        header = QLabel("Login")
        header.setProperty(QssStyle.HEADER1, True)
        header.setAlignment(Qt.AlignmentFlag.AlignLeft)

        subheader = QLabel("Scegliere il tipo di account:")
        subheader.setProperty(QssStyle.PARAGRAPH, True)
        subheader.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Pulsanti
        self.btn_cliente = QPushButton("Cliente")
        self.btn_cliente.setProperty(QssStyle.BLUE_BUTTON, True)
        self.btn_cliente.setProperty(QssStyle.MAIN_BUTTON, True)

        self.btn_biglietteria = QPushButton("Biglietteria")
        self.btn_biglietteria.setProperty(QssStyle.BLUE_BUTTON, True)
        self.btn_biglietteria.setProperty(QssStyle.MAIN_BUTTON, True)

        self.btn_admin = QPushButton("Amministratore")
        self.btn_admin.setProperty(QssStyle.BLUE_BUTTON, True)
        self.btn_admin.setProperty(QssStyle.MAIN_BUTTON, True)

        self.pulsanti_utente = QWidget()
        layout_pulsanti_utente = QVBoxLayout(self.pulsanti_utente)
        layout_pulsanti_utente.addWidget(self.btn_cliente)
        layout_pulsanti_utente.addWidget(self.btn_biglietteria)
        layout_pulsanti_utente.addWidget(self.btn_admin)

        # Layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        main_layout.addWidget(header)
        main_layout.addWidget(subheader)
        main_layout.addWidget(self.pulsanti_utente)
        main_layout.addStretch()
