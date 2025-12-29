from enum import Enum


class QssStyle(Enum):
    """Enum con i ruoli (keys) per assegnare uno style ai widget."""

    # Usare .setProperty(QssStyle.NOME_RUOLO.style_role, True) per assegnare uno style.
    HEADER1 = "header1"  # QLabel
    HEADER2 = "header2"  # QLabel
    HEADER3 = "header3"  # QLabel
    PARAGRAPH = "paragraph"  # QLabel
    SECONDARY_TEXT = "secondary-text"  # QLabel
    ERROR_MESSAGE = "error-message"  # QLabel

    MAIN_BUTTON = "main-button"  # QPushButton
    SEARCH_BUTTON = "search-button"  # QPushButton

    BLUE_BUTTON = "blue-button"  # QPushButton
    WHITE_BUTTON = "white-button"  # QPushButton

    SAVE_BUTTON = "save-button"  # QPushButton
    MODIFY_BUTTON = "modify-button"  # QPushButton
    DESTRUCTIVE_BUTTON = "destructive-button"  # QPushButton

    ITEM_CARD = "item-card"  # QWidget
    ITEM_LIST = "item-list"  # QWidget

    SEARCH_BAR = "search-bar"  # QLineEdit

    @property
    def style_role(self) -> str:
        """Ottieni la string con il ruolo da asegnare."""
        return self.value
