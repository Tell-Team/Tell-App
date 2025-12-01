from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QLabel,
    QCheckBox,
)
from functools import partial

from controller.info_controller import InfoController

from model.pianificazione.regia import Regia

from view.info.nuova_opera import FormNuovaOpera


class FormModificaOpera(FormNuovaOpera):
    """
    Sottoclasse di `FormularioNuovaOpera` che modifica la struttura della pagina e permette
    di assegnare una `Regia` all'opera da modifica. Modifica pure il funzionamento dei
    pulsante Cancella e Conferma, chiamando le funzioni `cancella_opera(is_new=False)` e
    `salva_opera(is_new=False)`, rispettivamente.
    """

    def __init__(self, info_controller: InfoController):
        super().__init__(info_controller)

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
        self.btn_cancella.clicked.disconnect()  # type:ignore
        self.btn_cancella.clicked.connect(  # type:ignore
            partial(self.info_controller.cancella_opera, is_new=False)
        )

        # ## Modifica il pulsanti Conferma
        self.btn_conferma.clicked.disconnect()  # type:ignore
        self.btn_conferma.clicked.connect(  # type:ignore
            lambda: print(
                "self.info_controller.salva_opera(is_new=False)"
            )  # - self.info_controller.salva_opera(is_new=False)
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
            partial(self.info_controller.nuova_regia, self.cur_id_opera)
            # - Ogni regia ha un id_opera
        )

        # ## Tabella delle regie
        self.tabella_regie = QTableWidget()
        self.tabella_regie.setColumnCount(4)
        self.tabella_regie.setHorizontalHeaderLabels(  # type:ignore
            [" ", "Regista", "Anno di produzione", " "]
        )

        tabella_header = self.tabella_regie.horizontalHeader()
        tabella_header.setSectionResizeMode(  # type:ignore
            QHeaderView.ResizeMode.Stretch
        )

        self.temp_cur_regie: list[Regia] = self.info_controller.get_regie_by_opera(
            self.cur_id_opera
        ).copy()

        # ### Lista regie non salvate
        self.temp_regie_nuove: list[Regia] = []

        # ### Lista regie eliminate
        self.temp_regie_eliminate: list[Regia] = []

        # ### Lista regie modificate
        self.temp_regie_modificate: list[tuple[int, str, int]] = []

        self.carica_tabella_regie()

        self.input_regia = QLabel("Nessuna")
        self.form_layout.addRow("Regia scelta:", self.input_regia)

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
        self.tabella_regie.clearContents()

        self.tabella_regie.setRowCount(
            len(self.temp_cur_regie)
            + len(self.temp_regie_nuove)
            # si pienso utilizar una lista de regie temporal, entoces debo cambiar
            # self.info_controller.get_regie_by_opera(self.cur_id_opera) por algo como
            # self.temp_lista_regie, y esta debe ser una copia de la anterior, pero no
            # una referencia que la modifique
        )

        for riga, regia in enumerate(self.temp_cur_regie + self.temp_regie_nuove):
            checkbox = QCheckBox()
            checkbox.stateChanged.connect(  # type:ignore
                lambda r=riga: self.checkbox_modificato(r)
            )
            self.tabella_regie.setCellWidget(riga, 0, checkbox)
            self.tabella_regie.setItem(riga, 1, QTableWidgetItem(regia.get_regista()))
            self.tabella_regie.setItem(
                riga, 2, QTableWidgetItem(regia.get_anno_produzione())
            )

            # Crear botón por fila
            btn_modifica_regia = QPushButton("Modifica")
            btn_modifica_regia.setObjectName("SmallButton")
            btn_modifica_regia.clicked.connect(  # type:ignore
                partial(
                    self.info_controller.modifica_regia,
                    regia.get_id(),
                    self.cur_id_opera,
                )
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

    def checkbox_modificato(self, r: int):
        checkbox = self.tabella_regie.cellWidget(r, 0)
        assert isinstance(checkbox, QCheckBox)
        regista, anno = (
            self.tabella_regie.item(r, 1).text(),  # type:ignore
            self.tabella_regie.item(r, 2).text(),  # type:ignore
        )

        if checkbox.isChecked():
            self.input_regia.setText(f"{regista} ({anno})")
