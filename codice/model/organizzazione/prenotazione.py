from model.exceptions import AzioneIncongruenteException, DatoIncongruenteException
from datetime import datetime


class Prenotazione:
    __next_id = 0

    def __init__(
        self,
        nominativo: str,
        data_ora_registrazione: datetime,
    ):
        """Throws: DatoIncongruenteException"""
        self.__id = Prenotazione.__next_id
        Prenotazione.__next_id += 1

        self.set_nominativo(nominativo)
        self.set_data_ora_registrazione(data_ora_registrazione)
        self.__pagata = False

    # Getters
    def get_id(self) -> int:
        return self.__id

    def get_nominativo(self) -> str:
        return self.__nominativo

    def get_data_ora_registrazione(self) -> datetime:
        return self.__data_ora_registrazione

    def pagata(self) -> bool:
        return self.__pagata

    # Setters
    @staticmethod
    def set_next_id(next_id: int):
        """Throws: DatoIncongruenteException"""
        if next_id < 0:
            raise DatoIncongruenteException("Il next_id non può essere minore di 0.")

        Prenotazione.__next_id = next_id

    def set_nominativo(self, nominativo: str):
        """Throws: DatoIncongruenteException"""
        nominativo_stripped = nominativo.strip()
        if nominativo_stripped == "":
            raise DatoIncongruenteException("Il nominativo non può essere vuoto.")

        self.__nominativo = nominativo_stripped

    def set_data_ora_registrazione(self, data_ora_registrazione: datetime):
        self.__data_ora_registrazione = data_ora_registrazione

    def segna_come_pagata(self):
        """Throws: AzioneIncongruenteException"""
        if self.__pagata:
            raise AzioneIncongruenteException(
                "La prenotazione è già segnata come pagata."
            )

        self.__pagata = True

    def segna_come_non_pagata(self):
        """Throws: AzioneIncongruenteException"""
        if not self.__pagata:
            raise AzioneIncongruenteException(
                "La prenotazione è già segnata come non pagata."
            )

        self.__pagata = False

    # Magics
    def __eq__(self, other: object) -> bool:
        if (
            self.get_nominativo() == other.get_nominativo()  # type: ignore
            and self.get_data_ora_registrazione() == other.get_data_ora_registrazione()  # type: ignore
            and self.pagata() == other.pagata()  # type: ignore
        ):
            return True

        return False
