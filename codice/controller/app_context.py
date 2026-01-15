from typing import Optional

from model.model import Model


class AppContext:
    """Classe dedicata a caricare tutto il contesto dell'app. Crea un'istanza di `Model`
    unica, carica i servizi necessari per il login e crea un `AppFlowController`, dove
    è definito il flusso dell'app da prima del login a dopo il logout.

    :raise DatoIncongruenteException: il percorso specificato per il salvataggio
    dei dati dell'applicazione non è valido (non è una cartella).
    """

    def __init__(self, db_path: Optional[str]):
        # Crea un Model unici per tutta l'app
        self.__model = Model(db_path)

        from controller.login import LoginController, AuthenticationService

        # SessionContext,

        from controller.app_flow_controller import AppFlowController

        # session = SessionContext()
        self.__auth = AuthenticationService()

        login_controller = LoginController(self.__model)

        self.__app_flow = AppFlowController(self.__model, login_controller, self.__auth)
