from model.pianificazione.genere import Genere


class GestoreGeneri:
    def __init__(self):
        self.__lista_generi: list[Genere] = []

    def ha_genere(self, id_: int) -> bool:
        for g in self.__lista_generi:
            if g.get_id() == id_:
                return True

        return False

    def aggiungi_genere(self, genere: Genere) -> bool:
        for g in self.__lista_generi:
            if g.get_id() == genere.get_id():
                return False

        self.__lista_generi.append(genere)
        return True

    def get_lista_generi(self) -> list[Genere]:
        return self.__lista_generi
