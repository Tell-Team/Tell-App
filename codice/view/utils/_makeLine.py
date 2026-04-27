from PyQt6.QtWidgets import QFrame


def make_vline() -> QFrame:
    """Crea una linea verticale usata per dividere widget di un Layout orizontale."""
    line = QFrame()
    line.setFrameShape(QFrame.Shape.VLine)
    line.setFrameShadow(QFrame.Shadow.Sunken)
    return line


def make_hline() -> QFrame:
    """Crea una linea orizontale per dividere widget di un Layout verticale"""
    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    return line
