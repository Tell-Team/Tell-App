# Widget speciali per il display delle lista di oggetti.

from PyQt6.QtWidgets import QWidget, QLabel, QLayout, QVBoxLayout
from typing import Optional


class EmptyStateLabel(QLabel):
    """Label usato per messaggi di 'Lista vuota' nelle pagine della view."""

    pass


class ListLayout(QVBoxLayout):
    """Layout per la visualizzazione delle istanze del model a schermo."""

    # Per creare un'istanza, è necessario inserire un EmptyStateLabel che funzionerà
    #   come messaggio di errore quando la lista sia svuotata.
    def __init__(self, parent: Optional[QWidget], label: EmptyStateLabel) -> None:
        super().__init__(parent)

        self.label = label

        self.addWidget(self.label)
        self.label.hide()  # Il label viene nascosto dalla propria ListLayout.

    def svuota_layout(self, layout: Optional[QLayout] = None) -> None:
        """Aggiunge il `EmptyStateLabel` indicato nell'`__init__` dopo svuotare il layout."""
        while self.count():
            item = self.takeAt(0)
            assert item is not None
            if widget := item.widget():
                widget.setParent(None)
            elif child_layout := item.layout():
                self.svuota_layout(child_layout)

        # Ritorna allo stato iniziale
        self.addWidget(self.label)
        self.label.hide()

    def if_lista_vuota(self) -> None:
        """Mostra un messaggio indicando che la lista non ha istanze da visualizzare."""
        item = self.itemAt(0)
        if not item:
            return

        error_msg = item.widget()
        if isinstance(error_msg, EmptyStateLabel):
            error_msg.show()
