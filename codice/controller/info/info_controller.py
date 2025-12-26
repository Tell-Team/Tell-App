from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal, QObject
from typing import Optional
from functools import partial

from controller.navigation import Pagina

from model.model import Model
from model.pianificazione.opera import Opera
from model.pianificazione.genere import Genere
from model.pianificazione.regia import Regia
from model.exceptions import OggettoInUsoException

from view.info.pagine import InfoSectionView
from view.info.widgets import OperaDisplay, GenereDisplay
from view.info.utils import OperaPageData, GenerePageData

from view.utils.list_widgets import ListLayout
from view.utils import PopupMessage
from view.style import QssStyle


class InfoController(QObject):
    """Gestice la sezione Info (`InfoSectionView`) dell'app.

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

    def __init__(self, model: Model, info_s: InfoSectionView) -> None:
        super().__init__()
        self.__model = model
        self.__info_section = info_s

        self.__connect_signals()

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    def __connect_signals(self) -> None:
        # Logout
        self.__info_section.logoutRequest.connect(  # type:ignore
            self.logoutRequest.emit  # - CORRIGGERE: Account ancora non implementato
        )
        # Visualizza Sezione Spettacoli
        self.__info_section.goToSpettacoli.connect(  # type:ignore
            partial(self.goToSectionRequest.emit, Pagina.SEZIONE_SPETTACOLI)
        )
        # Visualizza Sezione Account
        self.__info_section.goToAccount.connect(  # type:ignore
            partial(self.goToSectionRequest.emit, Pagina.SEZIONE_ACCOUNT)
            # - CORRIGGERE: Account ancora non implementato
        )

        # Display della Lista Opere
        self.__info_section.displayOpereRequest.connect(  # type:ignore
            self.__display_opere
        )
        # Display della Lista Generi
        self.__info_section.displayGeneriRequest.connect(  # type:ignore
            self.__display_generi
        )

        # Setup della pagina di creazione di opere
        self.__info_section.nuovaOperaRequest.connect(  # type:ignore
            self.__nuova_opera
        )
        # Setup della pagina di creazione di generi
        self.__info_section.nuovoGenereRequest.connect(  # type:ignore
            self.__nuovo_genere
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __get_opera(self, id_: int) -> Optional[Opera]:
        return self.__model.get_opera(id_)

    def __get_opere(self) -> list[Opera]:
        return self.__model.get_opere()

    def __get_opere_by_nome(self, nome: str) -> list[Opera]:
        return self.__model.get_opere_by_nome(nome)

    def __elimina_opera(self, id_: int) -> None:
        self.__model.elimina_opera(id_)

    def __get_genere(self, id_: int) -> Optional[Genere]:
        return self.__model.get_genere(id_)

    def __get_generi(self) -> list[Genere]:
        return self.__model.get_generi()

    def __elimina_genere(self, id_: int) -> None:
        self.__model.elimina_genere(id_)

    def __get_regie_by_opera(self, id_: int) -> list[Regia]:
        return self.__model.get_regie_by_opera(id_)

    def __display_opere(self, layout_opere: ListLayout) -> None:
        """Visualizza a schermo alcune informazioni delle opere salvate ed assegna a
        ciascuna pulsanti per visualizzarle in dettaglio, modificarle o eliminarle.

        :param layout: layout dove saranno caricate tutte le opere
        """
        lista_opere: list[Opera] = []

        # Verifica se c'è un filtro di ricerca
        filtro = self.__info_section.filtro_ricerca

        if filtro == "":
            lista_opere = self.__get_opere()
        else:
            lista_opere = self.__get_opere_by_nome(filtro)

        # Verifica che la lista non sia vuota
        if not lista_opere:
            layout_opere.if_lista_vuota()
            return

        # Mostra tutte le opere della lista a schermo
        for opera in lista_opere:
            cur_opera = OperaDisplay(opera)

            # Setup della pagina di visualizzazione delle opere
            cur_opera.visualizzaRequest.connect(  # type:ignore
                self.__visualizza_opera
            )

            # Setup della pagina di modifica delle opere
            cur_opera.modificaRequest.connect(  # type:ignore
                self.__modifica_opera
            )

            # Aggiungi cur_opera al layout di ListaOpere
            layout_opere.aggiungi_list_item(cur_opera, QssStyle.ITEM_CARD.style_role)

            # Funzione di elimina per l'opera
            def on_si(id_: int) -> None:
                """Prova di eliminare l'istanza d'opera.

                :param id_: id dell'opera da elimina
                """
                try:
                    self.__elimina_opera(id_)
                except OggettoInUsoException as exc:
                    cur_opera.annulla_elimina()
                    PopupMessage.mostra_errore(
                        self.__info_section,
                        "Opera in uso",
                        f"Si è verificato un errore: {exc}",
                    )
                else:
                    self.__info_section.aggiorna_pagina()

            cur_opera.eliminaConfermata.connect(  # type:ignore
                on_si
            )

    def __display_generi(self, layout_generi: ListLayout) -> None:
        """Visualizza a schermo le informazioni dei generi salvati ed assegna a
        ciascuno pulsanti per modificarli o eliminarli.

        :param layout: layout dove saranno caricate tutti i generi
        """
        lista_generi = self.__get_generi()

        # Verifica che la lista non sia vuota
        if not lista_generi:
            layout_generi.if_lista_vuota()
            return

        # Mostra tutti i generi salvati a schermo
        for genere in lista_generi:
            cur_genere = GenereDisplay(genere)

            # Setup della pagina di modifica dei generi
            cur_genere.modificaRequest.connect(  # type:ignore
                self.__modifica_genere
            )

            # Aggiungi cur_genere al layout di ListaOpere
            layout_generi.aggiungi_list_item(cur_genere, QssStyle.ITEM_CARD.style_role)

            # Funzione di elimina per il genere
            def on_si(id_: int) -> None:
                """Prova di eliminare l'istanza d'opera.

                :param id_: id dell'opera da elimina
                """
                try:
                    self.__elimina_genere(id_)
                except OggettoInUsoException as exc:
                    cur_genere.annulla_elimina()
                    PopupMessage.mostra_errore(
                        self.__info_section,
                        "Genere in uso",
                        f"Si è verificato un errore: {exc}",
                    )
                else:
                    self.__info_section.aggiorna_pagina()

            cur_genere.eliminaConfermata.connect(  # type:ignore
                on_si
            )

    def __visualizza_opera(self, id_: int) -> None:
        """Carica la pagina `VisualizzaOperaView` con i dati relativi all'opera
        indicata.

        :param id_: id dell'opera da visualizzare
        """
        # Copia dell'opera da visualizzare
        cur_opera = self.__get_opera(id_)
        if not cur_opera:
            PopupMessage.mostra_errore(
                self.__info_section,
                "Opera inesistente",
                f"Non è presente nessuna opera con id {id_}.",
            )
            return

        # Ottieni la pagina VisualizzaOperaView
        from view.info.pagine import VisualizzaOperaView

        cur_pagina_dict: dict[str, Optional[QWidget]] = {"value": None}
        pagina_nome = Pagina.VISUALIZZA_OPERA
        self.getNavPageRequest.emit(pagina_nome, cur_pagina_dict)
        cur_pagina: Optional[QWidget] = cur_pagina_dict.get("value")

        if type(cur_pagina) is not VisualizzaOperaView:
            PopupMessage.mostra_errore(
                self.__info_section,
                "Pagina non trovata",
                f"Si è verificato un errore: Non è stato trovata la pagina '{pagina_nome}'. "
                + f"Type trovato: {type(cur_pagina)}",
            )
            return

        # Setup pagina con i dati dell'opera
        cur_genere = self.__get_genere(cur_opera.get_id_genere())
        if not cur_genere:
            PopupMessage.mostra_errore(
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

        lista_regie = self.__get_regie_by_opera(cur_opera.get_id())

        cur_pagina.set_data(opera_data, cur_genere.get_nome(), lista_regie)

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)

    def __nuova_opera(self) -> None:
        """Carica la pagina `NuovaOperaView`, dove l'utente può inserire i dati
        necessari per creare un'opera."""
        # Ottieni la pagina NuovaOperaView
        from view.info.pagine import NuovaOperaView

        cur_pagina_dict: dict[str, Optional[QWidget]] = {"value": None}
        pagina_nome = Pagina.NUOVA_OPERA
        self.getNavPageRequest.emit(pagina_nome, cur_pagina_dict)
        cur_pagina: Optional[QWidget] = cur_pagina_dict.get("value")

        if type(cur_pagina) is not NuovaOperaView:
            PopupMessage.mostra_errore(
                self.__info_section,
                "Pagina non trovata",
                f"Si è verificato un errore: Non è stato trovata la pagina '{pagina_nome}'. "
                + f"Type trovato: {type(cur_pagina)}",
            )
            return

        # Setup pagina pulendo i campi
        cur_pagina.setup_genere_combobox(self.__get_generi())
        cur_pagina.reset_pagina()

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)

    def __modifica_opera(self, id_: int) -> None:
        """Carica la pagina `ModificaOperaView`, con i dati dell'opera indicata
        inseriti nei campo di input.

        :param id_: id dell'opera da modificare
        """
        # Copia dell'opera da modificare
        cur_opera = self.__get_opera(id_)
        if not cur_opera:
            PopupMessage.mostra_errore(
                self.__info_section,
                "Opera inesistente",
                f"Non è presente nessuna opera con id {id_}.",
            )
            return

        # Ottieni la pagina ModificaOperaView
        from view.info.pagine import ModificaOperaView

        cur_pagina_dict: dict[str, Optional[QWidget]] = {"value": None}
        pagina_nome = Pagina.MODIFICA_OPERA
        self.getNavPageRequest.emit(pagina_nome, cur_pagina_dict)
        cur_pagina: Optional[QWidget] = cur_pagina_dict.get("value")

        if type(cur_pagina) is not ModificaOperaView:
            PopupMessage.mostra_errore(
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
        cur_pagina.setup_genere_combobox(self.__get_generi())
        cur_pagina.set_data(opera_data)

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)

    def __nuovo_genere(self) -> None:
        """Carica la pagina `NuovoGenereView`, dove l'utente può inserire i dati
        necessari per creare un genere."""
        # Ottieni la pagina NuovoGenereView
        from view.info.pagine import NuovoGenereView

        cur_pagina_dict: dict[str, Optional[QWidget]] = {"value": None}
        pagina_nome = Pagina.NUOVO_GENERE
        self.getNavPageRequest.emit(pagina_nome, cur_pagina_dict)
        cur_pagina: Optional[QWidget] = cur_pagina_dict.get("value")

        if type(cur_pagina) is not NuovoGenereView:
            PopupMessage.mostra_errore(
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

    def __modifica_genere(self, id_: int) -> None:
        """Carica la pagina `ModificaGenereView`, con i dati del genere indicato
        inseriti nei campo di input.

        :param id_: id del genere da modificare
        """
        # Copia del genere da modificare
        cur_genere = self.__get_genere(id_)
        if not cur_genere:
            PopupMessage.mostra_errore(
                self.__info_section,
                "Genere inesistente",
                f"Non è presente nessun genere con id {id_}.",
            )
            return

        # Ottieni la pagina ModificaGenereView
        from view.info.pagine import ModificaGenereView

        cur_pagina_dict: dict[str, Optional[QWidget]] = {"value": None}
        pagina_nome = Pagina.MODIFICA_GENERE
        self.getNavPageRequest.emit(pagina_nome, cur_pagina_dict)
        cur_pagina: Optional[QWidget] = cur_pagina_dict.get("value")

        if type(cur_pagina) is not ModificaGenereView:
            PopupMessage.mostra_errore(
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
