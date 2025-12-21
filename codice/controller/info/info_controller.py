from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import pyqtSignal, QObject
from typing import Optional
from functools import partial

from model.model import Model
from model.pianificazione.opera import Opera
from model.pianificazione.genere import Genere
from model.pianificazione.regia import Regia
from model.exceptions import OggettoInUsoException

from view.info.pagine.info_section import InfoSectionView
from view.info.pagine.visualizza_opera import VisualizzaOperaView
from view.info.widgets.operaDisplay import OperaDisplay
from view.info.widgets.genereDisplay import GenereDisplay
from view.info.widgets.regiaDisplay import RegiaDisplay
from view.info.utils.operaPageData import OperaPageData
from view.info.utils.generePageData import GenerePageData
from view.info.utils.regiaPageData import RegiaPageData
from view.messageView import MessageView

# Regia, RegiaDisplay e RegiaPageData sono necessari per VisualizzaOpera.
# - Dovrei creare un visualizza_opera_controller.py per delegare funzioni e rendere
#   questo controller meno complesso?


class InfoController(QObject):
    """Gestice la sezione Info (`InfoSectionView`) dell'app e la pagina per visualizzare
    un'opera (`VisualizzaOperaView`).

    Segnali:
    - logoutRequest(): emesso per eseguire la funzione di logout dall`AppContext`;
    - goBackRequest(): emesso per tornare all'ultima pagina salvata nell'hitory del
    `NavigationController`;
    - goToPageRequest(str, bool): emesso per visualizzare un'altra pagina;
    - goToSectionRequest(str): emesso per visualizzare un'altra pagina, senza salvarla
    nell'history del `NavigationController`;
    - getNavPageRequest(str, dict): emesso per ottenere la pagina che vendrà visualizzata.
    """

    logoutRequest = pyqtSignal()
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
            self.logoutRequest.emit  # - CORRIGGERE: Account ancora non implementato
        )
        # Visualizza Sezione Spettacoli
        self.__info_section.goToSpettacoli.connect(  # type:ignore
            partial(self.goToSectionRequest.emit, "spettacoli_section")
        )
        # Visualizza Sezione Account
        self.__info_section.goToAccount.connect(  # type:ignore
            partial(self.goToSectionRequest.emit, "account_section")
            # - CORRIGGERE: Account ancora non implementato
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
        # Setup della pagina di creazione di regie
        self.__visualizza_opera_view.nuovaRegiaRequest.connect(  # type:ignore
            self.nuova_regia
        )
        # Display della Lista Regie
        self.__visualizza_opera_view.displayRegieRequest.connect(  # type:ignore
            self.display_regie
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

    def get_opere_by_nome(self, nome: str) -> list[Opera]:
        return self.__model.get_opere_by_nome(nome)

    def elimina_opera(self, id_: int) -> None:
        self.__model.elimina_opera(id_)

    def get_genere(self, id_: int) -> Optional[Genere]:
        return self.__model.get_genere(id_)

    def get_generi(self) -> list[Genere]:
        return self.__model.get_generi()

    def elimina_genere(self, id_: int) -> None:
        self.__model.elimina_genere(id_)

    def get_regia(self, id_: int) -> Optional[Regia]:
        regia = self.__model.get_spettacolo(id_)
        if not isinstance(regia, Regia):
            return None
        return regia
        # - Questa definizione dovrebbe esser parte del model?

    def get_regie_by_opera(self, id_: int) -> list[Regia]:
        return self.__model.get_regie_by_opera(id_)

    def elimina_regia(self, id_: int) -> None:
        self.__model.elimina_spettacolo(id_)
        # - Implementare elimina_spettacolo nel model

    def display_opere(self, layout: QVBoxLayout) -> None:
        """Visualizza a schermo alcune informazioni delle opere salvate ed assegna a
        ciascuna pulsanti per visualizzarle in dettaglio, modificarle o eliminarle.

        :param layout: layout dove saranno caricate tutte le opere
        """
        # Verifica se c'è un filtro di ricerca
        lista_opere: list[Opera] = []
        filtro = self.__info_section.filtro_ricerca

        if filtro == "":
            lista_opere = self.get_opere()
        else:
            lista_opere = self.get_opere_by_nome(filtro)

        # Verifica che la lista non sia vuota
        if not lista_opere:
            self.__info_section.if_lista_vuota(layout)
            return

        # Mostra tutte le opere della lista a schermo
        for opera in lista_opere:
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
            self.__info_section.aggiungi_widget_a_layout(cur_opera, layout)

            # Funzione di elimina per l'opera
            def on_si(id_: int) -> None:
                """Prova di eliminare l'istanza d'opera.

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
                    self.__info_section.aggiorna_pagina()

            cur_opera.eliminaConfermata.connect(  # type:ignore
                on_si
            )

    def display_generi(self, layout: QVBoxLayout) -> None:
        """Visualizza a schermo le informazioni dei generi salvati ed assegna a
        ciascuno pulsanti per modificarli o eliminarli.

        :param layout: layout dove saranno caricate tutti i generi
        """
        # Verifica che la lista non sia vuota
        if not self.get_generi():
            self.__info_section.if_lista_vuota(layout)
            return

        # Mostra tutti i generi salvati a schermo
        for genere in self.get_generi():
            cur_genere = GenereDisplay(genere)

            # Setup della pagina di modifica dei generi
            cur_genere.modificaRequest.connect(  # type:ignore
                self.modifica_genere
            )

            # Aggiungi cur_genere al layout di ListaOpere
            self.__info_section.aggiungi_widget_a_layout(cur_genere, layout)

            # Funzione di elimina per il genere
            def on_si(id_: int) -> None:
                """Prova di eliminare l'istanza d'opera.

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
                    self.__info_section.aggiorna_pagina()

            cur_genere.eliminaConfermata.connect(  # type:ignore
                on_si
            )

    def visualizza_opera(self, id_: int) -> None:
        """Carica la pagina `VisualizzaOperaView` con i dati relativi all'opera
        indicata.

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
        cur_pagina = self.__visualizza_opera_view

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

        cur_pagina.set_data(opera_data, cur_genere.get_nome(), lista_regie)

        # Apri la pagina
        self.goToPageRequest.emit("visualizza_opera", True)

    def display_regie(self, layout: QVBoxLayout) -> None:
        """Visualizza a schermo le informazioni delle regie salvati e vincolate ad
        un'opera ed assegna a ciascuna pulsanti per modificarli o eliminarli.

        :param layout: layout dove saranno caricate tutti le regie
        """
        # Verifica che la lista non sia vuota
        cur_lista = self.get_regie_by_opera(self.__visualizza_opera_view.id_cur_opera)
        if not cur_lista:
            self.__visualizza_opera_view.if_lista_vuota(layout)
            return

        # Mostra tutti le regie salvate a schermo
        for regia in cur_lista:
            cur_regia = RegiaDisplay(regia)

            # Setup della pagina di modifica delle regie
            cur_regia.modificaRequest.connect(  # type:ignore
                self.modifica_regia
            )

            # Aggiungi cur_regia al layout di ListaRegie
            self.__visualizza_opera_view.aggiungi_widget_a_layout(cur_regia, layout)

            # Funzione di elimina per la regia
            def on_si(id_: int) -> None:
                """Prova di eliminare l'istanza di regia.

                :param id_: id della regia da elimina
                """
                try:
                    self.elimina_regia(id_)
                except OggettoInUsoException as exc:
                    cur_regia.annulla_elimina()
                    self.__message_view.mostra_errore(
                        self.__info_section,
                        "Regia in uso",
                        f"Si è verificato un errore: {exc}",
                    )
                else:
                    self.__info_section.aggiorna_pagina()

            cur_regia.eliminaConfermata.connect(  # type:ignore
                on_si
            )

    def nuova_regia(self) -> None:
        """Carica la pagina `NuovaRegiaView`, dove l'utente può inserire i dati
        necessari per creare una regia.
        """
        # Ottieni la pagina NuovaOperaView
        from view.info.pagine.nuova_regia import NuovaRegiaView

        cur_pagina_dict: dict[str, Optional[QWidget]] = {"value": None}
        pagina_nome = "nuova_regia"
        self.getNavPageRequest.emit(pagina_nome, cur_pagina_dict)
        cur_pagina: Optional[QWidget] = cur_pagina_dict.get("value")

        if not isinstance(cur_pagina, NuovaRegiaView):
            self.__message_view.mostra_errore(
                self.__visualizza_opera_view,
                "Pagina non trovata",
                f"Si è verificato un errore: Non è stato trovata la pagina '{pagina_nome}'. "
                + f"Type trovato: {type(cur_pagina)}",
            )
            return

        # Setup pagina pulendo i campi
        cur_id_opera = self.__visualizza_opera_view.id_cur_opera
        cur_opera = self.get_opera(cur_id_opera)

        if not isinstance(cur_opera, Opera):
            self.__message_view.mostra_errore(
                self.__visualizza_opera_view,
                "Opera inesistente",
                f"Non è presente nessun'opera con id {cur_id_opera}.",
            )
            return

        cur_pagina.setup_opera_combobox(cur_opera)
        cur_pagina.reset_pagina()

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)

    def modifica_regia(self, id_: int) -> None:
        """Carica la pagina `ModificaRegiaView`, con i dati della regia indicata
        inseriti nei campo di input.

        :param id_: id della regia da modificare
        """
        # Copia della regia da modificare
        cur_regia = self.get_regia(id_)
        if not cur_regia:
            self.__message_view.mostra_errore(
                self.__visualizza_opera_view,
                "Regia inesistente",
                f"Non è presente nessuna regia con id {id_}.",
            )
            return

        # Ottieni la pagina ModificaRegiaView
        from view.info.pagine.modifica_regia import ModificaRegiaView

        cur_pagina_dict: dict[str, Optional[QWidget]] = {"value": None}
        pagina_nome = "modifica_regia"
        self.getNavPageRequest.emit(pagina_nome, cur_pagina_dict)
        cur_pagina: Optional[QWidget] = cur_pagina_dict.get("value")

        if not isinstance(cur_pagina, ModificaRegiaView):
            self.__message_view.mostra_errore(
                self.__visualizza_opera_view,
                "Pagina non trovata",
                f"Si è verificato un errore: Non è stato trovata la pagina '{pagina_nome}'. "
                + f"Type trovato: {type(cur_pagina)}",
            )
            return

        # Salva i dati dentro di un container
        regia_data = RegiaPageData(
            id=cur_regia.get_id(),
            regista=cur_regia.get_regista(),
            anno_produzione=cur_regia.get_anno_produzione(),
            id_opera=cur_regia.get_id_opera(),
            titolo=cur_regia.get_titolo(),
            note=cur_regia.get_note(),
            interpreti=cur_regia.get_interpreti(),
            tecnici=cur_regia.get_tecnici(),
        )

        cur_opera = self.get_opera(cur_regia.get_id_opera())
        if not isinstance(cur_opera, Opera):
            self.__message_view.mostra_errore(
                self.__visualizza_opera_view,
                "Opera inesistente",
                f"Non è presente nessun'opera con id '{cur_regia.get_id_opera()}'.",
            )
            return

        # Setup pagina con i data del genere
        cur_pagina.setup_opera_combobox(cur_opera)
        cur_pagina.set_data(regia_data)

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)

    def nuova_opera(self) -> None:
        """Carica la pagina `NuovaOperaView`, dove l'utente può inserire i dati
        necessari per creare un'opera.
        """
        # Ottieni la pagina NuovaOperaView
        from view.info.pagine.nuova_opera import NuovaOperaView

        cur_pagina_dict: dict[str, Optional[QWidget]] = {"value": None}
        pagina_nome = "nuova_opera"
        self.getNavPageRequest.emit(pagina_nome, cur_pagina_dict)
        cur_pagina: Optional[QWidget] = cur_pagina_dict.get("value")

        if not isinstance(cur_pagina, NuovaOperaView):
            self.__message_view.mostra_errore(
                self.__info_section,
                "Pagina non trovata",
                f"Si è verificato un errore: Non è stato trovata la pagina '{pagina_nome}'. "
                + f"Type trovato: {type(cur_pagina)}",
            )
            return

        # Setup pagina pulendo i campi
        cur_pagina.setup_genere_combobox(self.get_generi())
        cur_pagina.reset_pagina()

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)

    def modifica_opera(self, id_: int) -> None:
        """Carica la pagina `ModificaOperaView`, con i dati dell'opera indicata
        inseriti nei campo di input.

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
        from view.info.pagine.modifica_opera import ModificaOperaView

        cur_pagina_dict: dict[str, Optional[QWidget]] = {"value": None}
        pagina_nome = "modifica_opera"
        self.getNavPageRequest.emit(pagina_nome, cur_pagina_dict)
        cur_pagina: Optional[QWidget] = cur_pagina_dict.get("value")

        if not isinstance(cur_pagina, ModificaOperaView):
            self.__message_view.mostra_errore(
                self.__info_section,
                "Pagina non trovata",
                f"Si è verificato un errore: Non è stato trovata la pagina '{pagina_nome}'. "
                + f"Type trovato: {type(cur_pagina)}",
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
        cur_pagina.setup_genere_combobox(self.get_generi())
        cur_pagina.set_data(opera_data)

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)

    def nuovo_genere(self) -> None:
        """Carica la pagina `NuovoGenereView`, dove l'utente può inserire i dati
        necessari per creare un genere.
        """
        # Ottieni la pagina NuovoGenereView
        from view.info.pagine.nuovo_genere import NuovoGenereView

        cur_pagina_dict: dict[str, Optional[QWidget]] = {"value": None}
        pagina_nome = "nuovo_genere"
        self.getNavPageRequest.emit(pagina_nome, cur_pagina_dict)
        cur_pagina: Optional[QWidget] = cur_pagina_dict.get("value")

        if not isinstance(cur_pagina, NuovoGenereView):
            self.__message_view.mostra_errore(
                self.__info_section,
                "Pagina non trovata",
                f"Si è verificato un errore: Non è stato trovata la pagina '{pagina_nome}'. "
                + f"Type trovato: {type(cur_pagina)}",
            )
            return

        # Setup pagina pulendo i campi
        cur_pagina.reset_pagina()

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)

    def modifica_genere(self, id_: int) -> None:
        """Carica la pagina `ModificaGenereView`, con i dati del genere indicato
        inseriti nei campo di input.

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
        from view.info.pagine.modifica_genere import ModificaGenereView

        cur_pagina_dict: dict[str, Optional[QWidget]] = {"value": None}
        pagina_nome = "modifica_genere"
        self.getNavPageRequest.emit(pagina_nome, cur_pagina_dict)
        cur_pagina: Optional[QWidget] = cur_pagina_dict.get("value")

        if not isinstance(cur_pagina, ModificaGenereView):
            self.__message_view.mostra_errore(
                self.__info_section,
                "Pagina non trovata",
                f"Si è verificato un errore: Non è stato trovata la pagina '{pagina_nome}'. "
                + f"Type trovato: {type(cur_pagina)}",
            )
            return

        # Salva i dati dentro di un container
        genere_data = GenerePageData(
            id=cur_genere.get_id(),
            nome=cur_genere.get_nome(),
            descrizione=cur_genere.get_descrizione(),
        )

        # Setup pagina con i data del genere
        cur_pagina.set_data(genere_data)

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)
