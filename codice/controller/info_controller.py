from model.model import Model
from model.pianificazione.opera import Opera
from model.pianificazione.genere import Genere


class InfoController:
    def __init__(self, model: Model):
        self.__model = model

    def get_lista_opere(self) -> list[Opera]:
        return self.__model.get_lista_opere()

    def get_lista_generi(self) -> list[Genere]:
        return self.__model.get_lista_generi()
