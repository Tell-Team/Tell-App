from typing import Optional, override

from core.controller import AbstractCUController

from model.model.model import Model
from model.pianificazione.genere import Genere
from model.exceptions import (
    DatoIncongruenteException,
    IdInesistenteException,
    IdOccupatoException,
)

from view.info.pagine import ModificaGenerePage, NuovoGenerePage

from view.utils import mostra_error_popup


CAMPI_NECESSARI = "<b>ATTENZIONE</b>: È necessario compilare tutti i campi d'input."


class CUGenereController(AbstractCUController):
    """Gestisce il salvataggio dei generi creati e modificati.

    Segnali
    ---
    - `goBackRequest()`: emesso per tornare alla pagina `InfoSection`.
    """

    _view_nuova: NuovoGenerePage
    _view_modifica: ModificaGenerePage

    def __init__(
        self, model: Model, n_genere_v: NuovoGenerePage, m_genere_v: ModificaGenerePage
    ):
        if type(n_genere_v) is not NuovoGenerePage:
            raise TypeError("Atteso NuovoGenerePage per n_genere_v.")
        if type(m_genere_v) is not ModificaGenerePage:
            raise TypeError("Atteso ModificaGenerePage per m_genere_v.")

        super().__init__(model, n_genere_v, m_genere_v)

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __get_genere(self, id_: int) -> Optional[Genere]:
        return self._model.get_genere(id_)

    def __aggiungi_genere(self, genere: Genere) -> None:
        self._model.aggiungi_genere(genere)

    def __modifica_genere(self, genere_modificato: Genere) -> None:
        self._model.modifica_genere(genere_modificato)

    @override
    def _richiesta_nuovo(self) -> None:
        current_pagina = self._view_nuova

        # Ottieni l'input inserito
        nome = current_pagina.nome.text()
        descrizione = current_pagina.descrizione.toPlainText()

        # Tenta di creare il nuovo genere
        try:
            nuovo_genere = Genere(nome, descrizione)
        except DatoIncongruenteException as exc:
            # È stato trovato un campo con input non valido
            current_pagina.mostra_msg_input_error(CAMPI_NECESSARI)
            mostra_error_popup(current_pagina, "Input non valido", str(exc))
        else:
            current_pagina.mostra_msg_input_error("")

            try:
                self.__aggiungi_genere(nuovo_genere)
            except IdOccupatoException as exc:
                # Esiste già un genere con quell'id
                mostra_error_popup(current_pagina, "ID Genere occupato", str(exc))
            else:
                self.goBackRequest.emit()

    @override
    def _richiesta_modifica(self) -> None:
        current_pagina = self._view_modifica

        # Crea una copia del genere originale
        copia_genere = self.__get_genere(current_pagina.id_current_genere)
        if not isinstance(copia_genere, Genere):
            # Non esiste genere con l'id salvato nella pagina
            mostra_error_popup(
                current_pagina,
                "Errore nel salvataggio",
                f"Non è presente nessun genere con id {current_pagina.id_current_genere}. "
                + "Impossibile effettuare le modifiche.",
            )
            return

        # Ottiene l'input inserito
        nome = current_pagina.nome.text()
        descrizione = current_pagina.descrizione.toPlainText()

        # Tenta di modificare il genere
        try:
            copia_genere.set_nome(nome)
            copia_genere.set_descrizione(descrizione)
        except DatoIncongruenteException as exc:
            current_pagina.mostra_msg_input_error(CAMPI_NECESSARI)
            mostra_error_popup(current_pagina, "Input non valido", str(exc))
        else:
            current_pagina.mostra_msg_input_error("")

            try:
                self.__modifica_genere(copia_genere)
            except IdInesistenteException as exc:
                # Non esiste un genere con quell'id
                mostra_error_popup(current_pagina, "ID Generi insesistente", str(exc))
            else:
                self.goBackRequest.emit()
