from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QFormLayout,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QSizePolicy,
)
from PyQt6.QtCore import Qt


class CreaAbstractView(QWidget):
    """Classe pseudo-astratta che facilita la creazione delle pagine di crea
    e modifica dell'app."""

    def __init__(self) -> None:
        super().__init__()

        # Setup Header
        self.header = QLabel("")
        self.header.setObjectName("Header1")
        self.header.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Setup QFormLayout
        self.form_content = QWidget()
        self.form_content.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding
        )
        self.form_layout = QFormLayout(self.form_content)
        self.form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        # Funzione di scroll
        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setWidget(self.form_content)
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding
        )

        # Setup Pulsanti
        self._btn_annulla = QPushButton("Annulla")
        self._btn_annulla.setObjectName("WhiteButton")

        self._btn_conferma = QPushButton("Crea")
        self._btn_conferma.setObjectName("WhiteButton")

        self.pulsanti = QWidget()
        layout_pulsanti = QHBoxLayout(self.pulsanti)
        layout_pulsanti.addWidget(self._btn_annulla)
        layout_pulsanti.addWidget(self._btn_conferma)
        layout_pulsanti.addStretch()

        # Label input_error
        self.input_error = QLabel("")
        self.input_error.setObjectName("SubHeader")
        self.input_error.setStyleSheet(
            self.input_error.styleSheet() + "#SubHeader { color:#c3423f; }"
        )

        # Setup main layout
        self.main_layout = QVBoxLayout(self)

    # ------------------------- METODI DI VIEW -------------------------

    def reset_pagina(self) -> None:
        """Reset della pagina allo stato default."""
        ...

    def show_input_error(self, message: str) -> None:
        """Aggiorna il testo del label input_error.

        :param message: testo inserito nel label"""
        self.input_error.setText(message)
        self.input_error.show()  # Si assicura che il label sia visualizzato.

    def _setup_form(self) -> None:
        """Metodo protetto utilizzato per costruire e disporre i widget della form."""
        ...

    def _svuota_form_layout(self, form_layout: QFormLayout) -> None:
        """Rimuove tutte le righe di un `QFormLayout` senza eliminare i widget. Serve per
        ricaricare un form."""
        # - Non è stato ancora implementato, ma potrebbe essere utile per future pagine.
        while form_layout.rowCount() > 0:
            form_layout.removeRow(0)
