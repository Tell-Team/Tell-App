from model.pianificazione.spettacolo import Spettacolo
from model.exceptions import DatoIncongruenteException


class Regia(Spettacolo):
    def __init__(
        self,
        regista: str,
        anno_produzione: int,
        id_opera: int,
        titolo: str,
        note: str,
        interpreti: dict[str, str],
        tecnici: dict[str, str],
    ):
        """Throws: DatoIncongruenteException"""
        super().__init__(titolo, note, interpreti, tecnici)

        self.set_regista(regista)
        self.set_anno_produzione(anno_produzione)
        self.set_id_opera(id_opera)

    # Getters
    def get_regista(self) -> str:
        return self.__regista

    def get_anno_produzione(self) -> int:
        return self.__anno_produzione

    def get_id_opera(self) -> int:
        return self.__id_opera

    # Setters
    def set_regista(self, regista: str):
        """Throws: DatoIncongruenteException"""
        regista_stripped = regista.strip()
        if regista_stripped == "":
            raise DatoIncongruenteException("Il regista non può essere vuoto.")

        self.__regista = regista_stripped

    def set_anno_produzione(self, anno_produzione: int):
        """Throws: DatoIncongruenteException"""
        if anno_produzione < 0:
            raise DatoIncongruenteException(
                "L'anno di produzione non può essere minore di 0."
            )

        self.__anno_produzione = anno_produzione

    def set_id_opera(self, id_opera: int):
        """Throws: DatoIncongruenteException"""
        if id_opera < 0:
            raise DatoIncongruenteException("L'id opera non può essere minore di 0.")

        self.__id_opera = id_opera

    # Magics
    def __eq__(self, other: object) -> bool:
        if (
            self.get_regista() == other.get_regista()  # type: ignore
            and self.get_anno_produzione() == other.get_anno_produzione()  # type: ignore
            and self.get_id_opera() == other.get_id_opera()  # type: ignore
            and self.get_titolo() == other.get_titolo()  # type: ignore
            and self.get_note() == other.get_note()  # type: ignore
            and self.get_interpreti() == other.get_interpreti()  # type: ignore
            and self.get_tecnici() == other.get_tecnici()  # type: ignore
        ):
            return True

        return False
