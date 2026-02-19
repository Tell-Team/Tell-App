from PyQt6.QtWidgets import QLabel, QLineEdit, QComboBox
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from typing import override

from core.view import AbstractCreaView

from model.pianificazione.spettacolo import Spettacolo
from model.organizzazione.sezione import Sezione


class NuovoPrezzoPage(AbstractCreaView):
    """Pagina per la creazione di un nuovo prezzo."""

    def __init__(self) -> None:
        super().__init__()

        self.id_spettacolo = -1
        self.id_sezione = -1

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        # Header
        self._header.setText("Aggiungi nuovo prezzo")

        # Layout
        self._main_layout.addWidget(self._header)
        self._main_layout.addWidget(self._scroll_area)
        self._main_layout.addWidget(self._input_error)
        self._main_layout.addWidget(self._pulsanti)

    @override
    def _setup_form(self) -> None:
        label_spettacolo = QLabel('Spettacolo<span style="color:red;">*</span> :')
        self.spettacolo = QComboBox()
        self.spettacolo.setEnabled(False)

        label_sezione = QLabel('Sezione<span style="color:red;">*</span> :')
        self.sezione = QComboBox()
        self.sezione.setEnabled(False)

        label_prezzo = QLabel('Ammontare<span style="color:red;">*</span> :')
        self.prezzo = QLineEdit()
        self.prezzo.setPlaceholderText("Inserire prezzo in €, e.g. 30.00, 19.99")
        validator_prezzo = QRegularExpressionValidator(
            QRegularExpression(r"^\d+(\.\d{2})?$")
        )
        self.prezzo.setValidator(validator_prezzo)

        self._form_layout.addRow(label_spettacolo, self.spettacolo)
        self._form_layout.addRow(label_sezione, self.sezione)
        self._form_layout.addRow(label_prezzo, self.prezzo)

    # ------------------------- METODI DI VIEW -------------------------

    @override
    def reset_pagina(self) -> None:
        super().reset_pagina()

        self.id_spettacolo = -1
        self.id_sezione = -1
        self.prezzo.setText("")

    def set_data(self, spettacolo: Spettacolo, sezione: Sezione) -> None:
        self.spettacolo.insertItem(0, spettacolo.get_titolo())
        self.sezione.insertItem(0, sezione.get_nome())

        self.id_spettacolo = spettacolo.get_id()
        self.id_sezione = sezione.get_id()
