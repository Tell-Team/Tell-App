from controller.context import AppContext, NavigationController

from model.pianificazione.spettacolo import Spettacolo


class SpettacoliController:
    def __init__(self, app_context: AppContext):
        self.__model = app_context.model
        self.__nav = app_context.nav

    def get_nav(self) -> NavigationController:
        return self.__nav

    def get_spettacoli(self) -> list[Spettacolo]:
        return self.__model.get_spettacoli()
