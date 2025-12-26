from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtGui import QShowEvent
from typing import Optional
import sys

from controller.context import AppContext

from model.exceptions import DatoIncongruenteException

from view.style import load_main_stylesheet


# Con `# - ` ho segnato le annotazioni sui dettagli da modificare o corriggere
class MainWindow(QMainWindow):
    def __init__(self, db_path: Optional[str]) -> None:
        """Throws: DatoIncongruenteException"""
        super().__init__()
        self._geometry_initialized = False

        # Setup Applicazione
        self.__context = AppContext(self, db_path)

        # Setup finestra
        self.setWindowTitle("Tell")

        # Layout
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.addWidget(self.__context.get_stack())
        self.setCentralWidget(central)

    def showEvent(self, a0: Optional[QShowEvent]) -> None:
        super().showEvent(a0)

        if self._geometry_initialized:
            return

        window = self.windowHandle()
        if not window:
            return

        screen = window.screen()
        if not screen:
            return

        screen_geom = screen.availableGeometry()
        self.setMinimumHeight(screen_geom.height() - 100)
        self.setMinimumWidth(int(screen_geom.width() / 2))

        fg = self.frameGeometry()
        fg.moveCenter(screen_geom.center())
        self.move(fg.topLeft())

        self._geometry_initialized = True


if __name__ == "__main__":
    app = QApplication([])
    # app.setStyle("Fusion")
    app.setStyleSheet(load_main_stylesheet())

    try:
        window: MainWindow

        if len(sys.argv) == 2:
            window = MainWindow(sys.argv[1])
        elif len(sys.argv) == 1:
            window = MainWindow(None)
        else:
            print(
                f"Wrong number of arguments (expected 0 or 1, got {len(sys.argv)})",
                file=sys.stderr,
            )
            exit(1)

        window.show()
        app.exec()

    except DatoIncongruenteException as exc:
        print(exc, file=sys.stderr)
        exit(1)
