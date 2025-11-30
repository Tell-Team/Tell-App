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
from PyQt6.QtCore import Qt
from functools import partial

from controller.info_controller import InfoController


class FormNuovaOpera(QWidget):
    """
    Interfaccia utente di creazione di `Opera`. Contiene campi di input per inserire tutti gli
    attributo respettivi. Comunque non permette di crea istanze di `Regia` ammeno che non venga
    prima creata un'opera e questa venga modificata.
    """

    def __init__(self, info_controller: InfoController):
        super().__init__()

        self.info_controller = info_controller

        self._build_ui()

    def _build_ui(self):
        # - Lo style non è ancora applicato

        # # Header
        self.header = QLabel("Nuova opera")
        self.header.setObjectName("Header1")
        self.header.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # # Input rows
        label_nome = QLabel('Nome<span style="color:red">*</span> :')
        label_nome.setObjectName("SubHeader")
        self.input_nome = QLineEdit()

        label_trama = QLabel("Trama :")
        label_trama.setObjectName("SubHeader")
        self.input_trama = QTextEdit()
        self.input_trama.setFixedHeight(80)

        label_genere = QLabel('Genere<span style="color:red">*</span> :')
        label_genere.setObjectName("SubHeader")
        self.input_genere = QComboBox()
        self.input_genere.insertItem(0, "")
        for g in self.info_controller.get_generi():
            nome = g.get_nome()
            self.input_genere.addItem(nome)
        self.input_genere.setCurrentIndex(0)

        label_compositore = QLabel('Compositore<span style="color:red">*</span> :')
        label_compositore.setObjectName("SubHeader")
        self.input_compositore = QLineEdit()

        label_librettista = QLabel('Librettista<span style="color:red">*</span> :')
        label_librettista.setObjectName("SubHeader")
        self.input_librettista = QLineEdit()

        label_atti = QLabel('Numeri di atti<span style="color:red">*</span> :')
        label_atti.setObjectName("SubHeader")
        self.input_atti = QSpinBox()
        self.input_atti.setRange(0, 10)
        self.input_atti.setValue(0)

        label_data = QLabel("Prima rappresentazione :")
        label_data.setObjectName("SubHeader")
        self.input_data = QDateEdit()

        label_teatro = QLabel("Teatro prima rappresentazione :")
        label_teatro.setObjectName("SubHeader")
        self.input_teatro = QLineEdit()

        form_content = QWidget()
        self.form_layout = QFormLayout(form_content)
        self.form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        self.form_layout.addRow(label_nome, self.input_nome)
        self.form_layout.addRow(label_trama, self.input_trama)
        self.form_layout.addRow(label_genere, self.input_genere)
        self.form_layout.addRow(label_compositore, self.input_compositore)
        self.form_layout.addRow(label_librettista, self.input_librettista)
        self.form_layout.addRow(label_atti, self.input_atti)
        self.form_layout.addRow(label_data, self.input_data)
        self.form_layout.addRow(label_teatro, self.input_teatro)

        # # Lista regie
        self.label_lista_regie = QLabel("Lista regie")
        self.label_lista_regie.setObjectName("Header2")
        self.label_lista_regie.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.nota_regie = QLabel(
            "**Nota:** Le singole repliche (Regie) possono essere aggiunte solo dopo aver salvato l'opera."
        )
        self.nota_regie.setObjectName("SubHeader")
        self.nota_regie.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.nota_regie.setWordWrap(True)

        # # Pulsanti
        self.btn_cancella = QPushButton("Cancella")
        self.btn_cancella.setObjectName("SmallButton")
        self.btn_cancella.clicked.connect(  # type:ignore
            partial(self.info_controller.cancella_opera, is_new=True)
        )

        self.btn_conferma = QPushButton("Conferma")
        self.btn_conferma.setObjectName("SmallButton")
        self.btn_conferma.clicked.connect(  # type:ignore
            lambda: print(
                "self.info_controller.salva_opera"
            )  # - self.info_controller.salva_opera
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
        self.main_layout.addWidget(self.label_lista_regie)
        self.main_layout.addWidget(self.nota_regie)
        self.main_layout.addWidget(self.pulsanti)
        self.main_layout.addStretch()
