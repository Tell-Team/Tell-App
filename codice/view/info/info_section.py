from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QLayout,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Optional

from view.abstractView.sectionAbstract import AbstractSectionView


# - Se l'app, in teoria, vendrà usara in un schermo tattile dai cliente, sarà comoda scambiare
#   alcuni .clicked per .pressed


class InfoSectionView(AbstractSectionView):
    """
    Pagina principale della sezione Info dell'applicazione. Contiene l'interfaccia utente per
    interaggire con le istanze di `Opera` e `Genere` e una sezione in fondo con le informazioni
    del teatro.
    """

    request_display_opere = pyqtSignal(QVBoxLayout)
    request_display_generi = pyqtSignal(QVBoxLayout)

    def __init__(self):
        super().__init__()

        self._build_ui()

    def _build_ui(self):
        # Opere
        header_opere = QLabel("Opere")
        header_opere.setObjectName("Header1")
        header_opere.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.btn_nuova_opera = QPushButton("Nuova opera")
        self.btn_nuova_opera.setObjectName("SmallButton")

        layout_header_opere = QHBoxLayout()
        layout_header_opere.addWidget(header_opere)
        layout_header_opere.addWidget(self.btn_nuova_opera)
        layout_header_opere.addStretch()

        self.layout_lista_opere = QVBoxLayout()
        self.request_display_opere.emit(self.layout_lista_opere)

        container_opere = QWidget()
        layout_opere = QVBoxLayout(container_opere)
        layout_opere.addLayout(layout_header_opere)
        layout_opere.addLayout(self.layout_lista_opere)

        #
        #
        #

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
        self.request_display_generi.emit(self.layout_lista_generi)

        container_generi = QWidget()
        layout_generi = QVBoxLayout(container_generi)
        layout_generi.addLayout(layout_header_generi)
        layout_generi.addLayout(self.layout_lista_generi)

        #
        #
        #

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

        #
        #
        #

        # Scroll layout
        self.scroll_layout.addWidget(container_opere)
        self.scroll_layout.addWidget(container_generi)
        self.scroll_layout.addWidget(container_teatro)

    def refresh_page(self):
        self.clear_layout(self.layout_lista_opere)
        self.request_display_opere.emit(self.layout_lista_opere)

        self.clear_layout(self.layout_lista_generi)
        self.request_display_generi.emit(self.layout_lista_generi)

    def clear_layout(self, layout: Optional[QLayout]):
        if layout:
            while layout.count():
                item = layout.takeAt(0)
                assert item is not None
                widget = item.widget()

                if widget:
                    widget.setParent(None)
                else:
                    child_layout = item.layout()
                    if child_layout:
                        self.clear_layout(child_layout)
