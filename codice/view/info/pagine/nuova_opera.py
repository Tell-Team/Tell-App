from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QDateEdit,
    QSpinBox,
    # QHBoxLayout,
)
from PyQt6.QtCore import QDate, pyqtSignal
from functools import partial
from typing import override

from model.pianificazione.genere import Genere

from view.abstractView.creaAbstract import CreaAbstractView


class NuovaOperaView(CreaAbstractView):
    """View per la creazione di una nuova opera.

    Segnali:
    - annullaRequest(CreaAbstractView): emesso quando si clicca il pulsante Annulla;
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
        self.header.setText("Aggiungi nuova opera")

        # Form
        self._setup_form()

        # Layout
        self.main_layout.addWidget(self.header)
        self.main_layout.addWidget(self._scroll_area)
        self.main_layout.addWidget(self.input_error)
        self.main_layout.addWidget(self.pulsanti)

    @override
    def _setup_form(self) -> None:
        label_nome = QLabel("Nome :")
        label_nome.setObjectName("subheader")
        self.nome = QLineEdit()
        self.nome.setPlaceholderText("Inserire nome")

        label_trama = QLabel("Trama :")
        label_trama.setObjectName("subheader")
        self.trama = QTextEdit()
        self.trama.setPlaceholderText("Inserire trama")
        self.trama.setFixedHeight(80)

        label_genere = QLabel("Genere :")
        label_genere.setObjectName("subheader")
        self.genere = QComboBox()

        label_compositore = QLabel("Compositore :")
        label_compositore.setObjectName("subheader")
        self.compositore = QLineEdit()
        self.compositore.setPlaceholderText("Inserire compositore")

        label_librettista = QLabel("Librettista :")
        label_librettista.setObjectName("subheader")
        self.librettista = QLineEdit()
        self.librettista.setPlaceholderText("Inserire librettista")

        label_atti = QLabel("Numeri di atti :")
        label_atti.setObjectName("subheader")
        self.atti = QSpinBox()
        self.atti.setRange(0, 10)
        self.atti.setValue(0)

        label_data = QLabel("Prima rappresentazione :")
        label_data.setObjectName("subheader")
        self.data = QDateEdit()
        self.data.setCalendarPopup(True)
        self.data.setDisplayFormat("dd/MM/yyyy")

        # atti_data_layout = QHBoxLayout()
        # atti_data_layout.addWidget(label_atti)
        # atti_data_layout.addWidget(self.atti)
        # atti_data_layout.addWidget(label_data)
        # atti_data_layout.addWidget(self.data)

        label_teatro = QLabel("Teatro prima rappresentazione :")
        label_teatro.setObjectName("subheader")
        self.teatro = QLineEdit()
        self.teatro.setPlaceholderText("Inserire nome del teatro")

        self.form_layout.addRow(label_nome, self.nome)
        self.form_layout.addRow(label_trama, self.trama)
        self.form_layout.addRow(label_genere, self.genere)
        self.form_layout.addRow(label_compositore, self.compositore)
        self.form_layout.addRow(label_librettista, self.librettista)
        self.form_layout.addRow(label_atti, self.atti)
        self.form_layout.addRow(label_data, self.data)
        # self.form_layout.addRow(atti_data_layout)
        self.form_layout.addRow(label_teatro, self.teatro)

    def _connect_signals(self) -> None:
        self._btn_annulla.clicked.connect(  # type:ignore
            partial(self.annullaRequest.emit, self)
        )

        self._btn_conferma.clicked.connect(  # type:ignore
            self.salvaRequest.emit
        )

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
        self.input_error.setText("")
