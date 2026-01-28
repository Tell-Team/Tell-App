from model.organizzazione.posto import Posto
from model.exceptions import (
    IdOccupatoException,
    IdInesistenteException,
    OccupatoException,
)
from typing import Optional
import copy


class GestorePosti:
    def __init__(self):
        self.__lista_posti: list[Posto] = []

    # Stato
    def ha_posto(self, id_: int) -> bool:
        for p in self.__lista_posti:
            if p.get_id() == id_:
                return True

        return False

    def sezione_in_uso(self, id_: int) -> bool:
        for p in self.__lista_posti:
            if p.get_id_sezione() == id_:
                return True

        return False

    # Getters
    def get_max_id(self) -> int:
        ids = map(lambda x: x.get_id(), self.__lista_posti)

        try:
            return max(ids)
        except ValueError:
            return -1

    def get_posto(self, id_: int) -> Optional[Posto]:
        for p in self.__lista_posti:
            if p.get_id() == id_:
                return copy.copy(p)

        return None

    def get_posti(self) -> list[Posto]:
        return copy.deepcopy(self.__lista_posti)

    def get_posti_by_sezione(self, id_: int) -> list[Posto]:
        posti: list[Posto] = []
        for p in self.__lista_posti:
            if p.get_id_sezione() == id_:
                posti.append(p)
        return copy.deepcopy(posti)

    # Validazione
    def __controllo_unique_key(self, primo: Posto, secondo: Posto):
        """Throws: OccupatoException"""
        if (
            primo.get_numero() == secondo.get_numero()
            and primo.get_id_sezione() == secondo.get_id_sezione()
        ):
            raise OccupatoException(
                f"E' già presente un posto di numero {secondo.get_numero()} nella sezione con id {secondo.get_id_sezione()}."
            )

    # Modificatori
    def aggiungi_posto(self, posto: Posto):
        """Throws: IdOccupatoException, OccupatoException"""
        for p in self.__lista_posti:
            if p.get_id() == posto.get_id():
                raise IdOccupatoException(
                    f"E' già presente un posto con id {posto.get_id()}."
                )

            self.__controllo_unique_key(p, posto)

        self.__lista_posti.append(copy.copy(posto))

    def elimina_posto(self, id_: int):
        """Throws: IdInesistenteException"""
        for i, p in enumerate(self.__lista_posti):
            if p.get_id() == id_:
                self.__lista_posti.pop(i)
                return

        raise IdInesistenteException(f"Non è presente nessun posto con id {id_}.")

    def modifica_posto(self, posto_modificato: Posto):
        """Throws: IdInesistenteException, OccupatoException"""
        posizione_da_modificare: Optional[int] = None

        for i, p in enumerate(self.__lista_posti):
            if p.get_id() != posto_modificato.get_id():
                self.__controllo_unique_key(p, posto_modificato)
            else:
                posizione_da_modificare = i

        if posizione_da_modificare is None:
            raise IdInesistenteException(
                f"Non è presente nessun posto con id {posto_modificato.get_id()}."
            )

        self.__lista_posti[posizione_da_modificare] = copy.copy(posto_modificato)
