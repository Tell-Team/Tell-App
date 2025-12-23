# - Dovrei togliere questo file dalla view? Viene anche usato dai controller.
from abc import ABCMeta
from PyQt6.QtCore import QObject


class ABCQObjectMeta(ABCMeta, type(QObject)):
    """Metaclasse necessaria per la creazione di sottoclassi di QObject astratte."""

    pass
