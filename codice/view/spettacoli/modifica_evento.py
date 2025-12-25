from typing import Dict, Any, Optional
from PyQt6.QtCore import pyqtSignal, QDate, QTime, Qt
from PyQt6.QtWidgets import (
    QWidget, QLabel, QComboBox, QPushButton, QFormLayout, QHBoxLayout,
    QVBoxLayout, QMessageBox, QDateEdit, QTimeEdit, QCheckBox, QLineEdit
)
from PyQt6.QtGui import QIntValidator

class ModificaEventoView(QWidget):
    """
    View per la modifica di un Evento esistente.

    Segnali:
    - evento_modificato(dict): emesso al salvataggio.
    - annullato(): emesso all'annullamento.
    - evento_eliminato(): emesso all'eliminazione.
    """

    evento_modificato = pyqtSignal(object)
    annullato = pyqtSignal()
    evento_eliminato = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Inizializza view.
        :raises: nessuna eccezione prevista.
        """
        super().__init__(parent)
        self.__setup_ui()

    def __setup_ui(self) -> None:
        """Costruisce UI."""
        self.setWindowTitle("Modifica Evento")
        self.setMinimumWidth(500)
        self.__titolo = QLabel("<h2>Modifica Evento</h2>")
        
        self.__data_input = QDateEdit(calendarPopup=True)
        self.__ora_input = QTimeEdit()
        self.__sala_select = QComboBox()
        self.__sala_select.addItem("Sala Grande", "sala_grande")
        self.__sala_select.addItem("Piccolo Teatro", "sala_piccola")

        self.__stato_select = QComboBox()
        self.__stato_select.addItem("Pubblicato", "pubblicato")
        self.__stato_select.addItem("Bozza", "bozza")

        self.__prezzo_check = QCheckBox("Override Prezzo")
        self.__prezzo_check.stateChanged.connect(self.__toggle_prezzo)
        self.__prezzo_input = QLineEdit()
        self.__prezzo_input.setValidator(QIntValidator(0, 9999))
        self.__prezzo_input.setVisible(False)

        self.__btn_salva = QPushButton("Salva")
        self.__btn_elimina = QPushButton("Elimina")
        self.__btn_annulla = QPushButton("Annulla")

        layout = QVBoxLayout(self)
        layout.addWidget(self.__titolo)
        form = QFormLayout()
        form.addRow("Data:", self.__data_input)
        form.addRow("Ora:", self.__ora_input)
        form.addRow("Sala:", self.__sala_select)
        form.addRow("Stato:", self.__stato_select)
        form.addRow(self.__prezzo_check)
        form.addRow("Prezzo:", self.__prezzo_input)
        layout.addLayout(form)
        
        btns = QHBoxLayout()
        btns.addWidget(self.__btn_elimina)
        btns.addStretch()
        btns.addWidget(self.__btn_annulla)
        btns.addWidget(self.__btn_salva)
        layout.addLayout(btns)

        self.__btn_salva.clicked.connect(self.__on_salva)
        self.__btn_elimina.clicked.connect(self.__on_elimina)
        self.__btn_annulla.clicked.connect(lambda: self.annullato.emit())

    def __toggle_prezzo(self, stato: int) -> None:
        """
        Toggle visibilità prezzo.
        :raises: nessuna eccezione prevista.
        """
        self.__prezzo_input.setVisible(stato == 2)

    def set_dati_form(self, dati: Dict[str, Any]) -> None:
        """
        Popola il form.
        :raises: nessuna eccezione prevista.
        """
        self.__data_input.setDate(QDate.fromString(dati.get("data"), Qt.DateFormat.ISODate))
        self.__ora_input.setTime(QTime.fromString(dati.get("ora"), Qt.DateFormat.ISODate))
        #Aggiungere logica per settare combobox e checkbox(?)

    def get_dati_form(self) -> Dict[str, Any]:
        """
        Recupera dati.
        :raises: nessuna eccezione prevista.
        """
        return {
            "data": self.__data_input.date().toString(Qt.DateFormat.ISODate),
            # Altri campi da aggiungere(?)
        }

    def __on_salva(self) -> None:
        """
        Gestisce salvataggio.
        :raises: nessuna eccezione prevista.
        """
        self.evento_modificato.emit(self.get_dati_form())

    def __on_elimina(self) -> None:
        """
        Gestisce eliminazione.
        :raises: nessuna eccezione prevista.
        """
        if QMessageBox.question(self, "Elimina", "Confermi?") == QMessageBox.StandardButton.Yes:
            self.evento_eliminato.emit()