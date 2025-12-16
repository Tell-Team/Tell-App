from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)

from model.pianificazione.genere import Genere


class GenereDisplay(QWidget):
    """View dei singoli generi della Lista Generi."""

    def __init__(self, g: Genere) -> None:
        super().__init__()

        self._setup_ui(g)

    def _setup_ui(self, g: Genere) -> None:
        # Labels
        nome = QLabel(f"{g.get_nome()}")
        nome.setObjectName("Header2")

        descrizione = QLabel(f"{g.get_descrizione()}")
        descrizione.setObjectName("Paragraph")
        descrizione.setWordWrap(True)

        # Pulsanti Modifica-Elimina
        self.btn_modifica = QPushButton("Modifica")
        self.btn_modifica.setObjectName("SmallButton")

        self.btn_elimina = QPushButton("Elimina")
        self.btn_elimina.setObjectName("SmallButton")

        self.pulsanti = QWidget()
        layout_btn = QHBoxLayout(self.pulsanti)
        layout_btn.addWidget(self.btn_modifica)
        layout_btn.addWidget(self.btn_elimina)
        layout_btn.addStretch()

        # Pannello di eliminazione
        domanda = QLabel("Sicuro di eliminare?")
        domanda.setObjectName("Paragraph")

        self.btn_si = QPushButton("Sì")
        self.btn_si.setObjectName("SmallButton")

        self.btn_no = QPushButton("No")
        self.btn_no.setObjectName("SmallButton")

        self.conferma_elimina = QWidget()
        layout_conferma = QHBoxLayout(self.conferma_elimina)
        layout_conferma.addWidget(domanda)
        layout_conferma.addWidget(self.btn_si)
        layout_conferma.addWidget(self.btn_no)
        self.conferma_elimina.hide()

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(nome)
        layout.addWidget(descrizione)
        layout.addWidget(self.pulsanti)
        layout.addWidget(self.conferma_elimina)
