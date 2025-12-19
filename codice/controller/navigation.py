from PyQt6.QtWidgets import QStackedWidget, QMainWindow, QWidget
from typing import Optional


class NavigationController:
    """Permette all'utente di navigare le pagine e sezioni dell'app."""

    def __init__(self, main_window: QMainWindow) -> None:
        self._main_window = main_window
        self._stack = QStackedWidget()
        self._history: list[QWidget] = []  # Pile di widget per tornare dietro
        self._pages: dict[str, QWidget] = {}  # Registro delle pagine

    def get_stack(self) -> QStackedWidget:
        return self._stack

    def get_pages(self) -> dict[str, QWidget]:
        return self._pages

    def get_page(self, page_name: str) -> Optional[QWidget]:
        """Ritorna una pagina registrata.

        :param page_name: key usata per cercare la pagina nel dict"""
        for key in self._pages:
            if key == page_name:
                return self._pages.get(key)

    def get_cur_central_page(self) -> QWidget:
        """Ritorna la pagina visualizzata dall'utente.

        Usato dall'`AppContext` per sapere dove mostrare il messaggio d'errore generato
        da `go_to`.

        :raise RuntimeError: non c'è un central widget asegnato alla `QMainWindow`"""
        widget = self._main_window.centralWidget()
        if widget is None:
            raise RuntimeError("Non c'è un central widget asegnato.")
        return widget

    def add_page(self, page_name: str, widget: QWidget) -> None:
        """Registra una pagina nel controller.

        :param page_name: key usata per salvare la pagina nel dict
        :param widget: pagina da salvare nel dict"""
        self._pages[page_name] = widget
        self._stack.addWidget(widget)

    def go_to(self, page_name: str, save_history: bool = True) -> None:
        """Visualizza una pagina registrata nel controller.

        :param page_name: key usata per trovare la pagina
        :param save_history: verifica se la pagina sarà salvata nell'history del controller o no

        :raise KeyError: la pagina cercata non è stata trovata
        """
        try:
            widget = self._pages[page_name]
        except KeyError:
            raise KeyError(f"Non è stata trovata la pagina '{page_name}'.")

        current = self._stack.currentWidget()
        if current and save_history:
            self._history.append(current)

        # Dopo di andar ad un'altra pagina, questa viene aggiornata se ha il metodo
        #   `refresh_page` definito.
        if hasattr(widget, "refresh_page"):
            widget.refresh_page()  # type:ignore

        self._stack.setCurrentWidget(widget)

    def section_go_to(self, page_name: str) -> None:
        """Visualizza una pagina senza salvare la pagina corrente nell'history del controller.

        :param page_name: key usata per trovare la pagina"""
        self.go_to(page_name, save_history=False)

    def go_back(self) -> None:
        """Visualizza la pagina precedente, registrata nel'history del controller."""
        if not self._history:
            return
        last_widget = self._history.pop()

        if hasattr(last_widget, "refresh_page"):
            last_widget.refresh_page()  # type:ignore

        self._stack.setCurrentWidget(last_widget)
