from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    # QApplication,
    # QStyle,
)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import override

from view.abstractView.sectionAbstract import AbstractSectionView


class SpettacoliSectionView(AbstractSectionView):
    """View della sezione Spettacoli dell'app.

    Segnali:
    - logoutRequest(): emesso quando si clicca il pulsante Logout;
    - goToInfo(): emesso quando si clicca il pulsante Info;
    - goToAccount(): emesso quando si clicca il pulsante Account;
    - nuovoSpettacoloRequest(): emesso quando si clicca il pulsante Nuovo spettacolo;
    - displaySpettacoliRequest(QVBoxLayout): emesso per caricare la lista degli spettacoli
    nella sezione Spettacoli;
    """

    logoutRequest = pyqtSignal()
    goToInfo = pyqtSignal()
    goToAccount = pyqtSignal()

    nuovoSpettacoloRequest = pyqtSignal()
    displaySpettacoliRequest = pyqtSignal(QVBoxLayout)

    def __init__(self):
        super().__init__()

        self._setup_ui()
        self._connect_signals()

    # ------------------------- SETUP INIT -------------------------

    def _setup_ui(self):
        # Spettacoli
        header_spettacoli = QLabel("Spettacoli")
        header_spettacoli.setObjectName("header1")
        header_spettacoli.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.__btn_nuovo_spettacolo = QPushButton("Nuovo spettacolo")
        self.__btn_nuovo_spettacolo.setObjectName("whiteButton")

        self.filtro_ricerca: str = ""

        self.ricerca_bar = QLineEdit()
        self.ricerca_bar.setPlaceholderText("Inserire nome...")
        self.ricerca_bar.setClearButtonEnabled(True)
        self.ricerca_bar.setObjectName("searchBar")

        self._btn_ricerca = QPushButton()
        # icon = QApplication.style().standardIcon(
        #     QStyle.StandardPixmap.SP_FileDialogContentsView
        # )
        # self._btn_ricerca.setIcon(icon)
        self._btn_ricerca.setObjectName("searchButton")
        self._btn_ricerca.setFixedHeight(self.ricerca_bar.sizeHint().height())

        widget_ricerca = QWidget()
        layout_ricerca = QHBoxLayout(widget_ricerca)
        layout_ricerca.setSpacing(0)
        layout_ricerca.setContentsMargins(0, 0, 0, 0)
        layout_ricerca.addWidget(self.ricerca_bar)
        layout_ricerca.addWidget(self._btn_ricerca)

        layout_header_spettacoli = QHBoxLayout()
        layout_header_spettacoli.addWidget(header_spettacoli)
        layout_header_spettacoli.addWidget(self.__btn_nuovo_spettacolo)
        layout_header_spettacoli.addWidget(widget_ricerca)

        self.layout_lista_spettacoli = QVBoxLayout()

        self.label_lista_spettacoli_vuota = QLabel("Non vi sono spettacoli registrati.")
        self.label_lista_spettacoli_vuota.setObjectName("subheader")
        self.label_lista_spettacoli_vuota.hide()

        container_spettacoli = QWidget()
        layout_spettacoli = QVBoxLayout(container_spettacoli)
        layout_spettacoli.addLayout(layout_header_spettacoli)
        layout_spettacoli.addLayout(self.layout_lista_spettacoli)

        # Scroll layout
        self.scroll_layout.addWidget(container_spettacoli)
        self.scroll_layout.addStretch()

    def _connect_signals(self) -> None:
        self._btn_logout.clicked.connect(  # type:ignore
            self.logoutRequest.emit
        )

        self._btn_sezione_spettacoli.setEnabled(False)

        self._btn_sezione_info.clicked.connect(  # type:ignore
            self.goToInfo.emit
        )

        self._btn_sezione_account.clicked.connect(  # type:ignore
            self.goToAccount.emit
        )

        self.__btn_nuovo_spettacolo.clicked.connect(  # type:ignore
            self.nuovoSpettacoloRequest.emit
        )

        self._btn_ricerca.clicked.connect(  # type:ignore
            lambda: self.filtra_spettacoli(self.ricerca_bar.text())
        )

        self.displaySpettacoliRequest.emit(self.layout_lista_spettacoli)

    # ------------------------- METODI DI VIEW -------------------------

    def filtra_spettacoli(self, filtro: str) -> None:
        self.filtro_ricerca = filtro
        self.aggiorna_pagina()

    def if_lista_vuota(self, layout: QVBoxLayout) -> None:
        """Indica che la lista non ha istanze da visualizzare.

        :param layout: layout dove si mostrerà un messaggio indicando l'assenza di intanze
        """
        # Il suo funzionamento dipende di come aggiorna_pagina aggiunge il label di errore nei layout.
        lista_vuota_error = layout.itemAt(0).widget()  # type:QLabel # type:ignore
        lista_vuota_error.show()

    @override
    def aggiorna_pagina(self) -> None:
        self.svuota_layout(self.layout_lista_spettacoli)
        self.layout_lista_spettacoli.addWidget(self.label_lista_spettacoli_vuota)
        self.label_lista_spettacoli_vuota.hide()
        self.displaySpettacoliRequest.emit(self.layout_lista_spettacoli)

        vertical_scroll = self._scroll_area.verticalScrollBar()
        if not vertical_scroll:
            return
        vertical_scroll.setValue(0)
