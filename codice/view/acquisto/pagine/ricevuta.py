from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Optional

from model.organizzazione.evento import Evento
from model.organizzazione.sezione import Sezione
from model.organizzazione.posto import Posto

from view.prenotazioni.utils import PrenotazionePageData

from view.utils.list_widgets import ListLayout, EmptyStateLabel
from view.utils.hyphenate_text import HyphenatedLabel
from view.utils.custom_button import DefaultButton, CreaButton

from view.style.ui_style import WidgetRole, WidgetColor


class RicevutaView(QWidget):
    """Pagina per finire il processo di creazione di prenotazioni.

    Segnali
    ---
    - `displayPostiSceltiRequest(ListLayout)` : emesso per mostrare a schermo i posti prenotati;
    - `stampaRicevuta()` : emesso per stampare la ricevuta della prenotazione;
    - `ritornaAllaMainPage()` : emesso per tornare alla pagina `AcquistoSectionView`.
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
        label_header.setProperty(WidgetRole.HEADER1, True)
        label_header.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)
        label_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_spettacolo = HyphenatedLabel(
            "<b>Spettacolo</b>: [Titolo Spettacolo]"
        )
        self.label_spettacolo.setProperty(WidgetRole.BODY_TEXT, True)
        self.label_spettacolo.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)
        self.label_spettacolo.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.label_spettacolo.setStyleSheet(
            self.label_spettacolo.styleSheet() + " font-size: 16px; "
        )

        self.label_nominativo = HyphenatedLabel("<b>Nominativo</b>: [Nominativo]")
        self.label_nominativo.setProperty(WidgetRole.BODY_TEXT, True)
        self.label_nominativo.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)
        self.label_nominativo.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.label_nominativo.setStyleSheet(
            self.label_nominativo.styleSheet() + " font-size: 16px; "
        )

        self.label_prezzo = HyphenatedLabel("<b>Prezzo</b>: € [Ammontare Prezzo]")
        self.label_prezzo.setProperty(WidgetRole.BODY_TEXT, True)
        self.label_prezzo.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)
        self.label_prezzo.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.label_prezzo.setStyleSheet(
            self.label_prezzo.styleSheet() + " font-size: 16px; "
        )

        # Lista Posti prenotati
        self.lista_posti_scelti: tuple[
            Optional[Evento], list[tuple[Sezione, list[Posto]]]
        ] = (None, [])

        label_nessun_posto_scelto = EmptyStateLabel("Nessun posto scelto.")
        label_nessun_posto_scelto.setProperty(WidgetRole.BODY_TEXT, True)
        label_nessun_posto_scelto.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)

        content_lista_posti_scelti = QWidget()
        self.layout_lista_posti_scelti = ListLayout(
            content_lista_posti_scelti, label_nessun_posto_scelto
        )
        self.layout_lista_posti_scelti.setContentsMargins(0, 2, 0, 2)

        self.posti_scelti = QWidget()
        self.layout_posti_scelti = QVBoxLayout(self.posti_scelti)
        self.layout_posti_scelti.addWidget(content_lista_posti_scelti)
        self.layout_posti_scelti.addStretch()
        # end-Lista Posti prenotati

        self.label_emissione = QLabel("<b>Emissione</b>: [Data Emissione]")
        self.label_emissione.setProperty(WidgetRole.BODY_TEXT, True)
        self.label_emissione.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)

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

    def set_data(
        self,
        data: PrenotazionePageData,
        lista_posti_scelti: tuple[Evento, list[tuple[Sezione, list[Posto]]]],
    ) -> None:
        """Carica i dati dei posti prenotati.

        :param data: data della prenotazione salvata in una classe immutabile.
        :param lista_posti_scelti: lista dei posti scelti, insieme alle sezioni ed evento
        """
        self.layout_lista_posti_scelti.svuota_layout()

        self.label_spettacolo.setText("<b>Spettacolo</b>: " + data.titolo_spettacolo)
        self.label_nominativo.setText("<b>Nominativo</b>: " + data.nominativo)
        self.label_prezzo.setText(f"<b>Prezzo</b>: € {data.ammontare:.2f}")

        self.lista_posti_scelti = lista_posti_scelti

        self.label_emissione.setText(
            "<b>Emissione</b>: "
            + data.data_ora_registrazione.strftime("%a %b %d %Y %H:%M:%S")
        )

        self.abilita_btn_fine(False)

    def abilita_btn_fine(self, flag: bool) -> None:
        self.__btn_fine.setEnabled(flag)
        self.__btn_stampa.setEnabled(not flag)

    def aggiorna_pagina(self) -> None:
        self.layout_lista_posti_scelti.svuota_layout()
        self.displayPostiSceltiRequest.emit(self.layout_lista_posti_scelti)
