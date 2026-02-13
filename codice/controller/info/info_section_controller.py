from functools import partial
from typing import Optional

from core.controller import AbstractSectionController

from controller.navigation import Pagina

from model.model.model import Model
from model.pianificazione.opera import Opera
from model.pianificazione.genere import Genere
from model.pianificazione.regia import Regia
from model.exceptions import OggettoInUsoException

from view.info.pagine import InfoSectionView
from view.info.widgets import OperaDisplay, GenereDisplay
from view.info.utils import OperaPageData, GenerePageData

from view.utils.list_widgets import ListLayout
from view.utils import mostra_error_popup
from view.style.ui_style import WidgetRole


class InfoSectionController(AbstractSectionController):
    """Gestice la sezione Info (`InfoSectionView`) dell'app."""

    _view_section: InfoSectionView

    def __init__(self, model: Model, info_s: InfoSectionView):
        if type(info_s) is not InfoSectionView:
            raise TypeError("Atteso InfoSectionView per info_s.")

        super().__init__(model, info_s)

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    def _connect_signals(self) -> None:
        super()._connect_signals()

        # Display delle istanze del model
        self._view_section.displayOpereRequest.connect(  # type:ignore
            self.__display_opere
        )
        self._view_section.displayGeneriRequest.connect(  # type:ignore
            self.__display_generi
        )

        # Setup delle pagine di creazione
        self._view_section.nuovaOperaRequest.connect(  # type:ignore
            self.__nuova_opera
        )
        self._view_section.nuovoGenereRequest.connect(  # type:ignore
            self.__nuovo_genere
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __get_opera(self, id_: int) -> Optional[Opera]:
        return self._model.get_opera(id_)

    def __get_opere(self) -> list[Opera]:
        return self._model.get_opere()

    def __get_opere_by_nome(self, nome: str) -> list[Opera]:
        return self._model.get_opere_by_nome(nome)

    def __elimina_opera(self, id_: int) -> None:
        self._model.elimina_opera(id_)

    def __get_genere(self, id_: int) -> Optional[Genere]:
        return self._model.get_genere(id_)

    def __get_generi(self) -> list[Genere]:
        return self._model.get_generi()

    def __elimina_genere(self, id_: int) -> None:
        self._model.elimina_genere(id_)

    def __get_regie_by_opera(self, id_: int) -> list[Regia]:
        return self._model.get_regie_by_opera(id_)

    def __display_opere(self, layout_opere: ListLayout) -> None:
        """Mostra a schermo alcune informazioni delle opere salvate ed assegna a
        ciascuna pulsanti per visualizzarle in dettaglio, modificarle o eliminarle.

        :param layout_opere: layout dove saranno caricate tutte le opere
        """
        # Verifica se c'è un filtro di ricerca
        filtro = self._view_section.filtro_ricerca

        lista_opere = (
            self.__get_opere() if not filtro else self.__get_opere_by_nome(filtro)
        )

        if not lista_opere:
            layout_opere.mostra_msg_lista_vuota()
            return

        # Funzione di eliminazione per le opere
        def on_conferma(widget_opera: OperaDisplay, id_: int) -> None:
            """Prova ad eliminare l'istanza di Opera.

            :param widget_opera: widget associato all'`Opera` da eliminare
            :param id\\_: id dell'opera da eliminare
            """
            try:
                self.__elimina_opera(id_)
            except OggettoInUsoException as exc:
                widget_opera.annulla_elimina()
                mostra_error_popup(self._view_section, "Opera in uso", str(exc))
            else:
                self._view_section.aggiorna_pagina()

        for opera in lista_opere:
            current_opera = OperaDisplay(
                opera, editable=self._view_section.is_admin
            )  # - Esta vaina mejor que la guarde el controller y no las misma página

            current_opera.visualizzaRequest.connect(  # type:ignore
                self.__visualizza_opera
            )

            current_opera.modificaRequest.connect(  # type:ignore
                self.__modifica_opera
            )

            current_opera.eliminaConfermata.connect(  # type:ignore
                partial(on_conferma, current_opera, opera.get_id())
            )

            layout_opere.aggiungi_list_item(current_opera, WidgetRole.ITEM_CARD)

    def __display_generi(self, layout_generi: ListLayout) -> None:
        """Mostra a schermo le informazioni dei generi salvati ed assegna a
        ciascuno dei pulsanti per modificarli o eliminarli.

        :param layout_generi: layout dove saranno caricati tutti i generi
        """
        lista_generi = self.__get_generi()

        # Verifica che la lista non sia vuota
        if not lista_generi:
            layout_generi.mostra_msg_lista_vuota()
            return

        # Funzione di eliminazione per i generi
        def on_conferma(widget_genere: GenereDisplay, id_: int) -> None:
            """Prova ad eliminare l'istanza di Genere.

            :param widget_genere: widget associato al `Genere` da eliminare
            :param id\\_: id del genere da eliminare
            """
            try:
                self.__elimina_genere(id_)
            except OggettoInUsoException as exc:
                widget_genere.annulla_elimina()
                mostra_error_popup(self._view_section, "Genere in uso", str(exc))
            else:
                self._view_section.aggiorna_pagina()

        # Mostra tutti i generi salvati a schermo
        for genere in lista_generi:
            current_genere = GenereDisplay(genere, editable=self._view_section.is_admin)

            # Setup della pagina di modifica dei generi
            current_genere.modificaRequest.connect(  # type:ignore
                self.__modifica_genere
            )

            current_genere.eliminaConfermata.connect(  # type:ignore
                partial(on_conferma, current_genere, genere.get_id())
            )

            layout_generi.aggiungi_list_item(current_genere, WidgetRole.ITEM_CARD)

    def __visualizza_opera(self, id_: int) -> None:
        """Carica la pagina `VisualizzaOperaView` con i dati relativi all'opera
        indicata.

        :param id_: id dell'opera da visualizzare
        """
        # Copia dell'opera da visualizzare
        current_opera = self.__get_opera(id_)
        if not current_opera:
            mostra_error_popup(
                self._view_section,
                "Opera inesistente",
                f"Non è presente nessuna opera con id {id_}.",
            )
            return

        # Ottieni la pagina VisualizzaOperaView
        from view.info.pagine import VisualizzaOperaView

        pagina_nome = Pagina.VISUALIZZA_OPERA
        current_pagina = self._ottieni_pagina(pagina_nome)
        if type(current_pagina) is not VisualizzaOperaView:
            self._mostra_msg_pagina_non_trovata(pagina_nome, type(current_pagina))
            return

        # Setup pagina con i dati dell'opera
        genere_associato = self.__get_genere(current_opera.get_id_genere())
        if not genere_associato:
            mostra_error_popup(
                self._view_section,
                "Genere inesistente",
                f"Non è presente nessun genere con id {current_opera.get_id_genere()}.",
            )
            return

        opera_data = OperaPageData(
            id=current_opera.get_id(),
            nome=current_opera.get_nome(),
            trama=current_opera.get_trama(),
            id_genere=current_opera.get_id_genere(),
            compositore=current_opera.get_compositore(),
            librettista=current_opera.get_librettista(),
            atti=current_opera.get_numero_atti(),
            data_rappresentazione=current_opera.get_data_prima_rappresentazione(),
            teatro_rappresentazione=current_opera.get_teatro_prima_rappresentazione(),
        )

        lista_regie = self.__get_regie_by_opera(current_opera.get_id())

        current_pagina.set_data(opera_data, genere_associato.get_nome(), lista_regie)

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)

    def __nuova_opera(self) -> None:
        """Carica la pagina `NuovaOperaView`, dove l'utente può inserire i dati
        necessari per creare un'opera."""
        # Ottieni la pagina NuovaOperaView
        from view.info.pagine import NuovaOperaView

        pagina_nome = Pagina.NUOVA_OPERA
        current_pagina = self._ottieni_pagina(pagina_nome)
        if type(current_pagina) is not NuovaOperaView:
            self._mostra_msg_pagina_non_trovata(pagina_nome, type(current_pagina))
            return

        # Setup pagina pulendo i campi
        current_pagina.setup_genere_combobox(self.__get_generi())
        current_pagina.reset_pagina()

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)

    def __modifica_opera(self, id_: int) -> None:
        """Carica la pagina `ModificaOperaView`, con i dati dell'opera indicata
        inseriti nei campo di input.

        :param id_: id dell'opera da modificare
        """
        # Copia dell'opera da modificare
        current_opera = self.__get_opera(id_)
        if not current_opera:
            mostra_error_popup(
                self._view_section,
                "Opera inesistente",
                f"Non è presente nessuna opera con id {id_}.",
            )
            return

        # Ottieni la pagina ModificaOperaView
        from view.info.pagine import ModificaOperaView

        pagina_nome = Pagina.MODIFICA_OPERA
        current_pagina = self._ottieni_pagina(pagina_nome)
        if type(current_pagina) is not ModificaOperaView:
            self._mostra_msg_pagina_non_trovata(pagina_nome, type(current_pagina))
            return

        # Salva i dati dentro di un container
        opera_data = OperaPageData(
            id=current_opera.get_id(),
            nome=current_opera.get_nome(),
            trama=current_opera.get_trama(),
            id_genere=current_opera.get_id_genere(),
            compositore=current_opera.get_compositore(),
            librettista=current_opera.get_librettista(),
            atti=current_opera.get_numero_atti(),
            data_rappresentazione=current_opera.get_data_prima_rappresentazione(),
            teatro_rappresentazione=current_opera.get_teatro_prima_rappresentazione(),
        )

        # Setup pagina con i data dell'opera
        current_pagina.setup_genere_combobox(self.__get_generi())
        current_pagina.set_data(opera_data)

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)

    def __nuovo_genere(self) -> None:
        """Carica la pagina `NuovoGenereView`, dove l'utente può inserire i dati
        necessari per creare un genere."""
        # Ottieni la pagina NuovoGenereView
        from view.info.pagine import NuovoGenereView

        pagina_nome = Pagina.NUOVO_GENERE
        current_pagina = self._ottieni_pagina(pagina_nome)
        if type(current_pagina) is not NuovoGenereView:
            self._mostra_msg_pagina_non_trovata(pagina_nome, type(current_pagina))
            return

        # Setup pagina pulendo i campi
        current_pagina.reset_pagina()

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)

    def __modifica_genere(self, id_: int) -> None:
        """Carica la pagina `ModificaGenereView`, con i dati del genere indicato
        inseriti nei campo di input.

        :param id_: id del genere da modificare
        """
        # Copia del genere da modificare
        current_genere = self.__get_genere(id_)
        if not current_genere:
            mostra_error_popup(
                self._view_section,
                "Genere inesistente",
                f"Non è presente nessun genere con id {id_}.",
            )
            return

        # Ottieni la pagina ModificaGenereView
        from view.info.pagine import ModificaGenereView

        pagina_nome = Pagina.MODIFICA_GENERE
        current_pagina = self._ottieni_pagina(pagina_nome)
        if type(current_pagina) is not ModificaGenereView:
            self._mostra_msg_pagina_non_trovata(pagina_nome, type(current_pagina))
            return

        # Salva i dati dentro di un container
        genere_data = GenerePageData(
            id=current_genere.get_id(),
            nome=current_genere.get_nome(),
            descrizione=current_genere.get_descrizione(),
        )

        # Setup pagina con i data del genere
        current_pagina.set_data(genere_data)

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)
