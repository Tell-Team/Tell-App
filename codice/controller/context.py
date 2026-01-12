from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QObject
from typing import Optional, Callable, Tuple, Type, Any

from controller.navigation import NavigationController, Pagina

from model.model import Model

from view.utils import PopupMessage

from view.main_window import MainWindow


class AppContext:
    """Classe dedicata a caricare tutto il contesto dell'app.
    - Crea un QDialog per il login;
    - Crea le pagine della view;
    - Registra le pagine nel `NavigationController`;
    - Crea i controller delle pagine della view;
    - Collega i segnali di navigazione del controller al `NavigationController`.

    :raise DatoIncongruenteException: il percorso specificato per il salvataggio
    dei dati dell'applicazione non è valido (non è una cartella).
    """

    def __init__(self, db_path: Optional[str]) -> None:
        # Crea un Model unici per tutta l'app
        self.__model = Model(db_path)

        # Logica Login
        from view.login import LoginDialog
        from controller.login import LoginController

        self.__login_dialog = LoginDialog()
        self.__login_controller = LoginController(self.__model, self.__login_dialog)

        self.__login_controller.loginSucceeded.connect(  # type:ignore
            self.__successful_login
        )

    def start(self) -> None:
        self.__login_dialog.show()

    # ------------------------- METODI DI LOGGING -------------------------

    def __successful_login(self) -> None:
        """Effettua un login dopo aver ricevuto credenziali valide."""
        self.__main_window = MainWindow()

        self.__nav = NavigationController(self.__main_window)

        self.carica_pagine()  # Carica le pagine dell'app
        self.registra_pagine()  # Registra le pagine nel NavigationController
        controllers = self.carica_controllers()  # Carica i controller della view
        self.collega_controllers(controllers)  # Collega i segnali dei controller

        self.__login_dialog.close()  # Chiede il LoginDialog
        self.__main_window.show()  # Mostra la MainWindow

    # ------------------------- PAGINE DELL'APP -------------------------

    def carica_pagine(self) -> None:
        # Account
        from view.account.pagine import (
            AccountSectionView,  # NuovoAccountView, ModificaAccountView
        )

        self.__account_section = AccountSectionView()
        # self.nuovo_account_view = NuovoAccountView()
        # self.modifica_account_view = ModificaAccountView()

        # Spettacoli
        from view.spettacoli.pagine import (
            SpettacoliSectionView,
            NuovoSpettacoloView,
            ModificaSpettacoloView,
        )

        self.__spettacoli_section = SpettacoliSectionView()
        self.__nuovo_spettacolo_view = NuovoSpettacoloView()
        self.__modifica_spettacolo_view = ModificaSpettacoloView()

        # Info
        from view.info.pagine import (
            InfoSectionView,
            NuovaOperaView,
            ModificaOperaView,
            NuovoGenereView,
            ModificaGenereView,
            VisualizzaOperaView,
            NuovaRegiaView,
            ModificaRegiaView,
        )

        self.__info_section = InfoSectionView()
        self.__nuova_opera_view = NuovaOperaView()
        self.__modifica_opera_view = ModificaOperaView()
        self.__nuovo_genere_view = NuovoGenereView()
        self.__modifica_genere_view = ModificaGenereView()
        self.__visualizza_opera_view = VisualizzaOperaView()
        self.__nuova_regia_view = NuovaRegiaView()
        self.__modifica_regia_view = ModificaRegiaView()

    # ------------------------- REGISTRAZIONE DELLE PAGINE -------------------------

    def registra_pagine(self) -> None:
        nav = self.__nav

        nav.registra_pagina(Pagina.SEZIONE_SPETTACOLI, self.__spettacoli_section)
        nav.registra_pagina(Pagina.NUOVO_SPETTACOLO, self.__nuovo_spettacolo_view)
        nav.registra_pagina(Pagina.MODIFICA_SPETTACOLO, self.__modifica_spettacolo_view)
        nav.registra_pagina(Pagina.SEZIONE_INFO, self.__info_section)
        nav.registra_pagina(Pagina.NUOVA_OPERA, self.__nuova_opera_view)
        nav.registra_pagina(Pagina.MODIFICA_OPERA, self.__modifica_opera_view)
        nav.registra_pagina(Pagina.VISUALIZZA_OPERA, self.__visualizza_opera_view)
        nav.registra_pagina(Pagina.NUOVA_REGIA, self.__nuova_regia_view)
        nav.registra_pagina(Pagina.MODIFICA_REGIA, self.__modifica_regia_view)
        nav.registra_pagina(Pagina.NUOVO_GENERE, self.__nuovo_genere_view)
        nav.registra_pagina(Pagina.MODIFICA_GENERE, self.__modifica_genere_view)
        nav.registra_pagina(Pagina.SEZIONE_ACCOUNT, self.__account_section)

        nav.get_stack().setCurrentWidget(self.__spettacoli_section)

    # ------------------------- CONTROLLERS DELLA VIEW -------------------------

    def carica_controllers(self) -> list[QObject]:
        # Account
        from controller.account import AccountSectionController

        # Spettacoli
        from controller.spettacoli import (
            SpettacoliSectionController,
            CUSpettacoloController,
        )

        # Info
        from controller.info import (
            InfoSectionController,
            VisualizzaOperaController,
            CUOperaController,
            CUGenereController,
            CURegiaController,
        )

        # Definizioni dei controller come attributi privati
        controller_defs: list[tuple[str, Type[QObject], Tuple[Any, ...]]] = [
            (
                "__account_controller",
                AccountSectionController,
                (self.__model, self.__account_section),
            ),
            (
                "__spettacoli_controller",
                SpettacoliSectionController,
                (self.__model, self.__spettacoli_section),
            ),
            (
                "__cu_spettacolo_controller",
                CUSpettacoloController,
                (
                    self.__model,
                    self.__nuovo_spettacolo_view,
                    self.__modifica_spettacolo_view,
                ),
            ),
            (
                "__info_controller",
                InfoSectionController,
                (self.__model, self.__info_section),
            ),
            (
                "__cu_opera_controller",
                CUOperaController,
                (self.__model, self.__nuova_opera_view, self.__modifica_opera_view),
            ),
            (
                "__cu_genere_controller",
                CUGenereController,
                (self.__model, self.__nuovo_genere_view, self.__modifica_genere_view),
            ),
            (
                "__visualizza_opera_controller",
                VisualizzaOperaController,
                (self.__model, self.__visualizza_opera_view),
            ),
            (
                "__cu_regia_controller",
                CURegiaController,
                (self.__model, self.__nuova_regia_view, self.__modifica_regia_view),
            ),
        ]

        controllers: list[QObject] = []

        # Creazione dei controller
        for attr, cls, args in controller_defs:
            controller = cls(*args)
            setattr(self, attr, controller)
            controllers.append(controller)

        return controllers

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    def collega_controllers(self, controllers: list[QObject]) -> None:
        # Tutti i controller devono usare, al di più, questi 5 segnali per la navigazione.
        signal_map: dict[str, Callable[..., None]] = {
            "logoutRequest": self.__logout,
            "goBackRequest": self.__go_back,
            "goToPageRequest": self.__go_to_page,
            "goToSectionRequest": self.__go_to_section,
            "getNavPageRequest": self.__get_page,
        }

        def safe_connect(
            controller: QObject, sig_name: str, handler: Callable[..., None]
        ) -> None:
            """Verifica che il controller abbia un segnale con un nome specifice
            e lo collega con lo slot corrispondente.

            :param controller: controller da cui sarano collegati i segnali
            :param sig_name: nome del segnale da cercare
            :param handler: slot da collegare al segnale se trovato"""
            sig = getattr(controller, sig_name, None)
            if sig and hasattr(sig, "connect"):
                sig.connect(handler)
            # else:
            #     print(f" - {sig_name} non trovato o non è un segnale di {controller}")

        for c in controllers:
            for sig_name, handler in signal_map.items():
                safe_connect(c, sig_name, handler)

    # ------------------------- METODI DI NAVIGAZIONE -------------------------

    def __logout(self) -> None:
        """Effettua un logout eliminando la sessione utente."""
        if self.__main_window:  # Elimina la MainWindow
            self.__main_window.close()
            self.__main_window = None

        self.__login_dialog.show()  # Mostra il LoginDialog di nuovo

    def __go_back(self) -> None:
        self.__nav.go_back()

    def __go_to_page(self, nome: Pagina, save_history: bool) -> None:
        try:
            self.__nav.go_to(nome, save_history)
        except KeyError as exc:
            PopupMessage.mostra_errore(
                self.__nav.get_cur_central_page(),
                "Pagina non trovata",
                f"Si è verificato un errore: {exc}",
            )

    def __go_to_section(self, nome: Pagina) -> None:
        try:
            self.__nav.section_go_to(nome)
        except KeyError as exc:
            PopupMessage.mostra_errore(
                self.__nav.get_cur_central_page(),
                "Pagina non trovata",
                f"Si è verificato un errore: {exc}",
            )

    def __get_page(self, nome: Pagina, container: dict[str, Optional[QWidget]]) -> None:
        container["value"] = self.__nav.get_pagina(nome)
