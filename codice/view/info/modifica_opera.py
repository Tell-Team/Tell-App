from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton

from model.model import Model
from controller.navigation import NavigationController

from view.info.nuova_opera import FormularioNuovaOpera


class FormularioModificaOpera(FormularioNuovaOpera):
    """
    Sottoclasse di `FormularioNuovaOpera` che modifica la struttura della pagina e permette
    di assegnare una `Regia` all'opera da modifica. Modifica pure il funzionamento dei
    pulsante Cancella e Conferma, chiamando le funzioni `cancella_opera(is_new=False)` e
    `salva_opera(is_new=False)`, rispettivamente.
    """

    def __init__(self, model: Model, nav: NavigationController):
        super().__init__(model, nav)
        # I campi di input sono atributi di FormularioNuovaOpera

        # # Inziare pagina come ModificaOpera
        # ## Elimina lo Stretch alla fine del layout
        last_index = self.main_layout.count() - 1
        self.main_layout.takeAt(last_index)

        # ## Modifica il header del layout
        self.header.setText("Modifica opera")

        # ## Modifica il pulsanti Cancella
        self.btn_cancella.clicked.connect(  # type:ignore
            info_controller.cancella_opera(is_new=False)
        )

        # ## Modifica il pulsanti Conferma
        self.btn_conferma.clicked.connect(  # type:ignore
            info_controller.salva_opera(is_new=False)
        )

        # ## Rimuovi le regie dell layout (temporaneamente)
        self.main_layout.removeWidget(self.label_lista_regie)
        self.main_layout.removeWidget(self.nota_regie)
        del self.nota_regie
        self.main_layout.removeWidget(self.pulsanti)

        # ## Pulsante: Nuova regia
        btn_nuova_regia = QPushButton("Nuova regia")
        btn_nuova_regia.setObjectName("SmallButton")
        btn_nuova_regia.clicked.connect(  # type:ignore
            nav.go_back  # - Crea una regia salvata in una lista di regie unica per ogni opera
        )

        # - IMPORTANTE: Non c'è un display per le singole regie dell'opera

        # ## LAYOUT LISTA REGIE
        header_lista_regia = QWidget()
        layout_header_lista_regia = QHBoxLayout(header_lista_regia)
        layout_header_lista_regia.addWidget(self.label_lista_regie)
        layout_header_lista_regia.addWidget(btn_nuova_regia)
        layout_header_lista_regia.addStretch()

        # ## Aggiungi LAYOUT LISTA REGIE al layout principale
        self.main_layout.addWidget(header_lista_regia)
        self.main_layout.addWidget(self.pulsanti)
        self.main_layout.addStretch()
