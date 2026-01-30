from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QLayout,
    QHBoxLayout,
    QGridLayout,
    QScrollArea,
)
from PyQt6.QtCore import Qt, pyqtSignal

from controller.login.user_session import UserSession

from model.organizzazione.evento import Evento

from view.spettacoli.utils import SpettacoloPageData
from view.info.utils import RegiaPageData

from view.utils.list_widgets import ListLayout, EmptyStateLabel
from view.utils.hyphenate_text import HyphenatedLabel
from view.utils import make_vline
from view.style.ui_style import WidgetRole, WidgetColor


class VisualizzaSpettacoloView(QWidget):
    """Pagina per visualizzare i singoli `Spettacoli` in dettaglio.

    Contiene le tutte informazioni dello `Spettacolo` ed una lista con tutti gli `Eventi`
    associati ad essa.

    Segnali
    ---
    - `tornaIndietroRequest()`: emesso quando si clicca il pulsante Indietro;
    - `displayEventiRequest(QVBoxLayout)`: emesso per mostrare a schermo la lista eventi;
    - `nuovoEventoRequest()`: emesso quando si clicca il pulsante Nuovo evento.
    """

    tornaIndietroRequest = pyqtSignal()
    displayEventiRequest = pyqtSignal(QVBoxLayout)
    nuovoEventoRequest = pyqtSignal()

    def __init__(self, user_session: UserSession):
        super().__init__()

        self.is_biglietteria = user_session.ha_permessi_biglietteria()
        self.id_current_spettacolo: int = -1

        self._setup_ui()
        self._connect_signals()

    # ------------------------- SETUP INIT -------------------------

    def _setup_ui(self) -> None:
        # Top widget
        self.__btn_indietro = QPushButton("Indietro")
        self.__btn_indietro.setProperty(WidgetRole.DEFAULT_BUTTON, True)

        self.pagina_header = QWidget()
        layout_header = QHBoxLayout(self.pagina_header)
        layout_header.addWidget(self.__btn_indietro)
        layout_header.addStretch()

        # Labels
        self.label_titolo = HyphenatedLabel("[Titolo Spettacolo]")
        self.label_titolo.setProperty(WidgetRole.HEADER1, True)
        self.label_titolo.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.label_note = HyphenatedLabel("[Note Spettacolo]")
        self.label_note.setProperty(WidgetRole.BODY_TEXT, True)
        self.label_note.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)

        container_dati_speciali = QWidget()
        self.layout_dati_speciali = QVBoxLayout(container_dati_speciali)
        self.layout_dati_speciali.setContentsMargins(0, 0, 0, 0)

        # Lista Eventi
        label_lista_eventi = QLabel("Lista eventi")
        label_lista_eventi.setProperty(WidgetRole.HEADER2, True)

        header_eventi = QWidget()
        self.layout_header_eventi = QHBoxLayout(header_eventi)
        self.layout_header_eventi.setContentsMargins(0, 0, 0, 0)
        self.layout_header_eventi.addWidget(label_lista_eventi)

        if self.is_biglietteria:
            self.__btn_nuovo_evento = QPushButton("Nuovo evento")
            self.__btn_nuovo_evento.setProperty(WidgetRole.DEFAULT_BUTTON, True)
            self.layout_header_eventi.addWidget(self.__btn_nuovo_evento)

        self.layout_header_eventi.addStretch()

        self.lista_eventi: list[Evento] = []

        label_lista_eventi_vuota = EmptyStateLabel(
            "Al momento, non vi sono eventi per questo spettacolo."
        )
        label_lista_eventi_vuota.setProperty(WidgetRole.BODY_TEXT, True)
        label_lista_eventi_vuota.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)

        content_lista_eventi = QWidget()
        content_lista_eventi.setProperty(WidgetRole.ITEM_LIST, True)
        self.layout_lista_eventi = ListLayout(
            content_lista_eventi, label_lista_eventi_vuota
        )

        header_data = QLabel("Data")
        header_data.setProperty(WidgetRole.HEADER3, True)
        header_ora = QLabel("Ora")
        header_ora.setProperty(WidgetRole.HEADER3, True)
        header_opzioni = QLabel("Opzioni")
        header_opzioni.setProperty(WidgetRole.HEADER3, True)

        header_lista_eventi = QWidget()
        layout_header_lista_eventi = QGridLayout(header_lista_eventi)
        layout_header_lista_eventi.setContentsMargins(1, 1, 1, 1)
        layout_header_lista_eventi.addWidget(
            header_data, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout_header_lista_eventi.addWidget(make_vline(), 0, 1)
        layout_header_lista_eventi.addWidget(
            header_ora, 0, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )

        layout_header_lista_eventi.addWidget(make_vline(), 0, 3)
        layout_header_lista_eventi.addWidget(
            header_opzioni, 0, 4, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.eventi = QWidget()
        self.layout_eventi = QVBoxLayout(self.eventi)
        self.layout_eventi.addWidget(header_eventi)
        self.layout_eventi.addWidget(header_lista_eventi)
        self.layout_eventi.addWidget(content_lista_eventi)
        # end-Lista Eventi

        pagina_content = QWidget()
        layout_content = QVBoxLayout(pagina_content)
        layout_content.addWidget(self.label_titolo)
        layout_content.addWidget(self.label_note)
        layout_content.addWidget(container_dati_speciali)
        layout_content.addWidget(self.eventi)
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

        if self.is_biglietteria:
            self.__btn_nuovo_evento.clicked.connect(  # type:ignore
                self.nuovoEventoRequest.emit
            )

    # ------------------------- METODI DI VIEW -------------------------

    def set_data(
        self,
        data: SpettacoloPageData,
        lista_eventi: list[Evento],
    ) -> None:
        """Carica i dati dello spettacolo nella pagina.

        :param data: data salvata in una classe immutabile
        :param lista_eventi: lista degli eventi associati allo spettacolo"""
        # Reset layout lista regie
        self.layout_lista_eventi.svuota_layout()

        # Salva dati dello spettacolo nella pagina
        self.id_current_spettacolo = data.id
        self.lista_eventi = lista_eventi

        # Carica dati dello spettacolo
        self.label_titolo.setText(f"{data.titolo}")
        self.label_note.setText(f"{data.note}")
        self.__svuota_layout_generico(self.layout_dati_speciali)
        if type(data) is RegiaPageData:
            label_regista = QLabel(f"<b>Regista:</b> {data.regista}")
            label_regista.setProperty(WidgetRole.BODY_TEXT, True)
            label_regista.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)
            self.layout_dati_speciali.addWidget(label_regista)

            label_anno = QLabel(f"<b>Anno di produzione:</b> {data.anno_produzione}")
            label_anno.setProperty(WidgetRole.BODY_TEXT, True)
            label_anno.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)
            self.layout_dati_speciali.addWidget(label_anno)
        else:  # Caso Spettacolo generico
            ...

        # Carica lista regie
        if not self.lista_eventi:
            self.layout_lista_eventi.mostra_msg_lista_vuota()
        else:
            self.displayEventiRequest.emit(self.layout_lista_eventi)

    def aggiorna_pagina(self) -> None:
        """Permette di aggiornare la pagina e visualizzare modifiche previamente non mostrate."""
        self.layout_lista_eventi.svuota_layout()
        self.displayEventiRequest.emit(self.layout_lista_eventi)

    def __svuota_layout_generico(self, layout: QLayout):
        while layout.count() > 0:
            item = layout.takeAt(0)
            if item is None:
                raise ValueError("Expected item at index 0")
            if widget := item.widget():
                widget.setParent(None)
            elif child_layout := item.layout():
                self.__svuota_layout_generico(child_layout)
