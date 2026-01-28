from model.exceptions import DatoIncongruenteException


class Occupazione:
    __next_id = 0

    def __init__(
        self,
        id_evento: int,
        id_posto: int,
        id_prenotazione: int,
    ):
        """Throws: DatoIncongruenteException"""
        self.__id = Occupazione.__next_id
        Occupazione.__next_id += 1

        self.set_id_evento(id_evento)
        self.set_id_posto(id_posto)
        self.set_id_prenotazione(id_prenotazione)

    # Getters
    def get_id(self) -> int:
        return self.__id

    def get_id_evento(self) -> int:
        return self.__id_evento

    def get_id_posto(self) -> int:
        return self.__id_posto

    def get_id_prenotazione(self) -> int:
        return self.__id_prenotazione

    # Setters
    @staticmethod
    def set_next_id(next_id: int):
        """Throws: DatoIncongruenteException"""
        if next_id < 0:
            raise DatoIncongruenteException("Il next_id non può essere minore di 0.")

        Occupazione.__next_id = next_id

    def set_id_evento(self, id_evento: int):
        """Throws: DatoIncongruenteException"""
        if id_evento < 0:
            raise DatoIncongruenteException("L'id evento non può essere minore di 0.")

        self.__id_evento = id_evento

    def set_id_posto(self, id_posto: int):
        """Throws: DatoIncongruenteException"""
        if id_posto < 0:
            raise DatoIncongruenteException("L'id posto non può essere minore di 0.")

        self.__id_posto = id_posto

    def set_id_prenotazione(self, id_prenotazione: int):
        """Throws: DatoIncongruenteException"""
        if id_prenotazione < 0:
            raise DatoIncongruenteException(
                "L'id prenotazione non può essere minore di 0."
            )

        self.__id_prenotazione = id_prenotazione

    # Magics
    def __eq__(self, other: object) -> bool:
        if (
            self.get_id_evento() == other.get_id_evento()  # type: ignore
            and self.get_id_posto() == other.get_id_posto()  # type: ignore
            and self.get_id_prenotazione() == other.get_id_prenotazione()  # type: ignore
        ):
            return True

        return False
