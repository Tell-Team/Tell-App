from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    # QLayout,
    QGridLayout,
)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import override

from core.view import AbstractVisualizzaView

from view.utils.list_widgets import ListLayout, EmptyStateLabel
from view.utils import make_vline

from view.style.ui_style import WidgetRole, WidgetColor


class PrezziAssociatiView(AbstractVisualizzaView):
    """Pagina per visualizzare le coppie sezione-prezzo associate ad uno `Spettacolo`. Permette
    di crea, modificare o eliminare prezzi associati alle sezione per uno `Spettacolo`.

    Segnali
    ---
    - `displaySezioniPrezziRequest(ListLayout)`: emesso per mostrare a schermo la lista di
    coppie sezione-prezzo.
    """

    displaySezioniPrezziRequest = pyqtSignal(ListLayout)

    def __init__(self):
        self.id_current_spettacolo: int = -1

        super().__init__()

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        # Lista Sezioni-prezzi
        header_sezioni_prezzi = QLabel("Lista prezzi (associati a sezioni)")
        header_sezioni_prezzi.setProperty(WidgetRole.HEADER1, True)
        header_sezioni_prezzi.setAlignment(Qt.AlignmentFlag.AlignLeft)

        label_lista_sezioni_vuota = EmptyStateLabel(
            "Al momento, non vi sono sezioni registrate."
        )
        label_lista_sezioni_vuota.setProperty(WidgetRole.BODY_TEXT, True)
        label_lista_sezioni_vuota.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)

        content_sezioni_prezzi = QWidget()
        content_sezioni_prezzi.setProperty(WidgetRole.ITEM_LIST, True)
        self.layout_sezioni_prezzi_box = ListLayout(
            content_sezioni_prezzi, label_lista_sezioni_vuota
        )

        header_sezione = QLabel("Sezione")
        header_sezione.setProperty(WidgetRole.HEADER3, True)
        header_prezzo = QLabel("Prezzo")
        header_prezzo.setProperty(WidgetRole.HEADER3, True)
        header_opzioni = QLabel("Opzioni")
        header_opzioni.setProperty(WidgetRole.HEADER3, True)

        header_lista_sezioni_prezzi = QWidget()
        layout_lista_sezioni_prezzi = QGridLayout(header_lista_sezioni_prezzi)
        layout_lista_sezioni_prezzi.setContentsMargins(1, 1, 1, 1)
        layout_lista_sezioni_prezzi.addWidget(
            header_sezione, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout_lista_sezioni_prezzi.addWidget(make_vline(), 0, 1)
        layout_lista_sezioni_prezzi.addWidget(
            header_prezzo, 0, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )

        layout_lista_sezioni_prezzi.addWidget(make_vline(), 0, 3)
        layout_lista_sezioni_prezzi.addWidget(
            header_opzioni, 0, 4, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.sezioni_prezzi = QWidget()
        self.layout_sezioni_prezzi = QVBoxLayout(self.sezioni_prezzi)
        self.layout_sezioni_prezzi.addWidget(header_sezioni_prezzi)
        self.layout_sezioni_prezzi.addWidget(header_lista_sezioni_prezzi)
        self.layout_sezioni_prezzi.addWidget(content_sezioni_prezzi)
        # end-Lista Sezioni-prezzi

        # Layout
        self._layout_content.addWidget(self.sezioni_prezzi)
        self._layout_content.addStretch()

    # ------------------------- METODI DI VIEW -------------------------

    @override
    def set_data(self, id_spettacolo: int) -> None:  # type: ignore[override]
        """Carica i dati dello spettacolo nella pagina.

        :param data: data salvata in una classe immutabile"""
        # Reset layout lista sezioni-prezzi
        self.layout_sezioni_prezzi_box.svuota_layout()

        # Salva dati dello spettacolo nella pagina
        self.id_current_spettacolo = id_spettacolo

    @override
    def aggiorna_pagina(self) -> None:
        super().aggiorna_pagina()

        self.layout_sezioni_prezzi_box.svuota_layout()
        self.displaySezioniPrezziRequest.emit(self.layout_sezioni_prezzi_box)
