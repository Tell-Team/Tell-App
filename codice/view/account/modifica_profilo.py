from typing import Dict, Any, Optional
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QFormLayout, QHBoxLayout, QVBoxLayout, QMessageBox
)

class ModificaProfiloView(QWidget):
    """
    View per la modifica del profilo utente (Amministratore, Biglietteria e Cliente).

    Permette di modificare nome, email e password attuale/nuova.

    Segnali:
    - profilo_modificato(dict): emesso quando si salvano i nuovi dati.
    - annullato(): emesso quando l'utente annulla l'operazione.
    """

    profilo_modificato = pyqtSignal(object)
    annullato = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Inizializza la view del profilo.

        :param parent: widget genitore.(?)
        :raises: nessuna eccezione prevista.
        """
        super().__init__(parent)
        self.__setup_ui()

    def __setup_ui(self) -> None:
        """
        Costruisce l'interfaccia grafica.
        """
        self.setWindowTitle("Modifica Profilo")
        self.setMinimumWidth(400)

        self.__titolo: QLabel = QLabel("<h2>Il Mio Profilo</h2>")

        # Campi Input (Privati)
        self.__input_nome: QLineEdit = QLineEdit()
        self.__input_email: QLineEdit = QLineEdit()
        
        self.__input_old_password: QLineEdit = QLineEdit()
        self.__input_old_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.__input_old_password.setPlaceholderText("Richiesta per confermare modifiche")

        self.__input_new_password: QLineEdit = QLineEdit()
        self.__input_new_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.__input_new_password.setPlaceholderText("Lascia vuoto per non cambiare")

        # Bottoni
        self.__btn_salva: QPushButton = QPushButton("Salva Modifiche")
        self.__btn_salva.setStyleSheet("background-color: #007bff; color: white; font-weight: bold;")
        
        self.__btn_annulla: QPushButton = QPushButton("Annulla")
        self.__btn_annulla.setStyleSheet("background-color: #6c757d; color: white;")

        # Layout
        form_layout = QFormLayout()
        form_layout.addRow("Nome Utente:", self.__input_nome)
        form_layout.addRow("Email:", self.__input_email)
        form_layout.addRow(QLabel("<hr>"))
        form_layout.addRow("Nuova Password:", self.__input_new_password)
        form_layout.addRow("Password Attuale *:", self.__input_old_password)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.__btn_annulla)
        btn_layout.addWidget(self.__btn_salva)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.__titolo)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(btn_layout)

        # Connessioni
        self.__btn_salva.clicked.connect(self.__on_salva_clicked)
        self.__btn_annulla.clicked.connect(self.__on_annulla_clicked)

    # ------------------------- METODI PUBBLICI -------------------------

    def set_dati_form(self, dati: Dict[str, Any]) -> None:
        """
        Popola i campi con i dati attuali dell'utente.

        :param dati: Dizionario con chiavi 'nome', 'email'.
        :raises: nessuna eccezione prevista.
        """
        self.__input_nome.setText(dati.get("nome", ""))
        self.__input_email.setText(dati.get("email", ""))
        self.__input_old_password.clear()
        self.__input_new_password.clear()

    def get_dati_form(self) -> Dict[str, Any]:
        """
        Restituisce i dati inseriti nel form.

        :return: Dict con nome, email, old_password, new_password.
        :raises: nessuna eccezione prevista.
        """
        return {
            "nome": self.__input_nome.text().strip(),
            "email": self.__input_email.text().strip(),
            "old_password": self.__input_old_password.text(),
            "new_password": self.__input_new_password.text()
        }

    def reset_form(self) -> None:
        """
        Pulisce i campi password.
        
        :raises: nessuna eccezione prevista.
        """
        self.__input_old_password.clear()
        self.__input_new_password.clear()

    # ------------------------- VALIDAZIONE E CALLBACKS -------------------------

    def __valida_dati(self) -> bool:
        """
        Verifica i campi obbligatori.

        :return: True se validi, False altrimenti.
        :raises: nessuna eccezione prevista.
        """
        if not self.__input_nome.text().strip():
            self.__mostra_errore("Errore", "Il nome non può essere vuoto.")
            return False
        if not self.__input_email.text().strip():
            self.__mostra_errore("Errore", "L'email non può essere vuota.")
            return False
        if not self.__input_old_password.text():
            self.__mostra_errore("Errore", "Inserisci la password attuale per confermare.")
            return False
        return True

    def __on_salva_clicked(self) -> None:
        """
        Gestisce il salvataggio.
        
        :raises: nessuna eccezione prevista.
        """
        if self.__valida_dati():
            self.profilo_modificato.emit(self.get_dati_form())

    def __on_annulla_clicked(self) -> None:
        """
        Gestisce l'annullamento.
        
        :raises: nessuna eccezione prevista.
        """
        self.reset_form()
        self.annullato.emit()

    def __mostra_errore(self, titolo: str, messaggio: str) -> None:
        """
        Mostra popup errore.
        
        :raises: nessuna eccezione prevista.
        """
        QMessageBox.warning(self, titolo, messaggio)