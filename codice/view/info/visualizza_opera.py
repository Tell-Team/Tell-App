from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
)
from PyQt6.QtCore import Qt

from model.model import Model
from controller.navigation import NavigationController

from datetime import date


class VisualizzaOpera(QWidget):
    def __init__(self, model: Model, nav: NavigationController):
        super().__init__()

        # # Labels
        self.nome: str = ""
        label_nome = QLabel(f"{self.nome}")
        label_nome.setObjectName("Header1")
        label_nome.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.librettista: str = ""
        label_librettista = QLabel(f"Libretto di {self.librettista}")
        label_librettista.setWordWrap(True)
        label_librettista.setObjectName("Paragraph")

        self.compositore: str = ""
        label_compositore = QLabel(f"Musica composta da {self.compositore}.")
        label_compositore.setWordWrap(True)
        label_compositore.setObjectName("Paragraph")

        self.genere: str = ""
        label_genere = QLabel(f"Genere: {self.genere}")
        label_genere.setObjectName("Paragraph")

        self.atti: int = 0
        label_atti = QLabel(f"Numero di atti: {self.atti}")
        label_atti.setObjectName("Paragraph")

        self.data: date = date(1999, 1, 1)
        self.teatro: str = ""
        label_prima_rappresentazione = QLabel(
            f"È stata rappresentata per prima volta il {self.data.strftime("%d/%m/%Y")} nel teatro {self.teatro}"
        )
        label_prima_rappresentazione.setWordWrap(True)
        label_prima_rappresentazione.setObjectName("Paragraph")

        self.trama: str = ""
        label_trama = QLabel(f"{self.trama}")
        label_trama.setWordWrap(True)
        label_trama.setObjectName("Paragraph")

        content = QWidget()
        layout_content = QVBoxLayout(content)

        layout_content.addWidget(label_nome)
        layout_content.addWidget(label_librettista)
        layout_content.addWidget(label_compositore)
        layout_content.addWidget(label_genere)
        layout_content.addWidget(label_atti)
        layout_content.addWidget(label_prima_rappresentazione)
        layout_content.addWidget(label_trama)
        layout_content.addStretch()

        #
        #
        #

        # # Pulsante: Torna dietro
        btn_torna_dietro = QPushButton("Torna dietro")
        btn_torna_dietro.setObjectName("SmallButton")
        btn_torna_dietro.clicked.connect(  # type:ignore
            info_controller.get_nav().go_back
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
