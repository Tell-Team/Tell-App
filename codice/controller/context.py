from PyQt6.QtWidgets import QMainWindow, QWidget

from controller.navigation import NavigationController

from model.model import Model


class AppContext:
    def __init__(self, main_window: QMainWindow):
        # Crea un Navigation e un Model unici per tutta l'app
        self.nav = NavigationController(main_window)
        self.model = Model()

        #
        #
        #

        # Pagine Login
        from view.login.login_page import LoginPage

        self.login_page = LoginPage()

        from view.login.authentication_page import AuthenticationPage

        self.authentication_page = AuthenticationPage()

        # Pagine Info
        from view.info.info_section import InfoSectionView
        from view.info.visualizza_opera import OperaView

        self.info_section = InfoSectionView()
        self.visualizza_opera_view = OperaView()

        from view.info.modifica_opera import NuovaOperaView, ModificaOperaView

        self.nuova_opera_view = NuovaOperaView()
        self.modifica_opera_view = ModificaOperaView()

        from view.info.modifica_genere import NuovoGenereView, ModificaGenereView

        self.nuovo_genere_view = NuovoGenereView()
        self.modifica_genere_view = ModificaGenereView()

        # Pagine Account
        from view.account.account_section_rod import AccountSectionView

        self.account_section = AccountSectionView()

        #
        #
        #

        # Controller Login
        from controller.login.login_controller import LoginController

        self.login_controller = LoginController(
            self.model, self.login_page, self.authentication_page
        )

        # Controller Info
        from controller.info.info_controller import InfoController

        self.info_controller = InfoController(
            self.model,
            self.info_section,
            self.visualizza_opera_view,
        )

        from controller.info.CU_opera_controller import CUOperaController

        self.cu_opera_controller = CUOperaController(
            self.model, self.nuova_opera_view, self.modifica_opera_view
        )

        from controller.info.CU_genere_controller import CUGenereController

        self.cu_genere_controller = CUGenereController(
            self.model, self.nuovo_genere_view, self.modifica_genere_view
        )

        #
        #
        #

        # Assegnamento dei pyqtSignal() nei Controller
        self.login_controller.navigation_go_back.connect(  # type:ignore
            self.nav.go_back
        )

        self.login_controller.navigation_go_to.connect(  # type:ignore
            self.on_nav_request_go_to
        )

        self.info_controller.navigation_go_back.connect(  # type:ignore
            self.nav.go_back
        )

        self.info_controller.navigation_go_to.connect(  # type:ignore
            self.on_nav_request_go_to
        )

        self.info_controller.navigation_section_go_to.connect(  # type:ignore
            self.on_nav_request_section_go_to
        )

        self.info_controller.navigation_get_page.connect(  # type:ignore
            self.on_nav_request_get_page
        )

        self.cu_opera_controller.navigation_go_back.connect(  # type:ignore
            self.nav.go_back
        )

        self.cu_opera_controller.navigation_get_page.connect(  # type:ignore
            self.on_nav_request_get_page
        )

        self.cu_genere_controller.navigation_go_back.connect(  # type:ignore
            self.nav.go_back
        )

        self.cu_genere_controller.navigation_get_page.connect(  # type:ignore
            self.on_nav_request_get_page
        )

    def on_nav_request_go_to(self, page_name: str, save_history: bool):
        self.nav.go_to(page_name, save_history)

    def on_nav_request_section_go_to(self, page_name: str):
        self.nav.section_go_to(page_name)

    def on_nav_request_get_page(
        self, page_name: str, container: dict[str, QWidget | None]
    ):
        container["value"] = self.nav.get_page(page_name)
