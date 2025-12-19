from PyQt6.QtWidgets import QMainWindow, QWidget
from typing import Optional

from controller.navigation import NavigationController

from model.model import Model


class AppContext:
    def __init__(self, main_window: QMainWindow, db_path: Optional[str]) -> None:
        """Throws: DatoIncongruenteException"""

        # Crea un NavigationController ed un Model unici per tutta l'app
        self.nav = NavigationController(main_window)
        self.model = Model(db_path)

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

        # MessageView
        from view.messageView import MessageView

        self.message_view = MessageView()

        # ------------------------- CONTROLLERS DELLA VIEW -------------------------

        # Login
        from controller.login.login_controller import LoginController

        self.login_controller = LoginController(
            self.model, self.login_page, self.authentication_page
        )

        # Info
        from controller.info.info_controller import InfoController

        self.info_controller = InfoController(
            self.model, self.info_section, self.visualizza_opera_view, self.message_view
        )

        from controller.info.CU_opera_controller import CUOperaController

        self.cu_opera_controller = CUOperaController(
            self.model,
            self.nuova_opera_view,
            self.modifica_opera_view,
            self.message_view,
        )

        from controller.info.CU_genere_controller import CUGenereController

        self.cu_genere_controller = CUGenereController(
            self.model,
            self.nuovo_genere_view,
            self.modifica_genere_view,
            self.message_view,
        )

        # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

        # LoginController
        self.login_controller.goBackRequest.connect(  # type:ignore
            self._on_request_go_back
        )
        self.login_controller.goToPageRequest.connect(  # type:ignore
            self._on_request_go_to
        )

        # InfoController
        self.info_controller.goBackRequest.connect(  # type:ignore
            self._on_request_go_back
        )
        self.info_controller.goToPageRequest.connect(  # type:ignore
            self._on_request_go_to
        )
        self.info_controller.goToSectionRequest.connect(  # type:ignore
            self._on_request_section_go_to
        )
        self.info_controller.getNavPageRequest.connect(  # type:ignore
            self._on_request_get_page
        )

        # CUOperaController
        self.cu_opera_controller.goBackRequest.connect(  # type:ignore
            self._on_request_go_back
        )
        self.cu_opera_controller.getNavPageRequest.connect(  # type:ignore
            self._on_request_get_page
        )

        # CUGenereController
        self.cu_genere_controller.goBackRequest.connect(  # type:ignore
            self._on_request_go_back
        )
        self.cu_genere_controller.getNavPageRequest.connect(  # type:ignore
            self._on_request_get_page
        )

    # ------------------------- METODI DI NAVIGAZIONE -------------------------

    def _on_request_go_back(self) -> None:
        self.nav.go_back()

    def _on_request_go_to(self, page_name: str, save_history: bool) -> None:
        try:
            self.nav.go_to(page_name, save_history)
        except KeyError as exc:
            self.message_view.mostra_errore(
                self.nav.get_cur_central_page(),
                # E' sempre chiamato con un centralWidget definito. Quindi, in teoria,
                # get_cur_central_page non lancia mai un RuntimeError.
                "Pagina non trovata",
                f"Si è verificato un errore: {exc}",
            )

    def _on_request_section_go_to(self, page_name: str) -> None:
        try:
            self.nav.section_go_to(page_name)
        except KeyError as exc:
            self.message_view.mostra_errore(
                self.nav.get_cur_central_page(),
                # E' sempre chiamato con un centralWidget definito. Quindi, in teoria,
                # get_cur_central_page non lancia mai un RuntimeError.
                "Pagina non trovata",
                f"Si è verificato un errore: {exc}",
            )

    def _on_request_get_page(
        self, page_name: str, container: dict[str, Optional[QWidget]]
    ) -> None:
        container["value"] = self.nav.get_page(page_name)
