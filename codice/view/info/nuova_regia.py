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

from controller.info_controller import InfoController


class FormNuovaRegia(QWidget):
    def __init__(self, info_controller: InfoController):
        super().__init__()

        self.info_controller = info_controller

        self.cur_id_opera: int = -1

        self._build_ui()

    def _build_ui(self):
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
            self.info_controller.cancella_regia
        )

        self.btn_conferma = QPushButton("Conferma")
        self.btn_conferma.setObjectName("SmallButton")
        self.btn_conferma.clicked.connect(  # type:ignore
            lambda: print(
                "partial(self.info_controller.salva_regia, self.cur_id_opera)"
            )  # - partial(self.info_controller.salva_regia, self.cur_id_opera)
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
