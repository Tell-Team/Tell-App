from typing import Optional

from PyQt6.QtWidgets import QWidget, QPushButton

from view.style.ui_style import WidgetRole, WidgetColor
from view.utils import _svgIcon


class DefaultButton(QPushButton):
    def __init__(self, text: Optional[str] = None, parent: Optional[QWidget] = None):
        super().__init__(text, parent)

        self.setProperty(WidgetRole.DEFAULT_BUTTON, True)


class CreaButton(QPushButton):
    def __init__(
        self,
        text: Optional[str] = None,
        parent: Optional[QWidget] = None,
        has_icon: bool = True,
    ):
        super().__init__(text, parent)

        self.setProperty(WidgetColor.Button.BLUE_BUTTON, True)
        if has_icon:
            self.setIcon(_svgIcon.CREA_ICON)


class RicercaButton(QPushButton):
    def __init__(
        self,
        text: Optional[str] = None,
        parent: Optional[QWidget] = None,
        has_icon: bool = True,
    ):
        super().__init__(text, parent)

        self.setProperty(WidgetRole.SEARCH_BUTTON, True)
        self.setProperty(WidgetColor.Button.BLUE_BUTTON, True)
        if has_icon:
            self.setIcon(_svgIcon.RICERCA_ICON)


class SalvaButton(QPushButton):
    def __init__(
        self,
        text: Optional[str] = None,
        parent: Optional[QWidget] = None,
        has_icon: bool = True,
    ):
        super().__init__(text, parent)

        self.setProperty(WidgetRole.SAVE_BUTTON, True)
        if has_icon:
            self.setIcon(_svgIcon.SALVA_ICON)


class ModificaButton(QPushButton):
    def __init__(
        self,
        text: Optional[str] = None,
        parent: Optional[QWidget] = None,
        has_icon: bool = True,
    ):
        super().__init__(text, parent)

        self.setProperty(WidgetRole.MODIFY_BUTTON, True)
        if has_icon:
            self.setIcon(_svgIcon.MODIFICA_ICON)


class EliminaButton(QPushButton):
    def __init__(
        self,
        text: Optional[str] = None,
        parent: Optional[QWidget] = None,
        has_icon: bool = True,
    ):
        super().__init__(text, parent)

        self.setProperty(WidgetRole.DESTRUCTIVE_BUTTON, True)
        if has_icon:
            self.setIcon(_svgIcon.ELIMINA_ICON)
