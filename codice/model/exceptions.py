class DatoIncongruenteException(Exception):
    """Il valore fornito non rispetta il formato atteso."""

    pass


class IdInesistenteException(Exception):
    """Non è presente nessun oggetto in memoria con l'id fornito."""

    pass


class IdOccupatoException(Exception):
    """L'id fornito è già assegnato ad un altro oggetto in memoria."""

    pass


class OggettoInUsoException(Exception):
    """L'oggetto fornito è collegato ad altri oggetti in memoria."""

    pass
