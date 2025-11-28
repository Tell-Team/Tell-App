from exceptions import DatoIncongruenteException


class Spettacolo:
    __next_id = 0

    def __init__(
        self,
        titolo: str,
        note: str,
        interpreti: dict[str, str],
        tecnici: dict[str, str],
    ):
        """Throws: DatoIncongruenteException"""
        self.__id = Spettacolo.__next_id
        Spettacolo.__next_id += 1

        self.set_titolo(titolo)
        self.set_note(note)
        self.set_interpreti(interpreti)
        self.set_tecnici(tecnici)

    # Getters
    def get_id(self) -> int:
        return self.__id

    def get_titolo(self) -> str:
        return self.__titolo

    def get_note(self) -> str:
        return self.__note

    def get_interpreti(self) -> dict[str, str]:
        return self.__interpreti

    def get_tecnici(self) -> dict[str, str]:
        return self.__tecnici

    # Setters
    @staticmethod
    def set_next_id(next_id: int):
        """Throws: DatoIncongruenteException"""
        if next_id < 0:
            raise DatoIncongruenteException("Il next_id non può essere minore di 0.")

        Spettacolo.__next_id = next_id

    def set_titolo(self, titolo: str):
        """Throws: DatoIncongruenteException"""
        if titolo == "":
            raise DatoIncongruenteException("Il titolo non può essere vuoto.")

        self.__titolo = titolo

    def set_note(self, note: str):
        """Throws: DatoIncongruenteException"""
        if note == "":
            raise DatoIncongruenteException("Le note non possono essere vuote.")

        self.__note = note

    def set_interpreti(self, interpreti: dict[str, str]):
        """Throws: DatoIncongruenteException"""
        if "" in interpreti.keys():
            raise DatoIncongruenteException(
                "Il ruolo dell'interprete non può essere vuoto."
            )
        if "" in interpreti.values():
            raise DatoIncongruenteException(
                "Il nome dell'interprete non può essere vuoto."
            )

        self.__interpreti = interpreti

    def set_tecnici(self, tecnici: dict[str, str]):
        """Throws: DatoIncongruenteException"""
        if "" in tecnici.keys():
            raise DatoIncongruenteException(
                "Il ruolo del tecnico non può essere vuoto."
            )
        if "" in tecnici.values():
            raise DatoIncongruenteException("Il nome del tecnico non può essere vuoto.")

        self.__tecnici = tecnici
