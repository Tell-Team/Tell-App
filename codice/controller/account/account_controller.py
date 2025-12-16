class AccountController:
    pass


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
