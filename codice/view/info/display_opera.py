from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)

from model.pianificazione.opera import Opera


class OperaDisplay(QWidget):
    """View delle singole opere della Lista Opere."""

    def __init__(self, o: Opera) -> None:
        super().__init__()

        self._setup_ui(o)

    def _setup_ui(self, o: Opera) -> None:
        # Labels
        nome = QLabel(f"{o.get_nome()}")
        nome.setObjectName("Header2")

        librettista = QLabel(f"Libretto di {o.get_librettista()}")
        librettista.setObjectName("Paragraph")

        compositore = QLabel(f"Musica di {o.get_compositore()}")
        compositore.setObjectName("Paragraph")

        # Pulsanti
        self.btn_visualizza = QPushButton("Maggior info")
        self.btn_visualizza.setObjectName("SmallButton")

        self.btn_modifica = QPushButton("Modifica")
        self.btn_modifica.setObjectName("SmallButton")

        self.btn_elimina = QPushButton("Elimina")
        self.btn_elimina.setObjectName("SmallButton")

        self.pulsanti = QWidget()
        layout_btn = QHBoxLayout(self.pulsanti)
        layout_btn.addWidget(self.btn_visualizza)
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
        layout.addWidget(librettista)
        layout.addWidget(compositore)
        layout.addWidget(self.pulsanti)
        layout.addWidget(self.conferma_elimina)
