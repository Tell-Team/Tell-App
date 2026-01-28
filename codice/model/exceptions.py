class DatoIncongruenteException(Exception):
    """Il valore fornito non rispetta il formato atteso."""

    pass


class AzioneIncongruenteException(Exception):
    """L'azione richiesta non può essere effettuata allo stato corrente."""

    pass


class IdInesistenteException(Exception):
    """Non è presente nessun oggetto con l'id fornito."""

    pass


class IdOccupatoException(Exception):
    """L'id fornito è già assegnato ad un altro oggetto."""

    pass


class OccupatoException(Exception):
    """Il valore o la combinazione di valori forniti è già in uso da parte di un altro oggetto."""

    pass


class OggettoInUsoException(Exception):
    """L'oggetto fornito è collegato ad altri oggetti."""

    pass


class PermessiInsufficientiException(Exception):
    """L'utente corrente non ha permessi sufficienti per compiere l'azione."""

    pass


class CredenzialiErrateException(Exception):
    """Le credenziali fornite sono errate."""

    pass
