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

    # Getters
    def get_id(self) -> int:
        return self.__id

    def get_nome(self) -> str:
        return self.__nome

    def get_descrizione(self) -> str:
        return self.__descrizione

    # Setters
    @staticmethod
    def set_next_id(next_id: int) -> bool:
        if next_id < 0:
            return False

        Genere.__next_id = next_id
        return True

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
