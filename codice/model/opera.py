from datetime import date


class Opera:
    __next_id = 0

    def __init__(
        self,
        nome: str,
        compositore: str,
        librettista: str,
        numero_atti: int,
        prima_rappresentazione: date,
        trama: str,
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
        self.set_prima_rappresentazione(prima_rappresentazione)
        if not self.set_trama(trama):
            raise ValueError

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

    def set_prima_rappresentazione(self, prima_rappresentazione: date):
        self.__prima_rappresentazione = prima_rappresentazione

    def set_trama(self, trama: str) -> bool:
        if trama == "":
            return False

        self.__trama = trama
        return True
