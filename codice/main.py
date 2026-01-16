from PyQt6.QtWidgets import QApplication
import sys

from controller.app_context import AppContext
from model.exceptions import DatoIncongruenteException

from view.style.styleLoader import load_main_stylesheet, rileva_tema_os  # <- rilevamento automatico

def main() -> None:
    app = QApplication(sys.argv)

    # Rileva automaticamente il tema dall'OS
    tema_corrente: str = rileva_tema_os()  # ritorna "chiaro" o "scuro"
    app.setStyleSheet(load_main_stylesheet(tema_corrente))

    print (tema_corrente)

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

            _=context    
  
        sys.exit(app.exec())
    except DatoIncongruenteException as exc:
        print(exc, file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main()
