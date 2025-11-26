from model.model import Model
from model.pianificazione.opera import Opera
from model.pianificazione.genere import Genere

from controller.navigation import NavigationController


class InfoController:
    def __init__(self, model: Model, nav: NavigationController):
        self.__model = model
        self.__nav = nav

    def get_nav(self) -> NavigationController:
        return self.__nav

    def get_lista_opere(self) -> list[Opera]:
        return self.__model.get_lista_opere()

    def get_lista_generi(self) -> list[Genere]:
        return self.__model.get_lista_generi()
