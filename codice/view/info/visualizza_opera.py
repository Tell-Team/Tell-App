from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
)
from PyQt6.QtCore import Qt

from controller.info_controller import InfoController


class VisualizzaOpera(QWidget):
    def __init__(self, info_controller: InfoController):
        super().__init__()

        self.info_controller = info_controller

        self._build_ui()

    def _build_ui(self):
        # # Labels
        self.label_nome = QLabel("-NOME-")
        self.label_nome.setObjectName("Header1")
        self.label_nome.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.label_librettista = QLabel("Libretto di -LIBRETTISTA-")
        self.label_librettista.setWordWrap(True)
        self.label_librettista.setObjectName("Paragraph")

        self.label_compositore = QLabel("Musica composta da -COMPOSITORE-.")
        self.label_compositore.setWordWrap(True)
        self.label_compositore.setObjectName("Paragraph")

        self.label_genere = QLabel(f"Genere: -GENERE-")
        self.label_genere.setObjectName("Paragraph")

        self.label_atti = QLabel(f"Numero di atti: -ATTI-")
        self.label_atti.setObjectName("Paragraph")

        self.label_prima_rappresentazione = QLabel(
            f"È stata rappresentata per prima volta il -DATA- nel teatro -TEATRO-"
        )
        self.label_prima_rappresentazione.setWordWrap(True)
        self.label_prima_rappresentazione.setObjectName("Paragraph")

        self.label_trama = QLabel("-TRAMA-")
        self.label_trama.setWordWrap(True)
        self.label_trama.setObjectName("Paragraph")

        content = QWidget()
        layout_content = QVBoxLayout(content)

        layout_content.addWidget(self.label_nome)
        layout_content.addWidget(self.label_librettista)
        layout_content.addWidget(self.label_compositore)
        layout_content.addWidget(self.label_genere)
        layout_content.addWidget(self.label_atti)
        layout_content.addWidget(self.label_prima_rappresentazione)
        layout_content.addWidget(self.label_trama)
        layout_content.addStretch()

        #
        #
        #

        # # Pulsante: Torna dietro
        btn_torna_dietro = QPushButton("Torna dietro")
        btn_torna_dietro.setObjectName("SmallButton")
        btn_torna_dietro.clicked.connect(  # type:ignore
            self.info_controller.get_nav().go_back
        )

        #
        #
        #

        # # FUNZIONE DI SCROLL
        # ## Scroll Layout
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        scroll_layout.addWidget(content)

        # ## Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)

        pulsanti = QWidget()
        layout_pulsanti = QHBoxLayout(pulsanti)

        layout_pulsanti.addWidget(btn_torna_dietro)
        layout_pulsanti.addStretch()

        #
        #
        #

        # # MAIN LAYOUT
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(pulsanti)
        main_layout.addWidget(scroll_area)
