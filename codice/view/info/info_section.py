from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
)
from PyQt6.QtCore import Qt, pyqtSignal

from view.abstractView.sectionAbstract import AbstractSectionView

# - Se l'app, in teoria, vendrà usata in un schermo tattile dai cliente, sarà comodo scambiare
#   alcuni .clicked per .pressed


class InfoSectionView(AbstractSectionView):
    """
    View della sezione Info dell'app.

    Segnali:
    - request_display_opere(QVBoxLayout): emesso per caricare la lista delle opere nella sezione Info;
    - request_display_generi(QVBoxLayout): emesso per caricare la lista dei generi nella sezione Info.
    """

    request_display_opere = pyqtSignal(QVBoxLayout)
    request_display_generi = pyqtSignal(QVBoxLayout)

    def __init__(self) -> None:
        super().__init__()

        self._setup_ui()

    def _setup_ui(self) -> None:
        # Opere
        header_opere = QLabel("Opere")
        header_opere.setObjectName("Header1")
        header_opere.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.btn_nuova_opera = QPushButton("Nuova opera")
        self.btn_nuova_opera.setObjectName("SmallButton")

        self.ricerca_bar = QLineEdit()
        self.ricerca_bar.setPlaceholderText("Inserire nome...")
        self.ricerca_bar.setClearButtonEnabled(True)
        # - Dovrebbe includere un pulsante per iniziare la ricerca
        # - Manca request_ricerca_opera = pyqtSignal(str) per farla funzionale

        layout_header_opere = QHBoxLayout()
        layout_header_opere.addWidget(header_opere)
        layout_header_opere.addWidget(self.btn_nuova_opera)
        layout_header_opere.addWidget(self.ricerca_bar)

        self.layout_lista_opere = QVBoxLayout()

        self.label_lista_opere_vuota = QLabel("Non vi sono opere disponibili.")
        self.label_lista_opere_vuota.setObjectName("SubHeader")
        self.label_lista_opere_vuota.hide()

        self.request_display_opere.emit(self.layout_lista_opere)

        container_opere = QWidget()
        layout_opere = QVBoxLayout(container_opere)
        layout_opere.addLayout(layout_header_opere)
        layout_opere.addLayout(self.layout_lista_opere)

        # Generi
        header_generi = QLabel("Generi")
        header_generi.setObjectName("Header1")
        header_generi.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.btn_nuovo_genere = QPushButton("Nuovo genere")
        self.btn_nuovo_genere.setObjectName("SmallButton")

        layout_header_generi = QHBoxLayout()
        layout_header_generi.addWidget(header_generi)
        layout_header_generi.addWidget(self.btn_nuovo_genere)
        layout_header_generi.addStretch()

        self.layout_lista_generi = QVBoxLayout()

        self.label_lista_generi_vuota = QLabel("Non vi sono generi disponibili.")
        self.label_lista_generi_vuota.setObjectName("SubHeader")
        self.label_lista_generi_vuota.hide()

        self.request_display_generi.emit(self.layout_lista_generi)

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
            "Inaugurato nel 1996\nVia R. Ripa, 1\nLa Vitrifrigo Arena è un'ampio palazzetto che ospita numerosi eventi sportivi e musicali di rilevanza mondiale. In occasione dello Rossini Opera Festival, viene allestita una struttura in legno al suo interno per ricreare l'esperienza acustica di un teatro tradizionale."
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

    def refresh_page(self) -> None:
        self.clear_layout(self.layout_lista_opere)
        self.layout_lista_opere.addWidget(self.label_lista_opere_vuota)
        self.label_lista_opere_vuota.hide()
        self.request_display_opere.emit(self.layout_lista_opere)

        self.clear_layout(self.layout_lista_generi)
        self.layout_lista_generi.addWidget(self.label_lista_generi_vuota)
        self.label_lista_generi_vuota.hide()
        self.request_display_generi.emit(self.layout_lista_generi)
