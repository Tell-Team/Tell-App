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

from view.utils import ListLayout, EmptyStateLabel
from view.style import QssStyle


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
        header_opere.setProperty(QssStyle.HEADER1.style_role, True)
        header_opere.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self._btn_nuova_opera = QPushButton("Nuova opera")
        self._btn_nuova_opera.setProperty(QssStyle.WHITE_BUTTON.style_role, True)

        self.filtro_ricerca: str = ""

        self.ricerca_bar = QLineEdit()
        self.ricerca_bar.setPlaceholderText("Inserire nome...")
        self.ricerca_bar.setClearButtonEnabled(True)
        self.ricerca_bar.setProperty(QssStyle.SEARCH_BAR.style_role, True)

        self._btn_ricerca = QPushButton()
        # icon = QApplication.style().standardIcon(
        #     QStyle.StandardPixmap.SP_FileDialogContentsView
        # )
        # self._btn_ricerca.setIcon(icon)
        self._btn_ricerca.setProperty(QssStyle.SEARCH_BUTTON.style_role, True)
        self._btn_ricerca.setProperty(QssStyle.BLUE_BUTTON.style_role, True)
        self._btn_ricerca.setFixedHeight(self.ricerca_bar.sizeHint().height())

        widget_ricerca = QWidget()
        layout_ricerca = QHBoxLayout(widget_ricerca)
        layout_ricerca.setSpacing(0)
        layout_ricerca.setContentsMargins(0, 0, 0, 0)
        layout_ricerca.addWidget(self.ricerca_bar)
        layout_ricerca.addWidget(self._btn_ricerca)

        widget_header_opere = QWidget()
        layout_header_opere = QHBoxLayout(widget_header_opere)
        layout_header_opere.setContentsMargins(0, 0, 0, 0)
        layout_header_opere.addWidget(header_opere)
        layout_header_opere.addWidget(self._btn_nuova_opera)
        layout_header_opere.addWidget(widget_ricerca)

        # Non è necessario salvare questo label come attributo perché il suo funzionamento
        #   viene gestito dal ListLayout a cui viene collegato.
        label_lista_opere_vuota = EmptyStateLabel("Non vi sono opere disponibili.")
        label_lista_opere_vuota.setProperty(QssStyle.SECONDARY_TEXT.style_role, True)

        widget_lista_opere = QWidget()
        self.layout_lista_opere = ListLayout(
            widget_lista_opere, label_lista_opere_vuota
        )

        container_opere = QWidget()
        layout_opere = QVBoxLayout(container_opere)
        layout_opere.addWidget(widget_header_opere)
        layout_opere.addWidget(widget_lista_opere)

        # Generi
        header_generi = QLabel("Generi")
        header_generi.setProperty(QssStyle.HEADER1.style_role, True)
        header_generi.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self._btn_nuovo_genere = QPushButton("Nuovo genere")
        self._btn_nuovo_genere.setProperty(QssStyle.WHITE_BUTTON.style_role, True)

        widget_header_generi = QWidget()
        layout_header_generi = QHBoxLayout(widget_header_generi)
        layout_header_generi.setContentsMargins(0, 0, 0, 0)
        layout_header_generi.addWidget(header_generi)
        layout_header_generi.addWidget(self._btn_nuovo_genere)
        layout_header_generi.addStretch()

        label_lista_generi_vuota = EmptyStateLabel("Non vi sono generi disponibili.")
        label_lista_generi_vuota.setProperty(QssStyle.SECONDARY_TEXT.style_role, True)

        widget_lista_generi = QWidget()
        self.layout_lista_generi = ListLayout(
            widget_lista_generi, label_lista_generi_vuota
        )

        container_generi = QWidget()
        layout_generi = QVBoxLayout(container_generi)
        layout_generi.addWidget(widget_header_generi)
        layout_generi.addWidget(widget_lista_generi)

        # Teatro
        header_teatro = QLabel("Teatro")
        header_teatro.setProperty(QssStyle.HEADER1.style_role, True)
        header_teatro.setAlignment(Qt.AlignmentFlag.AlignLeft)

        teatro_nome = QLabel("Vitrifrigo Arena")
        teatro_nome.setProperty(QssStyle.HEADER2.style_role, True)

        teatro_desc = QLabel(
            "Inaugurato nel 1996\nVia R. Ripa, 1\nLa Vitrifrigo Arena è un'ampio "
            + "palazzetto che ospita numerosi eventi sportivi e musicali di "
            + "rilevanza mondiale. In occasione dello Rossini Opera Festival, "
            + "viene allestita una struttura in legno al suo interno per ricreare "
            + "l'esperienza acustica di un teatro tradizionale."
        )
        teatro_desc.setProperty(QssStyle.PARAGRAPH.style_role, True)
        teatro_desc.setWordWrap(True)

        info_teatro = QWidget()
        info_teatro.setProperty(QssStyle.ITEM_CARD.style_role, True)
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
        self.layout_lista_opere.svuota_layout()
        self.displayOpereRequest.emit(self.layout_lista_opere)

        self.layout_lista_generi.svuota_layout()
        self.displayGeneriRequest.emit(self.layout_lista_generi)

        vertical_scroll = self._scroll_area.verticalScrollBar()
        if not vertical_scroll:
            return
        vertical_scroll.setValue(0)
