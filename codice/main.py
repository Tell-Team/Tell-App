from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from model.model import Model
from controller.navigation import NavigationController
from view.styles.styles_loader import load_stylesheet

from view.login_page import LogInPage
from view.info.info_page import InfoPage
from view.account.account_page import AccountPage
from view.spettacoli.spettacoli_page import SpettacoliPage


# Con `# -` ho segnato le annotazione sopra dettagli a modificare
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # # Carica model
        self.model = Model()

        # # CONFIG FINESTRA
        self.setWindowTitle("Tell")
        self.setMinimumSize(800, 600)

        self.nav = NavigationController(self)

        # # Pagine disponibili
        self.login = LogInPage(self.model, self.nav)
        self.info = InfoPage(self.model, self.nav)
        from view.info.modifica_opera import (
            FormularioModificaOpera,
            FormularioNuovaOpera,
        )
        from view.info.visualizza_opera import VisualizzaOpera

        self.nuova_opera = FormularioNuovaOpera(self.model, self.nav)
        self.modifica_opera = FormularioModificaOpera(self.model, self.nav)
        self.visualizza_opera = VisualizzaOpera(self.model, self.nav)
        from view.info.modifica_regia import (
            FormularioModificaRegia,
            FormularioNuovaRegia,
        )

        self.nuova_regia = FormularioNuovaRegia(self.model, self.nav)
        self.modifica_regia = FormularioModificaRegia(self.model, self.nav)
        from view.info.modifica_genere import (
            FormularioModificaGenere,
            FormularioNuovoGenere,
        )

        self.nuovo_genere = FormularioNuovoGenere(self.model, self.nav)
        self.modifica_genere = FormularioModificaGenere(self.model, self.nav)
        self.account = AccountPage(self.model, self.nav)
        self.spettacoli = SpettacoliPage(self.model, self.nav)

        # # Registrazione delle pagine
        self.nav.add_page("login", self.login)
        self.nav.add_page("info", self.info)
        self.nav.add_page("nuova_opera", self.nuova_opera)
        self.nav.add_page("modifica_opera", self.modifica_opera)
        self.nav.add_page("visualizza_opera", self.visualizza_opera)
        self.nav.add_page("nuova_regia", self.nuova_regia)
        self.nav.add_page("modifica_regia", self.modifica_regia)
        self.nav.add_page("nuovo_genere", self.nuovo_genere)
        self.nav.add_page("modifica_genere", self.modifica_genere)
        self.nav.add_page("account", self.account)
        self.nav.add_page("spettacoli", self.spettacoli)

        # # Layout principale
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.addWidget(self.nav.get_stack())
        self.setCentralWidget(central)


if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet(load_stylesheet("view/styles/main.qss"))

    window = MainWindow()
    window.show()
    app.exec()


# no se quiso ejercutar el programa no sé por qué coño
# ESTUDIAR POSIBLES EXCEPCIONES
