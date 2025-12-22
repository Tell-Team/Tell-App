from PyQt6.QtWidgets import QMainWindow, QWidget, QStackedWidget
from typing import Optional

from controller.navigation import NavigationController

from model.model import Model

from view.messageView import MessageView


class AppContext:
    """Classe dedicata a caricare tutto il contesto dell'app.
    - Crea le pagine della view;
    - Registra le pagine nel controller di navigazione `self.__nav`;
    - Crea i controller delle pagine della view;
    - Collega i segnali di navigazione con metodi collegati a `self.__nav`.

    :raise DatoIncongruenteException: il percorso specificato per il salvataggio
    dei dati dell'applicazione non è valido (non è una cartella).
    """

    def __init__(self, main_window: QMainWindow, db_path: Optional[str]) -> None:

        # Crea un NavigationController ed un Model unici per tutta l'app
        self.__nav = NavigationController(main_window)
        self.__model = Model(db_path)

        # ------------------------- PAGINE DELL'APP -------------------------

        # Login
        from view.login.login_page import LoginPage

        self.__login_page = LoginPage()

        from view.login.authentication_page import AuthenticationPage

        self.__authentication_page = AuthenticationPage()

        # Spettacoli
        from view.spettacoli.pagine.spettacoli_section import SpettacoliSectionView

        self.__spettacoli_section = SpettacoliSectionView()

        # Info
        from view.info.pagine.info_section import InfoSectionView
        from view.info.pagine.visualizza_opera import VisualizzaOperaView

        self.__info_section = InfoSectionView()
        self.__visualizza_opera_view = VisualizzaOperaView()

        from view.info.pagine.modifica_opera import NuovaOperaView, ModificaOperaView

        self.__nuova_opera_view = NuovaOperaView()
        self.__modifica_opera_view = ModificaOperaView()

        from view.info.pagine.modifica_genere import NuovoGenereView, ModificaGenereView

        self.__nuovo_genere_view = NuovoGenereView()
        self.__modifica_genere_view = ModificaGenereView()

        from view.info.pagine.modifica_regia import NuovaRegiaView, ModificaRegiaView

        self.__nuova_regia_view = NuovaRegiaView()
        self.__modifica_regia_view = ModificaRegiaView()

        # Account
        from view.account.pagine.account_section import AccountSectionView

        self.__account_section = AccountSectionView()

        # from view.account.pagine.modifica_account import (
        #     NuovoAccountView,
        #     ModificaAccountView,
        # )

        # self.nuovo_account_view = NuovoAccountView()
        # self.modifica_account_view = ModificaAccountView()

        # ------------------------- REGISTRAZIONE DELLE PAGINE -------------------------

        self.__nav.registra_pagina("login_page", self.__login_page)
        self.__nav.registra_pagina("authentication_page", self.__authentication_page)
        self.__nav.registra_pagina("spettacoli_section", self.__spettacoli_section)
        self.__nav.registra_pagina("info_section", self.__info_section)
        self.__nav.registra_pagina("nuova_opera", self.__nuova_opera_view)
        self.__nav.registra_pagina("modifica_opera", self.__modifica_opera_view)
        self.__nav.registra_pagina("visualizza_opera", self.__visualizza_opera_view)
        self.__nav.registra_pagina("nuova_regia", self.__nuova_regia_view)
        self.__nav.registra_pagina("modifica_regia", self.__modifica_regia_view)
        self.__nav.registra_pagina("nuovo_genere", self.__nuovo_genere_view)
        self.__nav.registra_pagina("modifica_genere", self.__modifica_genere_view)
        self.__nav.registra_pagina("account_section", self.__account_section)

        # ------------------------- CONTROLLERS DELLA VIEW -------------------------

        # LoginController
        from controller.login.login_controller import LoginController

        self.__login_controller = LoginController(
            self.__model, self.__login_page, self.__authentication_page
        )

        # SpettacoliController
        from controller.spettacoli.spettacoli_controller import SpettacoliController

        self.__spettacoli_controller = SpettacoliController(
            self.__model, self.__spettacoli_section
        )

        # InfoController
        from controller.info.info_controller import InfoController

        self.__info_controller = InfoController(self.__model, self.__info_section)

        # CUOperaController
        from controller.info.CU_opera_controller import CUOperaController

        self.__cu_opera_controller = CUOperaController(
            self.__model, self.__nuova_opera_view, self.__modifica_opera_view
        )

        # CUGenereController
        from controller.info.CU_genere_controller import CUGenereController

        self.__cu_genere_controller = CUGenereController(
            self.__model, self.__nuovo_genere_view, self.__modifica_genere_view
        )

        # VisualizzaOperaController
        from controller.info.visualizza_opera_controller import (
            VisualizzaOperaController,
        )

        self.__visualizza_opera_controller = VisualizzaOperaController(
            self.__model, self.__visualizza_opera_view
        )

        # CURegiaController
        from controller.info.CU_regia_controller import CURegiaController

        self.__cu_regia_controller = CURegiaController(
            self.__model, self.__nuova_regia_view, self.__modifica_regia_view
        )

        # AccountController
        from controller.account.account_controller import AccountController

        self.__account_controller = AccountController(
            self.__model, self.__account_section
        )

        # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

        # LoginController
        self.__login_controller.goBackRequest.connect(  # type:ignore
            self.__on_request_go_back
        )
        self.__login_controller.goToPageRequest.connect(  # type:ignore
            self.__on_request_go_to
        )

        # InfoController
        self.__info_controller.logoutRequest.connect(  # type:ignore
            self.__on_request_logout
        )
        self.__info_controller.goToPageRequest.connect(  # type:ignore
            self.__on_request_go_to
        )
        self.__info_controller.goToSectionRequest.connect(  # type:ignore
            self.__on_request_section_go_to
        )
        self.__info_controller.getNavPageRequest.connect(  # type:ignore
            self.__on_request_get_page
        )

        # CUOperaController
        self.__cu_opera_controller.goBackRequest.connect(  # type:ignore
            self.__on_request_go_back
        )
        self.__cu_opera_controller.getNavPageRequest.connect(  # type:ignore
            self.__on_request_get_page
        )

        # CUGenereController
        self.__cu_genere_controller.goBackRequest.connect(  # type:ignore
            self.__on_request_go_back
        )
        self.__cu_genere_controller.getNavPageRequest.connect(  # type:ignore
            self.__on_request_get_page
        )

        # VisualizzaOperaController
        self.__visualizza_opera_controller.goBackRequest.connect(  # type:ignore
            self.__on_request_go_back
        )
        self.__visualizza_opera_controller.goToPageRequest.connect(  # type:ignore
            self.__on_request_go_to
        )
        self.__visualizza_opera_controller.getNavPageRequest.connect(  # type:ignore
            self.__on_request_get_page
        )

        # CURegiaController
        self.__cu_regia_controller.goBackRequest.connect(  # type:ignore
            self.__on_request_go_back
        )
        self.__cu_regia_controller.getNavPageRequest.connect(  # type:ignore
            self.__on_request_get_page
        )

        # AccountController
        self.__account_controller.logoutRequest.connect(  # type:ignore
            self.__on_request_logout
        )
        self.__account_controller.goToPageRequest.connect(  # type:ignore
            self.__on_request_go_to
        )
        self.__account_controller.goToSectionRequest.connect(  # type:ignore
            self.__on_request_section_go_to
        )
        self.__account_controller.getNavPageRequest.connect(  # type:ignore
            self.__on_request_get_page
        )

        # SpettacoliController
        self.__spettacoli_controller.logoutRequest.connect(  # type:ignore
            self.__on_request_logout
        )
        self.__spettacoli_controller.goToPageRequest.connect(  # type:ignore
            self.__on_request_go_to
        )
        self.__spettacoli_controller.goToSectionRequest.connect(  # type:ignore
            self.__on_request_section_go_to
        )
        self.__spettacoli_controller.getNavPageRequest.connect(  # type:ignore
            self.__on_request_get_page
        )

    # ------------------------- METODI DI NAVIGAZIONE -------------------------

    def get_stack(self) -> QStackedWidget:
        return self.__nav.get_stack()

    def __on_request_logout(self) -> None:
        # - CORRIGERE: Da implementare autenticazione.
        self.__nav.go_to("login_page", False)
        # - Come faccio per resettare i filtri di ricerca delle sezioni
        # - TEST
        self.__spettacoli_section.filtro_ricerca = ""
        self.__spettacoli_section.ricerca_bar.setText("")
        self.__info_section.filtro_ricerca = ""
        self.__info_section.ricerca_bar.setText("")
        # - END
        self.__nav.svuota_history()

    def __on_request_go_back(self) -> None:
        self.__nav.go_back()

    def __on_request_go_to(self, page_name: str, save_history: bool) -> None:
        try:
            self.__nav.go_to(page_name, save_history)
        except KeyError as exc:
            MessageView.mostra_errore(
                self.__nav.get_cur_central_page(),
                # E' sempre chiamato con un centralWidget definito. Quindi, lanciare
                #   un RuntimeError è segno di un bug.
                "Pagina non trovata",
                f"Si è verificato un errore: {exc}",
            )

    def __on_request_section_go_to(self, page_name: str) -> None:
        try:
            self.__nav.section_go_to(page_name)
        except KeyError as exc:
            MessageView.mostra_errore(
                self.__nav.get_cur_central_page(),
                # E' sempre chiamato con un centralWidget definito. Quindi, in teoria,
                #   get_cur_central_page non lancia mai un RuntimeError.
                "Pagina non trovata",
                f"Si è verificato un errore: {exc}",
            )

    def __on_request_get_page(
        self, page_name: str, container: dict[str, Optional[QWidget]]
    ) -> None:
        container["value"] = self.__nav.get_pagina(page_name)
