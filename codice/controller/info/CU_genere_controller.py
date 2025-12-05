from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal, QObject
from functools import partial

from model.model import Model
from model.pianificazione.genere import Genere
from model.exceptions import DatoIncongruenteException, IdInesistenteException

from view.info.modifica_genere import ModificaGenereView, NuovoGenereView

import copy


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

    #
    #
    #

    def cancella_genere(self):
        """
        Chiama il metodo `go_back()` del `NavigationController`. Non ha bisogno di riscrivere
        i campi di input perché le funzioni `crea_genere()` e `modifica_genere()` si caricano di
        farlo.
        """
        self.navigation_go_back.emit()

    def salva_genere(self, is_new: bool):
        CAMPI_NECESSARI = "È necessario compilare i campi segnati con *."

        if is_new:
            from view.info.nuovo_genere import NuovoGenereView

            cur_page_dict: dict[str, QWidget | None] = {"value": None}
            self.navigation_get_page.emit("nuovo_genere", cur_page_dict)
            cur_page = cur_page_dict.get("value")

            if not isinstance(cur_page, NuovoGenereView):
                raise TypeError(
                    f"cur_page deve essere NuovoGenereView, trovata {type(cur_page)}"
                )

            nome = cur_page.nome.text()
            descrizione = cur_page.descrizione.toPlainText()

            try:
                new_genere = Genere(nome, descrizione)
            except DatoIncongruenteException:
                cur_page.input_error.setText(CAMPI_NECESSARI)
            else:
                cur_page.input_error.setText("")

                self.__model.aggiungi_genere(new_genere)

                self.navigation_go_back.emit()
        elif not is_new:
            from view.info.modifica_genere import ModificaGenereView

            cur_page_dict: dict[str, QWidget | None] = {"value": None}
            self.navigation_get_page.emit("modifica_genere", cur_page_dict)
            cur_page = cur_page_dict.get("value")

            if not isinstance(cur_page, ModificaGenereView):
                raise TypeError(
                    f"cur_page deve essere ModificaGenereView, trovata {type(cur_page)}"
                )

            copia_genere = copy.deepcopy(
                self.__model.get_genere(cur_page.cur_id_genere)
            )
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
            else:
                cur_page.input_error.setText("")

                self.__model.modifica_genere(copia_genere)

                self.navigation_go_back.emit()
