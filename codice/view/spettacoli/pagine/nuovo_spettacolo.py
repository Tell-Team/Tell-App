from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtCore import pyqtSignal
from typing import override

from core.view import AbstractCreaView

from view.utils.list_widgets import ListLayout, EmptyStateLabel
from view.style import QssStyle


class NuovoSpettacoloView(AbstractCreaView):
    """View per la creazione di un nuovo spettacolo.

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
        self._header.setText("Aggiungi nuovo spettacolo")

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
        label_titolo.setProperty(QssStyle.SECONDARY_TEXT, True)
        self.titolo = QLineEdit()
        self.titolo.setPlaceholderText("Inserire titolo")

        label_note = QLabel('Note<span style="color:red;">*</span> :')
        label_note.setProperty(QssStyle.SECONDARY_TEXT, True)
        self.note = QTextEdit()
        self.note.setPlaceholderText("Inserire note")
        self.note.setFixedHeight(80)

        # Lista interpreti
        label_interprete = QLabel("Interprete :")
        label_interprete.setProperty(QssStyle.SECONDARY_TEXT, True)
        self.interprete_nome = QLineEdit()
        self.interprete_nome.setMaxLength(30)
        self.interprete_nome.setPlaceholderText("Inserire nome")
        self.interprete_ruolo = QLineEdit()
        self.interprete_ruolo.setMaxLength(30)
        self.interprete_ruolo.setPlaceholderText("Inserire ruolo")

        self._btn_aggiungi_interprete = QPushButton("Aggiungi")
        self._btn_aggiungi_interprete.setProperty(QssStyle.WHITE_BUTTON, True)

        interprete = QWidget()
        layout_interprete = QHBoxLayout(interprete)
        layout_interprete.addWidget(self.interprete_nome)
        layout_interprete.addWidget(self.interprete_ruolo)
        layout_interprete.addWidget(self._btn_aggiungi_interprete)

        label_interprete.setFixedHeight(interprete.sizeHint().height())

        self.lista_interpreti: dict[str, str] = {}

        self.label_lista_interpreti_error = QLabel("")
        self.label_lista_interpreti_error.setProperty(QssStyle.ERROR_MESSAGE, True)

        label_lista_interpreti_vuota = EmptyStateLabel(
            "Non vi sono interpreti registrati."
        )
        label_lista_interpreti_vuota.setProperty(QssStyle.SECONDARY_TEXT, True)

        widget_lista_interpreti = QWidget()
        widget_lista_interpreti.setProperty(QssStyle.ITEM_LIST, True)
        self.layout_lista_interpreti = ListLayout(
            widget_lista_interpreti, label_lista_interpreti_vuota
        )
        # end-Lista interpreti

        # Lista tectici
        label_tecnico = QLabel("Tecnico :")
        label_tecnico.setProperty(QssStyle.SECONDARY_TEXT, True)
        self.tecnico_nome = QLineEdit()
        self.tecnico_nome.setMaxLength(30)
        self.tecnico_nome.setPlaceholderText("Inserire nome")
        self.tecnico_posto = QLineEdit()
        self.tecnico_posto.setMaxLength(30)
        self.tecnico_posto.setPlaceholderText("Inserire posto")

        self._btn_aggiungi_tecnico = QPushButton("Aggiungi")
        self._btn_aggiungi_tecnico.setProperty(QssStyle.WHITE_BUTTON, True)

        tecnico = QWidget()
        layout_tecnico = QHBoxLayout(tecnico)
        layout_tecnico.addWidget(self.tecnico_nome)
        layout_tecnico.addWidget(self.tecnico_posto)
        layout_tecnico.addWidget(self._btn_aggiungi_tecnico)

        label_tecnico.setFixedHeight(tecnico.sizeHint().height())

        self.lista_tecnici: dict[str, str] = {}

        self.label_lista_tecnici_error = QLabel("")
        self.label_lista_tecnici_error.setProperty(QssStyle.ERROR_MESSAGE, True)

        label_lista_tecnici_vuota = EmptyStateLabel("Non vi sono tecnici registrati.")
        label_lista_tecnici_vuota.setProperty(QssStyle.SECONDARY_TEXT, True)

        widget_lista_tecnici = QWidget()
        widget_lista_tecnici.setProperty(QssStyle.ITEM_LIST, True)
        self.layout_lista_tecnici = ListLayout(
            widget_lista_tecnici, label_lista_tecnici_vuota
        )
        # end-Lista tecnici

        spacer = QWidget()
        l_spacer = QVBoxLayout(spacer)
        l_spacer.setContentsMargins(0, 0, 0, 0)
        l_spacer.addStretch()

        self._form_layout.addRow(label_titolo, self.titolo)
        self._form_layout.addRow(label_note, self.note)
        self._form_layout.addRow(label_interprete, interprete)
        self._form_layout.addRow(
            self.label_lista_interpreti_error, widget_lista_interpreti
        )
        self._form_layout.addRow(label_tecnico, tecnico)
        self._form_layout.addRow(self.label_lista_tecnici_error, widget_lista_tecnici)
        self._form_layout.addRow(None, spacer)

    @override
    def _connect_signals(self) -> None:
        super()._connect_signals()

        self._btn_aggiungi_interprete.clicked.connect(  # type:ignore
            lambda: self.aggiungiInterprete.emit(
                self,
                self.interprete_nome.text().strip(),
                self.interprete_ruolo.text().strip(),
            )
        )

        self._btn_aggiungi_tecnico.clicked.connect(  # type:ignore
            lambda: self.aggiungiTecnico.emit(
                self,
                self.tecnico_nome.text().strip(),
                self.tecnico_posto.text().strip(),
            )
        )

        self.displayInterpreti.emit(self)

        self.displayTecnici.emit(self)

    # ------------------------- METODI DI VIEW -------------------------

    def aggiorna_pagina(self) -> None:
        """Permette di aggiornare la pagina e visualizzare modifiche previamente non mostrate."""
        self.interprete_nome.setText("")
        self.interprete_ruolo.setText("")
        self.label_lista_interpreti_error.setText("")
        self.layout_lista_interpreti.svuota_layout()
        self.displayInterpreti.emit(self)

        self.tecnico_nome.setText("")
        self.tecnico_posto.setText("")
        self.label_lista_tecnici_error.setText("")
        self.layout_lista_tecnici.svuota_layout()
        self.displayTecnici.emit(self)

    @override
    def reset_pagina(self) -> None:
        self.titolo.setText("")
        self.note.setText("")
        self.lista_interpreti = {}
        self.lista_tecnici = {}
        self._input_error.setText("")
