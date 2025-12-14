from typing import Dict

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QFormLayout,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox,
)


class CreaProfiloView(QWidget):
    """
    View per la creazione di un nuovo account (solo la parte grafica).

    Segnali:
    - account_creato(dict): emesso quando l'utente clicca "Crea Account" con dati validi
    - annullato(): emesso quando l'utente clicca "Annulla"
    """

    account_creato = pyqtSignal(object)  # emette un dict con i valori del form
    annullato = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        """Inizializza la view.

        :param parent: widget genitore opzionale
        :raises: nessuna eccezione prevista direttamente da questo costruttore
        """
        super().__init__(parent)
        self.__setup_ui()

    def __setup_ui(self) -> None:
        """Costruisce e dispone i widget della form.

        Metodo privato utilizzato solo nel costruttore per separare la logica di inizializzazione.
        """
        # Labels
        self.__titolo = QLabel("Aggiungi Nuovo Account")
        self.__titolo.setStyleSheet("font-size: 18pt; font-weight: bold;")

        # Campi anagrafica
        self.__nome_input: QLineEdit = QLineEdit()
        self.__nome_input.setPlaceholderText("Nome")

        self.__cognome_input: QLineEdit = QLineEdit()
        self.__cognome_input.setPlaceholderText("Cognome")

        # Accesso e ruolo
        self.__username_input: QLineEdit = QLineEdit()
        self.__username_input.setPlaceholderText("Username")

        self.__password_input: QLineEdit = QLineEdit()
        self.__password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.__password_input.setPlaceholderText("Password")

        self.__ruolo_select: QComboBox = QComboBox()
        self.__ruolo_select.addItem("Seleziona un Ruolo", "")
        self.__ruolo_select.addItem("Amministratore", "amministratore")
        self.__ruolo_select.addItem("Biglietteria", "biglietteria")
        self.__ruolo_select.addItem("Cliente", "cliente")

        # Bottoni
        self.__btn_annulla: QPushButton = QPushButton("Annulla")
        self.__btn_crea: QPushButton = QPushButton("Crea Account")
        self.__btn_crea.setDefault(True)

        # Layout form
        form_layout = QFormLayout()
        form_layout.addRow(QLabel(""), self.__titolo)
        form_layout.addRow("Nome *", self.__nome_input)
        form_layout.addRow("Cognome *", self.__cognome_input)
        form_layout.addRow("", QLabel(""))  # separatore visuale
        form_layout.addRow("Username *", self.__username_input)
        form_layout.addRow("Password *", self.__password_input)
        form_layout.addRow("Ruolo *", self.__ruolo_select)

        # Layout bottoni orizzontale
        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.__btn_annulla)
        btn_layout.addWidget(self.__btn_crea)

        # Layout principale verticale
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

        # Connessioni
        self.__btn_crea.clicked.connect(self.__on_crea_clicked)
        self.__btn_annulla.clicked.connect(self.__on_annulla_clicked)

    def __mostra_errore(self, titolo: str, testo: str) -> None:
        """Mostra un messaggio di errore all'utente.

        :param titolo: titolo della finestra di errore
        :param testo: testo descrittivo
        :raises: nessuna eccezione; mostra una QMessageBox
        """
        QMessageBox.critical(self, titolo, testo)

    def __on_crea_clicked(self) -> None:
        """Callback privato chiamato quando l'utente clicca 'Crea Account'.

        Valida i dati, emette il segnale account_creato con un dict se i dati sono validi.
        :raises: nessuna eccezione - in caso di dati non validi mostra un errore all'utente
        """
        try:
            if not self.__valida_dati():
                return

            dati: Dict[str, str] = self.get_dati_form()
            # Emissione del segnale con i dati raccolti
            self.account_creato.emit(dati)

        except Exception as exc:  # pragma: no cover - gestito a livello UI
            # In produzione potresti loggare l'eccezione
            self.__mostra_errore("Errore interno", f"Si è verificato un errore: {exc}")

    def __on_annulla_clicked(self) -> None:
        """Callback privato chiamato quando l'utente clicca 'Annulla'.

        Pulisce la form e emette il segnale annullato.
        """
        self.reset_form()
        self.annullato.emit()

    def __valida_dati(self) -> bool:
        """Esegue controlli base sui campi obbligatori.

        Controlli eseguiti:
        - nome, cognome, username e password non vuoti
        - ruolo selezionato

        :returns: True se la validazione passa, False altrimenti
        :raises: nessuna eccezione prevista
        """
        if not self.__nome_input.text().strip():
            self.__mostra_errore("Valore mancante", "Il campo 'Nome' è obbligatorio.")
            return False
        if not self.__cognome_input.text().strip():
            self.__mostra_errore("Valore mancante", "Il campo 'Cognome' è obbligatorio.")
            return False
        if not self.__username_input.text().strip():
            self.__mostra_errore("Valore mancante", "Il campo 'Username' è obbligatorio.")
            return False
        if not self.__password_input.text().strip():
            self.__mostra_errore("Valore mancante", "Il campo 'Password' è obbligatorio.")
            return False
        if not self.__ruolo_select.currentData():
            self.__mostra_errore("Ruolo non selezionato", "Seleziona un ruolo per l'account.")
            return False
        return True

    def get_dati_form(self) -> Dict[str, str]:
        """Restituisce i valori correnti del form come dict.

        :returns: dizionario con chiavi: nome, cognome, username, password, ruolo
        :raises: nessuna eccezione prevista
        """
        return {
            "nome": self.__nome_input.text().strip(),
            "cognome": self.__cognome_input.text().strip(),
            "username": self.__username_input.text().strip(),
            "password": self.__password_input.text().strip(),
            "ruolo": str(self.__ruolo_select.currentData()),
        }

    def reset_form(self) -> None:
        """Azzera tutti i campi della form.

        :raises: nessuna eccezione prevista
        """
        self.__nome_input.clear()
        self.__cognome_input.clear()
        self.__username_input.clear()
        self.__password_input.clear()
        self.__ruolo_select.setCurrentIndex(0)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication, QMessageBox
    from typing import Any

    app = QApplication(sys.argv)
    finestra = CreaProfiloView()

    # Callback per segnale account_creato
    def on_creato(dati: Any) -> None:
        QMessageBox.information(finestra, "Dati ricevuti", str(dati))

    # Callback per segnale annullato
    def on_annullato() -> None:
        QMessageBox.information(finestra, "Annullato", "Operazione annullata")

    finestra.account_creato.connect(on_creato)
    finestra.annullato.connect(on_annullato)

    finestra.show()
    sys.exit(app.exec())
