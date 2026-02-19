from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
)
from PyQt6.QtCore import Qt, pyqtSignal
from datetime import datetime
from typing import Optional

from model.model.model import RicevutaData, SezionePostiInfo

from view.utils.list_widgets import ListLayout, EmptyStateLabel
from view.utils.hyphenate_text import HyphenatedLabel
from view.utils.custom_button import DefaultButton, CreaButton

from view.style.ui_style import WidgetRole, WidgetColor


class RicevutaPage(QWidget):
    """Pagina per finire il processo di creazione di prenotazioni.

    Segnali
    ---
    - `displayPostiSceltiRequest(ListLayout)` : emesso per mostrare a schermo i posti prenotati;
    - `stampaRicevuta()` : emesso per stampare la ricevuta della prenotazione;
    - `ritornaAllaMainPage()` : emesso per tornare alla pagina `AcquistoSection`.
    """

    displayPostiSceltiRequest = pyqtSignal(ListLayout)
    stampaRicevuta = pyqtSignal()
    ritornaAllaMainPage = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.__setup_ui()
        self.__connect_signals()

    # ------------------------- SETUP INIT -------------------------

    def __setup_ui(self) -> None:
        label_header = QLabel("Ricevuta")
        label_header.setProperty(WidgetRole.Label.HEADER1, True)
        label_header.setProperty(WidgetColor.Label.PRIMARY_COLOR, True)
        label_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_spettacolo = HyphenatedLabel(
            "<b>Spettacolo</b>: [Titolo Spettacolo]"
        )
        self.label_spettacolo.setProperty(WidgetRole.Label.BODY_TEXT, True)
        self.label_spettacolo.setProperty(WidgetColor.Label.PRIMARY_COLOR, True)
        self.label_spettacolo.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.label_spettacolo.setStyleSheet(
            self.label_spettacolo.styleSheet() + " font-size: 16px; "
        )

        self.label_nominativo = HyphenatedLabel("<b>Nominativo</b>: [Nominativo]")
        self.label_nominativo.setProperty(WidgetRole.Label.BODY_TEXT, True)
        self.label_nominativo.setProperty(WidgetColor.Label.PRIMARY_COLOR, True)
        self.label_nominativo.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.label_nominativo.setStyleSheet(
            self.label_nominativo.styleSheet() + " font-size: 16px; "
        )

        self.label_data_evento = HyphenatedLabel("<b>Data evento</b>: [Data Evento]")
        self.label_data_evento.setProperty(WidgetRole.Label.BODY_TEXT, True)
        self.label_data_evento.setProperty(WidgetColor.Label.PRIMARY_COLOR, True)
        self.label_data_evento.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.label_data_evento.setStyleSheet(
            self.label_data_evento.styleSheet() + " font-size: 16px; "
        )

        self.label_prezzo = HyphenatedLabel("<b>Prezzo</b>: € [Ammontare Prezzo]")
        self.label_prezzo.setProperty(WidgetRole.Label.BODY_TEXT, True)
        self.label_prezzo.setProperty(WidgetColor.Label.PRIMARY_COLOR, True)
        self.label_prezzo.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.label_prezzo.setStyleSheet(
            self.label_prezzo.styleSheet() + " font-size: 16px; "
        )

        # Lista Posti prenotati
        label_lista_posti = QLabel("Lista posti")
        label_lista_posti.setProperty(WidgetRole.Label.HEADER2, True)

        self.lista_posti_scelti: tuple[Optional[datetime], list[SezionePostiInfo]] = (
            None,
            [],
        )

        label_nessun_posto_scelto = EmptyStateLabel("Nessun posto scelto.")
        label_nessun_posto_scelto.setProperty(WidgetRole.Label.BODY_TEXT, True)
        label_nessun_posto_scelto.setProperty(WidgetColor.Label.SECONDARY_COLOR, True)

        content_lista_posti_scelti = QWidget()
        self.layout_lista_posti_scelti = ListLayout(
            content_lista_posti_scelti, label_nessun_posto_scelto
        )
        self.layout_lista_posti_scelti.setContentsMargins(0, 2, 0, 2)

        self.posti_scelti = QWidget()
        self.layout_posti_scelti = QVBoxLayout(self.posti_scelti)
        self.layout_posti_scelti.addWidget(label_lista_posti)
        self.layout_posti_scelti.addWidget(content_lista_posti_scelti)
        self.layout_posti_scelti.addStretch()
        # end-Lista Posti prenotati

        self.label_emissione = QLabel("<b>Emissione</b>: [Data Emissione]")
        self.label_emissione.setProperty(WidgetRole.Label.BODY_TEXT, True)
        self.label_emissione.setProperty(WidgetColor.Label.PRIMARY_COLOR, True)

        self.__btn_stampa = CreaButton("Stampa", has_icon=False)
        self.__btn_fine = DefaultButton("Fine")
        self.__btn_fine.setEnabled(False)

        pulsanti = QWidget()
        layout_pulsanti = QHBoxLayout(pulsanti)
        layout_pulsanti.addWidget(self.__btn_stampa)
        layout_pulsanti.addWidget(self.__btn_fine)

        # Layout
        pagina_content = QWidget()
        self.__layout_content = QVBoxLayout(pagina_content)
        self.__layout_content.addWidget(self.label_spettacolo)
        self.__layout_content.addWidget(self.label_nominativo)
        self.__layout_content.addWidget(self.label_data_evento)
        self.__layout_content.addWidget(self.label_prezzo)
        self.__layout_content.addWidget(self.posti_scelti)
        self.__layout_content.addStretch()
        self.__layout_content.addWidget(self.label_emissione)

        # Funzione di scroll
        self.__scroll_area = QScrollArea()
        self.__scroll_area.setWidgetResizable(True)
        self.__scroll_area.setWidget(pagina_content)

        # Layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(label_header)
        main_layout.addWidget(self.__scroll_area)
        main_layout.addWidget(pulsanti)

    def __connect_signals(self) -> None:
        self.__btn_stampa.clicked.connect(  # type:ignore
            self.stampaRicevuta.emit
        )

        self.__btn_fine.clicked.connect(  # type:ignore
            self.ritornaAllaMainPage.emit
        )

    # ------------------------- METODI DI VIEW -------------------------

    def set_data(self, data: RicevutaData) -> None:
        """Carica i dati dei posti prenotati.

        :param data: container con tutti i dati necessari per fare e mostrare una ricevuta.
        """
        # Reset layout lista posti scelti
        self.layout_lista_posti_scelti.svuota_layout()

        # Carica dati della prenotazione
        self.label_spettacolo.setText("<b>Spettacolo</b>: " + data.spettacolo_titolo)
        self.label_nominativo.setText("<b>Nominativo</b>: " + data.nominativo)
        self.label_data_evento.setText(
            "<b>Data evento</b>:" + data.evento_dataora.strftime("%d/%m/%y - %H:%M")
        )
        self.label_prezzo.setText(f"<b>Prezzo</b>: € {data.prezzo_complessivo:.2f}")

        self.lista_posti_scelti = (data.evento_dataora, data.sezioni_posti)

        self.label_emissione.setText(
            "<b>Emissione</b>: "
            + data.emmisione_dataora.strftime("%a %b %d %Y %H:%M:%S")
        )

        self.data_ricevuta = data  # Usato per stampare la ricevuta

        self.abilita_btn_fine(False)

    def abilita_btn_fine(self, flag: bool) -> None:
        self.__btn_fine.setEnabled(flag)
        self.__btn_stampa.setEnabled(not flag)

    def aggiorna_pagina(self) -> None:
        self.layout_lista_posti_scelti.svuota_layout()
        self.displayPostiSceltiRequest.emit(self.layout_lista_posti_scelti)
