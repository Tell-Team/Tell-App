from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtCore import pyqtSignal, QObject
from typing import Optional
from functools import partial

from model.model import Model
from model.pianificazione.opera import Opera
from model.exceptions import (
    DatoIncongruenteException,
    IdInesistenteException,
    IdOccupatoException,
)

from view.info.modifica_opera import ModificaOperaView, NuovaOperaView


class CUOperaController(QObject):
    """Gestisce il salvataggio delle opere create e modificate.

    Segnali:
    - navigation_go_back(): emesso per tornare all'ultima pagina visualizzata;
    - naviagation_get_page(str, dict): emesso per ottenere la pagina da cui si prenderà l'input.
    """

    navigation_go_back = pyqtSignal()
    navigation_get_page = pyqtSignal(str, dict)

    def __init__(
        self,
        model: Model,
        n_opera_v: NuovaOperaView,
        m_opera_v: ModificaOperaView,
    ) -> None:
        super().__init__()
        self.__model = model
        self.__nuova_opera_view = n_opera_v
        self.__modifica_opera_view = m_opera_v

        self._connect_signals()

    def _connect_signals(self) -> None:
        # Cancella creazione Opera
        self.__nuova_opera_view.btn_cancella.clicked.connect(  # type:ignore
            self.navigation_go_back.emit
        )
        # Conferma creazione Opera
        self.__nuova_opera_view.btn_conferma.clicked.connect(  # type:ignore
            partial(self.salva_opera, is_new=True)
        )

        # Cancella modifica Opera
        self.__modifica_opera_view.btn_cancella.clicked.connect(  # type:ignore
            self.navigation_go_back.emit
        )
        # Conferma modifica Opera
        self.__modifica_opera_view.btn_conferma.clicked.connect(  # type:ignore
            partial(self.salva_opera, is_new=False)
        )

    # ------------------------- METODI PUBBLICI -------------------------

    def get_opera(self, id_: int) -> Optional[Opera]:
        return self.__model.get_opera(id_)

    def aggiungi_opera(self, opera: Opera) -> None:
        self.__model.aggiungi_opera(opera)

    def modifica_opera(self, opera_modificata: Opera) -> None:
        self.__model.modifica_opera(opera_modificata)

    def get_generi(self):
        # - Il controller dovrebbe accedere alla lista originale?
        return self.__model.get_generi()

    def salva_opera(self, is_new: bool = True) -> None:
        """Salva l'opera creata o modificata nel `GestoreOpere`.

        :param is_new: verifica se si deve creare un'opera o modificare una esistente"""
        CAMPI_NECESSARI = (
            "<b>ATTENZIONE</b>: E' necessario compilare tutti i campi d'input."
        )

        if is_new:
            # Ottieni la pagina NuovaOperaView
            from view.info.nuova_opera import NuovaOperaView

            cur_page_dict: dict[str, Optional[QWidget]] = {"value": None}
            self.navigation_get_page.emit("nuova_opera", cur_page_dict)
            cur_page = cur_page_dict.get("value")

            if not isinstance(cur_page, NuovaOperaView):
                raise TypeError(
                    f"cur_page deve essere NuovaOperaView. Type trovato: {type(cur_page)}"
                )

            # Ottieni l'input inserito
            nome = cur_page.nome.text()
            trama = cur_page.trama.toPlainText()
            id_genere: int = cur_page.genere.currentData()
            compositore = cur_page.compositore.text()
            librettista = cur_page.librettista.text()
            atti = cur_page.atti.value()
            data = cur_page.data.date().toPyDate()
            teatro = cur_page.teatro.text()

            # Tenta di creare la nuova opera
            try:
                # - Sarebbe buono corriggere l'ordine dei parametri del costruttore di Opera
                nuova_opera = Opera(
                    nome, compositore, librettista, atti, data, teatro, trama, id_genere
                )
            except DatoIncongruenteException as exc:
                # E' stato trovato un campo con input non valido
                cur_page.input_error.setText(CAMPI_NECESSARI)
                self.__set_pagina_focus(cur_page)
                self.__mostra_errore(
                    cur_page, "Input non valido", f"Si è verificato un errore: {exc}"
                )
            else:
                cur_page.input_error.setText("")

                try:
                    # - È necessario corriggere l'ordine dei setter del costruttore di Opera
                    self.aggiungi_opera(nuova_opera)
                except IdInesistenteException as exc:
                    # L'opera è collegata ad un genere che non esiste
                    self.__mostra_errore(
                        cur_page,
                        "Genere inesistente",
                        f"Si è verificato un errore: {exc}",
                    )
                except IdOccupatoException as exc:
                    # Esiste già un'opera con quell'id
                    self.__mostra_errore(
                        cur_page,
                        "ID Opera occupato",
                        f"Si è verificato un errore: {exc}",
                    )
                else:
                    self.navigation_go_back.emit()
        elif not is_new:
            # Ottieni la pagina ModificaOperaView
            from view.info.modifica_opera import ModificaOperaView

            cur_page_dict: dict[str, Optional[QWidget]] = {"value": None}
            self.navigation_get_page.emit("modifica_opera", cur_page_dict)
            cur_page = cur_page_dict.get("value")

            if not isinstance(cur_page, ModificaOperaView):
                raise TypeError(
                    f"cur_page deve essere ModificaOperaView. Type trovato: {type(cur_page)}"
                )

            # Crea una copia dell'opera originale
            copia_opera = self.get_opera(cur_page.cur_id_opera)
            if not isinstance(copia_opera, Opera):
                raise IdInesistenteException(
                    f"Non e' presente nessun opera con id {cur_page.cur_id_opera}."
                )

            # Ottieni l'input inserito
            nome = cur_page.nome.text()
            trama = cur_page.trama.toPlainText()
            id_genere: int = cur_page.genere.currentData()
            compositore = cur_page.compositore.text()
            librettista = cur_page.librettista.text()
            atti = cur_page.atti.value()
            data = cur_page.data.date().toPyDate()
            teatro = cur_page.teatro.text()

            # Tenta di modificare l'opera
            try:
                copia_opera.set_nome(nome)
                copia_opera.set_trama(trama)
                copia_opera.set_id_genere(id_genere)
                copia_opera.set_compositore(compositore)
                copia_opera.set_librettista(librettista)
                copia_opera.set_numero_atti(atti)
                copia_opera.set_data_prima_rappresentazione(data)
                copia_opera.set_teatro_prima_rappresentazione(teatro)
            except DatoIncongruenteException as exc:
                # E' stato trovato un campo con input non valido
                cur_page.input_error.setText(CAMPI_NECESSARI)
                self.__set_pagina_focus(cur_page)
                self.__mostra_errore(
                    cur_page, "Input non valido", f"Si è verificato un errore: {exc}"
                )
            else:
                cur_page.input_error.setText("")

                try:
                    self.modifica_opera(copia_opera)
                except IdInesistenteException as exc:
                    # Non esiste un'opera con quell'id
                    self.__mostra_errore(
                        cur_page,
                        "ID Opera inesistente",
                        f"Si è verificato un errore: {exc}",
                    )
                else:
                    self.navigation_go_back.emit()

    # ------------------------- CALLBACKS -------------------------

    def __mostra_errore(self, widget: QWidget, titolo: str, testo: str) -> None:
        """Mostra un messaggio di errore all'utente.

        :param widget: parent widget delle finestra di errore
        :param titolo: titolo della finestra di errore
        :param testo: testo descrittivo
        """
        QMessageBox.critical(widget, titolo, testo)

    # - Potrei migliorare questo metodo
    def __set_pagina_focus(self, pagina: NuovaOperaView) -> None:
        """Evidenzia il campo con input non valido.

        :param pagina: widget dove si è verificato l'errore d'input"""
        pagina.focusNextChild()
        if not pagina.nome.text().strip():
            return
        pagina.focusNextChild()
        if not pagina.trama.toPlainText().strip():
            return
        pagina.focusNextChild()
        if pagina.genere.currentIndex() == 0:
            return
        pagina.focusNextChild()
        if not pagina.compositore.text().strip():
            return
        pagina.focusNextChild()
        if not pagina.librettista.text().strip():
            return
        pagina.focusNextChild()
        if not pagina.atti.value():
            return
        pagina.focusNextChild()
        if not pagina.data:
            return
        pagina.focusNextChild()
