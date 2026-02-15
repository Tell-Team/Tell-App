from enum import StrEnum, verify, UNIQUE
from typing import TypeAlias, Union


class WidgetRole:
    """Enum con i ruoli per assegnare un layout particulare ai widget.

    Modo di uso: `my_widget.setProperty(WidgetRole.Tipo.NOME_RUOLO, True)`"""

    @verify(UNIQUE)
    class Label(StrEnum):
        TITLE = "title"  # QLabel
        HEADER1 = "header1"  # QLabel
        HEADER2 = "header2"  # QLabel
        HEADER3 = "header3"  # QLabel
        BODY_TEXT = "body-text"  # QLabel

    @verify(UNIQUE)
    class Button(StrEnum):
        TRASPARENT = "transparent-button"  # QPushButton
        MAIN = "main-button"  # QPushButton
        DEFAULT = "default-button"  # QPushButton
        SEARCH = "search-button"  # QPushButton
        SAVE = "save-button"  # QPushButton
        MODIFY = "modify-button"  # QPushButton
        DESTRUCTIVE = "destructive-button"  # QPushButton

    @verify(UNIQUE)
    class Item(StrEnum):
        CARD = "item-card"  # QWidget
        LIST = "item-list"  # QWidget

    @verify(UNIQUE)
    class LineEdit(StrEnum):
        SEARCH_BAR = "search-bar"  # QLineEdit

    @verify(UNIQUE)
    class ScrollArea(StrEnum):
        INVISIBLE_H_SCROLL = "invisible-h-scroll"  # QScrollArea


WidgetRoleAlias: TypeAlias = Union[
    WidgetRole.Label,
    WidgetRole.Button,
    WidgetRole.Item,
    WidgetRole.LineEdit,
    WidgetRole.ScrollArea,
]


class WidgetColor:
    """Enum con i ruoli per assegnare un colore ai widget.

    Modo di uso: `my_widget.setProperty(WidgetColor.Tipo.NOME_RUOLO, True)`"""

    @verify(UNIQUE)
    class Label(StrEnum):
        PRIMARY_COLOR = "primary-text"  # QLabel
        SECONDARY_COLOR = "secondary-text"  # QLabel
        ERROR_COLOR = "error-message"  # QLabel

    @verify(UNIQUE)
    class Button(StrEnum):
        BLUE = "blue-button"  # QPushButton

    @verify(UNIQUE)
    class Item(StrEnum):
        RED = "red-item"  # QWidget
        BLUE = "blue-item"  # QWidget


WidgetColorAlias: TypeAlias = Union[
    WidgetColor.Label,
    WidgetColor.Button,
    WidgetColor.Item,
]

WidgetStyle: TypeAlias = Union[WidgetRoleAlias, WidgetColorAlias]
