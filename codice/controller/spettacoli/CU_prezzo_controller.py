from typing import Optional, override

from core.controller import AbstractCUController

from model.model.model import Model
from model.organizzazione.prezzo import Prezzo
from model.exceptions import (
    DatoIncongruenteException,
    IdOccupatoException,
    IdInesistenteException,
    OccupatoException,
)

from view.spettacoli.pagine import ModificaPrezzoView, NuovoPrezzoView

from view.utils import mostra_error_popup


DATI_INCONGRUENTI = "<b>ATTENZIONE</b>: È necessario inserire un prezzo valido."


class CUPrezzoController(AbstractCUController):
    """Gestisce il salvataggio degli eventi creati e modificati.

    Segnali
    ---
    - `goBackRequest()`: emesso per tornare alla pagina `VisualizzaSpettacoloView`.
    """

    _view_nuova: NuovoPrezzoView
    _view_modifica: ModificaPrezzoView

    def __init__(
        self,
        model: Model,
        n_prezzo_v: NuovoPrezzoView,
        m_prezzo_v: ModificaPrezzoView,
    ):
        if type(n_prezzo_v) is not NuovoPrezzoView:
            raise TypeError("Atteso NuovoPrezzoView per n_prezzo_v.")
        if type(m_prezzo_v) is not ModificaPrezzoView:
            raise TypeError("Atteso ModificaPrezzoView per m_prezzo_v.")

        super().__init__(model, n_prezzo_v, m_prezzo_v)

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __get_prezzo(self, id_: int) -> Optional[Prezzo]:
        return self._model.get_prezzo(id_)

    def __aggiungi_prezzo(self, prezzo: Prezzo) -> None:
        self._model.aggiungi_prezzo(prezzo)

    def __modifica_prezzo(self, prezzo_modificato: Prezzo) -> None:
        self._model.modifica_prezzo(prezzo_modificato)

    @override
    def _richiesta_nuovo(self) -> None:
        current_pagina = self._view_nuova

        # Ottieni l'input inserito
        ammontare_str = current_pagina.prezzo.text()
        ammontare = float(ammontare_str) if ammontare_str else -1
        id_spettacolo = current_pagina.id_spettacolo
        id_sezione = current_pagina.id_sezione

        # Tenta di creare il nuovo prezzo
        try:
            nuovo_prezzo = Prezzo(ammontare, id_spettacolo, id_sezione)
        except DatoIncongruenteException as exc:
            # È stato trovato un campo con input non valido
            current_pagina.mostra_msg_input_error(DATI_INCONGRUENTI)
            mostra_error_popup(current_pagina, "Input non valido", str(exc))
        else:
            current_pagina.mostra_msg_input_error("")

            try:
                self.__aggiungi_prezzo(nuovo_prezzo)
            except IdOccupatoException as exc:
                # Esiste già un evento con quell'id
                mostra_error_popup(current_pagina, "ID Evento occupato", str(exc))
            except OccupatoException as exc:
                # Esiste già un prezzo di la sezione indicata per lo spettacolo indicato
                mostra_error_popup(current_pagina, "Posto esistente", str(exc))
            else:
                self.goBackRequest.emit()

    @override
    def _richiesta_modifica(self) -> None:
        current_pagina = self._view_modifica

        # Crea una copia del prezzp originale
        copia_prezzo = self.__get_prezzo(current_pagina.id_current_prezzo)
        if not isinstance(copia_prezzo, Prezzo):
            # Non esiste prezzo con l'id salvato nella pagina
            mostra_error_popup(
                current_pagina,
                "Errore nel salvataggio",
                f"Non è presente nessun prezzo con id {current_pagina.id_current_prezzo}. "
                + "Impossibile effettuare le modifiche.",
            )
            return

        # Ottieni l'input inserito
        ammontare_str = current_pagina.prezzo.text()
        ammontare = float(ammontare_str) if ammontare_str else -1
        # id_spettacolo = current_pagina.id_spettacolo
        # id_sezione = current_pagina.id_sezione

        # Tenta di modificare l'evento
        try:
            copia_prezzo.set_ammontare(ammontare)
        except DatoIncongruenteException as exc:
            current_pagina.mostra_msg_input_error(DATI_INCONGRUENTI)
            mostra_error_popup(current_pagina, "Input non valido", str(exc))
        else:
            current_pagina.mostra_msg_input_error("")

            try:
                self.__modifica_prezzo(copia_prezzo)
            except IdInesistenteException as exc:
                # Non esiste un prezzo con quell'id
                mostra_error_popup(current_pagina, "ID Prezzo insesistente", str(exc))
            except OccupatoException as exc:
                # Esiste già un prezzo di la sezione indicata per lo spettacolo indicato
                mostra_error_popup(current_pagina, "Prezzo esistente", str(exc))
            else:
                self.goBackRequest.emit()
