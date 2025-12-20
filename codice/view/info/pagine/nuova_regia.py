from PyQt6.QtWidgets import QLabel, QLineEdit, QTextEdit, QComboBox, QSpinBox
from PyQt6.QtCore import pyqtSignal
from functools import partial
from typing import override

from model.pianificazione.opera import Opera

from view.abstractView.creaAbstract import CreaAbstractView


# - STUDIARE: Ci sarà una classe NuovoSpettacoloView da cui questa sarà una sottoclasse,
#   oppure questa sarà una classe dedicata esclusivamente alle regie?
class NuovaRegiaView(CreaAbstractView):
    """View per la creazione di una nuova regia.

    Segnali:
    - annullaRequest(CreaAbstractView): emesso quando si clicca il pulsante Annulla;
    - salvaRequest(): emesso quando si clicca il pulsante Conferma.
    """

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
        self.main_layout.addWidget(self.form_content)
        self.main_layout.addWidget(self.input_error)
        self.main_layout.addWidget(self.pulsanti)
        self.main_layout.addStretch()

    @override
    def _setup_form(self) -> None:
        label_titolo = QLabel("Titolo :")
        label_titolo.setObjectName("SubHeader")
        self.titolo = QLineEdit()
        self.titolo.setPlaceholderText("Inserire titolo")

        label_note = QLabel("Note :")
        label_note.setObjectName("SubHeader")
        self.note = QTextEdit()
        self.note.setPlaceholderText("Inserire note")
        self.note.setFixedHeight(80)

        # - CORRIGGERE: Aggiungere i metodi necessari per creare ed eliminare
        #   interpreti e tecnici

        label_regista = QLabel("Regista :")
        label_regista.setObjectName("SubHeader")
        self.regista = QLineEdit()
        self.regista.setPlaceholderText("Inserire regista")

        label_anno = QLabel("Anno di produzione :")
        label_anno.setObjectName("SubHeader")
        self.anno = QSpinBox()
        self.anno.setRange(0, 3000)  # - CORRIGGERE: Serve un rango in particolare?

        label_opera = QLabel("Opera :")
        label_opera.setObjectName("SubHeader")
        self.opera = QComboBox()
        # - CORRIGGERE: Caricare l'opera da cui si chiama i Crea/Modifica
        self.opera.setEnabled(False)
        # - TEMPORANEO: Non so se questa pagina sarà esclusiva di info

        self.form_layout.addRow(label_titolo, self.titolo)
        self.form_layout.addRow(label_note, self.note)
        self.form_layout.addRow(label_regista, self.regista)
        self.form_layout.addRow(label_anno, self.anno)
        self.form_layout.addRow(label_opera, self.opera)

    def _connect_signals(self) -> None:
        self._btn_annulla.clicked.connect(  # type:ignore
            partial(self.annullaRequest.emit, self)
        )  # - CORRIGGERE: E' collegato all'InfoController. Sarà corretto?

        self._btn_conferma.clicked.connect(  # type:ignore
            self.salvaRequest.emit
        )  # - CORRIGGERE: E' collegato all'InfoController. Sarà corretto?

    # ------------------------- METODI DI VIEW -------------------------

    # - TEMPORANEO: Solo inserisce l'opera da dove si chiama il Crea/Modifica Regia
    # - Se penso fare questa pagina, una pagina per creare regie ovunque, devo permettere di
    #   caricare tutte le opere a questo metodo.
    def setup_opera_combobox(self, o: Opera) -> None:
        """Riempisce il `QComboBox` de opere (con solo l'opera indicata)."""
        self.opera.clear()

        self.opera.insertItem(0, "Scegliere genere...", -1)
        self.opera.insertItem(1, o.get_nome(), o.get_id())

    def reset_pagina(self) -> None:
        """Reset della pagina allo stato default (con solo l'opera scelta)."""
        self.titolo.setText("")
        self.note.setText("")
        self.opera.setCurrentIndex(1)
        self.regista.setText("")
        self.anno.setValue(0)
        self.input_error.setText("")

    def set_pagina_focus(self) -> None:
        """Evidenzia il primo campo con input non valido trovato."""
        self.focusNextChild()
        if not self.titolo.text().strip():
            return
        self.focusNextChild()
        if not self.note.toPlainText().strip():
            return
        self.focusNextChild()
        if not self.regista.text().strip():
            return
        self.focusNextChild()
        if self.opera.currentIndex() == 0:
            return
        self.focusNextChild()
