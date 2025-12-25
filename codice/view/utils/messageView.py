# Metodi condivisi tra diverse pagine della view e controller.

from PyQt6.QtWidgets import QWidget, QMessageBox


class MessageView:
    """View dedicata alla visualizzazione di popup."""

    # Se servono altri tipi di popup, basta aggiungere un metodo nuovo alla classe.

    @staticmethod
    def mostra_errore(parent: QWidget, titolo: str, testo: str) -> None:
        """Mostra un messaggio di errore all'utente.

        :param widget: parent widget delle finestra di errore
        :param titolo: titolo della finestra di errore
        :param testo: testo descrittivo
        """
        QMessageBox.critical(parent, titolo, testo)
