from PyQt6.QtWidgets import QLabel, QLineEdit, QTextEdit, QSizePolicy
from PyQt6.QtCore import pyqtSignal
from functools import partial
from typing import override

from view.abstractView.creaAbstract import CreaAbstractView


class NuovoGenereView(CreaAbstractView):
    """View per la creazione di un nuovo genere.

    Segnali:
    - annullaRequest(): emesso quando si clicca il pulsante Annulla;
    - salvaRequest(): emesso quando si clicca il pulsante Conferma.
    """

    annullaRequest = pyqtSignal(CreaAbstractView)
    salvaRequest = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

        self._setup_ui()
        self._connect_signals()

    # ------------------------- SETUP INIT -------------------------

    def _setup_ui(self) -> None:
        # Header
        self.header.setText("Aggiungi nuovo genere")

        # Form
        self._setup_form()

        # Layout
        self.main_layout.addWidget(self.header)
        self.main_layout.addWidget(self.form_content)
        self.main_layout.addWidget(self.input_error)
        self.main_layout.addWidget(self.pulsanti)
        self.main_layout.addStretch()

    @override
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

    def _connect_signals(self) -> None:
        self._btn_annulla.clicked.connect(  # type:ignore
            partial(self.annullaRequest.emit, self)
        )

        self._btn_conferma.clicked.connect(  # type:ignore
            self.salvaRequest.emit
        )

    # ------------------------- METODI DI VIEW -------------------------

    def reset_pagina(self) -> None:
        """Reset della pagina allo stato default."""
        self.nome.setText("")
        self.descrizione.setText("")

    def set_pagina_focus(self) -> None:
        """Evidenzia il primo campo con input non valido trovato."""
        self.focusNextChild()
        if not self.nome.text().strip():
            return
        self.focusNextChild()
