from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QFormLayout,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QSpinBox,
    QPushButton,
)
from PyQt6.QtCore import Qt

from model.model import Model
from controller.navigation import NavigationController


class FormularioNuovaRegia(QWidget):
    def __init__(self, model: Model, nav: NavigationController):
        super().__init__()

        # - Non ho messo un riferimento al info_controller
        # - Lo style non è ancora applicato

        # # Header
        self.header = QLabel("Nuova regia")
        self.header.setObjectName("Header1")
        self.header.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # # Input rows
        label_regista = QLabel('Regista<span style="color:red">*</span> :')
        label_regista.setObjectName("SubHeader")
        self.input_regista = QLineEdit()

        label_anno = QLabel('Anno di produzione<span style="color:red">*</span> :')
        label_anno.setObjectName("SubHeader")
        self.input_anno = QSpinBox()
        self.input_anno.setRange(0, 2099)
        self.input_anno.setValue(0)

        form_content = QWidget()
        form_layout = QFormLayout(form_content)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.addRow(label_regista, self.input_regista)
        form_layout.addRow(label_anno, self.input_anno)

        # # Pulsanti
        self.btn_cancella = QPushButton("Cancella")
        self.btn_cancella.setObjectName("SmallButton")
        self.btn_cancella.clicked.connect(  # type:ignore
            nav.go_back  # - info_controller.cancella_creazione_regia
        )

        self.btn_conferma = QPushButton("Conferma")
        self.btn_conferma.setObjectName("SmallButton")
        self.btn_conferma.clicked.connect(  # type:ignore
            nav.go_back  # - DA CORRIGERE: Un trigger per verificare dati e salvare regia
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
