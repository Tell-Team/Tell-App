from model.exceptions import DatoIncongruenteException


class Prezzo:
    __next_id = 0

    def __init__(
        self,
        ammontare: float,
        id_spettacolo: int,
        id_sezione: int,
    ):
        """Throws: DatoIncongruenteException"""
        self.__id = Prezzo.__next_id
        Prezzo.__next_id += 1

        self.set_ammontare(ammontare)
        self.set_id_spettacolo(id_spettacolo)
        self.set_id_sezione(id_sezione)

    # Getters
    def get_id(self) -> int:
        return self.__id

    def get_ammontare(self) -> float:
        return self.__ammontare

    def get_id_spettacolo(self) -> int:
        return self.__id_spettacolo

    def get_id_sezione(self) -> int:
        return self.__id_sezione

    # Setters
    @staticmethod
    def set_next_id(next_id: int):
        """Throws: DatoIncongruenteException"""
        if next_id < 0:
            raise DatoIncongruenteException("Il next_id non può essere minore di 0.")

        Prezzo.__next_id = next_id

    def set_ammontare(self, ammontare: float):
        """Throws: DatoIncongruenteException"""
        if ammontare < 0:
            raise DatoIncongruenteException("L'ammontare non può essere minore di 0.")

        self.__ammontare = ammontare

    def set_id_spettacolo(self, id_spettacolo: int):
        """Throws: DatoIncongruenteException"""
        if id_spettacolo < 0:
            raise DatoIncongruenteException(
                "L'id spettacolo non può essere minore di 0."
            )

        self.__id_spettacolo = id_spettacolo

    def set_id_sezione(self, id_sezione: int):
        """Throws: DatoIncongruenteException"""
        if id_sezione < 0:
            raise DatoIncongruenteException("L'id sezione non può essere minore di 0.")

        self.__id_sezione = id_sezione

    # Magics
    def __eq__(self, other: object) -> bool:
        if (
            self.get_ammontare() == other.get_ammontare()  # type: ignore
            and self.get_id_spettacolo() == other.get_id_spettacolo()  # type: ignore
            and self.get_id_sezione() == other.get_id_sezione()  # type: ignore
        ):
            return True

        return False
