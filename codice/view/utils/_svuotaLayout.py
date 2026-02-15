from PyQt6.QtWidgets import QLayout


def svuota_layout_generico(layout: QLayout, keep: int = 0) -> None:
    """Rimuove tutti gli item da un QLayout eccetto i primi `keep` item.

    :param layout: `QLayout` da svuotare
    :param keep: numero di item da lasciare intatti (i primi item)"""
    if keep < 0:
        raise ValueError(f"keep can't be negative")

    for i in reversed(range(keep, layout.count())):
        item = layout.takeAt(i)
        if not item:
            continue  # Safety check
        if widget := item.widget():
            widget.setParent(None)
            widget.deleteLater()
        elif child_layout := item.layout():
            svuota_layout_generico(child_layout)
