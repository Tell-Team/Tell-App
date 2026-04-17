from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
import sys
from view import style

from controller.app_context import AppContext

from model.exceptions import DatoIncongruenteException


def main() -> None:
    app = QApplication(sys.argv)

    try:
        tema_corrente = style.rileva_tema_os()
    except NotImplementedError as exc:
        print(f"{type(exc).__name__}: {exc}", file=sys.stderr)
        tema_corrente = None  # L'app userà il tema chiaro per default
    app.setPalette(style.build_qpalette(tema_corrente))
    app.setStyleSheet(style.load_stylesheet(tema_corrente))

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
            sys.exit(2)

        _ = context

        sys.exit(app.exec())
    except DatoIncongruenteException as exc:
        print(f"{type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
