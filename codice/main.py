from PyQt6.QtWidgets import QApplication
import sys

from controller.context import AppContext

from model.exceptions import DatoIncongruenteException

from view.style import load_main_stylesheet


# Con `# - ` ho segnato le annotazioni sui dettagli da modificare o corriggere
def main():
    app = QApplication(sys.argv)
    # app.setStyle("Fusion")
    app.setStyleSheet(load_main_stylesheet())

    try:
        context: AppContext

        if len(sys.argv) == 2:
            context = AppContext(sys.argv[1])
        elif len(sys.argv) == 1:
            context = AppContext(None)
        else:
            print(
                f"Wrong number of arguments (expected 0 or 1, got {len(sys.argv)})",
                file=sys.stderr,
            )
            exit(1)

        context.start()

        sys.exit(app.exec())
    except DatoIncongruenteException as exc:
        print(exc, file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main()
