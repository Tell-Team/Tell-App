from PyQt6.QtCore import pyqtSignal, QObject
from typing import Optional

from model.model import Model
from model.organizzazione.posto import Posto
from model.exceptions import (
    DatoIncongruenteException,
    OccupatoException,
    IdInesistenteException,
)

from view.teatro.pagine import ModificaPostoView
from view.utils import PopupMessage


CAMPI_NECESSARI = (
    "<b>ATTENZIONE</b>: È necessario compilare i campi di input contrassegnati con *."
)


class ModificaPostoController(QObject):
    """Controller dedicato alla modifica di posti.

    Segnali
    ---
    - `goBackRequest()`: emesso per tornare alla pagina `VisualizzaSezioneView`.
    """

    goBackRequest: pyqtSignal = pyqtSignal()

    def __init__(self, model: Model, modifica: ModificaPostoView):
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
            PopupMessage.mostra_errore(
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
            PopupMessage.mostra_errore(
                pagina,
                "Input non valido",
                f"Si è verificato un errore: {exc}",
            )
        else:
            pagina.mostra_msg_input_error("")

            try:
                self.__modifica_posto(copia_posto)
            except OccupatoException as exc:
                # Esiste già un posto con quel numero
                PopupMessage.mostra_errore(
                    pagina,
                    "Numero Posto occupato",
                    f"Si è verificato un errore: {exc}",
                )
            except IdInesistenteException as exc:
                # Non esiste un posto con quell'id
                PopupMessage.mostra_errore(
                    pagina,
                    "ID Posto inesistente",
                    f"Si è verificato un errore: {exc}",
                )
            else:
                self.goBackRequest.emit()
