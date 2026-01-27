from core.controller import AbstractCUController

from controller.login.user_session import UserSession

from model.exceptions import (
    CredenzialiErrateException,
    DatoIncongruenteException,
    IdInesistenteException,
    IdOccupatoException,
    OccupatoException,
    PermessiInsufficientiException,
)
from model.model import Model
from model.account.account import Account

from view.account.pagine import NuovoAccountView, ModificaAccountView

from typing import Optional, override

from view.utils.popupView import PopupMessage


class CUAccountController(AbstractCUController):
    """Gestisce il salvataggio dgli account creati e modificati.

    Segnali
    ---
    - `goBackRequest()`: emesso per tornare alla pagina `AccountSectionView`.
    """

    __user_session_id: int

    def __init__(
        self,
        model: Model,
        n_account_v: NuovoAccountView,
        m_account_v: ModificaAccountView,
        session: UserSession,
    ):
        self.__user_session_id = session.id

        if type(n_account_v) is not NuovoAccountView:
            raise TypeError("Atteso NuovoAccountView per n_account_v.")

        if type(m_account_v) is not ModificaAccountView:
            raise TypeError("Atteso ModificaAccountView per m_account_v.")

        super().__init__(model, n_account_v, m_account_v)

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __get_account(self, id_: int) -> Optional[Account]:
        return self._model.get_account(id_)

    def __aggiungi_account(self, account: Account, agent_id: int) -> None:
        self._model.aggiungi_account(account, agent_id)

    def __modifica_account(self, account: Account) -> None: ...

    @override
    def _inizia_salvataggio(self, is_new: bool = True) -> None:
        """Salva l'account creato o modificato nel GestoreAccount

        :param is_new: verifica se si deve creare una account da zero o modificarne uno già esistente
        """

        CAMPI_NECESSARI = (
            "<b>ATTENZIONE</b>: È necessario compilare tutti i campi di input."
        )

        if is_new:
            # Ottieni la pagina NuovoAccountView
            current_pagina: NuovoAccountView = self._view_nuova  # type: ignore

            # Ottieni l'input inserito
            username = current_pagina.username.text()
            password = current_pagina.password.text()
            password_conferma = current_pagina.conferma.text()
            ruolo = current_pagina.ruolo.currentData()

            # Verifica i dati inseriti
            try:
                if password != password_conferma:
                    # La nuova password è diversa dalla conferma
                    raise DatoIncongruenteException(
                        "La password inserita non coincide con la sua conferma."
                    )
                if ruolo == None:
                    # Non è stato specificato un ruolo
                    raise DatoIncongruenteException("Selezionare un ruolo.")

                nuovo_account = Account(username, password, ruolo)

            except DatoIncongruenteException as e:
                # È stato trovato un campo con input non valido
                current_pagina.show_input_error(CAMPI_NECESSARI)
                PopupMessage.mostra_errore(
                    current_pagina,
                    "Input non valido",
                    f"{e}",
                )

            else:
                current_pagina.show_input_error("")

                # Tenta di creare il nuovo account
                try:
                    nuovo_account = Account(username, password, ruolo)
                except DatoIncongruenteException as e:
                    # È stato trovato un campo con input non valido
                    current_pagina.show_input_error(CAMPI_NECESSARI)
                    PopupMessage.mostra_errore(
                        current_pagina,
                        "Input non valido",
                        f"Si è verificato un errore: {e}",
                    )
                else:
                    current_pagina.show_input_error("")

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
        elif not is_new:
            current_pagina: ModificaAccountView = self._view_modifica  # type: ignore

            # Crea una copia dell'account originale
            copia_account = self.__get_account(current_pagina.id_current_account)
            if not isinstance(copia_account, Account):
                PopupMessage.mostra_errore(
                    # Non esiste account con l'id salvato nella pagina
                    current_pagina,
                    "Errore nel salvataggio",
                    f"Non è presente nessun account con id {current_pagina.id_current_account}. "
                    + "Impossibile effettuare le modifiche.",
                )
                return

            # Ottiene l'input inserito
            id_account = current_pagina.id_current_account
            username = current_pagina.username.text()
            password = current_pagina.password.text()
            password_new = current_pagina.nuova_password.text()
            password_conferma = current_pagina.conferma.text()
            ruolo = current_pagina.ruolo.currentData()

            if password_new != password_conferma:
                PopupMessage.mostra_errore(
                    current_pagina,
                    "Impossibile modificare la password ",
                    f"La nuova password non coincide con la sua conferma",
                )
            else:
                # Tenta di modificare l'account
                try:
                    copia_account.set_username(username)
                    if password_new:
                        self._model.cambia_password(id_account, password, password_new)
                        self._model.cambia_ruolo(id_account, ruolo, UserSession.id)

                except DatoIncongruenteException as e:
                    # È stato trovato un campo con input non valido
                    current_pagina.show_input_error(CAMPI_NECESSARI)
                    PopupMessage.mostra_errore(
                        current_pagina,
                        "Input non valido",
                        f"Si è verificato un errore: {e}",
                    )

                except CredenzialiErrateException as e:
                    # La vecchia password non è corretta
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

                else:
                    current_pagina.show_input_error("")

                    try:
                        self.__modifica_account(copia_account)
                    except IdInesistenteException as e:
                        # Non esiste un account con quell'id
                        PopupMessage.mostra_errore(
                            current_pagina,
                            "ID Account inesistente",
                            f"Si è verificato un errore: {e}",
                        )
                    else:
                        self.goBackRequest.emit()
