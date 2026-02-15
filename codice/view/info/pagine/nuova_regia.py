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

from view.utils import make_hline

from view.style.ui_style import WidgetRole, WidgetColor


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
        label_regista.setProperty(WidgetRole.Label.BODY_TEXT, True)
        label_regista.setProperty(WidgetColor.Label.SECONDARY_COLOR, True)
        self.regista = QLineEdit()
        self.regista.setPlaceholderText("Inserire regista")

        label_anno = QLabel('Anno di produzione<span style="color:red;">*</span> :')
        label_anno.setProperty(WidgetRole.Label.BODY_TEXT, True)
        label_anno.setProperty(WidgetColor.Label.SECONDARY_COLOR, True)
        self.anno = QSpinBox()
        self.anno.setRange(0, QDate().currentDate().year())

        label_opera = QLabel('Opera<span style="color:red;">*</span> :')
        label_opera.setProperty(WidgetRole.Label.BODY_TEXT, True)
        label_opera.setProperty(WidgetColor.Label.SECONDARY_COLOR, True)
        self.opera = QComboBox()
        self.opera.setEnabled(False)

        self._form_layout.addRow(make_hline())
        self._form_layout.addRow(label_regista, self.regista)
        self._form_layout.addRow(label_anno, self.anno)
        self._form_layout.addRow(label_opera, self.opera)

        self.titolo.setEnabled(False)
        self.titolo.setText("Viene assegnato dopo la creazione.")

    # ------------------------- METODI DI VIEW -------------------------

    def setup_opera_combobox(self, o: Opera) -> None:
        """Riempisce il `QComboBox` delle opere."""
        self.opera.clear()

        self.opera.insertItem(0, "Scegliere genere...", -1)
        self.opera.insertItem(1, o.get_nome(), o.get_id())

    @override
    def reset_pagina(self) -> None:
        """Reset della pagina allo stato default (con solo l'opera scelta)."""
        super().reset_pagina()
        self.titolo.setText("Viene assegnato dopo la creazione.")

        self.regista.setText("")
        self.anno.setValue(QDate().currentDate().year())
        self.opera.setCurrentIndex(1)
