class Genere:
    __next_id = 0

    def __init__(
        self,
        nome: str,
        descrizione: str,
    ):
        """Throws: ValueError"""
        self.__id = Genere.__next_id
        Genere.__next_id += 1

        if not self.set_nome(nome):
            raise ValueError
        if not self.set_descrizione(descrizione):
            raise ValueError

    def set_nome(self, nome: str) -> bool:
        if nome == "":
            return False

        self.__nome = nome
        return True

    def set_descrizione(self, descrizione: str) -> bool:
        if descrizione == "":
            return False

        self.__descrizione = descrizione
        return True

    @property
    def id(self):
        return self.__id

    @property
    def nome(self):
        return self.__nome

    @property
    def descrizione(self):
        return self.__descrizione
