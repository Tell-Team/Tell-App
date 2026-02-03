from typing import Optional

from PyQt6.QtWidgets import QWidget, QPushButton

from view.style.ui_style import WidgetRole, WidgetColor
from view.style.resource_svg import MODIFICA_ICON, ELIMINA_ICON, RICERCA_ICON


class ModificaButton(QPushButton):
    def __init__(self, text: Optional[str] = None, parent: Optional[QWidget] = None):
        super().__init__(text, parent)

        self.setProperty(WidgetRole.MODIFY_BUTTON, True)
        self.setIcon(MODIFICA_ICON)


class EliminaButton(QPushButton):
    def __init__(self, text: Optional[str] = None, parent: Optional[QWidget] = None):
        super().__init__(text, parent)

        self.setProperty(WidgetRole.DESTRUCTIVE_BUTTON, True)
        self.setIcon(ELIMINA_ICON)


class RicercaButton(QPushButton):
    def __init__(self, text: Optional[str] = None, parent: Optional[QWidget] = None):
        super().__init__(text, parent)

        self.setProperty(WidgetRole.SEARCH_BUTTON, True)
        self.setProperty(WidgetColor.Button.BLUE_BUTTON, True)
        self.setIcon(RICERCA_ICON)
