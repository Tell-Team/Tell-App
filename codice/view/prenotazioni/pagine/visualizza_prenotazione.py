from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QCheckBox
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Optional, override

from core.view import AbstractVisualizzaView

from model.model.model import DettagliPrenotazione
from model.organizzazione.evento import Evento
from model.organizzazione.sezione import Sezione
from model.organizzazione.posto import Posto

from view.prenotazioni.utils import PrenotazioneData

from view.utils.list_widgets import ListLayout, EmptyStateLabel
from view.utils.hyphenate_text import HyphenatedLabel

from view.style.ui_style import WidgetRole, WidgetColor


class VisualizzaPrenotazioneView(AbstractVisualizzaView):
    """Pagina per visualizzare le singoli `Prenotazione` in dettaglio.

    Contiene le tutte informazioni dello `Prenotazione` ed una lista con tutti i `Posto`
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

        # Lista Posti
        label_lista_posti = QLabel("Lista posti")
        label_lista_posti.setProperty(WidgetRole.HEADER2, True)

        self.lista_evento_posti: Optional[
            tuple[Evento, list[tuple[Sezione, list[Posto]]]]
        ] = None

        label_lista_posti_vuota = EmptyStateLabel("Non vi sono posti prenotati.")
        label_lista_posti_vuota.setProperty(WidgetRole.BODY_TEXT, True)
        label_lista_posti_vuota.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)

        content_lista_posti = QWidget()
        content_lista_posti.setProperty(WidgetRole.ITEM_LIST, True)
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
    def set_data(  # type: ignore[override]
        self,
        data: PrenotazioneData,
        dettagli: DettagliPrenotazione,
    ) -> None:
        """Carica i dati dello spettacolo nella pagina.

        :param data: data salvata in una classe immutabile
        :param dettagli: dataclass con lo spettacolo, evento e posti associati
        alla prenotazione"""
        # Reset layout lista posti
        self.layout_lista_posti.svuota_layout()

        # Salva dati della prenotazione nella pagina
        self.id_current_prenotazione = data.id
        lista_sezione_posti = [(x.sezione, x.posti) for x in dettagli.sezioni]
        self.lista_evento_posti = (dettagli.evento, lista_sezione_posti)

        # Carica dati della prenotazione
        self.label_nominativo.setText(f"{data.nominativo}")
        self.label_spettacolo.setText(
            f"<b>Spettacolo</b>: {dettagli.spettacolo.get_titolo()}"
        )
        self.label_emmisione.setText(
            "<b>Emissione</b>: "
            + data.data_ora_registrazione.strftime("%a %b %d %Y %H:%M:%S")
        )
        self.label_prezzo.setText(f"<b>Prezzo</b>: € {data.ammontare:.2f}")
        self.__on_checkbox_stato_toggled(data.is_pagata)
        self.__checkbox_stato.setChecked(data.is_pagata)

        # Carica lista posti
        if not self.lista_evento_posti:
            self.layout_lista_posti.mostra_msg_lista_vuota()
        else:
            self.displayPostiRequest.emit(self.layout_lista_posti)

    @override
    def aggiorna_pagina(self) -> None:
        super().aggiorna_pagina()

        self.layout_lista_posti.svuota_layout()
        self.displayPostiRequest.emit(self.layout_lista_posti)
