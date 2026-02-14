from PyQt6.QtWidgets import QLabel, QVBoxLayout
from datetime import datetime

from model.model.model import SezionePostiInfo
from model.organizzazione.posto import Posto

from view.utils.list_widgets import ItemDisplay

from view.style.ui_style import WidgetRole, WidgetColor


class EventoPostiDisplay(ItemDisplay):
    """View dei posti prenotati per un'evento. È usato nelle pagine `RicevutaView` e
    `VisualizzaPrenotazioneView`."""

    def __init__(self, evento_data: datetime, s_p: list[SezionePostiInfo]):
        super().__init__()

        self.__setup_ui(evento_data, s_p)

    def __setup_ui(self, evento_data: datetime, s_p: list[SezionePostiInfo]) -> None:
        label_data = QLabel(f"<b>Data</b>: {evento_data.strftime("%d/%m/%y - %H:%M")}")
        label_data.setProperty(WidgetRole.BODY_TEXT, True)
        label_data.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)

        label_posti = QLabel("<b>Posti</b>:")
        label_posti.setProperty(WidgetRole.BODY_TEXT, True)
        label_posti.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)

        layout = QVBoxLayout(self)
        layout.addWidget(label_data)
        layout.addWidget(label_posti)

        def make_label_posto(
            sezione_nome: str, prezzo_ammontare: float, p: Posto
        ) -> QLabel:
            label = QLabel(
                f"  - [€ {prezzo_ammontare:.2f}] Sezione: {sezione_nome}, Posto: {p.get_fila()} #{p.get_numero()}"
            )
            label.setProperty(WidgetRole.BODY_TEXT, True)
            label.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)
            return label

        for sezione_nome, prezzo_ammontare, posto in (
            (sp.sezione_nome, sp.prezzo_ammontare, p) for sp in s_p for p in sp.posti
        ):
            layout.addWidget(make_label_posto(sezione_nome, prezzo_ammontare, posto))

        layout.addStretch()
