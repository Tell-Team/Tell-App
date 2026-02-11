from PyQt6.QtWidgets import QWidget, QHBoxLayout, QCheckBox
from PyQt6.QtCore import Qt, pyqtSignal
from typing import override

from core.view import AbstractVisualizzaView

from view.prenotazioni.utils import PrenotazionePageData

from view.utils.list_widgets import ListLayout
from view.utils.hyphenate_text import HyphenatedLabel

from view.style.ui_style import WidgetRole, WidgetColor


class VisualizzaPrenotazioneView(AbstractVisualizzaView):
    """Pagina per visualizzare le singoli `Prenotazione` in dettaglio.

    Contiene le tutte informazioni dello `Prenotazione` ed una lista con tutti i `Posto`
    associati ad essa. Permette di segnarla come `pagata` o `non pagata`.

    Segnali
    ---
    - `displayEventiRequest(ListLayout)`: emesso per mostrare a schermo la lista eventi;
    - `nuovoEventoRequest()`: emesso quando si clicca il pulsante Nuovo evento;
    - `visualizzaPrezziRequest(int)`: emesso quando si clicca il pulsanti Lista prezzi.
    # - CORREGIR
    """

    # displayEventiRequest = pyqtSignal(ListLayout)
    # nuovoEventoRequest = pyqtSignal()
    # visualizzaPrezziRequest = pyqtSignal(int)
    aggiornaStatoPrenotazione = pyqtSignal(bool)

    def __init__(self):
        self.id_current_prenotazione: int = -1

        super().__init__()

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        # Labels
        self.label_nominativo = HyphenatedLabel("[Nominativo Prenotazione]")
        self.label_nominativo.setProperty(WidgetRole.HEADER1, True)
        self.label_nominativo.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.label_spettacolo = HyphenatedLabel(
            "<b>Spettacolo</b>: [Titolo Spettacolo]"
        )
        self.label_spettacolo.setProperty(WidgetRole.BODY_TEXT, True)
        self.label_spettacolo.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)

        self.label_emmisione = HyphenatedLabel("<b>Emissione</b>: [Data Emissione]")
        self.label_emmisione.setProperty(WidgetRole.BODY_TEXT, True)
        self.label_emmisione.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)

        self.label_prezzo = HyphenatedLabel("<b>Prezzo</b>: € [Ammontare Prezzo]")
        self.label_prezzo.setProperty(WidgetRole.BODY_TEXT, True)
        self.label_prezzo.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)

        # Stato pagata
        self.label_stato = HyphenatedLabel("<b>Stato</b>: [Pagata/Non pagata]")
        self.label_stato.setProperty(WidgetRole.BODY_TEXT, True)
        self.label_stato.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)
        self.label_stato.setFixedWidth(self.label_stato.sizeHint().width())

        self.__checkbox_stato = QCheckBox()

        content_stato = QWidget()
        layout_stato = QHBoxLayout(content_stato)
        layout_stato.setContentsMargins(0, 0, 0, 0)
        layout_stato.addWidget(self.label_stato)
        layout_stato.addWidget(self.__checkbox_stato)
        layout_stato.addStretch()

        # # Lista Eventi
        # label_lista_eventi = QLabel("Lista eventi")
        # label_lista_eventi.setProperty(WidgetRole.HEADER2, True)

        # header_eventi = QWidget()
        # self.layout_header_eventi = QHBoxLayout(header_eventi)
        # self.layout_header_eventi.setContentsMargins(0, 0, 0, 0)
        # self.layout_header_eventi.addWidget(label_lista_eventi)

        # if self.is_biglietteria:
        #     self.__btn_nuovo_evento = DefaultButton("Nuovo evento")
        #     self.layout_header_eventi.addWidget(self.__btn_nuovo_evento)

        # self.layout_header_eventi.addStretch()

        # self.lista_eventi: list[Evento] = []

        # label_lista_eventi_vuota = EmptyStateLabel(
        #     "Al momento, non vi sono eventi per questo spettacolo."
        # )
        # label_lista_eventi_vuota.setProperty(WidgetRole.BODY_TEXT, True)
        # label_lista_eventi_vuota.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)

        # content_lista_eventi = QWidget()
        # content_lista_eventi.setProperty(WidgetRole.ITEM_LIST, True)
        # self.layout_lista_eventi = ListLayout(
        #     content_lista_eventi, label_lista_eventi_vuota
        # )

        # header_data = QLabel("Data")
        # header_data.setProperty(WidgetRole.HEADER3, True)
        # header_ora = QLabel("Ora")
        # header_ora.setProperty(WidgetRole.HEADER3, True)
        # header_opzioni = QLabel("Opzioni")
        # header_opzioni.setProperty(WidgetRole.HEADER3, True)

        # header_lista_eventi = QWidget()
        # layout_header_lista_eventi = QGridLayout(header_lista_eventi)
        # layout_header_lista_eventi.setContentsMargins(1, 1, 1, 1)
        # layout_header_lista_eventi.addWidget(
        #     header_data, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter
        # )
        # layout_header_lista_eventi.addWidget(make_vline(), 0, 1)
        # layout_header_lista_eventi.addWidget(
        #     header_ora, 0, 2, alignment=Qt.AlignmentFlag.AlignCenter
        # )

        # layout_header_lista_eventi.addWidget(make_vline(), 0, 3)
        # layout_header_lista_eventi.addWidget(
        #     header_opzioni, 0, 4, alignment=Qt.AlignmentFlag.AlignCenter
        # )

        # self.eventi = QWidget()
        # self.layout_eventi = QVBoxLayout(self.eventi)
        # self.layout_eventi.addWidget(header_eventi)
        # self.layout_eventi.addWidget(header_lista_eventi)
        # self.layout_eventi.addWidget(content_lista_eventi)
        # # end-Lista Eventi

        # Layout
        self._layout_content.addWidget(self.label_nominativo)
        self._layout_content.addWidget(self.label_spettacolo)
        self._layout_content.addWidget(self.label_emmisione)
        self._layout_content.addWidget(self.label_prezzo)
        self._layout_content.addWidget(content_stato)
        # if self.is_biglietteria:
        #     self.__btn_visualizza_prezzi = DefaultButton("Lista Prezzi")
        #     self._layout_content.addWidget(self.__btn_visualizza_prezzi)
        # self._layout_content.addWidget(make_hline())
        # self._layout_content.addWidget(self.eventi)
        self._layout_content.addStretch()

    @override
    def _connect_signals(self) -> None:
        super()._connect_signals()

        self.__checkbox_stato.toggled.connect(  # type:ignore
            self.__on_checkbox_stato_toggled
        )

        # if self.is_biglietteria:
        #     self.__btn_nuovo_evento.clicked.connect(  # type:ignore
        #         self.nuovoEventoRequest.emit
        #     )

        #     self.__btn_visualizza_prezzi.clicked.connect(  # type:ignore
        #         lambda: self.visualizzaPrezziRequest.emit(self.id_current_spettacolo)
        #     )

    # ------------------------- METODI DI VIEW -------------------------

    @override
    def set_data(self, data: PrenotazionePageData) -> None:  # type: ignore[override]
        """Carica i dati dello spettacolo nella pagina.

        :param data: data salvata in una classe immutabile
        :param lista_eventi: lista degli eventi associati allo spettacolo
        # - CORREGIR"""
        # # Reset layout lista regie
        # self.layout_lista_eventi.svuota_layout()

        # Salva dati della prenotazione nella pagina
        self.id_current_prenotazione = data.id
        # self.lista_eventi = lista_eventi

        # Carica dati della prenotazione
        self.label_nominativo.setText(f"{data.nominativo}")
        self.label_spettacolo.setText(
            "<b>Spettacolo</b>: [Titolo Spettacolo]"
        )  # - ARREGLAR
        self.label_emmisione.setText(
            "<b>Emissione</b>: "
            + data.data_ora_registrazione.strftime("%a %b %d %Y %H:%M:%S")
        )
        self.label_prezzo.setText("<b>Prezzo</b>: € [Ammontare Prezzo]")  # - ARREGLAR
        self.__checkbox_stato.setChecked(data.is_pagata)

        # self.__svuota_layout_generico(self.layout_dati_speciali)
        # if type(data) is RegiaPageData:
        #     label_regista = QLabel(f"<b>Regista:</b> {data.regista}")
        #     label_regista.setProperty(WidgetRole.BODY_TEXT, True)
        #     label_regista.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)
        #     self.layout_dati_speciali.addWidget(label_regista)

        #     label_anno = QLabel(f"<b>Anno di produzione:</b> {data.anno_produzione}")
        #     label_anno.setProperty(WidgetRole.BODY_TEXT, True)
        #     label_anno.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)
        #     self.layout_dati_speciali.addWidget(label_anno)
        # else:  # Caso Spettacolo generico
        #     ...

        # # Carica lista regie
        # if not self.lista_eventi:
        #     self.layout_lista_eventi.mostra_msg_lista_vuota()
        # else:
        #     self.displayEventiRequest.emit(self.layout_lista_eventi)

    def __on_checkbox_stato_toggled(self, checked: bool) -> None:
        self.aggiornaStatoPrenotazione.emit(checked)
        stato = "Pagata" if checked else "Non pagata"
        self.label_stato.setText("<b>Stato</b>: " + stato)

    @override
    def aggiorna_pagina(self) -> None:
        super().aggiorna_pagina()

        # self.layout_lista_eventi.svuota_layout()
        # self.displayEventiRequest.emit(self.layout_lista_eventi)

    # def __svuota_layout_generico(self, layout: QLayout):
    #     while layout.count() > 0:
    #         item = layout.takeAt(0)
    #         if item is None:
    #             raise ValueError("Expected item at index 0")
    #         if widget := item.widget():
    #             widget.setParent(None)
    #         elif child_layout := item.layout():
    #             self.__svuota_layout_generico(child_layout)
