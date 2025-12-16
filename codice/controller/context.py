from PyQt6.QtWidgets import QMainWindow, QWidget
from typing import Optional

from controller.navigation import NavigationController

from model.model import Model


class AppContext:
    def __init__(self, main_window: QMainWindow) -> None:
        # Crea un NavigationController ed un Model unici per tutta l'app
        self.nav = NavigationController(main_window)
        self.model = Model()

        # ------------------------- PAGINE DELL'APP -------------------------

        # Login
        from view.login.login_page import LoginPage

        self.login_page = LoginPage()

        from view.login.authentication_page import AuthenticationPage

        self.authentication_page = AuthenticationPage()

        # Info
        from view.info.info_section import InfoSectionView
        from view.info.visualizza_opera import VisualizzaOperaView

        self.info_section = InfoSectionView()
        self.visualizza_opera_view = VisualizzaOperaView()

        from view.info.modifica_opera import NuovaOperaView, ModificaOperaView

        self.nuova_opera_view = NuovaOperaView()
        self.modifica_opera_view = ModificaOperaView()

        from view.info.modifica_genere import NuovoGenereView, ModificaGenereView

        self.nuovo_genere_view = NuovoGenereView()
        self.modifica_genere_view = ModificaGenereView()

        # Account
        from view.account.account_section_test import AccountSectionView

        self.account_section = AccountSectionView()

        # ------------------------- CONTROLLERS DELLA VIEW -------------------------

        # Login
        from controller.login.login_controller import LoginController

        self.login_controller = LoginController(
            self.model, self.login_page, self.authentication_page
        )

        # Info
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

        # ------------------------- ASSEGNAMENTO DEI pyqtSignal -------------------------

        # LoginController
        self.login_controller.navigation_go_back.connect(  # type:ignore
            self.nav.go_back
        )
        self.login_controller.navigation_go_to.connect(  # type:ignore
            self.on_nav_request_go_to
        )

        # InfoController
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

        # CUOperaController
        self.cu_opera_controller.navigation_go_back.connect(  # type:ignore
            self.nav.go_back
        )
        self.cu_opera_controller.navigation_get_page.connect(  # type:ignore
            self.on_nav_request_get_page
        )

        # CUGenereController
        self.cu_genere_controller.navigation_go_back.connect(  # type:ignore
            self.nav.go_back
        )
        self.cu_genere_controller.navigation_get_page.connect(  # type:ignore
            self.on_nav_request_get_page
        )

    def on_nav_request_go_to(self, page_name: str, save_history: bool) -> None:
        self.nav.go_to(page_name, save_history)

    def on_nav_request_section_go_to(self, page_name: str) -> None:
        self.nav.section_go_to(page_name)

    def on_nav_request_get_page(
        self, page_name: str, container: dict[str, Optional[QWidget]]
    ) -> None:
        container["value"] = self.nav.get_page(page_name)
