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

from view.info.utils.operaPageData import OperaPageData


class VisualizzaOperaView(QWidget):
    """View per visualizzare le singole opere in dettaglio.

    Contiene le informazioni anagrafiche dell'opera ed una lista con tutte
    le regie vinculate ad essa.

    Segnali:
    - tornaIndietroRequest(): emesso quando si clicca il pulsante Indietro;
    - displayRegieRequest(QVBoxLayout): emesso per mostrare la lista regie a schermo;
    - nuovaRegiaRequest(): emesso quando si clicca il pulsante Nuova regia.
    """

    tornaIndietroRequest = pyqtSignal()
    displayRegieRequest = pyqtSignal(QVBoxLayout)
    nuovaRegiaRequest = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

        self._setup_ui()
        self._connect_signals()

    # ------------------------- SETUP INIT -------------------------

    def _setup_ui(self) -> None:
        self.id_cur_opera: int = -1

        # Top widget
        self.__btn_indietro = QPushButton("Indietro")
        self.__btn_indietro.setObjectName("WhiteButton")

        self.pagina_header = QWidget()
        layout_header = QHBoxLayout(self.pagina_header)
        layout_header.addWidget(self.__btn_indietro)
        layout_header.addStretch()

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

        # Lista Regie
        label_lista_regie = QLabel("Lista regie")
        label_lista_regie.setObjectName("Header2")

        self.__btn_nuova_regia = QPushButton("Nuova regia")
        self.__btn_nuova_regia.setObjectName("WhiteButton")

        widget_header_regie = QWidget()
        self.layout_header_regie = QHBoxLayout(widget_header_regie)
        self.layout_header_regie.addWidget(label_lista_regie)
        self.layout_header_regie.addWidget(self.__btn_nuova_regia)
        self.layout_header_regie.addStretch()

        self.lista_regie: list[Regia] = []

        self.label_lista_regie_vuota = QLabel("")
        self.label_lista_regie_vuota.setObjectName("SubHeader")

        widget_lista_regie = QWidget()
        self.layout_lista_regie = QVBoxLayout(widget_lista_regie)
        self.layout_lista_regie.addWidget(self.label_lista_regie_vuota)

        self.regie = QWidget()
        self.layout_regie = QVBoxLayout(self.regie)
        self.layout_regie.addWidget(widget_header_regie)
        self.layout_regie.addWidget(widget_lista_regie)
        # end-Lista Regie

        pagina_content = QWidget()
        layout_content = QVBoxLayout(pagina_content)
        layout_content.addWidget(self.label_nome)
        layout_content.addWidget(self.label_librettista)
        layout_content.addWidget(self.label_compositore)
        layout_content.addWidget(self.label_genere)
        layout_content.addWidget(self.label_atti)
        layout_content.addWidget(self.label_prima_rappresentazione)
        layout_content.addWidget(self.label_trama)
        layout_content.addWidget(self.regie)
        layout_content.addStretch()

        # Funzione di scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(pagina_content)

        # Layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.pagina_header)
        main_layout.addWidget(scroll_area)

    def _connect_signals(self):
        self.__btn_indietro.clicked.connect(  # type:ignore
            self.tornaIndietroRequest.emit
        )

        self.__btn_nuova_regia.clicked.connect(  # type:ignore
            self.nuovaRegiaRequest.emit
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

        # Reset layout lista regie
        self.svuota_layout(self.layout_lista_regie)
        self.layout_lista_regie.addWidget(self.label_lista_regie_vuota)
        self.label_lista_regie_vuota.setText("")

        # Salva dati dell'opera nella pagina
        self.id_cur_opera = data.id
        self.lista_regie = lista_regie

        # Carica dati dell'opera
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

        # Carica lista regie
        if not self.lista_regie:
            self.label_lista_regie_vuota.setText(LISTA_REGIE_VUOTA)
        else:
            self.displayRegieRequest.emit(self.layout_lista_regie)

    # - STUDIARE: Come posso fare questi metodi modullari? (Sono usati i varii pagina non
    #   necessariamente relazionate tra loro)
    def aggiungi_widget_al_layout(self, widget: QWidget, layout: QVBoxLayout):
        """Aggiunge un widget creato per il display delle istanze del model.

        :param widget: widget speciale per visualizzare una instanza del model
        :param layout: layout dove sarà inserito il widget"""
        # C'era un errore al utilizzare widget.setObjectName("Container") direttamente:
        #   lo style non veniva asegnato al widget. Quindi ho decisso di aggiungere questo
        #   dummy widget per farlo funzionare.
        dummy_widget = QWidget()
        dummy_widget.setObjectName("Container")
        l = QVBoxLayout(dummy_widget)
        l.addWidget(widget)

        layout.addWidget(dummy_widget)

    # - Metodo da fare modullare(?)
    def if_lista_vuota(self, layout: QVBoxLayout) -> None:
        """Indica che la lista non ha istanze da visualizzare.

        :param layout: layout dove si mostrerà un messaggio indicando l'assenza di intanze
        """
        # Il suo funzionamento dipende di come aggiorna_pagina aggiunge il label di errore nei layout.
        lista_vuota_error = layout.itemAt(0).widget()  # type:QLabel # type:ignore
        lista_vuota_error.show()

    # - Metodo da fare modullare(?)
    def aggiorna_pagina(self) -> None:
        """Permette di aggiornare la pagina e visualizzare modifiche previamente non mostrate."""
        self.svuota_layout(self.layout_lista_regie)
        self.layout_lista_regie.addWidget(self.label_lista_regie_vuota)
        self.label_lista_regie_vuota.hide()
        self.displayRegieRequest.emit(self.layout_lista_regie)

    def svuota_layout(self, layout: Optional[QLayout]) -> None:
        """Svuota un layout, eliminando i riferimenti ai widget contenuti. In caso
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
                    self.svuota_layout(child_layout)
