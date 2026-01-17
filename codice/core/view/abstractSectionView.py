from abc import abstractmethod
from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
)
from PyQt6.QtCore import pyqtSignal

from core.metaclasses import ABCQObjectMeta

from view.style import WidgetRole


class AbstractSectionView(QWidget, metaclass=ABCQObjectMeta):
    """Classe astratta per la creazione di pagine di sezione dell'app: Acquisto,
    Spettacoli, Info ed Account.

    Segnali
    ---
    - `logoutRequest()`: emesso quando si clicca il pulsante Logout;
    - `goToAcquisto()`: emesso quando si clicca il pulsante Acquisto;
    - `goToSpettacoli()`: emesso quando si clicca il pulsante Spettacoli;
    - `goToInfo()`: emesso quando si clicca il pulsante Info;
    - `goToAccount()`: emesso quando si clicca il pulsante Account.
    """

    logoutRequest = pyqtSignal()

    goToAcquisto = pyqtSignal()
    goToSpettacoli = pyqtSignal()
    goToInfo = pyqtSignal()
    goToAccount = pyqtSignal()

    def __init__(self):
        super().__init__()

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        # Logout
        self._btn_logout = QPushButton("Logout")
        self._btn_logout.setProperty(WidgetRole.DEFAULT_BUTTON, True)

        widget_logout = QWidget()
        layout_logout = QHBoxLayout(widget_logout)
        layout_logout.addWidget(self._btn_logout)
        layout_logout.addStretch()

        # Sezioni dell'app
        self._btn_sezione_acquisto = QPushButton("Acquisto")
        self._btn_sezione_acquisto.setProperty(WidgetRole.DEFAULT_BUTTON, True)

        self._btn_sezione_spettacoli = QPushButton("Spettacoli")
        self._btn_sezione_spettacoli.setProperty(WidgetRole.DEFAULT_BUTTON, True)

        self._btn_sezione_info = QPushButton("Info")
        self._btn_sezione_info.setProperty(WidgetRole.DEFAULT_BUTTON, True)

        self._btn_sezione_account = QPushButton("Account")
        self._btn_sezione_account.setProperty(WidgetRole.DEFAULT_BUTTON, True)

        sezioni_app = QWidget()
        layout_sezioni = QHBoxLayout(sezioni_app)
        layout_sezioni.addWidget(self._btn_sezione_acquisto)
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

        self._btn_sezione_acquisto.clicked.connect(  # type:ignore
            self.goToAcquisto
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
