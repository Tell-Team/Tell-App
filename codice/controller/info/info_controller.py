from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import pyqtSignal, QObject
from typing import Optional
from functools import partial

from model.model import Model
from model.pianificazione.opera import Opera
from model.pianificazione.genere import Genere
from model.pianificazione.regia import Regia  # Necessario per VisualizzaOpera.
from model.exceptions import OggettoInUsoException

from view.info.info_section import InfoSectionView
from view.info.visualizza_opera import VisualizzaOperaView
from view.info.operaDisplay import OperaDisplay
from view.info.genereDisplay import GenereDisplay
from view.info.operaPageData import OperaPageData
from view.info.generePageData import GenerePageData
from view.messageView import MessageView


class InfoController(QObject):
    """
    Gestice la sezione Info (`InfoSectionView`) dell'app e la pagina per visualizzare un'opera
    (`VisualizzaOperaView`).

    Segnali:
    - goBackRequest(): emesso per tornare all'ultima pagina salvata nell'hitory del
    `NavigationController`;
    - goToPageRequest(str, bool): emesso per visualizzare un'altra pagina;
    - goToSectionRequest(str): emesso per visualizzare un'altra pagina, senza salvarla
    nell'history del `NavigationController`;
    - getNavPageRequest(str, dict): emesso per ottenere la pagina che vendrà visualizzata.
    """

    goBackRequest = pyqtSignal()
    goToPageRequest = pyqtSignal(str, bool)
    goToSectionRequest = pyqtSignal(str)
    getNavPageRequest = pyqtSignal(str, dict)

    def __init__(
        self,
        model: Model,
        info_s: InfoSectionView,
        opera_v: VisualizzaOperaView,
        message_v: MessageView,
    ) -> None:
        super().__init__()
        self.__model = model
        self.__info_section = info_s  # Sezione Info
        self.__visualizza_opera_view = opera_v  # Pagina Visualizza Opera
        self.__message_view = message_v  # View dedicata ai popup

        self._connect_signals()

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    def _connect_signals(self) -> None:
        # Logout
        self.__info_section.logoutRequest.connect(  # type:ignore
            self.goBackRequest.emit  # - Account ancora non implemetati
        )
        # Visualizza Sezione Spettacoli
        self.__info_section.goToSpettacoli.connect(  # type:ignore
            partial(self.goToSectionRequest.emit, "spettacoli_section")
        )

        # Visualizza Sezione Account
        self.__info_section.goToAccount.connect(  # type:ignore
            partial(self.goToSectionRequest.emit, "account_section")
            # - Account ancora non implemetati
        )

        # Display della Lista Opere
        self.__info_section.displayOpereRequest.connect(  # type:ignore
            self.display_opere
        )
        # Display della Lista Generi
        self.__info_section.displayGeneriRequest.connect(  # type:ignore
            self.display_generi
        )

        # Setup della pagina di creazione di opere
        self.__info_section.nuovaOperaRequest.connect(  # type:ignore
            self.nuova_opera
        )

        # Visualizza Opera
        self.__visualizza_opera_view.tornaIndietroRequest.connect(  # type:ignore
            self.goBackRequest.emit
        )

        # Setup della pagina di creazione di generi
        self.__info_section.nuovoGenereRequest.connect(  # type:ignore
            self.nuovo_genere
        )

    # ------------------------- METODI PUBBLICI -------------------------

    def get_opera(self, id_: int) -> Optional[Opera]:
        return self.__model.get_opera(id_)

    def get_opere(self) -> list[Opera]:
        return self.__model.get_opere()

    def elimina_opera(self, id_: int) -> None:
        return self.__model.elimina_opera(id_)

    def get_genere(self, id_: int) -> Optional[Genere]:
        return self.__model.get_genere(id_)

    def get_generi(self) -> list[Genere]:
        return self.__model.get_generi()

    def elimina_genere(self, id_: int) -> None:
        return self.__model.elimina_genere(id_)

    def get_regie_by_opera(self, id_: int) -> list[Regia]:
        return self.__model.get_regie_by_opera(id_)

    def display_opere(self, layout: QVBoxLayout) -> None:
        """
        Visualizza a schermo alcune informazioni delle opere salvate ed assegna a
        ciascuna pulsanti per visualizzarle in dettaglio, modificarle o eliminarle.

        :param layout: layout dove saranno caricate tutte le opere
        """
        if not self.get_opere():
            self.__info_section.if_lista_vuota(layout)
            return

        for opera in self.get_opere():
            cur_opera = OperaDisplay(opera)

            # Setup della pagina di visualizzazione delle opere
            cur_opera.visualizzaRequest.connect(  # type:ignore
                self.visualizza_opera
            )

            # Setup della pagina di modifica delle opere
            cur_opera.modificaRequest.connect(  # type:ignore
                self.modifica_opera
            )

            # Aggiungi cur_opera al layout di ListaOpere
            self.__info_section.aggiungi_widget_al_layout(cur_opera, layout)

            # Funzione di elimina per l'opera
            def on_si(id_: int) -> None:
                """Prova di eliminare l'istanza d'opera

                :param id_: id dell'opera da elimina
                """
                try:
                    self.elimina_opera(id_)
                except OggettoInUsoException as exc:
                    cur_opera.annulla_elimina()
                    self.__message_view.mostra_errore(
                        self.__info_section,
                        "Opera in uso",
                        f"Si è verificato un errore: {exc}",
                    )
                else:
                    self.__info_section.refresh_page()

            cur_opera.eliminaConfermata.connect(  # type:ignore
                on_si
            )

    def display_generi(self, layout: QVBoxLayout) -> None:
        """
        Visualizza a schermo le informazioni dei generi salvati ed assegna a ciascuno
        pulsanti per modificarli o eliminarli.

        :param layout: layout dove saranno caricate tutti i generi
        """
        if not self.get_generi():
            self.__info_section.if_lista_vuota(layout)
            return

        for genere in self.get_generi():
            cur_genere = GenereDisplay(genere)

            # Setup della pagina di modifica dei generi
            cur_genere.modificaRequest.connect(  # type:ignore
                self.modifica_genere
            )

            # Aggiungi cur_genere al layout di ListaOpere
            self.__info_section.aggiungi_widget_al_layout(cur_genere, layout)

            # Funzione di elimina per il genere
            def on_si(id_: int) -> None:
                """Prova di eliminare l'istanza d'opera

                :param id_: id dell'opera da elimina
                """
                try:
                    self.elimina_genere(id_)
                except OggettoInUsoException as exc:
                    cur_genere.annulla_elimina()
                    self.__message_view.mostra_errore(
                        self.__info_section,
                        "Genere in uso",
                        f"Si è verificato un errore: {exc}",
                    )
                else:
                    self.__info_section.refresh_page()

            cur_genere.eliminaConfermata.connect(  # type:ignore
                on_si
            )

    def visualizza_opera(self, id_: int) -> None:
        """
        Carica la pagina `VisualizzaOperaView` con i dati relativi all'opera indicata.

        :param id_: id dell'opera da visualizzare
        """
        # Copia dell'opera da visualizzare
        cur_opera = self.get_opera(id_)
        if not cur_opera:
            self.__message_view.mostra_errore(
                self.__info_section,
                "Opera inesistente",
                f"Non è presente nessun'opera con id {id_}.",
            )
            return

        # Ottieni la pagina VisualizzaOperaView
        cur_page = self.__visualizza_opera_view

        # Setup pagina con i dati dell'opera
        cur_genere = self.get_genere(cur_opera.get_id_genere())
        if not cur_genere:
            self.__message_view.mostra_errore(
                self.__info_section,
                "Genere inesistente",
                f"Non è presente nessun genere con id {cur_opera.get_id_genere()}.",
            )
            return

        opera_data = OperaPageData(
            id=cur_opera.get_id(),
            nome=cur_opera.get_nome(),
            trama=cur_opera.get_trama(),
            id_genere=cur_opera.get_id_genere(),
            compositore=cur_opera.get_compositore(),
            librettista=cur_opera.get_librettista(),
            atti=cur_opera.get_numero_atti(),
            data_rappresentazione=cur_opera.get_data_prima_rappresentazione(),
            teatro_rappresentazione=cur_opera.get_teatro_prima_rappresentazione(),
        )

        lista_regie = self.get_regie_by_opera(cur_opera.get_id())

        cur_page.set_data(opera_data, cur_genere.get_nome(), lista_regie)

        # Apri la pagina
        self.goToPageRequest.emit("visualizza_opera", True)

    def nuova_opera(self) -> None:
        """
        Carica la pagina `NuovaOperaView`, dove l'utente può inserire i dati necessari per
        creare un'opera.
        """
        # Ottieni la pagina NuovaOperaView
        from view.info.nuova_opera import NuovaOperaView

        cur_page_dict: dict[str, Optional[QWidget]] = {"value": None}
        self.getNavPageRequest.emit("nuova_opera", cur_page_dict)
        cur_page: Optional[QWidget] = cur_page_dict.get("value")

        if not isinstance(cur_page, NuovaOperaView):
            self.__message_view.mostra_errore(
                self.__info_section,
                "Pagina non trovata",
                "Si è verificato un errore: Non è stato trovata la pagina 'nuova_opera'. "
                + f"Type trovato: {type(cur_page)}",
            )
            return

        # Setup pagina pulendo i campi
        cur_page.setup_genere_combobox(self.get_generi())
        cur_page.reset_pagina()

        # Apri la pagina
        self.goToPageRequest.emit("nuova_opera", True)

    def modifica_opera(self, id_: int) -> None:
        """
        Carica la pagina `ModificaOperaView`, con i dati dell'opera indicata inseriti nei
        campo di input.

        :param id_: id dell'opera da modificare
        """
        # Copia dell'opera da modificare
        cur_opera = self.get_opera(id_)
        if not cur_opera:
            self.__message_view.mostra_errore(
                self.__info_section,
                "Opera inesistente",
                f"Non è presente nessun'opera con id {id_}.",
            )
            return

        # Ottieni la pagina ModificaOperaView
        from view.info.modifica_opera import ModificaOperaView

        cur_page_dict: dict[str, Optional[QWidget]] = {"value": None}
        self.getNavPageRequest.emit("modifica_opera", cur_page_dict)
        cur_page: Optional[QWidget] = cur_page_dict.get("value")

        if not isinstance(cur_page, ModificaOperaView):
            self.__message_view.mostra_errore(
                self.__info_section,
                "Pagina non trovata",
                "Si è verificato un errore: Non è stato trovata la pagina 'modifica_opera'. "
                + f"Type trovato: {type(cur_page)}",
            )
            return

        # Salva i dati dentro di un container
        opera_data = OperaPageData(
            id=cur_opera.get_id(),
            nome=cur_opera.get_nome(),
            trama=cur_opera.get_trama(),
            id_genere=cur_opera.get_id_genere(),
            compositore=cur_opera.get_compositore(),
            librettista=cur_opera.get_librettista(),
            atti=cur_opera.get_numero_atti(),
            data_rappresentazione=cur_opera.get_data_prima_rappresentazione(),
            teatro_rappresentazione=cur_opera.get_teatro_prima_rappresentazione(),
        )

        # Setup pagina con i data dell'opera
        cur_page.setup_genere_combobox(self.get_generi())
        cur_page.set_data(opera_data)

        # Apri la pagina
        self.goToPageRequest.emit("modifica_opera", True)

    def nuovo_genere(self) -> None:
        """
        Carica la pagina `NuovoGenereView`, dove l'utente può inserire i dati necessari per
        creare un genere.
        """
        # Ottieni la pagina NuovoGenereView
        from view.info.nuovo_genere import NuovoGenereView

        cur_page_dict: dict[str, Optional[QWidget]] = {"value": None}
        self.getNavPageRequest.emit("nuovo_genere", cur_page_dict)
        cur_page: Optional[QWidget] = cur_page_dict.get("value")

        if not isinstance(cur_page, NuovoGenereView):
            self.__message_view.mostra_errore(
                self.__info_section,
                "Pagina non trovata",
                "Si è verificato un errore: Non è stato trovata la pagina 'nuovo_genere'. "
                + f"Type trovato: {type(cur_page)}",
            )
            return

        # Setup pagina pulendo i campi
        cur_page.reset_pagina()

        # Apri la pagina
        self.goToPageRequest.emit("nuovo_genere", True)

    def modifica_genere(self, id_: int) -> None:
        """
        Carica la pagina `ModificaGenereView`, con i dati del genere indicato inseriti nei
        campo di input.

        :param id_: id del genere da modificare
        """
        # Copia del genere da modificare
        cur_genere = self.get_genere(id_)
        if not cur_genere:
            self.__message_view.mostra_errore(
                self.__info_section,
                "Genere inesistente",
                f"Non è presente nessun genere con id {id_}.",
            )
            return

        # Ottieni la pagina ModificaGenereView
        from view.info.modifica_genere import ModificaGenereView

        cur_page_dict: dict[str, Optional[QWidget]] = {"value": None}
        self.getNavPageRequest.emit("modifica_genere", cur_page_dict)
        cur_page: Optional[QWidget] = cur_page_dict.get("value")

        if not isinstance(cur_page, ModificaGenereView):
            self.__message_view.mostra_errore(
                self.__info_section,
                "Pagina non trovata",
                "Si è verificato un errore: Non è stato trovata la pagina 'modifica_genere'. "
                + f"Type trovato: {type(cur_page)}",
            )
            return

        # Salva i dati dentro di un container
        genere_data = GenerePageData(
            id=cur_genere.get_id(),
            nome=cur_genere.get_nome(),
            descrizione=cur_genere.get_descrizione(),
        )

        # Setup pagina con i data del genere
        cur_page.set_data(genere_data)

        # Apri la pagina
        self.goToPageRequest.emit("modifica_genere", True)
