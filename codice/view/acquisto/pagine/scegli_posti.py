from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QComboBox,
    QFormLayout,
    QSizePolicy,
)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import override

from core.view import AbstractVisualizzaView

from model.organizzazione.evento import Evento
from model.organizzazione.sezione import Sezione
from model.organizzazione.posto import Posto

from view.spettacoli.utils import SpettacoloPageData

from view.utils.list_widgets import ListLayout, EmptyStateLabel
from view.utils.hyphenate_text import HyphenatedLabel
from view.utils.custom_button import DefaultButton
from view.utils import make_hline

from view.style.ui_style import WidgetRole, WidgetColor


class ScegliPostiView(AbstractVisualizzaView):
    """Pagina per la creazione di prenotazioni agli spettacoli.

    Segnali
    ---
    - `getSezioniPostiRequest(int)`:
    - `displayPostiSceltiRequest(ListLayout)`:
    # - POR COMPLETAR
    """

    getSezioniPostiRequest = pyqtSignal(int)
    displayPostiSceltiRequest = pyqtSignal(ListLayout)

    def __init__(self):
        self.id_current_spettacolo: int = -1

        super().__init__()

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

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

        # Layout
        self._layout_content.addWidget(self.label_titolo)
        self._layout_content.addWidget(self.label_note)
        self._layout_content.addWidget(form_content)
        self._layout_content.addWidget(self.posti_scelti)
        self._layout_content.addStretch()

    def __setup_form(self):
        label_evento = QLabel('Data evento<span style="color:red;">*</span> :')
        label_evento.setProperty(WidgetRole.BODY_TEXT, True)
        label_evento.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
        self.evento = QComboBox()

        label_sezione = QLabel('Sezione<span style="color:red;">*</span> :')
        label_sezione.setProperty(WidgetRole.BODY_TEXT, True)
        label_sezione.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
        self.sezione = QComboBox()

        label_fila = QLabel('Fila<span style="color:red;">*</span> :')
        label_fila.setProperty(WidgetRole.BODY_TEXT, True)
        label_fila.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
        self.fila = QComboBox()

        label_numero = QLabel('Numero posto<span style="color:red;">*</span> :')
        label_numero.setProperty(WidgetRole.BODY_TEXT, True)
        label_numero.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
        self.numero = QComboBox()

        self.__btn_aggiungi = DefaultButton("Aggiungi")

        self.__form_layout.addRow(label_evento, self.evento)
        self.__form_layout.addRow(make_hline())
        self.__form_layout.addRow(label_sezione, self.sezione)
        self.__form_layout.addRow(label_fila, self.fila)
        self.__form_layout.addRow(label_numero, self.numero)
        self.__form_layout.addRow(self.__btn_aggiungi)

    @override
    def _connect_signals(self) -> None:
        super()._connect_signals()

        self.evento.currentIndexChanged.connect(  # type:ignore
            lambda: self.getSezioniPostiRequest.emit(self.evento.currentData())
        )

    # ------------------------- METODI DI VIEW -------------------------

    @override
    def set_data(  # type: ignore[override]
        self, data: SpettacoloPageData, lista_eventi: list[Evento]
    ) -> None:
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

    @override
    def aggiorna_pagina(self) -> None:
        super().aggiorna_pagina()

        self.layout_lista_posti_scelti.svuota_layout()
        self.displayPostiSceltiRequest.emit(self.layout_lista_posti_scelti)

    def __setup_evento_combobox(self, eventi: list[Evento]) -> None:
        """Riempisce il `QComboBox` degli eventi."""
        self.evento.clear()

        self.evento.insertItem(0, "Scegliere evento...", -1)
        for i, e in enumerate(eventi, start=1):
            self.evento.insertItem(
                i, e.get_data_ora().strftime("%d/%m/%y - %H:%M"), e.get_id()
            )
