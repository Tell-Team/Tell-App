from controller.login import LoginController
from controller.login.user_session import UserSession
from controller.navigation import NavigationController

from model.model.model import Model

from view.main_window import MainWindow


class AppFlowController:
    """Controller che gestisce il flusso di eventi dell'app. Mostra il `LoginDialog` ed inizia
    la `MainWindow` ed il `NavigationController` dopo un login riuscito. Dopo il logout, queste
    due istanze vengono eliminate e il dialog viene nuovamente visualizzato.
    """

    def __init__(
        self,
        model: Model,
        login_controller: LoginController,
    ):
        self.__model = model
        self.__login_controller = login_controller

        self.__show_login_dialog()

    def __show_login_dialog(self) -> None:
        dialog = self.__login_controller.get_dialog()
        self.__login_dialog = dialog

        self.__login_controller.loginSucceeded.connect(  # type:ignore
            self.__start_session
        )

        dialog.show()

    def __start_session(self, user_session: UserSession) -> None:
        """Effettua un login dopo aver ricevuto credenziali valide."""
        self.__user_session = user_session

        self.__main_window = MainWindow()

        self.__navigation = NavigationController(
            self.__model, self.__main_window, self.__user_session
        )

        self.__navigation.logoutRequest.connect(  # type:ignore
            self.__end_session
        )

        self.__login_dialog.hide()
        self.__main_window.show()

    def __end_session(self) -> None:
        if self.__main_window:
            self.__main_window.close()
            self.__main_window = None
            self.__navigation = None
        self.__user_session = None
        self.__login_dialog.show()
