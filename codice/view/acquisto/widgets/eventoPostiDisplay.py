from PyQt6.QtWidgets import QLabel, QVBoxLayout

from model.organizzazione.evento import Evento
from model.organizzazione.sezione import Sezione
from model.organizzazione.posto import Posto

from view.utils.list_widgets import ItemDisplay

from view.style.ui_style import WidgetRole, WidgetColor


class EventoPostiDisplay(ItemDisplay):
    """View dei posti prenotati per un'evento. È usato nella pagina `RicevutaView`."""

    def __init__(self, e: Evento, sp: list[tuple[Sezione, list[Posto]]]):
        super().__init__()

        self.__setup_ui(e, sp)

    def __setup_ui(self, e: Evento, sp: list[tuple[Sezione, list[Posto]]]) -> None:
        label_data = QLabel(
            f"<b>Data</b>: {e.get_data_ora().strftime("%d/%m/%y - %H:%M")}"
        )
        label_data.setProperty(WidgetRole.BODY_TEXT, True)
        label_data.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)

        label_posti = QLabel("<b>Posti</b>:")
        label_posti.setProperty(WidgetRole.BODY_TEXT, True)
        label_posti.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)

        layout = QVBoxLayout(self)
        layout.addWidget(label_data)
        layout.addWidget(label_posti)

        def make_label_posto(s: Sezione, p: Posto) -> QLabel:
            label = QLabel(
                f"  - Sezione: {s.get_nome()}, Posto: {p.get_fila()} #{p.get_numero()}"
            )
            label.setProperty(WidgetRole.BODY_TEXT, True)
            label.setProperty(WidgetColor.Text.PRIMARY_TEXT, True)
            return label

        for label in (make_label_posto(s, p) for s, posti in sp for p in posti):
            layout.addWidget(label)

        layout.addStretch()
