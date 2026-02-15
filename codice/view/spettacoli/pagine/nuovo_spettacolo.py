from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtCore import pyqtSignal
from typing import override

from core.view import AbstractCreaView

from view.utils.list_widgets import ListLayout, EmptyStateLabel
from view.utils.custom_button import DefaultButton
from view.utils.hyphenate_text import HyphenatedLabel

from view.style.ui_style import WidgetRole, WidgetColor


class NuovoSpettacoloView(AbstractCreaView):
    """Pagina per la creazione di un nuovo spettacolo.

    Segnali
    ---
    - `displayInterpreti(CreaAbstractView)`: emesso per mostrare la lista interpreti a schermo;
    - `displayMusicisti_e_direttori_artistici(CreaAbstractView)`: emesso per mostrare la lista musicisti_e_direttori_artistici a schermo;
    - `aggiungiInterprete(CreaAbstractView, str, str)`: emesso quando si clicca il pulsante
    Aggiungi degli interpreti;
    - `aggiungiTecnico(CreaAbstractView, str, str)`: emesso quando si clicca il pulsante Aggiungi
    dei musicisti_e_direttori_artistici.
    """

    displayInterpreti = pyqtSignal(AbstractCreaView)
    displayMusicisti_e_direttori_artistici = pyqtSignal(AbstractCreaView)
    aggiungiInterprete = pyqtSignal(AbstractCreaView, str, str)
    aggiungiTecnico = pyqtSignal(AbstractCreaView, str, str)

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        # Header
        self._header.setText("Aggiungi nuovo spettacolo")

        # Layout
        self._main_layout.addWidget(self._header)
        self._main_layout.addWidget(self._scroll_area)
        self._main_layout.addWidget(self._input_error)
        self._main_layout.addWidget(self._pulsanti)

    @override
    def _setup_form(self) -> None:
        label_titolo = QLabel('Titolo<span style="color:red;">*</span> :')
        label_titolo.setProperty(WidgetRole.Label.BODY_TEXT, True)
        label_titolo.setProperty(WidgetColor.Label.SECONDARY_COLOR, True)
        self.titolo = QLineEdit()
        self.titolo.setPlaceholderText("Inserire titolo")

        label_note = QLabel("Note :")
        label_note.setProperty(WidgetRole.Label.BODY_TEXT, True)
        label_note.setProperty(WidgetColor.Label.SECONDARY_COLOR, True)
        self.note = QTextEdit()
        self.note.setPlaceholderText("Inserire note")
        self.note.setFixedHeight(80)

        # Lista interpreti
        label_interprete = QLabel("Interprete :")
        label_interprete.setProperty(WidgetRole.Label.BODY_TEXT, True)
        label_interprete.setProperty(WidgetColor.Label.SECONDARY_COLOR, True)
        self.interprete_nome = QLineEdit()
        self.interprete_nome.setPlaceholderText("Inserire nome")
        self.interprete_ruolo = QLineEdit()
        self.interprete_ruolo.setPlaceholderText("Inserire ruolo")

        self._btn_aggiungi_interprete = DefaultButton("Aggiungi")

        interprete = QWidget()
        layout_interprete = QHBoxLayout(interprete)
        layout_interprete.addWidget(self.interprete_nome)
        layout_interprete.addWidget(self.interprete_ruolo)
        layout_interprete.addWidget(self._btn_aggiungi_interprete)

        label_interprete.setFixedHeight(interprete.sizeHint().height())

        self.lista_interpreti: dict[str, str] = {}

        self.label_lista_interpreti_error = QLabel("")
        self.label_lista_interpreti_error.setProperty(WidgetRole.Label.BODY_TEXT, True)
        self.label_lista_interpreti_error.setProperty(
            WidgetColor.Label.ERROR_COLOR, True
        )

        label_lista_interpreti_vuota = EmptyStateLabel(
            "Non vi sono interpreti registrati."
        )
        label_lista_interpreti_vuota.setProperty(WidgetRole.Label.BODY_TEXT, True)
        label_lista_interpreti_vuota.setProperty(
            WidgetColor.Label.SECONDARY_COLOR, True
        )

        widget_lista_interpreti = QWidget()
        widget_lista_interpreti.setProperty(WidgetRole.Item.LIST, True)
        self.layout_lista_interpreti = ListLayout(
            widget_lista_interpreti, label_lista_interpreti_vuota
        )
        # end-Lista interpreti

        # Lista tectici (Musicisti/Direttori artistici)
        label_tecnico = HyphenatedLabel("Musicista/direttore artistico :")
        label_tecnico.setProperty(WidgetRole.Label.BODY_TEXT, True)
        label_tecnico.setProperty(WidgetColor.Label.SECONDARY_COLOR, True)
        self.tecnico_nome = QLineEdit()
        self.tecnico_nome.setPlaceholderText("Inserire nome")
        self.tecnico_posto = QLineEdit()
        self.tecnico_posto.setPlaceholderText("Inserire posto")

        self._btn_aggiungi_tecnico = DefaultButton("Aggiungi")

        tecnico = QWidget()
        layout_tecnico = QHBoxLayout(tecnico)
        layout_tecnico.addWidget(self.tecnico_nome)
        layout_tecnico.addWidget(self.tecnico_posto)
        layout_tecnico.addWidget(self._btn_aggiungi_tecnico)

        label_tecnico.setFixedHeight(tecnico.sizeHint().height())

        self.lista_musicisti_e_direttori_artistici: dict[str, str] = {}

        self.label_lista_musicisti_e_direttori_artistici_error = QLabel("")
        self.label_lista_musicisti_e_direttori_artistici_error.setProperty(
            WidgetRole.Label.BODY_TEXT, True
        )
        self.label_lista_musicisti_e_direttori_artistici_error.setProperty(
            WidgetColor.Label.ERROR_COLOR, True
        )

        label_lista_musicisti_e_direttori_artistici_vuota = EmptyStateLabel(
            "Non vi sono musicisti/direttori artistici registrati."
        )
        label_lista_musicisti_e_direttori_artistici_vuota.setProperty(
            WidgetRole.Label.BODY_TEXT, True
        )
        label_lista_musicisti_e_direttori_artistici_vuota.setProperty(
            WidgetColor.Label.SECONDARY_COLOR, True
        )

        widget_lista_musicisti_e_direttori_artistici = QWidget()
        widget_lista_musicisti_e_direttori_artistici.setProperty(
            WidgetRole.Item.LIST, True
        )
        self.layout_lista_musicisti_e_direttori_artistici = ListLayout(
            widget_lista_musicisti_e_direttori_artistici,
            label_lista_musicisti_e_direttori_artistici_vuota,
        )
        # end-Lista musicisti_e_direttori_artistici

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
        self._form_layout.addRow(
            self.label_lista_musicisti_e_direttori_artistici_error,
            widget_lista_musicisti_e_direttori_artistici,
        )
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

        self.displayMusicisti_e_direttori_artistici.emit(self)

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
        self.label_lista_musicisti_e_direttori_artistici_error.setText("")
        self.layout_lista_musicisti_e_direttori_artistici.svuota_layout()
        self.displayMusicisti_e_direttori_artistici.emit(self)

    @override
    def reset_pagina(self) -> None:
        super().reset_pagina()

        self.titolo.setText("")
        self.note.setText("")
        self.lista_interpreti = {}
        self.lista_musicisti_e_direttori_artistici = {}
        self._input_error.setText("")
