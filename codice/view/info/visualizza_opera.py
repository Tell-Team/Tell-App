from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
)
from PyQt6.QtCore import Qt


class OperaView(QWidget):
    def __init__(self):
        super().__init__()

        self._build_ui()

    def _build_ui(self):
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

        self.lista_vuota_error = QLabel("")
        self.lista_vuota_error.setObjectName("SubHeader")

        self.regie = QWidget()
        self.layout_regie = QVBoxLayout(self.regie)
        self.layout_regie.addWidget(self.label_lista_regie)
        self.layout_regie.addStretch()

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

        #
        #
        #

        # Pulsante: Torna dietro
        self.btn_torna_dietro = QPushButton("Indietro")
        self.btn_torna_dietro.setObjectName("SmallButton")

        self.pulsanti = QWidget()
        layout_pulsanti = QHBoxLayout(self.pulsanti)
        layout_pulsanti.addWidget(self.btn_torna_dietro)
        layout_pulsanti.addStretch()

        #
        #
        #

        # Funzione di scroll
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        scroll_layout.addWidget(content)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)

        #
        #
        #

        # Layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.pulsanti)
        main_layout.addWidget(scroll_area)
