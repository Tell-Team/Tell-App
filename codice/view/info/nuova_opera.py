from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QDateEdit,
    QSpinBox,
)
from PyQt6.QtCore import pyqtSignal

from view.abstractView.creaAbstract import CreaAbstractView


class NuovaOperaView(CreaAbstractView):
    """
    GUI di creazione di `Opera`.

    Contiene campi di input per inserire tutti gli attributi respettivi.
    """

    request_lista_generi_nomi = pyqtSignal()

    def __init__(self):
        super().__init__()

        self._build_ui()

    def _build_ui(self):
        # Header
        self.header.setText("Nuova opera")

        # Form
        self._setup_form()

        # Layout
        self.main_layout.addWidget(self.header)
        self.main_layout.addWidget(self.form_content)
        self.main_layout.addWidget(self.input_error)
        self.main_layout.addWidget(self.pulsanti)
        self.main_layout.addStretch()

    def _setup_form(self):
        label_nome = QLabel("Nome :")
        label_nome.setObjectName("SubHeader")
        self.nome = QLineEdit()
        self.nome.setPlaceholderText("Inserire nome")

        label_trama = QLabel("Trama :")
        label_trama.setObjectName("SubHeader")
        self.trama = QTextEdit()
        self.trama.setPlaceholderText("Inserire trama")
        self.trama.setFixedHeight(80)

        label_genere = QLabel("Genere :")
        label_genere.setObjectName("SubHeader")
        self.genere = QComboBox()

        self.request_lista_generi_nomi.emit()

        label_compositore = QLabel("Compositore :")
        label_compositore.setObjectName("SubHeader")
        self.compositore = QLineEdit()
        self.compositore.setPlaceholderText("Inserire compositore")

        label_librettista = QLabel("Librettista :")
        label_librettista.setObjectName("SubHeader")
        self.librettista = QLineEdit()
        self.librettista.setPlaceholderText("Inserire librettista")

        label_atti = QLabel("Numeri di atti :")
        label_atti.setObjectName("SubHeader")
        self.atti = QSpinBox()
        self.atti.setRange(0, 10)
        self.atti.setValue(0)

        label_data = QLabel("Prima rappresentazione :")
        label_data.setObjectName("SubHeader")
        self.data = QDateEdit()

        label_teatro = QLabel("Teatro prima rappresentazione :")
        label_teatro.setObjectName("SubHeader")
        self.teatro = QLineEdit()
        self.teatro.setPlaceholderText("Inserire nome del teatro")

        self.add_row(label_nome, self.nome)
        self.add_row(label_trama, self.trama)
        self.add_row(label_genere, self.genere)
        self.add_row(label_compositore, self.compositore)
        self.add_row(label_librettista, self.librettista)
        self.add_row(label_atti, self.atti)
        self.add_row(label_data, self.data)
        self.add_row(label_teatro, self.teatro)

    def set_genere_combobox(self, names: list[str]):
        """Metodo chiamato dall'`InfoController` per riempire il `QComboBox` dei generi."""
        self.genere.clear()

        self.genere.insertItem(0, "Scegliere genere...")
        # - self.genere.setItemData(0, Qt.GlobalColor.gray, Qt.ItemDataRole.BackgroundRole)
        # - Come faccio per avere la opzione 0 di colore grigio
        for i, n in enumerate(names):
            i += 1
            self.genere.insertItem(i, n)
