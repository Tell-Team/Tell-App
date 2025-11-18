from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QScrollArea,
)

from navigation import NavigationController

from PyQt6.QtCore import Qt
from functools import partial

from classi.opera import Opera  ### TESTING ###
from classi.genere import Genere  ### TESTING ###
from ui.nuova_opera import FormularioOpera
from datetime import date  ### TESTING ###


class InfoPage(QWidget):
    def __init__(self, nav: NavigationController):
        super().__init__()

        """### TESTING ###"""
        opera_test1 = Opera(
            "Zelmira",
            "Gioachino Rossini",
            "Andrea Leone Tottola",
            2,
            date(1822, 2, 6),
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        )
        opera_test2 = Opera(
            "Opera_sample",
            "compositore_sample",
            "librettista_sample",
            1,
            date(1999, 1, 1),
            "trama_sample",
        )
        lista_opere: list[Opera] = [opera_test1, opera_test2]

        genere_test1 = Genere("Opera seria", "Lorem ipsum")
        lista_generi: list[Genere] = [genere_test1]
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
        btn_sezione_spettacoli.clicked.connect(  # type:ignore
            lambda: label_vuoto.setText("Spettacoli")
        )  # CORREGIR

        ## Pulsante: Sezioni Info
        btn_sezione_info = QPushButton("Info")
        btn_sezione_info.setObjectName("SmallButton")
        btn_sezione_info.setEnabled(False)

        ## Pulsante: Sezione Account (ESCLUSIVO PER ADMIN)
        btn_sezione_account = QPushButton("Account")  # CORREGIR
        btn_sezione_account.setObjectName("SmallButton")
        btn_sezione_account.clicked.connect(  # type:ignore
            lambda: label_vuoto.setText("Account")
        )  # CORREGIR

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
        btn_nuova_opera.clicked.connect(  # type:ignore
            # lambda: label_vuoto.setText("Nuova opera")
            partial(nav.go_to, FormularioOpera)
        )  # CORREGIR

        layout_header_opere = QHBoxLayout()
        layout_header_opere.addWidget(header_opere)
        layout_header_opere.addStretch()
        layout_header_opere.addWidget(btn_nuova_opera)

        """### TESTING ###"""
        layout_lista_opere = QVBoxLayout()
        # Puedo hacer una función del tipo visualizza_opera() o display_opera() para pulir el código
        for opera in lista_opere:
            container = QWidget()
            container.setObjectName("Container")
            layout_box = QVBoxLayout(container)

            nome = QLabel(f"{opera.nome}")
            nome.setObjectName("Header2")
            layout_box.addWidget(nome)

            librettista = QLabel(f"<b>Librettista:</b> {opera.librettisa}")
            librettista.setObjectName("Paragraph")
            layout_box.addWidget(librettista)

            trama = QLabel(f"{opera.trama}")
            trama.setObjectName("Paragraph")
            trama.setWordWrap(True)
            layout_box.addWidget(trama)

            btn_modifica = QPushButton("Modifica")
            btn_modifica.setObjectName("SmallButton")
            temp_modifica = QHBoxLayout()
            temp_modifica.addWidget(btn_modifica)
            temp_modifica.addStretch()
            layout_box.addLayout(temp_modifica)

            layout_lista_opere.addWidget(container)

        container_opere = QWidget()
        layout_opere = QVBoxLayout(container_opere)
        layout_opere.addLayout(layout_header_opere)
        layout_opere.addLayout(layout_lista_opere)
        """### TESTING ###"""

        # LAYOUT GENERI
        header_generi = QLabel("Generi")
        header_generi.setObjectName("Header1")
        header_generi.setAlignment(Qt.AlignmentFlag.AlignLeft)

        ## Pulsante: Nuovo genere
        btn_nuovo_genere = QPushButton("Nuovo genere")
        btn_nuovo_genere.setObjectName("SmallButton")
        btn_nuovo_genere.clicked.connect(  # type:ignore
            lambda: label_vuoto.setText("Nuovo genere")
        )  # CORREGIR

        layout_header_generi = QHBoxLayout()
        layout_header_generi.addWidget(header_generi)
        layout_header_generi.addStretch()
        layout_header_generi.addWidget(btn_nuovo_genere)

        """### TESTING ###"""
        layout_lista_generi = QVBoxLayout()
        for genere in lista_generi:
            container = QWidget()
            container.setObjectName("Container")
            layout_box = QVBoxLayout(container)

            nome = QLabel(f"{genere.nome}")
            nome.setObjectName("Header2")
            layout_box.addWidget(nome)

            descrizione = QLabel(f"{genere.descrizione}")
            descrizione.setObjectName("Paragraph")
            layout_box.addWidget(descrizione)

            btn_modifica = QPushButton("Modifica")
            btn_modifica.setObjectName("SmallButton")
            temp_modifica = QHBoxLayout()
            temp_modifica.addWidget(btn_modifica)
            temp_modifica.addStretch()
            layout_box.addLayout(temp_modifica)

            layout_lista_generi.addWidget(container)

        container_generi = QWidget()
        layout_generi = QVBoxLayout(container_generi)
        layout_generi.addLayout(layout_header_generi)
        layout_generi.addLayout(layout_lista_generi)

        """### TESTING ###"""

        ## QUITAR ##
        label_vuoto = QLabel("Label vuoto")
        label_vuoto.setObjectName("Paragraph")
        label_vuoto.setAlignment(Qt.AlignmentFlag.AlignLeft)
        ## QUITAR ##

        """ SENZA SCROLL """
        # layout = QVBoxLayout()

        # layout.addWidget(container_top)
        # layout.addWidget(container_opere)
        # layout.addWidget(container_generi)
        # layout.addWidget(label_vuoto)
        # layout.addStretch()

        # self.setLayout(layout)

        """ SCROLL INCLUISO """
        # SCROLL WIDGET
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        scroll_layout.addWidget(container_opere)
        scroll_layout.addWidget(container_generi)
        scroll_layout.addWidget(label_vuoto)  # CORREGIR

        # SCROLL AREA
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)

        # MAIN LAYOUT
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(container_top)
        main_layout.addWidget(scroll_area)


# HACER MÉTODOS PARA crea_opera y crea_genere

# CORREGIR EL FUNCIONAMIENTO, FORMATO Y QUITAR EL label_vuoto EN LA nuova_opera()

# FALTA AGREGAR TEATRO
