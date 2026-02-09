from pathlib import Path

from PyQt6.QtGui import QIcon


__ROOT = Path(__file__).resolve().parent


def __resource_path(*parts: str) -> str:
    return str(__ROOT.joinpath(*parts))


# - Debo compilar el resources.qrc con pyrcc6;
#   pyrcc6 viene con PyQt6-tools;
#   PyQt6-tools no se puede instalar sin qmake;
#   qmake se instala con el Qt Framework;
#   Puedo instalar el Qt Framework con "https://www.qt.io/download-qt-installer" y añadir
#   su bin en PATH.

#   python -m pip install PyQt6-tools
#   pyrcc6 resources.qrc -o resources_rc.py

# MODIFICA_ICON = QIcon(":/icons/modifica.svg")

# __ROOT = /codice/view//style/
CREA_ICON = QIcon(__resource_path("icons", "crea.svg"))
SALVA_ICON = QIcon(__resource_path("icons", "salva.svg"))
ELIMINA_ICON = QIcon(__resource_path("icons", "elimina.svg"))
MODIFICA_ICON = QIcon(__resource_path("icons", "modifica.svg"))
RICERCA_ICON = QIcon(__resource_path("icons", "ricerca.svg"))
