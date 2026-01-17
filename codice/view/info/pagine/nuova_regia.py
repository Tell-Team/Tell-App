from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QComboBox,
    QSpinBox,
)
from PyQt6.QtCore import QDate
from typing import override

from model.pianificazione.opera import Opera

from view.spettacoli.pagine import NuovoSpettacoloView
from view.style import WidgetRole, WidgetColor


class NuovaRegiaView(NuovoSpettacoloView):
    """Pagina per la creazione di una nuova regia."""

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        # Header
        self._header.setText("Aggiungi nuova regia")

    @override
    def _setup_form(self) -> None:
        super()._setup_form()

        label_regista = QLabel('Regista<span style="color:red;">*</span> :')
        label_regista.setProperty(WidgetRole.BODY_TEXT, True)
        label_regista.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
        self.regista = QLineEdit()
        self.regista.setPlaceholderText("Inserire regista")

        label_anno = QLabel('Anno di produzione<span style="color:red;">*</span> :')
        label_anno.setProperty(WidgetRole.BODY_TEXT, True)
        label_anno.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
        self.anno = QSpinBox()
        self.anno.setRange(1597, QDate().currentDate().year())
        # - Serve un rango in particolare?

        label_opera = QLabel('Opera<span style="color:red;">*</span> :')
        label_opera.setProperty(WidgetRole.BODY_TEXT, True)
        label_opera.setProperty(WidgetColor.Text.SECONDARY_TEXT, True)
        self.opera = QComboBox()
        self.opera.setEnabled(False)
        # - Questa pagina sarà esclusiva della sezione Info?

        self._form_layout.addRow(QLabel('<hr style="background-color:#b0b0b0;">'))
        self._form_layout.addRow(label_regista, self.regista)
        self._form_layout.addRow(label_anno, self.anno)
        self._form_layout.addRow(label_opera, self.opera)

    # ------------------------- METODI DI VIEW -------------------------

    def setup_opera_combobox(self, o: Opera) -> None:
        """Riempisce il `QComboBox` delle opere."""
        # - Solo inserisce l'opera da dove si chiama il Crea/Modifica Regia
        self.opera.clear()

        self.opera.insertItem(0, "Scegliere genere...", -1)
        self.opera.insertItem(1, o.get_nome(), o.get_id())
        # - Se questa pagina sarà usata anche dalla sezione Spettacoli, devo carica tutte le opere
        #   nel QComboBox e abilitarlo.

    @override
    def reset_pagina(self) -> None:
        """Reset della pagina allo stato default (con solo l'opera scelta)."""
        super().reset_pagina()

        self.regista.setText("")
        self.anno.setValue(QDate().currentDate().year())
        self.opera.setCurrentIndex(1)
