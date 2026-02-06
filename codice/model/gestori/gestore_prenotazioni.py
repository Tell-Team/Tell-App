from model.organizzazione.prenotazione import Prenotazione
from model.exceptions import (
    IdOccupatoException,
    IdInesistenteException,
)
from typing import Optional
import copy


class GestorePrenotazioni:
    def __init__(self):
        self.__lista_prenotazioni: list[Prenotazione] = []

    # Stato
    def ha_prenotazione(self, id_: int) -> bool:
        for p in self.__lista_prenotazioni:
            if p.get_id() == id_:
                return True

        return False

    # Getters
    def get_max_id(self) -> int:
        ids = map(lambda x: x.get_id(), self.__lista_prenotazioni)

        try:
            return max(ids)
        except ValueError:
            return -1

    def get_prenotazione(self, id_: int) -> Optional[Prenotazione]:
        for p in self.__lista_prenotazioni:
            if p.get_id() == id_:
                return copy.copy(p)

        return None

    def get_prenotazioni(self) -> list[Prenotazione]:
        return copy.deepcopy(self.__lista_prenotazioni)

    def get_prenotazioni_by_nominativo(self, nominativo: str) -> list[Prenotazione]:
        nominativo_lower = nominativo.lower()
        return copy.deepcopy(
            list(
                filter(
                    lambda p: nominativo_lower in p.get_nominativo().lower(),
                    self.__lista_prenotazioni,
                )
            )
        )

    # Modificatori
    def aggiungi_prenotazione(self, prenotazione: Prenotazione):
        """Throws: IdOccupatoException"""
        for p in self.__lista_prenotazioni:
            if p.get_id() == prenotazione.get_id():
                raise IdOccupatoException(
                    f"E' già presente una prenotazione con id {prenotazione.get_id()}."
                )

        self.__lista_prenotazioni.append(copy.copy(prenotazione))

    def elimina_prenotazione(self, id_: int):
        """Throws: IdInesistenteException"""
        for i, p in enumerate(self.__lista_prenotazioni):
            if p.get_id() == id_:
                self.__lista_prenotazioni.pop(i)
                return

        raise IdInesistenteException(
            f"Non è presente nessuna prenotazione con id {id_}."
        )

    def modifica_prenotazione(self, prenotazione_modificata: Prenotazione):
        """Throws: IdInesistenteException"""
        for i, p in enumerate(self.__lista_prenotazioni):
            if p.get_id() == prenotazione_modificata.get_id():
                self.__lista_prenotazioni[i] = copy.copy(prenotazione_modificata)
                return

        raise IdInesistenteException(
            f"Non è presente nessuna prenotazione con id {prenotazione_modificata.get_id()}."
        )
