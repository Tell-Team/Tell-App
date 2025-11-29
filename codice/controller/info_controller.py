from controller.context import AppContext, NavigationController

from model.pianificazione.opera import Opera
from model.pianificazione.genere import Genere
from model.pianificazione.regia import Regia  ### TESTING ###


class InfoController:
    def __init__(self, app_context: AppContext):
        self.__model = app_context.model
        self.__nav = app_context.nav

    def get_nav(self) -> NavigationController:
        return self.__nav

    def get_opere(self) -> list[Opera]:
        return self.__model.get_opere()

    def get_generi(self) -> list[Genere]:
        return self.__model.get_generi()

    ### TESTING ###
    def get_regie_by_opera(self, id_: int) -> list[Regia]:
        return self.__model.get_regie_by_opera(id_)
