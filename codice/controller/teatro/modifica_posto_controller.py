from PyQt6.QtCore import pyqtSignal, QObject
from typing import Optional

from model.model.model import Model
from model.organizzazione.posto import Posto
from model.exceptions import (
    DatoIncongruenteException,
    OccupatoException,
    IdInesistenteException,
)

from view.teatro.pagine import ModificaPostoPage

from view.utils import mostra_error_popup


CAMPI_NECESSARI = (
    "<b>ATTENZIONE</b>: È necessario compilare i campi di input contrassegnati con *."
)


class ModificaPostoController(QObject):
    """Controller dedicato alla modifica di posti.

    Segnali
    ---
    - `goBackRequest()`: emesso per tornare alla pagina `VisualizzaSezionePage`.
    """

    goBackRequest = pyqtSignal()

    def __init__(self, model: Model, modifica: ModificaPostoPage):
        super().__init__()

        self.__model = model
        self.__view_modifica = modifica

        self._connect_signals()

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    def _connect_signals(self) -> None:
        # Annulla modifica
        self.__view_modifica.annullaRequest.connect(  # type:ignore
            self.__annulla_salvataggio
        )
        # Conferma modifica
        self.__view_modifica.salvaRequest.connect(  # type:ignore
            self.__inizia_salvataggio
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __get_posto(self, id_: int) -> Optional[Posto]:
        return self.__model.get_posto(id_)

    def __modifica_posto(self, copia_posto: Posto) -> None:
        self.__model.modifica_posto(copia_posto)

    def __annulla_salvataggio(self) -> None:
        self.goBackRequest.emit()
        self.__view_modifica.reset_pagina()

    def __inizia_salvataggio(self) -> None:
        pagina = self.__view_modifica

        # Crea una copia dello posto originale
        copia_posto = self.__get_posto(pagina.id_current_posto)
        if not isinstance(copia_posto, Posto):
            # Non esiste posto con l'id salvato nella pagina
            mostra_error_popup(
                pagina,
                "Errore nel salvataggio",
                f"Non è presente nessun posto con id {pagina.id_current_posto}. "
                + "Impossibile effettuare le modifiche.",
            )
            return

        fila = pagina.fila.text()
        numero = pagina.numero.value()

        try:
            copia_posto.set_fila(fila)
            copia_posto.set_numero(numero)
        except DatoIncongruenteException as exc:
            pagina.mostra_msg_input_error(CAMPI_NECESSARI)
            mostra_error_popup(pagina, "Input non valido", str(exc))
        else:
            pagina.mostra_msg_input_error("")

            try:
                self.__modifica_posto(copia_posto)
            except OccupatoException as exc:
                # Esiste già un posto con quel numero
                mostra_error_popup(pagina, "Numero Posto occupato", str(exc))
            except IdInesistenteException as exc:
                # Non esiste un posto con quell'id
                mostra_error_popup(pagina, "ID Posto inesistente", str(exc))
            else:
                self.goBackRequest.emit()
