from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QTextEdit,
    QSizePolicy,
)

from view.abstractView.creaAbstract import CreaAbstractView


class NuovoGenereView(CreaAbstractView):
    """
    View per la creazione di un nuovo genere.
    """

    def __init__(self) -> None:
        super().__init__()

        self._setup_ui()

    def _setup_ui(self) -> None:
        # Header
        self.header.setText("Aggiungi Nuovo genere")

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

        label_descrizione = QLabel("Descrizione :")
        label_descrizione.setObjectName("SubHeader")
        self.descrizione = QTextEdit()
        self.descrizione.setPlaceholderText("Inserire descrizione")
        self.descrizione.setFixedHeight(80)
        self.descrizione.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )

        self.form_layout.addRow(label_nome, self.nome)
        self.form_layout.addRow(label_descrizione, self.descrizione)
