from enum import StrEnum, verify, UNIQUE
from typing import TypeAlias, Union


@verify(UNIQUE)
class WidgetRole(StrEnum):
    """Enum con i ruoli per assegnare un layout particulare ai widget.

    Modo di uso: `my_widget.setProperty(WidgetRole.NOME_RUOLO, True)`"""

    TITLE = "title"  # QLabel
    HEADER1 = "header1"  # QLabel
    HEADER2 = "header2"  # QLabel
    HEADER3 = "header3"  # QLabel
    BODY_TEXT = "body-text"  # QLabel

    TRASPARENT_BUTTON = "transparent-button"  # QPushButton
    MAIN_BUTTON = "main-button"  # QPushButton
    DEFAULT_BUTTON = "default-button"  # QPushButton
    SEARCH_BUTTON = "search-button"  # QPushButton
    SAVE_BUTTON = "save-button"  # QPushButton
    MODIFY_BUTTON = "modify-button"  # QPushButton
    DESTRUCTIVE_BUTTON = "destructive-button"  # QPushButton

    ITEM_CARD = "item-card"  # QWidget
    ITEM_LIST = "item-list"  # QWidget

    SEARCH_BAR = "search-bar"  # QLineEdit

    INVISIBLE_H_SCROLL = "invisible-h-scroll"  # QScrollArea


class WidgetColor:
    """Enum con i ruoli per assegnare un colore ai widget."""

    @verify(UNIQUE)
    class Text(StrEnum):
        PRIMARY_TEXT = "primary-text"  # QLabel
        SECONDARY_TEXT = "secondary-text"  # QLabel
        ERROR_MESSAGE = "error-message"  # QLabel

    @verify(UNIQUE)
    class Button(StrEnum):
        BLUE_BUTTON = "blue-button"  # QPushButton

    @verify(UNIQUE)
    class Item(StrEnum):
        RED_ITEM = "red-item"  # QWidget
        BLUE_ITEM = "blue-item"  # QWidget


WidgetColorAlias: TypeAlias = Union[
    WidgetColor.Text, WidgetColor.Button, WidgetColor.Item
]
