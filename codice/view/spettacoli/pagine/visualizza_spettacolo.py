from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt6.QtCore import Qt, pyqtSignal
from typing import override

from core.view import AbstractVisualizzaView

from controller.login.user_session import UserSession

from model.organizzazione.evento import Evento

from view.spettacoli.utils import SpettacoloData
from view.info.utils import RegiaData

from view.utils.list_widgets import ListLayout, EmptyStateLabel
from view.utils.hyphenate_text import HyphenatedLabel
from view.utils.custom_button import DefaultButton
from view.utils import make_vline, make_hline, svuota_layout_generico

from view.style.ui_style import WidgetRole, WidgetColor


class VisualizzaSpettacoloPage(AbstractVisualizzaView):
    """Pagina per visualizzare i singoli `Spettacolo` in dettaglio.

    Contiene le tutte informazioni dello `Spettacolo` ed una lista con tutti gli `Evento`
    associati ad essa.

    Segnali
    ---
    - `displayEventiRequest(ListLayout)`: emesso per mostrare a schermo la lista eventi;
    - `nuovoEventoRequest()`: emesso quando si clicca il pulsante Nuovo evento;
    - `visualizzaPrezziRequest(int)`: emesso quando si clicca il pulsanti Lista prezzi.
    """

    displayEventiRequest = pyqtSignal(ListLayout)
    nuovoEventoRequest = pyqtSignal()
    visualizzaPrezziRequest = pyqtSignal(int)

    def __init__(self, user_session: UserSession):
        self.is_biglietteria = user_session.ha_permessi_biglietteria()
        self.id_current_spettacolo: int = -1

        super().__init__()

    # ------------------------- SETUP INIT -------------------------

    @override
    def _setup_ui(self) -> None:
        super()._setup_ui()

        # Labels
        self.label_titolo = HyphenatedLabel("[Titolo Spettacolo]")
        self.label_titolo.setProperty(WidgetRole.Label.HEADER1, True)
        self.label_titolo.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.label_note = HyphenatedLabel("[Note Spettacolo]")
        self.label_note.setProperty(WidgetRole.Label.BODY_TEXT, True)
        self.label_note.setProperty(WidgetColor.Label.PRIMARY_COLOR, True)

        container_dati_speciali = QWidget()
        self.layout_dati_speciali = QVBoxLayout(container_dati_speciali)
        self.layout_dati_speciali.setContentsMargins(0, 0, 0, 0)

        # Lista Eventi
        label_lista_eventi = QLabel("Lista eventi")
        label_lista_eventi.setProperty(WidgetRole.Label.HEADER2, True)

        header_eventi = QWidget()
        self.layout_header_eventi = QHBoxLayout(header_eventi)
        self.layout_header_eventi.setContentsMargins(0, 0, 0, 0)
        self.layout_header_eventi.addWidget(label_lista_eventi)

        if self.is_biglietteria:
            self.__btn_nuovo_evento = DefaultButton("Nuovo evento")
            self.layout_header_eventi.addWidget(self.__btn_nuovo_evento)

        self.layout_header_eventi.addStretch()

        self.lista_eventi: list[Evento] = []

        label_lista_eventi_vuota = EmptyStateLabel(
            "Al momento, non vi sono eventi per questo spettacolo."
        )
        label_lista_eventi_vuota.setProperty(WidgetRole.Label.BODY_TEXT, True)
        label_lista_eventi_vuota.setProperty(WidgetColor.Label.SECONDARY_COLOR, True)

        content_lista_eventi = QWidget()
        content_lista_eventi.setProperty(WidgetRole.Item.LIST, True)
        self.layout_lista_eventi = ListLayout(
            content_lista_eventi, label_lista_eventi_vuota
        )

        header_data = QLabel("Data")
        header_data.setProperty(WidgetRole.Label.HEADER3, True)
        header_ora = QLabel("Ora")
        header_ora.setProperty(WidgetRole.Label.HEADER3, True)
        header_opzioni = QLabel("Opzioni")
        header_opzioni.setProperty(WidgetRole.Label.HEADER3, True)

        header_lista_eventi = QWidget()
        layout_header_lista_eventi = QGridLayout(header_lista_eventi)
        layout_header_lista_eventi.setContentsMargins(1, 1, 1, 1)
        layout_header_lista_eventi.addWidget(
            header_data, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout_header_lista_eventi.addWidget(make_vline(), 0, 1)
        layout_header_lista_eventi.addWidget(
            header_ora, 0, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )

        layout_header_lista_eventi.addWidget(make_vline(), 0, 3)
        layout_header_lista_eventi.addWidget(
            header_opzioni, 0, 4, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.eventi = QWidget()
        self.layout_eventi = QVBoxLayout(self.eventi)
        self.layout_eventi.addWidget(header_eventi)
        self.layout_eventi.addWidget(header_lista_eventi)
        self.layout_eventi.addWidget(content_lista_eventi)
        # end-Lista Eventi

        # Layout
        self._layout_content.addWidget(self.label_titolo)
        self._layout_content.addWidget(self.label_note)
        self._layout_content.addWidget(container_dati_speciali)
        if self.is_biglietteria:
            self.__btn_visualizza_prezzi = DefaultButton("Lista Prezzi")
            self._layout_content.addWidget(self.__btn_visualizza_prezzi)
        self._layout_content.addWidget(make_hline())
        self._layout_content.addWidget(self.eventi)
        self._layout_content.addStretch()

    @override
    def _connect_signals(self) -> None:
        super()._connect_signals()

        if self.is_biglietteria:
            self.__btn_nuovo_evento.clicked.connect(  # type:ignore
                self.nuovoEventoRequest.emit
            )

            self.__btn_visualizza_prezzi.clicked.connect(  # type:ignore
                lambda: self.visualizzaPrezziRequest.emit(self.id_current_spettacolo)
            )

    # ------------------------- METODI DI VIEW -------------------------

    @override
    def set_data(self, data: SpettacoloData) -> None:  # type: ignore[override]
        """Carica i dati dello spettacolo nella pagina.

        :param data: data salvata in una classe immutabile"""
        # Reset layout lista eventi
        self.layout_lista_eventi.svuota_layout()

        # Salva dati dello spettacolo nella pagina
        self.id_current_spettacolo = data.id
        # Carica dati dello spettacolo
        self.label_titolo.setText(f"{data.titolo}")
        self.label_note.show()
        if data.note:
            self.label_note.setText(f"{data.note}")
        else:
            self.label_note.hide()
        svuota_layout_generico(self.layout_dati_speciali)
        if type(data) is RegiaData:
            label_regista = QLabel(f"<b>Regista:</b> {data.regista}")
            label_regista.setProperty(WidgetRole.Label.BODY_TEXT, True)
            label_regista.setProperty(WidgetColor.Label.PRIMARY_COLOR, True)
            self.layout_dati_speciali.addWidget(label_regista)

            label_anno = QLabel(f"<b>Anno di produzione:</b> {data.anno_produzione}")
            label_anno.setProperty(WidgetRole.Label.BODY_TEXT, True)
            label_anno.setProperty(WidgetColor.Label.PRIMARY_COLOR, True)
            self.layout_dati_speciali.addWidget(label_anno)
        else:  # Caso Spettacolo generico
            ...

    @override
    def aggiorna_pagina(self) -> None:
        super().aggiorna_pagina()

        self.layout_lista_eventi.svuota_layout()
        self.displayEventiRequest.emit(self.layout_lista_eventi)
