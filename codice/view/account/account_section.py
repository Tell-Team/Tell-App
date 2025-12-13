from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt, pyqtSignal

from view.abstractView.sectionAbstract import AbstractSectionView


class AccountSectionView(AbstractSectionView):
    """
    GUI della sezione Account dell'app.

    Visualizza a schermo tutti gli account del `Model` separati secondo ruolo
    (Amministratore e Biglietteria) e permette di crearli, modificarli ed eliminarli.
    """

    request_display_admin = pyqtSignal(QVBoxLayout)
    request_display_biglietteria = pyqtSignal(QVBoxLayout)

    def __init__(self):
        super().__init__()

        self._build_ui()

    def _build_ui(self):
        # Account
        header_account = QLabel("Account")
        header_account.setObjectName("Header1")
        header_account.setAlignment(Qt.AlignmentFlag.AlignLeft)

        #
        #
        #

        # Amministratore
        header_admin = QLabel("Amministratore")
        header_admin.setObjectName("Header2")
        header_admin.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.btn_nuovo_admin = QPushButton("Nuovo Amministratore")
        self.btn_nuovo_admin.setObjectName("SmallButton")

        layout_header_admin = QHBoxLayout()
        layout_header_admin.addWidget(header_admin)
        layout_header_admin.addWidget(self.btn_nuovo_admin)
        layout_header_admin.addStretch()

        # Si usa 'admin' nei nomi delle variabili e 'amministratore' nei testi della UI.
        self.layout_lista_admin = QVBoxLayout()

        # - Non è necessario, per in pratica non vedrà mai. Comunque lo lascio in caso serva.
        self.label_lista_admin_vuota = QLabel(
            "Non vi sono account Amministratore registrati."
        )
        self.label_lista_admin_vuota.setObjectName("SubHeader")
        self.label_lista_admin_vuota.hide()

        self.request_display_admin.emit(self.layout_lista_admin)

        container_admin = QWidget()
        layout_admin = QVBoxLayout(container_admin)
        layout_admin.addLayout(layout_header_admin)
        layout_admin.addLayout(self.layout_lista_admin)

        #
        #
        #

        # Biglietteria
        header_biglietteria = QLabel("Biglietteria")
        header_biglietteria.setObjectName("Header2")
        header_biglietteria.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.btn_nuovo_biglietteria = QPushButton("Nuova Biglietteria")
        self.btn_nuovo_biglietteria.setObjectName("SmallButton")

        layout_header_biglietteria = QHBoxLayout()
        layout_header_biglietteria.addWidget(header_biglietteria)
        layout_header_biglietteria.addWidget(self.btn_nuovo_biglietteria)
        layout_header_biglietteria.addStretch()

        # Sempre viene usata 'biglietteria' in singolare per le variabili.
        self.layout_lista_biglietteria = QVBoxLayout()

        self.label_lista_biglietteria_vuota = QLabel(
            "Non vi sono account Biglietteria registrati."
        )
        self.label_lista_biglietteria_vuota.setObjectName("SubHeader")
        self.label_lista_biglietteria_vuota.hide()

        self.request_display_biglietteria.emit(self.layout_lista_biglietteria)

        container_biglietteria = QWidget()
        layout_biglietterie = QVBoxLayout(container_biglietteria)
        layout_biglietterie.addLayout(layout_header_biglietteria)
        layout_biglietterie.addLayout(self.layout_lista_biglietteria)

        #
        #
        #

        # Scroll layout
        self.scroll_layout.addWidget(header_account)
        self.scroll_layout.addWidget(container_admin)
        self.scroll_layout.addWidget(container_biglietteria)
        self.scroll_layout.addStretch()

    def refresh_page(self):
        self.clear_layout(self.layout_lista_admin)
        self.layout_lista_admin.addWidget(self.label_lista_admin_vuota)
        self.label_lista_admin_vuota.hide()
        self.request_display_admin.emit(self.layout_lista_admin)

        self.clear_layout(self.layout_lista_biglietteria)
        self.layout_lista_biglietteria.addWidget(self.label_lista_biglietteria_vuota)
        self.label_lista_biglietteria_vuota.hide()
        self.request_display_biglietteria.emit(self.layout_lista_biglietteria)


# - QUESTE FUNZIONE DOVREBBERO ANDAR BENE NEL CONTROLLER
# - SONO I display_admin() E display_biglietteria()
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
#     username.setObjectName("Header3")
#     username.setAlignment(Qt.AlignmentFlag.AlignLeft)

#     # ### Pulsanti
#     btn_modifica = QPushButton("Modifica")
#     btn_modifica.setObjectName("SmallButton")
#     btn_modifica.clicked.connect(  # type:ignore
#         partial(
#             AccountController.modifica_account, gestore_account, admin.get_id()
#         )
#     )

#     btn_elimina = QPushButton("Rimuovi")
#     btn_elimina.setObjectName("SmallButton")
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
#     username.setObjectName("Header3")
#     username.setAlignment(Qt.AlignmentFlag.AlignLeft)

#     # ### Pulsanti
#     btn_modifica = QPushButton("Modifica")
#     btn_modifica.setObjectName("SmallButton")
#     btn_modifica.clicked.connect(  # type:ignore
#         partial(
#             AccountController.modifica_account,
#             gestore_account,
#             biglietteria.get_id(),
#         )
#     )

#     btn_elimina = QPushButton("Rimuovi")
#     btn_elimina.setObjectName("SmallButton")
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
