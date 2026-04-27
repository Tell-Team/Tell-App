from model.organizzazione.occupazione import Occupazione
from model.exceptions import (
    IdOccupatoException,
    IdInesistenteException,
    OccupatoException,
)
from typing import Optional
import copy


class GestoreOccupazioni:
    def __init__(self):
        self.__lista_occupazioni: list[Occupazione] = []

    # Stato
    def evento_in_uso(self, id_: int) -> bool:
        for o in self.__lista_occupazioni:
            if o.get_id_evento() == id_:
                return True

        return False

    def posto_in_uso(self, id_: int) -> bool:
        for o in self.__lista_occupazioni:
            if o.get_id_posto() == id_:
                return True

        return False

    def prenotazione_in_uso(self, id_: int) -> bool:
        for o in self.__lista_occupazioni:
            if o.get_id_prenotazione() == id_:
                return True

        return False

    # Getters
    def get_max_id(self) -> int:
        ids = map(lambda x: x.get_id(), self.__lista_occupazioni)

        try:
            return max(ids)
        except ValueError:
            return -1

    def get_occupazione(self, id_: int) -> Optional[Occupazione]:
        for o in self.__lista_occupazioni:
            if o.get_id() == id_:
                return copy.copy(o)

        return None

    def get_occupazioni_by_prenotazione(
        self, id_prenotazione: int
    ) -> list[Occupazione]:
        return copy.deepcopy(
            list(
                filter(
                    lambda o: o.get_id_prenotazione() == id_prenotazione,
                    self.__lista_occupazioni,
                )
            )
        )

    def get_occupazioni_by_evento(self, id_evento: int) -> list[Occupazione]:
        return copy.deepcopy(
            list(
                filter(
                    lambda o: o.get_id_evento() == id_evento, self.__lista_occupazioni
                )
            )
        )

    # Validazione
    def __controllo_unique_key(self, primo: Occupazione, secondo: Occupazione):
        """Throws: OccupatoException"""
        if (
            primo.get_id_evento() == secondo.get_id_evento()
            and primo.get_id_posto() == secondo.get_id_posto()
        ):
            raise OccupatoException(
                f"Il posto con id {secondo.get_id_posto()} all'evento con id {secondo.get_id_evento()} è già occupato."
            )

    # Modificatori
    def aggiungi_occupazione(self, occupazione: Occupazione):
        """Throws: IdOccupatoException, OccupatoException"""
        for o in self.__lista_occupazioni:
            if o.get_id() == occupazione.get_id():
                raise IdOccupatoException(
                    f"E' già presente un'occupazione con id {occupazione.get_id()}."
                )

            self.__controllo_unique_key(o, occupazione)

        self.__lista_occupazioni.append(copy.copy(occupazione))

    def elimina_occupazione(self, id_: int):
        """Throws: IdInesistenteException"""
        for i, o in enumerate(self.__lista_occupazioni):
            if o.get_id() == id_:
                self.__lista_occupazioni.pop(i)
                return

        raise IdInesistenteException(
            f"Non è presente nessuna occupazione con id {id_}."
        )

    def elimina_occupazioni_by_prenotazione(self, id_prenotazione: int):
        self.__lista_occupazioni = list(
            filter(
                lambda p: p.get_id_prenotazione() != id_prenotazione,
                self.__lista_occupazioni,
            )
        )

    def modifica_occupazione(self, occupazione_modificata: Occupazione):
        """Throws: IdInesistenteException, OccupatoException"""
        posizione_da_modificare: Optional[int] = None

        for i, o in enumerate(self.__lista_occupazioni):
            if o.get_id() != occupazione_modificata.get_id():
                self.__controllo_unique_key(o, occupazione_modificata)
            else:
                posizione_da_modificare = i

        if posizione_da_modificare is None:
            raise IdInesistenteException(
                f"Non è presente nessuna occupazione con id {occupazione_modificata.get_id()}."
            )

        self.__lista_occupazioni[posizione_da_modificare] = copy.copy(
            occupazione_modificata
        )
