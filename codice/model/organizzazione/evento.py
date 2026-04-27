from model.exceptions import DatoIncongruenteException
from datetime import datetime


class Evento:
    __next_id = 0

    def __init__(
        self,
        data_ora: datetime,
        id_spettacolo: int,
    ):
        """Throws: DatoIncongruenteException"""
        self.__id = Evento.__next_id
        Evento.__next_id += 1

        self.set_data_ora(data_ora)
        self.set_id_spettacolo(id_spettacolo)

    # Getters
    def get_id(self) -> int:
        return self.__id

    def get_data_ora(self) -> datetime:
        return self.__data_ora

    def get_id_spettacolo(self) -> int:
        return self.__id_spettacolo

    # Stato
    def attivo(self) -> bool:
        return datetime.now() < self.get_data_ora()

    # Setters
    @staticmethod
    def set_next_id(next_id: int):
        """Throws: DatoIncongruenteException"""
        if next_id < 0:
            raise DatoIncongruenteException("Il next_id non può essere minore di 0.")

        Evento.__next_id = next_id

    def set_data_ora(self, data_ora: datetime):
        self.__data_ora = data_ora

    def set_id_spettacolo(self, id_spettacolo: int):
        """Throws: DatoIncongruenteException"""
        if id_spettacolo < 0:
            raise DatoIncongruenteException(
                "L'id spettacolo non può essere minore di 0."
            )

        self.__id_spettacolo = id_spettacolo

    # Magics
    def __eq__(self, other: object) -> bool:
        if (
            self.get_data_ora() == other.get_data_ora()  # type: ignore
            and self.get_id_spettacolo() == other.get_id_spettacolo()  # type: ignore
        ):
            return True

        return False
