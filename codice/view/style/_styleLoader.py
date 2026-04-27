"""
Loader centrale per gli stili dell'app.

- Rileva automaticamente il tema del sistema operativo.
- Crea la `QPalette` con colori per i `QWidget` secondo il tema dell'OS scelto.
- Gestisce il caricamento dei QSS per il layout ed i colori dei `QWidget` secondo
il tema dell'OS scelto.

Compatibile: Windows, macOS, fallback Linux (light)
"""

import subprocess
from PyQt6.QtGui import QPalette, QColor
from typing import Optional
from enum import StrEnum


class OSTheme(StrEnum):
    LIGHT = "light.qss"
    DARK = "dark.qss"


def rileva_tema_os() -> OSTheme:
    """Rileva automaticamente il tema del sistema operativo.

    Returns
    ---
        `"light.qss"` se il sistema è in light mode; `"dark.qss"`, se in dark mode.

    ---
    Throws: NotImplementedError
    """
    import platform

    match platform.system():
        case "Windows":
            # Windows 10/11: legge il registro
            try:
                import winreg

                chiave = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
                )
                valore, _ = winreg.QueryValueEx(chiave, "AppsUseLightTheme")
                winreg.CloseKey(chiave)
                return OSTheme.LIGHT if valore == 1 else OSTheme.DARK
            except Exception:
                return OSTheme.LIGHT  # fallback
        case "Darwin":
            # macOS: usa defaults read
            try:
                risultato = subprocess.run(
                    ["defaults", "read", "-g", "AppleInterfaceStyle"],
                    capture_output=True,
                    text=True,
                )
                if "Dark" in risultato.stdout:
                    return OSTheme.DARK
                return OSTheme.LIGHT
            except Exception:
                return OSTheme.LIGHT  # fallback
        case "Linux":
            # Linux: fallback light (GNOME/KDE differiscono)
            return OSTheme.LIGHT
        case _:
            raise NotImplementedError(
                f"Rilevamento tema non implementato per OS: {platform.system()}"
            )


def build_qpalette(theme: Optional[OSTheme] = None):
    """Crea un `QPalette` che corrisponda al tema dell'OS selezionato. Se nessun
    tema è selezionato, `light.qss` viene usato come default value.

    Returns
    ---
        `QPalette` pronta per `QApplication.setPalette`.
    """
    from view.style.palette import LIGHT, DARK

    qp = QPalette()

    if theme is None:
        palette = LIGHT
    palette = LIGHT if theme == OSTheme.LIGHT else DARK

    qp.setColor(QPalette.ColorRole.Window, QColor(palette.window_bg))
    qp.setColor(QPalette.ColorRole.WindowText, QColor(palette.window_text))
    qp.setColor(QPalette.ColorRole.Base, QColor(palette.editable_bg))

    qp.setColor(QPalette.ColorRole.Text, QColor(palette.editable_text))
    qp.setColor(QPalette.ColorRole.ButtonText, QColor(palette.button_text))
    qp.setColor(QPalette.ColorRole.PlaceholderText, QColor(palette.placeholder_text))

    qp.setColor(QPalette.ColorRole.Button, QColor(palette.button_bg))

    qp.setColor(QPalette.ColorRole.Highlight, QColor(palette.highlight))
    qp.setColor(QPalette.ColorRole.HighlightedText, QColor(palette.highlighted_text))
    qp.setColor(QPalette.ColorRole.Accent, QColor(palette.accent))

    qp.setColor(QPalette.ColorRole.ToolTipText, QColor(palette.tooltip_text))

    return qp


def load_stylesheet(theme: Optional[OSTheme] = None) -> str:
    """Carica lo style QSS applicando il tema dell'OS selezionato. Se nessun
    tema è selezionato, `light.qss` viene usato come default value.

    Returns
    ---
        QSS completo come stringa pronta per `QApplication.setStyleSheet`.

    ---
    Throws: FileNotFoundError, IOError
    """
    from PyQt6.QtCore import QFile, QTextStream

    if theme is None:
        theme = OSTheme.LIGHT

    paths = [
        ":/qss/themes/" + theme,  # QSS with color styling
        ":/qss/layouts/layout.qss",  # QSS with layout styling
    ]

    final_stylesheet = ""
    for path in paths:
        file = QFile(path)
        if not file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            raise FileNotFoundError(f"Cannot open QSS resource: {path}")
        stream = QTextStream(file)
        final_stylesheet += stream.readAll() + "\n"

    return final_stylesheet
