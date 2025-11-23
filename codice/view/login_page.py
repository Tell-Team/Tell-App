from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt
from functools import partial

from view.navigation import NavigationController

from view.info_page import InfoPage


class LogInPage(QWidget):
    def __init__(self, nav: NavigationController):
        super().__init__()

        # # CONTENT
        # ## Header
        header = QLabel("Login")
        header.setObjectName("Header1")
        header.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # ## Subheader
        subheader = QLabel("Scegliere il tipo di account:")
        subheader.setObjectName("Paragraph")
        subheader.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # ## Pulsanti
        btn_cliente = QPushButton("Cliente")
        btn_cliente.setObjectName("BlueButton")
        btn_cliente.clicked.connect(partial(nav.go_to, InfoPage))  # type:ignore

        btn_biglietteria = QPushButton("Biglietteria")
        btn_biglietteria.setObjectName("BlueButton")
        btn_biglietteria.clicked.connect(  # type:ignore
            partial(nav.go_to, InfoPage)
        )  # DA CORRIGERE: utente ancora non implementati

        btn_admin = QPushButton("Amministratore")
        btn_admin.setObjectName("BlueButton")
        btn_admin.clicked.connect(  # type:ignore
            partial(nav.go_to, InfoPage)
        )  # DA CORRIGERE: Ruoli utente ancora non implementati

        pulsanti_utente = QWidget()
        layout_pulsanti_utente = QVBoxLayout(pulsanti_utente)
        layout_pulsanti_utente.addWidget(btn_cliente)
        layout_pulsanti_utente.addWidget(btn_biglietteria)
        layout_pulsanti_utente.addWidget(btn_admin)

        #
        #
        #

        # # MAIN LAYOUT
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        main_layout.addWidget(header)
        main_layout.addWidget(subheader)
        main_layout.addWidget(pulsanti_utente)
        main_layout.addStretch()

        # DA CORRIGERE: Non c'è uno stato default per ogni volta che un cliente accede all'app
