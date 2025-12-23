from PyQt6.QtWidgets import QMainWindow, QWidget, QStackedWidget
from enum import Enum
from typing import Optional


class Pagina(Enum):
    """Enum con i nomi (keys) per registrare pagine nel `NavigationController`."""

    # I valori indicano il nome del file dove si trova la classe della pagina.
    # Non hanno uno scopo funzionale dentro del codice.
    PAGINA_LOGIN = "login_page"
    PAGINA_AUTENTICAZIONE = "authentication_page"
    SEZIONE_SPETTACOLI = "spettacoli_section"
    SEZIONE_INFO = "info_section"
    NUOVA_OPERA = "nuova_opera"
    MODIFICA_OPERA = "modifica_opera"
    VISUALIZZA_OPERA = "visualizza_opera"
    NUOVA_REGIA = "nuova_regia"
    MODIFICA_REGIA = "modifica_regia"
    NUOVO_GENERE = "nuovo_genere"
    MODIFICA_GENERE = "modifica_genere"
    SEZIONE_ACCOUNT = "account_section"


class NavigationController:
    """Permette all'utente di navigare le pagine e sezioni dell'app."""

    def __init__(self, main_window: QMainWindow) -> None:
        self._main_window = main_window
        self._stack = QStackedWidget()
        self._history: list[QWidget] = []  # Pile di widget per tornare dietro
        self._pagine: dict[Pagina, QWidget] = {}  # Registro delle pagine

    def get_stack(self) -> QStackedWidget:
        return self._stack

    # def get_pagine(self) -> dict[str, QWidget]:
    #     return self._pagine

    def get_pagina(self, nome: Pagina) -> Optional[QWidget]:
        """Ritorna una pagina registrata.

        :param nome: key usata per cercare la pagina nel dict"""
        for key in self._pagine:
            if key == nome:
                return self._pagine.get(key)

    def get_cur_central_page(self) -> QWidget:
        """Ritorna la pagina visualizzata dall'utente.

        Usato dall'`AppContext` per sapere dove mostrare il messaggio d'errore generato
        da `go_to`.

        :raise RuntimeError: non c'è un central widget asegnato alla `QMainWindow`"""
        widget = self._main_window.centralWidget()
        if widget is None:
            raise RuntimeError("Non c'è un central widget asegnato.")
        return widget

    def registra_pagina(self, nome: Pagina, widget: QWidget) -> None:
        """Registra una pagina nel controller.

        :param nome: key usata per salvare la pagina nel dict
        :param widget: pagina da salvare nel dict"""
        self._pagine[nome] = widget
        self._stack.addWidget(widget)

    def go_to(self, nome: Pagina, save_history: bool = True) -> None:
        """Visualizza una pagina registrata nel controller.

        :param nome: key usata per trovare la pagina
        :param save_history: verifica se la pagina sarà salvata nell'history del controller o no

        :raise KeyError: la pagina cercata non è stata trovata
        """
        try:
            widget = self._pagine[nome]
        except KeyError:
            raise KeyError(f"Non è stata trovata la pagina '{nome}'.")

        current = self._stack.currentWidget()
        if current and save_history:
            self._history.append(current)

        # Dopo di andar ad un'altra pagina, questa viene aggiornata se ha il metodo
        #   `aggiorna_pagina` definito.
        if hasattr(widget, "aggiorna_pagina"):
            widget.aggiorna_pagina()  # type:ignore

        self._stack.setCurrentWidget(widget)

    def section_go_to(self, nome: Pagina) -> None:
        """Visualizza una pagina senza salvare la pagina corrente nell'history del controller.

        :param nome: key usata per trovare la pagina"""
        self.go_to(nome, save_history=False)

    def go_back(self) -> None:
        """Visualizza la pagina precedente, registrata nel'history del controller."""
        if not self._history:
            return
        last_widget = self._history.pop()

        if hasattr(last_widget, "aggiorna_pagina"):
            last_widget.aggiorna_pagina()  # type:ignore

        self._stack.setCurrentWidget(last_widget)

    def svuota_history(self) -> None:
        """Svuota la lista history del controller."""
        self._history.clear()
