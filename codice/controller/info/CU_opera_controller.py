from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal, QObject
from typing import Optional
from functools import partial

from model.model import Model
from model.pianificazione.opera import Opera
from model.exceptions import (
    DatoIncongruenteException,
    IdInesistenteException,
    IdOccupatoException,
)

from view.info.modifica_opera import ModificaOperaView, NuovaOperaView


class CUOperaController(QObject):
    navigation_go_back = pyqtSignal()
    navigation_get_page = pyqtSignal(str, dict)

    def __init__(
        self,
        model: Model,
        n_opera_v: NuovaOperaView,
        m_opera_v: ModificaOperaView,
    ):
        super().__init__()
        self.__model = model
        self.__nuova_opera_view = n_opera_v
        self.__modifica_opera_view = m_opera_v
        self._connect_signals()

    def _connect_signals(self):
        # OPERE
        # Crea una Opera
        self.__nuova_opera_view.request_lista_generi_nomi.connect(  # type:ignore
            self.carica_genere_opzioni
        )

        # Cancella creazione Opera
        self.__nuova_opera_view.btn_cancella.clicked.connect(  # type:ignore
            self.cancella_opera
        )
        # Conferma creazione Opera
        self.__nuova_opera_view.btn_conferma.clicked.connect(  # type:ignore
            partial(self.salva_opera, is_new=True)
        )

        # Cancella modifica Opera
        self.__modifica_opera_view.btn_cancella.clicked.connect(  # type:ignore
            self.cancella_opera
        )
        # Conferma modifica Opera
        self.__modifica_opera_view.btn_conferma.clicked.connect(  # type:ignore
            partial(self.salva_opera, is_new=False)
        )

    def get_opera(self, id_: int) -> Optional[Opera]:
        return self.__model.get_opera(id_)

    def aggiungi_opera(self, opera: Opera):
        self.__model.aggiungi_opera(opera)

    def modifica_opera(self, opera_modificata: Opera):
        self.__model.modifica_opera(opera_modificata)

    def get_generi(self):
        # - Da modificare (Il controller non dovrebbe accedere alla lista)
        return self.__model.get_generi()

    #
    #
    #

    def carica_genere_opzioni(self):
        generi = self.get_generi()
        nomi = [g.get_nome() for g in generi]
        self.__nuova_opera_view.set_genere_combobox(nomi)

    def cancella_opera(self):
        self.navigation_go_back.emit()

    def salva_opera(self, is_new: bool = True):
        # - Serve modificare i construttore di Opera per fare la trama, la data di prima
        #   rappresentazione e il teatro di prima rappresentazione parametri opzionali.
        #   Oppure possono essere segnati como necessari in NuovaOperaView con *.
        CAMPI_NECESSARI = "È necessario compilare tutti i campi."

        if is_new:
            from view.info.nuova_opera import NuovaOperaView

            cur_page_dict: dict[str, QWidget | None] = {"value": None}
            self.navigation_get_page.emit("nuova_opera", cur_page_dict)
            cur_page = cur_page_dict.get("value")

            if not isinstance(cur_page, NuovaOperaView):
                raise TypeError(
                    f"cur_page deve essere NuovaOperaView. Type trovato: {type(cur_page)}"
                )

            nome = cur_page.nome.text()
            trama = cur_page.trama.toPlainText()

            # -- WHAT DOES THIS MEAN???
            nome_genere = cur_page.genere.currentText()
            id_genere = -1
            for g in self.get_generi():
                if g.get_nome() == nome_genere:
                    id_genere = g.get_id()
            # -- END

            compositore = cur_page.compositore.text()
            librettista = cur_page.librettista.text()
            atti = cur_page.atti.value()
            data = cur_page.data.date().toPyDate()
            teatro = cur_page.teatro.text()

            try:
                nuova_opera = Opera(
                    nome, compositore, librettista, atti, data, teatro, trama, id_genere
                )
            except DatoIncongruenteException:
                cur_page.input_error.setText(CAMPI_NECESSARI)
                self.set_pagina_focus(cur_page)  # - TEST
            else:
                cur_page.input_error.setText("")

                try:
                    self.aggiungi_opera(nuova_opera)
                except IdInesistenteException:
                    # L'OPERA E' COLLEGATA AD UN GENERE CHE NON ESISTE
                    # - Nel caso, mostrare popup di errore all'utente
                    pass
                except IdOccupatoException:
                    # ESISTE GIA' UN'OPERA CON QUELL'ID
                    # - Nel caso, mostrare popup di errore all'utente
                    pass
                else:
                    self.navigation_go_back.emit()
        elif not is_new:
            from view.info.modifica_opera import ModificaOperaView

            cur_page_dict: dict[str, QWidget | None] = {"value": None}
            self.navigation_get_page.emit("modifica_opera", cur_page_dict)
            cur_page = cur_page_dict.get("value")

            if not isinstance(cur_page, ModificaOperaView):
                raise TypeError(
                    f"cur_page deve essere ModificaOperaView. Type trovato: {type(cur_page)}"
                )

            copia_opera = self.get_opera(cur_page.cur_id_opera)
            if not isinstance(copia_opera, Opera):
                raise IdInesistenteException(
                    f"Non e' presente nessun opera con id {cur_page.cur_id_opera}."
                )

            nome = cur_page.nome.text()
            trama = cur_page.trama.toPlainText()

            nome_genere = cur_page.genere.currentText()
            id_genere = -1
            for g in self.get_generi():
                if g.get_nome() == nome_genere:
                    id_genere = g.get_id()

            compositore = cur_page.compositore.text()
            librettista = cur_page.librettista.text()
            atti = cur_page.atti.value()
            data = cur_page.data.date().toPyDate()
            teatro = cur_page.teatro.text()

            try:
                copia_opera.set_nome(nome)
                copia_opera.set_compositore(compositore)
                copia_opera.set_librettista(librettista)
                copia_opera.set_numero_atti(atti)
                copia_opera.set_data_prima_rappresentazione(data)
                copia_opera.set_teatro_prima_rappresentazione(teatro)
                copia_opera.set_trama(trama)
                copia_opera.set_id_genere(id_genere)
            except DatoIncongruenteException:
                cur_page.input_error.setText(CAMPI_NECESSARI)
                self.set_pagina_focus(cur_page)  # - TEST
            else:
                cur_page.input_error.setText("")

                try:
                    self.modifica_opera(copia_opera)
                except IdInesistenteException:
                    # NON ESISTE UN'OPERA CON QUELL'ID
                    # - Nel caso, mostrare popup di errore all'utente
                    pass
                else:
                    self.navigation_go_back.emit()

    def set_pagina_focus(self, pagina: NuovaOperaView):  # - TEST
        pagina.focusNextChild()
        if not pagina.nome.text().strip():
            return
        pagina.focusNextChild()
        if not pagina.trama.toPlainText().strip():
            return
        pagina.focusNextChild()
        if pagina.genere.currentIndex() == 0:
            return
        pagina.focusNextChild()
        if not pagina.compositore.text().strip():
            return
        pagina.focusNextChild()
        if not pagina.librettista.text().strip():
            return
        pagina.focusNextChild()
        if not pagina.atti.value():
            return
        pagina.focusNextChild()
        if not pagina.data:
            return
        pagina.focusNextChild()
