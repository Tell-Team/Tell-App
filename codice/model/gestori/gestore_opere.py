from model.pianificazione.opera import Opera
from model.exceptions import IdOccupatoException, IdInesistenteException
from typing import Optional
import copy


class GestoreOpere:
    def __init__(self):
        self.__lista_opere: list[Opera] = []

    # Stato
    def genere_in_uso(self, id_: int) -> bool:
        for o in self.__lista_opere:
            if o.get_id_genere() == id_:
                return True

        return False

    def ha_opera(self, id_: int) -> bool:
        for o in self.__lista_opere:
            if o.get_id() == id_:
                return True

        return False

    # Getters
    def get_max_id(self) -> int:
        ids = map(lambda x: x.get_id(), self.__lista_opere)

        try:
            return max(ids)
        except ValueError:
            return -1

    def get_opera(self, id_: int) -> Optional[Opera]:
        for o in self.__lista_opere:
            if o.get_id() == id_:
                return copy.copy(o)

        return None

    def get_opere(self) -> list[Opera]:
        return copy.deepcopy(self.__lista_opere)

    def get_opere_by_nome(self, nome: str) -> list[Opera]:
        nome_lower = nome.lower()
        return copy.deepcopy(
            list(
                filter(lambda o: nome_lower in o.get_nome().lower(), self.__lista_opere)
            )
        )

    # Modificatori
    def aggiungi_opera(self, opera: Opera):
        """Throws: IdOccupatoException"""
        if self.ha_opera(opera.get_id()):
            raise IdOccupatoException(
                f"E' già presente un'opera con id {opera.get_id()}."
            )

        self.__lista_opere.append(copy.copy(opera))

    def elimina_opera(self, id_: int):
        """Throws: IdInesistenteException"""
        for i, o in enumerate(self.__lista_opere):
            if o.get_id() == id_:
                self.__lista_opere.pop(i)
                return

        raise IdInesistenteException(f"Non è presente nessuna opera con id {id_}.")

    def modifica_opera(self, opera_modificata: Opera):
        """Throws: IdInesistenteException"""
        for i, o in enumerate(self.__lista_opere):
            if o.get_id() == opera_modificata.get_id():
                self.__lista_opere[i] = copy.copy(opera_modificata)
                return

        raise IdInesistenteException(
            f"Non è presente nessuna opera con id {opera_modificata.get_id()}."
        )
