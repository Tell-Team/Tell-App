from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt
from functools import partial

from view.navigation import NavigationController


# COPIA DI login.py. NON E' FUNZIONALE
class SpettacoliPage(QWidget):
    def __init__(self, nav: NavigationController):
        super().__init__()

        header = QLabel("Login")
        header.setObjectName("Header1")
        header.setAlignment(Qt.AlignmentFlag.AlignLeft)

        subheader = QLabel("Scegliere il tipo di account:")
        subheader.setObjectName("Paragraph")
        subheader.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Pulsante: Utente Cliente
        btn_cliente = QPushButton("Cliente")
        btn_cliente.setObjectName("BlueButton")
        btn_cliente.clicked.connect(partial(nav.go_to, InfoPage))  # type:ignore

        # Pulsante: Utente Biglietteria
        btn_biglietteria = QPushButton("Biglietteria")
        btn_biglietteria.setObjectName("BlueButton")
        btn_biglietteria.clicked.connect(partial(nav.go_to, InfoPage))  # type:ignore
        # CORREGIR

        # Pulsante: Utente Amministratore
        btn_admin = QPushButton("Amministratore")
        btn_admin.setObjectName("BlueButton")
        btn_admin.clicked.connect(partial(nav.go_to, InfoPage))  # type:ignore
        # CORREGIR

        """ MAIN LAYOUT """
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        layout.addWidget(header)
        layout.addWidget(subheader)
        layout.addWidget(btn_cliente)
        layout.addWidget(btn_biglietteria)
        layout.addWidget(btn_admin)
        layout.addStretch()

        self.setLayout(layout)

        # OBVIAMENTE NO UTILIZA ACCOUNTS PARA SEPARAR LAS PESTAÑAS.
        # NO EXISTE ESTADO BASE PARA CADA QUE SE ENTRA COMO CLIENTE
