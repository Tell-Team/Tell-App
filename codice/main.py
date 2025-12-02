from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout

from controller.context import AppContext

from view.styles.styles_loader import load_stylesheet


# Con `# -` ho segnato le annotazione sui dettagli a modificare
class MainWindowView(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Controller principale (model, nav e controller inclusi)
        self.context = AppContext(self)

        # Config. finestra
        self.setWindowTitle("Tell")
        self.setMinimumSize(800, 600)

        """ 
        Per testare le singole pagine, basta registrare la pagina desiderata
        in self.context.nav prima di tutte le altre. (login_page è la prima pagina
        registrata, quindi diventa la prima pagina visualizzata.)
        """
        # Registrazione delle pagine
        self.context.nav.add_page("login_page", self.context.login_page)
        self.context.nav.add_page("info_section", self.context.info_section)
        self.context.nav.add_page("nuova_opera", self.context.nuova_opera_view)
        self.context.nav.add_page("modifica_opera", self.context.modifica_opera_view)
        self.context.nav.add_page(
            "visualizza_opera", self.context.visualizza_opera_view
        )
        self.context.nav.add_page("nuovo_genere", self.context.nuovo_genere_view)
        self.context.nav.add_page("modifica_genere", self.context.modifica_genere_view)
        # self.context.nav.add_page("account_section", self.context.account_section)
        # self.context.nav.add_page("spettacoli_section", self.context.spettacoli_section)

        # Layout
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.addWidget(self.context.nav.get_stack())
        self.setCentralWidget(central)


if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet(load_stylesheet("view/styles/main.qss"))

    window = MainWindowView()
    window.show()
    app.exec()
