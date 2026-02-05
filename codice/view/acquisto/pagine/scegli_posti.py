from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QFormLayout,
    QSizePolicy,
    #     QGridLayout,
    QScrollArea,
)
from PyQt6.QtCore import Qt, pyqtSignal

from model.organizzazione.evento import Evento
from model.organizzazione.sezione import Sezione
from model.organizzazione.posto import Posto

from view.spettacoli.utils import SpettacoloPageData

from view.utils.list_widgets import ListLayout, EmptyStateLabel
from view.utils.hyphenate_text import HyphenatedLabel
from view.utils.custom_button import DefaultButton

from view.style.ui_style import WidgetRole, WidgetColor


class ScegliPostiView(QWidget):
    """Pagina per la creazione di prenotazioni agli spettacoli.

    Segnali
    ---
    - `tornaIndietroRequest()`: emesso quando si clicca il pulsante Indietro;
    # - POR COMPLETAR
    """

    tornaIndietroRequest = pyqtSignal()
    getSezioniPostiRequest = pyqtSignal(int)
    displayPostiSceltiRequest = pyqtSignal(ListLayout)

    def __init__(self):
        super().__init__()

        self.id_current_spettacolo: int = -1

        self._setup_ui()
        self._connect_signals()

    # ------------------------- SETUP INIT -------------------------

    def _setup_ui(self) -> None:
        # Top widget
        self.__btn_indietro = DefaultButton("Indietro")

        self.pagina_header = QWidget()
        layout_header = QHBoxLayout(self.pagina_header)
        layout_header.addWidget(self.__btn_indietro)
        layout_header.addStretch()

        self.label_titolo = QLabel("[Titolo Spettacolo]")
        self.label_titolo.setProperty(WidgetRole.HEADER1, True)
        self.label_titolo.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.label_note = HyphenatedLabel("[Note Spettacolo]")
        self.label_note.setProperty(WidgetRole.BODY_TEXT, True)
        self.label_note.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)

        # Form
        form_content = QWidget()
        form_content.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding
        )
        self.__form_layout = QFormLayout(form_content)
        self.__form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.__setup_form()
        # end-Form

        # Lista Posti prenotati
        header_posti_scelti = QLabel("Posti scelti")
        header_posti_scelti.setProperty(WidgetRole.HEADER2, True)

        self.lista_posti_scelti: list[tuple[Sezione, Posto]] = []

        label_nessun_posto_scelto = EmptyStateLabel("Nessun posto scelto.")
        label_nessun_posto_scelto.setProperty(WidgetRole.BODY_TEXT, True)
        label_nessun_posto_scelto.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)

        content_lista_posti_scelti = QWidget()
        content_lista_posti_scelti.setProperty(WidgetRole.ITEM_LIST, True)
        self.layout_lista_posti_scelti = ListLayout(
            content_lista_posti_scelti, label_nessun_posto_scelto
        )

        self.posti_scelti = QWidget()
        self.layout_posti_scelti = QVBoxLayout(self.posti_scelti)
        self.layout_posti_scelti.addWidget(header_posti_scelti)
        self.layout_posti_scelti.addWidget(content_lista_posti_scelti)
        # end-Lista Posti prenotati

        pagina_content = QWidget()
        layout_content = QVBoxLayout(pagina_content)
        layout_content.addWidget(self.label_titolo)
        layout_content.addWidget(self.label_note)
        layout_content.addWidget(form_content)
        layout_content.addWidget(self.posti_scelti)
        layout_content.addStretch()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(pagina_content)
        scroll_area.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding
        )

        # Layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.pagina_header)
        main_layout.addWidget(scroll_area)

    def __setup_form(self):
        label_evento = QLabel('Data evento<span style="color:red;">*</span> :')
        label_evento.setProperty(WidgetRole.BODY_TEXT, True)
        label_evento.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
        self.evento = QComboBox()

        label_sezione = QLabel('Sezione<span style="color:red;">*</span> :')
        label_sezione.setProperty(WidgetRole.BODY_TEXT, True)
        label_sezione.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
        self.sezione = QComboBox()

        label_posto = QLabel('Posto<span style="color:red;">*</span> :')
        label_posto.setProperty(WidgetRole.BODY_TEXT, True)
        label_posto.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
        self.posto = QComboBox()

        self.__btn_aggiungi = DefaultButton("Aggiungi")

        self.__form_layout.addRow(label_evento, self.evento)
        self.__form_layout.addRow(QLabel("<hr>"))
        self.__form_layout.addRow(label_sezione, self.sezione)
        self.__form_layout.addRow(label_posto, self.posto)
        self.__form_layout.addRow(self.__btn_aggiungi)

    def _connect_signals(self) -> None:
        self.__btn_indietro.clicked.connect(  # type:ignore
            self.tornaIndietroRequest.emit
        )

        self.evento.currentIndexChanged.connect(  # type:ignore
            lambda: self.getSezioniPostiRequest.emit(self.evento.currentData())
        )

        self.sezione.currentIndexChanged.connect(  # type:ignore
            lambda: self.__setup_posto_combobox(self.sezione.currentData())
        )

    # ------------------------- METODI DI VIEW -------------------------

    def __setup_evento_combobox(self, eventi: list[Evento]) -> None:
        """Riempisce il `QComboBox` degli eventi."""
        self.evento.clear()

        self.evento.insertItem(0, "Scegliere evento...", -1)
        for i, e in enumerate(eventi, start=1):
            self.evento.insertItem(
                i, e.get_data_ora().strftime("%d/%m/%y - %H:%M"), e.get_id()
            )

    def setup_sezione_combobox(
        self, lista_sezioni_posti: list[tuple[Sezione, list[Posto]]]
    ) -> None:
        self.__lista_sezioni_posti = lista_sezioni_posti

        self.sezione.clear()

        if not self.__lista_sezioni_posti:
            return
        self.sezione.insertItem(0, "Scegliere sezione...", -1)
        for i, couple in enumerate(self.__lista_sezioni_posti, start=1):
            s, lista_p = couple
            self.sezione.insertItem(i, s.get_nome(), s.get_id())

    def __setup_posto_combobox(self, id_sezione: int) -> None:
        self.posto.clear()

        if id_sezione == -1:
            return

        posti = []
        for s, lista_p in self.__lista_sezioni_posti:
            if s.get_id() == id_sezione:
                posti = lista_p

        self.sezione.insertItem(0, "Scegliere posto...", -1)
        for i, p in enumerate(posti, start=1):
            self.sezione.insertItem(i, str(p.get_numero()), p.get_id())

    def set_data(self, data: SpettacoloPageData, lista_eventi: list[Evento]) -> None:
        """Carica i dati dello spettacolo nella pagina.

        :param data: data salvata in una classe immutabile
        :param lista_eventi: lista degli eventi associati allo spettacolo"""
        self.layout_lista_posti_scelti.svuota_layout()

        # Salva dati dello spettacolo nella pagina
        self.id_current_spettacolo = data.id

        # # Carica dati dello spettacolo
        self.label_titolo.setText(data.titolo)
        self.label_note.setText(data.note)
        self.__setup_evento_combobox(lista_eventi)

    def aggiorna_pagina(self) -> None:
        """Permette di aggiornare la pagina e visualizzare modifiche previamente non mostrate."""
        self.layout_lista_posti_scelti.svuota_layout()
        self.displayPostiSceltiRequest.emit(self.layout_lista_posti_scelti)
