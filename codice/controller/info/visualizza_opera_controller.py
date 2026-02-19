from PyQt6.QtWidgets import QWidget
from functools import partial
from typing import Optional, override

from core.controller import AbstractVisualizzaController

from controller.navigation import Pagina

from model.model.model import Model
from model.pianificazione.opera import Opera
from model.pianificazione.regia import Regia, Spettacolo
from model.exceptions import OggettoInUsoException

from view.info.pagine import VisualizzaOperaPage
from view.info.widgets import RegiaDisplay
from view.info.utils import RegiaData

from view.utils.list_widgets import ListLayout
from view.utils import mostra_error_popup


class VisualizzaOperaController(AbstractVisualizzaController):
    """Gestice la pagina `VisualizzaOperaPage` dell'app.

    Segnali
    ---
    - `goBackRequest()`: emesso per tornare alla pagina `InfoSection`;
    """

    _view_page: VisualizzaOperaPage

    def __init__(self, model: Model, opera_v: VisualizzaOperaPage):
        if type(opera_v) is not VisualizzaOperaPage:
            raise TypeError("Atteso VisualizzaOperaPage per opera_v.")

        super().__init__(model, opera_v)

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    @override
    def _connect_signals(self) -> None:
        super()._connect_signals()

        self._view_page.displayRegieRequest.connect(  # type:ignore
            self.__display_regie
        )

        self._view_page.nuovaRegiaRequest.connect(  # type:ignore
            self.__nuova_regia
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __get_opera(self, id_: int) -> Optional[Opera]:
        return self._model.get_opera(id_)

    def __get_spettacolo(self, id_: int) -> Optional[Spettacolo]:
        return self._model.get_spettacolo(id_)

    def __get_regie_by_opera(self, id_: int) -> list[Regia]:
        return self._model.get_regie_by_opera(id_)

    def __elimina_regia(self, id_: int) -> None:
        self._model.elimina_spettacolo(id_)

    def __display_regie(self, layout_regie: ListLayout) -> None:
        """Mostra a schermo le informazioni delle regie salvate e associate ad
        un'opera ed assegna a ciascuna pulsanti per modificarle o eliminarle.

        :param layout_regie: layout dove saranno caricate tutti le regie
        """
        lista_regie = self.__get_regie_by_opera(self._view_page.id_current_opera)

        if not lista_regie:
            layout_regie.mostra_msg_lista_vuota()
            return

        lista_regie = sorted(lista_regie, key=lambda x: (x.get_anno_produzione()))

        # Funzione di eliminazione per le regie
        def on_conferma(widget_regia: RegiaDisplay, id_: int) -> None:
            """Prova ad eliminare l'istanza di `Regia`.

            :param widget_regia: widget associato alla `Regia` da eliminare
            :param id\\_: id della regia da eliminare
            """
            try:
                self.__elimina_regia(id_)
            except OggettoInUsoException as exc:
                widget_regia.annulla_elimina()
                mostra_error_popup(self._view_page, "Regia in uso", str(exc))
            else:
                self._view_page.aggiorna_pagina()

        for regia in lista_regie:
            current_regia = RegiaDisplay(regia, editable=self._view_page.is_admin)

            current_regia.modificaRequest.connect(  # type:ignore
                self.__modifica_regia
            )

            current_regia.eliminaConfermata.connect(  # type:ignore
                partial(on_conferma, current_regia, regia.get_id())
            )

            layout_regie.aggiungi_list_item(current_regia)

    def __nuova_regia(self) -> None:
        """Carica la pagina `NuovaRegiaPage`, dove l'utente può inserire i dati
        necessari per creare una regia."""
        # Ottieni la pagina NuovaOperaPage
        from view.info.pagine import NuovaRegiaPage

        cur_pagina_dict: dict[str, Optional[QWidget]] = {"value": None}
        pagina_nome = Pagina.NUOVA_REGIA
        self.getPageRequest.emit(pagina_nome, cur_pagina_dict)
        current_pagina: Optional[QWidget] = cur_pagina_dict.get("value")

        if type(current_pagina) is not NuovaRegiaPage:
            mostra_error_popup(
                self._view_page,
                "Pagina non trovata",
                f"Non è stato trovata la pagina '{pagina_nome}'. "
                + f"Type trovato: {type(current_pagina)}",
            )
            return

        # Setup pagina pulendo i campi
        id_current_opera = self._view_page.id_current_opera
        current_opera = self.__get_opera(id_current_opera)

        if not isinstance(current_opera, Opera):
            mostra_error_popup(
                self._view_page,
                "Opera inesistente",
                f"Non è presente nessuna opera con id {id_current_opera}.",
            )
            return

        current_pagina.setup_opera_combobox(current_opera)
        current_pagina.reset_pagina()

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)

    def __modifica_regia(self, id_: int) -> None:
        """Carica la pagina `ModificaRegiaPage`, con i dati della regia indicata
        inseriti nei campo di input.

        :param id_: id della regia da modificare
        """
        # Copia della regia da modificare
        current_regia = self.__get_spettacolo(id_)
        if not isinstance(current_regia, Regia):
            mostra_error_popup(
                self._view_page,
                "Regia inesistente",
                f"Non è presente nessuna regia con id {id_}.",
            )
            return

        # Ottieni la pagina ModificaRegiaPage
        from view.info.pagine import ModificaRegiaPage

        cur_pagina_dict: dict[str, Optional[QWidget]] = {"value": None}
        pagina_nome = Pagina.MODIFICA_REGIA
        self.getPageRequest.emit(pagina_nome, cur_pagina_dict)
        current_pagina: Optional[QWidget] = cur_pagina_dict.get("value")

        if type(current_pagina) is not ModificaRegiaPage:
            mostra_error_popup(
                self._view_page,
                "Pagina non trovata",
                f"Non è stato trovata la pagina '{pagina_nome}'. "
                + f"Type trovato: {type(current_pagina)}",
            )
            return

        # Salva i dati dentro di un container
        regia_data = RegiaData(
            id=current_regia.get_id(),
            titolo=current_regia.get_titolo(),
            note=current_regia.get_note(),
            interpreti=current_regia.get_interpreti(),
            musicisti_e_direttori_artistici=current_regia.get_musicisti_e_direttori_artistici(),
            regista=current_regia.get_regista(),
            anno_produzione=current_regia.get_anno_produzione(),
            id_opera=current_regia.get_id_opera(),
        )

        opera_associata = self.__get_opera(current_regia.get_id_opera())
        if not isinstance(opera_associata, Opera):
            mostra_error_popup(
                self._view_page,
                "Opera inesistente",
                f"Non è presente nessuna opera con id '{current_regia.get_id_opera()}'.",
            )
            return

        # Setup pagina con i data del genere
        current_pagina.setup_opera_combobox(opera_associata)
        current_pagina.set_data(regia_data)

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)
