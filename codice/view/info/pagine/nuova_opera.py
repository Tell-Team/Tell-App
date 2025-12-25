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

from model.pianificazione.genere import Genere

from view.abstractView.abstractCreaView import AbstractCreaView

from view.style import QssStyle


class NuovaOperaView(AbstractCreaView):
    """View per la creazione di una nuova opera.

    Segnali:
    - annullaRequest(QWidget): emesso quando si clicca il pulsante Annulla;
    - salvaRequest(): emesso quando si clicca il pulsante Crea.
    """

    def __init__(self) -> None:
        super().__init__()

        self._setup_ui()
        self._connect_signals()

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        # Header
        self._header.setText("Aggiungi nuova opera")

        # Form
        self._setup_form()

        # Layout
        self._main_layout.addWidget(self._header)
        self._main_layout.addWidget(self._scroll_area)
        self._main_layout.addWidget(self._input_error)
        self._main_layout.addWidget(self._pulsanti)

    @override
    def _setup_form(self) -> None:
        label_nome = QLabel('Nome<span style="color:red;">*</span> :')
        label_nome.setProperty(QssStyle.SECONDARY_TEXT.style_role, True)
        self.nome = QLineEdit()
        self.nome.setPlaceholderText("Inserire nome")

        label_trama = QLabel('Trama<span style="color:red;">*</span> :')
        label_trama.setProperty(QssStyle.SECONDARY_TEXT.style_role, True)
        self.trama = QTextEdit()
        self.trama.setPlaceholderText("Inserire trama")
        self.trama.setFixedHeight(80)

        label_genere = QLabel('Genere<span style="color:red;">*</span> :')
        label_genere.setProperty(QssStyle.SECONDARY_TEXT.style_role, True)
        self.genere = QComboBox()

        label_compositore = QLabel('Compositore<span style="color:red;">*</span> :')
        label_compositore.setProperty(QssStyle.SECONDARY_TEXT.style_role, True)
        self.compositore = QLineEdit()
        self.compositore.setPlaceholderText("Inserire compositore")

        label_librettista = QLabel('Librettista<span style="color:red;">*</span> :')
        label_librettista.setProperty(QssStyle.SECONDARY_TEXT.style_role, True)
        self.librettista = QLineEdit()
        self.librettista.setPlaceholderText("Inserire librettista")

        label_atti = QLabel('Numeri di atti<span style="color:red;">*</span> :')
        label_atti.setProperty(QssStyle.SECONDARY_TEXT.style_role, True)
        self.atti = QSpinBox()
        self.atti.setRange(0, 10)
        self.atti.setValue(0)

        label_data = QLabel('Prima rappresentazione<span style="color:red;">*</span> :')
        label_data.setProperty(QssStyle.SECONDARY_TEXT.style_role, True)
        self.data = QDateEdit()
        self.data.setCalendarPopup(True)
        self.data.setDisplayFormat("dd/MM/yyyy")

        # atti_data_layout = QHBoxLayout()
        # atti_data_layout.addWidget(label_atti)
        # atti_data_layout.addWidget(self.atti)
        # atti_data_layout.addWidget(label_data)
        # atti_data_layout.addWidget(self.data)

        label_teatro = QLabel(
            'Teatro prima rappresentazione<span style="color:red;">*</span> :'
        )
        label_teatro.setProperty(QssStyle.SECONDARY_TEXT.style_role, True)
        self.teatro = QLineEdit()
        self.teatro.setPlaceholderText("Inserire nome del teatro")

        self._form_layout.addRow(label_nome, self.nome)
        self._form_layout.addRow(label_trama, self.trama)
        self._form_layout.addRow(label_genere, self.genere)
        self._form_layout.addRow(label_compositore, self.compositore)
        self._form_layout.addRow(label_librettista, self.librettista)
        self._form_layout.addRow(label_atti, self.atti)
        self._form_layout.addRow(label_data, self.data)
        # self.form_layout.addRow(atti_data_layout)
        self._form_layout.addRow(label_teatro, self.teatro)

    # ------------------------- METODI DI VIEW -------------------------

    def setup_genere_combobox(self, generi: list[Genere]) -> None:
        """Riempisce il `QComboBox` dei generi."""
        self.genere.clear()

        self.genere.insertItem(0, "Scegliere genere...", -1)
        # Avevo pensato di fare la prima opzione di colore grigio per far carire che non
        #   è una opzione valida, ma per quello dovrei creare un delegate e non ho voglia.
        for i, g in enumerate(generi):
            i += 1
            self.genere.insertItem(i, g.get_nome(), g.get_id())

    @override
    def reset_pagina(self) -> None:
        self.nome.setText("")
        self.trama.setText("")
        self.genere.setCurrentIndex(0)
        self.compositore.setText("")
        self.librettista.setText("")
        self.atti.setValue(0)
        self.data.setDate(QDate.currentDate())
        self.teatro.setText("")
        self._input_error.setText("")
