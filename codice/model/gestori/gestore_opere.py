from pianificazione.opera import Opera
from typing import Optional


class GestoreOpere:
    def __init__(self):
        self.__lista_opere: list[Opera] = []

    # Stato
    def genere_in_uso(self, id_: int) -> bool:
        for o in self.__lista_opere:
            if o.get_id_genere() == id_:
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
                return o

        return None

    def get_lista_opere(self) -> list[Opera]:
        return self.__lista_opere

    # Modificatori
    def aggiungi_opera(self, opera: Opera) -> bool:
        for o in self.__lista_opere:
            if o.get_id() == opera.get_id():
                return False

        self.__lista_opere.append(opera)
        return True

    def modifica_opera(self, opera_modificata: Opera):
        for i, o in enumerate(self.__lista_opere):
            if o.get_id() == opera_modificata.get_id():
                self.__lista_opere.pop(i)
                if not self.aggiungi_opera(opera_modificata):
                    self.__lista_opere.append(o)
                    return False
                return True

        return False
