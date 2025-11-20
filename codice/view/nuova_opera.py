from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QFormLayout,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QDateEdit,
    QSpinBox,
    QPushButton,
)

from view.navigation import NavigationController

from PyQt6.QtCore import Qt


class FormularioOpera(QWidget):
    def __init__(self, nav: NavigationController):
        super().__init__()

        header = QLabel("Nuova opera")
        header.setObjectName("Header2")
        header.setAlignment(Qt.AlignmentFlag.AlignLeft)

        label_nome = QLabel("Nome:")
        input_nome = QLineEdit()

        label_trama = QLabel("Trama:")
        input_trama = QTextEdit()
        input_trama.setFixedHeight(80)

        label_genere = QLabel("Genere:")
        input_genere = QComboBox()

        label_compositore = QLabel("Compositore:")
        input_compositore = QLineEdit()

        label_librettista = QLabel("Librettista:")
        input_librettista = QLineEdit()

        label_data = QLabel("Prima rappresentazione:")
        input_data = QDateEdit()

        label_atti = QLabel("Numeri di atti:")
        input_atti = QSpinBox()
        input_atti.setRange(0, 10)
        input_atti.setValue(0)

        label_teatro = QLabel("Teatro prima rappresentazione:")
        input_teatro = QLineEdit()

        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)

        form_layout.addRow(label_nome, input_nome)
        form_layout.addRow(label_trama, input_trama)
        form_layout.addRow(label_genere, input_genere)
        form_layout.addRow(label_compositore, input_compositore)
        form_layout.addRow(label_librettista, input_librettista)
        form_layout.addRow(label_data, input_data)
        form_layout.addRow(label_atti, input_atti)
        form_layout.addRow(label_teatro, input_teatro)

        widget_pulsanti = QWidget()
        layout_pulsanti = QHBoxLayout(widget_pulsanti)

        btn_cancella = QPushButton("Cancella")
        btn_cancella.setObjectName("SmallButton")
        btn_cancella.clicked.connect(nav.go_back)  # type:ignore

        btn_conferma = QPushButton("Conferma")
        btn_conferma.setObjectName("SmallButton")

        layout_pulsanti.addWidget(btn_cancella)
        layout_pulsanti.addWidget(btn_conferma)
        layout_pulsanti.addStretch()

        main_layout = QVBoxLayout()
        main_layout.addWidget(header)
        main_layout.addWidget(form_widget)
        main_layout.addWidget(widget_pulsanti)
        main_layout.addStretch()

        self.setLayout(main_layout)
