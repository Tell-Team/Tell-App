from PyQt6.QtCore import QObject, pyqtSignal
from functools import partial

from controller.navigation import Pagina

from model.model.model import Model, RicevutaData

from view.acquisto.pagine import RicevutaView
from view.acquisto.widgets import EventoPostiDisplay

from view.utils.list_widgets import ListLayout

from view.style.ui_style import WidgetRole


class RicevutaController(QObject):
    """Gestice la pagina `RicevutaView` dell'app."""

    goToSectionRequest = pyqtSignal(Pagina)

    def __init__(self, model: Model, pagina_ricevuta: RicevutaView):
        super().__init__()

        self.__model = model
        self.__pagina_ricevuta = pagina_ricevuta

        self.__connect_signals()

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    def __connect_signals(self) -> None:
        self.__pagina_ricevuta.displayPostiSceltiRequest.connect(  # type:ignore
            self.__display_posti_scelti
        )

        self.__pagina_ricevuta.stampaRicevuta.connect(  # type:ignore
            self.__stampa_ricevuta
        )

        self.__pagina_ricevuta.ritornaAllaMainPage.connect(  # type:ignore
            partial(self.goToSectionRequest.emit, Pagina.SEZIONE_ACQUISTO)
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __display_posti_scelti(self, layout_posti_scelti: ListLayout) -> None:
        """Mostra a schermo le informazioni dei posti prenotati.

        :param layout_posti_scelti: layout dove saranno caricati tutti i posti scelti
        """
        pagina = self.__pagina_ricevuta
        evento_dataora, lista_sezione_posti = pagina.lista_posti_scelti

        if evento_dataora is None or not lista_sezione_posti:
            layout_posti_scelti.mostra_msg_lista_vuota()
            return

        current_posto_scelto = EventoPostiDisplay(evento_dataora, lista_sezione_posti)

        layout_posti_scelti.aggiungi_list_item(
            current_posto_scelto, WidgetRole.ITEM_CARD
        )

    def __stampa_ricevuta(self) -> None:

        data = self.__pagina_ricevuta.data_ricevuta
        html_output = render_ricevuta_html(data)
        stampa_ricevuta_html(html_output)

        # - TESTING
        with open("controller/acquisto/output.html", "w", encoding="utf-8") as f:
            f.write(html_output)

        self.__pagina_ricevuta.abilita_btn_fine(True)


# ------------------------- Funzioni per stampare ricevuta -------------------------
def render_ricevuta_html(data: RicevutaData) -> str:
    posti_scelti_html = "\n".join(
        f"""
    <div>
        <span>Sezione: {s_p.sezione_nome}</span>
        {''.join(
            f'''
            <div class="justified-text">
                <span style="margin-left: 20px;">{posto.get_fila()} #{posto.get_numero()}</span>
                <span>{s_p.prezzo_ammontare:.2f}</span>
            </div>
            '''
            for posto in s_p.posti
        )}
    </div>
    """
        for s_p in data.sezioni_posti
    )

    return f"""
<html>
    <head>
        <style>
            @page {{ size: A4; margin: 1in; }}

            body {{
                font-family: monospace;
                padding-left: 5px;
            }}

            body * {{
                font-size: 16px;
            }}

            h1, h2, h3 {{
                font-family: "Playfair Display", serif;
            }}

            .title-block {{
                text-align: center;
                line-height: 18px;
            }}

            .title-block * {{
                margin: 2px;
            }}

            .justified-text {{
                display: flex;
                justify-content: space-between;
            }}

            .text-box {{
                margin-top: 10px;
                margin-bottom: 10px;
            }}

            .text-box * {{
                font-size: 16px;
                margin: 0;
                line-height: 1;
            }}
        </style>
    </head>
    <body>

        <div class="title-block">
            <h2>Tell</h2>
            <h3>Descrizione del teatro</h3>
        </div>

        <div class="text-box">
            <p>SPETTACOLO: {data.spettacolo_titolo}</p>
            <p>DATA EVENTO: {data.evento_dataora.strftime("%d/%m/%y - %H:%M")}</p>
        </div>

        <div class="justified-text">
            <span style="font-size: 18px;">POSTI SCELTI</span>
            <span style="font-size: 18px;">PREZZO</span>
        </div>

        <div style="text-align: left;">
            {posti_scelti_html}
        </div>

        <hr style="border: none; border-top: 1px solid black;">

        <div class="justified-text">
            <span style="font-size: 20px;">TOTALE COMPLESSIVO</span>
            <span style="font-size: 20px;">{data.prezzo_complessivo:.2f}</span>
        </div>

        <div class="text-box">
            <p>DATA EMMISSIONE: {data.emmisione_dataora.strftime("%d/%m/%y - %H:%M")}</p>
            <p>NOMINATIVO: {data.nominativo}</p>
        </div>

    </body>
</html>
"""


def stampa_ricevuta_html(html: str) -> None:
    from PyQt6.QtPrintSupport import QPrinter, QPrinterInfo
    from PyQt6.QtGui import QTextDocument

    doc = QTextDocument()
    doc.setHtml(html)

    default_info = QPrinterInfo.defaultPrinter()
    if default_info.isNull():
        print("No default printer found!")
    else:
        printer = QPrinter(default_info)
        print("Using:", default_info.printerName())
        doc.print(printer)
