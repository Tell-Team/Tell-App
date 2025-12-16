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
        self.btn_logout = QPushButton("Logout")
        self.btn_logout.setObjectName("SmallButton")

        widget_logout = QWidget()
        layout_logout = QHBoxLayout(widget_logout)
        layout_logout.addWidget(self.btn_logout)
        layout_logout.addStretch()

        # Sezioni dell'app
        self.btn_sezione_spettacoli = QPushButton("Spettacoli")
        self.btn_sezione_spettacoli.setObjectName("SmallButton")

        self.btn_sezione_info = QPushButton("Info")
        self.btn_sezione_info.setObjectName("SmallButton")

        self.btn_sezione_account = QPushButton("Account")
        self.btn_sezione_account.setObjectName("SmallButton")

        sezioni_app = QWidget()
        layout_sezioni = QHBoxLayout(sezioni_app)
        layout_sezioni.addWidget(self.btn_sezione_spettacoli)
        layout_sezioni.addWidget(self.btn_sezione_info)
        layout_sezioni.addWidget(self.btn_sezione_account)
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

    def refresh_page(self) -> None:
        """Permette di aggiornare la pagina e visualizzare modifiche previamente non mostrate."""
        ...

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
