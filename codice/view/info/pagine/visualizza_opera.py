from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QScrollArea,
)
from PyQt6.QtCore import Qt, pyqtSignal

from controller.login.auth_service import AuthenticationService

from model.pianificazione.regia import Regia

from view.info.utils import OperaPageData

from view.utils.list_widgets import ListLayout, EmptyStateLabel
from view.utils.hyphenate_text import HyphenatedLabel
from view.utils import make_vline
from view.style import WidgetRole, WidgetColor


class VisualizzaOperaView(QWidget):
    """Pagina per visualizzare le singole `Opera` in dettaglio.

    Contiene le tutte informazioni dell'`Opera` ed una lista con tutte le `Regia`
    associate ad essa.

    Segnali
    ---
    - `tornaIndietroRequest()`: emesso quando si clicca il pulsante Indietro;
    - `displayRegieRequest(QVBoxLayout)`: emesso per mostrare la lista regie a schermo;
    - `nuovaRegiaRequest()`: emesso quando si clicca il pulsante Nuova regia.
    """

    tornaIndietroRequest = pyqtSignal()
    displayRegieRequest = pyqtSignal(QVBoxLayout)
    nuovaRegiaRequest = pyqtSignal()

    def __init__(self, auth: AuthenticationService):
        super().__init__()

        self.can_cud_regie = auth.is_admin()

        self._setup_ui()
        self._connect_signals()

    # ------------------------- SETUP INIT -------------------------

    def _setup_ui(self) -> None:
        self.id_cur_opera: int = -1

        # Top widget
        self.__btn_indietro = QPushButton("Indietro")
        self.__btn_indietro.setProperty(WidgetRole.DEFAULT_BUTTON, True)

        self.pagina_header = QWidget()
        layout_header = QHBoxLayout(self.pagina_header)
        layout_header.addWidget(self.__btn_indietro)
        layout_header.addStretch()

        # Labels
        self.label_nome = HyphenatedLabel("[Nome Opera]")
        self.label_nome.setProperty(WidgetRole.HEADER1, True)
        self.label_nome.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.label_librettista = HyphenatedLabel("Libretto di [Librettista Opera].")
        self.label_librettista.setProperty(WidgetRole.BODY_TEXT, True)
        self.label_librettista.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)

        self.label_compositore = HyphenatedLabel(
            "Musica composta da [Compositore Opera]."
        )
        self.label_compositore.setProperty(WidgetRole.BODY_TEXT, True)
        self.label_compositore.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)

        self.label_genere = HyphenatedLabel(f"Genere: [Genere Opera]")
        self.label_genere.setProperty(WidgetRole.BODY_TEXT, True)
        self.label_genere.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)

        self.label_atti = QLabel(f"Numero di atti: [Atti Opera]")
        self.label_atti.setProperty(WidgetRole.BODY_TEXT, True)
        self.label_atti.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)

        self.label_prima_rappresentazione = HyphenatedLabel(
            f"È stata rappresentata per prima volta il [Data Opera] nel teatro [Teatro Opera]."
        )
        self.label_prima_rappresentazione.setProperty(WidgetRole.BODY_TEXT, True)
        self.label_prima_rappresentazione.setProperty(
            WidgetColor.Text.PRIMARY_TEXT, True
        )

        self.label_trama = HyphenatedLabel("[Trama Opera]")
        self.label_trama.setProperty(WidgetRole.BODY_TEXT, True)
        self.label_trama.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)

        # Lista Regie
        label_lista_regie = QLabel("Lista regie")
        label_lista_regie.setProperty(WidgetRole.HEADER2, True)

        header_regie = QWidget()
        self.layout_header_regie = QHBoxLayout(header_regie)
        self.layout_header_regie.setContentsMargins(0, 0, 0, 0)
        self.layout_header_regie.addWidget(label_lista_regie)

        if self.can_cud_regie:
            self.__btn_nuova_regia = QPushButton("Nuova regia")
            self.__btn_nuova_regia.setProperty(WidgetRole.DEFAULT_BUTTON, True)
            self.layout_header_regie.addWidget(self.__btn_nuova_regia)

        self.layout_header_regie.addStretch()

        self.lista_regie: list[Regia] = []

        label_lista_regie_vuota = EmptyStateLabel(
            "Al momento, non vi sono regie per questa opera."
        )
        label_lista_regie_vuota.setProperty(WidgetRole.BODY_TEXT, True)
        label_lista_regie_vuota.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)

        content_lista_regie = QWidget()
        content_lista_regie.setProperty(WidgetRole.ITEM_LIST, True)
        self.layout_lista_regie = ListLayout(
            content_lista_regie, label_lista_regie_vuota
        )

        header_titolo = QLabel("Titolo")
        header_titolo.setProperty(WidgetRole.HEADER3, True)
        header_regista = QLabel("Regista")
        header_regista.setProperty(WidgetRole.HEADER3, True)
        header_opzioni = QLabel("Opzioni")
        header_opzioni.setProperty(WidgetRole.HEADER3, True)

        header_lista_regie = QWidget()
        layout_header_lista_regie = QGridLayout(header_lista_regie)
        layout_header_lista_regie.setContentsMargins(1, 1, 1, 1)
        layout_header_lista_regie.addWidget(
            header_titolo, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout_header_lista_regie.addWidget(make_vline(), 0, 1)
        layout_header_lista_regie.addWidget(
            header_regista, 0, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )
        if self.can_cud_regie:
            layout_header_lista_regie.addWidget(make_vline(), 0, 3)
            layout_header_lista_regie.addWidget(
                header_opzioni, 0, 4, alignment=Qt.AlignmentFlag.AlignCenter
            )

        self.regie = QWidget()
        self.layout_regie = QVBoxLayout(self.regie)
        self.layout_regie.addWidget(header_regie)
        self.layout_regie.addWidget(header_lista_regie)
        self.layout_regie.addWidget(content_lista_regie)
        # end-Lista Regie

        pagina_content = QWidget()
        layout_content = QVBoxLayout(pagina_content)
        layout_content.addWidget(self.label_nome)
        layout_content.addWidget(self.label_librettista)
        layout_content.addWidget(self.label_compositore)
        layout_content.addWidget(self.label_genere)
        layout_content.addWidget(self.label_atti)
        layout_content.addWidget(self.label_prima_rappresentazione)
        layout_content.addWidget(self.label_trama)
        layout_content.addWidget(self.regie)
        layout_content.addStretch()

        # Funzione di scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(pagina_content)

        # Layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.pagina_header)
        main_layout.addWidget(scroll_area)

    def _connect_signals(self) -> None:
        self.__btn_indietro.clicked.connect(  # type:ignore
            self.tornaIndietroRequest.emit
        )

        if self.can_cud_regie:
            self.__btn_nuova_regia.clicked.connect(  # type:ignore
                self.nuovaRegiaRequest.emit
            )

    # ------------------------- METODI DI VIEW -------------------------

    def set_data(
        self, data: OperaPageData, genere_nome: str, lista_regie: list[Regia]
    ) -> None:
        """Carica i dati dell'opera nella pagina.

        :param data: data salvata in una classe immutabile
        :param genere_nome: nome del genere scelto per l'opera
        :param lista_regie: lista delle regie associate all'opera"""
        # Reset layout lista regie
        self.layout_lista_regie.svuota_layout()

        # Salva dati dell'opera nella pagina
        self.id_cur_opera = data.id
        self.lista_regie = lista_regie

        # Carica dati dell'opera
        self.label_nome.setText(f"{data.nome}")
        self.label_librettista.setText(f"Libretto di {data.librettista}")
        self.label_compositore.setText(f"Musica composta da {data.compositore}")
        self.label_genere.setText(f"Genere: {genere_nome}")
        self.label_atti.setText(f"Numero di atti: {data.atti}")
        self.label_prima_rappresentazione.setText(
            "È stata rappresentata per prima volta il "
            + f"{data.data_rappresentazione.strftime("%d/%m/%y")} "
            + f"nel teatro {data.teatro_rappresentazione}"
        )
        self.label_trama.setText(f"{data.trama}")

        # Carica lista regie
        if not self.lista_regie:
            self.layout_lista_regie.if_lista_vuota()
        else:
            self.displayRegieRequest.emit(self.layout_lista_regie)

    def aggiungi_widget_a_layout(self, widget: QWidget, layout: ListLayout):
        """Aggiunge un widget creato per il display delle istanze del model.

        :param widget: widget speciale per visualizzare una instanza del model
        :param layout: layout dove sarà inserito il widget"""
        layout.addWidget(widget)

    def aggiorna_pagina(self) -> None:
        """Permette di aggiornare la pagina e visualizzare modifiche previamente non mostrate."""
        self.layout_lista_regie.svuota_layout()
        self.displayRegieRequest.emit(self.layout_lista_regie)
