from typing import Optional, override

from core.controller import AbstractCUController

from model.model.model import Model
from model.pianificazione.opera import Opera
from model.exceptions import (
    DatoIncongruenteException,
    IdInesistenteException,
    IdOccupatoException,
)

from view.info.pagine import ModificaOperaView, NuovaOperaView

from view.utils import mostra_error_popup


CAMPI_NECESSARI = "<b>ATTENZIONE</b>: È necessario compilare tutti i campi d'input."


class CUOperaController(AbstractCUController):
    """Gestisce il salvataggio delle opere create e modificate.

    Segnali
    ---
    - `goBackRequest()`: emesso per tornare alla pagina `InfoSectionView`.
    """

    _view_nuova: NuovaOperaView
    _view_modifica: ModificaOperaView

    def __init__(
        self, model: Model, n_opera_v: NuovaOperaView, m_opera_v: ModificaOperaView
    ):
        if type(n_opera_v) is not NuovaOperaView:
            raise TypeError("Atteso NuovaOperaView per n_opera_v.")
        if type(m_opera_v) is not ModificaOperaView:
            raise TypeError("Atteso ModificaOperaView per m_regia_v.")

        super().__init__(model, n_opera_v, m_opera_v)

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __get_opera(self, id_: int) -> Optional[Opera]:
        return self._model.get_opera(id_)

    def __aggiungi_opera(self, opera: Opera) -> None:
        self._model.aggiungi_opera(opera)

    def __modifica_opera(self, opera_modificata: Opera) -> None:
        self._model.modifica_opera(opera_modificata)

    @override
    def _richiesta_nuovo(self) -> None:
        current_pagina = self._view_nuova

        # Ottieni l'input inserito
        nome = current_pagina.nome.text()
        trama = current_pagina.trama.toPlainText()
        id_genere = current_pagina.genere.currentData()
        compositore = current_pagina.compositore.text()
        librettista = current_pagina.librettista.text()
        atti = current_pagina.atti.value()
        data = current_pagina.data.date().toPyDate()
        teatro = current_pagina.teatro.text()

        # Tenta di creare la nuova opera
        try:
            nuova_opera = Opera(
                nome, compositore, librettista, atti, data, teatro, trama, id_genere
            )
        except DatoIncongruenteException as exc:
            # È stato trovato un campo con input non valido
            current_pagina.mostra_msg_input_error(CAMPI_NECESSARI)
            mostra_error_popup(current_pagina, "Input non valido", str(exc))
        else:
            current_pagina.mostra_msg_input_error("")

            try:
                self.__aggiungi_opera(nuova_opera)
            except IdInesistenteException as exc:
                # L'opera è collegata ad un genere che non esiste
                mostra_error_popup(current_pagina, "Genere inesistente", str(exc))
            except IdOccupatoException as exc:
                # Esiste già un'opera con quell'id
                mostra_error_popup(current_pagina, "ID Opera occupato", str(exc))
            else:
                self.goBackRequest.emit()

    @override
    def _richiesta_modifica(self) -> None:
        current_pagina = self._view_modifica

        # Crea una copia dell'opera originale
        copia_opera = self.__get_opera(current_pagina.id_current_opera)
        if not isinstance(copia_opera, Opera):
            # Non esiste opera con l'id salvata nella pagina
            mostra_error_popup(
                current_pagina,
                "Errore nel salvataggio",
                f"Non è presente nessuna opera con id {current_pagina.id_current_opera}. "
                + "Impossibile effettuare le modifiche.",
            )
            return

        # Ottieni l'input inserito
        nome = current_pagina.nome.text()
        trama = current_pagina.trama.toPlainText()
        id_genere = current_pagina.genere.currentData()
        compositore = current_pagina.compositore.text()
        librettista = current_pagina.librettista.text()
        atti = current_pagina.atti.value()
        data = current_pagina.data.date().toPyDate()
        teatro = current_pagina.teatro.text()

        # Tenta di modificare l'opera
        try:
            copia_opera.set_nome(nome)
            copia_opera.set_trama(trama)

            if id_genere < 0:
                current_pagina.mostra_msg_input_error(CAMPI_NECESSARI)
                mostra_error_popup(
                    current_pagina,
                    "Input non valido",
                    "È necessario selezionare un genere.",
                )
                return

            copia_opera.set_id_genere(id_genere)
            copia_opera.set_compositore(compositore)
            copia_opera.set_librettista(librettista)
            copia_opera.set_numero_atti(atti)
            copia_opera.set_data_prima_rappresentazione(data)
            copia_opera.set_teatro_prima_rappresentazione(teatro)

        except DatoIncongruenteException as exc:
            # È stato trovato un campo con input non valido
            current_pagina.mostra_msg_input_error(CAMPI_NECESSARI)
            mostra_error_popup(current_pagina, "Input non valido", str(exc))
        else:
            current_pagina.mostra_msg_input_error("")

            try:
                self.__modifica_opera(copia_opera)
            except IdInesistenteException as exc:
                # Non esiste un'opera con quell'id
                mostra_error_popup(current_pagina, "ID Opera inesistente", str(exc))
            else:
                self.goBackRequest.emit()
