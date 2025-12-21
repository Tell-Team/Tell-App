from PyQt6.QtCore import pyqtSignal, QObject
from functools import partial

from model.model import Model

from view.account.pagine.account_section import AccountSectionView
from view.messageView import MessageView


class AccountController(QObject):
    """Gestice la sezione Account (`AccountSectionView`) dell'app.

    Segnali:
    - logoutRequest(): emesso per eseguire la funzione di logout dall`AppContext`;
    - goToPageRequest(str, bool): emesso per visualizzare un'altra pagina;
    - goToSectionRequest(str): emesso per visualizzare un'altra pagina, senza salvarla
    nell'history del `NavigationController`;
    - getNavPageRequest(str, dict): emesso per ottenere la pagina che vendrà visualizzata.
    """

    logoutRequest = pyqtSignal()
    goToPageRequest = pyqtSignal(str, bool)
    goToSectionRequest = pyqtSignal(str)
    getNavPageRequest = pyqtSignal(str, dict)

    def __init__(
        self,
        model: Model,
        account_s: AccountSectionView,
        message_v: MessageView,
    ) -> None:
        super().__init__()
        self.__model = model
        self.__account_section = account_s  # Sezione Account
        self.__message_view = message_v  # View dedicata ai popup

        self._connect_signals()

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    def _connect_signals(self) -> None:
        # Logout
        self.__account_section.logoutRequest.connect(  # type:ignore
            self.logoutRequest.emit  # - CORRIGGERE: Account ancora non implementato
        )
        # Visualizza Sezione Spettacoli
        self.__account_section.goToSpettacoli.connect(  # type:ignore
            partial(self.goToSectionRequest.emit, "spettacoli_section")
        )
        # Visualizza Sezione Info
        self.__account_section.goToInfo.connect(  # type:ignore
            partial(self.goToSectionRequest.emit, "info_section")
        )

        # Display della Lista Account
        self.__account_section.displayAdminRequest.connect(  # type:ignore
            partial(self.display_account, "amministratore")  # - Ruolo non implementato
        )

        # Setup della pagina di creazione di account
        self.__account_section.nuovoAdminRequest.connect(  # type:ignore
            partial(self.nuovo_account, "amministratore")  # - Ruolo non implementato
        )

        # Display della Lista Account
        self.__account_section.displayBiglietteriaRequest.connect(  # type:ignore
            partial(self.display_account, "biglietteria")  # - Ruolo non implementato
        )

        # Setup della pagina di creazione di account
        self.__account_section.nuovoBiglietteriaRequest.connect(  # type:ignore
            partial(self.nuovo_account, "biglietteria")  # - Ruolo non implementato
        )

    # ------------------------- METODI PUBBLICI -------------------------

    def display_account(self, ruolo: str) -> None:  # - Ruolo non implementato
        ...

    def nuovo_account(self, ruolo: str) -> None:  # - Ruolo non implementato
        ...

    def modifica_account(self, id_: int) -> None:  # - Account non implementato
        ...


# - QUESTE FUNZIONE DOVREBBERO ANDAR BENE NEL CONTROLLER (DOPO ADATTARLI OVVIAMENTE)
# - SONO I display_admin() E display_biglietteria()
# - EQUIVALENTI A display_opera() E display_genere() DELL'InfoController

# Questi metodi gli avevo scritto quando la view ed i controller stavano scritti insieme.
# ## ADMIN DISPLAY
# lista_admin = QWidget()
# layout_lista_admin = QVBoxLayout(lista_admin)
# for admin in (
#     a
#     for a in model.get_lista_account()
#     if a.get_ruolo() == Ruolo.AMMINISTRATORE
# ):
#     # ### Labels
#     username = QLabel(f"{admin.get_username()}")
#     username.setObjectName("header3")
#     username.setAlignment(Qt.AlignmentFlag.AlignLeft)

#     # ### Pulsanti
#     btn_modifica = QPushButton("Modifica")
#     btn_modifica.setObjectName("whiteButton")
#     btn_modifica.clicked.connect(  # type:ignore
#         partial(
#             AccountController.modifica_account, gestore_account, admin.get_id()
#         )
#     )

#     btn_elimina = QPushButton("Rimuovi")
#     btn_elimina.setObjectName("whiteButton")
#     btn_elimina.clicked.connect(  # type:ignore
#         partial(
#             AccountController.elimina_account, gestore_account, admin.get_id()
#         )
#     )

#     pulsanti = QWidget()
#     temp_layout_btn = QHBoxLayout(pulsanti)
#     temp_layout_btn.addWidget(btn_modifica)
#     temp_layout_btn.addStretch()

#     # ### Layout
#     current_admin = QWidget()
#     layout_cur_admin = QHBoxLayout(current_admin)

#     layout_cur_admin.addWidget(username)
#     layout_cur_admin.addWidget(pulsanti)

#     layout_lista_admin.addWidget(current_admin)

# ## BIGLIETTERIE DISPLAY
# lista_biglietterie = QWidget()
# layout_lista_biglietterie = QVBoxLayout(lista_biglietterie)
# for biglietteria in (
#     b for b in model.get_lista_account() if b.get_ruolo() == Ruolo.BIGLIETTERIA
# ):
#     # ### Labels
#     username = QLabel(f"{biglietteria.get_username()}")
#     username.setObjectName("header3")
#     username.setAlignment(Qt.AlignmentFlag.AlignLeft)

#     # ### Pulsanti
#     btn_modifica = QPushButton("Modifica")
#     btn_modifica.setObjectName("whiteButton")
#     btn_modifica.clicked.connect(  # type:ignore
#         partial(
#             AccountController.modifica_account,
#             gestore_account,
#             biglietteria.get_id(),
#         )
#     )

#     btn_elimina = QPushButton("Rimuovi")
#     btn_elimina.setObjectName("whiteButton")
#     btn_elimina.clicked.connect(  # type:ignore
#         partial(
#             AccountController.elimina_account,
#             gestore_account,
#             biglietteria.get_id(),
#         )
#     )

#     pulsanti = QWidget()
#     temp_layout_btn = QHBoxLayout(pulsanti)
#     temp_layout_btn.addWidget(btn_modifica)
#     temp_layout_btn.addStretch()

#     # ### Layout
#     current_biglietteria = QWidget()
#     layout_cur_biglietteria = QHBoxLayout(current_biglietteria)

#     layout_cur_biglietteria.addWidget(username)
#     layout_cur_biglietteria.addWidget(pulsanti)

#     layout_lista_biglietterie.addWidget(current_biglietteria)
