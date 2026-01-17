from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from PyQt6.QtGui import QShowEvent
from typing import Optional


class MainWindow(QMainWindow):
    """Widget in cui vengono caricate tutte le pagine dell'app nel suo `QStackedWidget`."""

    def __init__(self):
        super().__init__()
        self.__geometry_initialized = False

        # Setup finestra
        self.setWindowTitle("Tell")

        self.__stack = QStackedWidget()
        self.setCentralWidget(self.__stack)

    def showEvent(self, a0: Optional[QShowEvent]) -> None:
        super().showEvent(a0)

        if self.__geometry_initialized:
            return

        window = self.windowHandle()
        if not window:
            return

        screen = window.screen()
        if not screen:
            return

        screen_geom = screen.availableGeometry()
        self.setMinimumHeight(screen_geom.height() - 100)
        self.setMinimumWidth(int(screen_geom.width() / 1.8))

        fg = self.frameGeometry()
        fg.moveCenter(screen_geom.center())
        self.move(fg.topLeft())

        self.__geometry_initialized = True

    def get_stack(self) -> QStackedWidget:
        return self.__stack
