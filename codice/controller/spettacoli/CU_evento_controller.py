from PyQt6.QtCore import QDateTime
from typing import Optional, override

from core.controller import AbstractCUController

from model.model import Model
from model.organizzazione.evento import Evento
from model.exceptions import (
    DatoIncongruenteException,
    IdOccupatoException,
    IdInesistenteException,
)

from view.spettacoli.pagine import ModificaEventoView, NuovoEventoView

from view.utils import PopupMessage


class CUEventoController(AbstractCUController):
    """Gestisce il salvataggio degli eventi creati e modificati.

    Segnali
    ---
    - `goBackRequest()`: emesso per tornare alla pagina `VisualizzaSpettacoloView`.
    """

    _view_nuova: NuovoEventoView
    _view_modifica: ModificaEventoView

    def __init__(
        self,
        model: Model,
        n_evento_v: NuovoEventoView,
        m_evento_v: ModificaEventoView,
    ):
        if type(n_evento_v) is not NuovoEventoView:
            raise TypeError("Atteso NuovoEventoView per n_evento_v.")
        if type(m_evento_v) is not ModificaEventoView:
            raise TypeError("Atteso ModificaEventoView per m_evento_v.")

        super().__init__(model, n_evento_v, m_evento_v)

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __get_evento(self, id_: int) -> Optional[Evento]:
        return self._model.get_evento(id_)

    def __aggiungi_evento(self, evento: Evento) -> None:
        self._model.aggiungi_evento(evento)

    def __modifica_evento(self, evento_modificato: Evento) -> None:
        self._model.modifica_evento(evento_modificato)

    @override
    def _inizia_salvataggio(self, is_new: bool) -> None:
        """Salva l'evento creato o modificato nel `GestoreGeneri`.

        :param is_new: verifica se si deve creare un evento o modificare una esistente
        """
        DATI_INCONGRUENTI = (
            "<b>ATTENZIONE</b>: È necessario inserire una data ed ore validi."
        )

        if is_new:
            current_pagina = self._view_nuova

            # Ottieni l'input inserito
            data = current_pagina.data.date()
            time = current_pagina.ora.time()
            py_date = QDateTime(data, time).toPyDateTime()

            # Tenta di creare il nuovo evento
            try:
                nuovo_evento = Evento(py_date, current_pagina.id_spettacolo)
            except DatoIncongruenteException as exc:
                # È stato trovato un campo con input non valido
                current_pagina.mostra_msg_input_error(DATI_INCONGRUENTI)
                PopupMessage.mostra_errore(
                    current_pagina,
                    "Input non valido",
                    f"Si è verificato un errore: {exc}",
                )
            else:
                current_pagina.mostra_msg_input_error("")

                try:
                    self.__aggiungi_evento(nuovo_evento)
                except IdOccupatoException as exc:
                    # Esiste già un evento con quell'id
                    PopupMessage.mostra_errore(
                        current_pagina,
                        "ID Evento occupato",
                        f"Si è verificato un errore: {exc}",
                    )
                else:
                    self.goBackRequest.emit()
        elif not is_new:
            current_pagina = self._view_modifica

            # Crea una copia del evento originale
            copia_evento = self.__get_evento(current_pagina.id_current_evento)
            if not isinstance(copia_evento, Evento):
                # Non esiste evento con l'id salvato nella pagina
                PopupMessage.mostra_errore(
                    current_pagina,
                    "Errore nel salvataggio",
                    f"Non è presente nessun evento con id {current_pagina.id_current_evento}. "
                    + "Impossibile effettuare le modifiche.",
                )
                return

            # Ottieni l'input inserito
            data = current_pagina.data.date()
            time = current_pagina.ora.time()

            py_date = QDateTime(data, time).toPyDateTime()

            # Tenta di modificare l'evento
            try:
                copia_evento.set_data_ora(py_date)
            except DatoIncongruenteException as exc:
                current_pagina.mostra_msg_input_error(DATI_INCONGRUENTI)
                PopupMessage.mostra_errore(
                    current_pagina,
                    "Input non valido",
                    f"Si è verificato un errore: {exc}",
                )
            else:
                current_pagina.mostra_msg_input_error("")

                try:
                    self.__modifica_evento(copia_evento)
                except IdInesistenteException as exc:
                    # Non esiste un genere con quell'id
                    PopupMessage.mostra_errore(
                        current_pagina,
                        "ID Evento insesistente",
                        f"Si è verificato un errore: {exc}",
                    )
                else:
                    self.goBackRequest.emit()
