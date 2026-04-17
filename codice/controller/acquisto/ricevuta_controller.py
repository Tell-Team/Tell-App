from PyQt6.QtCore import QObject, pyqtSignal
from functools import partial

from controller.navigation import Pagina

from model.model.model import Model, RicevutaData

from view.acquisto.pagine import RicevutaPage
from view.acquisto.widgets import EventoPostiDisplay

from view.utils.list_widgets import ListLayout

from view.style.ui_style import WidgetRole


class RicevutaController(QObject):
    """Gestice la pagina `RicevutaPage` dell'app."""

    goToSectionRequest = pyqtSignal(Pagina)

    def __init__(self, model: Model, pagina_ricevuta: RicevutaPage):
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

        :param layout_posti_scelti: layout dove saranno caricati tutti i posti scelti"""
        evento_dataora, lista_sezione_posti = self.__pagina_ricevuta.lista_posti_scelti

        # Verifica che la lista non sia vuota
        if evento_dataora is None or not lista_sezione_posti:
            layout_posti_scelti.mostra_msg_lista_vuota()
            return

        current_evento_posti = EventoPostiDisplay(evento_dataora, lista_sezione_posti)

        layout_posti_scelti.aggiungi_list_item(
            current_evento_posti, WidgetRole.Item.CARD
        )

    def __stampa_ricevuta(self) -> None:
        data = self.__pagina_ricevuta.data_ricevuta
        html_output = render_ricevuta_html(data)
        stampa_ricevuta_html(html_output)

        # Se è necessario accedere al HTML direttamente
        # with open("controller/acquisto/output.html", "w", encoding="utf-8") as f:
        #     f.write(html_output)

        self.__pagina_ricevuta.abilita_btn_fine(True)


# ------------------------- Funzioni per stampare ricevuta -------------------------
def render_ricevuta_html(data: RicevutaData) -> str:
    posti_scelti_html = "\n".join(
        f"""
    <div>
        <span>Sezione: {s_p.sezione_nome}</span>
        {''.join(
            f'''
            <table width="100%">
                <tr>
                    <td align="left">
                        <span>- {posto.get_fila()} #{posto.get_numero()}</span>
                    </td>
                    <td align="right">
                        <span>{s_p.prezzo_ammontare:.2f}</span>
                    </td>
                </tr>
            </table>
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
            @page {{ size: A5; margin: 1in; }}

            body {{
                font-family: monospace;
                padding-left: 5px;
                color: #000000;
            }}

            body * {{
                font-size: 16px;
            }}

            h1, h2, h3 {{
                font-family: "Playfair Display", serif;
            }}

            .title-block {{
                line-height: 18px;
            }}

            .title-block * {{
                text-align: center;
                margin: 2px;
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

        <table width="100%">
            <tr>
                <td align="left">
                    <span style="font-size: 18px;">POSTI SCELTI</span>
                </td>
                <td align="right">
                    <span style="font-size: 18px;">PREZZO</span>
                </td>
            </tr>
        </table>

        <div style="text-align: left;">
            {posti_scelti_html}
        </div>

        <hr style="border: none; border-top: 1px solid black;">

        <table width="100%">
            <tr>
                <td align="left">
                    <span style="font-size: 20px;">TOTALE COMPLESSIVO</span>
                </td>
                <td align="right">
                    <span style="font-size: 20px;">{data.prezzo_complessivo:.2f}</span>
                </td>
            </tr>
        </table>

        <div class="text-box">
            <p>DATA EMMISSIONE: {data.emmisione_dataora.strftime("%d/%m/%y - %H:%M")}</p>
            <p>NOMINATIVO: {data.nominativo}</p>
        </div>

    </body>
</html>
"""


def stampa_ricevuta_html(html: str) -> None:
    from PyQt6.QtPrintSupport import QPrinter, QPrinterInfo
    from PyQt6.QtGui import QTextDocument, QPageSize

    doc = QTextDocument()
    doc.setHtml(html)

    default_info = QPrinterInfo.defaultPrinter()
    if default_info.isNull():
        print("No default printer found!")
    else:
        printer = QPrinter(default_info)
        printer.setPageSize(QPageSize(QPageSize.PageSizeId.A5))
        printer.setFullPage(False)

        # Blocco per testare il formato del HTML prima di stamparlo
        # from PyQt6.QtPrintSupport import QPrintPreviewDialog
        # preview = QPrintPreviewDialog(printer)
        # preview.paintRequested.connect(doc.print)
        # preview.exec()

        print("Using:", default_info.printerName())
        doc.print(printer)
