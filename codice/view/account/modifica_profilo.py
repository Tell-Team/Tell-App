from typing import Dict
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QComboBox,
    QPushButton, QFormLayout, QHBoxLayout, QVBoxLayout, QMessageBox
)


class ModificaProfiloView(QWidget):
    """
    View per la modifica di un profilo utente.
    Contiene campi anagrafici, credenziali e ruolo, con bottoni per
    eliminazione account, annullamento e salvataggio modifiche.

    Segnali:
    - account_modificato(dict): emesso quando l'utente clicca 'Salva Modifiche' con dati validi
    - annullato(): emesso quando l'utente clicca 'Annulla'
    - account_eliminato(str): emesso quando l'utente clicca 'Elimina Account' con username
    """

    account_modificato = pyqtSignal(object)
    annullato = pyqtSignal()
    account_eliminato = pyqtSignal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.__setup_ui()

    def __setup_ui(self) -> None:
        """Costruisce la UI della schermata di modifica profilo."""

        # Titolo
        self.__titolo = QLabel("Modifica Account: [Nome Cognome Utente]")
        self.__titolo.setStyleSheet("font-size: 18pt; font-weight: bold;")

        # Campi anagrafica
        self.__nome_input = QLineEdit()
        self.__nome_input.setPlaceholderText("Nome")
        self.__cognome_input = QLineEdit()
        self.__cognome_input.setPlaceholderText("Cognome")

        # Campi accesso e ruolo
        self.__username_input = QLineEdit()
        self.__username_input.setPlaceholderText("Username")
        self.__password_input = QLineEdit()
        self.__password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.__password_input.setPlaceholderText("Lascia vuoto per non modificare la password")

        self.__ruolo_select = QComboBox()
        self.__ruolo_select.addItem("Seleziona un Ruolo", "")
        self.__ruolo_select.addItem("Amministratore", "amministratore")
        self.__ruolo_select.addItem("Biglietteria", "biglietteria")
        self.__ruolo_select.addItem("Cliente", "cliente")

        # Bottoni
        self.__btn_elimina = QPushButton("Elimina Account")
        self.__btn_elimina.setStyleSheet("background-color: #dc3545; color: white;")
        self.__btn_annulla = QPushButton("Annulla")
        self.__btn_annulla.setStyleSheet("background-color: #6c757d; color: white;")
        self.__btn_salva = QPushButton("Salva Modifiche")
        self.__btn_salva.setStyleSheet("background-color: #007bff; color: white;")
        self.__btn_salva.setDefault(True)

        # Layout form
        form_layout = QFormLayout()
        form_layout.addRow(QLabel(""), self.__titolo)
        form_layout.addRow("Nome *", self.__nome_input)
        form_layout.addRow("Cognome *", self.__cognome_input)
        form_layout.addRow("Username *", self.__username_input)
        form_layout.addRow("Nuova Password", self.__password_input)
        form_layout.addRow("Ruolo *", self.__ruolo_select)

        # Layout bottoni
        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.__btn_elimina)
        btn_layout.addWidget(self.__btn_annulla)
        btn_layout.addWidget(self.__btn_salva)

        # Layout principale
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)
        self.setMinimumWidth(550)
        self.setWindowTitle("Modifica Profilo Utente")

        # Connessioni bottoni
        self.__btn_salva.clicked.connect(self.__on_salva_clicked)
        self.__btn_annulla.clicked.connect(self.__on_annulla_clicked)
        self.__btn_elimina.clicked.connect(self.__on_elimina_clicked)

    # ------------------------- METODI PUBBLICI -------------------------
    def set_titolo(self, nome: str, cognome: str) -> None:
        """Aggiorna il titolo con nome e cognome dell'utente."""
        self.__titolo.setText(f"Modifica Account: {nome} {cognome}")

    def get_dati_form(self) -> Dict[str, str]:
        """Restituisce i valori correnti del form come dict."""
        return {
            "nome": self.__nome_input.text().strip(),
            "cognome": self.__cognome_input.text().strip(),
            "username": self.__username_input.text().strip(),
            "password": self.__password_input.text().strip(),
            "ruolo": str(self.__ruolo_select.currentData()),
        }

    def set_dati_form(self, dati: Dict[str, str]) -> None:
        """Popola i campi della form con i dati esistenti."""
        self.__nome_input.setText(dati.get("nome", ""))
        self.__cognome_input.setText(dati.get("cognome", ""))
        self.__username_input.setText(dati.get("username", ""))
        self.__password_input.clear()
        ruolo_val = dati.get("ruolo", "")
        index = self.__ruolo_select.findData(ruolo_val)
        if index >= 0:
            self.__ruolo_select.setCurrentIndex(index)
        else:
            self.__ruolo_select.setCurrentIndex(0)

    def reset_form(self) -> None:
        """Azzera tutti i campi del form."""
        self.__nome_input.clear()
        self.__cognome_input.clear()
        self.__username_input.clear()
        self.__password_input.clear()
        self.__ruolo_select.setCurrentIndex(0)

    # ------------------------- METODI PRIVATI -------------------------
    def __mostra_errore(self, titolo: str, testo: str) -> None:
        QMessageBox.critical(self, titolo, testo)

    def __valida_dati(self) -> bool:
        """Controlla campi obbligatori: nome, cognome, username e ruolo."""
        if not self.__nome_input.text().strip():
            self.__mostra_errore("Valore mancante", "Il campo 'Nome' è obbligatorio.")
            return False
        if not self.__cognome_input.text().strip():
            self.__mostra_errore("Valore mancante", "Il campo 'Cognome' è obbligatorio.")
            return False
        if not self.__username_input.text().strip():
            self.__mostra_errore("Valore mancante", "Il campo 'Username' è obbligatorio.")
            return False
        if not self.__ruolo_select.currentData():
            self.__mostra_errore("Ruolo non selezionato", "Seleziona un ruolo per l'account.")
            return False
        return True

    def __on_salva_clicked(self) -> None:
        if not self.__valida_dati():
            return
        dati = self.get_dati_form()
        self.account_modificato.emit(dati)

    def __on_annulla_clicked(self) -> None:
        self.reset_form()
        self.annullato.emit()

    def __on_elimina_clicked(self) -> None:
        username = self.__username_input.text().strip()
        if username:
            self.account_eliminato.emit(username)
        else:
            self.__mostra_errore("Errore", "Impossibile eliminare un account senza username.")


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication, QMessageBox
    from typing import Any

    app = QApplication(sys.argv)
    finestra = ModificaProfiloView()

    # Callback per segnale account_modificato
    def on_modificato(dati: Any) -> None:
        QMessageBox.information(finestra, "Modificato", str(dati))

    # Callback per segnale annullato
    def on_annullato() -> None:
        QMessageBox.information(finestra, "Annullato", "Operazione annullata")

    # Callback per segnale account_eliminato
    def on_eliminato(username: str) -> None:
        QMessageBox.information(finestra, "Eliminato", f"Account eliminato: {username}")

    finestra.account_modificato.connect(on_modificato)
    finestra.annullato.connect(on_annullato)
    finestra.account_eliminato.connect(on_eliminato)

    finestra.show()
    sys.exit(app.exec())
