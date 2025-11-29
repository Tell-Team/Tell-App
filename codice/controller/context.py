from PyQt6.QtWidgets import QMainWindow

from controller.navigation import NavigationController
from model.model import Model


class AppContext:
    def __init__(self, main_window: QMainWindow):
        # # Crea un Navigation e un Model unici per tutta l'app
        self.nav = NavigationController(main_window)
        self.model = Model()

        # # Crea i controller delle sezioni dell'app
        from controller.info_controller import InfoController

        self.info_controller = InfoController(self)
