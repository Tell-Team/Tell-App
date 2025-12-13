from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal, QObject
from typing import Optional
from functools import partial

from model.model import Model
from model.pianificazione.genere import Genere
from model.exceptions import (
    DatoIncongruenteException,
    IdInesistenteException,
    IdOccupatoException,
)

from view.info.modifica_genere import ModificaGenereView, NuovoGenereView


class CUGenereController(QObject):
    navigation_go_back = pyqtSignal()
    navigation_get_page = pyqtSignal(str, dict)

    def __init__(
        self,
        model: Model,
        n_genere_v: NuovoGenereView,
        m_genere_v: ModificaGenereView,
    ):
        super().__init__()
        self.__model = model
        self.__nuovo_genere_view = n_genere_v
        self.__modifica_genere_view = m_genere_v
        self._connect_signals()

    def _connect_signals(self):
        # GENERI
        # Cancella creazione Genere
        self.__nuovo_genere_view.btn_cancella.clicked.connect(  # type:ignore
            self.cancella_genere
        )
        # Conferma creazione Genere
        self.__nuovo_genere_view.btn_conferma.clicked.connect(  # type:ignore
            partial(self.salva_genere, is_new=True)
        )

        # Cancella modifica Genere
        self.__modifica_genere_view.btn_cancella.clicked.connect(  # type:ignore
            self.cancella_genere
        )
        # Conferma modifica Genere
        self.__modifica_genere_view.btn_conferma.clicked.connect(  # type:ignore
            partial(self.salva_genere, is_new=False)
        )

    def get_genere(self, id_: int) -> Optional[Genere]:
        return self.__model.get_genere(id_)

    def aggiungi_genere(self, genere: Genere):
        self.__model.aggiungi_genere(genere)

    def modifica_genere(self, genere_modificato: Genere):
        self.__model.modifica_genere(genere_modificato)

    #
    #
    #

    def cancella_genere(self):
        self.navigation_go_back.emit()

    def salva_genere(self, is_new: bool):
        CAMPI_NECESSARI = "È necessario compilare tutti i campi."

        if is_new:
            from view.info.nuovo_genere import NuovoGenereView

            cur_page_dict: dict[str, QWidget | None] = {"value": None}
            self.navigation_get_page.emit("nuovo_genere", cur_page_dict)
            cur_page = cur_page_dict.get("value")

            if not isinstance(cur_page, NuovoGenereView):
                raise TypeError(
                    f"cur_page deve essere NuovoGenereView. Type trovato: {type(cur_page)}"
                )

            nome = cur_page.nome.text()
            descrizione = cur_page.descrizione.toPlainText()

            try:
                nuovo_genere = Genere(nome, descrizione)
            except DatoIncongruenteException:
                cur_page.input_error.setText(CAMPI_NECESSARI)
                self.set_pagina_focus(cur_page)  # - TEST
            else:
                cur_page.input_error.setText("")

                try:
                    self.aggiungi_genere(nuovo_genere)
                except IdOccupatoException:
                    # ESISTE GIA' UN GENERE CON QUELL'ID
                    # - Nel caso, mostrare popup di errore all'utente
                    pass
                else:
                    self.navigation_go_back.emit()
        elif not is_new:
            from view.info.modifica_genere import ModificaGenereView

            cur_page_dict: dict[str, QWidget | None] = {"value": None}
            self.navigation_get_page.emit("modifica_genere", cur_page_dict)
            cur_page = cur_page_dict.get("value")

            if not isinstance(cur_page, ModificaGenereView):
                raise TypeError(
                    f"cur_page deve essere ModificaGenereView. Type trovato: {type(cur_page)}"
                )

            copia_genere = self.get_genere(cur_page.cur_id_genere)
            if not isinstance(copia_genere, Genere):
                raise IdInesistenteException(
                    f"Non e' presente nessun genere con id {cur_page.cur_id_genere}."
                )

            nome = cur_page.nome.text()
            descrizione = cur_page.descrizione.toPlainText()

            try:
                copia_genere.set_nome(nome)
                copia_genere.set_descrizione(descrizione)
            except DatoIncongruenteException:
                cur_page.input_error.setText(CAMPI_NECESSARI)
                self.set_pagina_focus(cur_page)  # - TEST
            else:
                cur_page.input_error.setText("")

                try:
                    self.modifica_genere(copia_genere)
                except IdInesistenteException:
                    # NON ESISTE UN GENERE CON QUELL'ID
                    # - Nel caso, mostrare popup di errore all'utente
                    pass
                else:
                    self.navigation_go_back.emit()

    def set_pagina_focus(self, pagina: NuovoGenereView):  # - TEST
        pagina.focusNextChild()
        if not pagina.nome.text().strip():
            return
        pagina.focusNextChild()
