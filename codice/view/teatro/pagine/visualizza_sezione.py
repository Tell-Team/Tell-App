from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLineEdit,
    QSpinBox,
    QCheckBox,
    QStackedWidget,
)
from PyQt6.QtCore import Qt, pyqtSignal, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from typing import override

from core.view import AbstractVisualizzaView

from model.organizzazione.posto import Posto

from view.teatro.utils import SezionePageData

from view.utils.list_widgets import ListLayout, EmptyStateLabel
from view.utils.hyphenate_text import HyphenatedLabel
from view.utils.custom_button import SalvaButton
from view.utils import make_vline

from view.style.ui_style import WidgetRole, WidgetColor


class VisualizzaSezioneView(AbstractVisualizzaView):
    """Pagina per visualizzare le signole `Sezione` in dettaglio.

    Contiene le tutte informazioni della `Sezione` ed una lista con tutti i `Posto`
    associati ad essa.

    Segnali
    ---
    - `displayPostiRequest(ListLayout)`: emesso per mostrare a schermo la lista eventi;
    - `aggiungiPostoRequest(bool)`: emesso quando si clicca il pulsante Aggiungi.
    """

    displayPostiRequest = pyqtSignal(ListLayout)
    aggiungiPostoRequest = pyqtSignal(bool)

    def __init__(self):
        self.id_current_sezione: int = -1

        super().__init__()

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        # Labels
        self.label_nome = HyphenatedLabel("[Nome Sezione]")
        self.label_nome.setProperty(WidgetRole.HEADER1, True)
        self.label_nome.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.label_descrizione = HyphenatedLabel("[Descrizione Sezione]")
        self.label_descrizione.setProperty(WidgetRole.BODY_TEXT, True)
        self.label_descrizione.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Crea posto/i widget
        self.lista_posti: list[Posto] = []

        label_crea_posto_box = QLabel("Aggiungi posto:")
        label_crea_posto_box.setProperty(WidgetRole.HEADER2, True)

        label_fila = QLabel('Fila<span style="color:red;">*</span> :')
        label_fila.setProperty(WidgetRole.BODY_TEXT, True)
        label_fila.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)

        self.fila = QLineEdit()
        self.fila.setPlaceholderText("Inserire nome")

        label_numero = QLabel('Numero<span style="color:red;">*</span> :')
        label_numero.setProperty(WidgetRole.BODY_TEXT, True)
        label_numero.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)

        self.single_numero = QSpinBox()
        self.single_numero.setMinimum(0)

        self.range_numeri = QLineEdit()
        self.range_numeri.setPlaceholderText("Inserire rango, e.g. 1,4-6,9,11")
        validator_numeri = QRegularExpressionValidator(
            QRegularExpression(r"^\s*\d+(\s*-\s*\d+)?(\s*,\s*\d+(\s*-\s*\d+)?)*\s*$")
        )
        self.range_numeri.setValidator(validator_numeri)

        self.stack_numeri = QStackedWidget()
        self.stack_numeri.setFixedHeight(self.fila.sizeHint().height())
        self.stack_numeri.addWidget(self.single_numero)
        self.stack_numeri.addWidget(self.range_numeri)

        self.checkbox_numeri = QCheckBox()

        self.__btn_aggiungi_posto = SalvaButton("Aggiungi", has_icon=False)

        crea_posto_fields = QWidget()
        layout_crea_posto_fields = QHBoxLayout(crea_posto_fields)
        layout_crea_posto_fields.addWidget(label_fila)
        layout_crea_posto_fields.addWidget(self.fila)
        layout_crea_posto_fields.addWidget(label_numero)
        layout_crea_posto_fields.addWidget(self.stack_numeri)
        layout_crea_posto_fields.addWidget(self.checkbox_numeri)
        layout_crea_posto_fields.addWidget(self.__btn_aggiungi_posto)

        self.__input_error = QLabel("")
        self.__input_error.setProperty(WidgetRole.BODY_TEXT, True)
        self.__input_error.setProperty(WidgetColor.Text.ERROR_MESSAGE, True)

        crea_posto_box = QWidget()
        crea_posto_box.setProperty(WidgetRole.ITEM_CARD, True)
        layout_crea_posto_box = QVBoxLayout(crea_posto_box)
        layout_crea_posto_box.addWidget(label_crea_posto_box)
        layout_crea_posto_box.addWidget(crea_posto_fields)
        layout_crea_posto_box.addWidget(self.__input_error)
        layout_crea_posto_box.addStretch()

        # Lista posti
        label_lista_posti = QLabel("Lista posti")
        label_lista_posti.setProperty(WidgetRole.HEADER2, True)

        label_lista_posti_vuota = EmptyStateLabel(
            "Al momento, non vi sono posti assegnati alla sezione."
        )
        label_lista_posti_vuota.setProperty(WidgetRole.BODY_TEXT, True)
        label_lista_posti_vuota.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)

        content_lista_posti = QWidget()
        content_lista_posti.setProperty(WidgetRole.ITEM_LIST, True)
        self.layout_lista_posti = ListLayout(
            content_lista_posti, label_lista_posti_vuota
        )

        header_numero = QLabel("Fila | Numero")
        header_numero.setProperty(WidgetRole.HEADER3, True)
        header_opzioni = QLabel("Opzioni")
        header_opzioni.setProperty(WidgetRole.HEADER3, True)

        header_lista_posti = QWidget()
        layout_header_lista_posti = QGridLayout(header_lista_posti)
        layout_header_lista_posti.setContentsMargins(1, 1, 1, 1)
        layout_header_lista_posti.addWidget(
            header_numero, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout_header_lista_posti.addWidget(make_vline(), 0, 1)
        layout_header_lista_posti.addWidget(
            header_opzioni, 0, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.posti = QWidget()
        self.layout_posti = QVBoxLayout(self.posti)
        self.layout_posti.addWidget(header_lista_posti)
        self.layout_posti.addWidget(content_lista_posti)

        # Layout
        self._layout_content.addWidget(self.label_nome)
        self._layout_content.addWidget(self.label_descrizione)
        self._layout_content.addSpacing(20)
        self._layout_content.addWidget(crea_posto_box)
        self._layout_content.addSpacing(20)
        self._layout_content.addWidget(label_lista_posti)
        self._layout_content.addWidget(self.posti)
        self._layout_content.addStretch()

    @override
    def _connect_signals(self) -> None:
        super()._connect_signals()

        # La QLineEdit per la fila solo mostra maiuscole
        def to_upper(text: str) -> None:
            self.fila.blockSignals(True)
            self.fila.setText(text.upper())
            self.fila.blockSignals(False)

        self.fila.textChanged.connect(  # type:ignore
            to_upper
        )

        self.checkbox_numeri.toggled.connect(  # type:ignore
            lambda: self.stack_numeri.setCurrentIndex(
                1 if self.checkbox_numeri.isChecked() else 0
            )
        )

        self.__btn_aggiungi_posto.clicked.connect(  # type:ignore
            lambda: self.aggiungiPostoRequest.emit(
                bool(not self.checkbox_numeri.isChecked())
            )
        )

    # ------------------------- METODI DI VIEW -------------------------

    @override
    def set_data(  # type: ignore[override]
        self, data: SezionePageData, lista_posti: list[Posto]
    ) -> None:
        """Carica i dati della sezione nella pagina.

        :param data: data salvata in una classe immutabile
        :param lista_posti: lista dei posti associati alla sezione"""
        # Reset layout lista posti
        self.layout_lista_posti.svuota_layout()
        self.__input_error.setText("")

        # Salva dati della sezione nella pagina
        self.id_current_sezione = data.id
        self.lista_posti = lista_posti

        # Carica dati della sezione
        self.label_nome.setText(f"{data.nome}")
        self.label_descrizione.setText(f"{data.descrizione}")

        # Carica lista posti
        if not self.lista_posti:
            self.layout_lista_posti.mostra_msg_lista_vuota()
        else:
            self.displayPostiRequest.emit(self.layout_lista_posti)

    @override
    def aggiorna_pagina(self) -> None:
        super().aggiorna_pagina()

        self.layout_lista_posti.svuota_layout()
        self.displayPostiRequest.emit(self.layout_lista_posti)

    def reset_pagina(self) -> None:
        """Resetta la pagina svuotando i campi d'input per creare posti."""
        self.fila.setText("")
        self.single_numero.setValue(0)
        self.range_numeri.setText("")
        self.checkbox_numeri.setChecked(False)

    def mostra_msg_input_error(self, message: str) -> None:
        """Aggiorna il testo della label `input_error`.

        :param message: testo inserito nel label
        """
        self.__input_error.setText(message)
        self.__input_error.show()  # Si assicura che la label sia visualizzata.
