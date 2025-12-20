from PyQt6.QtCore import pyqtSignal, QObject
from typing import Optional
from functools import partial

from model.model import Model
from model.pianificazione.regia import Regia
from model.exceptions import (
    DatoIncongruenteException,
    IdInesistenteException,
    IdOccupatoException,
)

from view.info.pagine.modifica_regia import ModificaRegiaView, NuovaRegiaView
from view.messageView import MessageView


class CURegiaController(QObject):
    """Gestisce il salvataggio delle regie create e modificate.

    Segnali:
    - goBackRequest(): emesso per tornare all'ultima pagina visualizzata
    - getNavPageRequest(str, dict): emesso per ottenere la pagina da cui si prenderà l'input
    """

    goBackRequest = pyqtSignal()
    getNavPageRequest = pyqtSignal(str, dict)

    def __init__(
        self,
        model: Model,
        n_regia_v: NuovaRegiaView,
        m_regia_v: ModificaRegiaView,
        messsage_v: MessageView,
    ) -> None:
        super().__init__()
        self.__model = model
        self.__nuova_regia_view = n_regia_v  # Pagina Nuova Regia
        self.__modifica_regia_view = m_regia_v  # Pagina Modifica Regia
        self.__message_view = messsage_v  # View dedicata ai popup

        self._connect_signals()

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    def _connect_signals(self) -> None:
        # Annulla creazione Regia
        self.__nuova_regia_view.annullaRequest.connect(  # type:ignore
            self.annulla_salvataggio
        )
        # Conferma creazione Regia
        self.__nuova_regia_view.salvaRequest.connect(  # type:ignore
            partial(self.salva_regia, is_new=True)
        )

        # Annulla modifica Regia
        self.__modifica_regia_view.annullaRequest.connect(  # type:ignore
            self.annulla_salvataggio
        )
        # Conferma modifica Regia
        self.__modifica_regia_view.salvaRequest.connect(  # type:ignore
            partial(self.salva_regia, is_new=False)
        )

    # ------------------------- METODI PUBBLICI -------------------------

    def get_regia(self, id_: int) -> Optional[Regia]:
        return self.__model.get_spettacolo(id_)
        # - CORRIGGERE: Come mi assicuro che sia Regia?

    def aggiungi_regia(self, regia: Regia) -> None:
        self.__model.aggiungi_spettacolo(regia)

    def modifica_regia(self, regia_modificata: Regia) -> None:
        self.__model.modifica_spettacolo(regia_modificata)

    def annulla_salvataggio(self, cur_pagina: NuovaRegiaView) -> None:
        """Annulla l'operazione di creazione o modifica di una regia.

        :param cur_pagina: pagina dove fare il reset dopo ritornare alla paginaVisualizzaOpera
        """
        self.goBackRequest.emit()
        cur_pagina.reset_pagina()

    def salva_regia(self, is_new: bool) -> None:
        """Salva la regia creata o modificata nel `GestoreSpettacoli`.

        :param is_new: verifica se si deve creare una regia o modificare una esistente
        """
        CAMPI_NECESSARI = (
            "<b>ATTENZIONE</b>: E' necessario compilare tutti i campi d'input."
        )

        if is_new:
            # Ottieni la pagina NuovaRegiaView
            cur_pagina = self.__nuova_regia_view

            # Ottieni l'input inserito
            titolo = cur_pagina.titolo.text()
            note = cur_pagina.note.toPlainText()
            # - Aggiungere interpreti
            # - Aggiungere tecnici
            regista = cur_pagina.regista.text()
            anno = cur_pagina.anno.value()
            id_opera = cur_pagina.opera.currentData()

            # Tenta di creare la nuova opera
            try:
                nuova_regia = Regia(
                    regista, anno, id_opera, titolo, note, {}, {}
                )  # - CORRIGERE: Non usare questi dict vuoti
            except DatoIncongruenteException as exc:
                # E' stato trovato un campo con input non valido
                cur_pagina.show_input_error(CAMPI_NECESSARI)
                cur_pagina.set_pagina_focus()
                self.__message_view.mostra_errore(
                    cur_pagina, "Input non valido", f"Si è verificato un errore: {exc}"
                )
            else:
                cur_pagina.show_input_error("")

                try:
                    self.aggiungi_regia(nuova_regia)
                except IdOccupatoException as exc:
                    # Esiste già una regia con quell'id
                    self.__message_view.mostra_errore(
                        cur_pagina,
                        "ID Regia occupata",
                        f"Si è verificato un errore: {exc}",
                    )
                else:
                    self.goBackRequest.emit()
        elif not is_new:
            # Ottieni la pagina ModificaRegiaView
            cur_pagina = self.__modifica_regia_view

            # Crea una copia della regia originale
            copia_regia: Optional[Regia] = self.get_regia(cur_pagina.cur_id_regia)
            if not isinstance(copia_regia, Regia):
                # Non esiste regia con l'id salvata nella pagina
                self.__message_view.mostra_errore(
                    cur_pagina,
                    "Errore nel salvataggio",
                    f"Non è presente nessuna regia con id {cur_pagina.cur_id_regia}. "
                    + "Impossibile effettuare le modifiche.",
                )
                return

            # Ottieni l'input inserito
            titolo = cur_pagina.titolo.text()
            note = cur_pagina.note.toPlainText()
            # - Aggiungere interpreti
            # - Aggiungere tecnici
            regista = cur_pagina.regista.text()
            anno = cur_pagina.anno.value()
            id_opera = cur_pagina.opera.currentData()

            # Tenta di modificare la regia
            try:
                copia_regia.set_titolo(titolo)
                copia_regia.set_note(note)
                copia_regia.set_interpreti({})  # - CORRIGGERE!!!
                copia_regia.set_tecnici({})  # - CORRIGGERE!!!
                copia_regia.set_regista(regista)
                copia_regia.set_anno_produzione(anno)
                copia_regia.set_id_opera(id_opera)
            except DatoIncongruenteException as exc:
                cur_pagina.show_input_error(CAMPI_NECESSARI)
                cur_pagina.set_pagina_focus()
                self.__message_view.mostra_errore(
                    cur_pagina, "Input non valido", f"Si è verificato un errore: {exc}"
                )
            else:
                cur_pagina.show_input_error("")

                try:
                    self.modifica_regia(copia_regia)
                except IdInesistenteException as exc:
                    # Non esiste una regia con quell'id
                    self.__message_view.mostra_errore(
                        cur_pagina,
                        "ID Regia insesistente",
                        f"Si è verificato un errore: {exc}",
                    )
                else:
                    self.goBackRequest.emit()
