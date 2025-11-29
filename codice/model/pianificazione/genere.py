from model.exceptions import DatoIncongruenteException


class Genere:
    __next_id = 0

    def __init__(
        self,
        nome: str,
        descrizione: str,
    ):
        """Throws: DatoIncongruenteException"""
        self.__id = Genere.__next_id
        Genere.__next_id += 1

        self.set_nome(nome)
        self.set_descrizione(descrizione)

    # Getters
    def get_id(self) -> int:
        return self.__id

    def get_nome(self) -> str:
        return self.__nome

    def get_descrizione(self) -> str:
        return self.__descrizione

    # Setters
    @staticmethod
    def set_next_id(next_id: int):
        """Throws: DatoIncongruenteException"""
        if next_id < 0:
            raise DatoIncongruenteException("Il next_id non può essere minore di 0.")

        Genere.__next_id = next_id

    def set_nome(self, nome: str):
        """Throws: DatoIncongruenteException"""
        nome_stripped = nome.strip()
        if nome_stripped == "":
            raise DatoIncongruenteException("Il nome non può essere vuoto.")

        self.__nome = nome_stripped

    def set_descrizione(self, descrizione: str):
        """Throws: DatoIncongruenteException"""
        descrizione_stripped = descrizione.strip()
        if descrizione_stripped == "":
            raise DatoIncongruenteException("La descrizione non può essere vuota.")

        self.__descrizione = descrizione_stripped
