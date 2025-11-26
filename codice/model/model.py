from gestori.gestore_generi import GestoreGeneri
from gestori.gestore_opere import GestoreOpere
from pianificazione.genere import Genere
from pianificazione.opera import Opera
from pickle import load, dump


class Model:
    def __init__(self):
        try:
            self.carica_tutto()

            # Rimessa in pari degli ID
            Genere.set_next_id(self.__gestore_generi.get_max_id() + 1)
            Opera.set_next_id(self.__gestore_opere.get_max_id() + 1)

        except FileNotFoundError:
            self.__gestore_generi = GestoreGeneri()
            self.__gestore_opere = GestoreOpere()

    # Caricamenti
    def carica_tutto(self):
        self.carica_generi()
        self.carica_opere()

    def carica_generi(self):
        with open("db/generi.pkl", "rb") as f:
            self.__gestore_generi: GestoreGeneri = load(f)

    def carica_opere(self):
        with open("db/opere.pkl", "rb") as f:
            self.__gestore_opere: GestoreOpere = load(f)

    # Salvataggi
    def salva_tutto(self):
        self.salva_generi()
        self.salva_opere()

    def salva_generi(self):
        with open("db/generi.pkl", "wb") as f:
            dump(self.__gestore_generi, f)

    def salva_opere(self):
        with open("db/opere.pkl", "wb") as f:
            dump(self.__gestore_opere, f)

    # Getters
    def get_lista_generi(self) -> list[Genere]:
        return self.__gestore_generi.get_lista_generi()

    def get_lista_opere(self) -> list[Opera]:
        return self.__gestore_opere.get_lista_opere()

    # Validazione
    def __genere_valido(self, genere: Genere) -> bool:
        return True

    def __opera_valida(self, opera: Opera) -> bool:
        if not self.__gestore_generi.ha_genere(opera.get_id_genere()):
            return False

        return True

    # Modificatori
    def aggiungi_genere(self, genere: Genere) -> bool:
        if not self.__genere_valido(genere):
            return False

        return self.__gestore_generi.aggiungi_genere(genere)

    def elimina_genere(self, id_: int) -> bool:
        if self.__gestore_opere.genere_in_uso(id_):
            return False

        return self.__gestore_generi.elimina_genere(id_)

    def modifica_genere(self, genere_modificato: Genere) -> bool:
        if not self.__genere_valido(genere_modificato):
            return False

        return self.__gestore_generi.modifica_genere(genere_modificato)

    def aggiungi_opera(self, opera: Opera) -> bool:
        if not self.__opera_valida(opera):
            return False

        return self.__gestore_opere.aggiungi_opera(opera)

    def modifica_opera(self, opera_modificata: Opera) -> bool:
        if not self.__opera_valida(opera_modificata):
            return False

        return self.__gestore_opere.modifica_opera(opera_modificata)
