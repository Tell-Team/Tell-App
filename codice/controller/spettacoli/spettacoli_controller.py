from PyQt6.QtCore import pyqtSignal, QObject
from functools import partial

from model.model import Model

from view.spettacoli.pagine.spettacoli_section import SpettacoliSectionView
from view.messageView import MessageView


class SpettacoliController(QObject):
    """Gestice la sezione Spettacoli (`SpettacoliSectionView`) dell'app.

    Segnali:
    - logoutRequest(): emesso per eseguire la funzione di logout dall`AppContext`;
    - goToPageRequest(str, bool): emesso per visualizzare un'altra pagina;
    - goToSectionRequest(str): emesso per visualizzare un'altra pagina, senza salvarla
    nell'history del `NavigationController`;
    - getNavPageRequest(str, dict): emesso per ottenere la pagina che vendrà visualizzata.
    """

    logoutRequest = pyqtSignal()
    goToPageRequest = pyqtSignal(str, bool)
    goToSectionRequest = pyqtSignal(str)
    getNavPageRequest = pyqtSignal(str, dict)

    def __init__(
        self,
        model: Model,
        spettacoli_s: SpettacoliSectionView,
        message_v: MessageView,
    ) -> None:
        super().__init__()
        self.__model = model
        self.__spettacoli_section = spettacoli_s  # Sezione Spettacoli
        self.__message_view = message_v  # View dedicata ai popup

        self._connect_signals()

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    def _connect_signals(self) -> None:
        # Logout
        self.__spettacoli_section.logoutRequest.connect(  # type:ignore
            self.logoutRequest.emit  # - CORRIGGERE: Account ancora non implementato
        )
        # Visualizza Sezione Info
        self.__spettacoli_section.goToInfo.connect(  # type:ignore
            partial(self.goToSectionRequest.emit, "info_section")
        )
        # Visualizza Sezione Account
        self.__spettacoli_section.goToAccount.connect(  # type:ignore
            partial(self.goToSectionRequest.emit, "account_section")
        )

        # Display della Lista Spettacoli
        self.__spettacoli_section.displaySpettacoliRequest.connect(  # type:ignore
            self.display_spettacoli
        )

        # Setup della pagina di creazione di spettacoli
        self.__spettacoli_section.nuovoSpettacoloRequest.connect(  # type:ignore
            self.nuovo_spettacolo
        )

    # ------------------------- METODI PUBBLICI -------------------------

    def display_spettacoli(self) -> None: ...

    def nuovo_spettacolo(self) -> None: ...

    def modifica_spettacolo(self, id_: int) -> None: ...

    # # - QUESTI METODI GLI AVEVO CREATO NEL info_controller.py E IN TEORIA DEvOno RIFERIRSI AGLI
    # #   SPETTACOLI. QUINDI DEVONO ESSER MODIFICATI.
    # # - Funziona con la struttura di NuovaRegiaView e deve essere aggiorna se quella classe
    # #   è modificata. Comunque, è abbastanza coeso nel suo funzionamento.
    # def nuova_regia(self, id_opera: int):
    #     from view.info.nuova_regia import NuovaRegiaView

    #     cur_page: Optional[QWidget] = QWidget()
    #     self.getNavPageRequest.emit("nuova_regia", cur_page)

    #     if not isinstance(cur_page, NuovaRegiaView):
    #         raise TypeError(
    #             f"cur_page deve essere NuovaRegiaView. Type trovato: {type(cur_page)}"
    #         )

    #     # Setup default values
    #     cur_page.cur_id_opera = id_opera
    #     cur_page.regista.setText("")
    #     cur_page.anno.setValue(0)

    #     # Apri la pagina NuovoGenereView
    #     self.goToPageRequest.emit("nuova_regia", True)

    # def modifica_regia(self, id_: int, id_opera: int):
    #     # Get genere da modificare
    #     # - Non c'è una forma diretta di chiamare l'istanza da modificare
    #     cur_regia = next(
    #         (r for r in self.get_regie_by_opera(id_opera) if r.get_id() == id_), None
    #     )
    #     if not cur_regia:
    #         raise IdInesistenteException(f"Non è presente nessuna regia con id {id_}.")

    #     from view.info.modifica_regia import ModificaRegiaView

    #     cur_page: Optional[QWidget] = QWidget()
    #     self.getNavPageRequest.emit("modifica_regia", cur_page)

    #     if not isinstance(cur_page, ModificaRegiaView):
    #         raise TypeError(
    #             f"cur_page deve essere ModificaRegiaView. Type trovato: {type(cur_page)}"
    #         )

    #     # ID utilizato quando si Conferma la modifica
    #     cur_page.cur_id_regia = id_

    #     # Setup values
    #     cur_page.regista.setText(cur_regia.get_regista())
    #     cur_page.anno.setValue(cur_regia.get_anno_produzione())

    #     # Apri la pagina ModificaGenereView
    #     self.goToPageRequest.emit("modifica_regia", True)

    # def cancella_regia(self):
    #     """
    #     Chiama il metodo `go_back()` del `NavigationController`. Non ha bisogno di riscrivere
    #     i campi di input perché le funzioni `crea_regia()` e `modifica_regia()` si caricano di
    #     farlo.
    #     """
    #     self.goBackRequest.emit()
