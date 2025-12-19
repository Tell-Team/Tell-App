from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QLayout,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
)
from typing import Optional


class AbstractSectionView(QWidget):
    """
    Classe pseudo-astratta che facilita la creazione delle pagine di sezione dell'app: Spettacoli,
    Info ed Account.
    """

    def __init__(self) -> None:
        super().__init__()

        # Logout
        self._btn_logout = QPushButton("Logout")
        self._btn_logout.setObjectName("WhiteButton")

        widget_logout = QWidget()
        layout_logout = QHBoxLayout(widget_logout)
        layout_logout.addWidget(self._btn_logout)
        layout_logout.addStretch()

        # Sezioni dell'app
        self._btn_sezione_spettacoli = QPushButton("Spettacoli")
        self._btn_sezione_spettacoli.setObjectName("WhiteButton")

        self._btn_sezione_info = QPushButton("Info")
        self._btn_sezione_info.setObjectName("WhiteButton")

        self._btn_sezione_account = QPushButton("Account")
        self._btn_sezione_account.setObjectName("WhiteButton")

        sezioni_app = QWidget()
        layout_sezioni = QHBoxLayout(sezioni_app)
        layout_sezioni.addWidget(self._btn_sezione_spettacoli)
        layout_sezioni.addWidget(self._btn_sezione_info)
        layout_sezioni.addWidget(self._btn_sezione_account)
        layout_sezioni.addStretch()

        # Top layout
        container_top = QWidget()
        layout_top = QVBoxLayout(container_top)
        layout_top.addWidget(widget_logout)
        layout_top.addSpacing(15)
        layout_top.addWidget(sezioni_app)

        # Funzione di scroll
        scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_widget)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)

        # Main layout Setup
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(container_top)
        self.main_layout.addWidget(scroll_area)

    # ------------------------- METODI DI VIEW -------------------------

    def refresh_page(self) -> None:
        """Permette di aggiornare la pagina e visualizzare modifiche previamente non mostrate."""
        ...

    def aggiungi_widget_al_layout(self, widget: QWidget, layout: QVBoxLayout):
        """Aggiunge un widget creato per il display delle istanze del model.

        :param widget: widget speciale per visualizzare una instanza del model
        :param layout: layout dove sarà inserito il widget"""
        # C'era un errore al utilizzare widget.setObjectName("Container") direttamente:
        #   lo style non veniva asegnato al widget. Quindi ho decisso di aggiungere questo
        #   dummy widget per farlo funzionare.
        dummy_widget = QWidget()
        dummy_widget.setObjectName("Container")
        l = QVBoxLayout(dummy_widget)
        l.addWidget(widget)

        layout.addWidget(dummy_widget)

    def clear_layout(self, layout: Optional[QLayout]) -> None:
        """
        Pulisce un layout, eliminando i riferimenti ai widget contenuti. In caso
        ci sia un layout contenuto, questo viene anche pulito.

        :param layout: layout da pulire
        """
        if layout:
            while layout.count():
                item = layout.takeAt(0)
                assert item is not None
                widget = item.widget()

                if widget:
                    widget.setParent(None)
                    continue

                child_layout = item.layout()
                if child_layout:
                    self.clear_layout(child_layout)
