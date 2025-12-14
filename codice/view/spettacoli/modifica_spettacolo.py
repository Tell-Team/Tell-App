from typing import Dict, List
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QComboBox, QPushButton,
    QVBoxLayout, QHBoxLayout, QGroupBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor


class ModificaSpettacoloView(QWidget):
    """
    View per la modifica di uno spettacolo esistente.
    Contiene campi per titolo, opera e regia associata, tipo evento e lista repliche.
    """

    spettacolo_modificato = pyqtSignal(object)  # dict dei dati modificati
    spettacolo_eliminato = pyqtSignal()
    evento_aggiunto = pyqtSignal()
    evento_modificato = pyqtSignal(int)  # indice riga
    evento_eliminato_signal = pyqtSignal(int)  # indice riga
    annullato = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.__eventi: List[Dict[str, str]] = []  # lista di eventi (repliche)
        self.__setup_ui()

    def __setup_ui(self) -> None:
        # Titolo principale
        self.__label_titolo: QLabel = QLabel("Modifica Spettacolo")
        self.__label_titolo.setStyleSheet("font-size: 20px; font-weight: bold;")

        # Dati Base
        box_dati: QGroupBox = QGroupBox("Dati Base e Contenuto")
        layout_dati = QVBoxLayout()

        self.__input_titolo = QLineEdit()
        self.__input_titolo.setPlaceholderText("Titolo spettacolo")

        self.__select_opera = QComboBox()
        self.__select_opera.addItem("Seleziona l'Opera")
        self.__select_opera.addItem("La Traviata")

        self.__select_regia = QComboBox()
        self.__select_regia.addItem("Seleziona la Regia")
        self.__select_regia.addItem("Produzione Corrente 2024")

        layout_dati.addWidget(QLabel("Titolo Spettacolo *"))
        layout_dati.addWidget(self.__input_titolo)

        layout_dual = QHBoxLayout()
        layout_dual.addWidget(self.__select_opera)
        layout_dual.addWidget(self.__select_regia)
        layout_dati.addLayout(layout_dual)
        box_dati.setLayout(layout_dati)

        # Politiche di prezzo
        box_prezzo: QGroupBox = QGroupBox("Politiche di Prezzo Generali")
        layout_prezzo = QVBoxLayout()
        layout_prezzo.addWidget(QLabel("Definisci il prezzo base del biglietto."))
        self.__select_tipo_evento = QComboBox()
        self.__select_tipo_evento.addItems(["Standard", "Prima/Gala", "Recita Ridotta"])
        layout_prezzo.addWidget(QLabel("Tipo Evento *"))
        layout_prezzo.addWidget(self.__select_tipo_evento)
        box_prezzo.setLayout(layout_prezzo)

        # Lista Eventi
        box_eventi: QGroupBox = QGroupBox("Lista Eventi (Repliche)")
        layout_eventi = QVBoxLayout()

        self.btn_aggiungi_evento = QPushButton("+ Aggiungi Nuovo Evento")
        self.btn_aggiungi_evento.setStyleSheet("background-color: #28a745; color: white;")
        self.btn_aggiungi_evento.clicked.connect(lambda: self.evento_aggiunto.emit())
        layout_eventi.addWidget(self.btn_aggiungi_evento, alignment=Qt.AlignmentFlag.AlignRight)

        self.__tabella_eventi = QTableWidget(0, 4)
        self.__tabella_eventi.setHorizontalHeaderLabels(["Data e Ora", "Sala", "Stato", "Azioni"])
        self.__tabella_eventi.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout_eventi.addWidget(self.__tabella_eventi)
        box_eventi.setLayout(layout_eventi)

        # Pulsanti Azione
        layout_bottoni = QHBoxLayout()
        layout_bottoni.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.btn_elimina_spettacolo = QPushButton("Elimina Spettacolo")
        self.btn_elimina_spettacolo.setStyleSheet("background-color: #dc3545; color: white;")
        self.btn_elimina_spettacolo.clicked.connect(lambda: self.spettacolo_eliminato.emit())

        self.btn_annulla = QPushButton("Annulla")
        self.btn_annulla.setStyleSheet("background-color: #6c757d; color: white;")
        self.btn_annulla.clicked.connect(lambda: self.annullato.emit())

        self.btn_salva = QPushButton("Salva Modifiche")
        self.btn_salva.setStyleSheet("background-color: #007bff; color: white;")
        self.btn_salva.clicked.connect(self.__on_salva_clicked)

        layout_bottoni.addWidget(self.btn_elimina_spettacolo)
        layout_bottoni.addWidget(self.btn_annulla)
        layout_bottoni.addWidget(self.btn_salva)

        # Layout principale
        layout_principale = QVBoxLayout()
        layout_principale.addWidget(self.__label_titolo)
        layout_principale.addSpacing(10)
        layout_principale.addWidget(box_dati)
        layout_principale.addWidget(box_prezzo)
        layout_principale.addWidget(box_eventi)
        layout_principale.addLayout(layout_bottoni)

        self.setLayout(layout_principale)
        self.setMinimumWidth(700)
        self.setWindowTitle("Modifica Spettacolo")

    # --------------------------
    # Form
    # --------------------------
    def get_dati_form(self) -> Dict[str, str]:
        return {
            "titolo": self.__input_titolo.text().strip(),
            "opera": self.__select_opera.currentText(),
            "regia": self.__select_regia.currentText(),
            "tipo_evento": self.__select_tipo_evento.currentText(),
        }

    def set_dati_form(self, dati: Dict[str, str]) -> None:
        self.__input_titolo.setText(dati.get("titolo", ""))
        index_opera = self.__select_opera.findText(dati.get("opera", "Seleziona l'Opera"))
        if index_opera >= 0:
            self.__select_opera.setCurrentIndex(index_opera)
        index_regia = self.__select_regia.findText(dati.get("regia", "Seleziona la Regia"))
        if index_regia >= 0:
            self.__select_regia.setCurrentIndex(index_regia)
        index_tipo = self.__select_tipo_evento.findText(dati.get("tipo_evento", "Standard"))
        if index_tipo >= 0:
            self.__select_tipo_evento.setCurrentIndex(index_tipo)
        self.__label_titolo.setText(f"Modifica Spettacolo: {dati.get('titolo','')}")

    # --------------------------
    # Tabella Eventi con callback sicure
    # --------------------------
    def popola_tabella_eventi(self, eventi: List[Dict[str, str]]) -> None:
        self.__tabella_eventi.setRowCount(0)
        self.__eventi = eventi
        for idx, evento in enumerate(eventi):
            self.__tabella_eventi.insertRow(idx)
            self.__tabella_eventi.setItem(idx, 0, QTableWidgetItem(evento.get("data", "")))
            self.__tabella_eventi.setItem(idx, 1, QTableWidgetItem(evento.get("sala", "")))
            stato_item = QTableWidgetItem(evento.get("stato", ""))
            if evento.get("stato", "").lower() == "pubblicato":
                stato_item.setForeground(QColor("green"))
            elif evento.get("stato", "").lower() == "bozza":
                stato_item.setForeground(QColor("orange"))
            self.__tabella_eventi.setItem(idx, 2, stato_item)

            # Colonna Azioni
            widget_azioni = QWidget()
            btn_modifica = QPushButton("Modifica")
            btn_elimina = QPushButton("Elimina")
            btn_modifica.clicked.connect(self.__make_evento_modificato_callback(idx))
            btn_elimina.clicked.connect(self.__make_evento_eliminato_callback(idx))
            layout_azioni = QHBoxLayout()
            layout_azioni.addWidget(btn_modifica)
            layout_azioni.addWidget(btn_elimina)
            layout_azioni.setContentsMargins(0, 0, 0, 0)
            widget_azioni.setLayout(layout_azioni)
            self.__tabella_eventi.setCellWidget(idx, 3, widget_azioni)

    # --------------------------
    # Closure callback per eventi
    # --------------------------
    def __make_evento_modificato_callback(self, idx: int):
        def callback() -> None:
            self.evento_modificato.emit(idx)
        return callback

    def __make_evento_eliminato_callback(self, idx: int):
        def callback() -> None:
            self.evento_eliminato_signal.emit(idx)
        return callback

    # --------------------------
    # Pulsante Salva
    # --------------------------
    def __on_salva_clicked(self) -> None:
        dati = self.get_dati_form()
        if not dati["titolo"] or dati["opera"] == "Seleziona l'Opera" or dati["regia"] == "Seleziona la Regia":
            QMessageBox.warning(self, "Errore", "Compila tutti i campi obbligatori!")
            return
        self.spettacolo_modificato.emit(dati)


