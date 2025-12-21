from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QSpinBox,
    QPushButton,
    QLayout,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtCore import pyqtSignal, QDate
from functools import partial
from typing import Optional, override

from model.pianificazione.opera import Opera

from view.abstractView.creaAbstract import CreaAbstractView


# - Questa classe sarà una sottoclasse di un NuovoSpettacoloView o sarà una pagina
#   dedicata per le regie?
class NuovaRegiaView(CreaAbstractView):
    """View per la creazione di una nuova regia.

    Segnali:
    - displayInterpreti(CreaAbstractView): emesso per mostrare la lista interpreti a schermo;
    - displayTecnici(CreaAbstractView): emesso per mostrare la lista tecnici a schermo
    - aggiungiInterprete(CreaAbstractView, str, str): emesso quando si clicca il pulsante
    Aggiungi degli interpreti;
    - aggiungiTecnico(CreaAbstractView, str, str): emesso quando si clicca il pulsante Aggiungi
    dei tecnici;
    - annullaRequest(CreaAbstractView): emesso quando si clicca il pulsante Annulla;
    - salvaRequest(): emesso quando si clicca il pulsante Conferma.
    """

    displayInterpreti = pyqtSignal(CreaAbstractView)
    displayTecnici = pyqtSignal(CreaAbstractView)
    aggiungiInterprete = pyqtSignal(CreaAbstractView, str, str)
    aggiungiTecnico = pyqtSignal(CreaAbstractView, str, str)
    annullaRequest = pyqtSignal(CreaAbstractView)
    salvaRequest = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

        self._setup_ui()
        self._connect_signals()

    # ------------------------- SETUP INIT -------------------------

    def _setup_ui(self) -> None:
        # Header
        self.header.setText("Aggiungi nuova regia")

        # Form
        self._setup_form()

        # Layout
        self.main_layout.addWidget(self.header)
        self.main_layout.addWidget(self._scroll_area)
        self.main_layout.addWidget(self.input_error)
        self.main_layout.addWidget(self.pulsanti)

    @override
    def _setup_form(self) -> None:
        label_titolo = QLabel('Titolo<span style="color:red;">*</span> :')
        label_titolo.setObjectName("SubHeader")
        self.titolo = QLineEdit()
        self.titolo.setPlaceholderText("Inserire titolo")

        label_note = QLabel('Note<span style="color:red;">*</span> :')
        label_note.setObjectName("SubHeader")
        self.note = QTextEdit()
        self.note.setPlaceholderText("Inserire note")
        self.note.setFixedHeight(80)

        # Lista interpreti
        label_interprete = QLabel("Interprete :")
        label_interprete.setObjectName("SubHeader")
        self.interprete_nome = QLineEdit()
        self.interprete_nome.setPlaceholderText("Inserire nome")
        self.interprete_ruolo = QLineEdit()
        self.interprete_ruolo.setPlaceholderText("Inserire ruolo")

        self.__btn_aggiungi_interprete = QPushButton("Aggiungi")
        self.__btn_aggiungi_interprete.setObjectName("WhiteButton")

        interprete = QWidget()
        layout_interprete = QHBoxLayout(interprete)
        layout_interprete.addWidget(self.interprete_nome)
        layout_interprete.addWidget(self.interprete_ruolo)
        layout_interprete.addWidget(self.__btn_aggiungi_interprete)

        self.lista_interpreti: dict[str, str] = {}

        self.label_lista_interpreti_error = QLabel("")
        self.label_lista_interpreti_error.setObjectName("SubHeader")
        self.label_lista_interpreti_error.setStyleSheet(
            self.label_lista_interpreti_error.styleSheet()
            + "#SubHeader { color:#c3423f; }"
        )

        widget_lista_interpreti = QWidget()
        self.layout_lista_interpreti = QVBoxLayout(widget_lista_interpreti)
        self.layout_lista_interpreti.setContentsMargins(0, 0, 0, 0)

        # Lista tectici
        label_tecnico = QLabel("Tecnico :")
        label_tecnico.setObjectName("SubHeader")
        self.tecnico_nome = QLineEdit()
        self.tecnico_nome.setPlaceholderText("Inserire nome")
        self.tecnico_posto = QLineEdit()
        self.tecnico_posto.setPlaceholderText("Inserire posto")

        self.__btn_aggiungi_tecnico = QPushButton("Aggiungi")
        self.__btn_aggiungi_tecnico.setObjectName("WhiteButton")

        tecnico = QWidget()
        layout_tecnico = QHBoxLayout(tecnico)
        layout_tecnico.addWidget(self.tecnico_nome)
        layout_tecnico.addWidget(self.tecnico_posto)
        layout_tecnico.addWidget(self.__btn_aggiungi_tecnico)

        self.lista_tecnici: dict[str, str] = {}

        self.label_lista_tecnici_error = QLabel("")
        self.label_lista_tecnici_error.setObjectName("SubHeader")
        self.label_lista_tecnici_error.setStyleSheet(
            self.label_lista_tecnici_error.styleSheet()
            + "#SubHeader { color:#c3423f; }"
        )

        widget_lista_tecnici = QWidget()
        self.layout_lista_tecnici = QVBoxLayout(widget_lista_tecnici)
        self.layout_lista_tecnici.setContentsMargins(0, 0, 0, 0)

        label_regista = QLabel('Regista<span style="color:red;">*</span> :')
        label_regista.setObjectName("SubHeader")
        self.regista = QLineEdit()
        self.regista.setPlaceholderText("Inserire regista")

        label_anno = QLabel('Anno di produzione<span style="color:red;">*</span> :')
        label_anno.setObjectName("SubHeader")
        self.anno = QSpinBox()
        self.anno.setRange(1597, QDate().currentDate().year())
        # - Serve un rango in particolare?

        label_opera = QLabel('Opera<span style="color:red;">*</span> :')
        label_opera.setObjectName("SubHeader")
        self.opera = QComboBox()
        self.opera.setEnabled(False)
        # - Non so se questa pagina sarà esclusiva della sezione Info

        self.form_layout.addRow(label_titolo, self.titolo)
        self.form_layout.addRow(label_note, self.note)
        self.form_layout.addRow(label_interprete, interprete)
        self.form_layout.addRow(
            self.label_lista_interpreti_error, widget_lista_interpreti
        )
        self.form_layout.addRow(label_tecnico, tecnico)
        self.form_layout.addRow(self.label_lista_tecnici_error, widget_lista_tecnici)
        self.form_layout.addRow(label_regista, self.regista)
        self.form_layout.addRow(label_anno, self.anno)
        self.form_layout.addRow(label_opera, self.opera)

    def _connect_signals(self) -> None:
        self.__btn_aggiungi_interprete.clicked.connect(  # type:ignore
            lambda: self.aggiungiInterprete.emit(
                self,
                self.interprete_nome.text().strip(),
                self.interprete_ruolo.text().strip(),
            )
        )

        self.__btn_aggiungi_tecnico.clicked.connect(  # type:ignore
            lambda: self.aggiungiTecnico.emit(
                self,
                self.tecnico_nome.text().strip(),
                self.tecnico_posto.text().strip(),
            )
        )

        self._btn_annulla.clicked.connect(  # type:ignore
            partial(self.annullaRequest.emit, self)
        )

        self._btn_conferma.clicked.connect(  # type:ignore
            self.salvaRequest.emit
        )

        self.displayInterpreti.emit(self)

        self.displayTecnici.emit(self)

    # ------------------------- METODI DI VIEW -------------------------

    def setup_opera_combobox(self, o: Opera) -> None:
        """Riempisce il `QComboBox` de opere (con solo l'opera indicata)."""
        # - Solo inserisce l'opera da dove si chiama il Crea/Modifica Regia
        self.opera.clear()

        self.opera.insertItem(0, "Scegliere genere...", -1)
        self.opera.insertItem(1, o.get_nome(), o.get_id())
        # - Se questa pagina sarà usata anche dalla sezione Spettacoli, devo carica tutte le opere
        #   nel QComboBox e abilitarlo.

    @override
    def reset_pagina(self) -> None:
        """Reset della pagina allo stato default (con solo l'opera scelta)."""
        self.titolo.setText("")
        self.note.setText("")
        self.lista_interpreti = {}
        self.lista_tecnici = {}
        self.regista.setText("")
        self.anno.setValue(QDate().currentDate().year())
        self.opera.setCurrentIndex(1)
        self.input_error.setText("")

    def aggiungi_widget_a_layout(self, widget: QWidget, layout: QVBoxLayout):
        """Aggiunge un widget creato per il display del personale della regia (interpreti e tecnici).

        :param widget: widget speciale per visualizzare un membro del personale
        :param layout: layout dove sarà inserito il widget"""
        layout.addWidget(widget)

    def aggiorna_pagina(self) -> None:
        """Permette di aggiornare la pagina e visualizzare modifiche previamente non mostrate."""
        self.interprete_nome.setText("")
        self.interprete_ruolo.setText("")
        self.svuota_layout(self.layout_lista_interpreti)
        self.label_lista_interpreti_error.setText("")
        self.displayInterpreti.emit(self)

        self.tecnico_nome.setText("")
        self.tecnico_posto.setText("")
        self.svuota_layout(self.layout_lista_tecnici)
        self.label_lista_tecnici_error.setText("")
        self.displayTecnici.emit(self)

    def svuota_layout(self, layout: Optional[QLayout]) -> None:
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
                    self.svuota_layout(child_layout)
