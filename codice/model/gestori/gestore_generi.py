from pianificazione.genere import Genere
from typing import Optional


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
                return g

        return None

    def get_lista_generi(self) -> list[Genere]:
        return self.__lista_generi

    # Validazione
    def __genere_valido(self, genere: Genere) -> bool:
        for g in self.__lista_generi:
            if g.get_id() == genere.get_id():
                return False

        return True

    # Modificatori
    def aggiungi_genere(self, genere: Genere) -> bool:
        if not self.__genere_valido(genere):
            return False

        self.__lista_generi.append(genere)
        return True

    def elimina_genere(self, id_: int) -> bool:
        for i, g in enumerate(self.__lista_generi):
            if g.get_id() == id_:
                self.__lista_generi.pop(i)
                return True

        return False

    def modifica_genere(self, genere_modificato: Genere) -> bool:
        for i, g in enumerate(self.__lista_generi):
            if g.get_id() == genere_modificato.get_id():
                if not self.__genere_valido(genere_modificato):
                    return False

                self.__lista_generi[i] = genere_modificato
                return True

        return False
