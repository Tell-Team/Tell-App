from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QDateEdit,
    QSpinBox,
    # QHBoxLayout,
)

from view.abstractView.creaAbstract import CreaAbstractView

from model.pianificazione.genere import Genere


class NuovaOperaView(CreaAbstractView):
    """
    View per la creazione di una nuova opera.
    """

    def __init__(self) -> None:
        super().__init__()

        self._setup_ui()

    def _setup_ui(self) -> None:
        # Header
        self.header.setText("Aggiungi Nuova opera")

        # Form
        self._setup_form()

        # Layout
        self.main_layout.addWidget(self.header)
        self.main_layout.addWidget(self.form_content)
        self.main_layout.addWidget(self.input_error)
        self.main_layout.addWidget(self.pulsanti)
        self.main_layout.addStretch()

    def _setup_form(self) -> None:
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
        self.data.setCalendarPopup(True)
        self.data.setDisplayFormat("dd/MM/yyyy")

        # atti_data_layout = QHBoxLayout()
        # atti_data_layout.addWidget(label_atti)
        # atti_data_layout.addWidget(self.atti)
        # atti_data_layout.addWidget(label_data)
        # atti_data_layout.addWidget(self.data)

        label_teatro = QLabel("Teatro prima rappresentazione :")
        label_teatro.setObjectName("SubHeader")
        self.teatro = QLineEdit()
        self.teatro.setPlaceholderText("Inserire nome del teatro")

        self.form_layout.addRow(label_nome, self.nome)
        self.form_layout.addRow(label_trama, self.trama)
        self.form_layout.addRow(label_genere, self.genere)
        self.form_layout.addRow(label_compositore, self.compositore)
        self.form_layout.addRow(label_librettista, self.librettista)
        self.form_layout.addRow(label_atti, self.atti)
        self.form_layout.addRow(label_data, self.data)
        # self.form_layout.addRow(atti_data_layout)
        self.form_layout.addRow(label_teatro, self.teatro)

    # - Ci dovrebbe essere nel controller o vabbene nella view?
    def setup_genere_combobox(self, generi: list[Genere]) -> None:
        """Riempisce il `QComboBox` dei generi."""
        self.genere.clear()

        self.genere.insertItem(0, "Scegliere genere...", -1)
        # - Come faccio per avere l'opzione 0 di colore grigio?
        for i, g in enumerate(generi):
            i += 1
            self.genere.insertItem(i, g.get_nome(), g.get_id())
