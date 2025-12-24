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

from view.abstractView.abstractSectionView import AbstractSectionView
from view.style import QssStyle

# - Se l'app, in teoria, vendrà usata in un schermo tattile dai clienti, sarà comodo scambiare
#   alcuni .clicked per .pressed


class InfoSectionView(AbstractSectionView):
    """View della sezione Info dell'app.

    Segnali:
    - logoutRequest(): emesso quando si clicca il pulsante Logout;
    - goToSpettacoli(): emesso quando si clicca il pulsante Spettacoli;
    - goToAccount(): emesso quando si clicca il pulsante Account;
    - nuovaOperaRequest(): emesso quando si clicca il pulsante Nuova opera;
    - nuovoGenereRequest(): emesso quando si clicca il pulsante Nuovo genere;
    - displayOpereRequest(QVBoxLayout): emesso per caricare la lista delle opere nella sezione Info;
    - displayGeneriRequest(QVBoxLayout): emesso per caricare la lista dei generi nella sezione Info.
    """

    nuovaOperaRequest = pyqtSignal()
    nuovoGenereRequest = pyqtSignal()
    displayOpereRequest = pyqtSignal(QVBoxLayout)
    displayGeneriRequest = pyqtSignal(QVBoxLayout)

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        # Opere
        header_opere = QLabel("Opere")
        header_opere.setObjectName(QssStyle.HEADER1.style_name)
        header_opere.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self._btn_nuova_opera = QPushButton("Nuova opera")
        self._btn_nuova_opera.setObjectName(QssStyle.WHITE_BUTTON.style_name)

        self.filtro_ricerca: str = ""

        self.ricerca_bar = QLineEdit()
        self.ricerca_bar.setPlaceholderText("Inserire nome...")
        self.ricerca_bar.setClearButtonEnabled(True)
        self.ricerca_bar.setObjectName(QssStyle.SEARCH_BAR.style_name)

        self._btn_ricerca = QPushButton()
        # icon = QApplication.style().standardIcon(
        #     QStyle.StandardPixmap.SP_FileDialogContentsView
        # )
        # self._btn_ricerca.setIcon(icon)
        self._btn_ricerca.setObjectName(QssStyle.SEARCH_BUTTON.style_name)
        self._btn_ricerca.setFixedHeight(self.ricerca_bar.sizeHint().height())

        widget_ricerca = QWidget()
        layout_ricerca = QHBoxLayout(widget_ricerca)
        layout_ricerca.setSpacing(0)
        layout_ricerca.setContentsMargins(0, 0, 0, 0)
        layout_ricerca.addWidget(self.ricerca_bar)
        layout_ricerca.addWidget(self._btn_ricerca)

        layout_header_opere = QHBoxLayout()
        layout_header_opere.addWidget(header_opere)
        layout_header_opere.addWidget(self._btn_nuova_opera)
        layout_header_opere.addWidget(widget_ricerca)

        self.layout_lista_opere = QVBoxLayout()

        self.label_lista_opere_vuota = QLabel("Non vi sono opere disponibili.")
        self.label_lista_opere_vuota.setObjectName(QssStyle.SECONDARY_TEXT.style_name)
        self.label_lista_opere_vuota.hide()

        container_opere = QWidget()
        layout_opere = QVBoxLayout(container_opere)
        layout_opere.addLayout(layout_header_opere)
        layout_opere.addLayout(self.layout_lista_opere)

        # Generi
        header_generi = QLabel("Generi")
        header_generi.setObjectName(QssStyle.HEADER1.style_name)
        header_generi.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self._btn_nuovo_genere = QPushButton("Nuovo genere")
        self._btn_nuovo_genere.setObjectName(QssStyle.WHITE_BUTTON.style_name)

        layout_header_generi = QHBoxLayout()
        layout_header_generi.addWidget(header_generi)
        layout_header_generi.addWidget(self._btn_nuovo_genere)
        layout_header_generi.addStretch()

        self.layout_lista_generi = QVBoxLayout()

        self.label_lista_generi_vuota = QLabel("Non vi sono generi disponibili.")
        self.label_lista_generi_vuota.setObjectName(QssStyle.SECONDARY_TEXT.style_name)
        self.label_lista_generi_vuota.hide()

        container_generi = QWidget()
        layout_generi = QVBoxLayout(container_generi)
        layout_generi.addLayout(layout_header_generi)
        layout_generi.addLayout(self.layout_lista_generi)

        # Teatro
        header_teatro = QLabel("Teatro")
        header_teatro.setObjectName(QssStyle.HEADER1.style_name)
        header_teatro.setAlignment(Qt.AlignmentFlag.AlignLeft)

        teatro_nome = QLabel("Vitrifrigo Arena")
        teatro_nome.setObjectName(QssStyle.HEADER2.style_name)

        teatro_desc = QLabel(
            "Inaugurato nel 1996\nVia R. Ripa, 1\nLa Vitrifrigo Arena è un'ampio "
            + "palazzetto che ospita numerosi eventi sportivi e musicali di "
            + "rilevanza mondiale. In occasione dello Rossini Opera Festival, "
            + "viene allestita una struttura in legno al suo interno per ricreare "
            + "l'esperienza acustica di un teatro tradizionale."
        )
        teatro_desc.setObjectName(QssStyle.PARAGRAPH.style_name)
        teatro_desc.setWordWrap(True)

        info_teatro = QWidget()
        info_teatro.setObjectName(QssStyle.ITEM_CARD.style_name)
        layout_info_teatro = QVBoxLayout(info_teatro)
        layout_info_teatro.addWidget(teatro_nome)
        layout_info_teatro.addWidget(teatro_desc)

        container_teatro = QWidget()
        layout_teatro = QVBoxLayout(container_teatro)
        layout_teatro.addWidget(header_teatro)
        layout_teatro.addWidget(info_teatro)

        # Scroll layout
        self.scroll_layout.addWidget(container_opere)
        self.scroll_layout.addWidget(container_generi)
        self.scroll_layout.addWidget(container_teatro)
        self.scroll_layout.addStretch()

    @override
    def _connect_signals(self) -> None:
        super()._connect_signals()

        self._btn_sezione_info.setEnabled(False)

        self._btn_nuova_opera.clicked.connect(  # type:ignore
            self.nuovaOperaRequest.emit
        )

        self._btn_ricerca.clicked.connect(  # type:ignore
            lambda: self.__filtra_opere(self.ricerca_bar.text())
        )

        self._btn_nuovo_genere.clicked.connect(  # type:ignore
            self.nuovoGenereRequest.emit
        )

        self.displayOpereRequest.emit(self.layout_lista_opere)

        self.displayGeneriRequest.emit(self.layout_lista_generi)

    # ------------------------- METODI DI VIEW -------------------------

    def __filtra_opere(self, filtro: str) -> None:
        self.filtro_ricerca = filtro
        self.aggiorna_pagina()

    @override
    def aggiorna_pagina(self) -> None:
        self._svuota_layout(self.layout_lista_opere)
        self.layout_lista_opere.addWidget(self.label_lista_opere_vuota)
        self.label_lista_opere_vuota.hide()
        self.displayOpereRequest.emit(self.layout_lista_opere)

        self._svuota_layout(self.layout_lista_generi)
        self.layout_lista_generi.addWidget(self.label_lista_generi_vuota)
        self.label_lista_generi_vuota.hide()
        self.displayGeneriRequest.emit(self.layout_lista_generi)

        vertical_scroll = self._scroll_area.verticalScrollBar()
        if not vertical_scroll:
            return
        vertical_scroll.setValue(0)
