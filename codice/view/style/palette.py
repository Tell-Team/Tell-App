"""
Palette di colori centralizzata per i temi dell'app.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Palette:
    window_bg: str  # QMainWindow, QDialog, QWidget, QGroupBox
    window_text: str  # QLabel, QGroupBox, static text
    editable_bg: str  # QLineEdit, QTextEdit, QPlainTextEdit, QComboBox

    editable_text: str  # QLineEdit, QTextEdit, item views
    button_text: str  # QPushButton, QToolButton
    placeholder_text: str  # QLineEdit, QTextEdit

    button_bg: str  # All button widgets.

    highlight: str  # Selected text, selected items, focused selections.
    highlighted_text: str  # Selections.
    accent: str  # Modern Qt styles, focus indicators

    tooltip_text: str  # Tooltip text.


LIGHT = Palette(
    window_bg="#f3f3f3",
    window_text="#222222",
    editable_bg="#ffffff",
    editable_text="#222222",
    button_text="#222222",
    placeholder_text="#909090",
    button_bg="#ffffff",
    highlight="#3182ce",
    highlighted_text="#ffffff",
    accent="#2b7cff",
    tooltip_text="#909090",
)

DARK = Palette(
    window_bg="#1e1e1e",
    window_text="#eeeeee",
    editable_bg="#000000",
    editable_text="#eeeeee",
    button_text="#eeeeee",
    placeholder_text="#bbbbbb",
    button_bg="#000000",
    highlight="#4a90e2",
    highlighted_text="#ffffff",
    accent="#2b7cff",
    tooltip_text="#bbbbbb",
)
