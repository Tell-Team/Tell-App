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


class PermessiInsufficientiException(Exception):
    """L'utente corrente non ha permessi sufficienti per compiere l'azione."""

    pass


class AccountInesistenteException(Exception):
    """L'account richiesto non è presente in memoria."""

    pass


class CredenzialiErrateException(Exception):
    """Le credenziali fornite sono errate."""

    pass


class OccupatoException(Exception):
    """Il valore o la combinazione di valori forniti è già in uso da parte di un altro oggetto"""

    pass
