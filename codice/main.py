from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from view.navigation import NavigationController
from view.styles.styles_loader import load_stylesheet

from view.info_page import InfoPage
from view.login_page import LogInPage
from view.nuova_opera import FormularioOpera
from view.account_page import AccountPage
from view.spettacoli_page import SpettacoliPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # # CONFIG FINESTRA
        self.setWindowTitle("Tell")
        self.setMinimumSize(800, 600)

        self.nav = NavigationController(self)

        # # Pagine disponibili
        login = LogInPage(self.nav)
        info = InfoPage(self.nav)
        nuova_opera = FormularioOpera(self.nav)
        account = AccountPage(self.nav)
        spettacoli = SpettacoliPage(self.nav)

        # # Registrazione delle pagine
        self.nav.add_page(LogInPage, login)
        self.nav.add_page(InfoPage, info)
        self.nav.add_page(FormularioOpera, nuova_opera)
        self.nav.add_page(AccountPage, account)
        self.nav.add_page(SpettacoliPage, spettacoli)

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
