from PyQt6.QtWidgets import QFrame


def make_vline() -> QFrame:
    """Crea una linea verticale usata per dividere celle di un QGridLayout."""
    line = QFrame()
    line.setFrameShape(QFrame.Shape.VLine)
    line.setFrameShadow(QFrame.Shadow.Sunken)
    return line
