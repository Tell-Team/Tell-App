from typing import Optional, override

from core.controller import AbstractCUController

from controller.login.user_session import UserSession

from model.model import Model
from model.account.account import Account, Ruolo
from model.exceptions import (
    CredenzialiErrateException,
    DatoIncongruenteException,
    IdInesistenteException,
    IdOccupatoException,
    OccupatoException,
    PermessiInsufficientiException,
)

from view.account.pagine import NuovoAccountView, ModificaAccountView

from view.utils import PopupMessage


CAMPI_NECESSARI = "<b>ATTENZIONE</b>: È necessario compilare tutti i campi di input."
CREDENZIALI_ERRATE = "<b>ATTENZIONE</b>: La password originale non è corretta."


class CUAccountController(AbstractCUController):
    """Gestisce il salvataggio dgli account creati e modificati.

    Segnali
    ---
    - `goBackRequest()`: emesso per tornare alla pagina `AccountSectionView`.
    """

    _view_nuova: NuovoAccountView
    _view_modifica: ModificaAccountView

    def __init__(
        self,
        model: Model,
        n_account_v: NuovoAccountView,
        m_account_v: ModificaAccountView,
        session: UserSession,
    ):
        if type(n_account_v) is not NuovoAccountView:
            raise TypeError("Atteso NuovoAccountView per n_account_v.")
        if type(m_account_v) is not ModificaAccountView:
            raise TypeError("Atteso ModificaAccountView per m_account_v.")

        self.__user_session_id = session.id

        super().__init__(model, n_account_v, m_account_v)

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    @override
    def _connect_signals(self) -> None:
        super()._connect_signals()

        self._view_modifica.nuova_password.textChanged.connect(  # type:ignore
            self.__set_modifica_password_enabled
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __aggiungi_account(self, account: Account, agent_id: int) -> None:
        self._model.aggiungi_account(account, agent_id)

    def __set_modifica_password_enabled(self, text: str) -> None:
        self._view_modifica.set_modifica_password_enabled(bool(text))

    @override
    def _richiesta_nuovo(self) -> None:
        current_pagina = self._view_nuova

        # Ottieni l'input inserito
        username = current_pagina.username.text()
        password = current_pagina.password.text()
        password_conferma = current_pagina.conferma.text()
        ruolo: Optional[Ruolo] = current_pagina.ruolo.currentData()

        # Verifica i dati inseriti
        try:
            if password != password_conferma:
                # La nuova password è diversa dalla conferma
                raise DatoIncongruenteException(
                    "La password inserita non coincide con la sua conferma."
                )
            if ruolo is None:
                # Non è stato specificato un ruolo
                raise DatoIncongruenteException("Selezionare un ruolo.")
            nuovo_account = Account(username, password, ruolo)
        except DatoIncongruenteException as e:
            # È stato trovato un campo con input non valido
            current_pagina.mostra_msg_input_error(CAMPI_NECESSARI)
            PopupMessage.mostra_errore(
                current_pagina,
                "Input non valido",
                f"Si è verificato un errore: {e}",
            )
        else:
            current_pagina.mostra_msg_input_error("")

            try:
                self.__aggiungi_account(nuovo_account, self.__user_session_id)
            except IdInesistenteException as e:
                # Non esiste un account (agent) con quell'id
                PopupMessage.mostra_errore(
                    current_pagina,
                    "ID Account inesistente",
                    f"Si è verificato un errore: {e}",
                )
            except IdOccupatoException as e:
                # Esiste già un account con quell'id
                PopupMessage.mostra_errore(
                    current_pagina,
                    "ID Account occupato",
                    f"Si è verificato un errore: {e}",
                )
            except OccupatoException as e:
                # L'account è in uso
                PopupMessage.mostra_errore(
                    current_pagina,
                    "Account occupato",
                    f"Si è verificato un errore: {e}",
                )
            except PermessiInsufficientiException as e:
                # L'account richiedente non ha i permessi necessari
                PopupMessage.mostra_errore(
                    current_pagina,
                    "Privilegi insufficienti",
                    f"Si è verificato un errore {e}",
                )
            else:
                self.goBackRequest.emit()

    @override
    def _richiesta_modifica(self) -> None:
        current_pagina = self._view_modifica

        # Ottiene l'input inserito
        id_account = current_pagina.id_current_account
        password_new = current_pagina.nuova_password.text()
        password = current_pagina.password.text()
        ruolo: Optional[Ruolo] = current_pagina.ruolo.currentData()

        # Tenta di modificare l'account
        try:
            if password_new:
                if password_new != current_pagina.conferma.text():
                    raise DatoIncongruenteException(
                        "La nuova password non coincide con la sua conferma."
                    )
                self._model.cambia_password(
                    id_account, password, password_new, self.__user_session_id
                )
            if ruolo is None:
                # Non è stato specificato un ruolo
                raise DatoIncongruenteException("Selezionare un ruolo.")
            self._model.cambia_ruolo(id_account, ruolo, self.__user_session_id)
        except DatoIncongruenteException as e:
            # È stato trovato un campo con input non valido
            current_pagina.mostra_msg_input_error(CAMPI_NECESSARI)
            PopupMessage.mostra_errore(
                current_pagina,
                "Input non valido",
                f"Si è verificato un errore: {e}",
            )
        except CredenzialiErrateException as e:
            # La vecchia password non è corretta
            current_pagina.mostra_msg_input_error(CREDENZIALI_ERRATE)
            PopupMessage.mostra_errore(
                current_pagina,
                "Credenziali errate",
                f"Si è verificato un errore: {e}",
            )
        except PermessiInsufficientiException as e:
            # L'account richiedente non ha i permessi necessari
            PopupMessage.mostra_errore(
                current_pagina,
                "Privilegi insufficienti",
                f"Si è verificato un errore {e}",
            )
        except IdInesistenteException as e:
            # L'ID non esiste
            PopupMessage.mostra_errore(
                current_pagina,
                "ID inesistente",
                f"Si è verificato un errore {e}",
            )
        else:
            current_pagina.mostra_msg_input_error("")
            self.goBackRequest.emit()
