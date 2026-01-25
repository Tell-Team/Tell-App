from model.organizzazione.prezzo import Prezzo
from model.exceptions import (
    IdOccupatoException,
    IdInesistenteException,
    OccupatoException,
)
from typing import Optional
import copy


class GestorePrezzi:
    def __init__(self):
        self.__lista_prezzi: list[Prezzo] = []

    # Getters
    def get_max_id(self) -> int:
        ids = map(lambda x: x.get_id(), self.__lista_prezzi)

        try:
            return max(ids)
        except ValueError:
            return -1

    def get_prezzo(self, id_: int) -> Optional[Prezzo]:
        for p in self.__lista_prezzi:
            if p.get_id() == id_:
                return copy.copy(p)

        return None

    def get_prezzo_by_spettacolo_e_sezione(
        self, id_spettacolo: int, id_sezione: int
    ) -> Optional[Prezzo]:
        for p in self.__lista_prezzi:
            if (
                p.get_id_spettacolo() == id_spettacolo
                and p.get_id_sezione() == id_sezione
            ):
                return copy.copy(p)

        return None

    def get_prezzi_by_spettacolo(self, id_spettacolo: int) -> list[Prezzo]:
        return copy.deepcopy(
            list(
                filter(
                    lambda p: p.get_id_spettacolo() == id_spettacolo,
                    self.__lista_prezzi,
                )
            )
        )

    # Validazione
    def __controllo_unique_key(self, primo: Prezzo, secondo: Prezzo):
        """Throws: OccupatoException"""
        if (
            primo.get_id_spettacolo() == secondo.get_id_spettacolo()
            and primo.get_id_sezione() == secondo.get_id_sezione()
        ):
            raise OccupatoException(
                f"E' già stato inserito il prezzo della sezione con id {secondo.get_id_sezione()} per lo spettacolo con id {secondo.get_id_spettacolo()}."
            )

    # Modificatori
    def aggiungi_prezzo(self, prezzo: Prezzo):
        """Throws: IdOccupatoException, OccupatoException"""
        for p in self.__lista_prezzi:
            if p.get_id() == prezzo.get_id():
                raise IdOccupatoException(
                    f"E' già presente un prezzo con id {prezzo.get_id()}."
                )

            self.__controllo_unique_key(p, prezzo)

        self.__lista_prezzi.append(copy.copy(prezzo))

    def elimina_prezzo(self, id_: int):
        """Throws: IdInesistenteException"""
        for i, p in enumerate(self.__lista_prezzi):
            if p.get_id() == id_:
                self.__lista_prezzi.pop(i)
                return

        raise IdInesistenteException(f"Non è presente nessun prezzo con id {id_}.")

    def elimina_prezzi_by_spettacolo(self, id_spettacolo: int):
        self.__lista_prezzi = list(
            filter(
                lambda p: p.get_id_spettacolo() != id_spettacolo, self.__lista_prezzi
            )
        )

    def elimina_prezzi_by_sezione(self, id_sezione: int):
        self.__lista_prezzi = list(
            filter(lambda p: p.get_id_sezione() != id_sezione, self.__lista_prezzi)
        )

    def modifica_prezzo(self, prezzo_modificato: Prezzo):
        """Throws: IdInesistenteException, OccupatoException"""
        posizione_da_modificare: Optional[int] = None

        for i, p in enumerate(self.__lista_prezzi):
            if p.get_id() != prezzo_modificato.get_id():
                self.__controllo_unique_key(p, prezzo_modificato)
            else:
                posizione_da_modificare = i

        if posizione_da_modificare is None:
            raise IdInesistenteException(
                f"Non è presente nessun prezzo con id {prezzo_modificato.get_id()}."
            )

        self.__lista_prezzi[posizione_da_modificare] = copy.copy(prezzo_modificato)
