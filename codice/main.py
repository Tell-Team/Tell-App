from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from controller.context import AppContext

from view.login_page import LogInPage
from view.info.info_page import InfoPage
from view.styles.styles_loader import load_stylesheet

# from view.account.account_page import AccountPage <- INCOMPLETO
# from view.spettacoli.spettacoli_page import SpettacoliPage <- INCOMPLETO


# Con `# -` ho segnato le annotazione sui dettagli a modificare
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # # Set Controller principale (model, nav e controller inclusi)
        self.context = AppContext(self)

        # # Set Controllers
        self.info_controller = self.context.info_controller

        # # CONFIG FINESTRA
        self.setWindowTitle("Tell")
        self.setMinimumSize(800, 600)

        # # Pagine disponibili
        self.login = LogInPage(
            self.context
        )  # - Magari posso usare un controller nuovo o semplicemente model e nav come parametri
        self.info = InfoPage(self.info_controller)
        from view.info.modifica_opera import (
            FormModificaOpera,
            FormNuovaOpera,
        )
        from view.info.visualizza_opera import VisualizzaOpera

        self.nuova_opera = FormNuovaOpera(self.info_controller)
        self.modifica_opera = FormModificaOpera(self.info_controller)
        self.visualizza_opera = VisualizzaOpera(self.info_controller)
        from view.info.modifica_regia import (
            FormModificaRegia,
            FormNuovaRegia,
        )

        self.nuova_regia = FormNuovaRegia(self.info_controller)
        self.modifica_regia = FormModificaRegia(self.info_controller)
        from view.info.modifica_genere import (
            FormModificaGenere,
            FormNuovoGenere,
        )

        self.nuovo_genere = FormNuovoGenere(self.info_controller)
        self.modifica_genere = FormModificaGenere(self.info_controller)

        # self.account = AccountPage(self.context) <- Non sono acora finiti
        # self.spettacoli = SpettacoliPage(self.context) <- alt: (self.model, self.nav)

        """ 
        Per testare le singole pagine, basta registrare la pagina desiderata
        in self.context.nav prima di tutte le altre. (login è la prima pagina
        registrata, quindi diventa la prima pagina visualizzata.)
        """
        # # Registrazione delle pagine
        self.context.nav.add_page("login", self.login)
        self.context.nav.add_page("info", self.info)
        self.context.nav.add_page("nuova_opera", self.nuova_opera)
        self.context.nav.add_page("modifica_opera", self.modifica_opera)
        self.context.nav.add_page("visualizza_opera", self.visualizza_opera)
        self.context.nav.add_page("nuova_regia", self.nuova_regia)
        self.context.nav.add_page("modifica_regia", self.modifica_regia)
        self.context.nav.add_page("nuovo_genere", self.nuovo_genere)
        self.context.nav.add_page("modifica_genere", self.modifica_genere)
        # self.context.nav.add_page("account", self.account)
        # self.context.nav.add_page("spettacoli", self.spettacoli)

        # # Layout principale
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.addWidget(self.context.nav.get_stack())
        self.setCentralWidget(central)


if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet(load_stylesheet("view/styles/main.qss"))

    window = MainWindow()
    window.show()
    app.exec()