if __name__ == "__main__":
    import sys
    from typing import Dict
    from PyQt6.QtWidgets import QApplication, QMessageBox

    app = QApplication(sys.argv)
    finestra = ModificaSpettacoloView()

    # Callback per modifica spettacolo
    def on_modificato(dati: Dict[str, str]) -> None:
        QMessageBox.information(finestra, "Spettacolo Modificato", str(dati))

    finestra.spettacolo_modificato.connect(on_modificato)

    # Callback per eliminazione spettacolo
    def on_eliminato() -> None:
        QMessageBox.warning(finestra, "Spettacolo Eliminato", "Lo spettacolo è stato eliminato!")

    finestra.spettacolo_eliminato.connect(on_eliminato)

    # Callback aggiungi nuovo evento
    def on_aggiungi_evento() -> None:
        QMessageBox.information(finestra, "Nuovo Evento", "Qui puoi aggiungere un nuovo evento.")

    finestra.evento_aggiunto.connect(on_aggiungi_evento)

    # Esempio dati spettacolo
    dati_esempio: Dict[str, str] = {
        "titolo": "La Traviata - Stagione 2025",
        "opera": "La Traviata",
        "regia": "Produzione Corrente 2024",
        "tipo_evento": "Prima/Gala"
    }
    finestra.set_dati_form(dati_esempio)

    # Esempio repliche
    repliche = [
        {"data": "20/11/2025 - 20:30", "sala": "Sala Grande", "stato": "Pubblicato"},
        {"data": "22/11/2025 - 17:00", "sala": "Sala Grande", "stato": "Bozza"}
    ]
    finestra.popola_tabella_eventi(repliche)

    finestra.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    import sys
    from typing import Dict
    from PyQt6.QtWidgets import QApplication, QMessageBox

    app = QApplication(sys.argv)
    finestra = ModificaSpettacoloView()

    # --------------------------
    # Callback per modifica spettacolo
    # --------------------------
    def on_modificato(dati: Dict[str, str]) -> None:
        """Mostra messaggio con i dati modificati dello spettacolo."""
        QMessageBox.information(finestra, "Spettacolo Modificato", str(dati))

    finestra.spettacolo_modificato.connect(on_modificato)

    # --------------------------
    # Callback per eliminazione spettacolo
    # --------------------------
    def on_eliminato() -> None:
        QMessageBox.warning(finestra, "Spettacolo Eliminato", "Lo spettacolo è stato eliminato!")

    finestra.spettacolo_eliminato.connect(on_eliminato)

    # --------------------------
    # Callback aggiungi nuovo evento
    # --------------------------
    def on_aggiungi_evento() -> None:
        QMessageBox.information(finestra, "Nuovo Evento", "Qui puoi aggiungere un nuovo evento.")

    finestra.evento_aggiunto.connect(on_aggiungi_evento)

    # --------------------------
    # Callback modifica ed elimina evento
    # --------------------------
    def make_callback_modifica(riga: int):
        def callback() -> None:
            QMessageBox.information(finestra, "Modifica Evento", f"Modifica evento riga {riga}")
        return callback

    def make_callback_elimina(riga: int):
        def callback() -> None:
            QMessageBox.warning(finestra, "Elimina Evento", f"Elimina evento riga {riga}")
        return callback

    # --------------------------
    # Esempio dati spettacolo
    # --------------------------
    dati_esempio: Dict[str, str] = {
        "titolo": "La Traviata - Stagione 2025",
        "opera": "La Traviata",
        "regia": "Produzione Corrente 2024",
        "tipo_evento": "Prima/Gala"
    }
    finestra.set_dati_form(dati_esempio)

    # --------------------------
    # Esempio repliche
    # --------------------------
    repliche = [
        {"data": "20/11/2025 - 20:30", "sala": "Sala Grande", "stato": "Pubblicato"},
        {"data": "22/11/2025 - 17:00", "sala": "Sala Grande", "stato": "Bozza"}
    ]
    finestra.popola_tabella_eventi(repliche)

    # Colleghiamo le funzioni helper per ogni riga della tabella
    for idx in range(len(repliche)):
        finestra.evento_modificato.connect(make_callback_modifica(idx))
        finestra.evento_eliminato_signal.connect(make_callback_elimina(idx))

    # Mostra la finestra
    finestra.show()
    sys.exit(app.exec())


