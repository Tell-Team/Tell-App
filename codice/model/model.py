from model.gestori.gestore_generi import GestoreGeneri
from model.gestori.gestore_opere import GestoreOpere
from model.gestori.gestore_spettacoli import GestoreSpettacoli
from model.pianificazione.genere import Genere
from model.pianificazione.opera import Opera
from model.pianificazione.spettacolo import Spettacolo
from model.pianificazione.regia import Regia
from model.exceptions import (
    IdInesistenteException,
    OggettoInUsoException,
)
from pickle import load, dump
from typing import Optional


class Model:
    def __init__(self):
        try:
            self.__carica_generi()
            Genere.set_next_id(self.__gestore_generi.get_max_id() + 1)
        except FileNotFoundError:
            self.__gestore_generi = GestoreGeneri()

        try:
            self.__carica_opere()
            Opera.set_next_id(self.__gestore_opere.get_max_id() + 1)
        except FileNotFoundError:
            self.__gestore_opere = GestoreOpere()

        try:
            self.__carica_spettacoli()
            Spettacolo.set_next_id(self.__gestore_spettacoli.get_max_id() + 1)
        except FileNotFoundError:
            self.__gestore_spettacoli = GestoreSpettacoli()

    # Caricamenti
    def __carica_generi(self):
        with open("db/generi.pkl", "rb") as f:
            self.__gestore_generi: GestoreGeneri = load(f)

    def __carica_opere(self):
        with open("db/opere.pkl", "rb") as f:
            self.__gestore_opere: GestoreOpere = load(f)

    def __carica_spettacoli(self):
        with open("db/spettacoli.pkl", "rb") as f:
            self.__gestore_spettacoli: GestoreSpettacoli = load(f)

    # Salvataggi
    def __salva_generi(self):
        with open("db/generi.pkl", "wb") as f:
            dump(self.__gestore_generi, f)

    def __salva_opere(self):
        with open("db/opere.pkl", "wb") as f:
            dump(self.__gestore_opere, f)

    def __salva_spettacoli(self):
        with open("db/spettacoli.pkl", "wb") as f:
            dump(self.__gestore_spettacoli, f)

    # Getters
    def get_genere(self, id_: int) -> Optional[Genere]:
        return self.__gestore_generi.get_genere(id_)

    def get_generi(self) -> list[Genere]:
        return self.__gestore_generi.get_generi()

    def get_opera(self, id_: int) -> Optional[Opera]:
        return self.__gestore_opere.get_opera(id_)

    def get_opere(self) -> list[Opera]:
        return self.__gestore_opere.get_opere()

    def get_opere_by_nome(self, nome: str) -> list[Opera]:
        return self.__gestore_opere.get_opere_by_nome(nome)

    def get_spettacoli(self) -> list[Spettacolo]:
        return self.__gestore_spettacoli.get_spettacoli()

    def get_spettacoli_by_titolo(self, titolo: str) -> list[Spettacolo]:
        return self.__gestore_spettacoli.get_spettacoli_by_titolo(titolo)

    def get_regie_by_opera(self, id_: int) -> list[Regia]:
        return self.__gestore_spettacoli.get_regie_by_opera(id_)

    # Validazione
    def __valida_opera(self, opera: Opera):
        """Throws: IdInesistenteException"""
        if not self.__gestore_generi.ha_genere(opera.get_id_genere()):
            raise IdInesistenteException(
                f"Non è presente nessun genere con id {opera.get_id_genere()}."
            )

    def __valida_regia(self, regia: Regia):
        """Throws: IdInesistenteException"""
        if not self.__gestore_opere.ha_opera(regia.get_id_opera()):
            raise IdInesistenteException(
                f"Non è presente nessun'opera con id {regia.get_id_opera()}."
            )

    # Modificatori
    def aggiungi_genere(self, genere: Genere):
        """Throws: IdOccupatoException"""
        self.__gestore_generi.aggiungi_genere(genere)
        self.__salva_generi()

    def elimina_genere(self, id_: int):
        """Throws: OggettoInUsoException, IdInesistenteException"""
        if self.__gestore_opere.genere_in_uso(id_):
            raise OggettoInUsoException("Il genere è ancora legato ad una o più opere.")

        self.__gestore_generi.elimina_genere(id_)
        self.__salva_generi()

    def modifica_genere(self, id_: int, nuovi_dati: tuple[str, str]):
        """Throws: IdInesistenteException"""
        self.__gestore_generi.modifica_genere(id_, nuovi_dati)
        self.__salva_generi()

    def aggiungi_opera(self, opera: Opera):
        """Throws: IdInesistenteException, IdOccupatoException"""
        self.__valida_opera(opera)

        self.__gestore_opere.aggiungi_opera(opera)
        self.__salva_opere()

    def elimina_opera(self, id_: int):
        """Throws: OggettoInUsoException, IdInesistenteException"""
        if self.__gestore_spettacoli.opera_in_uso(id_):
            raise OggettoInUsoException(
                "L'opera è ancora è ancora legata ad una o più regie."
            )

        self.__gestore_opere.elimina_opera(id_)
        self.__salva_opere()

    def modifica_opera(self, opera_modificata: Opera):
        """Throws: IdInesistenteException"""
        self.__valida_opera(opera_modificata)

        self.__gestore_opere.modifica_opera(opera_modificata)
        self.__salva_opere()

    def aggiungi_spettacolo(self, spettacolo: Spettacolo):
        """Throws: IdInesistenteException, IdOccupatoException"""
        if type(spettacolo) is Regia:
            self.__valida_regia(spettacolo)

        self.__gestore_spettacoli.aggiungi_spettacolo(spettacolo)
        self.__salva_spettacoli()

    def modifica_spettacolo(self, spettacolo_modificato: Spettacolo):
        """Throws: IdInesistenteException"""
        if type(spettacolo_modificato) is Regia:
            self.__valida_regia(spettacolo_modificato)

        self.__gestore_spettacoli.modifica_spettacolo(spettacolo_modificato)
        self.__salva_spettacoli()
