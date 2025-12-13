from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QSpinBox,
)

from view.abstractView.creaAbstract import CreaAbstractView


# - ESTO VA EN LA CARPETA spettacoli, Y DEBERÍA SER UN NuovoSpettacolo CON UNA OPCIÓN
#   DE Regia PARA AJUSTAR EL QFormLayout, PERO ES UN BUEN INICIO
class NuovaRegiaView(CreaAbstractView):
    def __init__(self):
        super().__init__()

        self.cur_id_opera: int = -1

        self._build_ui()

    def _build_ui(self):
        # - Lo style non è ancora applicato

        # Header
        self.header.setText("Nuova regia")

        # Form
        self._setup_form()

        # Layout
        self.main_layout.addWidget(self.header)
        self.main_layout.addWidget(self.form_content)
        self.main_layout.addWidget(self.pulsanti)
        self.main_layout.addStretch()

    def _setup_form(self):
        label_regista = QLabel("Regista :")
        label_regista.setObjectName("SubHeader")
        self.regista = QLineEdit()

        label_anno = QLabel("Anno di produzione :")
        label_anno.setObjectName("SubHeader")
        self.anno = QSpinBox()
        self.anno.setRange(0, 2099)
        self.anno.setValue(0)

        self.add_row(label_regista, self.regista)
        self.add_row(label_anno, self.anno)
