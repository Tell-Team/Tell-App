from enum import Enum
from PyQt6.QtWidgets import QWidget, QStackedWidget
from PyQt6.QtCore import QObject, pyqtSignal
from typing import Optional, Callable, Tuple, Type, Any

from controller.login.user_session import UserSession

from model.model import Model

from view.main_window import MainWindow

from view.utils import PopupMessage


class Pagina(Enum):
    """Enum con i nomi (keys) per registrare pagine nel `NavigationController`."""

    # I valori indicano il nome del file dove si trova la classe della pagina.
    # Non hanno uno scopo funzionale dentro del codice.
    SEZIONE_ACQUISTO = "acquisto_section"
    SCEGLI_POSTI = "scegli_posti"

    SEZIONE_SPETTACOLI = "spettacoli_section"
    VISUALIZZA_SPETTACOLO = "visualizza_spettacolo"
    NUOVO_SPETTACOLO = "nuovo_spettacolo"
    MODIFICA_SPETTACOLO = "modifica_spettacolo"
    NUOVO_EVENTO = "nuovo_evento"
    MODIFICA_EVENTO = "modifica_evento"

    SEZIONE_INFO = "info_section"
    VISUALIZZA_OPERA = "visualizza_opera"
    NUOVA_OPERA = "nuova_opera"
    MODIFICA_OPERA = "modifica_opera"
    NUOVO_GENERE = "nuovo_genere"
    MODIFICA_GENERE = "modifica_genere"
    NUOVA_REGIA = "nuova_regia"
    MODIFICA_REGIA = "modifica_regia"

    SEZIONE_TEATRO = "teatro_section"
    VISUALIZZA_SEZIONE = "visualizza_sezione"
    NUOVA_SEZIONE = "nuova_sezione"
    MODIFICA_SEZIONE = "modifica_sezione"

    SEZIONE_ACCOUNT = "account_section"
    NUOVO_ACCOUNT = "nuovo_account"
    MODIFICA_ACCOUNT = "modifica_account"


