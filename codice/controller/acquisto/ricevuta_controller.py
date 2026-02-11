from PyQt6.QtCore import QObject, pyqtSignal

from controller.navigation import Pagina

from model.model.model import Model

# from model.organizzazione.prenotazione import Prenotazione
# from model.organizzazione.occupazione import Occupazione
# from model.exceptions import DatoIncongruenteException, IdOccupatoException

from view.acquisto.pagine import RicevutaView
from view.acquisto.widgets import EventoPostiDisplay

from view.utils.list_widgets import ListLayout

# from view.utils import PopupMessage

from view.style.ui_style import WidgetRole


class RicevutaController(QObject):
    """Gestice la pagina `RicevutaView` dell'app."""

    goToSectionRequest = pyqtSignal(Pagina)

    def __init__(self, model: Model, pagina_ricevuta: RicevutaView):
        super().__init__()

        self.__model = model
        self.__pagina_ricevuta = pagina_ricevuta

        self.__connect_signals()

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    def __connect_signals(self) -> None:
        self.__pagina_ricevuta.displayPostiSceltiRequest.connect(  # type:ignore
            self.__display_posti_scelti
        )

        self.__pagina_ricevuta.stampaRicevuta.connect(  # type:ignore
            self.__stampa_ricevuta_e_crea_prenotazione
        )

        self.__pagina_ricevuta.ritornaAllaMainPage.connect(  # type:ignore
            self.__ritorna_alla_main_page
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    # def __aggiungi_prenotazione(self, prenotazione: Prenotazione) -> None:
    #     self.__model.aggiungi_prenotazione(prenotazione)

    # def __aggiungi_occupazione(self, occupazione: Occupazione) -> None:
    #     self.__model.aggiungi_occupazione(occupazione)

    def __display_posti_scelti(self, layout_posti_scelti: ListLayout) -> None:
        """Mostra a schermo le informazioni dei posti prenotati.

        :param layout_posti_scelti: layout dove saranno caricati tutti i posti scelti
        """
        pagina = self.__pagina_ricevuta
        evento, lista_sezione_posti = pagina.lista_posti_scelti

        if evento is None or not lista_sezione_posti:
            layout_posti_scelti.mostra_msg_lista_vuota()
            return

        current_posto_scelto = EventoPostiDisplay(evento, lista_sezione_posti)

        layout_posti_scelti.aggiungi_list_item(
            current_posto_scelto, WidgetRole.ITEM_CARD
        )

    def __stampa_ricevuta_e_crea_prenotazione(self) -> None:
        # Logica per stampare ricevuta
        ...  # - CÓMO COÑO HAGO ESTO? TOCA ESTUDIAR

        self.__pagina_ricevuta.abilita_btn_fine(True)

        # pagina = self.__pagina_ricevuta

        # # Ottieni i dati per creare la prenotazione
        # nominativo = "texto de mierda"
        # tempo_emission = pagina.tempo_emission

        # # Tenta di creare la nuova prenotazione
        # try:
        #     nuova_prenotazione = Prenotazione(nominativo, tempo_emission)
        # except DatoIncongruenteException as exc:
        #     # È stato trovato un dato non valido
        #     PopupMessage.mostra_errore(
        #         pagina,
        #         "Impossibile creare prenotazione",
        #         f"Si è verificato un errore: {exc}",
        #     )
        # else:
        #     try:
        #         self.__aggiungi_prenotazione(nuova_prenotazione)
        #     except IdOccupatoException as exc:
        #         # Esiste già una prenotazione con quell'id
        #         PopupMessage.mostra_errore(
        #             pagina,
        #             "ID Prenotazione occupato",
        #             f"Si è verificato un errore: {exc}",
        #         )

        #     # Tenta di creare le istanze di Occupazione
        #     lista_eventi_posti = pagina.lista_posti_scelti
        #     for e, sp in lista_eventi_posti:
        #         for _, posti in sp:
        #             for p in posti:
        #                 try:
        #                     nuova_occupazione = Occupazione(
        #                         e.get_id(), p.get_id(), nuova_prenotazione.get_id()
        #                     )
        #                 except DatoIncongruenteException as exc:
        #                     # È stato trovato un dato non valido
        #                     PopupMessage.mostra_errore(
        #                         pagina,
        #                         "Impossibile occupare posto",
        #                         f"Si è verificato un errore: {exc}",
        #                     )
        #                 else:
        #                     try:
        #                         self.__aggiungi_occupazione(nuova_occupazione)
        #                     except IdOccupatoException as exc:
        #                         # Esiste già una Occupazione con quell'id
        #                         PopupMessage.mostra_errore(
        #                             pagina,
        #                             "Impossibile occupare posto",
        #                             f"Si è verificato un errore: {exc}",
        #                         )

        #     pagina.abilita_btn_fine(True)

    def __ritorna_alla_main_page(self) -> None:
        self.goToSectionRequest.emit(Pagina.SEZIONE_ACQUISTO)
