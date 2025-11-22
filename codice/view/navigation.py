from PyQt6.QtWidgets import QStackedWidget, QMainWindow, QWidget


class NavigationController:
    def __init__(self, main_window: QMainWindow):
        self._main_window = main_window
        self._stack = QStackedWidget()
        self._history: list[QWidget] = []  # Pile di widget per andar dietro
        self._pages: dict[type[QWidget], QWidget] = {}

    def add_page(self, page_class: type[QWidget], widget: QWidget):
        """Registra una pagina usando la classe come keyword."""
        self._pages[page_class] = widget
        self._stack.addWidget(widget)

    def get_stack(self):
        return self._stack

    def go_to(self, page_class: type[QWidget]):
        """Visualizza la pagina dalla classe."""
        widget = self._pages.get(page_class)
        if widget is None:
            raise ValueError(f"Non e' stata trovata la pagina: {page_class}")

        current = self._stack.currentWidget()
        if current:
            self._history.append(current)

        self._stack.setCurrentWidget(widget)

    def go_back(self):
        """Visualizza la pagina precedente."""
        if not self._history:
            return
        last_widget = self._history.pop()
        self._stack.setCurrentWidget(last_widget)
