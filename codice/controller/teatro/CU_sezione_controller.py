from typing import Optional, override

from core.controller import AbstractCUController

from model.model.model import Model
from model.organizzazione.sezione import Sezione
from model.exceptions import (
    DatoIncongruenteException,
    IdInesistenteException,
    IdOccupatoException,
)

from view.teatro.pagine import ModificaSezionePage, NuovaSezionePage

from view.utils import mostra_error_popup


CAMPI_NECESSARI = "<b>ATTENZIONE</b>: È necessario compilare tutti i campi d'input."


class CUSezioneController(AbstractCUController):
    """Gestisce il salvataggio delle sezioni create e modificate.

    Segnali
    ---
    - `goBackRequest()`: emesso per tornare alla pagina `TeatroSection`.
    """

    _view_nuova: NuovaSezionePage
    _view_modifica: ModificaSezionePage

    def __init__(
        self,
        model: Model,
        n_sezione_v: NuovaSezionePage,
        m_sezione_v: ModificaSezionePage,
    ):
        if type(n_sezione_v) is not NuovaSezionePage:
            raise TypeError("Atteso NuovaSezionePage per n_sezione_v.")
        if type(m_sezione_v) is not ModificaSezionePage:
            raise TypeError("Atteso ModificaSezionePage per m_sezione_v.")

        super().__init__(model, n_sezione_v, m_sezione_v)

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __get_sezione(self, id_: int) -> Optional[Sezione]:
        return self._model.get_sezione(id_)

    def __aggiungi_sezione(self, sezione: Sezione) -> None:
        self._model.aggiungi_sezione(sezione)

    def __modifica_sezione(self, sezione_modificata: Sezione) -> None:
        self._model.modifica_sezione(sezione_modificata)

    @override
    def _richiesta_nuovo(self) -> None:
        current_pagina = self._view_nuova

        # Ottieni l'input inserito
        nome = current_pagina.nome.text()
        descrizione = current_pagina.descrizione.toPlainText()

        # Tenta di creare il nuovo genere
        try:
            nuova_sezione = Sezione(nome, descrizione)
        except DatoIncongruenteException as exc:
            # È stato trovato un campo con input non valido
            current_pagina.mostra_msg_input_error(CAMPI_NECESSARI)
            mostra_error_popup(current_pagina, "Input non valido", str(exc))
        else:
            current_pagina.mostra_msg_input_error("")

            try:
                self.__aggiungi_sezione(nuova_sezione)
            except IdOccupatoException as exc:
                # Esiste già una sezione con quell'id
                mostra_error_popup(current_pagina, "ID Sezione occupato", str(exc))
            else:
                self.goBackRequest.emit()

    @override
    def _richiesta_modifica(self) -> None:
        current_pagina = self._view_modifica

        # Crea una copia della sezione originale
        copia_sezione = self.__get_sezione(current_pagina.id_current_sezione)
        if not isinstance(copia_sezione, Sezione):
            # Non esiste sezine con l'id salvato nella pagina
            mostra_error_popup(
                current_pagina,
                "Errore nel salvataggio",
                f"Non è presente nessuna sezione con id {current_pagina.id_current_sezione}. "
                + "Impossibile effettuare le modifiche.",
            )
            return

        # Ottiene l'input inserito
        nome = current_pagina.nome.text()
        descrizione = current_pagina.descrizione.toPlainText()

        # Tenta di modificare il genere
        try:
            copia_sezione.set_nome(nome)
            copia_sezione.set_descrizione(descrizione)
        except DatoIncongruenteException as exc:
            current_pagina.mostra_msg_input_error(CAMPI_NECESSARI)
            mostra_error_popup(current_pagina, "Input non valido", str(exc))
        else:
            current_pagina.mostra_msg_input_error("")

            try:
                self.__modifica_sezione(copia_sezione)
            except IdInesistenteException as exc:
                # Non esiste una sezione con quell'id
                mostra_error_popup(current_pagina, "ID Sezione insesistente", str(exc))
            else:
                self.goBackRequest.emit()
