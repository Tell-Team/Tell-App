# -*- coding: utf-8 -*-
"""
Loader centrale per gli stili QSS dell'app
Gestisce il caricamento del template QSS e la sostituzione dei colori
secondo il tema scelto (chiaro/scuro). Rileva automaticamente il tema del sistema operativo.

Compatibile: Windows, macOS, fallback Linux (light)
"""

import sys
import platform
import subprocess
from pathlib import Path
from typing import Literal

from view.style.palette import COLORI_CHIARO, COLORI_SCURO

# Percorso del QSS template
MAIN_QSS_PATH: Path = Path(__file__).parent / "main.qss"


def __carica_file_qss(percorso: Path) -> str:
    """Carica il contenuto di un file QSS e lo ritorna come stringa.
    Throws: FileNotFoundError, IOError
    """
    with open(percorso, "r", encoding="utf-8") as file:
        return file.read()


def __sostituisci_placeholder_qss(qss_template: str, palette: dict[str, str]) -> str:
    """Sostituisce i placeholder del QSS con i colori della palette.
    Placeholder nel QSS: {{nome_colore}}
    Throws: KeyError
    """
    qss_finale: str = qss_template
    for nome_colore, valore in palette.items():
        qss_finale = qss_finale.replace(f"{{{{{nome_colore}}}}}", valore)
    return qss_finale


def rileva_tema_os() -> Literal["chiaro", "scuro"]:
    """Rileva automaticamente il tema del sistema operativo.
    
    Returns:
        "chiaro" se il sistema è in light mode, "scuro" se in dark mode.
    
    Throws: NotImplementedError, subprocess.CalledProcessError
    """
    sistema: str = platform.system()

    if sistema == "Windows":
        # Windows 10/11: legge il registro
        try:
            import winreg
            chiave = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            )
            valore, _ = winreg.QueryValueEx(chiave, "AppsUseLightTheme")
            winreg.CloseKey(chiave)
            return "chiaro" if valore == 1 else "scuro"
        except Exception:
            return "chiaro"  # fallback

    elif sistema == "Darwin":
        # macOS: usa defaults read
        try:
            risultato = subprocess.run(
                ["defaults", "read", "-g", "AppleInterfaceStyle"],
                capture_output=True, text=True
            )
            if "Dark" in risultato.stdout:
                return "scuro"
            else:
                return "chiaro"
        except Exception:
            return "chiaro"  # fallback

    elif sistema == "Linux":
        # Linux: fallback light (GNOME/KDE differiscono)
        return "chiaro"

    else:
        raise NotImplementedError(f"Rilevamento tema non implementato per OS: {sistema}")


def load_main_stylesheet(tema: Literal["chiaro", "scuro"] | None = None) -> str:
    """Carica il QSS principale e applica il tema selezionato o rilevato automaticamente.
    
    Args:
        tema: stringa 'chiaro' o 'scuro'. Se None, rileva automaticamente il tema OS.
    
    Returns:
        QSS completo come stringa pronta per QApplication.setStyleSheet()
    
    Throws: FileNotFoundError, IOError, KeyError, ValueError
    """
    if tema is None:
        tema = rileva_tema_os()

    if tema == "chiaro":
        palette: dict[str, str] = COLORI_CHIARO
    elif tema == "scuro":
        palette: dict[str, str] = COLORI_SCURO
    else:
        raise ValueError(f"Tema non valido: {tema}. Usare 'chiaro' o 'scuro'.")

    template_qss: str = __carica_file_qss(MAIN_QSS_PATH)
    qss_finale: str = __sostituisci_placeholder_qss(template_qss, palette)
    return qss_finale
