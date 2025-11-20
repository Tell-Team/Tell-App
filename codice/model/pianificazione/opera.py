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

    @property
    def id(self):
        return self.__id

    @property
    def nome(self):
        return self.__nome

    @property
    def compositore(self):
        return self.__compositore

    @property
    def librettista(self):
        return self.__librettista

    @property
    def numero_atti(self):
        return self.__numero_atti

    @property
    def data_prima_rappresentazione(self):
        return self.__data_prima_rappresentazione

    @property
    def teatro_prima_rappresentazione(self):
        return self.__teatro_prima_rappresentazione

    @property
    def trama(self):
        return self.__trama

    @property
    def id_genere(self):
        return self.__id_genere
