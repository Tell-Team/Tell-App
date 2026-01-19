from model.exceptions import DatoIncongruenteException


class Posto:
    __next_id = 0

    def __init__(
        self,
        numero: int,
        id_sezione: int,
    ):
        """Throws: DatoIncongruenteException"""
        self.__id = Posto.__next_id
        Posto.__next_id += 1

        self.set_numero(numero)
        self.set_id_sezione(id_sezione)

    # Getters
    def get_id(self) -> int:
        return self.__id

    def get_numero(self) -> int:
        return self.__numero

    def get_id_sezione(self) -> int:
        return self.__id_sezione

    # Setters
    @staticmethod
    def set_next_id(next_id: int):
        """Throws: DatoIncongruenteException"""
        if next_id < 0:
            raise DatoIncongruenteException("Il next_id non può essere minore di 0.")

        Posto.__next_id = next_id

    def set_numero(self, numero: int):
        """Throws: DatoIncongruenteException"""
        if numero <= 0:
            raise DatoIncongruenteException("Il numero deve essere maggiore di 0.")

        self.__numero = numero

    def set_id_sezione(self, id_sezione: int):
        """Throws: DatoIncongruenteException"""
        if id_sezione < 0:
            raise DatoIncongruenteException("L'id sezione non può essere minore di 0.")

        self.__id_sezione = id_sezione

    # Magics
    def __eq__(self, other: object) -> bool:
        if (
            self.get_numero() == other.get_numero()  # type: ignore
            and self.get_id_sezione() == other.get_id_sezione()  # type: ignore
        ):
            return True

        return False
