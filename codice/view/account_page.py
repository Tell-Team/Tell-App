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


class AccountPage(QWidget):
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
            partial(nav.section_go_to, SpettacoliPage)
        )

        # ## Pulsante: Sezioni Info
        btn_sezione_info = QPushButton("Info")
        btn_sezione_info.setObjectName("SmallButton")
        from view.info_page import InfoPage

        btn_sezione_info.clicked.connect(  # type:ignore
            partial(nav.section_go_to, InfoPage)
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

        # # ACCOUNT HEADER
        # ## Header
        header_account = QLabel("Account")
        header_account.setObjectName("Header1")
        header_account.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # ## Layout: Header Account
        layout_header_account = QHBoxLayout()
        layout_header_account.addWidget(header_account)
        layout_header_account.addStretch()

        #
        #
        #

        # ## ADMIN HEADER
        # ### Header
        header_admin = QLabel("Amministratore")
        header_admin.setObjectName("Header2")
        header_admin.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # ### Pulsante: Nuovo Admin
        btn_nuovo_admin = QPushButton("Nuovo amministratore")
        btn_nuovo_admin.setObjectName("SmallButton")
        btn_nuovo_admin.clicked.connect(  # type:ignore
            partial(
                AccountController.crea_account,
                gestore_account,
                Ruolo.AMMINISTRATORE,
            )
        )

        # ### Layout: Header Admin
        layout_header_admin = QHBoxLayout()
        layout_header_admin.addWidget(header_admin)
        layout_header_admin.addWidget(btn_nuovo_admin)
        layout_header_admin.addStretch()

        # ## ADMIN DISPLAY
        lista_admin = QWidget()
        layout_lista_admin = QVBoxLayout(lista_admin)
        for admin in (
            a
            for a in gestore_account.get_lista_account()
            if a.get_ruolo() == Ruolo.AMMINISTRATORE
        ):
            # ### Labels
            username = QLabel(f"{admin.get_username()}")
            username.setObjectName("Header3")
            username.setAlignment(Qt.AlignmentFlag.AlignLeft)

            # ### Pulsanti
            btn_modifica = QPushButton("Modifica")
            btn_modifica.setObjectName("SmallButton")
            btn_modifica.clicked.connect(  # type:ignore
                partial(
                    AccountController.modifica_account, gestore_account, admin.get_id()
                )
            )

            btn_elimina = QPushButton("Rimuovi")
            btn_elimina.setObjectName("SmallButton")
            btn_elimina.clicked.connect(  # type:ignore
                partial(
                    AccountController.elimina_account, gestore_account, admin.get_id()
                )
            )

            pulsanti = QWidget()
            temp_layout_btn = QHBoxLayout(pulsanti)
            temp_layout_btn.addWidget(btn_modifica)
            temp_layout_btn.addStretch()

            # ### Layout
            current_admin = QWidget()
            layout_cur_admin = QHBoxLayout(current_admin)

            layout_cur_admin.addWidget(username)
            layout_cur_admin.addWidget(pulsanti)

            layout_lista_admin.addWidget(current_admin)

        # ## LAYOUT ADMIN : Header Admin + ADMIN DISPLAY
        container_admin = QWidget()
        layout_admin = QVBoxLayout(container_admin)
        layout_admin.addLayout(layout_header_admin)
        layout_admin.addLayout(layout_lista_admin)

        #
        #
        #

        # ## BIGLIETTERIA HEADER
        # ### Header
        header_biglietteria = QLabel("Biglietteria")
        header_biglietteria.setObjectName("Header2")
        header_biglietteria.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # ### Pulsante: Nuova Biglietteria
        btn_nuovo_biglietteria = QPushButton("Nuova Biglietteria")
        btn_nuovo_biglietteria.setObjectName("SmallButton")
        btn_nuovo_biglietteria.clicked.connect(  # type:ignore
            partial(
                AccountController.crea_account,
                gestore_account,
                Ruolo.BIGLIETTERIA,
            )
        )

        # ### Layout: Header Biglietteria
        layout_header_biglietteria = QHBoxLayout()
        layout_header_biglietteria.addWidget(header_biglietteria)
        layout_header_biglietteria.addWidget(btn_nuovo_biglietteria)
        layout_header_biglietteria.addStretch()

        # ## BIGLIETTERIE DISPLAY
        lista_biglietterie = QWidget()
        layout_lista_biglietterie = QVBoxLayout(lista_biglietterie)
        for biglietteria in (
            b
            for b in gestore_account.get_lista_account()
            if b.get_ruolo() == Ruolo.BIGLIETTERIA
        ):
            # ### Labels
            username = QLabel(f"{biglietteria.get_username()}")
            username.setObjectName("Header3")
            username.setAlignment(Qt.AlignmentFlag.AlignLeft)

            # ### Pulsanti
            btn_modifica = QPushButton("Modifica")
            btn_modifica.setObjectName("SmallButton")
            btn_modifica.clicked.connect(  # type:ignore
                partial(
                    AccountController.modifica_account,
                    gestore_account,
                    biglietteria.get_id(),
                )
            )

            btn_elimina = QPushButton("Rimuovi")
            btn_elimina.setObjectName("SmallButton")
            btn_elimina.clicked.connect(  # type:ignore
                partial(
                    AccountController.elimina_account,
                    gestore_account,
                    biglietteria.get_id(),
                )
            )

            pulsanti = QWidget()
            temp_layout_btn = QHBoxLayout(pulsanti)
            temp_layout_btn.addWidget(btn_modifica)
            temp_layout_btn.addStretch()

            # ### Layout
            current_biglietteria = QWidget()
            layout_cur_biglietteria = QHBoxLayout(current_biglietteria)

            layout_cur_biglietteria.addWidget(username)
            layout_cur_biglietteria.addWidget(pulsanti)

            layout_lista_biglietterie.addWidget(current_biglietteria)

        # ## LAYOUT BIGLIETTERIA : Header Biglietteria + BIGLIETTERIE DISPLAY
        container_biglietterie = QWidget()
        layout_biglietterie = QVBoxLayout(container_biglietterie)
        layout_biglietterie.addLayout(layout_header_biglietteria)
        layout_biglietterie.addLayout(layout_lista_biglietterie)

        #
        #
        #

        # # LAYOUT ACCOUNT : Header Account + LAYOUT ADMIN + LAYOUT BIGLIETTERIA
        container_account = QWidget()
        layout_account = QVBoxLayout(container_account)
        layout_account.addLayout(layout_header_account)
        layout_account.addLayout(layout_admin)
        layout_account.addLayout(layout_biglietterie)
        layout_account.addStretch()

        #
        #
        #

        # # FUNZIONE DI SCROLL
        # ## Scroll Layout
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        scroll_layout.addWidget(container_account)

        # ## Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)

        #
        #
        #

        # # MAIN LAYOUT
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(container_top)
        main_layout.addWidget(scroll_area)


# Funzioni implementate dal controller e dal gestore:
#   AccountController.crea_account(gestore: GestoreAccount, ruolo:Ruolo) @line_104 @line_181
#   GestoreAccount.get_lista_account() @line_121 @line_198
#   AccountController.modifica_account(gestore: GestoreAccount, id_account: int) @line_133 @line_211
#   AccountController.elimina_account(gestore: GestoreAccount, id_account: int) @line_142 @line_221

# NOTA: modifica_account() ed elimina_account() potrebbero usare il ruolo come parametro
#       per distinguere il modo di uso degli account admin e degli account biglietteria.
