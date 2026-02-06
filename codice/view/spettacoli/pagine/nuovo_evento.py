from PyQt6.QtWidgets import QLabel, QDateEdit, QTimeEdit
from PyQt6.QtCore import QDate, QTime
from typing import override

from core.view import AbstractCreaView

from view.style.ui_style import WidgetRole, WidgetColor


class NuovoEventoView(AbstractCreaView):
    """Pagina per la creazione di un nuovo evento."""

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        self.id_spettacolo = -1

        # Header
        self._header.setText("Aggiungi nuovo evento")

        # Layout
        self._main_layout.addWidget(self._header)
        self._main_layout.addWidget(self._scroll_area)
        self._main_layout.addWidget(self._input_error)
        self._main_layout.addWidget(self._pulsanti)

    @override
    def _setup_form(self) -> None:
        label_data = QLabel('Data<span style="color:red;">*</span> :')
        label_data.setProperty(WidgetRole.BODY_TEXT, True)
        label_data.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
        self.data = QDateEdit()
        self.data.setDisplayFormat("dd/MM/yyyy")
        self.data.setDate(QDate.currentDate())
        self.data.setMinimumDate(QDate.currentDate())

        label_ora = QLabel('Ora<span style="color:red;">*</span> :')
        label_ora.setProperty(WidgetRole.BODY_TEXT, True)
        label_ora.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
        self.ora = QTimeEdit()
        self.ora.setTime(QTime.currentTime())

        self._form_layout.addRow(label_data, self.data)
        self._form_layout.addRow(label_ora, self.ora)

    # ------------------------- METODI DI VIEW -------------------------

    @override
    def reset_pagina(self) -> None:
        super().reset_pagina()

        self.id_spettacolo = -1
        self.data.setDate(QDate.currentDate())
        self.ora.setTime(QTime.currentTime())
