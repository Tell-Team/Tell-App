from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
)
from PyQt6.QtCore import Qt
from functools import partial

from view.navigation import NavigationController


class SpettacoliPage(QWidget):
    def __init__(self, nav: NavigationController):
        super().__init__()

        # # LOGOUT
        # ## Pulsante: Logout
        btn_logout = QPushButton("Logout")
        btn_logout.setObjectName("SmallButton")
        btn_logout.clicked.connect(  # type:ignore
            nav.go_back
        )

        # ## Layout: Logout
        widget_logout = QWidget()
        layout_logout = QHBoxLayout(widget_logout)
        layout_logout.addWidget(btn_logout)
        layout_logout.addStretch()

        # # SEZIONI DELL'APP
        # ## Pulsante: Sezione Spettacoli
        btn_sezione_spettacoli = QPushButton("Spettacoli")
        btn_sezione_spettacoli.setObjectName("SmallButton")
        from view.spettacoli_page import SpettacoliPage

        btn_sezione_spettacoli.clicked.connect(  # type:ignore
            partial(nav.go_to, SpettacoliPage)
        )

        # ## Pulsante: Sezioni Info
        btn_sezione_info = QPushButton("Info")
        btn_sezione_info.setObjectName("SmallButton")
        from view.info_page import InfoPage

        btn_sezione_info.clicked.connect(  # type:ignore
            partial(nav.go_to, InfoPage)
        )

        # ## Pulsante: Sezione Account
        btn_sezione_account = QPushButton(
            "Account"
        )  # DA CORRIGERE: Sezione esclusiva dell'admin
        btn_sezione_account.setObjectName("SmallButton")
        btn_sezione_account.setEnabled(False)

        # ## Layout: Sezioni App
        sezioni_app = QWidget()
        layout_sezioni = QHBoxLayout(sezioni_app)
        layout_sezioni.addWidget(btn_sezione_spettacoli)
        layout_sezioni.addWidget(btn_sezione_info)
        layout_sezioni.addWidget(btn_sezione_account)
        layout_sezioni.addStretch()

        # # TOP LAYOUT : Logout + Sezioni App
        container_top = QWidget()
        layout_top = QVBoxLayout(container_top)
        layout_top.addWidget(widget_logout)
        layout_top.addSpacing(15)
        layout_top.addWidget(sezioni_app)

        #
        #
        #

        # DA CORRIGERE: File ancora non completo
