from pianificazione.opera import Opera
from gestori.gestore_generi import GestoreGeneri


class GestoreOpere:
    def __init__(self, gestore_generi: GestoreGeneri):
        self.__gestore_generi = gestore_generi

        self.__lista_opere: list[Opera] = []

    def aggiungi_opera(self, opera: Opera) -> bool:
        for o in self.__lista_opere:
            if o.id == opera.id:
                return False

        if not self.__gestore_generi.ha_genere(opera.id_genere):
            return False

        self.__lista_opere.append(opera)
        return True
