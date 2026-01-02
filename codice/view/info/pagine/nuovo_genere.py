from PyQt6.QtWidgets import QLabel, QLineEdit, QTextEdit, QSizePolicy
from typing import override

from core.view import AbstractCreaView

from view.style import QssStyle


class NuovoGenereView(AbstractCreaView):
    """View per la creazione di un nuovo genere.

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
        self._header.setText("Aggiungi nuovo genere")

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
        label_nome.setProperty(QssStyle.SECONDARY_TEXT, True)
        self.nome = QLineEdit()
        self.nome.setPlaceholderText("Inserire nome")

        label_descrizione = QLabel('Descrizione<span style="color:red;">*</span> :')
        label_descrizione.setProperty(QssStyle.SECONDARY_TEXT, True)
        self.descrizione = QTextEdit()
        self.descrizione.setPlaceholderText("Inserire descrizione")
        self.descrizione.setFixedHeight(80)
        self.descrizione.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )

        self._form_layout.addRow(label_nome, self.nome)
        self._form_layout.addRow(label_descrizione, self.descrizione)

    # ------------------------- METODI DI VIEW -------------------------

    @override
    def reset_pagina(self) -> None:
        self.nome.setText("")
        self.descrizione.setText("")
