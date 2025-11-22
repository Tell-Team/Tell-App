from model.pianificazione.opera import Opera
from model.gestori.gestore_generi import GestoreGeneri


class GestoreOpere:
    def __init__(self, gestore_generi: GestoreGeneri):
        self.__gestore_generi = gestore_generi

        self.__lista_opere: list[Opera] = []

    def aggiungi_opera(self, opera: Opera) -> bool:
        for o in self.__lista_opere:
            if o.get_id() == opera.get_id():
                return False

        if not self.__gestore_generi.ha_genere(opera.get_id_genere()):
            return False

        self.__lista_opere.append(opera)
        return True

    def get_lista_opere(self) -> list[Opera]:
        return self.__lista_opere
