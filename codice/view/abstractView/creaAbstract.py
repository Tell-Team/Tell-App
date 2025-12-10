from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QFormLayout,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt


class CreaAbstractView(QWidget):
    """
    Classe pseudo-astratta che facilita la creazione delle pagine di crea e modifica dell'app.
    """

    def __init__(self):
        super().__init__()

        # Header Setup
        self.header = QLabel("")
        self.header.setObjectName("Header1")
        self.header.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # QFormLayout Setup
        self.form_content = QWidget()
        self.form_layout = QFormLayout(self.form_content)
        self.form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        # Pulsanti Setup
        self.btn_cancella = QPushButton("Cancella")
        self.btn_cancella.setObjectName("SmallButton")

        self.btn_conferma = QPushButton("Conferma")
        self.btn_conferma.setObjectName("SmallButton")

        self.pulsanti = QWidget()
        layout_pulsanti = QHBoxLayout(self.pulsanti)
        layout_pulsanti.addWidget(self.btn_cancella)
        layout_pulsanti.addWidget(self.btn_conferma)
        layout_pulsanti.addStretch()

        # Label input_error
        self.input_error = QLabel("")
        self.input_error.setObjectName("SubHeader")
        self.input_error.setStyleSheet(
            self.input_error.styleSheet() + "#SubHeader { color:red; }"
        )

        # Main layout Setup
        self.main_layout = QVBoxLayout(self)

    def _setup_form(self): ...

    def _clear_form_layout(self, form_layout: QFormLayout):
        """
        Rimuove tutte le righe di un `QFormLayout` senza eliminare i widget. Serve per
        ricaricare un form.
        """
        # - Non è stato ancora implementato, ma potrebbe essere utile.

        while form_layout.rowCount() > 0:
            form_layout.removeRow(0)

    def add_row(self, label_text: QLabel, widget: QWidget):
        """
        Metodo per tener il codice pulito ed aggiungere una riga al `QFormLayout`
        della pagina per cui viene chiamato.
        """
        self.form_layout.addRow(label_text, widget)
