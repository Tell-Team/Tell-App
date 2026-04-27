from abc import abstractmethod
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea
from PyQt6.QtCore import pyqtSignal

from core.metaclasses import ABCQObjectMeta

from view.utils.custom_button import DefaultButton


class AbstractVisualizzaView(QWidget, metaclass=ABCQObjectMeta):
    """Classe astratta per la creazione di pagine dell'app che non sono pagine di sezione
    persé, ma permettono di navigare verso altre pagine, e.g. pagine di crea/modifica, e
    tornare dietro.

    Segnali
    ---
    - `tornaIndietroRequest()`: emesso quando si clicca il pulsante Indietro.
    """

    tornaIndietroRequest = pyqtSignal()

    def __init__(self):
        super().__init__()

        self._setup_ui()
        self._connect_signals()

    # ------------------------- SETUP INIT -------------------------

    def _setup_ui(self) -> None:
        # Top widget
        self._btn_indietro = DefaultButton("Indietro")

        pagina_header = QWidget()
        layout_header = QHBoxLayout(pagina_header)
        layout_header.addWidget(self._btn_indietro)
        layout_header.addStretch()

        pagina_content = QWidget()
        self._layout_content = QVBoxLayout(pagina_content)

        # Funzione di scroll
        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setWidget(pagina_content)

        # Layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(pagina_header)
        main_layout.addWidget(self._scroll_area)

    def _connect_signals(self) -> None:
        self._btn_indietro.clicked.connect(  # type:ignore
            self.tornaIndietroRequest.emit
        )

    # ------------------------- METODI DI VIEW -------------------------

    @abstractmethod
    def set_data(self, data: object, lista: list[object]) -> None:
        """Carica i dati dell'oggetto associato alla pagina.

        :param data: data dell'oggetto centrale salvata in una classe immutabile
        :param lista: lista di oggetti associata all'oggetto centrale, non è sempre
        necessaria"""
        ...

    @abstractmethod
    def aggiorna_pagina(self) -> None:
        """Permette di aggiornare la pagina e visualizzare modifiche previamente non mostrate."""
        if vertical_scroll := self._scroll_area.verticalScrollBar():
            vertical_scroll.setValue(0)
