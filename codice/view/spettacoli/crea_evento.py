from typing import Dict, Any, Optional
from PyQt6.QtCore import pyqtSignal, QDate, QTime
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QComboBox,
    QPushButton,
    QFormLayout,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox,
    QDateEdit,
    QTimeEdit,
    QCheckBox,
    QLineEdit,
)
from PyQt6.QtGui import QFont, QIntValidator


class CreaEventoView(QWidget):
    """
    View per l'aggiunta di un nuovo Evento (Replica di uno Spettacolo).

    Permette di definire data, ora, sala, stato di pubblicazione e opzioni di prezzo/posti.

    Segnali:
    - evento_creato(dict): emesso quando l'utente clicca 'Salva Evento' con dati validi.
    - annullato(): emesso quando l'utente clicca 'Annulla'.
    - modifica_mappa_posti_richiesta(): emesso quando l'utente clicca 'Vedi/Modifica Mappa Posti'.
    """

    evento_creato = pyqtSignal(object)
    annullato = pyqtSignal()
    modifica_mappa_posti_richiesta = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Inizializza la view per la creazione di un nuovo evento.

        :param parent: widget genitore. (?)
        :raises: nessuna eccezione prevista direttamente da questo costruttore.
        """
        super().__init__(parent)
        self.__setup_ui()

    # ------------------------- SETUP UI -------------------------

    def __setup_ui(self) -> None:
        """
        Costruisce e dispone i widget della form per la creazione evento.
        """
        self.setWindowTitle("Aggiungi Nuovo Evento (Replica)")
        self.setMinimumWidth(550)

        # 1. Titolo
        self.__titolo: QLabel = QLabel("Aggiungi Nuovo Evento (Replica)")
        self.__titolo.setStyleSheet(
            "font-size: 18pt; font-weight: bold; border-bottom: 2px solid #ccc;"
        )
        self.__titolo.setContentsMargins(0, 0, 0, 10)

        # 2. Campi Data e Luogo (Gestiti in una griglia per l'allineamento affiancato)

        # Input Data e Ora
        self.__data_input: QDateEdit = QDateEdit(calendarPopup=True)
        self.__data_input.setDate(QDate.currentDate())
        self.__data_input.setDisplayFormat("dd/MM/yyyy")

        self.__ora_input: QTimeEdit = QTimeEdit()
        self.__ora_input.setTime(QTime(21, 0))  # Default ora serale
        self.__ora_input.setDisplayFormat("HH:mm")

        # Input Sala
        self.__sala_select: QComboBox = QComboBox()
        self.__sala_select.addItem("Seleziona Sala", "")
        self.__sala_select.addItem("Sala Grande", "sala_grande")
        self.__sala_select.addItem("Sala Piccolo Teatro", "sala_piccola")

        # Input Stato Pubblicazione
        self.__stato_pubblicazione_select: QComboBox = QComboBox()
        self.__stato_pubblicazione_select.addItem("Bozza (Non in vendita)", "bozza")
        self.__stato_pubblicazione_select.addItem(
            "Pubblicato (In vendita)", "pubblicato"
        )
        self.__stato_pubblicazione_select.addItem("Annullato", "annullato")

        # Layout Data e Ora Affiancati (Simulazione form-row)
        data_ora_layout: QHBoxLayout = QHBoxLayout()
        data_ora_layout.addWidget(QLabel("Data Evento *"))
        data_ora_layout.addWidget(self.__data_input)
        data_ora_layout.addWidget(QLabel("Ora Evento *"))
        data_ora_layout.addWidget(self.__ora_input)

        # Layout Dettagli (Form Layout per il resto)
        dettagli_layout: QFormLayout = QFormLayout()
        dettagli_layout.addRow(QLabel("<h2>Dettagli Data e Luogo</h2>"))
        dettagli_layout.addRow(data_ora_layout)
        dettagli_layout.addRow(QLabel("Luogo/Sala *"), self.__sala_select)
        dettagli_layout.addRow(
            QLabel("Stato Pubblicazione *"), self.__stato_pubblicazione_select
        )

        # 3. Prezzo e Posti

        self.__override_prezzo_check: QCheckBox = QCheckBox(
            "Applica Prezzo Manuale (Override del prezzo dello Spettacolo)"
        )
        self.__override_prezzo_check.stateChanged.connect(self.__toggle_prezzo_manuale)

        # Campo per il prezzo manuale (visibile solo se il checkbox è spuntato)
        self.__prezzo_input: QLineEdit = QLineEdit()
        self.__prezzo_input.setPlaceholderText("Prezzo in EUR (es. 25.00)")
        self.__prezzo_input.setVisible(False)
        self.__prezzo_input.setValidator(
            QIntValidator(0, 9999)
        )  # Esempio di validatore numerico

        self.__btn_mappa_posti: QPushButton = QPushButton("Vedi/Modifica Mappa Posti")
        self.__btn_mappa_posti.setStyleSheet(
            "margin-top: 10px;"
        )  # Stile per spaziatura

        # Layout Prezzo e Posti
        prezzo_posti_layout: QVBoxLayout = QVBoxLayout()
        prezzo_posti_layout.addWidget(QLabel("<h3>Prezzo e Posti</h3>"))
        prezzo_posti_layout.addWidget(self.__override_prezzo_check)
        prezzo_posti_layout.addWidget(self.__prezzo_input)
        prezzo_posti_layout.addWidget(self.__btn_mappa_posti)

        # 4. Bottoni Azioni
        self.__btn_annulla: QPushButton = QPushButton("Annulla")
        self.__btn_annulla.setStyleSheet("background-color: #6c757d; color: white;")
        self.__btn_salva: QPushButton = QPushButton("Salva Evento")
        self.__btn_salva.setStyleSheet("background-color: #28a745; color: white;")
        self.__btn_salva.setDefault(True)

        btn_layout: QHBoxLayout = QHBoxLayout()
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.__btn_annulla)
        btn_layout.addWidget(self.__btn_salva)

        # 5. Layout Principale Verticale
        main_layout: QVBoxLayout = QVBoxLayout(self)
        main_layout.addWidget(self.__titolo)
        main_layout.addLayout(dettagli_layout)
        main_layout.addWidget(QLabel("<hr>"))
        main_layout.addLayout(prezzo_posti_layout)
        main_layout.addWidget(QLabel("<hr>"))  # Separatore per i bottoni
        main_layout.addLayout(btn_layout)
        main_layout.addStretch(1)
        main_layout.setSpacing(15)

        # Connessioni
        self.__btn_salva.clicked.connect(self.__on_salva_clicked)
        self.__btn_annulla.clicked.connect(self.__on_annulla_clicked)
        self.__btn_mappa_posti.clicked.connect(self.modifica_mappa_posti_richiesta.emit)

    # ------------------------- METODI PRIVATI DI GESTIONE UI -------------------------

    def __toggle_prezzo_manuale(self, stato: int) -> None:
        """
        Mostra o nasconde il campo di input del prezzo in base allo stato del checkbox.

        :param stato: 2 se checkato (Qt.Checked), 0 se non checkato (Qt.Unchecked).
        :raises: nessuna eccezione prevista.
        """
        # stato == Qt.Checked (2)
        self.__prezzo_input.setVisible(stato == 2)
        if stato == 0:
            self.__prezzo_input.clear()

    def __mostra_errore(self, titolo: str, testo: str) -> None:
        """
        Mostra un messaggio di errore all'utente.

        :param titolo: titolo della finestra di errore.
        :param testo: testo descrittivo.
        :raises: nessuna eccezione; mostra una QMessageBox.
        """
        QMessageBox.critical(self, titolo, testo)

    # ------------------------- METODI PUBBLICI DI INTERFACCIA -------------------------

    def get_dati_form(self) -> Dict[str, Any]:
        """
        Restituisce i valori correnti del form come dict.

        :returns: dizionario con chiavi: data, ora, sala, stato_pubblicazione, override_prezzo, prezzo_manuale.
        :raises: nessuna eccezione prevista.
        """
        override: bool = self.__override_prezzo_check.isChecked()
        prezzo_manuale: Optional[float] = None

        if override and self.__prezzo_input.text().strip():
            # Assumiamo che l'input sia gestito come stringa per i decimali, sebbene QIntValidator sia stato usato per esempio.
            try:
                prezzo_manuale = float(
                    self.__prezzo_input.text().replace(",", ".").strip()
                )
            except ValueError:
                # In caso di errore (se avessimo usato un LineEdit senza validatore)
                prezzo_manuale = 0.0

        return {
            "data": self.__data_input.date().toString(
                Qt.DateFormat.ISODate
            ),  # Es. 2025-12-14
            "ora": self.__ora_input.time().toString(
                Qt.DateFormat.ISODate
            ),  # Es. 21:00:00
            "sala": str(self.__sala_select.currentData()),
            "stato_pubblicazione": str(self.__stato_pubblicazione_select.currentData()),
            "override_prezzo": override,
            "prezzo_manuale": prezzo_manuale,
        }

    def reset_form(self) -> None:
        """
        Azzera tutti i campi della form ai valori di default.

        :raises: nessuna eccezione prevista.
        """
        self.__data_input.setDate(QDate.currentDate())
        self.__ora_input.setTime(QTime(21, 0))
        self.__sala_select.setCurrentIndex(0)
        self.__stato_pubblicazione_select.setCurrentIndex(0)
        self.__override_prezzo_check.setChecked(False)
        self.__prezzo_input.clear()
        self.__prezzo_input.setVisible(False)

    # ------------------------- VALIDAZIONE E CALLBACKS -------------------------

    def __valida_dati(self) -> bool:
        """
        Esegue controlli base sui campi obbligatori.

        Controlli: data, ora, sala, stato_pubblicazione non vuoti.
        Inoltre, se 'override_prezzo' è attivo, il prezzo manuale deve essere un valore numerico valido.

        :returns: True se la validazione passa, False altrimenti.
        :raises: nessuna eccezione prevista.
        """
        if not self.__sala_select.currentData():
            self.__mostra_errore(
                "Valore mancante", "Il campo 'Luogo/Sala' è obbligatorio."
            )
            return False

        # Data e ora sono quasi sempre validi se usiamo QDateEdit/QTimeEdit,
        # ma controllare per completezza la selezione Sala e Stato
        if not self.__stato_pubblicazione_select.currentData():
            self.__mostra_errore(
                "Valore mancante", "Il campo 'Stato Pubblicazione' è obbligatorio."
            )
            return False

        if self.__override_prezzo_check.isChecked():
            prezzo_str: str = self.__prezzo_input.text().strip().replace(",", ".")
            if not prezzo_str:
                self.__mostra_errore(
                    "Valore mancante",
                    "Se l'Override Prezzo è attivo, il prezzo manuale è obbligatorio.",
                )
                return False
            try:
                if float(prezzo_str) < 0:
                    self.__mostra_errore(
                        "Valore non valido", "Il prezzo non può essere negativo."
                    )
                    return False
            except ValueError:
                self.__mostra_errore(
                    "Formato non valido",
                    "Il prezzo manuale deve essere un numero valido.",
                )
                return False

        return True

    def __on_salva_clicked(self) -> None:
        """
        Callback privato chiamato quando l'utente clicca 'Salva Evento'.

        Valida i dati ed emette il segnale 'evento_creato' se validi.
        """
        if not self.__valida_dati():
            return

        dati: Dict[str, Any] = self.get_dati_form()
        self.evento_creato.emit(dati)

    def __on_annulla_clicked(self) -> None:
        """
        Callback privato chiamato quando l'utente clicca 'Annulla'.

        Pulisce la form ed emette il segnale 'annullato'.
        """
        self.reset_form()
        self.annullato.emit()


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    finestra = CreaEventoView()

    def on_evento_creato(dati: Any) -> None:
        print("\n--- EVENTO CREATO ---")
        QMessageBox.information(finestra, "Dati Evento", str(dati))

    def on_mappa_richiesta() -> None:
        QMessageBox.information(
            finestra, "Azione", "Richiesta di Modifica Mappa Posti."
        )

    finestra.evento_creato.connect(on_evento_creato)
    finestra.modifica_mappa_posti_richiesta.connect(on_mappa_richiesta)
    finestra.annullato.connect(
        lambda: QMessageBox.information(
            finestra, "Annullato", "Creazione evento annullata"
        )
    )

    finestra.show()
    sys.exit(app.exec())
