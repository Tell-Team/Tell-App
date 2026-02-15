"""
Modulo dedicato al display delle lista di oggetti.

Contieni le classi e metodi necessari per aggiungere item alle liste,
resettarle e mostrare in messaggio di errore nel caso non ci sia nessun
item.
"""

from PyQt6.QtWidgets import QWidget, QLabel, QLayout, QVBoxLayout
from typing import Optional

from view.style.ui_style import WidgetStyle


# Queste classi vuote servono per evitare possibili errori al chiamare i metodi di ListLayout.
class ItemDisplay(QWidget):
    """Widget per caricare le informazionidelle istanze del model."""

    pass


class EmptyStateLabel(QLabel):
    """Label per messaggi di 'Lista vuota' nelle pagine della view."""

    pass


class ListLayout(QVBoxLayout):
    """Layout per la visualizzazione delle istanze del model a schermo."""

    def __init__(self, parent: Optional[QWidget], label: EmptyStateLabel):
        super().__init__(parent)
        # Asegna lo stesso margine a tutte le istanze
        self.setContentsMargins(1, 1, 1, 1)

        # self.__error_msg = label
        # self.addWidget(self.__error_msg)
        # self.__error_msg.hide()
        self.__box = QWidget()
        dummy_layout = QVBoxLayout(self.__box)
        dummy_layout.addWidget(label)
        self.addWidget(self.__box)
        self.__box.hide()

    def svuota_layout(self, layout: Optional[QLayout] = None) -> None:
        """Aggiunge il `EmptyStateLabel` indicato nell'`__init__` dopo svuotare il layout."""
        # Non elimina il primo elemento: il EmptyStateLabel
        if self.count() <= 1:
            self.__box.hide()
            self.setContentsMargins(1, 1, 1, 1)
            return

        from view.utils import svuota_layout_generico

        svuota_layout_generico(self, 1)

    def mostra_msg_lista_vuota(self) -> None:
        """Mostra un messaggio indicando che la lista non ha istanze da visualizzare."""
        self.setContentsMargins(2, 2, 2, 2)
        self.__box.show()

    def aggiungi_list_item(self, widget: ItemDisplay, *styles: WidgetStyle) -> None:
        """Aggiunge un widget creato per il display delle istanze del model.

        :param widget: widget speciale per visualizzare una instanza del model
        :param styles: style opzionale da assegnare al widget (0...*)
        """
        # C'è un errore al utilizzare widget.setProperty() direttamente:
        #   lo style non veniva asegnato per qualche motivo. Quindi ho decisso
        #   di aggiungere questo dummy_widget per farlo funzionare.
        if not styles:
            self.addWidget(widget)
            return
        dummy_widget = QWidget()
        for style in styles:
            dummy_widget.setProperty(style, True)
        l = QVBoxLayout(dummy_widget)
        l.addWidget(widget)
        self.addWidget(dummy_widget)
