from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from typing import Optional
import sys

from controller.context import AppContext

from model.exceptions import DatoIncongruenteException

from view.style import load_main_stylesheet


# Con `# - ` ho segnato le annotazioni sui dettagli da modificare o corriggere
class MainWindowView(QMainWindow):
    def __init__(self, db_path: Optional[str]) -> None:
        """Throws: DatoIncongruenteException"""
        super().__init__()

        # Setup Applicazione
        self.__context = AppContext(self, db_path)

        # Setup finestra
        self.setWindowTitle("Tell")
        self.setMinimumSize(800, 600)

        # Layout
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.addWidget(self.__context.get_stack())
        self.setCentralWidget(central)


if __name__ == "__main__":
    app = QApplication([])
    # app.setStyle("Fusion")
    app.setStyleSheet(load_main_stylesheet())

    try:
        window: MainWindowView

        if len(sys.argv) == 2:
            window = MainWindowView(sys.argv[1])
        elif len(sys.argv) == 1:
            window = MainWindowView(None)
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
