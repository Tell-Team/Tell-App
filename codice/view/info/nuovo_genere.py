from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QFormLayout,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QSizePolicy,
)
from PyQt6.QtCore import Qt

from controller.info_controller import InfoController


class FormNuovoGenere(QWidget):
    def __init__(self, info_controller: InfoController):
        super().__init__()

        self.info_controller = info_controller

        self._build_ui()

    def _build_ui(self):
        # - Lo style non è ancora applicato

        # # Header
        self.header = QLabel("Nuovo genere")
        self.header.setObjectName("Header1")
        self.header.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # # Input rows
        label_nome = QLabel('Nome<span style="color:red">*</span> :')
        label_nome.setObjectName("SubHeader")
        self.input_nome = QLineEdit()

        label_descrizione = QLabel('Descrizione<span style="color:red">*</span> :')
        label_descrizione.setObjectName("SubHeader")
        self.input_descrizione = QTextEdit()
        self.input_descrizione.setFixedHeight(80)
        self.input_descrizione.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )

        form_content = QWidget()
        form_layout = QFormLayout(form_content)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.addRow(label_nome, self.input_nome)
        form_layout.addRow(label_descrizione, self.input_descrizione)

        # # Pulsanti
        self.btn_cancella = QPushButton("Cancella")
        self.btn_cancella.setObjectName("SmallButton")
        self.btn_cancella.clicked.connect(  # type:ignore
            self.info_controller.cancella_genere
        )

        self.btn_conferma = QPushButton("Conferma")
        self.btn_conferma.setObjectName("SmallButton")
        self.btn_conferma.clicked.connect(  # type:ignore
            lambda: print(
                "self.info_controller.salva_genere"
            )  # - self.info_controller.salva_genere
        )

        self.pulsanti = QWidget()
        layout_pulsanti = QHBoxLayout(self.pulsanti)
        layout_pulsanti.addWidget(self.btn_cancella)
        layout_pulsanti.addWidget(self.btn_conferma)
        layout_pulsanti.addStretch()

        # # Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.header)
        self.main_layout.addWidget(form_content)
        self.main_layout.addWidget(self.pulsanti)
        self.main_layout.addStretch()
