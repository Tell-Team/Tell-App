from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QTextEdit,
    QSizePolicy,
)

from view.abstractView.creaAbstract import CreaAbstractView


class NuovoGenereView(CreaAbstractView):
    """
    GUI di creazione di `Genere`.

    Contiene campi di input per inserire tutti gli attributi respettivi.
    """

    def __init__(self):
        super().__init__()

        self._build_ui()

    def _build_ui(self):
        # Header
        self.header.setText("Nuovo genere")

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

        label_descrizione = QLabel("Descrizione :")
        label_descrizione.setObjectName("SubHeader")
        self.descrizione = QTextEdit()
        self.descrizione.setPlaceholderText("Inserire descrizione")
        self.descrizione.setFixedHeight(80)
        self.descrizione.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )

        self.add_row(label_nome, self.nome)
        self.add_row(label_descrizione, self.descrizione)
