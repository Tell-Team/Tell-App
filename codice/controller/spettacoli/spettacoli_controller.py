from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal, QObject
from functools import partial
from typing import Optional

from controller.navigation import Pagina

from model.model import Model
from model.pianificazione.spettacolo import Spettacolo
from model.pianificazione.regia import Regia
from model.exceptions import OggettoInUsoException

from view.spettacoli.pagine import SpettacoliSectionView
from view.spettacoli.widgets import SpettacoloDisplay
from view.spettacoli.utils import SpettacoloPageData

from view.utils.list_widgets import ListLayout
from view.utils import PopupMessage
from view.style import QssStyle


class SpettacoliController(QObject):
    """Gestice la sezione Spettacoli (`SpettacoliSectionView`) dell'app.

    Segnali:
    - logoutRequest(): emesso per eseguire la funzione di logout dall`AppContext`;
    - goToPageRequest(Pagina, bool): emesso per visualizzare un'altra pagina;
    - goToSectionRequest(Pagina): emesso per visualizzare un'altra pagina, senza salvarla
    nell'history del `NavigationController`;
    - getNavPageRequest(Pagina, dict): emesso per ottenere la pagina che vendrà visualizzata.
    """

    logoutRequest: pyqtSignal = pyqtSignal()
    goToPageRequest: pyqtSignal = pyqtSignal(Pagina, bool)
    goToSectionRequest: pyqtSignal = pyqtSignal(Pagina)
    getNavPageRequest: pyqtSignal = pyqtSignal(Pagina, dict)

    def __init__(self, model: Model, spettacoli_s: SpettacoliSectionView) -> None:
        super().__init__()
        self.__model = model
        self.__spettacoli_section = spettacoli_s

        self.__connect_signals()

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    def __connect_signals(self) -> None:
        # Logout
        self.__spettacoli_section.logoutRequest.connect(  # type:ignore
            self.logoutRequest.emit  # - CORRIGGERE: Account ancora non implementato
        )
        # Visualizza Sezione Info
        self.__spettacoli_section.goToInfo.connect(  # type:ignore
            partial(self.goToSectionRequest.emit, Pagina.SEZIONE_INFO)
        )
        # Visualizza Sezione Account
        self.__spettacoli_section.goToAccount.connect(  # type:ignore
            partial(self.goToSectionRequest.emit, Pagina.SEZIONE_ACCOUNT)
        )

        # Display della Lista Spettacoli
        self.__spettacoli_section.displaySpettacoliRequest.connect(  # type:ignore
            self.__display_spettacoli
        )

        # Setup della pagina di creazione di spettacoli
        self.__spettacoli_section.nuovoSpettacoloRequest.connect(  # type:ignore
            self.__nuovo_spettacolo
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __get_spettacolo(self, id_: int) -> Optional[Spettacolo]:
        return self.__model.get_spettacolo(id_)

    def __get_spettacoli(self) -> list[Spettacolo]:
        return self.__model.get_spettacoli()

    def __get_spettacoli_by_titolo(self, titolo: str) -> list[Spettacolo]:
        return self.__model.get_spettacoli_by_titolo(titolo)

    def __elimina_spettacolo(self, id_: int) -> None:
        self.__model.elimina_spettacolo(id_)
        # - Implementare elimina_spettacolo nel model

    def __display_spettacoli(self, layout_spettacoli: ListLayout) -> None:
        """Visualizza a schermo alcune informazioni delgli spettacoli salvati ed assegna a
        ciascuno pulsanti per [# - CORRIGGERE].

        :param layout: layout dove saranno caricate tutte le opere
        """
        # Verifica se c'è un filtro di ricerca
        filtro = self.__spettacoli_section.filtro_ricerca

        lista_spettacoli = (
            self.__get_spettacoli()
            if not filtro
            else self.__get_spettacoli_by_titolo(filtro)
        )

        # Verifica che la lista non sia vuota
        if not lista_spettacoli:
            layout_spettacoli.if_lista_vuota()
            return

        # Mostra tutti gli spettacoli della lista a schermo
        for spettacolo in lista_spettacoli:
            # Verifica che classe di Spettacolo è l'istanza
            if isinstance(spettacolo, Regia):
                compositore: str = ""
                if cur_opera := self.__model.get_opera(spettacolo.get_id_opera()):
                    compositore = cur_opera.get_compositore()
                dati = (compositore, spettacolo.get_regista())
                cur_spettacolo = SpettacoloDisplay(spettacolo, dati)
            else:
                cur_spettacolo = SpettacoloDisplay(spettacolo)

            # Setup della pagina di visualizzazione delgli spettacoli
            cur_spettacolo.visualizzaRequest.connect(  # type:ignore
                self.__visualizza_spettacolo
            )

            cur_spettacolo.scegliPostoRequest.connect(  # type:ignore
                self.__scegli_posti
            )

            # Setup della pagina di modifica degli spettacoli
            cur_spettacolo.modificaRequest.connect(  # type:ignore
                self.__modifica_spettacolo
            )

            # Aggiungi cur_spettacolo al layout di ListaSpettacoli
            layout_spettacoli.aggiungi_list_item(cur_spettacolo, QssStyle.ITEM_CARD)

            # Funzione di elimina per lo spettacolo
            def on_si(id_: int) -> None:
                """Prova di eliminare l'istanza di spettacolo.

                :param id_: id dello spettacolo da elimina
                """
                try:
                    self.__elimina_spettacolo(id_)
                except OggettoInUsoException as exc:
                    cur_spettacolo.annulla_elimina()
                    PopupMessage.mostra_errore(
                        self.__spettacoli_section,
                        "Spettacolo in uso",
                        f"Si è verificato un errore: {exc}",
                    )
                else:
                    self.__spettacoli_section.aggiorna_pagina()

            cur_spettacolo.eliminaConfermata.connect(  # type:ignore
                on_si
            )

    def __visualizza_spettacolo(self, id_: int) -> None: ...

    def __scegli_posti(self, id_: int) -> None: ...

    def __nuovo_spettacolo(self) -> None:
        """Carica la pagina `NuovoSpettacoloView`, dove l'utente può inserire i dati
        necessari per creare uno spettacolo."""
        # Ottieni la pagina NuovoSpettacoloView
        from view.spettacoli.pagine import NuovoSpettacoloView

        cur_pagina_dict: dict[str, Optional[QWidget]] = {"value": None}
        pagina_nome = Pagina.NUOVO_SPETTACOLO
        self.getNavPageRequest.emit(pagina_nome, cur_pagina_dict)
        cur_pagina: Optional[QWidget] = cur_pagina_dict.get("value")

        if type(cur_pagina) is not NuovoSpettacoloView:
            PopupMessage.mostra_errore(
                self.__spettacoli_section,
                "Pagina non trovata",
                f"Si è verificato un errore: Non è stato trovata la pagina '{pagina_nome}'. "
                + f"Type trovato: {type(cur_pagina)}",
            )
            return

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)

    def __modifica_spettacolo(self, id_: int) -> None:
        """Carica la pagina `ModificaSpettacoloView`, con i dati dello spettacolo indicato
        inseriti nei campo di input.

        :param id_: id dello spettacolo da modificare
        """
        # Copia dello spettacolo da modificare
        cur_spettacolo = self.__get_spettacolo(id_)
        if not cur_spettacolo:
            PopupMessage.mostra_errore(
                self.__spettacoli_section,
                "Spettacolo inesistente",
                f"Non è presente nessuno spettacolo con id {id_}.",
            )
            return

        # Ottieni la pagina ModificaSpettacoloView
        from view.spettacoli.pagine import ModificaSpettacoloView

        cur_pagina_dict: dict[str, Optional[QWidget]] = {"value": None}
        pagina_nome = Pagina.MODIFICA_SPETTACOLO
        self.getNavPageRequest.emit(pagina_nome, cur_pagina_dict)
        cur_pagina: Optional[QWidget] = cur_pagina_dict.get("value")

        if type(cur_pagina) is not ModificaSpettacoloView:
            PopupMessage.mostra_errore(
                self.__spettacoli_section,
                "Pagina non trovata",
                f"Si è verificato un errore: Non è stato trovata la pagina '{pagina_nome}'. "
                + f"Type trovato: {type(cur_pagina)}",
            )
            return

        # Salva i dati dentro di un container
        spettacolo_data = SpettacoloPageData(
            id=cur_spettacolo.get_id(),
            titolo=cur_spettacolo.get_titolo(),
            note=cur_spettacolo.get_note(),
            interpreti=cur_spettacolo.get_interpreti(),
            tecnici=cur_spettacolo.get_tecnici(),
        )

        # Setup pagina con i data dello spettacolo
        if isinstance(cur_spettacolo, Regia):
            tipo_spettacolo: str = ""
            if cur_opera := self.__model.get_opera(cur_spettacolo.get_id_opera()):
                tipo_spettacolo = (
                    "**Questo spettacolo è una Regia associata "
                    + f'all\'opera "{cur_opera.get_nome()}".**'
                )
            cur_pagina.set_data(spettacolo_data, tipo_spettacolo)
        else:
            cur_pagina.set_data(spettacolo_data)

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)
