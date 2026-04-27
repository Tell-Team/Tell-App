from PyQt6.QtWidgets import QWidget, QMessageBox


def mostra_error_popup(parent: QWidget, titolo: str, testo: str) -> None:
    """Mostra un messaggio di errore all'utente.

    :param widget: parent widget delle finestra di errore
    :param titolo: titolo della finestra di errore
    :param testo: testo descrittivo
    """
    QMessageBox.critical(parent, titolo, "Si è verificato un erorre: " + testo)
