from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal, QObject
from functools import partial
from typing import Optional

from controller.navigation import Pagina

from model.model import Model
from model.pianificazione.opera import Opera
from model.pianificazione.regia import Regia, Spettacolo
from model.exceptions import OggettoInUsoException

from view.info.pagine import VisualizzaOperaView
from view.info.widgets import RegiaDisplay
from view.info.utils import RegiaPageData

from view.utils.list_widgets import ListLayout
from view.utils import PopupMessage


class VisualizzaOperaController(QObject):
    """Gestice la pagina `VisualizzaOperaView` dell'app.

    Segnali
    ---
    - `goBackRequest()`: emesso per tornare alla pagina `InfoSectionView`;
    - `goToPageRequest(Pagina, bool)`: emesso per visualizzare un'altra pagina;
    - `getPageRequest(Pagina, dict)`: emesso per ottenere la pagina che vendrà visualizzata.
    """

    goBackRequest: pyqtSignal = pyqtSignal()
    goToPageRequest: pyqtSignal = pyqtSignal(Pagina, bool)
    getPageRequest: pyqtSignal = pyqtSignal(Pagina, dict)

    def __init__(self, model: Model, opera_v: VisualizzaOperaView):
        super().__init__()
        self.__model = model
        self.__visualizza_opera_view = opera_v

        self.__connect_signals()

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    def __connect_signals(self) -> None:
        # Torna indietro dalla pagina VisualizzaOperaView
        self.__visualizza_opera_view.tornaIndietroRequest.connect(  # type:ignore
            self.goBackRequest.emit
        )

        # Display della Lista Regie
        self.__visualizza_opera_view.displayRegieRequest.connect(  # type:ignore
            self.__display_regie
        )

        # Setup della pagina di creazione di regie
        self.__visualizza_opera_view.nuovaRegiaRequest.connect(  # type:ignore
            self.__nuova_regia
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __get_opera(self, id_: int) -> Optional[Opera]:
        return self.__model.get_opera(id_)

    def __get_spettacolo(self, id_: int) -> Optional[Spettacolo]:
        return self.__model.get_spettacolo(id_)

    def __get_regie_by_opera(self, id_: int) -> list[Regia]:
        return self.__model.get_regie_by_opera(id_)

    def __elimina_regia(self, id_: int) -> None:
        ...
        # - self.__model.elimina_spettacolo(id_)

    def __display_regie(self, layout_regie: ListLayout) -> None:
        """Mostra a schermo le informazioni delle regie salvati e associate ad
        un'opera ed assegna a ciascuna pulsanti per modificarli o eliminarli.

        :param layout: layout dove saranno caricate tutti le regie
        """
        lista_regie = self.__get_regie_by_opera(
            self.__visualizza_opera_view.id_cur_opera
        )

        # Verifica che la lista non sia vuota
        if not lista_regie:
            layout_regie.if_lista_vuota()
            return

        # Funzione di elimina per le regie
        def on_conferma(widget_regia: RegiaDisplay, id_: int) -> None:
            """Prova di eliminare l'istanza di regia.

            :param id_: id della regia da eliminare
            """
            try:
                self.__elimina_regia(id_)
            except OggettoInUsoException as exc:
                widget_regia.annulla_elimina()
                PopupMessage.mostra_errore(
                    self.__visualizza_opera_view,
                    "Regia in uso",
                    f"Si è verificato un errore: {exc}",
                )
            else:
                self.__visualizza_opera_view.aggiorna_pagina()

        # Mostra tutti le regie salvate a schermo
        for regia in lista_regie:
            cur_regia = RegiaDisplay(
                regia, editable=self.__visualizza_opera_view.is_admin
            )

            # Setup della pagina di modifica delle regie
            cur_regia.modificaRequest.connect(  # type:ignore
                self.__modifica_regia
            )

            cur_regia.eliminaConfermata.connect(  # type:ignore
                partial(on_conferma, cur_regia, regia.get_id())
            )

            # Aggiungi cur_regia al layout di ListaRegie
            self.__visualizza_opera_view.aggiungi_widget_a_layout(
                cur_regia, layout_regie
            )

    def __nuova_regia(self) -> None:
        """Carica la pagina `NuovaRegiaView`, dove l'utente può inserire i dati
        necessari per creare una regia."""
        # Ottieni la pagina NuovaOperaView
        from view.info.pagine import NuovaRegiaView

        cur_pagina_dict: dict[str, Optional[QWidget]] = {"value": None}
        pagina_nome = Pagina.NUOVA_REGIA
        self.getPageRequest.emit(pagina_nome, cur_pagina_dict)
        cur_pagina: Optional[QWidget] = cur_pagina_dict.get("value")

        if type(cur_pagina) is not NuovaRegiaView:
            PopupMessage.mostra_errore(
                self.__visualizza_opera_view,
                "Pagina non trovata",
                f"Si è verificato un errore: Non è stato trovata la pagina '{pagina_nome}'. "
                + f"Type trovato: {type(cur_pagina)}",
            )
            return

        # Setup pagina pulendo i campi
        cur_id_opera = self.__visualizza_opera_view.id_cur_opera
        cur_opera = self.__get_opera(cur_id_opera)

        if not isinstance(cur_opera, Opera):
            PopupMessage.mostra_errore(
                self.__visualizza_opera_view,
                "Opera inesistente",
                f"Non è presente nessuna opera con id {cur_id_opera}.",
            )
            return

        cur_pagina.setup_opera_combobox(cur_opera)
        cur_pagina.reset_pagina()

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)

    def __modifica_regia(self, id_: int) -> None:
        """Carica la pagina `ModificaRegiaView`, con i dati della regia indicata
        inseriti nei campo di input.

        :param id_: id della regia da modificare
        """
        # Copia della regia da modificare
        cur_regia = self.__get_spettacolo(id_)
        if not isinstance(cur_regia, Regia):
            PopupMessage.mostra_errore(
                self.__visualizza_opera_view,
                "Regia inesistente",
                f"Non è presente nessuna regia con id {id_}.",
            )
            return

        # Ottieni la pagina ModificaRegiaView
        from view.info.pagine import ModificaRegiaView

        cur_pagina_dict: dict[str, Optional[QWidget]] = {"value": None}
        pagina_nome = Pagina.MODIFICA_REGIA
        self.getPageRequest.emit(pagina_nome, cur_pagina_dict)
        cur_pagina: Optional[QWidget] = cur_pagina_dict.get("value")

        if type(cur_pagina) is not ModificaRegiaView:
            PopupMessage.mostra_errore(
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

        cur_opera = self.__get_opera(cur_regia.get_id_opera())
        if not isinstance(cur_opera, Opera):
            PopupMessage.mostra_errore(
                self.__visualizza_opera_view,
                "Opera inesistente",
                f"Non è presente nessuna opera con id '{cur_regia.get_id_opera()}'.",
            )
            return

        # Setup pagina con i data del genere
        cur_pagina.setup_opera_combobox(cur_opera)
        cur_pagina.set_data(regia_data)

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)
