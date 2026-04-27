from model.exceptions import DatoIncongruenteException
import copy


class Spettacolo:
    __next_id = 0

    def __init__(
        self,
        titolo: str,
        note: str,
        interpreti: dict[str, str],
        musicisti_e_direttori_artistici: dict[str, str],
    ):
        """Throws: DatoIncongruenteException"""
        self.__id = Spettacolo.__next_id
        Spettacolo.__next_id += 1

        self.set_titolo(titolo)
        self.set_note(note)
        self.set_interpreti(interpreti)
        self.set_musicisti_e_direttori_artistici(musicisti_e_direttori_artistici)

    # Getters
    def get_id(self) -> int:
        return self.__id

    def get_titolo(self) -> str:
        return self.__titolo

    def get_note(self) -> str:
        return self.__note

    def get_interpreti(self) -> dict[str, str]:
        return copy.copy(self.__interpreti)

    def get_musicisti_e_direttori_artistici(self) -> dict[str, str]:
        return copy.copy(self.__musicisti_e_direttori_artistici)

    # Setters
    @staticmethod
    def set_next_id(next_id: int):
        """Throws: DatoIncongruenteException"""
        if next_id < 0:
            raise DatoIncongruenteException("Il next_id non può essere minore di 0.")

        Spettacolo.__next_id = next_id

    def set_titolo(self, titolo: str):
        """Throws: DatoIncongruenteException"""
        titolo_stripped = titolo.strip()
        if titolo_stripped == "":
            raise DatoIncongruenteException("Il titolo non può essere vuoto.")

        self.__titolo = titolo_stripped

    def set_note(self, note: str):
        self.__note = note

    def set_interpreti(self, interpreti: dict[str, str]):
        """Throws: DatoIncongruenteException"""
        interpreti_stripped = dict(
            zip(
                map(lambda i: i.strip(), interpreti.keys()),
                map(lambda i: i.strip(), interpreti.values()),
            )
        )

        if "" in interpreti_stripped.keys():
            raise DatoIncongruenteException(
                "Il ruolo dell'interprete non può essere vuoto."
            )
        if "" in interpreti_stripped.values():
            raise DatoIncongruenteException(
                "Il nome dell'interprete non può essere vuoto."
            )

        self.__interpreti = interpreti_stripped

    def set_musicisti_e_direttori_artistici(
        self, musicisti_e_direttori_artistici: dict[str, str]
    ):
        """Throws: DatoIncongruenteException"""
        musicisti_e_direttori_artistici_stripped = dict(
            zip(
                map(lambda i: i.strip(), musicisti_e_direttori_artistici.keys()),
                map(lambda i: i.strip(), musicisti_e_direttori_artistici.values()),
            )
        )

        if "" in musicisti_e_direttori_artistici_stripped.keys():
            raise DatoIncongruenteException(
                "Il ruolo del tecnico non può essere vuoto."
            )
        if "" in musicisti_e_direttori_artistici_stripped.values():
            raise DatoIncongruenteException("Il nome del tecnico non può essere vuoto.")

        self.__musicisti_e_direttori_artistici = (
            musicisti_e_direttori_artistici_stripped
        )

    # Magics
    def __eq__(self, other: object) -> bool:
        if (
            self.get_titolo() == other.get_titolo()  # type: ignore
            and self.get_note() == other.get_note()  # type: ignore
            and self.get_interpreti() == other.get_interpreti()  # type: ignore
            and self.get_musicisti_e_direttori_artistici() == other.get_musicisti_e_direttori_artistici()  # type: ignore
        ):
            return True

        return False
