from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QSizePolicy,
)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Optional, override

from core.view import AbstractVisualizzaView

from model.organizzazione.evento import Evento
from model.organizzazione.sezione import Sezione
from model.organizzazione.posto import Posto

from view.spettacoli.utils import SpettacoloData

from view.utils.list_widgets import ListLayout, EmptyStateLabel
from view.utils.hyphenate_text import HyphenatedLabel
from view.utils.custom_button import DefaultButton, SalvaButton
from view.utils.fixed_size_widget import FixedSizeLineEdit, FixedSizeComboBox
from view.utils import make_hline

from view.style.ui_style import WidgetRole, WidgetColor


class ScegliPostiPage(AbstractVisualizzaView):
    """Pagina per la creazione di prenotazioni agli spettacoli.

    Segnali
    ---
    - `setupEventoCombobox(int)` : emesso per riempire la combobox `self.evento` con eventi
        disponibili;
    - `setupSezioneCombobox(int)` : emesso per riempire la combobox `self.sezione` con sezioni
        disponibili associate all'evento scelto;
    - `setupFilaCombobox(int)` : emesso per riempire la combobox `self.fila` con file
        disponibili associate alla sezione scelta;
    - `setupPostoCombobox(str)` : emesso per riempire la combobox `self.numero` con i numeri
        dei posti disponibili relativi alla fila scelta;
    - `aggiungiPostoScelto(int, int, int)` : emesso per aggiungere un
        `tuple[Evento, Sezione, Posto]` alla `self.lista_posti_scelti` e mostrare il posto a
        schermo;
    - `displayPostiSceltiRequest(ListLayout)` : emesso per mostrare i posti scelti a schermo;
    - `creaNuovaPrenotazione()` : emesso per salvare una nuova prenotazione nel sistema.
    """

    setupEventoCombobox = pyqtSignal(int)
    setupSezioneCombobox = pyqtSignal(int)
    setupFilaCombobox = pyqtSignal(int)
    setupPostoCombobox = pyqtSignal(str)

    aggiungiPostoScelto = pyqtSignal(int, int, int)
    displayPostiSceltiRequest = pyqtSignal(ListLayout)
    creaNuovaPrenotazione = pyqtSignal()

    def __init__(self):
        self.id_current_spettacolo: int = -1

        super().__init__()

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        self.label_titolo = HyphenatedLabel("[Titolo Spettacolo]")
        self.label_titolo.setProperty(WidgetRole.Label.HEADER1, True)
        self.label_titolo.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.label_note = HyphenatedLabel("[Note Spettacolo]")
        self.label_note.setProperty(WidgetRole.Label.BODY_TEXT, True)
        self.label_note.setProperty(WidgetColor.Label.PRIMARY_COLOR, True)

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
        header_posti_scelti.setProperty(WidgetRole.Label.HEADER2, True)

        self.evento_scelto: Optional[Evento] = None
        self.lista_posti_scelti: list[tuple[Sezione, Posto]] = []

        label_nessun_posto_scelto = EmptyStateLabel("Nessun posto scelto.")
        label_nessun_posto_scelto.setProperty(WidgetRole.Label.BODY_TEXT, True)
        label_nessun_posto_scelto.setProperty(WidgetColor.Label.SECONDARY_COLOR, True)

        content_lista_posti_scelti = QWidget()
        content_lista_posti_scelti.setProperty(WidgetRole.Item.LIST, True)
        self.layout_lista_posti_scelti = ListLayout(
            content_lista_posti_scelti, label_nessun_posto_scelto
        )

        self.posti_scelti = QWidget()
        self.layout_posti_scelti = QVBoxLayout(self.posti_scelti)
        self.layout_posti_scelti.addWidget(header_posti_scelti)
        self.layout_posti_scelti.addWidget(content_lista_posti_scelti)
        # end-Lista Posti prenotati

        self.__btn_conferma = SalvaButton("Conferma", has_icon=False)

        conferma_box = QWidget()
        btn_conferma_box = QHBoxLayout(conferma_box)
        btn_conferma_box.addStretch()
        btn_conferma_box.addWidget(self.__btn_conferma)

        # Layout
        self._layout_content.addWidget(self.label_titolo)
        self._layout_content.addWidget(self.label_note)
        self._layout_content.addWidget(form_content)
        self._layout_content.addWidget(make_hline())
        self._layout_content.addWidget(self.posti_scelti)
        self._layout_content.addWidget(conferma_box)
        self._layout_content.addStretch()

    def __setup_form(self):
        label_nominativo = QLabel('Nominativo<span style="color:red;">*</span> :')
        label_nominativo.setProperty(WidgetRole.Label.BODY_TEXT, True)
        label_nominativo.setProperty(WidgetColor.Label.SECONDARY_COLOR, True)
        self.nominativo = FixedSizeLineEdit(width=230)
        self.nominativo.setPlaceholderText("Inserire nominativo")

        label_evento = QLabel('Data evento<span style="color:red;">*</span> :')
        label_evento.setProperty(WidgetRole.Label.BODY_TEXT, True)
        label_evento.setProperty(WidgetColor.Label.SECONDARY_COLOR, True)
        self.evento = FixedSizeComboBox(width=230)

        label_sezione = QLabel('Sezione<span style="color:red;">*</span> :')
        label_sezione.setProperty(WidgetRole.Label.BODY_TEXT, True)
        label_sezione.setProperty(WidgetColor.Label.SECONDARY_COLOR, True)
        label_sezione.setMinimumWidth(label_evento.sizeHint().width())
        label_sezione.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.sezione = FixedSizeComboBox(width=230)

        sezione_box = QWidget()
        layout_sezione_box = QFormLayout(sezione_box)
        layout_sezione_box.setContentsMargins(0, 2, 0, 2)
        layout_sezione_box.addRow(label_sezione, self.sezione)

        label_fila = QLabel('Fila<span style="color:red;">*</span> :')
        label_fila.setProperty(WidgetRole.Label.BODY_TEXT, True)
        label_fila.setProperty(WidgetColor.Label.SECONDARY_COLOR, True)
        label_fila.setMinimumWidth(label_evento.sizeHint().width())
        label_fila.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.fila = FixedSizeComboBox(width=230)

        label_numero = QLabel('Numero posto<span style="color:red;">*</span> :')
        label_numero.setProperty(WidgetRole.Label.BODY_TEXT, True)
        label_numero.setProperty(WidgetColor.Label.SECONDARY_COLOR, True)
        label_numero.setMinimumWidth(label_evento.sizeHint().width())
        label_numero.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.numero = FixedSizeComboBox(width=220)

        fila_box = QWidget()
        layout_fila_box = QFormLayout(fila_box)
        layout_fila_box.setContentsMargins(0, 2, 0, 2)
        layout_fila_box.addRow(label_fila, self.fila)

        numero_box = QWidget()
        layout_numero_box = QFormLayout(numero_box)
        layout_numero_box.setContentsMargins(0, 2, 0, 2)
        layout_numero_box.addRow(label_numero, self.numero)

        fila_numero_box = QWidget()
        layout_fila_numero = QHBoxLayout(fila_numero_box)
        layout_fila_numero.setContentsMargins(0, 0, 0, 0)
        layout_fila_numero.addWidget(fila_box)
        layout_fila_numero.addWidget(numero_box)

        self.__btn_aggiungi = DefaultButton("Aggiungi posto")

        aggiungi_box = QWidget()
        layout_aggiungi_box = QHBoxLayout(aggiungi_box)
        layout_aggiungi_box.setContentsMargins(0, 0, 0, 0)
        layout_aggiungi_box.addStretch()
        layout_aggiungi_box.addWidget(self.__btn_aggiungi)

        self.__form_layout.addRow(label_nominativo, self.nominativo)
        self.__form_layout.addRow(make_hline())
        self.__form_layout.addRow(label_evento, self.evento)
        self.__form_layout.addRow(sezione_box)
        self.__form_layout.addRow(fila_numero_box)
        self.__form_layout.addRow(aggiungi_box)

    @override
    def _connect_signals(self) -> None:
        super()._connect_signals()

        self.evento.currentIndexChanged.connect(  # type:ignore
            lambda: self.setupSezioneCombobox.emit(self.evento.currentData())
        )

        self.sezione.currentIndexChanged.connect(  # type:ignore
            lambda: self.setupFilaCombobox.emit(self.sezione.currentData())
        )

        self.fila.currentTextChanged.connect(  # type:ignore
            lambda: self.setupPostoCombobox.emit(self.fila.currentText())
        )

        self.__btn_aggiungi.clicked.connect(  # type:ignore
            lambda: self.aggiungiPostoScelto.emit(
                self.evento.currentData(),
                self.sezione.currentData(),
                self.numero.currentData(),
            )
        )

        self.__btn_conferma.clicked.connect(  # type:ignore
            self.creaNuovaPrenotazione.emit
        )

    # ------------------------- METODI DI VIEW -------------------------

    @override
    def set_data(self, data: SpettacoloData) -> None:  # type: ignore[override]
        """Carica i dati dello spettacolo nella pagina.

        :param data: data salvata in una classe immutabile
        :param lista_eventi: lista degli eventi associati allo spettacolo"""
        self.layout_lista_posti_scelti.svuota_layout()

        # Salva dati dello spettacolo nella pagina
        self.id_current_spettacolo = data.id

        # # Carica dati dello spettacolo
        self.label_titolo.setText(data.titolo)
        self.label_note.setText(data.note)
        self.setupEventoCombobox.emit(self.id_current_spettacolo)

    @override
    def aggiorna_pagina(self) -> None:
        super().aggiorna_pagina()

        self.evento.setEnabled(True)

        self.layout_lista_posti_scelti.svuota_layout()
        self.displayPostiSceltiRequest.emit(self.layout_lista_posti_scelti)

        # Questo evita di creare una prenotazione per più di un'evento alla volta.
        if self.layout_lista_posti_scelti.count() > 1:
            self.evento.setEnabled(False)
