from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
)
from PyQt6.QtCore import Qt, pyqtSignal

from model.organizzazione.evento import Evento
from model.organizzazione.sezione import Sezione
from model.organizzazione.posto import Posto

from view.spettacoli.utils import SpettacoloPageData

from view.utils.list_widgets import ListLayout, EmptyStateLabel
from view.utils.hyphenate_text import HyphenatedLabel
from view.utils.custom_button import DefaultButton, SalvaButton
from view.utils import make_hline

from view.style.ui_style import WidgetRole, WidgetColor


class RicevutaView(QWidget):
    """Pagina per la creazione di prenotazioni agli spettacoli.

    Segnali
    ---
    - `setupEventoCombobox(int)` :
    - `setupSezioneCombobox(int)` :
    - `setupFilaCombobox(int, int)` :
    - `setupPostoCombobox(str)` :
    - `aggiungiPostoScelto(int, int, int)` :
    - `displayPostiSceltiRequest(ListLayout)` :
    # - COMPLETAR
    """

    setupEventoCombobox = pyqtSignal(int)
    setupSezioneCombobox = pyqtSignal(int)
    setupFilaCombobox = pyqtSignal(int)
    setupPostoCombobox = pyqtSignal(str)

    aggiungiPostoScelto = pyqtSignal(int, int, int)
    displayPostiSceltiRequest = pyqtSignal(ListLayout)

    def __init__(self):
        super().__init__()

        # self.id_current_spettacolo: int = -1

        self._setup_ui()
        self._connect_signals()

    # ------------------------- SETUP INIT -------------------------

    def _setup_ui(self) -> None:

        label_header = QLabel("Ricevuta")
        label_header.setProperty(WidgetRole.HEADER1, True)
        label_header.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)
        label_header.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.__btn_stampa = DefaultButton("Stampa")
        self.__btn_fine = DefaultButton("Fine")
        self.__btn_fine.setEnabled(False)

        pulsanti = QWidget()
        layout_pulsanti = QHBoxLayout(pulsanti)
        layout_pulsanti.addWidget(self.__btn_stampa)
        layout_pulsanti.addWidget(self.__btn_fine)

        pagina_content = QWidget()
        self._layout_content = QVBoxLayout(pagina_content)

        # Funzione di scroll
        self.__scroll_area = QScrollArea()
        self.__scroll_area.setWidgetResizable(True)
        self.__scroll_area.setWidget(pagina_content)

        # Layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(label_header)
        main_layout.addWidget(self.__scroll_area)
        main_layout.addWidget(pulsanti)

        ##################

        self.label_spettacolo = HyphenatedLabel(
            "<b>Spettacolo:</b> [Titolo Spettacolo]"
        )
        self.label_spettacolo.setProperty(WidgetRole.HEADER1, True)
        self.label_spettacolo.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.label_data = HyphenatedLabel("[Data Evento]")
        self.label_data.setProperty(WidgetRole.BODY_TEXT, True)
        self.label_data.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)

        # # Form
        # form_content = QWidget()
        # form_content.setSizePolicy(
        #     QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding
        # )
        # self.__form_layout = QFormLayout(form_content)
        # self.__form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        # self.__setup_form()
        # # end-Form

        # Lista Posti prenotati
        header_posti_scelti = QLabel("Posti scelti")
        header_posti_scelti.setProperty(WidgetRole.HEADER2, True)

        self.lista_posti_scelti: dict[Evento, dict[Sezione, set[Posto]]] = {}

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

        self.__btn_conferma = SalvaButton("Conferma", has_icon=False)
        # - DARLE UN NOMBRE MEJOR
        # - FALTA CONECTARLOS
        # - A LO MEJOR DEBERÍA DEJAR PEGADO A LA IZQUIERDA

        # Layout
        self._layout_content.addWidget(self.label_spettacolo)
        self._layout_content.addWidget(self.label_data)
        # self._layout_content.addWidget(form_content)
        self._layout_content.addWidget(make_hline())
        self._layout_content.addWidget(self.posti_scelti)
        self._layout_content.addWidget(self.__btn_conferma)
        self._layout_content.addStretch()

    # def __setup_form(self):
    #     label_evento = QLabel('Data evento<span style="color:red;">*</span> :')
    #     label_evento.setProperty(WidgetRole.BODY_TEXT, True)
    #     label_evento.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
    #     self.evento = QComboBox()

    #     label_sezione = QLabel('Sezione<span style="color:red;">*</span> :')
    #     label_sezione.setProperty(WidgetRole.BODY_TEXT, True)
    #     label_sezione.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
    #     label_sezione.setMinimumWidth(label_evento.sizeHint().width())
    #     label_sezione.setAlignment(Qt.AlignmentFlag.AlignRight)
    #     self.sezione = QComboBox()

    #     sezione_box = QWidget()
    #     layout_sezione_box = QFormLayout(sezione_box)
    #     layout_sezione_box.setContentsMargins(0, 2, 0, 2)
    #     layout_sezione_box.addRow(label_sezione, self.sezione)

    #     label_fila = QLabel('Fila<span style="color:red;">*</span> :')
    #     label_fila.setProperty(WidgetRole.BODY_TEXT, True)
    #     label_fila.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
    #     label_fila.setMinimumWidth(label_evento.sizeHint().width())
    #     label_fila.setAlignment(Qt.AlignmentFlag.AlignRight)
    #     self.fila = QComboBox()

    #     label_numero = QLabel('Numero posto<span style="color:red;">*</span> :')
    #     label_numero.setProperty(WidgetRole.BODY_TEXT, True)
    #     label_numero.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
    #     label_numero.setMinimumWidth(label_evento.sizeHint().width())
    #     label_numero.setAlignment(Qt.AlignmentFlag.AlignRight)
    #     self.numero = QComboBox()

    #     # layout_fila_numero.addWidget(label_fila)
    #     # layout_fila_numero.addWidget(self.fila)
    #     # layout_fila_numero.addWidget(label_numero)
    #     # layout_fila_numero.addWidget(self.numero)

    #     fila_box = QWidget()
    #     layout_fila_box = QFormLayout(fila_box)
    #     layout_fila_box.setContentsMargins(0, 2, 0, 2)
    #     layout_fila_box.addRow(label_fila, self.fila)

    #     numero_box = QWidget()
    #     layout_numero_box = QFormLayout(numero_box)
    #     layout_numero_box.setContentsMargins(0, 2, 0, 2)
    #     layout_numero_box.addRow(label_numero, self.numero)

    #     fila_numero_box = QWidget()
    #     layout_fila_numero = QHBoxLayout(fila_numero_box)
    #     layout_fila_numero.setContentsMargins(0, 0, 0, 0)
    #     layout_fila_numero.addWidget(fila_box)
    #     layout_fila_numero.addWidget(numero_box)

    #     self.__btn_aggiungi = DefaultButton("Aggiungi posto")

    #     self.__form_layout.addRow(label_evento, self.evento)
    #     # self.__form_layout.addRow(make_hline())
    #     self.__form_layout.addRow(sezione_box)
    #     self.__form_layout.addRow(fila_numero_box)
    #     # self.__form_layout.addRow(label_fila, self.fila)
    #     # self.__form_layout.addRow(label_numero, self.numero)
    #     self.__form_layout.addRow(self.__btn_aggiungi)

    def _connect_signals(self) -> None:
        ...
        # self.evento.currentIndexChanged.connect(  # type:ignore
        #     lambda: self.setupSezioneCombobox.emit(self.evento.currentData())
        # )

        # self.sezione.currentIndexChanged.connect(  # type:ignore
        #     lambda: self.setupFilaCombobox.emit(self.sezione.currentData())
        # )

        # self.fila.currentTextChanged.connect(  # type:ignore
        #     lambda: self.setupPostoCombobox.emit(self.fila.currentText())
        # )

        # self.__btn_aggiungi.clicked.connect(  # type:ignore
        #     lambda: self.aggiungiPostoScelto.emit(
        #         self.evento.currentData(),
        #         self.sezione.currentData(),
        #         self.numero.currentData(),
        #     )
        # )

    # ------------------------- METODI DI VIEW -------------------------

    def set_data(self, data: dict[Evento, dict[Sezione, set[Posto]]]) -> None:  # type: ignore
        """Carica i dati dello spettacolo nella pagina.

        :param data: data salvata in una classe immutabile
        :param lista_eventi: lista degli eventi associati allo spettacolo"""
        self.layout_lista_posti_scelti.svuota_layout()

        # # Salva dati dello spettacolo nella pagina
        # self.id_current_spettacolo = data.id

        # # # Carica dati dello spettacolo
        # self.label_spettacolo.setText(data.titolo)
        # self.label_data.setText(data.note)
        # self.setupEventoCombobox.emit(self.id_current_spettacolo)

    def aggiorna_pagina(self) -> None:

        self.layout_lista_posti_scelti.svuota_layout()
        self.displayPostiSceltiRequest.emit(self.layout_lista_posti_scelti)
