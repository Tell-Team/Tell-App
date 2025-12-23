from model.exceptions import DatoIncongruenteException
from datetime import date


class Opera:
    __next_id = 0

    def __init__(
        self,
        nome: str,
        compositore: str,
        librettista: str,
        numero_atti: int,
        data_prima_rappresentazione: date,
        teatro_prima_rappresentazione: str,
        trama: str,
        id_genere: int,
    ):
        """Throws: DatoIncongruenteException"""
        self.__id = Opera.__next_id
        Opera.__next_id += 1

        self.set_nome(nome)
        self.set_compositore(compositore)
        self.set_librettista(librettista)
        self.set_numero_atti(numero_atti)
        self.set_data_prima_rappresentazione(data_prima_rappresentazione)
        self.set_teatro_prima_rappresentazione(teatro_prima_rappresentazione)
        self.set_trama(trama)
        self.set_id_genere(id_genere)

    # Getters
    def get_id(self) -> int:
        return self.__id

    def get_nome(self) -> str:
        return self.__nome

    def get_compositore(self) -> str:
        return self.__compositore

    def get_librettista(self) -> str:
        return self.__librettista

    def get_numero_atti(self) -> int:
        return self.__numero_atti

    def get_data_prima_rappresentazione(self) -> date:
        return self.__data_prima_rappresentazione

    def get_teatro_prima_rappresentazione(self) -> str:
        return self.__teatro_prima_rappresentazione

    def get_trama(self) -> str:
        return self.__trama

    def get_id_genere(self) -> int:
        return self.__id_genere

    # Setters
    @staticmethod
    def set_next_id(next_id: int):
        """Throws: DatoIncongruenteException"""
        if next_id < 0:
            raise DatoIncongruenteException("Il next_id non può essere minore di 0.")

        Opera.__next_id = next_id
        return True

    def set_nome(self, nome: str):
        """Throws: DatoIncongruenteException"""
        nome_stripped = nome.strip()
        if nome_stripped == "":
            raise DatoIncongruenteException("Il nome non può essere vuoto.")

        self.__nome = nome_stripped
        return True

    def set_compositore(self, compositore: str):
        """Throws: DatoIncongruenteException"""
        compositore_stripped = compositore.strip()
        if compositore_stripped == "":
            raise DatoIncongruenteException("Il compositore non può essere vuoto.")

        self.__compositore = compositore_stripped
        return True

    def set_librettista(self, librettista: str):
        """Throws: DatoIncongruenteException"""
        librettista_stripped = librettista.strip()
        if librettista_stripped == "":
            raise DatoIncongruenteException("Il librettista non può essere vuoto.")

        self.__librettista = librettista_stripped
        return True

    def set_numero_atti(self, numero_atti: int):
        """Throws: DatoIncongruenteException"""
        if numero_atti <= 0:
            raise DatoIncongruenteException(
                "Il numero atti non può essere minore di 1."
            )

        self.__numero_atti = numero_atti
        return True

    def set_data_prima_rappresentazione(self, data_prima_rappresentazione: date):
        self.__data_prima_rappresentazione = data_prima_rappresentazione

    def set_teatro_prima_rappresentazione(self, teatro_prima_rappresentazione: str):
        """Throws: DatoIncongruenteException"""
        teatro_prima_rappresentazione_stripped = teatro_prima_rappresentazione.strip()
        if teatro_prima_rappresentazione_stripped == "":
            raise DatoIncongruenteException(
                "Il teatro prima rappresentazione non può essere vuoto."
            )

        self.__teatro_prima_rappresentazione = teatro_prima_rappresentazione_stripped
        return True

    def set_trama(self, trama: str):
        """Throws: DatoIncongruenteException"""
        trama_stripped = trama.strip()
        if trama_stripped == "":
            raise DatoIncongruenteException("La trama non può essere vuota.")

        self.__trama = trama_stripped
        return True

    def set_id_genere(self, id_genere: int):
        """Throws: DatoIncongruenteException"""
        if id_genere < 0:
            raise DatoIncongruenteException("L'id genere non può essere minore di 0.")

        self.__id_genere = id_genere

    # Magics
    def __eq__(self, other: object) -> bool:
        if (
            self.get_nome() == other.get_nome()  # type: ignore
            and self.get_compositore() == other.get_compositore()  # type: ignore
            and self.get_librettista() == other.get_librettista()  # type: ignore
            and self.get_numero_atti() == other.get_numero_atti()  # type: ignore
            and self.get_data_prima_rappresentazione() == other.get_data_prima_rappresentazione()  # type: ignore
            and self.get_teatro_prima_rappresentazione() == other.get_teatro_prima_rappresentazione()  # type: ignore
            and self.get_trama() == other.get_trama()  # type: ignore
            and self.get_id_genere() == other.get_id_genere()  # type: ignore
        ):
            return True

        return False
