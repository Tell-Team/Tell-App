from model.pianificazione.spettacolo import Spettacolo
from model.pianificazione.regia import Regia
from model.exceptions import IdOccupatoException, IdInesistenteException
from typing import Optional


class GestoreSpettacoli:
    def __init__(self):
        self.__lista_spettacoli: list[Spettacolo] = []

    # Stato
    def opera_in_uso(self, id_: int) -> bool:
        for s in self.__lista_spettacoli:
            if type(s) is Regia and s.get_id_opera() == id_:
                return True

        return False

    # Getters
    def get_max_id(self) -> int:
        ids = map(lambda x: x.get_id(), self.__lista_spettacoli)

        try:
            return max(ids)
        except ValueError:
            return -1

    def get_spettacolo(self, id_: int) -> Optional[Spettacolo]:
        for s in self.__lista_spettacoli:
            if s.get_id() == id_:
                return s

        return None

    def get_spettacoli(self) -> list[Spettacolo]:
        return self.__lista_spettacoli

    def get_spettacoli_by_titolo(self, titolo: str) -> list[Spettacolo]:
        return list(filter(lambda o: titolo in o.get_titolo(), self.__lista_spettacoli))

    def get_regie_by_opera(self, id_: int) -> list[Regia]:
        regie: list[Regia] = []
        for s in self.__lista_spettacoli:
            if type(s) is Regia and s.get_id_opera() == id_:
                regie.append(s)
        return regie

    # Modificatori
    def aggiungi_spettacolo(self, spettacolo: Spettacolo):
        """Throws: IdOccupatoException"""
        for s in self.__lista_spettacoli:
            if s.get_id() == spettacolo.get_id():
                raise IdOccupatoException(
                    f"E' già presente uno spettacolo con id {s.get_id()}."
                )

        self.__lista_spettacoli.append(spettacolo)

    def modifica_spettacolo(self, spettacolo_modificato: Spettacolo):
        """Throws: IdInesistenteException"""
        for i, s in enumerate(self.__lista_spettacoli):
            if s.get_id() == spettacolo_modificato.get_id():
                self.__lista_spettacoli[i] = spettacolo_modificato
                return

        raise IdInesistenteException(
            f"Non è presente nessuno spettacolo con id {spettacolo_modificato.get_id()}."
        )
