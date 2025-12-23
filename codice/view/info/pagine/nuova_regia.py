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
from typing import Optional, override

from model.pianificazione.opera import Opera

from view.abstractView.abstractCreaView import AbstractCreaView


# - Questa classe sarà una sottoclasse di un NuovoSpettacoloView o sarà una pagina
#   dedicata per le regie?
class NuovaRegiaView(AbstractCreaView):
    """View per la creazione di una nuova regia.

    Segnali:
    - displayInterpreti(CreaAbstractView): emesso per mostrare la lista interpreti a schermo;
    - displayTecnici(CreaAbstractView): emesso per mostrare la lista tecnici a schermo;
    - aggiungiInterprete(CreaAbstractView, str, str): emesso quando si clicca il pulsante
    Aggiungi degli interpreti;
    - aggiungiTecnico(CreaAbstractView, str, str): emesso quando si clicca il pulsante Aggiungi
    dei tecnici;
    - annullaRequest(QWidget): emesso quando si clicca il pulsante Annulla;
    - salvaRequest(): emesso quando si clicca il pulsante Crea.
    """

    displayInterpreti = pyqtSignal(AbstractCreaView)
    displayTecnici = pyqtSignal(AbstractCreaView)
    aggiungiInterprete = pyqtSignal(AbstractCreaView, str, str)
    aggiungiTecnico = pyqtSignal(AbstractCreaView, str, str)

    def __init__(self) -> None:
        super().__init__()

        self._setup_ui()
        self._connect_signals()

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        # Header
        self._header.setText("Aggiungi nuova regia")

        # Form
        self._setup_form()

        # Layout
        self._main_layout.addWidget(self._header)
        self._main_layout.addWidget(self._scroll_area)
        self._main_layout.addWidget(self._input_error)
        self._main_layout.addWidget(self._pulsanti)

    @override
    def _setup_form(self) -> None:
        label_titolo = QLabel('Titolo<span style="color:red;">*</span> :')
        label_titolo.setObjectName("subheader")
        self.titolo = QLineEdit()
        self.titolo.setPlaceholderText("Inserire titolo")

        label_note = QLabel('Note<span style="color:red;">*</span> :')
        label_note.setObjectName("subheader")
        self.note = QTextEdit()
        self.note.setPlaceholderText("Inserire note")
        self.note.setFixedHeight(80)

        # Lista interpreti
        label_interprete = QLabel("Interprete :")
        label_interprete.setObjectName("subheader")
        self.interprete_nome = QLineEdit()
        self.interprete_nome.setMaxLength(30)
        self.interprete_nome.setPlaceholderText("Inserire nome")
        self.interprete_ruolo = QLineEdit()
        self.interprete_ruolo.setMaxLength(30)
        self.interprete_ruolo.setPlaceholderText("Inserire ruolo")

        self.__btn_aggiungi_interprete = QPushButton("Aggiungi")
        self.__btn_aggiungi_interprete.setObjectName("whiteButton")

        interprete = QWidget()
        layout_interprete = QHBoxLayout(interprete)
        layout_interprete.addWidget(self.interprete_nome)
        layout_interprete.addWidget(self.interprete_ruolo)
        layout_interprete.addWidget(self.__btn_aggiungi_interprete)

        label_interprete.setFixedHeight(interprete.sizeHint().height())

        self.lista_interpreti: dict[str, str] = {}

        self.label_lista_interpreti_error = QLabel("")
        self.label_lista_interpreti_error.setObjectName("subheaderRed")

        self.label_lista_interpreti_vuota = QLabel("Non vi sono interpreti registrati.")
        self.label_lista_interpreti_vuota.setObjectName("subheader")
        self.label_lista_interpreti_vuota.hide()

        widget_lista_interpreti = QWidget()
        widget_lista_interpreti.setObjectName("listView")
        self.layout_lista_interpreti = QVBoxLayout(widget_lista_interpreti)
        self.layout_lista_interpreti.setContentsMargins(5, 5, 5, 5)
        self.layout_lista_interpreti.addWidget(self.label_lista_interpreti_vuota)

        # Lista tectici
        label_tecnico = QLabel("Tecnico :")
        label_tecnico.setObjectName("subheader")
        self.tecnico_nome = QLineEdit()
        self.tecnico_nome.setMaxLength(30)
        self.tecnico_nome.setPlaceholderText("Inserire nome")
        self.tecnico_posto = QLineEdit()
        self.tecnico_posto.setMaxLength(30)
        self.tecnico_posto.setPlaceholderText("Inserire posto")

        self.__btn_aggiungi_tecnico = QPushButton("Aggiungi")
        self.__btn_aggiungi_tecnico.setObjectName("whiteButton")

        tecnico = QWidget()
        layout_tecnico = QHBoxLayout(tecnico)
        layout_tecnico.addWidget(self.tecnico_nome)
        layout_tecnico.addWidget(self.tecnico_posto)
        layout_tecnico.addWidget(self.__btn_aggiungi_tecnico)

        label_tecnico.setFixedHeight(tecnico.sizeHint().height())

        self.lista_tecnici: dict[str, str] = {}

        self.label_lista_tecnici_error = QLabel("")
        self.label_lista_tecnici_error.setObjectName("subheaderRed")

        self.label_lista_tecnici_vuota = QLabel("Non vi sono tecnici registrati.")
        self.label_lista_tecnici_vuota.setObjectName("subheader")
        self.label_lista_tecnici_vuota.hide()

        widget_lista_tecnici = QWidget()
        widget_lista_tecnici.setObjectName("listView")
        self.layout_lista_tecnici = QVBoxLayout(widget_lista_tecnici)
        self.layout_lista_tecnici.setContentsMargins(5, 5, 5, 5)
        self.layout_lista_tecnici.addWidget(self.label_lista_tecnici_vuota)

        label_regista = QLabel('Regista<span style="color:red;">*</span> :')
        label_regista.setObjectName("subheader")
        self.regista = QLineEdit()
        self.regista.setPlaceholderText("Inserire regista")

        label_anno = QLabel('Anno di produzione<span style="color:red;">*</span> :')
        label_anno.setObjectName("subheader")
        self.anno = QSpinBox()
        self.anno.setRange(1597, QDate().currentDate().year())
        # - Serve un rango in particolare?

        label_opera = QLabel('Opera<span style="color:red;">*</span> :')
        label_opera.setObjectName("subheader")
        self.opera = QComboBox()
        self.opera.setEnabled(False)
        # - Questa pagina sarà esclusiva della sezione Info?

        self._form_layout.addRow(label_titolo, self.titolo)
        self._form_layout.addRow(label_note, self.note)
        self._form_layout.addRow(label_interprete, interprete)
        self._form_layout.addRow(
            self.label_lista_interpreti_error, widget_lista_interpreti
        )
        self._form_layout.addRow(label_tecnico, tecnico)
        self._form_layout.addRow(self.label_lista_tecnici_error, widget_lista_tecnici)
        self._form_layout.addRow(QLabel('<hr style="background-color:#b0b0b0;">'))
        self._form_layout.addRow(label_regista, self.regista)
        self._form_layout.addRow(label_anno, self.anno)
        self._form_layout.addRow(label_opera, self.opera)

    @override
    def _connect_signals(self) -> None:
        super()._connect_signals()

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

    def aggiungi_widget_a_layout(self, widget: QWidget, layout: QVBoxLayout):
        """Aggiunge un widget creato per il display del personale della regia (interpreti e tecnici).

        :param widget: widget speciale per visualizzare un membro del personale
        :param layout: layout dove sarà inserito il widget"""
        layout.addWidget(widget)

    def __svuota_layout(self, layout: Optional[QLayout]) -> None:
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
                    self.__svuota_layout(child_layout)

    def aggiorna_pagina(self) -> None:
        """Permette di aggiornare la pagina e visualizzare modifiche previamente non mostrate."""
        self.interprete_nome.setText("")
        self.interprete_ruolo.setText("")
        self.label_lista_interpreti_error.setText("")
        self.__svuota_layout(self.layout_lista_interpreti)
        self.label_lista_interpreti_vuota.hide()
        self.layout_lista_interpreti.addWidget(self.label_lista_interpreti_vuota)
        self.displayInterpreti.emit(self)

        self.tecnico_nome.setText("")
        self.tecnico_posto.setText("")
        self.label_lista_tecnici_error.setText("")
        self.__svuota_layout(self.layout_lista_tecnici)
        self.label_lista_tecnici_vuota.hide()
        self.layout_lista_tecnici.addWidget(self.label_lista_tecnici_vuota)
        self.displayTecnici.emit(self)

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
        self._input_error.setText("")
