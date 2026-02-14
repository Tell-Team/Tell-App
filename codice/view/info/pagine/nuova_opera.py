from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QDateEdit,
    QSpinBox,
    # QHBoxLayout,
)
from PyQt6.QtCore import QDate
from typing import override

from core.view import AbstractCreaView

from model.pianificazione.genere import Genere

from view.style.ui_style import WidgetRole, WidgetColor


class NuovaOperaView(AbstractCreaView):
    """Pagina per la creazione di una nuova opera."""

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        # Header
        self._header.setText("Aggiungi nuova opera")

        # Layout
        self._main_layout.addWidget(self._header)
        self._main_layout.addWidget(self._scroll_area)
        self._main_layout.addWidget(self._input_error)
        self._main_layout.addWidget(self._pulsanti)

    @override
    def _setup_form(self) -> None:
        label_nome = QLabel('Nome<span style="color:red;">*</span> :')
        label_nome.setProperty(WidgetRole.BODY_TEXT, True)
        label_nome.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
        self.nome = QLineEdit()
        self.nome.setPlaceholderText("Inserire nome")

        label_trama = QLabel('Trama<span style="color:red;">*</span> :')
        label_trama.setProperty(WidgetRole.BODY_TEXT, True)
        label_trama.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
        self.trama = QTextEdit()
        self.trama.setPlaceholderText("Inserire trama")
        self.trama.setFixedHeight(80)

        label_genere = QLabel('Genere<span style="color:red;">*</span> :')
        label_genere.setProperty(WidgetRole.BODY_TEXT, True)
        label_genere.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
        self.genere = QComboBox()

        label_compositore = QLabel('Compositore<span style="color:red;">*</span> :')
        label_compositore.setProperty(WidgetRole.BODY_TEXT, True)
        label_compositore.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
        self.compositore = QLineEdit()
        self.compositore.setPlaceholderText("Inserire compositore")

        label_librettista = QLabel('Librettista<span style="color:red;">*</span> :')
        label_librettista.setProperty(WidgetRole.BODY_TEXT, True)
        label_librettista.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
        self.librettista = QLineEdit()
        self.librettista.setPlaceholderText("Inserire librettista")

        label_atti = QLabel('Numeri di atti<span style="color:red;">*</span> :')
        label_atti.setProperty(WidgetRole.BODY_TEXT, True)
        label_atti.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
        self.atti = QSpinBox()
        self.atti.setRange(0, 10)
        self.atti.setValue(0)

        label_data = QLabel('Prima rappresentazione<span style="color:red;">*</span> :')
        label_data.setProperty(WidgetRole.BODY_TEXT, True)
        label_data.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
        self.data = QDateEdit()
        self.data.setDisplayFormat("dd/MM/yyyy")

        label_teatro = QLabel(
            'Teatro prima rappresentazione<span style="color:red;">*</span> :'
        )
        label_teatro.setProperty(WidgetRole.BODY_TEXT, True)
        label_teatro.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
        self.teatro = QLineEdit()
        self.teatro.setPlaceholderText("Inserire nome del teatro")

        self._form_layout.addRow(label_nome, self.nome)
        self._form_layout.addRow(label_trama, self.trama)
        self._form_layout.addRow(label_genere, self.genere)
        self._form_layout.addRow(label_compositore, self.compositore)
        self._form_layout.addRow(label_librettista, self.librettista)
        self._form_layout.addRow(label_atti, self.atti)
        self._form_layout.addRow(label_data, self.data)
        self._form_layout.addRow(label_teatro, self.teatro)

    # ------------------------- METODI DI VIEW -------------------------

    def setup_genere_combobox(self, generi: list[Genere]) -> None:
        """Riempisce il `QComboBox` dei generi."""
        self.genere.clear()

        self.genere.insertItem(0, "Scegliere genere...", -1)
        # Avevo pensato di fare la prima opzione di colore grigio per chiarire che non
        #   è una opzione valida, ma per quello dovrei creare un delegate e non ho voglia.
        for i, g in enumerate(generi, start=1):
            self.genere.insertItem(i, g.get_nome(), g.get_id())

    @override
    def reset_pagina(self) -> None:
        super().reset_pagina()

        self.nome.setText("")
        self.trama.setText("")
        self.genere.setCurrentIndex(0)
        self.compositore.setText("")
        self.librettista.setText("")
        self.atti.setValue(0)
        self.data.setDate(QDate.currentDate())
        self.teatro.setText("")
        self._input_error.setText("")
