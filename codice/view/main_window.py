from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShowEvent
from typing import Optional

from view.utils import TELL_ICON


class MainWindow(QMainWindow):
    """Widget in cui vengono caricate tutte le pagine dell'app nel suo `QStackedWidget`."""

    def __init__(self):
        super().__init__()
        self.__geometry_initialized = False

        # Setup finestra
        self.setWindowIcon(TELL_ICON)
        self.setWindowTitle("Tell")

        self.__stack = QStackedWidget()
        self.setCentralWidget(self.__stack)

        self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, False)

        # flags = self.windowFlags()
        # flags &= ~Qt.WindowType.WindowMaximizeButtonHint
        # self.setWindowFlags(flags)

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

        self.setFixedHeight(screen_geom.height() - 100)
        self.setFixedWidth(int(screen_geom.width() / 1.8))

        fg = self.frameGeometry()
        fg.moveCenter(screen_geom.center())
        self.move(fg.topLeft())

        self.__geometry_initialized = True

    def get_stack(self) -> QStackedWidget:
        return self.__stack
