from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import override

from view.abstractView.sectionAbstract import AbstractSectionView

# - Se l'app, in teoria, vendrà usata in un schermo tattile dai cliente, sarà comodo scambiare
#   alcuni .clicked per .pressed


class InfoSectionView(AbstractSectionView):
    """
    View della sezione Info dell'app.

    Segnali:
    - logoutRequest(): emesso quando si clicca il pulsante Logout;
    - goToSpettacoli(): emesso quando si clicca il pulsante Spettacoli;
    - goToAccount(): emesso quando si clicca il pulsante Account;
    - nuovaOperaRequest(): emesso quando si clicca il pulsante Nuova opera;
    - nuovoGenereRequest(): emesso quando si clicca il pulsante Nuovo genere;
    - displayOpereRequest(QVBoxLayout): emesso per caricare la lista delle opere nella sezione Info;
    - displayGeneriRequest(QVBoxLayout): emesso per caricare la lista dei generi nella sezione Info.
    """

    logoutRequest = pyqtSignal()
    goToSpettacoli = pyqtSignal()
    goToAccount = pyqtSignal()

    nuovaOperaRequest = pyqtSignal()
    nuovoGenereRequest = pyqtSignal()
    displayOpereRequest = pyqtSignal(QVBoxLayout)
    displayGeneriRequest = pyqtSignal(QVBoxLayout)

    def __init__(self) -> None:
        super().__init__()

        self._setup_ui()
        self._connect_signals()

    # ------------------------- SETUP INIT -------------------------

    def _setup_ui(self) -> None:
        # Opere
        header_opere = QLabel("Opere")
        header_opere.setObjectName("Header1")
        header_opere.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self._btn_nuova_opera = QPushButton("Nuova opera")
        self._btn_nuova_opera.setObjectName("SmallButton")

        self.ricerca_bar = QLineEdit()
        self.ricerca_bar.setPlaceholderText("Inserire nome...")
        self.ricerca_bar.setClearButtonEnabled(True)
        # - Dovrebbe includere un pulsante per iniziare la ricerca
        # - Manca ricercaOperaRequest = pyqtSignal(str) per farla funzionale

        layout_header_opere = QHBoxLayout()
        layout_header_opere.addWidget(header_opere)
        layout_header_opere.addWidget(self._btn_nuova_opera)
        layout_header_opere.addWidget(self.ricerca_bar)

        self.layout_lista_opere = QVBoxLayout()

        self.label_lista_opere_vuota = QLabel("Non vi sono opere disponibili.")
        self.label_lista_opere_vuota.setObjectName("SubHeader")
        self.label_lista_opere_vuota.hide()

        container_opere = QWidget()
        layout_opere = QVBoxLayout(container_opere)
        layout_opere.addLayout(layout_header_opere)
        layout_opere.addLayout(self.layout_lista_opere)

        # Generi
        header_generi = QLabel("Generi")
        header_generi.setObjectName("Header1")
        header_generi.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self._btn_nuovo_genere = QPushButton("Nuovo genere")
        self._btn_nuovo_genere.setObjectName("SmallButton")

        layout_header_generi = QHBoxLayout()
        layout_header_generi.addWidget(header_generi)
        layout_header_generi.addWidget(self._btn_nuovo_genere)
        layout_header_generi.addStretch()

        self.layout_lista_generi = QVBoxLayout()

        self.label_lista_generi_vuota = QLabel("Non vi sono generi disponibili.")
        self.label_lista_generi_vuota.setObjectName("SubHeader")
        self.label_lista_generi_vuota.hide()

        container_generi = QWidget()
        layout_generi = QVBoxLayout(container_generi)
        layout_generi.addLayout(layout_header_generi)
        layout_generi.addLayout(self.layout_lista_generi)

        # Teatro
        header_teatro = QLabel("Teatro")
        header_teatro.setObjectName("Header1")
        header_teatro.setAlignment(Qt.AlignmentFlag.AlignLeft)

        teatro_nome = QLabel("Vitrifrigo Arena")
        teatro_nome.setObjectName("Header2")

        teatro_desc = QLabel(
            "Inaugurato nel 1996\nVia R. Ripa, 1\nLa Vitrifrigo Arena è un'ampio "
            + "palazzetto che ospita numerosi eventi sportivi e musicali di "
            + "rilevanza mondiale. In occasione dello Rossini Opera Festival, "
            + "viene allestita una struttura in legno al suo interno per ricreare "
            + "l'esperienza acustica di un teatro tradizionale."
        )
        teatro_desc.setObjectName("Paragraph")
        teatro_desc.setWordWrap(True)

        info_teatro = QWidget()
        info_teatro.setObjectName("Container")
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

    def _connect_signals(self) -> None:
        self._btn_logout.clicked.connect(  # type:ignore
            self.logoutRequest.emit
        )

        self._btn_sezione_spettacoli.clicked.connect(  # type:ignore
            self.goToSpettacoli.emit
        )

        self._btn_sezione_info.setEnabled(False)

        self._btn_sezione_account.clicked.connect(  # type:ignore
            self.goToAccount.emit
        )

        self._btn_nuova_opera.clicked.connect(  # type:ignore
            self.nuovaOperaRequest.emit
        )

        self._btn_nuovo_genere.clicked.connect(  # type:ignore
            self.nuovoGenereRequest.emit
        )

        self.displayOpereRequest.emit(self.layout_lista_opere)

        self.displayGeneriRequest.emit(self.layout_lista_generi)

    # ------------------------- METODI DI VIEW -------------------------

    def if_lista_vuota(self, layout: QVBoxLayout) -> None:
        """Indica che la lista non ha istanze da visualizzare.

        :param layout: layout dove si mostrerà un messaggio indicando l'assenza di intanze
        """
        # Il suo funzionamento dipende di come refresh_page aggiunge il label di errore nei layout.
        lista_vuota_error = layout.itemAt(0).widget()  # type:QLabel # type:ignore
        lista_vuota_error.show()

    @override
    def refresh_page(self) -> None:
        self.clear_layout(self.layout_lista_opere)
        self.layout_lista_opere.addWidget(self.label_lista_opere_vuota)
        self.label_lista_opere_vuota.hide()
        self.displayOpereRequest.emit(self.layout_lista_opere)

        self.clear_layout(self.layout_lista_generi)
        self.layout_lista_generi.addWidget(self.label_lista_generi_vuota)
        self.label_lista_generi_vuota.hide()
        self.displayGeneriRequest.emit(self.layout_lista_generi)
