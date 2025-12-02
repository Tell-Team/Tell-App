from PyQt6.QtCore import pyqtSignal, QObject

from model.model import Model
from view.login_page import LoginPage


class LoginController(QObject):
    navigation_go_back = pyqtSignal()  # - Da implementare
    navigation_go_to = pyqtSignal(str, bool)

    def __init__(self, model: Model, login_v: LoginPage):
        super().__init__()
        self.__model = model
        self.__login_page = login_v
        self._connect_signals()

    def _connect_signals(self):
        self.__login_page.btn_cliente.clicked.connect(  # type:ignore
            lambda: self.navigation_go_to.emit("info_section", True)
        )

        # - Il ruolo dell'utente non è ancora implementato
        self.__login_page.btn_biglietteria.clicked.connect(  # type:ignore
            lambda: self.navigation_go_to.emit("info_section", True)
        )

        # - Il ruolo dell'utente non è ancora implementato
        self.__login_page.btn_amministratore.clicked.connect(  # type:ignore
            lambda: self.navigation_go_to.emit("info_section", True)
        )

    # - Il model dovrebbe usarsi per verificare la account o enviar all'utente a una
    #   nuova page login_utente per verificare che sia un biglietteria o amministratore.
