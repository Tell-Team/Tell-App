from model.organizzazione.sezione import Sezione
from model.exceptions import IdOccupatoException, IdInesistenteException
from typing import Optional
import copy


class GestoreSezioni:
    def __init__(self):
        self.__lista_sezioni: list[Sezione] = []

    # Stato
    # def opera_in_uso(self, id_: int) -> bool:
    #     for s in self.__lista_spettacoli:
    #         if type(s) is Regia and s.get_id_opera() == id_:
    #             return True

    #     return False

    # def ha_spettacolo(self, id_: int) -> bool:
    #     for s in self.__lista_spettacoli:
    #         if s.get_id() == id_:
    #             return True

    #     return False

    # Getters
    def get_max_id(self) -> int:
        ids = map(lambda x: x.get_id(), self.__lista_sezioni)

        try:
            return max(ids)
        except ValueError:
            return -1

    def get_sezione(self, id_: int) -> Optional[Sezione]:
        for s in self.__lista_sezioni:
            if s.get_id() == id_:
                return copy.copy(s)

        return None

    def get_sezioni(self) -> list[Sezione]:
        return copy.deepcopy(self.__lista_sezioni)

    # Modificatori
    def aggiungi_sezione(self, sezione: Sezione):
        """Throws: IdOccupatoException"""
        for s in self.__lista_sezioni:
            if s.get_id() == sezione.get_id():
                raise IdOccupatoException(
                    f"E' già presente una sezione con id {s.get_id()}."
                )

        self.__lista_sezioni.append(sezione)

    # def elimina_spettacolo(self, id_: int):
    #     """Throws: IdInesistenteException"""
    #     for i, s in enumerate(self.__lista_spettacoli):
    #         if s.get_id() == id_:
    #             self.__lista_spettacoli.pop(i)
    #             return

    #     raise IdInesistenteException(f"Non è presente nessuno spettacolo con id {id_}.")

    def modifica_sezione(self, sezione_modificata: Sezione):
        """Throws: IdInesistenteException"""
        for i, s in enumerate(self.__lista_sezioni):
            if s.get_id() == sezione_modificata.get_id():
                self.__lista_sezioni[i] = sezione_modificata
                return

        raise IdInesistenteException(
            f"Non è presente nessuna sezione con id {sezione_modificata.get_id()}."
        )
