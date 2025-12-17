from PyQt6.QtWidgets import QWidget, QMessageBox
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
    """Gestisce il salvataggio dei generi creati e modificati.

    Segnali:
    - navigation_go_back(): emesso per tornare all'ultima pagina visualizzata
    - naviagation_get_page(str, dict): emesso per ottenere la pagina da cui si prenderà l'input
    """

    navigation_go_back = pyqtSignal()
    navigation_get_page = pyqtSignal(str, dict)

    def __init__(
        self,
        model: Model,
        n_genere_v: NuovoGenereView,
        m_genere_v: ModificaGenereView,
    ) -> None:
        super().__init__()
        self.__model = model
        self.__nuovo_genere_view = n_genere_v
        self.__modifica_genere_view = m_genere_v

        self._connect_signals()

    def _connect_signals(self) -> None:
        # Cancella creazione Genere
        self.__nuovo_genere_view.btn_cancella.clicked.connect(  # type:ignore
            self.navigation_go_back.emit
        )
        # Conferma creazione Genere
        self.__nuovo_genere_view.btn_conferma.clicked.connect(  # type:ignore
            partial(self.salva_genere, is_new=True)
        )

        # Cancella modifica Genere
        self.__modifica_genere_view.btn_cancella.clicked.connect(  # type:ignore
            self.navigation_go_back.emit
        )
        # Conferma modifica Genere
        self.__modifica_genere_view.btn_conferma.clicked.connect(  # type:ignore
            partial(self.salva_genere, is_new=False)
        )

    # ------------------------- METODI PUBBLICI -------------------------

    def get_genere(self, id_: int) -> Optional[Genere]:
        return self.__model.get_genere(id_)

    def aggiungi_genere(self, genere: Genere) -> None:
        self.__model.aggiungi_genere(genere)

    def modifica_genere(self, genere_modificato: Genere) -> None:
        self.__model.modifica_genere(genere_modificato)

    def salva_genere(self, is_new: bool) -> None:
        """Salva il genere creato o modificato nel `GestoreGeneri`.

        :param is_new: verifica se si deve creare un genere o modificare uno esistente
        """
        CAMPI_NECESSARI = (
            "<b>ATTENZIONE</b>: E' necessario compilare tutti i campi d'input."
        )

        if is_new:
            # Ottieni la pagina NuovoGenereView
            cur_page = self.__nuovo_genere_view

            # Ottieni l'input inserito
            nome = cur_page.nome.text()
            descrizione = cur_page.descrizione.toPlainText()

            # Tenta di creare la nuova opera
            try:
                nuovo_genere = Genere(nome, descrizione)
            except DatoIncongruenteException as exc:
                # E' stato trovato un campo con input non valido
                cur_page.input_error.setText(CAMPI_NECESSARI)
                self.__set_pagina_focus(cur_page)
                self.__mostra_errore(
                    cur_page, "Input non valido", f"Si è verificato un errore: {exc}"
                )
            else:
                cur_page.input_error.setText("")

                try:
                    self.aggiungi_genere(nuovo_genere)
                except IdOccupatoException as exc:
                    # Ediste già un genere con quell'id
                    self.__mostra_errore(
                        cur_page,
                        "ID Genere occupato",
                        f"Si è verificato un errore: {exc}",
                    )
                else:
                    self.navigation_go_back.emit()
        elif not is_new:
            # Ottieni la pagina ModificaGenereView
            cur_page = self.__modifica_genere_view

            # Crea una copia del genere originale
            copia_genere: Optional[Genere] = self.get_genere(cur_page.cur_id_genere)
            if not isinstance(copia_genere, Genere):
                # Non esiste genere con l'id salvata nella pagina
                self.__mostra_errore(
                    cur_page,
                    "Errore nel salvataggio",
                    f"Non è presente nessun genere con id {cur_page.cur_id_genere}. "
                    + "Impossibile effettuare le modifiche.",
                )
                return

            # Ottieni l'input inserito
            nome = cur_page.nome.text()
            descrizione = cur_page.descrizione.toPlainText()

            # Tenta di modificare il genere
            try:
                copia_genere.set_nome(nome)
                copia_genere.set_descrizione(descrizione)
            except DatoIncongruenteException as exc:
                cur_page.input_error.setText(CAMPI_NECESSARI)
                self.__set_pagina_focus(cur_page)
                self.__mostra_errore(
                    cur_page, "Input non valido", f"Si è verificato un errore: {exc}"
                )
            else:
                cur_page.input_error.setText("")

                try:
                    self.modifica_genere(copia_genere)
                except IdInesistenteException as exc:
                    # Non esiste un genere con quell'id
                    self.__mostra_errore(
                        cur_page,
                        "ID Generi insesistente",
                        f"Si è verificato un errore: {exc}",
                    )
                    pass
                else:
                    self.navigation_go_back.emit()

    # ------------------------- METODI PRIVATI -------------------------

    def __mostra_errore(self, widget: QWidget, titolo: str, testo: str) -> None:
        """Mostra un messaggio di errore all'utente.

        :param widget: parent widget delle finestra di errore
        :param titolo: titolo della finestra di errore
        :param testo: testo descrittivo
        """
        QMessageBox.critical(widget, titolo, testo)

    def __set_pagina_focus(self, pagina: NuovoGenereView) -> None:
        """Evidenzia il campo con input non valido.

        :param pagina: widget dove si è verificato l'errore d'input"""
        pagina.focusNextChild()
        if not pagina.nome.text().strip():
            return
        pagina.focusNextChild()
