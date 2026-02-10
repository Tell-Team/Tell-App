from abc import abstractmethod
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QFormLayout,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QSizePolicy,
)
from PyQt6.QtCore import Qt, pyqtSignal
from functools import partial

from core.metaclasses import ABCQObjectMeta

from view.utils.custom_button import DefaultButton, SalvaButton

from view.style.ui_style import WidgetRole, WidgetColor


class AbstractCreaView(QWidget, metaclass=ABCQObjectMeta):
    """Classe astratta per la creazione di pagine dell'app dedicate alla creazione
    e modifica di oggetti del model.

    Segnali
    ---
    - `annullaRequest(QWidget)`: emesso quando si clicca il pulsante Annulla;
    - `salvaRequest()`: emesso quando si clicca il pulsante Salva.
    """

    annullaRequest = pyqtSignal(QWidget)
    salvaRequest = pyqtSignal()

    def __init__(self):
        super().__init__()

        self._setup_ui()
        self._connect_signals()

    # ------------------------- SETUP INIT -------------------------

    def _setup_ui(self) -> None:
        # Setup Header
        self._header = QLabel("")
        self._header.setProperty(WidgetRole.HEADER1, True)
        self._header.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Setup QFormLayout
        self.__form_content = QWidget()
        self.__form_content.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding
        )
        self._form_layout = QFormLayout(self.__form_content)
        self._form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self._setup_form()

        # Funzione di scroll
        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setWidget(self.__form_content)
        self._scroll_area.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding
        )

        # Setup Pulsanti
        self._btn_annulla = DefaultButton("Annulla")

        self._btn_conferma = SalvaButton("Salva")

        self._pulsanti = QWidget()
        layout_pulsanti = QHBoxLayout(self._pulsanti)
        layout_pulsanti.addWidget(self._btn_annulla)
        layout_pulsanti.addWidget(self._btn_conferma)
        layout_pulsanti.addStretch()

        # Label input_error
        self._input_error = QLabel("")
        self._input_error.setProperty(WidgetRole.BODY_TEXT, True)
        self._input_error.setProperty(WidgetColor.Text.ERROR_MESSAGE, True)

        # Setup main layout
        self._main_layout = QVBoxLayout(self)

    def _connect_signals(self) -> None:
        self._btn_annulla.clicked.connect(  # type:ignore
            partial(self.annullaRequest.emit, self)
        )

        self._btn_conferma.clicked.connect(  # type:ignore
            self.salvaRequest.emit
        )

    @abstractmethod
    def _setup_form(self) -> None:
        """Costruisce e dispone i widget della form."""
        ...

    # ------------------------- METODI DI VIEW -------------------------

    @abstractmethod
    def reset_pagina(self) -> None:
        """Resetta la pagina allo stato default."""
        if vertical_scroll := self._scroll_area.verticalScrollBar():
            vertical_scroll.setValue(0)

    def mostra_msg_input_error(self, message: str) -> None:
        """Aggiorna il testo della label `input_error`.

        :param message: testo inserito nel label
        """
        self._input_error.setText(message)
        self._input_error.show()  # Si assicura che la label sia visualizzata.

    def _svuota_form_layout(self, form_layout: QFormLayout) -> None:
        """Rimuove tutte le righe di un `QFormLayout` senza eliminare i widget. Serve per
        ricaricare un form."""
        while form_layout.rowCount():
            row = form_layout.takeRow(0)

            label_item, field_item = row.labelItem, row.fieldItem

            widget = label_item.widget()
            if widget is not None:
                widget.setParent(None)

            widget = field_item.widget()
            if widget is not None:
                widget.setParent(None)
