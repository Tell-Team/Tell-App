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


from controller.info_controller import InfoController


class InfoPage(QWidget):
    """
    Pagina principale della sezione Info dell'applicazione. Contiene l'interfaccia utente per
    interaggire con le istanze di `Opera`, `Regia` e `Genere` e una sezione in fondo con le
    informazioni del teatro.

    """

    def __init__(self, info_controller: InfoController):
        super().__init__()

        self.info_controller = info_controller

        self._build_ui()

    def _build_ui(self):
        # # LOGOUT
        # ## Pulsante: Logout
        btn_logout = QPushButton("Logout")
        btn_logout.setObjectName("SmallButton")
        btn_logout.clicked.connect(  # type:ignore
            self.info_controller.get_nav().go_back
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
        btn_sezione_spettacoli.clicked.connect(  # type:ignore
            partial(self.info_controller.get_nav().section_go_to, "spettacoli")
        )
        # ## Pulsante: Sezioni Info
        btn_sezione_info = QPushButton("Info")
        btn_sezione_info.setObjectName("SmallButton")
        btn_sezione_info.setEnabled(False)

        # ## Pulsante: Sezione Account
        btn_sezione_account = QPushButton(
            "Account"
        )  # - Questa sezione deve essere esclusiva dell'admin
        btn_sezione_account.setObjectName("SmallButton")
        btn_sezione_account.clicked.connect(  # type:ignore
            partial(self.info_controller.get_nav().section_go_to, "account")
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
            lambda: print(
                "self.info_controller.nuova_opera"
            )  # - self.info_controller.nuova_opera
        )
        # ## Layout: Header Opere
        layout_header_opere = QHBoxLayout()
        layout_header_opere.addWidget(header_opere)
        layout_header_opere.addWidget(btn_nuova_opera)
        layout_header_opere.addStretch()

        # # OPERE DISPLAY
        layout_lista_opere = QVBoxLayout()
        self.display_opere_widget(layout_lista_opere)

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
            lambda: print(
                "self.info_controller.nuovo_genere"
            )  # - self.info_controller.nuovo_genere
        )

        # ## Layout: Header Generi
        layout_header_generi = QHBoxLayout()
        layout_header_generi.addWidget(header_generi)
        layout_header_generi.addWidget(btn_nuovo_genere)
        layout_header_generi.addStretch()

        # # GENERI DISPLAY
        layout_lista_generi = QVBoxLayout()
        self.display_generi_widget(layout_lista_generi)

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

    def display_opere_widget(self, layout: QVBoxLayout):
        for opera in self.info_controller.get_opere():
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
                lambda: print(
                    "partial(self.info_controller.visualizza_opera, opera.get_id())"
                )  # - partial(self.info_controller.visualizza_opera, opera.get_id())
            )

            btn_modifica = QPushButton("Modifica")
            btn_modifica.setObjectName("SmallButton")
            btn_modifica.clicked.connect(  # type:ignore
                lambda: print(
                    "partial(self.info_controller.modifica_opera, opera.get_id())"
                )  # - partial(self.self.info_controller.modifica_opera, opera.get_id())
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

            layout.addWidget(current_opera)

    def display_generi_widget(self, layout: QVBoxLayout):
        for genere in self.info_controller.get_generi():
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
                lambda: print(
                    "partial(self.info_controller.modifica_genere, genere.get_id())"
                )  # - partial(self.info_controller.modifica_genere, genere.get_id())
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

            layout.addWidget(current_genere)


# - Funzioni implementate dal controller e dal gestore:
#   InfoController.nuova_opera()
#       Carica la pagina FormularioNuovaOpera, dove l'utente può cancellare l'operazione
#       tornando dietro utilizando .cancella_opera(is_new=True) o confermare la creazione, chiamando
#       altro metodo .salva_opera(), che verifica la correttezza dei dati, crea l'istanza di Opera e
#       la salva nella lista di opere. (Anche riscrive i campi di input per prossime chiamate sia
#       dopo cancellare che dopo salvare)

#   InfoController.visualizza_opera(id_opera: int)
#       Utilizando il NavigationCotroller, il controller assegna i valori necessari dell'opera
#       relativa all'id in VisualizzaOpera (visualizza_opera.py).

#   InfoController.modifica_opera(id_opera: int)
#       Carica la pagina FormularioModificaOpera, con i dati dell'opera `id_opera` nei campo di
#       input. Il pulsante Conferma chiama la stessa funzione .salva_opera(is_new=False), ma con
#       altra opzione che permette di modificare i dati dell'opera esistente e creare regie
#       (necessarie per salvare la modifica), mentre che il pulsante Cancella elimina le regie se
#       non salvate e torna dietro con .cancella_opera(is_new=False) (non è necessario riscrivere
#       i campi di inpu perché sarano riscritti con la prossima chiamata).

#   InfoController.nuovo_genere()
#       Fa essenzialmente lo stesso che .nuova_opera(), ma con la pagina FormularioNuovoGenere.

#   InfoController.modifica_genere(id_genere: int)
#       Come .nuovo_genere(), questa è altra versione di .modifica_opera(). Il piccolo dettaglio è
#       che non è necessario un .cancella_genere(is_new=False) perché non vengono aggiunti nuovi
#       campi dopo la sua creazione (come sì occorre con le opere e gli spettacoli)
