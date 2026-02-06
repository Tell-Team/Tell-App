from typing import Dict, Any, Optional
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QFormLayout,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox,
    QSpinBox,
)


class ModificaSpettacoloView(QWidget):
    """
    View per la modifica di uno Spettacolo esistente.

    Estende la logica di creazione aggiungendo la possibilità di
    popolare i campi ed eliminare lo spettacolo.

    Segnali:
    - spettacolo_modificato(dict): emesso quando si salvano modifiche valide.
    - spettacolo_eliminato(): emesso dopo la conferma di eliminazione.
    - annullato(): emesso quando si annulla l'operazione.
    """

    spettacolo_modificato = pyqtSignal(object)
    spettacolo_eliminato = pyqtSignal()
    annullato = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Inizializza la view.

        :param parent: widget genitore.(?)
        :raises: nessuna eccezione prevista.
        """
        super().__init__(parent)
        # Variabile per tracciare l'ID dello spettacolo in modifica (? ma utile)
        self.__id_spettacolo_corrente: Optional[int] = None
        self.__setup_ui()

    def __setup_ui(self) -> None:
        """
        Costruisce l'interfaccia grafica per la modifica.
        """
        self.setWindowTitle("Modifica Spettacolo")
        self.setMinimumWidth(400)

        self.__titolo_label: QLabel = QLabel("<h2>Modifica Spettacolo</h2>")

        # Widget Input (Privati)
        self.__input_titolo: QLineEdit = QLineEdit()
        self.__input_descrizione: QTextEdit = QTextEdit()
        self.__input_durata: QSpinBox = QSpinBox()
        self.__input_durata.setRange(1, 300)
        self.__input_durata.setSuffix(" min")

        # Bottoni
        self.__btn_salva: QPushButton = QPushButton("Salva Modifiche")
        self.__btn_salva.setStyleSheet(
            "background-color: #007bff; color: white; font-weight: bold;"
        )

        self.__btn_elimina: QPushButton = QPushButton("Elimina Spettacolo")
        self.__btn_elimina.setStyleSheet("background-color: #dc3545; color: white;")

        self.__btn_annulla: QPushButton = QPushButton("Annulla")
        self.__btn_annulla.setStyleSheet("background-color: #6c757d; color: white;")

        # Layout Form
        form_layout = QFormLayout()
        form_layout.addRow("Titolo *:", self.__input_titolo)
        form_layout.addRow("Descrizione:", self.__input_descrizione)
        form_layout.addRow("Durata (minuti) *:", self.__input_durata)

        # Layout Bottoni
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.__btn_elimina)
        btn_layout.addStretch()
        btn_layout.addWidget(self.__btn_annulla)
        btn_layout.addWidget(self.__btn_salva)

        # Layout Principale
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.__titolo_label)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(btn_layout)

        # Connessioni
        self.__btn_salva.clicked.connect(self.__on_salva_clicked)
        self.__btn_elimina.clicked.connect(self.__on_elimina_clicked)
        self.__btn_annulla.clicked.connect(self.__on_annulla_clicked)

    # ------------------------- METODI PUBBLICI -------------------------

    def set_dati_form(self, dati: Dict[str, Any]) -> None:
        """
        Popola il form con i dati dello spettacolo esistente.

        :param dati: Dict contenente 'titolo', 'descrizione', 'durata', e opzionalmente 'id'.
        :raises: nessuna eccezione prevista.
        """
        self.__id_spettacolo_corrente = dati.get(
            "id"
        )  # modificabile con "id_spettacolo"(?)

        self.__input_titolo.setText(dati.get("titolo", ""))
        self.__input_descrizione.setText(dati.get("descrizione", ""))
        self.__input_durata.setValue(int(dati.get("durata", 60)))

        # Aggiornamento titolo finestra per feedback visivo
        if self.__id_spettacolo_corrente:
            self.__titolo_label.setText(
                f"<h2>Modifica Spettacolo #{self.__id_spettacolo_corrente}</h2>"
            )

    def get_dati_form(self) -> Dict[str, Any]:
        """
        Restituisce i dati correnti del form.

        :return: Dict con i nuovi valori inseriti.
        :raises: nessuna eccezione prevista.
        """
        return {
            "id": self.__id_spettacolo_corrente,
            "titolo": self.__input_titolo.text().strip(),
            "descrizione": self.__input_descrizione.toPlainText().strip(),
            "durata": self.__input_durata.value(),
        }

    def reset_form(self) -> None:
        """
        Pulisce i campi e l'ID corrente.

        :raises: nessuna eccezione prevista.
        """
        self.__id_spettacolo_corrente = None
        self.__input_titolo.clear()
        self.__input_descrizione.clear()
        self.__input_durata.setValue(60)
        self.__titolo_label.setText("<h2>Modifica Spettacolo</h2>")

    # ------------------------- VALIDAZIONE E CALLBACKS -------------------------

    def __valida_dati(self) -> bool:
        """
        Verifica che i dati siano coerenti prima del salvataggio.

        :return: True se validi, False altrimenti.
        :raises: nessuna eccezione prevista.
        """
        if not self.__input_titolo.text().strip():
            self.__mostra_errore("Errore", "Il titolo è obbligatorio.")
            return False
        return True

    def __on_salva_clicked(self) -> None:
        """
        Gestisce il salvataggio delle modifiche.

        :raises: nessuna eccezione prevista.
        """
        if self.__valida_dati():
            self.spettacolo_modificato.emit(self.get_dati_form())

    def __on_elimina_clicked(self) -> None:
        """
        Chiede conferma e poi emette il segnale di eliminazione.

        :raises: nessuna eccezione prevista.
        """
        risposta = QMessageBox.question(
            self,
            "Conferma Eliminazione",
            "Sei sicuro di voler eliminare questo spettacolo? L'operazione è irreversibile.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if risposta == QMessageBox.StandardButton.Yes:
            self.spettacolo_eliminato.emit()

    def __on_annulla_clicked(self) -> None:
        """
        Gestisce l'annullamento.

        :raises: nessuna eccezione prevista.
        """
        self.annullato.emit()

    def __mostra_errore(self, titolo: str, messaggio: str) -> None:
        """
        Mostra popup di errore.

        :raises: nessuna eccezione prevista.
        """
        QMessageBox.critical(self, titolo, messaggio)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    finestra = ModificaSpettacoloView()

    # Esempio di utilizzo:

    def on_regia_creata(dati: Any) -> None:
        print("\n--- REGIA CREATA ---")
        print(f"Dati Base: {dati['nome_regia']}, {dati['regista']}, {dati['stagione']}")
        print(f"Dettagli Flessibili ({len(dati['dettagli'])}):")
        for dett in dati["dettagli"]:
            print(f"  - Ruolo: {dett['ruolo']}, Nominativo: {dett['nominativo']}")
        QMessageBox.information(
            finestra, "Dati Ricevuti", "Regia salvata con successo!"
        )

    def on_annullata() -> None:
        QMessageBox.information(finestra, "Annullato", "Operazione annullata")

    finestra.spettacolo_modificato.connect(on_regia_creata)
    finestra.annullato.connect(on_annullata)

    finestra.show()
    sys.exit(app.exec())
