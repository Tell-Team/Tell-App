from model.pianificazione.regia import Regia
from model.exceptions import IdOccupatoException, IdInesistenteException
from typing import Optional


class GestoreRegie:
    def __init__(self):
        self.__lista_regie: list[Regia] = []

    # Stato
    def ha_regia(self, id_: int) -> bool:
        for g in self.__lista_regie:
            if g.get_id() == id_:
                return True

        return False

    # Getters
    def get_max_id(self) -> int:
        ids = map(lambda x: x.get_id(), self.__lista_regie)

        try:
            return max(ids)
        except ValueError:
            return -1

    def get_regia(self, id_: int) -> Optional[Regia]:
        for g in self.__lista_regie:
            if g.get_id() == id_:
                return g

        return None

    def get_regie(self) -> list[Regia]:
        return self.__lista_regie

    # Modificatori
    def aggiungi_regia(self, regia: Regia):
        """Throws: IdOccupatoException"""
        for g in self.__lista_regie:
            if g.get_id() == regia.get_id():
                raise IdOccupatoException(
                    f"E' già presente un regia con id {g.get_id()}."
                )

        self.__lista_regie.append(regia)

    def elimina_regia(self, id_: int):
        """Throws: IdInesistenteException"""
        for i, g in enumerate(self.__lista_regie):
            if g.get_id() == id_:
                self.__lista_regie.pop(i)
                return

        raise IdInesistenteException(f"Non è presente nessun regia con id {id_}.")

    def modifica_regia(self, regia_modificato: Regia):
        """Throws: IdInesistenteException"""
        for i, g in enumerate(self.__lista_regie):
            if g.get_id() == regia_modificato.get_id():
                self.__lista_regie[i] = regia_modificato
                return

        raise IdInesistenteException(
            f"Non è presente nessun regia con id {regia_modificato.get_id()}."
        )
