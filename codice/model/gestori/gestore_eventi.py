from model.pianificazione.evento import Evento
from model.exceptions import IdOccupatoException, IdInesistenteException
from typing import Optional
import copy


class GestoreEventi:
    def __init__(self):
        self.__lista_eventi: list[Evento] = []

    # Stato
    def spettacolo_in_uso(self, id_: int) -> bool:
        for e in self.__lista_eventi:
            if e.get_id_spettacolo() == id_:
                return True

        return False

    def ha_evento(self, id_: int) -> bool:
        for e in self.__lista_eventi:
            if e.get_id() == id_:
                return True

        return False

    # Getters
    def get_max_id(self) -> int:
        ids = map(lambda x: x.get_id(), self.__lista_eventi)

        try:
            return max(ids)
        except ValueError:
            return -1

    def get_evento(self, id_: int) -> Optional[Evento]:
        for e in self.__lista_eventi:
            if e.get_id() == id_:
                return copy.copy(e)

        return None

    def get_eventi(self) -> list[Evento]:
        return copy.deepcopy(self.__lista_eventi)

    def get_eventi_by_spettacolo(self, id_: int) -> list[Evento]:
        eventi: list[Evento] = []
        for e in self.__lista_eventi:
            if e.get_id_spettacolo() == id_:
                eventi.append(e)
        return copy.deepcopy(eventi)

    # State
    def attivo(self, id_: int) -> bool:
        """Throws: IdInesistenteException"""
        e = self.get_evento(id_)
        if e is None:
            raise IdInesistenteException(f"Non è presente nessun evento con id {id_}.")

        return e.attivo()

    # Modificatori
    def aggiungi_evento(self, evento: Evento):
        """Throws: IdOccupatoException"""
        if self.ha_evento(evento.get_id()):
            raise IdOccupatoException(
                f"E' già presente un evento con id {evento.get_id()}."
            )

        self.__lista_eventi.append(evento)

    def elimina_evento(self, id_: int):
        """Throws: IdInesistenteException"""
        for i, e in enumerate(self.__lista_eventi):
            if e.get_id() == id_:
                self.__lista_eventi.pop(i)
                return

        raise IdInesistenteException(f"Non è presente nessun evento con id {id_}.")

    def modifica_evento(self, evento_modificato: Evento):
        """Throws: IdInesistenteException"""
        for i, e in enumerate(self.__lista_eventi):
            if e.get_id() == evento_modificato.get_id():
                self.__lista_eventi[i] = evento_modificato
                return

        raise IdInesistenteException(
            f"Non è presente nessun evento con id {evento_modificato.get_id()}."
        )
