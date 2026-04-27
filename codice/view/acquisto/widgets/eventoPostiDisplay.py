from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from datetime import datetime

from model.model.model import SezionePostiInfo
from model.organizzazione.posto import Posto

from view.utils.list_widgets import ItemDisplay
from view.utils.hyphenate_text import HyphenatedLabel

from view.style.ui_style import WidgetRole, WidgetColor


class EventoPostiDisplay(ItemDisplay):
    """View dei posti prenotati per un evento. È usato nelle pagine `RicevutaPage` e
    `VisualizzaPrenotazionePage`."""

    def __init__(self, evento_data: datetime, s_p: list[SezionePostiInfo]):
        super().__init__()

        self.__setup_ui(evento_data, s_p)

    def __setup_ui(self, evento_data: datetime, s_p: list[SezionePostiInfo]) -> None:
        label_data = QLabel(f"<b>Data</b>: {evento_data.strftime("%d/%m/%y - %H:%M")}")
        label_data.setProperty(WidgetRole.Label.BODY_TEXT, True)
        label_data.setProperty(WidgetColor.Label.PRIMARY_COLOR, True)

        label_posti = QLabel("<b>Posti</b>:")
        label_posti.setProperty(WidgetRole.Label.BODY_TEXT, True)
        label_posti.setProperty(WidgetColor.Label.PRIMARY_COLOR, True)

        container_posti = QWidget()
        layout_posti = QVBoxLayout(container_posti)
        layout_posti.setContentsMargins(15, 1, 1, 1)

        layout = QVBoxLayout(self)
        layout.addWidget(label_data)
        layout.addWidget(label_posti)
        layout.addWidget(container_posti)

        def make_label_posto(
            sezione_nome: str, prezzo_ammontare: float, p: Posto
        ) -> QLabel:
            label = HyphenatedLabel(
                f"- [<b>€ {prezzo_ammontare:.2f}</b>] "
                + f"<b>Sezione:</b> {sezione_nome}, "
                + f"<b>Posto:</b> {p.get_fila()} #{p.get_numero()}"
            )
            label.setProperty(WidgetRole.Label.BODY_TEXT, True)
            label.setProperty(WidgetColor.Label.PRIMARY_COLOR, True)
            return label

        for sezione_nome, prezzo_ammontare, posto in (
            (sp.sezione_nome, sp.prezzo_ammontare, p) for sp in s_p for p in sp.posti
        ):
            layout_posti.addWidget(
                make_label_posto(sezione_nome, prezzo_ammontare, posto)
            )

        layout.addStretch()
