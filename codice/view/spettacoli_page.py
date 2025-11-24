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
        btn_sezione_spettacoli.setEnabled(False)

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
        from view.account_page import AccountPage

        btn_sezione_account.clicked.connect(  # type:ignore
            partial(nav.section_go_to, AccountPage)
        )

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

        # # SPETTACOLI HEADER
        # ## Header
        header_spettacoli = QLabel("Spettacoli")
        header_spettacoli.setObjectName("Header1")
        header_spettacoli.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # ## Pulsante: Nuovo spettacoli
        btn_nuovo_spettacolo = QPushButton("Nuovo spettacoli")
        btn_nuovo_spettacolo.setObjectName("SmallButton")
        btn_nuovo_spettacolo.clicked.connect(  # type:ignore
            partial(SpettacoloController.crea_spettacolo, gestore_spettacoli)
        )

        # ## Layout: Header Spettacoli
        layout_header_spettacoli = QHBoxLayout()
        layout_header_spettacoli.addWidget(header_spettacoli)
        layout_header_spettacoli.addWidget(btn_nuovo_spettacolo)
        layout_header_spettacoli.addStretch()

        # # SPETTACOLI DISPLAY
        layout_lista_spettacoli = QVBoxLayout()
        for spettacolo in gestore_spettacoli.get_lista_spettacoli():
            # ## Labels
            titolo = QLabel(f"{spettacolo.get_titolo()}")
            titolo.setObjectName("Header2")

            cur_opera = gestore_opere.get_opera(spettacolo.get_id_opera())
            librettista = QLabel(f"Diretto di {cur_opera.get_librettista()}")
            librettista.setObjectName("Paragraph")

            cur_regia = gestore_regie.get_regia(cur_opera.get_id_regia())  # ???
            regia = QLabel(f"Regia di {cur_regia.get_regista()}")  # ???
            regia.setObjectName("Paragraph")

            # ## Pulsanti
            btn_scegli_posti = QPushButton("Scegli posti")
            btn_scegli_posti.setObjectName("SmallButton")
            btn_scegli_posti.clicked.connect(  # type:ignore
                partial(
                    SpettacoloController.scegli_posti,
                    gestore_spettacoli,
                    spettacolo.get_id(),
                )
            )

            btn_modifica = QPushButton("Modifica")
            btn_modifica.setObjectName("SmallButton")
            btn_modifica.clicked.connect(  # type:ignore
                partial(
                    ControllerSpettacoli.modifica_spettacolo,
                    gestore_spettacoli,
                    spettacolo.get_id(),
                )
            )

            pulsanti = QWidget()
            temp_layout_btn = QHBoxLayout(pulsanti)
            temp_layout_btn.addWidget(btn_scegli_posti)
            temp_layout_btn.addWidget(btn_modifica)
            temp_layout_btn.addStretch()

            # ## Layout
            current_spettacolo = QWidget()
            current_spettacolo.setObjectName("Container")
            layout_cur_spettacolo = QVBoxLayout(current_spettacolo)

            layout_cur_spettacolo.addWidget(titolo)
            layout_cur_spettacolo.addWidget(librettista)
            layout_cur_spettacolo.addWidget(regia)
            layout_cur_spettacolo.addWidget(pulsanti)

            layout_lista_spettacoli.addWidget(current_spettacolo)

        # # LAYOUT SPETTACOLI : Header Spettacoli + SPETTACOLI DISPLAY
        container_spettacoli = QWidget()
        layout_spettacoli = QVBoxLayout(container_spettacoli)
        layout_spettacoli.addLayout(layout_header_spettacoli)
        layout_spettacoli.addLayout(layout_lista_spettacoli)

        #
        #
        #

        # # FUNZIONE DI SCROLL
        # ## Scroll Layout
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        scroll_layout.addWidget(container_spettacoli)

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
#   SpettacoloController.crea_spettacolo(gestore: GestoreSpettacoli) @line_88
#   GestoreSpettacoli.get_lista_spettacoli() @line_99
#   GestoreOpera.get_opera(id_opera: int) @line_104
#   GestoreRegie.get_regia(id_regia: int) @line_108
#   SpettacoloController.scegli_posti(gestore: GestoreSpettacoli, id_spettacolo: int) @line_117
#   GestoreSpettacoli.modifica_spettacolo(gestore: GestoreSpettacoli, id_spettacolo: int) @line_127
