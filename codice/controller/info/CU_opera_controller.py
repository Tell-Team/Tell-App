from PyQt6.QtCore import pyqtSignal, QObject
from typing import Optional
from functools import partial

from model.model import Model
from model.pianificazione.opera import Opera
from model.pianificazione.genere import Genere
from model.exceptions import (
    DatoIncongruenteException,
    IdInesistenteException,
    IdOccupatoException,
)

from view.info.pagine.modifica_opera import ModificaOperaView, NuovaOperaView
from view.messageView import MessageView


class CUOperaController(QObject):
    """Gestisce il salvataggio delle opere create e modificate.

    Segnali:
    - goBackRequest(): emesso per tornare all'ultima pagina visualizzata;
    - getNavPageRequest(str, dict): emesso per ottenere la pagina da cui si prenderà l'input.
    """

    goBackRequest = pyqtSignal()
    getNavPageRequest = pyqtSignal(str, dict)

    def __init__(
        self,
        model: Model,
        n_opera_v: NuovaOperaView,
        m_opera_v: ModificaOperaView,
        message_v: MessageView,
    ) -> None:
        super().__init__()
        self.__model = model
        self.__nuova_opera_view = n_opera_v  # Pagina Nuova Opera
        self.__modifica_opera_view = m_opera_v  # Pagina Modifica Opera
        self.__message_view = message_v  # View dedicata ai popup

        self._connect_signals()

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    def _connect_signals(self) -> None:
        # Annulla creazione Opera
        self.__nuova_opera_view.annullaRequest.connect(  # type:ignore
            self.annulla_salvataggio
        )
        # Conferma creazione Opera
        self.__nuova_opera_view.salvaRequest.connect(  # type:ignore
            partial(self.salva_opera, is_new=True)
        )

        # Annulla modifica Opera
        self.__modifica_opera_view.annullaRequest.connect(  # type:ignore
            self.annulla_salvataggio
        )
        # Conferma modifica Opera
        self.__modifica_opera_view.salvaRequest.connect(  # type:ignore
            partial(self.salva_opera, is_new=False)
        )

    # ------------------------- METODI PUBBLICI -------------------------

    def get_opera(self, id_: int) -> Optional[Opera]:
        return self.__model.get_opera(id_)

    def aggiungi_opera(self, opera: Opera) -> None:
        self.__model.aggiungi_opera(opera)

    def modifica_opera(self, opera_modificata: Opera) -> None:
        self.__model.modifica_opera(opera_modificata)

    def get_generi(self) -> list[Genere]:
        return self.__model.get_generi()

    def annulla_salvataggio(self, cur_pagina: NuovaOperaView) -> None:
        """Annulla l'operazione di creazione o modifica di un'opera.

        :param cur_pagina: pagina dove fare il reset dopo ritornare alla sezione Info"""
        self.goBackRequest.emit()
        cur_pagina.reset_pagina()

    def salva_opera(self, is_new: bool = True) -> None:
        """Salva l'opera creata o modificata nel `GestoreOpere`.

        :param is_new: verifica se si deve creare un'opera o modificare una esistente"""
        CAMPI_NECESSARI = (
            "<b>ATTENZIONE</b>: E' necessario compilare tutti i campi d'input."
        )

        if is_new:
            # Ottieni la pagina NuovaOperaView
            cur_pagina = self.__nuova_opera_view

            # Ottieni l'input inserito
            nome = cur_pagina.nome.text()
            trama = cur_pagina.trama.toPlainText()
            id_genere: int = cur_pagina.genere.currentData()
            compositore = cur_pagina.compositore.text()
            librettista = cur_pagina.librettista.text()
            atti = cur_pagina.atti.value()
            data = cur_pagina.data.date().toPyDate()
            teatro = cur_pagina.teatro.text()

            # Tenta di creare la nuova opera
            try:
                nuova_opera = Opera(
                    nome, compositore, librettista, atti, data, teatro, trama, id_genere
                )
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
                    self.aggiungi_opera(nuova_opera)
                except IdInesistenteException as exc:
                    # L'opera è collegata ad un genere che non esiste
                    self.__message_view.mostra_errore(
                        cur_pagina,
                        "Genere inesistente",
                        f"Si è verificato un errore: {exc}",
                    )
                except IdOccupatoException as exc:
                    # Esiste già un'opera con quell'id
                    self.__message_view.mostra_errore(
                        cur_pagina,
                        "ID Opera occupato",
                        f"Si è verificato un errore: {exc}",
                    )
                else:
                    self.goBackRequest.emit()
        elif not is_new:
            # Ottieni la pagina ModificaOperaView
            cur_pagina = self.__modifica_opera_view

            # Crea una copia dell'opera originale
            copia_opera: Optional[Opera] = self.get_opera(cur_pagina.cur_id_opera)
            if not isinstance(copia_opera, Opera):
                # Non esiste opera con l'id salvata nella pagina
                self.__message_view.mostra_errore(
                    cur_pagina,
                    "Errore nel salvataggio",
                    f"Non è presente nessun'opera con id {cur_pagina.cur_id_opera}. "
                    + "Impossibile effettuare le modifiche.",
                )
                return

            # Ottieni l'input inserito
            nome = cur_pagina.nome.text()
            trama = cur_pagina.trama.toPlainText()
            id_genere: int = cur_pagina.genere.currentData()
            compositore = cur_pagina.compositore.text()
            librettista = cur_pagina.librettista.text()
            atti = cur_pagina.atti.value()
            data = cur_pagina.data.date().toPyDate()
            teatro = cur_pagina.teatro.text()

            # Tenta di modificare l'opera
            try:
                copia_opera.set_nome(nome)
                copia_opera.set_trama(trama)
                copia_opera.set_id_genere(id_genere)
                copia_opera.set_compositore(compositore)
                copia_opera.set_librettista(librettista)
                copia_opera.set_numero_atti(atti)
                copia_opera.set_data_prima_rappresentazione(data)
                copia_opera.set_teatro_prima_rappresentazione(teatro)
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
                    self.modifica_opera(copia_opera)
                except IdInesistenteException as exc:
                    # Non esiste un'opera con quell'id
                    self.__message_view.mostra_errore(
                        cur_pagina,
                        "ID Opera inesistente",
                        f"Si è verificato un errore: {exc}",
                    )
                else:
                    self.goBackRequest.emit()
