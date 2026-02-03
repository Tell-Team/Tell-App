from pathlib import Path

from PyQt6.QtGui import QIcon


__ROOT = Path(__file__).resolve().parent


def __resource_path(*parts: str) -> str:
    return str(__ROOT.joinpath(*parts))


# __ROOT = /codice/view//style/
ELIMINA_ICON = QIcon(__resource_path("icons", "elimina.svg"))
MODIFICA_ICON = QIcon(__resource_path("icons", "modifica.svg"))
RICERCA_ICON = QIcon(__resource_path("icons", "ricerca.svg"))
