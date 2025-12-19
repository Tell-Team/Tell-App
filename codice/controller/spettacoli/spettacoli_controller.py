# from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal

# from typing import Optional

from controller.context import AppContext, NavigationController

from model.pianificazione.spettacolo import Spettacolo


class SpettacoliController:
    goBackRequest = pyqtSignal()
    goToPageRequest = pyqtSignal(str, bool)
    getNavPageRequest = pyqtSignal(str, dict)

    def __init__(self, app_context: AppContext):
        self.__model = app_context.model
        self.__nav = app_context.nav

    def get_nav(self) -> NavigationController:
        return self.__nav

    def get_spettacoli(self) -> list[Spettacolo]:
        return self.__model.get_spettacoli()

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
