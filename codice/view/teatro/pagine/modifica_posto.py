from PyQt6.QtWidgets import QLabel, QLineEdit, QSpinBox
from typing import override

from core.view import AbstractCreaView

from view.teatro.utils import PostoData

from view.style.ui_style import WidgetRole, WidgetColor


class ModificaPostoView(AbstractCreaView):
    """Pagina per la modifica dei posti di una sezione."""

    def __init__(self):
        super().__init__()

        self.id_current_posto: int = -1

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        # Header
        self._header.setText("Modifica posto")

        # Layout
        self._main_layout.addWidget(self._header)
        self._main_layout.addWidget(self._scroll_area)
        self._main_layout.addWidget(self._input_error)
        self._main_layout.addWidget(self._pulsanti)

    @override
    def _setup_form(self) -> None:
        label_fila = QLabel('Fila<span style="color:red;">*</span> :')
        label_fila.setProperty(WidgetRole.BODY_TEXT, True)
        label_fila.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
        self.fila = QLineEdit()
        self.fila.setPlaceholderText("Inserire nome")

        label_numero = QLabel('Numero<span style="color:red;">*</span> :')
        label_numero.setProperty(WidgetRole.BODY_TEXT, True)
        label_numero.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
        self.numero = QSpinBox()
        self.numero.setMinimum(0)

        self._form_layout.addRow(label_fila, self.fila)
        self._form_layout.addRow(label_numero, self.numero)

    @override
    def _connect_signals(self) -> None:
        super()._connect_signals()

        # La QLineEdit per la fila solo mostra maiuscole
        def to_upper(text: str) -> None:
            self.fila.blockSignals(True)
            self.fila.setText(text.upper())
            self.fila.blockSignals(False)

        self.fila.textChanged.connect(  # type:ignore
            to_upper
        )

    # ------------------------- METODI DI VIEW -------------------------

    def set_data(self, data: PostoData) -> None:
        self.id_current_posto = data.id

        self.fila.setText(data.fila)
        self.numero.setValue(data.numero)

    @override
    def reset_pagina(self) -> None:
        super().reset_pagina()

        self.id_spettacolo = -1
        self.fila.setText("")
        self.numero.setValue(0)
