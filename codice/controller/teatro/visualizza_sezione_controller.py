from PyQt6.QtWidgets import QWidget
from functools import partial
from typing import Optional, override

from core.controller import AbstractVisualizzaController

from controller.navigation import Pagina

from model.model.model import Model
from model.organizzazione.posto import Posto
from model.exceptions import (
    OggettoInUsoException,
    DatoIncongruenteException,
    IdOccupatoException,
    OccupatoException,
)

from view.teatro.pagine import VisualizzaSezioneView
from view.teatro.utils import PostoPageData
from view.teatro.widgets import PostoDisplay

from view.utils.list_widgets import ListLayout
from view.utils import PopupMessage


CAMPI_NECESSARI = "<b>ATTENZIONE</b>: È necessario compilare tutti i campi d'input."
FORMATO_SVAGLIATO = (
    "<b>ATTENZIONE</b>: Il formato deve essere ordinato, e.g. 6-3 non è valido."
)


class VisualizzaSezioneController(AbstractVisualizzaController):
    """Gestice la pagina `VisualizzaSezioneView` dell'app.

    Segnali
    ---
    - `goBackRequest()`: emesso per tornare alla pagina `TeatroSectionView`.
    """

    _view_page: VisualizzaSezioneView

    def __init__(self, model: Model, sezione_v: VisualizzaSezioneView):
        if type(sezione_v) is not VisualizzaSezioneView:
            raise TypeError("Atteso VisualizzaSezioneView per sezione_v.")

        super().__init__(model, sezione_v)

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    @override
    def _connect_signals(self) -> None:
        super()._connect_signals()

        self._view_page.displayPostiRequest.connect(  # type:ignore
            self.__display_posti
        )

        self._view_page.aggiungiPostoRequest.connect(  # type:ignore
            self.__inizia_salvataggio
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __get_posto(self, id_: int) -> Optional[Posto]:
        return self._model.get_posto(id_)

    def __get_posti_by_sezione(self, id_: int) -> list[Posto]:
        return self._model.get_posti_by_sezione(id_)

    def __aggiungi_posto(self, posto: Posto) -> None:
        self._model.aggiungi_posto(posto)

    def __elimina_posto(self, id_: int) -> None:
        self._model.elimina_posto(id_)

    def __display_posti(self, layout_posti: ListLayout) -> None:
        """Mostra a schermo il numero dei posti salvati e associati ad una sezione
        ed assegna a ciascuno pulsanti per modificarli o eliminarli.

        :param layout_posti: layout dove saranno caricate tutti i posti
        """
        lista_posti = self.__get_posti_by_sezione(self._view_page.id_current_sezione)

        if not lista_posti:
            layout_posti.mostra_msg_lista_vuota()
            return

        # Ordina la lista per renderla più chiara nella UI
        lista_posti = sorted(lista_posti, key=lambda x: (x.get_fila(), x.get_numero()))

        # Funzione di eliminazione per le regie
        def on_conferma(id_: int) -> None:
            """Prova ad eliminare l'istanza di `Posto`.

            :param id_: id del posto da eliminare
            """
            try:
                self.__elimina_posto(id_)
            except OggettoInUsoException as exc:
                PopupMessage.mostra_errore(
                    self._view_page,
                    "Posto in uso",
                    f"Si è verificato un errore: {exc}",
                )
            else:
                self._view_page.aggiorna_pagina()

        for posto in lista_posti:
            current_posto = PostoDisplay(posto)

            current_posto.modificaRequest.connect(  # type:ignore
                self.__modifica_posto
            )

            current_posto.eliminaConfermata.connect(  # type:ignore
                partial(on_conferma, posto.get_id())
            )

            layout_posti.aggiungi_list_item(current_posto)

    def __inizia_salvataggio(self, is_only_one: bool) -> None:
        """Salva l'istanza o istanze di `Posto` nel `GestorePosti`.

        :param is_only_one: verifica se si deve creare un'instanza o multipli
        """
        if is_only_one:
            self.__salva_singolo_posto()
        else:
            self.__salva_multipli_posti()

    def __salva_singolo_posto(self) -> None:
        pagina = self._view_page

        fila = pagina.fila.text()
        numero = pagina.single_numero.value()
        id_sezione = pagina.id_current_sezione

        try:
            nuovo_posto = Posto(fila, numero, id_sezione)
        except DatoIncongruenteException as exc:
            pagina.mostra_msg_input_error(CAMPI_NECESSARI)
            PopupMessage.mostra_errore(
                pagina,
                "Input non valido",
                f"Si è verificato un errore: {exc}",
            )
        else:
            pagina.mostra_msg_input_error("")

            try:
                self.__aggiungi_posto(nuovo_posto)
            except OccupatoException as exc:
                # Esiste già un posto con quel numero
                PopupMessage.mostra_errore(
                    pagina,
                    "Numero Posto occupato",
                    f"Si è verificato un errore: {exc}",
                )
            except IdOccupatoException as exc:
                # Esiste già un posto con quell'id
                PopupMessage.mostra_errore(
                    pagina,
                    "ID Posto occupato",
                    f"Si è verificato un errore: {exc}",
                )
            else:
                pagina.aggiorna_pagina()

    def __salva_multipli_posti(self) -> None:
        pagina = self._view_page

        def parse_ranges(text: str) -> list[int]:
            result: set[int] = set()

            for part in text.split(","):
                part = part.strip()
                if "-" in part:
                    start, end = map(int, part.split("-"))
                    if start > end:
                        raise ValueError("Rango non valido.")
                    result.update(range(start, end + 1))
                else:
                    result.add(int(part))

            return sorted(result)

        if not pagina.range_numeri.text().strip():
            pagina.mostra_msg_input_error(CAMPI_NECESSARI)
            PopupMessage.mostra_errore(
                pagina,
                "Input non valido",
                "Si è verificato un errore: È necessari inserire un rango.",
            )
            return

        try:
            numeri = parse_ranges(pagina.range_numeri.text())
        except ValueError as exc:
            pagina.mostra_msg_input_error(FORMATO_SVAGLIATO)
            PopupMessage.mostra_errore(
                pagina,
                "Input non valido",
                f"Si è verificato un errore: {exc}",
            )
            return

        fila = pagina.fila.text()
        id_sezione = pagina.id_current_sezione

        lista_posti: list[Posto] = []
        for num in numeri:
            try:
                nuovo_posto = Posto(fila, num, id_sezione)
            except DatoIncongruenteException as exc:
                pagina.mostra_msg_input_error(CAMPI_NECESSARI)
                PopupMessage.mostra_errore(
                    pagina,
                    "Input non valido",
                    f"Si è verificato un errore: {exc}",
                )
                return
            else:
                lista_posti.append(nuovo_posto)

        pagina.mostra_msg_input_error("")
        posti_errati: list[str] = []
        for posto in lista_posti:
            try:
                self.__aggiungi_posto(posto)
            except (IdOccupatoException, OccupatoException) as exc:
                posti_errati.append(
                    f"Posto {posto.get_fila()}{posto.get_numero()}: {exc}"
                )

        pagina.aggiorna_pagina()

        if posti_errati:
            error_msg: str = ""
            for msg in posti_errati:
                error_msg = error_msg + f"{msg}\n"
            PopupMessage.mostra_errore(
                pagina,
                "Posti non validi",
                f"Si sono verificati i seguenti errori:\n{error_msg}",
            )

    def __modifica_posto(self, id_: int) -> None:
        """Carica la pagina `ModificaPostoView`, con i dati del posto indicato
        inseriti nei campo di input.

        :param id_: id del posto da modificare
        """
        # Copia del posto da modificare
        current_posto = self.__get_posto(id_)
        if not current_posto:
            PopupMessage.mostra_errore(
                self._view_page,
                "Posto inesistente",
                f"Non è presente nessun posto con id {id_}.",
            )
            return

        # Ottieni la pagina ModificaPostoView
        from view.teatro.pagine import ModificaPostoView

        cur_pagina_dict: dict[str, Optional[QWidget]] = {"value": None}
        pagina_nome = Pagina.MODIFICA_POSTO
        self.getPageRequest.emit(pagina_nome, cur_pagina_dict)
        current_pagina: Optional[QWidget] = cur_pagina_dict.get("value")

        if type(current_pagina) is not ModificaPostoView:
            PopupMessage.mostra_errore(
                self._view_page,
                "Pagina non trovata",
                f"Si è verificato un errore: Non è stato trovata la pagina '{pagina_nome}'. "
                + f"Type trovato: {type(current_pagina)}",
            )
            return

        # Salva i dati dentro di un container
        posto_data = PostoPageData(
            id=current_posto.get_id(),
            fila=current_posto.get_fila(),
            numero=current_posto.get_numero(),
            id_sezione=current_posto.get_id_sezione(),
        )

        # Setup pagina con i data del posto
        current_pagina.set_data(posto_data)

        # Apri la pagina
        self.goToPageRequest.emit(pagina_nome, True)
