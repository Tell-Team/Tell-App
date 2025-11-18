from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from navigation import NavigationController
from ui.styles.styles_loader import load_stylesheet

from ui.info import InfoPage
from ui.login import LogInPage
from ui.nuova_opera import FormularioOpera


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # CONFIG FINESTRA
        self.setWindowTitle("Tell-project")
        self.setMinimumSize(800, 600)

        self.nav = NavigationController(self)

        # Pagine disponibili
        login = LogInPage(self.nav)
        info = InfoPage(self.nav)
        nuova_opera = FormularioOpera(self.nav)

        # Registrazione delle pagine
        self.nav.add_page(LogInPage, login)
        self.nav.add_page(InfoPage, info)
        self.nav.add_page(FormularioOpera, nuova_opera)

        # Layout principale
        central = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.nav.stack)
        central.setLayout(layout)
        self.setCentralWidget(central)


if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet(load_stylesheet("ui/styles/main.qss"))

    window = MainWindow()
    window.show()
    app.exec()


# no se quiso ejercutar el programa no sé por qué coño

# ESTUDIAR POSIBLES EXCEPCIONES
