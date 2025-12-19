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

    def __init__(self) -> None:
        super().__init__()

        # Setup Header
        self.header = QLabel("")
        self.header.setObjectName("Header1")
        self.header.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Setup QFormLayout
        self.form_content = QWidget()
        self.form_layout = QFormLayout(self.form_content)
        self.form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        # Setup Pulsanti
        self._btn_cancella = QPushButton("Cancella")
        self._btn_cancella.setObjectName("SmallButton")

        self._btn_conferma = QPushButton("Conferma")
        self._btn_conferma.setObjectName("SmallButton")

        self.pulsanti = QWidget()
        layout_pulsanti = QHBoxLayout(self.pulsanti)
        layout_pulsanti.addWidget(self._btn_cancella)
        layout_pulsanti.addWidget(self._btn_conferma)
        layout_pulsanti.addStretch()

        # Label input_error
        self.input_error = QLabel("")
        self.input_error.setObjectName("SubHeader")
        self.input_error.setStyleSheet(
            self.input_error.styleSheet() + "#SubHeader { color:red; }"
        )

        # Setup main layout
        self.main_layout = QVBoxLayout(self)

    def _setup_form(self) -> None:
        """Metodo privato utilizzato per costruire e disporre i widget della form."""
        ...

    def _clear_form_layout(self, form_layout: QFormLayout) -> None:
        """
        Rimuove tutte le righe di un `QFormLayout` senza eliminare i widget. Serve per
        ricaricare un form.
        """
        # - Non è stato ancora implementato, ma potrebbe essere utile per future pagine.
        while form_layout.rowCount() > 0:
            form_layout.removeRow(0)
