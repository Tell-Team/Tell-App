from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt6.QtCore import Qt, pyqtSignal
from typing import override

from core.view import AbstractVisualizzaView

from controller.login.user_session import UserSession

from model.pianificazione.regia import Regia

from view.info.utils import OperaData

from view.utils.list_widgets import ListLayout, EmptyStateLabel
from view.utils.hyphenate_text import HyphenatedLabel
from view.utils.custom_button import DefaultButton
from view.utils import make_vline

from view.style.ui_style import WidgetRole, WidgetColor


class VisualizzaOperaView(AbstractVisualizzaView):
    """Pagina per visualizzare le singole `Opera` in dettaglio.

    Contiene le tutte informazioni dell'`Opera` ed una lista con tutte le `Regia`
    associate ad essa.

    Segnali
    ---
    - `displayRegieRequest(ListLayout)`: emesso per mostrare a schermo la lista regie;
    - `nuovaRegiaRequest()`: emesso quando si clicca il pulsante Nuova regia.
    """

    displayRegieRequest = pyqtSignal(ListLayout)
    nuovaRegiaRequest = pyqtSignal()

    def __init__(self, user_session: UserSession):
        self.is_admin = user_session.ha_permessi_admin()
        self.id_current_opera: int = -1

        super().__init__()

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        # Labels
        self.label_nome = HyphenatedLabel("[Nome Opera]")
        self.label_nome.setProperty(WidgetRole.Label.HEADER1, True)
        self.label_nome.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.label_librettista = HyphenatedLabel("Libretto di [Librettista Opera].")
        self.label_librettista.setProperty(WidgetRole.Label.BODY_TEXT, True)
        self.label_librettista.setProperty(WidgetColor.Label.PRIMARY_COLOR, True)

        self.label_compositore = HyphenatedLabel(
            "Musica composta da [Compositore Opera]."
        )
        self.label_compositore.setProperty(WidgetRole.Label.BODY_TEXT, True)
        self.label_compositore.setProperty(WidgetColor.Label.PRIMARY_COLOR, True)

        self.label_genere = HyphenatedLabel(f"Genere: [Genere Opera]")
        self.label_genere.setProperty(WidgetRole.Label.BODY_TEXT, True)
        self.label_genere.setProperty(WidgetColor.Label.PRIMARY_COLOR, True)

        self.label_atti = QLabel(f"Numero di atti: [Atti Opera]")
        self.label_atti.setProperty(WidgetRole.Label.BODY_TEXT, True)
        self.label_atti.setProperty(WidgetColor.Label.PRIMARY_COLOR, True)

        self.label_prima_rappresentazione = HyphenatedLabel(
            f"È stata rappresentata per prima volta il [Data Opera] nel teatro [Teatro Opera]."
        )
        self.label_prima_rappresentazione.setProperty(WidgetRole.Label.BODY_TEXT, True)
        self.label_prima_rappresentazione.setProperty(
            WidgetColor.Label.PRIMARY_COLOR, True
        )

        self.label_trama = HyphenatedLabel("[Trama Opera]")
        self.label_trama.setProperty(WidgetRole.Label.BODY_TEXT, True)
        self.label_trama.setProperty(WidgetColor.Label.PRIMARY_COLOR, True)

        # Lista Regie
        label_lista_regie = QLabel("Lista regie")
        label_lista_regie.setProperty(WidgetRole.Label.HEADER2, True)

        header_regie = QWidget()
        self.layout_header_regie = QHBoxLayout(header_regie)
        self.layout_header_regie.setContentsMargins(0, 0, 0, 0)
        self.layout_header_regie.addWidget(label_lista_regie)

        if self.is_admin:
            self.__btn_nuova_regia = DefaultButton("Nuova regia")
            self.layout_header_regie.addWidget(self.__btn_nuova_regia)

        self.layout_header_regie.addStretch()

        self.lista_regie: list[Regia] = []

        label_lista_regie_vuota = EmptyStateLabel(
            "Al momento, non vi sono regie per questa opera."
        )
        label_lista_regie_vuota.setProperty(WidgetRole.Label.BODY_TEXT, True)
        label_lista_regie_vuota.setProperty(WidgetColor.Label.SECONDARY_COLOR, True)

        content_lista_regie = QWidget()
        content_lista_regie.setProperty(WidgetRole.Item.LIST, True)
        self.layout_lista_regie = ListLayout(
            content_lista_regie, label_lista_regie_vuota
        )

        # header_titolo = QLabel("Titolo")
        # header_titolo.setProperty(WidgetRole.HEADER3, True)
        header_regista = QLabel("Regista")
        header_regista.setProperty(WidgetRole.Label.HEADER3, True)
        header_opzioni = QLabel("Opzioni")
        header_opzioni.setProperty(WidgetRole.Label.HEADER3, True)

        header_lista_regie = QWidget()
        layout_header_lista_regie = QGridLayout(header_lista_regie)
        layout_header_lista_regie.setContentsMargins(1, 1, 1, 1)
        # layout_header_lista_regie.addWidget(
        #     header_titolo, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter
        # )
        # layout_header_lista_regie.addWidget(make_vline(), 0, 1)
        layout_header_lista_regie.addWidget(
            header_regista, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter
        )
        if self.is_admin:
            layout_header_lista_regie.addWidget(make_vline(), 0, 1)
            layout_header_lista_regie.addWidget(
                header_opzioni, 0, 2, alignment=Qt.AlignmentFlag.AlignCenter
            )

        self.regie = QWidget()
        self.layout_regie = QVBoxLayout(self.regie)
        self.layout_regie.addWidget(header_regie)
        self.layout_regie.addWidget(header_lista_regie)
        self.layout_regie.addWidget(content_lista_regie)
        # end-Lista Regie

        # Layout
        self._layout_content.addWidget(self.label_nome)
        self._layout_content.addWidget(self.label_librettista)
        self._layout_content.addWidget(self.label_compositore)
        self._layout_content.addWidget(self.label_genere)
        self._layout_content.addWidget(self.label_atti)
        self._layout_content.addWidget(self.label_prima_rappresentazione)
        self._layout_content.addWidget(self.label_trama)
        self._layout_content.addWidget(self.regie)
        self._layout_content.addStretch()

    @override
    def _connect_signals(self) -> None:
        super()._connect_signals()

        if self.is_admin:
            self.__btn_nuova_regia.clicked.connect(  # type:ignore
                self.nuovaRegiaRequest.emit
            )

    # ------------------------- METODI DI VIEW -------------------------

    @override
    def set_data(  # type: ignore[override]
        self, data: OperaData, genere_nome: str, lista_regie: list[Regia]
    ) -> None:
        """Carica i dati dell'opera nella pagina.

        :param data: data salvata in una classe immutabile
        :param genere_nome: nome del genere scelto per l'opera
        :param lista_regie: lista delle regie associate all'opera"""
        # Reset layout lista regie
        self.layout_lista_regie.svuota_layout()

        # Salva dati dell'opera nella pagina
        self.id_current_opera = data.id
        self.lista_regie = lista_regie

        # Carica dati dell'opera
        self.label_nome.setText(f"{data.nome}")
        self.label_librettista.setText(f"Libretto di {data.librettista}")
        self.label_compositore.setText(f"Musica composta da {data.compositore}")
        self.label_genere.setText(f"Genere: {genere_nome}")
        self.label_atti.setText(f"Numero di atti: {data.atti}")
        self.label_prima_rappresentazione.setText(
            "È stata rappresentata per prima volta il "
            + f"{data.data_rappresentazione.strftime("%d/%m/%Y")} "
            + f"nel teatro {data.teatro_rappresentazione}"
        )
        self.label_trama.setText(f"{data.trama}")

        # Carica lista regie
        if not self.lista_regie:
            self.layout_lista_regie.mostra_msg_lista_vuota()
        else:
            self.displayRegieRequest.emit(self.layout_lista_regie)

    @override
    def aggiorna_pagina(self) -> None:
        super().aggiorna_pagina()

        self.layout_lista_regie.svuota_layout()
        self.displayRegieRequest.emit(self.layout_lista_regie)
