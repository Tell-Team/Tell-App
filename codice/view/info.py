from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QScrollArea,
)
from PyQt6.QtCore import Qt
from functools import partial

from view.navigation import NavigationController

from model.pianificazione.opera import Opera
from model.pianificazione.genere import Genere
from model.gestori.gestore_opere import GestoreOpere
from model.gestori.gestore_generi import GestoreGeneri

from view.spettacoli_test import SpettacoliPage  ### TESTING ###
from view.account_test import AccountPage  ### TESTING ###

# from view.nuova_opera import FormularioOpera
from datetime import date  ### TESTING ###


class InfoPage(QWidget):
    def __init__(self, nav: NavigationController):
        super().__init__()

        """### TESTING ###"""
        gestore_generi = GestoreGeneri()
        genere_test1 = Genere(
            "Opera seria",
            "Genere dell'opera italiana. Si contrappone storicamente al genere dell'opera buffa, al punto tale che la decadenza di quest'ultima, nel corso del XIX secolo, finì per renderne prima incerti, poi irriconoscibili i contorni. I temi portanti dell'opera seria sono il dramma e le passioni umane con storie e personaggi tratti dalla mitologia, dall'epica cavalleresca e dalla storia antica o medievale.",
        )
        genere_test2 = Genere("Genere_sample", "descrizione_sample")
        gestore_generi.aggiungi_genere(genere_test1)
        gestore_generi.aggiungi_genere(genere_test2)

        opera_test1 = Opera(
            "Zelmira",
            "Gioachino Rossini",
            "Andrea Leone Tottola",
            2,
            date(1822, 2, 6),
            "Teatro Rossini",
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            0,
        )
        opera_test2 = Opera(
            "Opera_sample",
            "compositore_sample",
            "librettista_sample",
            1,
            date(1999, 1, 1),
            "teatro_sample",
            "trama_sample",
            1,
        )

        gestore_opere = GestoreOpere(gestore_generi)
        gestore_opere.aggiungi_opera(opera_test1)
        gestore_opere.aggiungi_opera(opera_test2)
        """### TESTING ###"""

        # LAYOUT LOGOUT
        ## Pulsante: Logout
        btn_logout = QPushButton("Logout")
        btn_logout.setObjectName("SmallButton")
        btn_logout.clicked.connect(nav.go_back)  # type:ignore

        layout_logout = QHBoxLayout()
        layout_logout.addWidget(btn_logout)
        layout_logout.addStretch()

        # LAYOUT SEZIONI DELL'APP
        ## Pulsante: Sezione Spettacoli
        btn_sezione_spettacoli = QPushButton("Spettacoli")
        btn_sezione_spettacoli.setObjectName("SmallButton")
        btn_sezione_spettacoli.clicked.connect(partial(nav.go_to, SpettacoliPage))
        # <-- Creare un file spettacoli.py con la classe SpettacoliPage --!>

        ## Pulsante: Sezioni Info
        btn_sezione_info = QPushButton("Info")
        btn_sezione_info.setObjectName("SmallButton")
        btn_sezione_info.setEnabled(False)

        ## Pulsante: Sezione Account (ESCLUSIVO PER ADMIN)
        btn_sezione_account = QPushButton("Account")  # CORREGIR
        btn_sezione_account.setObjectName("SmallButton")
        btn_sezione_account.clicked.connect(partial(nav.go_to, AccountPage))
        # <-- Creare un file account.py con la classe AccountPage --!>

        layout_sezioni = QHBoxLayout()
        layout_sezioni.addWidget(btn_sezione_spettacoli)
        layout_sezioni.addWidget(btn_sezione_info)
        layout_sezioni.addWidget(btn_sezione_account)
        layout_sezioni.addStretch()

        # TOP LAYOUT
        container_top = QWidget()
        layout_top = QVBoxLayout(container_top)
        layout_top.addLayout(layout_logout)
        layout_top.addSpacing(15)
        layout_top.addLayout(layout_sezioni)

        # LAYOUT OPERE
        header_opere = QLabel("Opere")
        header_opere.setObjectName("Header1")
        header_opere.setAlignment(Qt.AlignmentFlag.AlignLeft)

        ## Pulsante: Nuova opera
        btn_nuova_opera = QPushButton("Nuova opera")
        btn_nuova_opera.setObjectName("SmallButton")
        btn_nuova_opera.clicked.connect(
            partial(OperaController.crea_opera, gestore_opere)
        )
        # <-- Implementare una funzione OperaController.crea_opera(gestore: GestoreOpere) --!>

        layout_header_opere = QHBoxLayout()
        layout_header_opere.addWidget(header_opere)
        layout_header_opere.addStretch()
        layout_header_opere.addWidget(btn_nuova_opera)

        # Display delle opere
        layout_lista_opere = QVBoxLayout()
        for opera in gestore_opere.get_lista_opere():
            container = QWidget()
            container.setObjectName("Container")
            layout_box = QVBoxLayout(container)

            nome = QLabel(f"{opera.get_nome()}")
            nome.setObjectName("Header2")
            layout_box.addWidget(nome)

            librettista = QLabel(f"Libretto di {opera.get_librettista()}")
            librettista.setObjectName("Paragraph")
            layout_box.addWidget(librettista)

            compositore = QLabel(f"Musica di {opera.get_compositore()}")
            compositore.setObjectName("Paragraph")
            layout_box.addWidget(compositore)

            temp_layout_btn = QHBoxLayout()

            btn_visualizza = QPushButton("Maggior info")
            btn_visualizza.setObjectName("SmallButton")
            btn_visualizza.clicked.connect(
                partial(OperaController.visualizza_opera, opera.get_id())
            )
            # <-- Implementare una funzione OperaController.visualizza_opera(id: int) --!>
            temp_layout_btn.addWidget(btn_visualizza)

            btn_modifica = QPushButton("Modifica")
            btn_modifica.setObjectName("SmallButton")
            btn_modifica.clicked.connect(
                partial(OperaController.modifica_opera, opera.get_id())
            )
            # <-- Implementare una funzione OperaController.modifica_opera(id: int) --!>
            temp_layout_btn.addWidget(btn_modifica)
            temp_layout_btn.addStretch()

            layout_box.addLayout(temp_layout_btn)

            layout_lista_opere.addWidget(container)

        container_opere = QWidget()
        layout_opere = QVBoxLayout(container_opere)
        layout_opere.addLayout(layout_header_opere)
        layout_opere.addLayout(layout_lista_opere)

        # LAYOUT GENERI
        header_generi = QLabel("Generi")
        header_generi.setObjectName("Header1")
        header_generi.setAlignment(Qt.AlignmentFlag.AlignLeft)

        ## Pulsante: Nuovo genere
        btn_nuovo_genere = QPushButton("Nuovo genere")
        btn_nuovo_genere.setObjectName("SmallButton")
        btn_nuovo_genere.clicked.connect(
            partial(GenereController.crea_genere, gestore_generi)
        )
        # <-- Implementare una funzione GenereController.crea_genere(gestore: GestoreGenere) --!>

        layout_header_generi = QHBoxLayout()
        layout_header_generi.addWidget(header_generi)
        layout_header_generi.addStretch()
        layout_header_generi.addWidget(btn_nuovo_genere)

        ## Display dei generi
        layout_lista_generi = QVBoxLayout()
        for genere in gestore_generi.get_lista_generi():
            container = QWidget()
            container.setObjectName("Container")
            layout_box = QVBoxLayout(container)

            nome = QLabel(f"{genere.get_nome()}")
            nome.setObjectName("Header2")
            layout_box.addWidget(nome)

            descrizione = QLabel(f"{genere.get_descrizione()}")
            descrizione.setObjectName("Paragraph")
            descrizione.setWordWrap(True)
            layout_box.addWidget(descrizione)

            temp_layout_btn = QHBoxLayout()

            btn_modifica = QPushButton("Modifica")
            btn_modifica.setObjectName("SmallButton")
            btn_modifica.clicked.connect(
                partial(GenereController.modifica_genere, genere.get_id())
            )
            # <-- Implementare una funzione GenereController.modifica_genere(id: int) --!>
            temp_layout_btn.addWidget(btn_modifica)
            temp_layout_btn.addStretch()
            layout_box.addLayout(temp_layout_btn)

            layout_lista_generi.addWidget(container)

        container_generi = QWidget()
        layout_generi = QVBoxLayout(container_generi)
        layout_generi.addLayout(layout_header_generi)
        layout_generi.addLayout(layout_lista_generi)

        # LAYOUT TEATRO
        header_teatro = QLabel("Teatro")
        header_teatro.setObjectName("Header1")
        header_teatro.setAlignment(Qt.AlignmentFlag.AlignLeft)

        box_teatro = QWidget()
        box_teatro.setObjectName("Container")
        layout_box_teatro = QVBoxLayout(box_teatro)

        teatro_nome = QLabel("Vitrifrigo Arena")
        teatro_nome.setObjectName("Header2")
        layout_box_teatro.addWidget(teatro_nome)

        teatro_desc = QLabel(
            "Inaugurato nel 1996\nVia R. Ripa, 1\nLa Vitrifrigo Arena è un'ampio palazzetto che ospita numerosi eventi sportivi e musicali di rilevanza mondiale. In occasione dello Rossini Opera Festival, viene allestita una struttura in legno al suo interno per ricreare l'esperienza acustica di un teatro tradizionale."
        )
        teatro_desc.setObjectName("Paragraph")
        teatro_desc.setWordWrap(True)
        layout_box_teatro.addWidget(teatro_desc)

        container_teatro = QWidget()
        layout_teatro = QVBoxLayout(container_teatro)
        layout_teatro.addWidget(header_teatro)
        layout_teatro.addWidget(box_teatro)

        # FUNZIONE DI SCROLL
        ## SCROLL WIDGET
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        scroll_layout.addWidget(container_opere)
        scroll_layout.addWidget(container_generi)
        scroll_layout.addWidget(container_teatro)

        ## SCROLL AREA
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)

        # MAIN LAYOUT
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(container_top)
        main_layout.addWidget(scroll_area)
