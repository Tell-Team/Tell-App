from typing import Dict, Any, Optional
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QPushButton,
    QFormLayout, QHBoxLayout, QVBoxLayout, QMessageBox, QSpinBox
)

class CreaSpettacoloView(QWidget):
    """
    View per la creazione di un nuovo Spettacolo.

    Gestisce l'input dei dati base (titolo, descrizione, durata) e
    la validazione prima dell'emissione del segnale di creazione.

    Segnali:
    - spettacolo_creato(dict): emesso quando l'utente salva con dati validi.
    - annullato(): emesso quando l'utente annulla l'operazione.
    """

    spettacolo_creato = pyqtSignal(object)
    annullato = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Inizializza la view.

        :param parent: widget genitore.(?)
        :raises: nessuna eccezione prevista.
        """
        super().__init__(parent)
        self.__setup_ui()

    def __setup_ui(self) -> None:
        """
        Costruisce l'interfaccia grafica.
        """
        self.setWindowTitle("Nuovo Spettacolo")
        self.setMinimumWidth(400)

        # Widget Input (Privati)
        self.__input_titolo: QLineEdit = QLineEdit()
        self.__input_descrizione: QTextEdit = QTextEdit()
        self.__input_durata: QSpinBox = QSpinBox()
        self.__input_durata.setRange(1, 300)
        self.__input_durata.setSuffix(" min")

        # Bottoni
        self.__btn_salva: QPushButton = QPushButton("Salva")
        self.__btn_salva.setStyleSheet("background-color: #28a745; color: white; font-weight: bold;")
        self.__btn_annulla: QPushButton = QPushButton("Annulla")
        self.__btn_annulla.setStyleSheet("background-color: #6c757d; color: white;")

        # Layout Form
        form_layout = QFormLayout()
        form_layout.addRow("Titolo *:", self.__input_titolo)
        form_layout.addRow("Descrizione:", self.__input_descrizione)
        form_layout.addRow("Durata (minuti) *:", self.__input_durata)

        # Layout Bottoni
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.__btn_annulla)
        btn_layout.addWidget(self.__btn_salva)

        # Layout Principale
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(QLabel("<h2>Crea Nuovo Spettacolo</h2>"))
        main_layout.addLayout(form_layout)
        main_layout.addLayout(btn_layout)

        # Connessioni
        self.__btn_salva.clicked.connect(self.__on_salva_clicked)
        self.__btn_annulla.clicked.connect(self.__on_annulla_clicked)

    # ------------------------- METODI PUBBLICI -------------------------

    def get_dati_form(self) -> Dict[str, Any]:
        """
        Restituisce i dati inseriti nel form.

        :return: Dizionario con chiavi 'titolo', 'descrizione', 'durata'.
        :raises: nessuna eccezione prevista.
        """
        return {
            "titolo": self.__input_titolo.text().strip(),
            "descrizione": self.__input_descrizione.toPlainText().strip(),
            "durata": self.__input_durata.value()
        }

    def reset_form(self) -> None:
        """
        Pulisce i campi del form.

        :raises: nessuna eccezione prevista.
        """
        self.__input_titolo.clear()
        self.__input_descrizione.clear()
        self.__input_durata.setValue(60)

    # ------------------------- VALIDAZIONE E CALLBACKS -------------------------

    def __valida_dati(self) -> bool:
        """
        Controlla che i campi obbligatori siano compilati.

        :return: True se i dati sono validi, False altrimenti.
        :raises: nessuna eccezione prevista.
        """
        titolo = self.__input_titolo.text().strip()
        if not titolo:
            self.__mostra_errore("Errore Validazione", "Il campo 'Titolo' è obbligatorio.")
            return False
        
        # Esempio di validazione aggiuntiva(?)
        if self.__input_durata.value() <= 0:
            self.__mostra_errore("Errore Validazione", "La durata deve essere maggiore di 0.")
            return False

        return True

    def __on_salva_clicked(self) -> None:
        """
        Gestisce il click sul tasto Salva.
        Valida i dati ed emette il segnale se tutto è corretto.
        
        :raises: nessuna eccezione prevista.
        """
        if self.__valida_dati():
            self.spettacolo_creato.emit(self.get_dati_form())

    def __on_annulla_clicked(self) -> None:
        """
        Gestisce il click sul tasto Annulla.
        
        :raises: nessuna eccezione prevista.
        """
        self.reset_form()
        self.annullato.emit()

    def __mostra_errore(self, titolo: str, messaggio: str) -> None:
        """
        Mostra una popup di errore.

        :param titolo: Titolo della finestra.
        :param messaggio: Testo dell'errore.
        :raises: nessuna eccezione prevista.
        """
        QMessageBox.warning(self, titolo, messaggio)