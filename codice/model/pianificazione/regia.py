from spettacolo import Spettacolo
from exceptions import DatoIncongruenteException


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
        if regista == "":
            raise DatoIncongruenteException("Il regista non può essere vuoto.")

        self.__regista = regista

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
