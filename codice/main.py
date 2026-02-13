from PyQt6.QtWidgets import QApplication
import logging
import sys
from view.style import resources_rc  # type:ignore

from controller.app_context import AppContext

from model.exceptions import DatoIncongruenteException

from view.style import rileva_tema_os, build_qpalette, load_stylesheet


def main() -> None:
    app = QApplication(sys.argv)

    try:
        tema_corrente = rileva_tema_os()
    except NotImplementedError as exc:
        logging.error("%s: %s", type(exc).__name__, exc)
        tema_corrente = None  # L'app userà il tema chiaro per default
    app.setPalette(build_qpalette(tema_corrente))
    app.setStyleSheet(load_stylesheet(tema_corrente))

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

        _ = context

        sys.exit(app.exec())
    except DatoIncongruenteException as exc:
        print(exc, file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main()
