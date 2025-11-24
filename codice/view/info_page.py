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


class InfoPage(QWidget):
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
        btn_sezione_info.setEnabled(False)

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

        # # OPERE HEADER
        # ## Header
        header_opere = QLabel("Opere")
        header_opere.setObjectName("Header1")
        header_opere.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # ## Pulsante: Nuova opera
        btn_nuova_opera = QPushButton("Nuova opera")
        btn_nuova_opera.setObjectName("SmallButton")
        btn_nuova_opera.clicked.connect(  # type:ignore
            partial(OperaController.crea_opera, gestore_opere)
        )
        # ## Layout: Header Opere
        layout_header_opere = QHBoxLayout()
        layout_header_opere.addWidget(header_opere)
        layout_header_opere.addWidget(btn_nuova_opera)
        layout_header_opere.addStretch()

        # # OPERE DISPLAY
        layout_lista_opere = QVBoxLayout()
        for opera in gestore_opere.get_lista_opere():
            # ## Labels
            nome = QLabel(f"{opera.get_nome()}")
            nome.setObjectName("Header2")

            librettista = QLabel(f"Libretto di {opera.get_librettista()}")
            librettista.setObjectName("Paragraph")

            compositore = QLabel(f"Musica di {opera.get_compositore()}")
            compositore.setObjectName("Paragraph")

            # ## Pulsanti
            btn_visualizza = QPushButton("Maggior info")
            btn_visualizza.setObjectName("SmallButton")
            btn_visualizza.clicked.connect(  # type:ignore
                partial(OperaController.visualizza_opera, opera)
            )

            btn_modifica = QPushButton("Modifica")
            btn_modifica.setObjectName("SmallButton")
            btn_modifica.clicked.connect(  # type:ignore
                partial(OperaController.modifica_opera, gestore_opere, opera.get_id())
            )

            pulsanti = QWidget()
            temp_layout_btn = QHBoxLayout(pulsanti)
            temp_layout_btn.addWidget(btn_visualizza)
            temp_layout_btn.addWidget(btn_modifica)
            temp_layout_btn.addStretch()

            # ## Layout
            current_opera = QWidget()
            current_opera.setObjectName("Container")
            layout_cur_opera = QVBoxLayout(current_opera)

            layout_cur_opera.addWidget(nome)
            layout_cur_opera.addWidget(librettista)
            layout_cur_opera.addWidget(compositore)
            layout_cur_opera.addWidget(pulsanti)

            layout_lista_opere.addWidget(current_opera)

        # # LAYOUT OPERE : Header Opere + OPERE DISPLAY
        container_opere = QWidget()
        layout_opere = QVBoxLayout(container_opere)
        layout_opere.addLayout(layout_header_opere)
        layout_opere.addLayout(layout_lista_opere)

        #
        #
        #

        # # GENERI HEADER
        # ## Header
        header_generi = QLabel("Generi")
        header_generi.setObjectName("Header1")
        header_generi.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # ## Pulsante: Nuovo genere
        btn_nuovo_genere = QPushButton("Nuovo genere")
        btn_nuovo_genere.setObjectName("SmallButton")
        btn_nuovo_genere.clicked.connect(  # type:ignore
            partial(GenereController.crea_genere, gestore_generi)
        )

        # ## Layout: Header Generi
        layout_header_generi = QHBoxLayout()
        layout_header_generi.addWidget(header_generi)
        layout_header_generi.addWidget(btn_nuovo_genere)
        layout_header_generi.addStretch()

        # # GENERI DISPLAY
        layout_lista_generi = QVBoxLayout()
        for genere in gestore_generi.get_lista_generi():
            # ## Labels
            nome = QLabel(f"{genere.get_nome()}")
            nome.setObjectName("Header2")

            descrizione = QLabel(f"{genere.get_descrizione()}")
            descrizione.setObjectName("Paragraph")
            descrizione.setWordWrap(True)

            # Pulsanti
            btn_modifica = QPushButton("Modifica")
            btn_modifica.setObjectName("SmallButton")
            btn_modifica.clicked.connect(  # type:ignore
                partial(
                    GenereController.modifica_genere, gestore_generi, genere.get_id()
                )
            )

            pulsanti = QWidget()
            temp_layout_btn = QHBoxLayout(pulsanti)
            temp_layout_btn.addWidget(btn_modifica)
            temp_layout_btn.addStretch()

            # ## Layout
            current_genere = QWidget()
            current_genere.setObjectName("Container")
            layout_cur_genere = QVBoxLayout(current_genere)

            layout_cur_genere.addWidget(nome)
            layout_cur_genere.addWidget(descrizione)
            layout_cur_genere.addWidget(pulsanti)

            layout_lista_generi.addWidget(current_genere)

        # # LAYOUT GENERI : Header Generi + GENERI DISPLAY
        container_generi = QWidget()
        layout_generi = QVBoxLayout(container_generi)
        layout_generi.addLayout(layout_header_generi)
        layout_generi.addLayout(layout_lista_generi)

        #
        #
        #

        # # TEATRO
        # ## Header Teatro
        header_teatro = QLabel("Teatro")
        header_teatro.setObjectName("Header1")
        header_teatro.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # ## Informazioni Teatro
        teatro_nome = QLabel("Vitrifrigo Arena")
        teatro_nome.setObjectName("Header2")

        teatro_desc = QLabel(
            "Inaugurato nel 1996\nVia R. Ripa, 1\nLa Vitrifrigo Arena è un'ampio palazzetto che ospita numerosi eventi sportivi e musicali di rilevanza mondiale. In occasione dello Rossini Opera Festival, viene allestita una struttura in legno al suo interno per ricreare l'esperienza acustica di un teatro tradizionale."
        )
        teatro_desc.setObjectName("Paragraph")
        teatro_desc.setWordWrap(True)

        info_teatro = QWidget()
        info_teatro.setObjectName("Container")
        layout_info_teatro = QVBoxLayout(info_teatro)
        layout_info_teatro.addWidget(teatro_nome)
        layout_info_teatro.addWidget(teatro_desc)

        # ## LAYOUT TEATRO : Header Teatro + Informazioni Teatro
        container_teatro = QWidget()
        layout_teatro = QVBoxLayout(container_teatro)
        layout_teatro.addWidget(header_teatro)
        layout_teatro.addWidget(info_teatro)

        #
        #
        #

        # # FUNZIONE DI SCROLL
        # ## Scroll Layout
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        scroll_layout.addWidget(container_opere)
        scroll_layout.addWidget(container_generi)
        scroll_layout.addWidget(container_teatro)

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
#   OperaController.crea_opera(gestore: GestoreOpere) @line_87
#   GestoreOpere.get_lista_opere() @line_97
#   OperaController.visualizza_opera(opera: Opera) @line_112
#   OperaController.modifica_opera(gestore: GestoreOpere, id_opera: int) @line_118
#   GenereController.crea_genere(gestore: GestoreGenere) @line_159
#   GestoreGeneri.get_lista_generi() @line_170
#   GenereController.modifica_genere(gestore: GestoreGeneri, id_genere: int) @line_183
