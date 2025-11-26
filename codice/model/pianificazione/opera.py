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
        """Throws: ValueError"""
        self.__id = Opera.__next_id
        Opera.__next_id += 1

        if not self.set_nome(nome):
            raise ValueError
        if not self.set_compositore(compositore):
            raise ValueError
        if not self.set_librettista(librettista):
            raise ValueError
        if not self.set_numero_atti(numero_atti):
            raise ValueError
        self.set_data_prima_rappresentazione(data_prima_rappresentazione)
        if not self.set_teatro_prima_rappresentazione(teatro_prima_rappresentazione):
            raise ValueError
        if not self.set_trama(trama):
            raise ValueError
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
    def set_next_id(next_id: int) -> bool:
        if next_id < 0:
            return False

        Opera.__next_id = next_id
        return True

    def set_nome(self, nome: str) -> bool:
        if nome == "":
            return False

        self.__nome = nome
        return True

    def set_compositore(self, compositore: str) -> bool:
        if compositore == "":
            return False

        self.__compositore = compositore
        return True

    def set_librettista(self, librettista: str) -> bool:
        if librettista == "":
            return False

        self.__librettista = librettista
        return True

    def set_numero_atti(self, numero_atti: int) -> bool:
        if numero_atti <= 0:
            return False

        self.__numero_atti = numero_atti
        return True

    def set_data_prima_rappresentazione(self, data_prima_rappresentazione: date):
        self.__data_prima_rappresentazione = data_prima_rappresentazione

    def set_teatro_prima_rappresentazione(
        self, teatro_prima_rappresentazione: str
    ) -> bool:
        if teatro_prima_rappresentazione == "":
            return False

        self.__teatro_prima_rappresentazione = teatro_prima_rappresentazione
        return True

    def set_trama(self, trama: str) -> bool:
        if trama == "":
            return False

        self.__trama = trama
        return True

    def set_id_genere(self, id_genere: int):
        self.__id_genere = id_genere
