from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QCheckBox
from PyQt6.QtCore import Qt, pyqtSignal
from datetime import datetime
from typing import Optional, override

from core.view import AbstractVisualizzaView

from model.model.model import PrenotazioneData, SezionePostiInfo

from view.utils.list_widgets import ListLayout, EmptyStateLabel
from view.utils.hyphenate_text import HyphenatedLabel

from view.style.ui_style import WidgetRole, WidgetColor


class VisualizzaPrenotazionePage(AbstractVisualizzaView):
    """Pagina per visualizzare le singoli `Prenotazione` in dettaglio.

    Contiene le tutte informazioni di `Prenotazione` ed una lista con tutti i `Posto`
    associati ad essa. Permette di segnarla come `pagata` o `non pagata`.

    Segnali
    ---
    - `displayPostiRequest(ListLayout)`: emesso per mostrare a schermo la lista posti.
    - `aggiornaStatoPrenotazione(bool)`: emesso per aggiornare lo stato di `pagata` della
        prenotazione.
    """

    displayPostiRequest = pyqtSignal(ListLayout)
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
        self.label_nominativo.setProperty(WidgetRole.Label.HEADER1, True)
        self.label_nominativo.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.label_spettacolo = HyphenatedLabel(
            "<b>Spettacolo</b>: [Titolo Spettacolo]"
        )
        self.label_spettacolo.setProperty(WidgetRole.Label.BODY_TEXT, True)
        self.label_spettacolo.setProperty(WidgetColor.Label.PRIMARY_COLOR, True)

        self.label_emmisione = HyphenatedLabel("<b>Emissione</b>: [Data Emissione]")
        self.label_emmisione.setProperty(WidgetRole.Label.BODY_TEXT, True)
        self.label_emmisione.setProperty(WidgetColor.Label.PRIMARY_COLOR, True)

        self.label_prezzo = HyphenatedLabel("<b>Prezzo</b>: € [Ammontare Prezzo]")
        self.label_prezzo.setProperty(WidgetRole.Label.BODY_TEXT, True)
        self.label_prezzo.setProperty(WidgetColor.Label.PRIMARY_COLOR, True)

        # Stato pagata
        self.label_stato = HyphenatedLabel("<b>Stato</b>: [Pagata/Non pagata]")
        self.label_stato.setProperty(WidgetRole.Label.BODY_TEXT, True)
        self.label_stato.setProperty(WidgetColor.Label.PRIMARY_COLOR, True)
        self.label_stato.setFixedWidth(self.label_stato.sizeHint().width())

        self.__checkbox_stato = QCheckBox()
        self.__checkbox_stato.setProperty("stato-pagamento", True)

        content_stato = QWidget()
        layout_stato = QHBoxLayout(content_stato)
        layout_stato.setContentsMargins(0, 0, 0, 0)
        layout_stato.addWidget(self.label_stato)
        layout_stato.addWidget(self.__checkbox_stato)
        layout_stato.addStretch()

        # Lista Posti
        label_lista_posti = QLabel("Lista posti")
        label_lista_posti.setProperty(WidgetRole.Label.HEADER2, True)

        self.lista_evento_posti: tuple[Optional[datetime], list[SezionePostiInfo]] = (
            None,
            [],
        )

        label_lista_posti_vuota = EmptyStateLabel("Non vi sono posti prenotati.")
        label_lista_posti_vuota.setProperty(WidgetRole.Label.BODY_TEXT, True)
        label_lista_posti_vuota.setProperty(WidgetColor.Label.SECONDARY_COLOR, True)

        content_lista_posti = QWidget()
        self.layout_lista_posti = ListLayout(
            content_lista_posti, label_lista_posti_vuota
        )

        self.posti = QWidget()
        self.layout_posti = QVBoxLayout(self.posti)
        self.layout_posti.addWidget(label_lista_posti)
        self.layout_posti.addWidget(content_lista_posti)
        self.layout_posti.addStretch()
        # end-Lista Posti

        # Layout
        self._layout_content.addWidget(self.label_nominativo)
        self._layout_content.addWidget(self.label_spettacolo)
        self._layout_content.addWidget(self.label_emmisione)
        self._layout_content.addWidget(self.label_prezzo)
        self._layout_content.addWidget(content_stato)
        self._layout_content.addWidget(self.posti)
        self._layout_content.addStretch()

    @override
    def _connect_signals(self) -> None:
        super()._connect_signals()

        self.__checkbox_stato.toggled.connect(  # type:ignore
            self.__on_checkbox_stato_toggled
        )

    # ------------------------- METODI DI VIEW -------------------------

    def __on_checkbox_stato_toggled(self, checked: bool) -> None:
        stato = "Pagata" if checked else "Non pagata"
        self.label_stato.setText("<b>Stato</b>: " + stato)
        self.aggiornaStatoPrenotazione.emit(checked)

    @override
    def set_data(self, data: PrenotazioneData) -> None:  # type: ignore[override]
        """Carica i dati dello spettacolo nella pagina.

        :param data: data salvata in una classe immutabile
        :param dettagli: dataclass con lo spettacolo, evento e posti associati
        alla prenotazione"""
        # Reset layout lista posti
        self.layout_lista_posti.svuota_layout()

        # Carica dati della prenotazione
        self.id_current_prenotazione = data.id

        self.label_nominativo.setText(f"{data.nominativo}")
        self.label_spettacolo.setText(f"<b>Spettacolo</b>: {data.spettacolo_titolo}")
        self.label_emmisione.setText(
            "<b>Emissione</b>: "
            + data.emmisione_dataora.strftime("%a %b %d %Y %H:%M:%S")
        )
        self.label_prezzo.setText(f"<b>Prezzo</b>: € {data.prezzo_complessivo:.2f}")

        self.lista_evento_posti = (data.evento_dataora, data.sezioni_posti)

        self.__on_checkbox_stato_toggled(data.is_pagata)
        self.__checkbox_stato.setChecked(data.is_pagata)

    @override
    def aggiorna_pagina(self) -> None:
        super().aggiorna_pagina()

        self.layout_lista_posti.svuota_layout()
        self.displayPostiRequest.emit(self.layout_lista_posti)
