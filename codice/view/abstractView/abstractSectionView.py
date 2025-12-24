from abc import abstractmethod
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QLayout,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
)
from PyQt6.QtCore import pyqtSignal
from typing import Optional

from view.abstractView.abcQObjectMeta import ABCQObjectMeta
from view.style import QssStyle


class AbstractSectionView(QWidget, metaclass=ABCQObjectMeta):
    """Classe astratta che facilita la creazione delle pagine di sezione
    dell'app: Spettacoli, Info ed Account.

    - logoutRequest(): emesso quando si clicca il pulsante Logout;
    - goToSpettacoli(): emesso quando si clicca il pulsante Spettacoli;
    - goToInfo(): emesso quando si clicca il pulsante Info;
    - goToAccount(): emesso quando si clicca il pulsante Account.
    """

    logoutRequest = pyqtSignal()
    goToSpettacoli = pyqtSignal()
    goToInfo = pyqtSignal()
    goToAccount = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        # Logout
        self._btn_logout = QPushButton("Logout")
        self._btn_logout.setProperty(QssStyle.WHITE_BUTTON.style_role, True)

        widget_logout = QWidget()
        layout_logout = QHBoxLayout(widget_logout)
        layout_logout.addWidget(self._btn_logout)
        layout_logout.addStretch()

        # Sezioni dell'app
        self._btn_sezione_spettacoli = QPushButton("Spettacoli")
        self._btn_sezione_spettacoli.setProperty(QssStyle.WHITE_BUTTON.style_role, True)

        self._btn_sezione_info = QPushButton("Info")
        self._btn_sezione_info.setProperty(QssStyle.WHITE_BUTTON.style_role, True)

        self._btn_sezione_account = QPushButton("Account")
        self._btn_sezione_account.setProperty(QssStyle.WHITE_BUTTON.style_role, True)

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
        layout_top.addSpacing(5)
        layout_top.addWidget(sezioni_app)

        # Funzione di scroll
        scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_widget)

        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setWidget(scroll_widget)

        # Main layout Setup
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(container_top)
        self.main_layout.addWidget(self._scroll_area)

    def _connect_signals(self) -> None:
        self._btn_logout.clicked.connect(  # type:ignore
            self.logoutRequest.emit
        )

        self._btn_sezione_spettacoli.clicked.connect(  # type:ignore
            self.goToSpettacoli
        )

        self._btn_sezione_info.clicked.connect(  # type:ignore
            self.goToInfo.emit
        )

        self._btn_sezione_account.clicked.connect(  # type:ignore
            self.goToAccount.emit
        )

    # ------------------------- METODI DI VIEW -------------------------

    @abstractmethod
    def aggiorna_pagina(self) -> None:
        """Permette di aggiornare la pagina e visualizzare modifiche previamente non mostrate."""
        ...

    def if_lista_vuota(self, layout: QVBoxLayout) -> None:
        """Indica che la lista non ha istanze da visualizzare.

        :param layout: layout dove si mostrerà un messaggio indicando l'assenza di intanze
        """
        # Il suo funzionamento dipende di come aggiorna_pagina aggiunge il label di errore nei layout.
        error_msg = layout.itemAt(0).widget()  # type:QLabel # type:ignore
        error_msg.show()

    def aggiungi_widget_a_layout(self, widget: QWidget, layout: QVBoxLayout):
        """Aggiunge un widget creato per il display delle istanze del model.

        :param widget: widget speciale per visualizzare una instanza del model
        :param layout: layout dove sarà inserito il widget"""
        # C'era un errore al utilizzare widget.setProperty() direttamente:
        #   lo style non veniva asegnato al widget. Quindi ho decisso di aggiungere questo
        #   dummy widget per farlo funzionare.
        dummy_widget = QWidget()
        dummy_widget.setProperty(QssStyle.ITEM_CARD.style_role, True)
        l = QVBoxLayout(dummy_widget)
        l.addWidget(widget)

        layout.addWidget(dummy_widget)

    def _svuota_layout(self, layout: Optional[QLayout]) -> None:
        """Svuota un layout, eliminando i riferimenti ai widget contenuti. In caso
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
                    self._svuota_layout(child_layout)
