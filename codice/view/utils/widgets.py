# Widget speciali per il display delle lista di oggetti.

from PyQt6.QtWidgets import QWidget, QLabel, QLayout, QVBoxLayout
from typing import Optional


class EmptyStateLabel(QLabel):
    """Label usato per messaggi di 'Lista vuota' nelle pagine della view."""

    pass


class ListLayout(QVBoxLayout):
    """Layout per la visualizzazione delle istanze del model a schermo."""

    def __init__(self, parent: Optional[QWidget], label: EmptyStateLabel) -> None:
        super().__init__(parent)
        # Asegna lo stesso margine a tutte le istanze
        self.setContentsMargins(1, 1, 1, 1)

        self.__label = label  # Messagi di errore quando la lista è vuota

        self.addWidget(self.__label)
        self.__label.hide()  # Il label viene nascosto dalla propria ListLayout.

    def svuota_layout(self, layout: Optional[QLayout] = None) -> None:
        """Aggiunge il `EmptyStateLabel` indicato nell'`__init__` dopo svuotare il layout."""
        # Non elimina il primo elemento: il EmptyStateLabel
        if self.count() <= 1:
            self.__label.hide()
            return

        while self.count() > 1:
            item = self.takeAt(1)
            assert item is not None
            if widget := item.widget():
                widget.setParent(None)
                widget.deleteLater()  # Evita potenziali memory leaks
            elif child_layout := item.layout():
                self.svuota_layout(child_layout)

    def if_lista_vuota(self) -> None:
        """Mostra un messaggio indicando che la lista non ha istanze da visualizzare."""
        item = self.itemAt(0)
        if not item:
            return

        error_msg = item.widget()
        if isinstance(error_msg, EmptyStateLabel):
            error_msg.show()

    def aggiungi_list_item(self, widget: QWidget, style: Optional[str] = None):
        """Aggiunge un widget creato per il display delle istanze del model.

        :param widget: widget speciale per visualizzare una instanza del model
        :param style: style opzionale da assegnare al widget"""
        # C'è un errore al utilizzare widget.setProperty() direttamente al widget:
        #   lo style non veniva asegnato. Quindi ho decisso di aggiungere questo
        #   dummy_widget per farlo funzionare.
        dummy_widget = QWidget()
        if style:
            dummy_widget.setProperty(style, True)

        l = QVBoxLayout(dummy_widget)
        l.addWidget(widget)

        self.addWidget(dummy_widget)
