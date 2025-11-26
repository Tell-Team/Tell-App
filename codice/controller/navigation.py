from PyQt6.QtWidgets import QStackedWidget, QMainWindow, QWidget


class NavigationController:
    """
    Permette all'utente di navegare nelle pagine e sezioni della applicazione, utilizando una lista
    `__history` per indicare a che pagina andare dietro con `go_back` e due funzioni diverse per
    indicare se la pagina corrente vendrà salvata nella detta lista (`go_to`) o meno (`section_go_to`)
    dopo di andar a un'altra.
    """

    def __init__(self, main_window: QMainWindow):
        self._main_window = main_window
        self._stack = QStackedWidget()
        self._history: list[QWidget] = []  # Pile di widget per andar dietro
        self._pages: dict[str, QWidget] = {}

    def get_stack(self) -> QStackedWidget:
        return self._stack

    def add_page(self, page_name: str, widget: QWidget):
        """Registra una pagina nel dict `__pages` della classe con una `str` come keyword."""
        self._pages[page_name] = widget
        self._stack.addWidget(widget)

    def go_to(self, page_name: str, save_history: bool = True):
        """Visualizza una pagina registrata in `__pages`."""
        # ¿CÓMO ASIGNO LA DATA OBTENIDA POR ID A LAS PÁGINA QUE DEPENDE DE UNA INSTANCIA?
        widget = self._pages.get(page_name)
        if widget is None:
            raise ValueError(f"Non e' stata trovata la pagina: {page_name}")

        current = self._stack.currentWidget()
        if current and save_history:
            self._history.append(current)

        self._stack.setCurrentWidget(widget)

    def section_go_to(self, page_name: str):
        """Visualizza una pagina di sezione (Spettacoli, Info, Account) senza salvare la pagina
        corrente nella list `__history`."""
        self.go_to(page_name, save_history=False)

    def go_back(self):
        """Visualizza la pagina precedente, registrata nella list `__history`."""
        if not self._history:
            return
        last_widget = self._history.pop()
        self._stack.setCurrentWidget(last_widget)
