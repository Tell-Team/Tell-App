from typing import Dict
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QComboBox, QPushButton,
    QVBoxLayout, QHBoxLayout, QGroupBox, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt, pyqtSignal


class CreaSpettacoloView(QWidget):
    """
    View per la creazione di un nuovo spettacolo.
    Contiene campi per titolo, opera e regia associata, tipo evento e lista repliche.

    Segnali:
    - spettacolo_salvato(dict): emesso quando l'utente clicca 'Salva Spettacolo'
    - annullato(): emesso quando l'utente clicca 'Annulla'
    """

    spettacolo_salvato = pyqtSignal(object)  # dict dei dati inseriti
    annullato = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.__setup_ui()

    # ------------------------------------------------------------------
    def __setup_ui(self) -> None:
        """Imposta la UI della schermata di creazione spettacolo."""

        # Titolo principale
        self.label_titolo: QLabel = QLabel("Aggiungi Nuovo Spettacolo (Programmazione)")
        self.label_titolo.setStyleSheet("font-size: 20px; font-weight: bold;")

        # -------------------------------
        # Dati Base e Contenuto
        # -------------------------------
        box_dati: QGroupBox = QGroupBox("Dati Base e Contenuto")
        layout_dati: QVBoxLayout = QVBoxLayout()

        self.input_titolo: QLineEdit = QLineEdit()
        self.input_titolo.setPlaceholderText("Es. La Traviata - Stagione 2025")

        self.select_opera: QComboBox = QComboBox()
        self.select_opera.addItem("Seleziona l'Opera")
        self.select_opera.addItem("La Traviata")

        self.select_regia: QComboBox = QComboBox()
        self.select_regia.addItem("Seleziona la Regia")
        self.select_regia.addItem("Produzione Corrente 2024")

        layout_dati.addWidget(QLabel("Titolo Spettacolo *"))
        layout_dati.addWidget(self.input_titolo)

        # Layout in due colonne per opera e regia
        layout_dual: QHBoxLayout = QHBoxLayout()
        layout_dual.addWidget(self.select_opera)
        layout_dual.addWidget(self.select_regia)
        layout_dati.addLayout(layout_dual)

        box_dati.setLayout(layout_dati)

        # -------------------------------
        # Politiche di Prezzo Generali
        # -------------------------------
        box_prezzo: QGroupBox = QGroupBox("Politiche di Prezzo Generali")
        layout_prezzo: QVBoxLayout = QVBoxLayout()

        layout_prezzo.addWidget(QLabel("Questi criteri definiranno il prezzo base del biglietto (tipologia posto + tipologia evento)."))

        self.select_tipo_evento: QComboBox = QComboBox()
        self.select_tipo_evento.addItems(["Standard", "Prima/Gala", "Recita Ridotta"])

        layout_prezzo.addWidget(QLabel("Tipo Evento (Per Logica Prezzo Base) *"))
        layout_prezzo.addWidget(self.select_tipo_evento)

        box_prezzo.setLayout(layout_prezzo)

        # -------------------------------
        # Lista Eventi (Repliche)
        # -------------------------------
        box_eventi: QGroupBox = QGroupBox("Lista Eventi (Repliche)")
        layout_eventi: QVBoxLayout = QVBoxLayout()

        self.tabella_eventi: QTableWidget = QTableWidget(1, 4)
        self.tabella_eventi.setHorizontalHeaderLabels(["Data e Ora", "Sala", "Stato", "Azioni"])
        self.tabella_eventi.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabella_eventi.setItem(0, 0, QTableWidgetItem("Nessun evento associato. Salva lo spettacolo per aggiungerne uno."))
        self.tabella_eventi.setSpan(0, 0, 1, 4)
        self.tabella_eventi.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        layout_eventi.addWidget(self.tabella_eventi)
        box_eventi.setLayout(layout_eventi)

        # -------------------------------
        # Pulsanti di azione
        # -------------------------------
        layout_bottoni: QHBoxLayout = QHBoxLayout()
        layout_bottoni.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.btn_annulla: QPushButton = QPushButton("Annulla")
        self.btn_annulla.setStyleSheet("background-color: #6c757d; color: white;")

        self.btn_salva: QPushButton = QPushButton("Salva Spettacolo")
        self.btn_salva.setStyleSheet("background-color: #28a745; color: white;")

        layout_bottoni.addWidget(self.btn_annulla)
        layout_bottoni.addWidget(self.btn_salva)

        # -------------------------------
        # Layout principale
        # -------------------------------
        layout_principale: QVBoxLayout = QVBoxLayout()
        layout_principale.addWidget(self.label_titolo)
        layout_principale.addSpacing(10)
        layout_principale.addWidget(box_dati)
        layout_principale.addWidget(box_prezzo)
        layout_principale.addWidget(box_eventi)
        layout_principale.addLayout(layout_bottoni)

        self.setLayout(layout_principale)
        self.setMinimumWidth(700)
        self.setWindowTitle("Crea Nuovo Spettacolo")

        # Connessioni bottoni
        self.btn_salva.clicked.connect(self.__on_salva_clicked)
        self.btn_annulla.clicked.connect(self.__on_annulla_clicked)

    # ------------------------------------------------------------------
    def get_dati_form(self) -> Dict[str, str]:
        """Restituisce i valori correnti del form come dict."""
        return {
            "titolo": self.input_titolo.text().strip(),
            "opera": self.select_opera.currentText(),
            "regia": self.select_regia.currentText(),
            "tipo_evento": self.select_tipo_evento.currentText(),
        }

    def reset_form(self) -> None:
        """Azzera tutti i campi del form."""
        self.input_titolo.clear()
        self.select_opera.setCurrentIndex(0)
        self.select_regia.setCurrentIndex(0)
        self.select_tipo_evento.setCurrentIndex(0)

    # ------------------------------------------------------------------
    def __on_salva_clicked(self) -> None:
        dati = self.get_dati_form()
        if not dati["titolo"] or dati["opera"] == "Seleziona l'Opera" or dati["regia"] == "Seleziona la Regia":
            return  # qui eventualmente mostrare un messaggio di errore
        self.spettacolo_salvato.emit(dati)

    def __on_annulla_clicked(self) -> None:
        self.reset_form()
        self.annullato.emit()


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication, QMessageBox
    from typing import Dict

    app = QApplication(sys.argv)
    finestra = CreaSpettacoloView()  

    # Callback chiamata quando il segnale viene emesso
    def on_salvato(dati: Dict[str, str]) -> None:
        """Mostra un messaggio di conferma con i dati dello spettacolo."""
        QMessageBox.information(finestra, "Spettacolo Salvato", str(dati))

    # Connessione del segnale corretto
    finestra.spettacolo_salvato.connect(on_salvato)

    # Callback per annullamento
    def on_annullato() -> None:
        QMessageBox.information(finestra, "Annullato", "Operazione annullata")

    finestra.annullato.connect(on_annullato)

    finestra.show()
    sys.exit(app.exec())
