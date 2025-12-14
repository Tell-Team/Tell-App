from typing import Dict, List, Any, Optional
from PyQt6.QtCore import pyqtSignal, QMargins, Qt
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QFormLayout, QHBoxLayout,
    QVBoxLayout, QMessageBox, QGridLayout, QScrollArea, QSizePolicy
)

# Definizione di un tipo per rappresentare il dettaglio di un ruolo
DettaglioRuolo = Dict[str, str]


class CreaRegiaView(QWidget):
    """
    View per la creazione di una nuova Regia (o edizione di un'Opera).

    Permette l'inserimento di dati base (nome, regista, stagione)
    e dettagli flessibili (ruolo: nominativo) gestiti tramite righe dinamiche.

    Segnali:
    - regia_creata(dict): emesso quando l'utente clicca 'Salva Nuova Regia' con dati validi.
    - annullata(): emesso quando l'utente clicca 'Annulla'.
    """

    regia_creata = pyqtSignal(object)  # emette un dict con i valori del form
    annullata = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Inizializza la view per la creazione di una nuova regia.

        :param parent: widget genitore opzionale.
        :raises: nessuna eccezione prevista direttamente da questo costruttore.
        """
        super().__init__(parent)
        # Lista che memorizza tutti i campi di input dinamici (Ruolo/Nominativo)
        self.__campi_dettagli: List[Dict[str, QLineEdit]] = []
        self.__setup_ui()

    # ------------------------- SETUP UI -------------------------

    def __setup_ui(self) -> None:
        """
        Costruisce e dispone i widget della form, creando l'interfaccia utente.
        """
        self.setWindowTitle("Aggiungi Nuova Regia")
        self.setMinimumWidth(650)

        # 1. Titolo
        self.__titolo: QLabel = QLabel("Aggiungi Nuova Regia per: [Titolo Opera]")
        self.__titolo.setStyleSheet("font-size: 18pt; font-weight: bold; border-bottom: 2px solid #ccc;")
        self.__titolo.setContentsMargins(0, 0, 0, 10)

        # 2. Dati Base Regia (FormLayout)
        self.__nome_regia_input: QLineEdit = QLineEdit()
        self.__nome_regia_input.setPlaceholderText("Es. Regia di [Nome] - Stagione [Anno]")
        self.__regista_input: QLineEdit = QLineEdit()
        self.__stagione_input: QLineEdit = QLineEdit()
        self.__stagione_input.setPlaceholderText("Es. 2025/2026")

        dati_base_layout: QFormLayout = QFormLayout()
        dati_base_layout.setContentsMargins(0, 10, 0, 10)
        dati_base_layout.addRow(QLabel("Nome Regia *"), self.__nome_regia_input)
        dati_base_layout.addRow(QLabel("Regista *"), self.__regista_input)
        dati_base_layout.addRow(QLabel("Stagione / Anno di Validità *"), self.__stagione_input)

        # 3. Dettagli Artistici e Tecnici Flessibili (QGridLayout in QScrollArea)

        # Layout per i dettagli (Griglia dove aggiungeremo le righe)
        self.__dettagli_grid_layout: QGridLayout = QGridLayout()
        self.__dettagli_grid_layout.setSpacing(5)
        # Intestazioni della tabella
        self.__dettagli_grid_layout.addWidget(QLabel("<b>Ruolo (Chiave)</b>"), 0, 0)
        self.__dettagli_grid_layout.addWidget(QLabel("<b>Nominativo (Valore)</b>"), 0, 1)
        self.__dettagli_grid_layout.addWidget(QLabel(""), 0, 2) # Per il bottone 'X'

        # Widget contenitore e Area di Scorrimento per i dettagli
        dettagli_container: QWidget = QWidget()
        dettagli_container.setLayout(self.__dettagli_grid_layout)

        scroll_area: QScrollArea = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(dettagli_container)
        scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        scroll_area.setMaximumHeight(200) # Limita l'altezza della tabella

        self.__btn_aggiungi_ruolo: QPushButton = QPushButton("+ Aggiungi Ruolo")
        self.__btn_aggiungi_ruolo.setStyleSheet("background-color: #17a2b8; color: white;")
        self.__btn_aggiungi_ruolo.clicked.connect(self.__aggiungi_riga_dettaglio)

        # Aggiungi una riga iniziale come da mockup
        self.__aggiungi_riga_dettaglio()


        # 4. Bottoni Azioni
        self.__btn_annulla: QPushButton = QPushButton("Annulla")
        self.__btn_salva: QPushButton = QPushButton("Salva Nuova Regia")
        self.__btn_salva.setStyleSheet("background-color: #28a745; color: white;")
        self.__btn_salva.setDefault(True)

        btn_layout: QHBoxLayout = QHBoxLayout()
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.__btn_annulla)
        btn_layout.addWidget(self.__btn_salva)

        # 5. Layout Principale Verticale
        main_layout: QVBoxLayout = QVBoxLayout(self)
        main_layout.addWidget(self.__titolo)
        main_layout.addWidget(QLabel("<h2>Dati Base Regia</h2>"))
        main_layout.addLayout(dati_base_layout)
        main_layout.addWidget(QLabel("<hr>"))
        main_layout.addWidget(QLabel("<h2>Dettagli Artistici e Tecnici Flessibili</h2>"))
        main_layout.addWidget(QLabel("<p>Aggiungere i membri del team (Direttore d'orchestra, Costumista, Scenografo, ecc.).</p>"))
        main_layout.addWidget(scroll_area)
        main_layout.addWidget(self.__btn_aggiungi_ruolo, alignment=Qt.AlignmentFlag.AlignLeft)
        main_layout.addLayout(btn_layout)
        main_layout.setSpacing(15)

        # Connessioni
        self.__btn_salva.clicked.connect(self.__on_salva_clicked)
        self.__btn_annulla.clicked.connect(self.__on_annulla_clicked)

    # ------------------------- METODI PUBBLICI -------------------------

    def set_titolo_opera(self, titolo_opera: str) -> None:
        """
        Imposta il titolo dell'opera a cui è associata questa regia.

        :param titolo_opera: il titolo dell'opera.
        :raises: nessuna eccezione prevista.
        """
        self.__titolo.setText(f"Aggiungi Nuova Regia per: {titolo_opera}")

    def get_dati_form(self) -> Dict[str, Any]:
        """
        Restituisce i valori correnti del form (dati base + dettagli) come dict.

        I dettagli flessibili vengono restituiti come lista di dizionari:
        `[{'ruolo': 'Costumista', 'nominativo': 'Tizio Caio'}, ...]`

        :returns: dizionario con chiavi: nome_regia, regista, stagione, dettagli.
        :raises: nessuna eccezione prevista.
        """
        return {
            "nome_regia": self.__nome_regia_input.text().strip(),
            "regista": self.__regista_input.text().strip(),
            "stagione": self.__stagione_input.text().strip(),
            "dettagli": self.__get_dettagli_form(),
        }

    def reset_form(self) -> None:
        """
        Azzera tutti i campi della form, inclusi i dettagli dinamici.

        :raises: nessuna eccezione prevista.
        """
        self.__nome_regia_input.clear()
        self.__regista_input.clear()
        self.__stagione_input.clear()
        self.__pulisci_dettagli()
        # Aggiunge una riga iniziale pulita
        self.__aggiungi_riga_dettaglio()


    # ------------------------- METODI PRIVATI DI GESTIONE DATI/UI -------------------------

    def __pulisci_dettagli(self) -> None:
        """
        Rimuove tutti i widget dinamici e svuota la lista di riferimento.

        :raises: nessuna eccezione prevista.
        """
        while self.__dettagli_grid_layout.count() > 3: # 3 sono le intestazioni
            item = self.__dettagli_grid_layout.takeAt(3) # Partiamo dalla quarta posizione (indice 3)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.__campi_dettagli.clear()


    def __aggiungi_riga_dettaglio(self, ruolo: str = "", nominativo: str = "") -> None:
        """
        Aggiunge una nuova riga (ruolo/nominativo/bottone X) alla griglia dei dettagli.

        :param ruolo: valore iniziale per il campo ruolo.
        :param nominativo: valore iniziale per il campo nominativo.
        :raises: nessuna eccezione prevista.
        """
        riga: int = len(self.__campi_dettagli) + 1 # +1 perché 0 è l'intestazione

        # Campi Input
        ruolo_input: QLineEdit = QLineEdit(ruolo)
        nominativo_input: QLineEdit = QLineEdit(nominativo)

        # Bottone Rimuovi
        btn_rimuovi: QPushButton = QPushButton("X")
        btn_rimuovi.setFixedSize(25, 25)
        btn_rimuovi.setStyleSheet("background-color: #dc3545; color: white; font-weight: bold;")

        # Memorizza i riferimenti ai campi e la loro riga
        nuova_riga: Dict[str, QLineEdit] = {
            "ruolo": ruolo_input,
            "nominativo": nominativo_input,
            "bottone": btn_rimuovi,
            "riga_indice": riga
        }
        self.__campi_dettagli.append(nuova_riga)

        # Aggiungi i widget alla griglia
        self.__dettagli_grid_layout.addWidget(ruolo_input, riga, 0)
        self.__dettagli_grid_layout.addWidget(nominativo_input, riga, 1)
        self.__dettagli_grid_layout.addWidget(btn_rimuovi, riga, 2)

        # Connessione per la rimozione
        # Usa lambda per passare l'oggetto riga quando il bottone è cliccato
        btn_rimuovi.clicked.connect(lambda: self.__rimuovi_riga_dettaglio(nuova_riga))


    def __rimuovi_riga_dettaglio(self, riga_da_rimuovere: Dict[str, Any]) -> None:
        """
        Rimuove i widget di una riga dinamica e aggiorna la lista.

        :param riga_da_rimuovere: Il dizionario che contiene i QLineEdit e il QPushButton da rimuovere.
        :raises: nessuna eccezione prevista.
        """
        try:
            # 1. Rimuovi i widget dalla UI
            riga_da_rimuovere["ruolo"].deleteLater()
            riga_da_rimuovere["nominativo"].deleteLater()
            riga_da_rimuovere["bottone"].deleteLater()

            # 2. Rimuovi il dizionario dalla lista di tracciamento
            self.__campi_dettagli.remove(riga_da_rimuovere)

            # 3. Ridisponi i widget rimanenti per eliminare lo spazio vuoto
            self.__aggiorna_layout_dettagli()

        except ValueError: # pragma: no cover
            # Questo non dovrebbe succedere se la logica è corretta
            self.__mostra_errore("Errore Interno", "Riferimento alla riga di dettaglio non trovato.")


    def __aggiorna_layout_dettagli(self) -> None:
        """
        Ridisegna tutti i widget dinamici sulla griglia dopo una rimozione.

        Questo è necessario in QGridLayout per far "collassare" le righe.
        :raises: nessuna eccezione prevista.
        """
        # Svuota (quasi) completamente la griglia, mantenendo solo l'intestazione
        while self.__dettagli_grid_layout.count() > 3:
            item = self.__dettagli_grid_layout.takeAt(3)
            widget = item.widget()
            if widget is not None:
                # Disaccoppia il widget, ma non lo distruggere ancora
                item.widget().setParent(None)

        # Reinserisce i widget dalla lista aggiornata
        for i, riga in enumerate(self.__campi_dettagli):
            nuova_riga = i + 1 # L'indice di riga effettivo
            self.__dettagli_grid_layout.addWidget(riga["ruolo"], nuova_riga, 0)
            self.__dettagli_grid_layout.addWidget(riga["nominativo"], nuova_riga, 1)
            self.__dettagli_grid_layout.addWidget(riga["bottone"], nuova_riga, 2)
            # Potrebbe essere necessario aggiornare riga_indice in riga (anche se non strettamente necessario per la logica)
            riga["riga_indice"] = nuova_riga


    def __get_dettagli_form(self) -> List[DettaglioRuolo]:
        """
        Raccoglie i dati da tutte le righe dinamiche dei dettagli.

        Ignora le righe dove sia ruolo che nominativo sono vuoti.

        :returns: lista di dizionari con chiave 'ruolo' e 'nominativo'.
        :raises: nessuna eccezione prevista.
        """
        dettagli_raccolti: List[DettaglioRuolo] = []
        for riga in self.__campi_dettagli:
            ruolo: str = riga["ruolo"].text().strip()
            nominativo: str = riga["nominativo"].text().strip()

            # Include solo se almeno un campo è valorizzato (per la validazione successiva)
            if ruolo or nominativo:
                dettagli_raccolti.append({
                    "ruolo": ruolo,
                    "nominativo": nominativo
                })
        return dettagli_raccolti


    def __mostra_errore(self, titolo: str, testo: str) -> None:
        """
        Mostra un messaggio di errore all'utente.

        :param titolo: titolo della finestra di errore.
        :param testo: testo descrittivo.
        :raises: nessuna eccezione; mostra una QMessageBox.
        """
        QMessageBox.critical(self, titolo, testo)

    # ------------------------- VALIDAZIONE E CALLBACKS -------------------------

    def __valida_dati(self) -> bool:
        """
        Esegue controlli base sui campi obbligatori.

        Campi obbligatori: nome_regia, regista, stagione.

        :returns: True se la validazione passa, False altrimenti.
        :raises: nessuna eccezione prevista.
        """
        if not self.__nome_regia_input.text().strip():
            self.__mostra_errore("Valore mancante", "Il campo 'Nome Regia' è obbligatorio.")
            return False
        if not self.__regista_input.text().strip():
            self.__mostra_errore("Valore mancante", "Il campo 'Regista' è obbligatorio.")
            return False
        if not self.__stagione_input.text().strip():
            self.__mostra_errore("Valore mancante", "Il campo 'Stagione/Anno di Validità' è obbligatorio.")
            return False

        # Validazione Dettagli Flessibili:
        # Assicura che, se una riga è parzialmente compilata, l'utente sia avvisato
        dettagli = self.__get_dettagli_form()
        for i, dettaglio in enumerate(dettagli):
            if (dettaglio["ruolo"] and not dettaglio["nominativo"]):
                 self.__mostra_errore("Dettaglio incompleto", f"Nella riga {i+1} dei Dettagli Flessibili, hai inserito un Ruolo ma non il Nominativo.")
                 return False
            if (dettaglio["nominativo"] and not dettaglio["ruolo"]):
                 self.__mostra_errore("Dettaglio incompleto", f"Nella riga {i+1} dei Dettagli Flessibili, hai inserito un Nominativo ma non il Ruolo.")
                 return False
        return True

    def __on_salva_clicked(self) -> None:
        """
        Callback privato chiamato quando l'utente clicca 'Salva Nuova Regia'.

        Valida i dati ed emette il segnale 'regia_creata' se validi.
        """
        if not self.__valida_dati():
            return

        dati: Dict[str, Any] = self.get_dati_form()
        # Emissione del segnale con i dati raccolti
        self.regia_creata.emit(dati)

    def __on_annulla_clicked(self) -> None:
        """
        Callback privato chiamato quando l'utente clicca 'Annulla'.

        Pulisce la form ed emette il segnale 'annullata'.
        """
        self.reset_form()
        self.annullata.emit()


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    finestra = CreaRegiaView()

    # Esempio di utilizzo:
    finestra.set_titolo_opera("La Traviata")

    def on_regia_creata(dati: Any) -> None:
        print("\n--- REGIA CREATA ---")
        print(f"Dati Base: {dati['nome_regia']}, {dati['regista']}, {dati['stagione']}")
        print(f"Dettagli Flessibili ({len(dati['dettagli'])}):")
        for dett in dati['dettagli']:
            print(f"  - Ruolo: {dett['ruolo']}, Nominativo: {dett['nominativo']}")
        QMessageBox.information(finestra, "Dati Ricevuti", "Regia salvata con successo!")

    def on_annullata() -> None:
        QMessageBox.information(finestra, "Annullato", "Operazione annullata")

    finestra.regia_creata.connect(on_regia_creata)
    finestra.annullata.connect(on_annullata)

    finestra.show()
    sys.exit(app.exec())