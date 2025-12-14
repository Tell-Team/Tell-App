from typing import Dict, List, Optional, Any
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, 
    QPushButton, QHBoxLayout, QScrollArea, QFrame, QMessageBox
)

class ModificaRegiaView(QWidget):
    """
    View per la modifica di una scheda di Regia esistente.
    Gestisce righe dinamiche per i dettagli tecnici.

    Segnali:
    - regia_modificata(dict): emesso al salvataggio.
    - annullato(): emesso all'annullamento.
    - regia_eliminata(): emesso alla conferma eliminazione.
    """

    regia_modificata = pyqtSignal(object)
    annullato = pyqtSignal()
    regia_eliminata = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Inizializza la view.
        
        :param parent: widget genitore.
        :raises: nessuna eccezione prevista.
        """
        super().__init__(parent)
        self.__righe_dettaglio: List[Dict[str, Any]] = []
        self.__setup_ui()

    def __setup_ui(self) -> None:
        """
        Costruisce l'interfaccia.
        """
        self.setWindowTitle("Modifica Scheda Regia")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)

        # Intestazione
        self.__titolo_label: QLabel = QLabel("Modifica Regia: [Titolo]")
        self.__titolo_label.setStyleSheet("font-size: 16pt; font-weight: bold;")

        # Container Righe
        self.__scroll_area: QScrollArea = QScrollArea()
        self.__scroll_area.setWidgetResizable(True)
        self.__container_dettagli: QWidget = QWidget()
        self.__layout_dettagli: QVBoxLayout = QVBoxLayout(self.__container_dettagli)
        self.__layout_dettagli.addStretch()
        self.__scroll_area.setWidget(self.__container_dettagli)

        # Bottoni Azione
        self.__btn_aggiungi_riga: QPushButton = QPushButton("+ Aggiungi Dettaglio")
        self.__btn_aggiungi_riga.clicked.connect(self.__aggiungi_riga_dettaglio)

        self.__btn_salva: QPushButton = QPushButton("Salva Modifiche")
        self.__btn_salva.setStyleSheet("background-color: #007bff; color: white;")
        
        self.__btn_elimina: QPushButton = QPushButton("Elimina Regia")
        self.__btn_elimina.setStyleSheet("background-color: #dc3545; color: white;")

        self.__btn_annulla: QPushButton = QPushButton("Annulla")

        # Layout Bottoni
        btn_layout: QHBoxLayout = QHBoxLayout()
        btn_layout.addWidget(self.__btn_elimina)
        btn_layout.addStretch()
        btn_layout.addWidget(self.__btn_annulla)
        btn_layout.addWidget(self.__btn_salva)

        # Layout Principale
        main_layout: QVBoxLayout = QVBoxLayout(self)
        main_layout.addWidget(self.__titolo_label)
        main_layout.addWidget(QLabel("Dettagli Tecnici (Luci, Audio, Scena):"))
        main_layout.addWidget(self.__scroll_area)
        main_layout.addWidget(self.__btn_aggiungi_riga)
        main_layout.addLayout(btn_layout)

        # Connessioni
        self.__btn_salva.clicked.connect(self.__on_salva_clicked)
        self.__btn_annulla.clicked.connect(self.__on_annulla_clicked)
        self.__btn_elimina.clicked.connect(self.__on_elimina_clicked)

    # ------------------------- METODI PRIVATI -------------------------

    def __aggiungi_riga_dettaglio(self, dati: Optional[Dict[str, str]] = None) -> None:
        """
        Aggiunge una riga visiva per un dettaglio tecnico.
        
        :param dati: Dati opzionali per popolare la riga.
        :raises: nessuna eccezione prevista.
        """
        frame = QFrame()
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(0, 5, 0, 5)

        input_tipo = QLineEdit()
        input_tipo.setPlaceholderText("Tipo (es. Luci)")
        input_desc = QTextEdit()
        input_desc.setPlaceholderText("Descrizione tecnica...")
        input_desc.setFixedHeight(40)
        btn_remove = QPushButton("X")
        btn_remove.setFixedWidth(30)
        btn_remove.setStyleSheet("background-color: #dc3545; color: white;")

        if dati:
            input_tipo.setText(dati.get("tipo", ""))
            input_desc.setText(dati.get("descrizione", ""))

        layout.addWidget(input_tipo, 1)
        layout.addWidget(input_desc, 3)
        layout.addWidget(btn_remove)

        riga_obj = {
            "widget": frame,
            "input_tipo": input_tipo,
            "input_desc": input_desc
        }
        self.__righe_dettaglio.append(riga_obj)
        
        # Inserisci prima dello stretch
        self.__layout_dettagli.insertWidget(self.__layout_dettagli.count() - 1, frame)
        
        btn_remove.clicked.connect(lambda: self.__rimuovi_riga(riga_obj))

    def __rimuovi_riga(self, riga_obj: Dict[str, Any]) -> None:
        """
        Rimuove una riga dalla UI e dalla lista interna.
        
        :raises: nessuna eccezione prevista.
        """
        if riga_obj in self.__righe_dettaglio:
            riga_obj["widget"].deleteLater()
            self.__righe_dettaglio.remove(riga_obj)

    # ------------------------- METODI PUBBLICI -------------------------

    def set_dati_form(self, dati: Dict[str, Any]) -> None:
        """
        Popola la view con i dati della regia.
        
        :param dati: Dict con 'titolo_spettacolo' e lista 'dettagli'.
        :raises: nessuna eccezione prevista.
        """
        titolo = dati.get("titolo_spettacolo", "Sconosciuto")
        self.__titolo_label.setText(f"Modifica Regia: {titolo}")

        # Pulisci righe esistenti
        for riga in self.__righe_dettaglio:
            riga["widget"].deleteLater()
        self.__righe_dettaglio.clear()

        lista_dettagli = dati.get("dettagli", [])
        for dett in lista_dettagli:
            self.__aggiungi_riga_dettaglio(dett)

    def get_dati_form(self) -> Dict[str, Any]:
        """
        Recupera i dati modificati.
        
        :return: Dict con la lista 'dettagli'.
        :raises: nessuna eccezione prevista.
        """
        dettagli_output = []
        for riga in self.__righe_dettaglio:
            t = riga["input_tipo"].text().strip()
            d = riga["input_desc"].toPlainText().strip()
            if t or d:
                dettagli_output.append({"tipo": t, "descrizione": d})
        return {"dettagli": dettagli_output}

    # ------------------------- CALLBACKS -------------------------

    def __on_salva_clicked(self) -> None:
        """
        Gestisce il salvataggio.
        
        :raises: nessuna eccezione prevista.
        """
        # Qui potresti aggiungere __valida_dati se necessario
        self.regia_modificata.emit(self.get_dati_form())

    def __on_elimina_clicked(self) -> None:
        """
        Gestisce l'eliminazione.
        
        :raises: nessuna eccezione prevista.
        """
        risp = QMessageBox.question(self, "Elimina", "Eliminare questa scheda tecnica?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if risp == QMessageBox.StandardButton.Yes:
            self.regia_eliminata.emit()

    def __on_annulla_clicked(self) -> None:
        """
        Gestisce l'annullamento.
        
        :raises: nessuna eccezione prevista.
        """
        self.annullato.emit()