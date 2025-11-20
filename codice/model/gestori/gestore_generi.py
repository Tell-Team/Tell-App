from pianificazione.genere import Genere


class GestoreGeneri:
    def __init__(self):
        self.__lista_generi: list[Genere] = []

    def ha_genere(self, id_: int) -> bool:
        for g in self.__lista_generi:
            if g.id == id_:
                return True

        return False

    def aggiungi_genere(self, genere: Genere) -> bool:
        for g in self.__lista_generi:
            if g.id == genere.id:
                return False

        self.__lista_generi.append(genere)
        return True
