from model.pianificazione.genere import Genere
from model.exceptions import IdOccupatoException, IdInesistenteException
from typing import Optional
import copy


class GestoreGeneri:
    def __init__(self):
        self.__lista_generi: list[Genere] = []

    # Stato
    def ha_genere(self, id_: int) -> bool:
        for g in self.__lista_generi:
            if g.get_id() == id_:
                return True

        return False

    # Getters
    def get_max_id(self) -> int:
        ids = map(lambda x: x.get_id(), self.__lista_generi)

        try:
            return max(ids)
        except ValueError:
            return -1

    def get_genere(self, id_: int) -> Optional[Genere]:
        for g in self.__lista_generi:
            if g.get_id() == id_:
                return copy.copy(g)

        return None

    def get_generi(self) -> list[Genere]:
        return copy.deepcopy(self.__lista_generi)

    # Modificatori
    def aggiungi_genere(self, genere: Genere):
        """Throws: IdOccupatoException"""
        for g in self.__lista_generi:
            if g.get_id() == genere.get_id():
                raise IdOccupatoException(
                    f"E' già presente un genere con id {g.get_id()}."
                )

        self.__lista_generi.append(genere)

    def elimina_genere(self, id_: int):
        """Throws: IdInesistenteException"""
        for i, g in enumerate(self.__lista_generi):
            if g.get_id() == id_:
                self.__lista_generi.pop(i)
                return

        raise IdInesistenteException(f"Non è presente nessun genere con id {id_}.")

    def modifica_genere(self, genere_modificato: Genere):
        """Throws: IdInesistenteException"""
        for i, g in enumerate(self.__lista_generi):
            if g.get_id() == genere_modificato.get_id():
                self.__lista_generi[i] = genere_modificato
                return

        raise IdInesistenteException(
            f"Non è presente nessun genere con id {genere_modificato.get_id()}."
        )
