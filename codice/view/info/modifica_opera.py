from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)
from functools import partial  # - Necessario nel codice reale

from controller.info_controller import InfoController

from view.info.nuova_opera import FormNuovaOpera


# - I pulsanti di Cancella e Conferma devo riscrivere il dati della pagina per prossime chiamate.
#   Questo include self.cur_id_opera
class FormModificaOpera(FormNuovaOpera):
    """
    Sottoclasse di `FormularioNuovaOpera` che modifica la struttura della pagina e permette
    di assegnare una `Regia` all'opera da modifica. Modifica pure il funzionamento dei
    pulsante Cancella e Conferma, chiamando le funzioni `cancella_opera(is_new=False)` e
    `salva_opera(is_new=False)`, rispettivamente.
    """

    def __init__(self, info_controller: InfoController):
        super().__init__(info_controller)

        self._build_ui()

        # I campi di input sono atributi di FormNuovaOpera

    def _build_ui(self):
        super()._build_ui()

        # # Inziare pagina come ModificaOpera

        # Il valore di cur_id_opera è assegnato quando si chiama .modifica_opera(id_opera)
        self.cur_id_opera: int = -1

        # ## Elimina lo Stretch alla fine del layout
        last_index = self.main_layout.count() - 1
        self.main_layout.takeAt(last_index)

        # ## Modifica il header del layout
        self.header.setText("Modifica opera")

        # ## Modifica il pulsanti Cancella
        self.btn_cancella.clicked.connect(  # type:ignore
            lambda: print(
                "info_controller.cancella_opera(is_new=False)"
            )  # - info_controller.cancella_opera(is_new=False)
        )

        # ## Modifica il pulsanti Conferma
        self.btn_conferma.clicked.connect(  # type:ignore
            lambda: print(
                "info_controller.salva_opera(is_new=False)"
            )  # - info_controller.salva_opera(is_new=False)
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
            lambda: print(
                "info_controller.nuova_regia"
            )  # - info_controller.nuova_regia
            # - In teoria, ogni opera ha una sua lista regie.
        )

        # ## Tabella delle regie
        self.tabella_regie = QTableWidget()
        self.tabella_regie.setColumnCount(4)
        self.tabella_regie.setHorizontalHeaderLabels(  # type:ignore
            ["Indice", "Regista", "Anno di produzione", " "]
        )

        tabella_header = self.tabella_regie.horizontalHeader()
        tabella_header.setSectionResizeMode(  # type:ignore
            QHeaderView.ResizeMode.Stretch
        )

        self.carica_tabella_regie()

        # ## LAYOUT LISTA REGIE
        header_lista_regia = QWidget()
        layout_header_lista_regia = QHBoxLayout(header_lista_regia)
        layout_header_lista_regia.addWidget(self.label_lista_regie)
        layout_header_lista_regia.addWidget(btn_nuova_regia)
        layout_header_lista_regia.addStretch()

        # ## Aggiungi LAYOUT LISTA REGIE al layout principale
        self.main_layout.addWidget(header_lista_regia)
        self.main_layout.addWidget(self.tabella_regie)
        self.main_layout.addWidget(self.pulsanti)
        self.main_layout.addStretch()

    def carica_tabella_regie(self):
        self.tabella_regie.setRowCount(
            len(self.info_controller.get_regie_by_opera(self.cur_id_opera))
        )
        i = 0

        for riga, regia in enumerate(
            self.info_controller.get_regie_by_opera(self.cur_id_opera)
        ):
            self.tabella_regie.setItem(riga, 0, QTableWidgetItem(str(i + 1)))
            self.tabella_regie.setItem(riga, 1, QTableWidgetItem(regia.get_regista()))
            self.tabella_regie.setItem(
                riga, 2, QTableWidgetItem(regia.get_anno_produzione())
            )

            # Crear botón por fila
            btn_modifica_regia = QPushButton("Modifica")
            btn_modifica_regia.setObjectName("SmallButton")
            btn_modifica_regia.clicked.connect(  # type:ignore
                lambda: print(
                    "partial(self.info_controller.modifica_regia, regia.get_id())"
                )  # partial(self.info_controller.modifica_regia, regia.get_id())
            )

            btn_elimina_regia = QPushButton("Elimina")
            btn_elimina_regia.setObjectName("SmallButton")
            btn_elimina_regia.clicked.connect(  # type:ignore
                lambda: print(
                    "partial(self.info_controller.elimina_regia, regia.get_id())"
                )  # partial(self.info_controller.elimina_regia, regia.get_id())
            )

            pulsanti_regia = QWidget()
            temp_layout_btn = QHBoxLayout(pulsanti_regia)
            temp_layout_btn.addWidget(btn_modifica_regia)
            temp_layout_btn.addWidget(btn_elimina_regia)
            temp_layout_btn.addStretch()

            # Insertar botón en la celda
            self.tabella_regie.setCellWidget(riga, 3, pulsanti_regia)
