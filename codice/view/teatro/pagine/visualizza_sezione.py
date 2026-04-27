from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QGridLayout,
    QCheckBox,
    QStackedWidget,
)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import override

from core.view import AbstractVisualizzaView

from model.organizzazione.posto import Posto

from view.teatro.utils import SezioneData

from view.utils.list_widgets import ListLayout, EmptyStateLabel
from view.utils.hyphenate_text import HyphenatedLabel
from view.utils.custom_button import SalvaButton
from view.utils.fixed_size_widget import FixedSizeLineEdit, FixedSizeSpinBox
from view.utils import make_vline

from view.style.ui_style import WidgetRole, WidgetColor


class VisualizzaSezionePage(AbstractVisualizzaView):
    """Pagina per visualizzare una signola `Sezione` in dettaglio.

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
        self.label_nome.setProperty(WidgetRole.Label.HEADER1, True)
        self.label_nome.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.label_descrizione = HyphenatedLabel("[Descrizione Sezione]")
        self.label_descrizione.setProperty(WidgetRole.Label.BODY_TEXT, True)
        self.label_descrizione.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Crea posto/i widget
        self.lista_posti: list[Posto] = []

        label_crea_posto_box = QLabel("Aggiungi posto:")
        label_crea_posto_box.setProperty(WidgetRole.Label.HEADER2, True)

        label_fila = QLabel('Fila<span style="color:red;">*</span> :')
        label_fila.setProperty(WidgetRole.Label.BODY_TEXT, True)
        label_fila.setProperty(WidgetColor.Label.SECONDARY_COLOR, True)

        self.fila = FixedSizeLineEdit(width=230)
        self.fila.setPlaceholderText("Inserire nome")

        fila_box = QWidget()
        layout_fila_box = QHBoxLayout(fila_box)
        layout_fila_box.setContentsMargins(0, 0, 0, 0)
        layout_fila_box.addWidget(label_fila)
        layout_fila_box.addWidget(self.fila)
        layout_fila_box.addStretch()

        self.__label_numero = QLabel('Numero<span style="color:red;">*</span> :')
        self.__label_numero.setProperty(WidgetRole.Label.BODY_TEXT, True)
        self.__label_numero.setProperty(WidgetColor.Label.SECONDARY_COLOR, True)
        self.__label_numero.setMinimumWidth(self.__label_numero.sizeHint().width())

        self.single_numero = FixedSizeSpinBox(width=100)
        self.single_numero.setMinimum(1)

        self.range_numero1 = FixedSizeSpinBox(width=100)
        self.range_numero1.setMinimum(1)

        hyphen_label = QLabel("-")
        hyphen_label.setProperty(WidgetRole.Label.BODY_TEXT, True)

        self.range_numero2 = FixedSizeSpinBox(width=100)
        self.range_numero2.setMinimum(1)

        range_numeri_widget = QWidget()
        layout_range_numeri = QHBoxLayout(range_numeri_widget)
        layout_range_numeri.setContentsMargins(1, 1, 5, 1)
        layout_range_numeri.addWidget(self.range_numero1)
        layout_range_numeri.addWidget(hyphen_label)
        layout_range_numeri.addWidget(self.range_numero2)
        layout_range_numeri.addStretch()

        self.stack_numeri = QStackedWidget()
        self.stack_numeri.setFixedHeight(self.fila.sizeHint().height())
        self.stack_numeri.addWidget(self.single_numero)
        self.stack_numeri.addWidget(range_numeri_widget)

        numeri_box = QWidget()
        layout_numeri_box = QHBoxLayout(numeri_box)
        layout_numeri_box.setContentsMargins(5, 1, 1, 1)
        layout_numeri_box.addWidget(self.__label_numero)
        layout_numeri_box.addWidget(self.stack_numeri)

        fila_numeri = QWidget()
        tmp_layout = QHBoxLayout(fila_numeri)
        tmp_layout.setContentsMargins(0, 0, 0, 0)
        tmp_layout.addWidget(fila_box)
        tmp_layout.addWidget(numeri_box)

        #   Checkbox + Label
        self.checkbox_numeri = QCheckBox()
        label_range_numeri = QLabel("Inserire range di numeri")
        label_range_numeri.setProperty(WidgetRole.Label.BODY_TEXT, True)
        checkbox_numeri_widget = QWidget()
        layout_checkbox_widget = QHBoxLayout(checkbox_numeri_widget)
        layout_checkbox_widget.setContentsMargins(0, 0, 0, 1)
        layout_checkbox_widget.addWidget(self.checkbox_numeri)
        layout_checkbox_widget.addWidget(label_range_numeri)
        layout_checkbox_widget.addStretch()

        #   Btn aggiungi
        self.__btn_aggiungi_posto = SalvaButton("Aggiungi", has_icon=False)
        aggiungi_box = QWidget()
        layout_aggiungi_box = QVBoxLayout(aggiungi_box)
        layout_aggiungi_box.setContentsMargins(0, 0, 0, 0)
        layout_aggiungi_box.addWidget(
            self.__btn_aggiungi_posto, alignment=Qt.AlignmentFlag.AlignLeft
        )

        crea_posto_fields = QWidget()
        layout_crea_posto_fields = QFormLayout(crea_posto_fields)
        layout_crea_posto_fields.addRow(fila_numeri)
        layout_crea_posto_fields.addWidget(checkbox_numeri_widget)
        layout_crea_posto_fields.addRow(aggiungi_box)

        self.__input_error = QLabel("")
        self.__input_error.setProperty(WidgetRole.Label.BODY_TEXT, True)
        self.__input_error.setProperty(WidgetColor.Label.ERROR_COLOR, True)

        crea_posto_box = QWidget()
        crea_posto_box.setProperty(WidgetRole.Item.CARD, True)
        layout_crea_posto_box = QVBoxLayout(crea_posto_box)
        layout_crea_posto_box.addWidget(label_crea_posto_box)
        layout_crea_posto_box.addWidget(crea_posto_fields)
        layout_crea_posto_box.addWidget(self.__input_error)
        layout_crea_posto_box.addStretch()

        # Lista posti
        label_lista_posti = QLabel("Lista posti")
        label_lista_posti.setProperty(WidgetRole.Label.HEADER2, True)

        label_lista_posti_vuota = EmptyStateLabel(
            "Al momento, non vi sono posti assegnati alla sezione."
        )
        label_lista_posti_vuota.setProperty(WidgetRole.Label.BODY_TEXT, True)
        label_lista_posti_vuota.setProperty(WidgetColor.Label.SECONDARY_COLOR, True)

        content_lista_posti = QWidget()
        content_lista_posti.setProperty(WidgetRole.Item.LIST, True)
        self.layout_lista_posti = ListLayout(
            content_lista_posti, label_lista_posti_vuota
        )

        header_numero = QLabel("Fila | Numero")
        header_numero.setProperty(WidgetRole.Label.HEADER3, True)
        header_opzioni = QLabel("Opzioni")
        header_opzioni.setProperty(WidgetRole.Label.HEADER3, True)

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
        self._layout_content.addStretch(0)
        self._layout_content.addSpacing(20)
        self._layout_content.addWidget(label_lista_posti)
        self._layout_content.addWidget(self.posti)
        self._layout_content.addStretch(1)

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
            lambda: self.opzione_checkbox_numeri(self.checkbox_numeri.isChecked())
        )

        self.__btn_aggiungi_posto.clicked.connect(  # type:ignore
            lambda: self.aggiungiPostoRequest.emit(
                bool(not self.checkbox_numeri.isChecked())
            )
        )

    # ------------------------- METODI DI VIEW -------------------------

    def opzione_checkbox_numeri(self, is_checked: bool) -> None:
        self.stack_numeri.setCurrentIndex(is_checked)
        self.__label_numero.setText(
            'Range<span style="color:red;">*</span> :'
            if is_checked
            else 'Numero<span style="color:red;">*</span> :'
        )

    @override
    def set_data(self, data: SezioneData) -> None:  # type: ignore[override]
        """Carica i dati della sezione nella pagina.

        :param data: data salvata in una classe immutabile"""
        # Reset layout lista posti
        self.layout_lista_posti.svuota_layout()
        self.__input_error.setText("")

        # Salva dati della sezione nella pagina
        self.id_current_sezione = data.id

        # Carica dati della sezione
        self.label_nome.setText(f"{data.nome}")
        self.label_descrizione.setText(f"{data.descrizione}")

    @override
    def aggiorna_pagina(self) -> None:
        super().aggiorna_pagina()

        self.layout_lista_posti.svuota_layout()
        self.displayPostiRequest.emit(self.layout_lista_posti)

    def reset_pagina(self) -> None:
        """Resetta la pagina svuotando i campi d'input per creare posti."""
        self.fila.setText("")
        self.single_numero.setValue(1)
        self.range_numero1.setValue(1)
        self.range_numero2.setValue(1)
        self.checkbox_numeri.setChecked(False)

    def mostra_msg_input_error(self, message: str) -> None:
        """Aggiorna il testo della label `input_error`.

        :param message: testo inserito nel label
        """
        self.__input_error.setText(message)
        self.__input_error.show()  # Si assicura che la label sia visualizzata.
