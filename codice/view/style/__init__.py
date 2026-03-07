"""
Contiene le risorse (stili `qss` e iconi) dell'app, compilate nel modulo `resources_rc`,
e funzioni per applicarli nell'istanza `QApplication`.

- rileva_tema_os: Verifica se l'OS sta usando il tema chiaro o scuro, e ritorna una string.
- build_qpalette: Crea una `QPalette` pasando il tema dell'OS.
- load_stylesheet: Carica lo stylesheet come una string per applicarlo con `setStyleSheet` all'istanza `QApplication`.
"""

from .resources import resources_rc
from ._styleLoader import rileva_tema_os, build_qpalette, load_stylesheet

__all__ = ["resources_rc", "rileva_tema_os", "build_qpalette", "load_stylesheet"]
