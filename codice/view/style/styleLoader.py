"""
Loader centrale per gli stili dell'app.

- Rileva automaticamente il tema del sistema operativo.
- Crea la `QPalette` con colori per i `QWidget` secondo il tema dell'OS scelto.
- Gestisce il caricamento dei QSS per il layout ed i colori dei `QWidget` secondo
il tema dell'OS scelto.

Compatibile: Windows, macOS, fallback Linux (light)
"""

import platform
import subprocess
from pathlib import Path
from PyQt6.QtGui import QPalette, QColor
from typing import Literal, Optional

from view.style.palette import LIGHT, DARK

type OSTheme = Literal["light.qss", "dark.qss"]


def rileva_tema_os() -> OSTheme:
    """Rileva automaticamente il tema del sistema operativo.

    Returns
    ---
        `"light.qss"` se il sistema è in light mode; `"dark.qss"`, se in dark mode.

    ---
    Throws: NotImplementedError
    """
    sistema: str = platform.system()

    if sistema == "Windows":
        # Windows 10/11: legge il registro
        try:
            import winreg

            chiave = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
            )
            valore, _ = winreg.QueryValueEx(chiave, "AppsUseLightTheme")
            winreg.CloseKey(chiave)
            return "light.qss" if valore == 1 else "dark.qss"
        except Exception:
            return "light.qss"  # fallback
    elif sistema == "Darwin":
        # macOS: usa defaults read
        try:
            risultato = subprocess.run(
                ["defaults", "read", "-g", "AppleInterfaceStyle"],
                capture_output=True,
                text=True,
            )
            if "Dark" in risultato.stdout:
                return "dark.qss"
            else:
                return "light.qss"
        except Exception:
            return "light.qss"  # fallback
    elif sistema == "Linux":
        # Linux: fallback light (GNOME/KDE differiscono)
        return "light.qss"
    else:
        raise NotImplementedError(
            f"Rilevamento tema non implementato per OS: {sistema}"
        )


def build_qpalette(theme: Optional[OSTheme] = None) -> QPalette:
    """Crea un `QPalette` che corrisponda al tema dell'OS selezionato. Se nessun
    tema è selezionato, `light.qss` viene usato come default value.

    Returns
    ---
        `QPalette` pronta per `QApplication.setPalette`.
    """
    qp = QPalette()

    if theme is None or theme == "light.qss":
        palette = LIGHT
    elif theme == "dark.qss":
        palette = DARK

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
    if theme is None:
        theme = "light.qss"

    COLORS_QSS_PATH = Path(__file__).parent / "qss" / "themes" / theme
    LAYOUT_QSS_PATH = Path(__file__).parent / "qss" / "layouts" / "layout.qss"

    qss_finale: str
    with open(COLORS_QSS_PATH, "r", encoding="utf-8") as f:
        qss_finale = f.read()
    with open(LAYOUT_QSS_PATH, "r", encoding="utf-8") as file:
        qss_finale = qss_finale + file.read()

    return qss_finale
