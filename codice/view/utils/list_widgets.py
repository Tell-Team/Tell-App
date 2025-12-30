"""
Modulo dedicato al display delle lista di oggetti.

Contieni le classi e metodi necessari per aggiungere item alle liste,
resettarle e mostrare in messaggio di errore nel caso non ci sia nessun
item.
"""

from PyQt6.QtWidgets import QWidget, QLabel, QLayout, QVBoxLayout
from typing import Optional


# Queste classi vuote servono per evitare possibili errori al chiamare i metodi di ListLayout.
class ItemDisplay(QWidget):
    """Widget per caricare le informazionidelle istanze del model."""

    pass


class EmptyStateLabel(QLabel):
    """Label per messaggi di 'Lista vuota' nelle pagine della view."""

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
            self.setContentsMargins(1, 1, 1, 1)
            return

        while self.count() > 1:
            item = self.takeAt(1)
            if item is None:  # Sempre c'è un EmptyStateLabel
                raise ValueError("Expected item at index 1")  # Non lancia mai l'error
            if widget := item.widget():
                widget.setParent(None)
                widget.deleteLater()  # Evita potenziali memory leaks
            elif child_layout := item.layout():
                self.svuota_layout(child_layout)

    def if_lista_vuota(self) -> None:
        """Mostra un messaggio indicando che la lista non ha istanze da visualizzare."""
        self.setContentsMargins(2, 2, 2, 2)
        self.__label.show()
        # Siccome il label non viene mai rimosso dal layout, usare direttamente
        #   self.__label.show() è sicuro. Comunque, questa è la logica usata nel
        #   caso in cui non è sicuro che il primo elemento (se c'è) sia EmptyStateLabel.
        # item = self.itemAt(0)
        # if not item:
        #     return

        # error_msg = item.widget()
        # if isinstance(error_msg, EmptyStateLabel):
        #     self.setContentsMargins(2, 2, 2, 2)
        #     error_msg.show()

    def aggiungi_list_item(self, widget: ItemDisplay, style: str = "") -> None:
        """Aggiunge un widget creato per il display delle istanze del model.

        :param widget: widget speciale per visualizzare una instanza del model
        :param style: style opzionale da assegnare al widget"""
        # C'è un errore al utilizzare widget.setProperty() direttamente:
        #   lo style non veniva asegnato per qualche motivo. Quindi ho decisso
        #   di aggiungere questo dummy_widget per farlo funzionare.
        if not style:
            self.addWidget(widget)
            return
        dummy_widget = QWidget()
        dummy_widget.setProperty(style, True)
        l = QVBoxLayout(dummy_widget)
        l.addWidget(widget)
        self.addWidget(dummy_widget)
