from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QLayout,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Optional

from model.pianificazione.regia import Regia

from view.info.operaPageData import OperaPageData


class VisualizzaOperaView(QWidget):
    """
    View per visualizzare le singole opere in dettaglio.

    Contiene le informazioni anagrafiche dell'opera ed una lista con tutte
    le regie vinculate ad essa.

    Segnali:
    - tornaIndietroRequest(): emesso quando si clicca il pulsante Indietro.
    """

    tornaIndietroRequest = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

        self._setup_ui()
        self._connect_signals()

    # ------------------------- SETUP INIT -------------------------

    def _setup_ui(self) -> None:
        # Labels
        self.label_nome = QLabel("NOME")
        self.label_nome.setObjectName("Header1")
        self.label_nome.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.label_librettista = QLabel("Libretto di LIBRETTISTA.")
        self.label_librettista.setWordWrap(True)
        self.label_librettista.setObjectName("Paragraph")

        self.label_compositore = QLabel("Musica composta da COMPOSITORE.")
        self.label_compositore.setWordWrap(True)
        self.label_compositore.setObjectName("Paragraph")

        self.label_genere = QLabel(f"Genere: GENERE")
        self.label_genere.setObjectName("Paragraph")

        self.label_atti = QLabel(f"Numero di atti: ATTI")
        self.label_atti.setObjectName("Paragraph")

        self.label_prima_rappresentazione = QLabel(
            f"È stata rappresentata per prima volta il DATA nel teatro TEATRO."
        )
        self.label_prima_rappresentazione.setWordWrap(True)
        self.label_prima_rappresentazione.setObjectName("Paragraph")

        self.label_trama = QLabel("TRAMA")
        self.label_trama.setWordWrap(True)
        self.label_trama.setObjectName("Paragraph")

        self.label_lista_regie = QLabel("Lista regie")
        self.label_lista_regie.setObjectName("Header2")

        self.regie = QWidget()
        self.layout_regie = QVBoxLayout(self.regie)
        self.layout_regie.addWidget(self.label_lista_regie)
        self.layout_regie.addStretch()

        self.lista_vuota_error = QLabel("")
        self.lista_vuota_error.setObjectName("SubHeader")

        content = QWidget()
        layout_content = QVBoxLayout(content)
        layout_content.addWidget(self.label_nome)
        layout_content.addWidget(self.label_librettista)
        layout_content.addWidget(self.label_compositore)
        layout_content.addWidget(self.label_genere)
        layout_content.addWidget(self.label_atti)
        layout_content.addWidget(self.label_prima_rappresentazione)
        layout_content.addWidget(self.label_trama)
        layout_content.addWidget(self.regie)
        layout_content.addWidget(self.lista_vuota_error)
        layout_content.addStretch()

        # Pulsante: Indientro
        self._btn_indietro = QPushButton("Indietro")
        self._btn_indietro.setObjectName("WhiteButton")

        self.pulsanti = QWidget()
        layout_pulsanti = QHBoxLayout(self.pulsanti)
        layout_pulsanti.addWidget(self._btn_indietro)
        layout_pulsanti.addStretch()

        # Funzione di scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(content)

        # Layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.pulsanti)
        main_layout.addWidget(scroll_area)

    def _connect_signals(self):
        self._btn_indietro.clicked.connect(  # type:ignore
            self.tornaIndietroRequest.emit
        )

    # ------------------------- METODI DI VIEW -------------------------

    def set_data(
        self, data: OperaPageData, genere_nome: str, lista_regie: list[Regia]
    ) -> None:
        """Carica i dati dell'opera nella pagina.

        :param data: data salvata in una classe immutabile
        :param genere_nome: nome del genere scelto per l'opera
        :param lista_regie: lista delle regie vincolate all'opera"""
        LISTA_REGIE_VUOTA = "Al momento, non vi sono regie per questa opera."

        self.clear_layout(self.layout_regie)
        self.layout_regie.addWidget(self.label_lista_regie)
        self.lista_vuota_error.setText("")

        self.label_nome.setText(f"{data.nome}")
        self.label_librettista.setText(f"Libretto di {data.librettista}")
        self.label_compositore.setText(f"Musica composta da {data.compositore}")
        self.label_genere.setText(f"Genere: {genere_nome}")
        self.label_atti.setText(f"Numero di atti: {data.atti}")
        self.label_prima_rappresentazione.setText(
            "È stata rappresentata per prima volta il "
            + f"{data.data_rappresentazione.strftime("%d/%m/%y")} "
            + f"nel teatro {data.teatro_rappresentazione}"
        )
        self.label_trama.setText(f"{data.trama}")

        if not lista_regie:
            self.lista_vuota_error.setText(LISTA_REGIE_VUOTA)

        for r in lista_regie:
            self.display_regia(r, self.layout_regie)

    def display_regia(self, r: Regia, layout: QVBoxLayout) -> None:
        """Visualizza a schermo alcune informazioni della regia.

        :param r: regia da mostrare
        :param layout: layout in cui sarà mostrata la regia"""
        # - Creo un regiaDisplay per questo o lo lascio così? Dipenderà di come vogliono
        #   loro che le regie siano visualizzate.
        widget_regia = QWidget()
        widget_regia.setObjectName("Container")
        layout_regia = QVBoxLayout(widget_regia)

        titolo = QLabel(f"{r.get_titolo()}")
        titolo.setObjectName("Header2")
        titolo.setAlignment(Qt.AlignmentFlag.AlignLeft)

        regista = QLabel(f"Regista: {r.get_regista()}")
        regista.setObjectName("Paragraph")

        anno = QLabel(f"Anno di produzione: {r.get_anno_produzione()}")
        anno.setObjectName("Paragraph")

        layout_regia.addWidget(titolo)
        layout_regia.addWidget(regista)
        layout_regia.addWidget(anno)
        layout_regia.addStretch()

        layout.addWidget(widget_regia)

    def clear_layout(self, layout: Optional[QLayout]) -> None:
        """Pulisce un layout, eliminando i riferimenti ai widget contenuti. In caso
        ci sia un layout contenuto, questo viene anche pulito.

        :param layout: layout da pulire"""
        # Siccome il layout solo contiene widget di regie, non è necessario rimuovere dei layout.
        #   Comunque, lascio la parte finale per completezza.
        if layout:
            while layout.count():
                item = layout.takeAt(0)
                assert item is not None
                widget = item.widget()

                if widget:
                    widget.setParent(None)
                    continue

                child_layout = item.layout()
                if child_layout:
                    self.clear_layout(child_layout)