class NavigationController(QObject):
    """Controller che carica tutte le pagine e controller necessari secondo i permessi
    forniti dall'`AuthenticationService`, con la sessione utente corrente memorizzata.
    """

    logoutRequest: pyqtSignal = pyqtSignal()

    def __init__(
        self, model: Model, main_window: MainWindow, user_session: UserSession
    ):
        super().__init__()

        self.__main_window = main_window
        self.__user_session = user_session
        self.__history: list[QWidget] = []  # Pile di widget per tornare dietro
        self.__pagine: dict[Pagina, QWidget] = {}  # Registro delle pagine

        self.__carica_pagine()
        self.__registra_pagine_in_stack()
        controllers = self.__carica_controllers(model)
        self.__collega_controllers(controllers)

    # ------------------------- METODI DI NAVIGAZIONE -------------------------
    # --- Metodi della classe ---
    def __get_stack(self) -> QStackedWidget:
        return self.__main_window.get_stack()

    def __get_current_central_page(self) -> QWidget:
        """Ritorna la pagina visualizzata dall'utente.

        :raise RuntimeError: non c'è un central widget asegnato alla `QMainWindow`
        """
        # È sempre chiamato con un centralWidget definito. Quindi, lanciare
        #   un RuntimeError è segno di un bug.
        widget = self.__main_window.centralWidget()
        if widget is None:
            raise RuntimeError("Non c'è un central widget asegnato.")
        return widget

    def __registra_pagina(self, nome: Pagina, widget: QWidget) -> None:
        """Registra una pagina nell'history.

        :param nome: key usata per salvare la pagina nel dict
        :param widget: pagina da salvare nel dict
        """
        self.__pagine[nome] = widget
        self.__get_stack().addWidget(widget)

    def esiste_pagina(self, nome: Pagina) -> Optional[QWidget]:
        """Ritorna una pagina registrata nell'history.

        :param nome: key usata per cercare la pagina nel dict
        """
        for key in self.__pagine:
            if key == nome:
                return self.__pagine.get(key)

    # --- Metodi da collegare ai controller ---
    def __go_back(self) -> None:
        """Visualizza la pagina precedente, registrata nell'history."""
        if not self.__history:
            return
        last_widget = self.__history.pop()

        attr = getattr(last_widget, "aggiorna_pagina", None)
        if callable(attr):
            attr()

        self.__get_stack().setCurrentWidget(last_widget)

    def __go_to_page(self, nome: Pagina, save_history: bool = True) -> None:
        """Visualizza una pagina registrata.

        :param nome: key usata per trovare la pagina
        :param save_history: verifica se la pagina sarà salvata nell'history o no

        :raise KeyError: la pagina cercata non è stata trovata
        """
        try:
            widget = self.__pagine[nome]
        except KeyError as exc:
            PopupMessage.mostra_errore(
                self.__get_current_central_page(),
                "Pagina non trovata",
                f"Si è verificato un errore: {exc}",
            )
        else:
            current = self.__get_stack().currentWidget()
            if current and save_history:
                self.__history.append(current)

            # Dopo di andar ad un'altra pagina, questa viene aggiornata se ha il metodo
            #   `aggiorna_pagina` definito.
            attr = getattr(widget, "aggiorna_pagina", None)
            if callable(attr):
                attr()

            self.__get_stack().setCurrentWidget(widget)

    def __go_to_section(self, nome: Pagina) -> None:
        """Visualizza una pagina senza salvare la pagina corrente nell'history.

        :param nome: key usata per trovare la pagina
        """
        self.__go_to_page(nome, save_history=False)

    # Questo metodo è chiamato per ottenere l'istanza di pagina nei controller della view
    def __get_page(self, nome: Pagina, container: dict[str, Optional[QWidget]]) -> None:
        container["value"] = self.esiste_pagina(nome)

    # ------------------------- CREAZIONE DELLE PAGINE -------------------------

    def __carica_pagine(self) -> None:
        # Acquisto
        from view.acquisto.pagine import AcquistoSectionView, ScegliPostiView

        self.__acquisto_section = AcquistoSectionView(self.__user_session)
        self.__scegli_posti_view = ScegliPostiView()

        # Info
        from view.info.pagine import InfoSectionView, VisualizzaOperaView

        self.__info_section = InfoSectionView(self.__user_session)
        self.__visualizza_opera_view = VisualizzaOperaView(self.__user_session)

        if self.__user_session.ha_permessi_biglietteria():
            # Spettacoli
            from view.spettacoli.pagine import (
                SpettacoliSectionView,
                VisualizzaSpettacoloView,
                NuovoSpettacoloView,
                ModificaSpettacoloView,
                NuovoEventoView,
                ModificaEventoView,
            )

            self.__spettacoli_section = SpettacoliSectionView(self.__user_session)
            self.__visualizza_spettacolo_view = VisualizzaSpettacoloView(
                self.__user_session
            )
            self.__nuovo_spettacolo_view = NuovoSpettacoloView()
            self.__modifica_spettacolo_view = ModificaSpettacoloView()
            self.__nuovo_evento_view = NuovoEventoView()
            self.__modifica_evento_view = ModificaEventoView()

        if self.__user_session.ha_permessi_admin():
            # Info
            from view.info.pagine import (
                NuovaOperaView,
                ModificaOperaView,
                NuovoGenereView,
                ModificaGenereView,
                NuovaRegiaView,
                ModificaRegiaView,
            )

            self.__nuova_opera_view = NuovaOperaView()
            self.__modifica_opera_view = ModificaOperaView()
            self.__nuovo_genere_view = NuovoGenereView()
            self.__modifica_genere_view = ModificaGenereView()
            self.__nuova_regia_view = NuovaRegiaView()
            self.__modifica_regia_view = ModificaRegiaView()

            # Teatro
            from view.teatro.pagine import (
                TeatroSectionView,
                VisualizzaSezioneView,
                NuovaSezioneView,
                ModificaSezioneView,
            )

            self.__teatro_section = TeatroSectionView()
            self.__visualizza_sezione_view = VisualizzaSezioneView()
            self.__nuova_sezione_view = NuovaSezioneView()
            self.__modifica_sezione_view = ModificaSezioneView()

            # Account
            from view.account.pagine import (
                AccountSectionView,
                NuovoAccountView,
                ModificaAccountView,
            )

            self.__account_section = AccountSectionView(self.__user_session)
            self.__nuovo_account_view = NuovoAccountView()
            self.__modifica_account_view = ModificaAccountView()

    # ------------------------- REGISTRAZIONE DELLE PAGINE -------------------------

    def __registra_pagine_in_stack(self) -> None:
        # Acquisto
        self.__registra_pagina(Pagina.SEZIONE_ACQUISTO, self.__acquisto_section)
        self.__registra_pagina(Pagina.SCEGLI_POSTI, self.__scegli_posti_view)
        # Info
        self.__registra_pagina(Pagina.SEZIONE_INFO, self.__info_section)
        self.__registra_pagina(Pagina.VISUALIZZA_OPERA, self.__visualizza_opera_view)

        if self.__user_session.ha_permessi_biglietteria():
            # Spettacoli
            self.__registra_pagina(Pagina.SEZIONE_SPETTACOLI, self.__spettacoli_section)
            self.__registra_pagina(
                Pagina.VISUALIZZA_SPETTACOLO, self.__visualizza_spettacolo_view
            )
            self.__registra_pagina(
                Pagina.NUOVO_SPETTACOLO, self.__nuovo_spettacolo_view
            )
            self.__registra_pagina(
                Pagina.MODIFICA_SPETTACOLO, self.__modifica_spettacolo_view
            )
            self.__registra_pagina(Pagina.NUOVO_EVENTO, self.__nuovo_evento_view)
            self.__registra_pagina(Pagina.MODIFICA_EVENTO, self.__modifica_evento_view)

        if self.__user_session.ha_permessi_admin():
            # Info
            self.__registra_pagina(Pagina.NUOVA_OPERA, self.__nuova_opera_view)
            self.__registra_pagina(Pagina.MODIFICA_OPERA, self.__modifica_opera_view)
            self.__registra_pagina(Pagina.NUOVO_GENERE, self.__nuovo_genere_view)
            self.__registra_pagina(Pagina.MODIFICA_GENERE, self.__modifica_genere_view)
            self.__registra_pagina(Pagina.NUOVA_REGIA, self.__nuova_regia_view)
            self.__registra_pagina(Pagina.MODIFICA_REGIA, self.__modifica_regia_view)
            # Teatro
            self.__registra_pagina(Pagina.SEZIONE_TEATRO, self.__teatro_section)
            self.__registra_pagina(
                Pagina.VISUALIZZA_SEZIONE, self.__visualizza_sezione_view
            )
            self.__registra_pagina(Pagina.NUOVA_SEZIONE, self.__nuova_sezione_view)
            self.__registra_pagina(
                Pagina.MODIFICA_SEZIONE, self.__modifica_sezione_view
            )
            # Account
            self.__registra_pagina(Pagina.SEZIONE_ACCOUNT, self.__account_section)
            self.__registra_pagina(Pagina.NUOVO_ACCOUNT, self.__nuovo_account_view)
            self.__registra_pagina(
                Pagina.MODIFICA_ACCOUNT, self.__modifica_account_view
            )

        self.__get_stack().setCurrentWidget(self.__acquisto_section)

    # ------------------------- CONTROLLER DELLA VIEW -------------------------

    def __carica_controllers(self, model: Model) -> list[QObject]:
        # Controller necessario per gli utenti Cliente
        from controller.acquisto import AcquistoSectionController, ScegliPostiController
        from controller.info import InfoSectionController, VisualizzaOperaController

        # Definizioni dei controller come attributi privati
        controller_defs: list[tuple[str, Type[QObject], Tuple[Any, ...]]] = [
            (
                "__acquisto_controller",
                AcquistoSectionController,
                (model, self.__acquisto_section),
            ),
            (
                "__scegli_posti_controller",
                ScegliPostiController,
                (model, self.__scegli_posti_view),
            ),
            (
                "__info_controller",
                InfoSectionController,
                (model, self.__info_section),
            ),
            (
                "__visualizza_opera_controller",
                VisualizzaOperaController,
                (model, self.__visualizza_opera_view),
            ),
        ]

        if self.__user_session.ha_permessi_biglietteria():
            # Spettacoli
            from controller.spettacoli import (
                SpettacoliSectionController,
                VisualizzaSpettacoloController,
                CUSpettacoloController,
                CUEventoController,
            )

            controller_defs.extend(
                [
                    (
                        "__spettacoli_controller",
                        SpettacoliSectionController,
                        (model, self.__spettacoli_section),
                    ),
                    (
                        "__visualizza_spettacolo_controller",
                        VisualizzaSpettacoloController,
                        (model, self.__visualizza_spettacolo_view),
                    ),
                    (
                        "__cu_spettacolo_controller",
                        CUSpettacoloController,
                        (
                            model,
                            self.__nuovo_spettacolo_view,
                            self.__modifica_spettacolo_view,
                        ),
                    ),
                    (
                        "__cu_evento_controller",
                        CUEventoController,
                        (
                            model,
                            self.__nuovo_evento_view,
                            self.__modifica_evento_view,
                        ),
                    ),
                ]
            )

        if self.__user_session.ha_permessi_admin():
            # Info
            from controller.info import (
                CUOperaController,
                CUGenereController,
                CURegiaController,
            )

            controller_defs.extend(
                [
                    (
                        "__cu_opera_controller",
                        CUOperaController,
                        (model, self.__nuova_opera_view, self.__modifica_opera_view),
                    ),
                    (
                        "__cu_genere_controller",
                        CUGenereController,
                        (model, self.__nuovo_genere_view, self.__modifica_genere_view),
                    ),
                    (
                        "__cu_regia_controller",
                        CURegiaController,
                        (model, self.__nuova_regia_view, self.__modifica_regia_view),
                    ),
                ]
            )
            # Teatro
            from controller.teatro import (
                TeatroSectionController,
                VisualizzaSezioneController,
                CUSezioneController,
            )

            controller_defs.extend(
                [
                    (
                        "__teatro_controller",
                        TeatroSectionController,
                        (model, self.__teatro_section),
                    ),
                    (
                        "__visualizza_sezione_controller",
                        VisualizzaSezioneController,
                        (model, self.__visualizza_sezione_view),
                    ),
                    (
                        "__cu_sezione_controller",
                        CUSezioneController,
                        (
                            model,
                            self.__nuova_sezione_view,
                            self.__modifica_sezione_view,
                        ),
                    ),
                ]
            )
            # Account
            from controller.account import AccountSectionController, CUAccountController

            controller_defs.extend(
                [
                    (
                        "__account_controller",
                        AccountSectionController,
                        (model, self.__account_section, self.__user_session),
                    ),
                    (
                        "__cu_account_controller",
                        CUAccountController,
                        (
                            model,
                            self.__nuovo_account_view,
                            self.__modifica_account_view,
                            self.__user_session,
                        ),
                    ),
                ]
            )

        controllers: list[QObject] = []

        # Creazione dei controller
        for attr, cls, args in controller_defs:
            controller = cls(*args)
            setattr(self, attr, controller)
            controllers.append(controller)

        return controllers

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    def __collega_controllers(self, controllers: list[QObject]) -> None:
        # Tutti i controller devono usare, al di più, questi 5 segnali per la navigazione.
        signal_map: dict[str, Callable[..., None]] = {
            "logoutRequest": self.logoutRequest.emit,
            "goBackRequest": self.__go_back,
            "goToPageRequest": self.__go_to_page,
            "goToSectionRequest": self.__go_to_section,
            "getPageRequest": self.__get_page,
        }

        def safe_connect(
            controller: QObject, signal_name: str, handler: Callable[..., None]
        ) -> None:
            """Verifica che il controller abbia un segnale con un nome specifice
            e lo collega con lo slot corrispondente.

            :param controller: controller da cui sarano collegati i segnali
            :param signal_name: nome del segnale da cercare
            :param handler: slot da collegare al segnale se trovato
            """
            signal = getattr(controller, signal_name, None)
            if signal and hasattr(signal, "connect"):
                signal.connect(handler)
            # else:
            #     print(f" - {sig_name} non trovato o non è un segnale di {controller}")

        for c in controllers:
            for sig_name, handler in signal_map.items():
                safe_connect(c, sig_name, handler)
