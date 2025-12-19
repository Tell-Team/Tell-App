from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox
from PyQt6.QtCore import Qt, QDate, pyqtSignal, QObject
from typing import Optional
from functools import partial

from model.model import Model
from model.pianificazione.opera import Opera
from model.pianificazione.genere import Genere
from model.pianificazione.regia import Regia  # Necessario per VisualizzaOpera.
from model.exceptions import OggettoInUsoException

from view.info.info_section import InfoSectionView
from view.info.visualizza_opera import VisualizzaOperaView

from view.info.display_opera import OperaDisplay
from view.info.display_genere import GenereDisplay


class InfoController(QObject):
    """
    Gestice la sezione Info (`InfoSectionView`) dell'app e la pagina per visualizzare un'opera
    (`VisualizzaOperaView`).

    Segnali:
    - goBackRequest(): emesso per tornare all'ultima pagina salvata nell'hitory del
    `NavigationController`;
    - goToPageRequest(str, bool): emesso per visualizzare un'altra pagina;
    - goToSectionRequest(str): emesso per visualizzare un'altra pagina, senza salvarla
    nell'history del `NavigationController`;
    - getNavPageRequest(str, dict): emesso per ottenere la pagina che vendrà visualizzata.
    """

    goBackRequest = pyqtSignal()
    goToPageRequest = pyqtSignal(str, bool)
    goToSectionRequest = pyqtSignal(str)
    getNavPageRequest = pyqtSignal(str, dict)

    def __init__(
        self,
        model: Model,
        info_s: InfoSectionView,
        opera_v: VisualizzaOperaView,
    ) -> None:
        super().__init__()
        self.__model = model
        self.__info_section = info_s
        self.__visualizza_opera_view = opera_v

        self._connect_signals()

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    def _connect_signals(self) -> None:
        # Logout
        self.__info_section.logoutRequest.connect(  # type:ignore
            self.goBackRequest.emit  # - Account ancora non implemetati
        )
        # Visualizza Sezione Spettacoli
        self.__info_section.goToSpettacoli.connect(  # type:ignore
            partial(self.goToSectionRequest.emit, "spettacoli_section")
        )

        # Visualizza Sezione Account
        self.__info_section.goToAccount.connect(  # type:ignore
            partial(self.goToSectionRequest.emit, "account_section")
            # - Account ancora non implemetati
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

        # Setup della pagina di creazione di generi
        self.__info_section.nuovoGenereRequest.connect(  # type:ignore
            self.nuovo_genere
        )

    # ------------------------- METODI PUBBLICI -------------------------

    def get_opera(self, id_: int) -> Optional[Opera]:
        return self.__model.get_opera(id_)

    def get_opere(self) -> list[Opera]:
        return self.__model.get_opere()

    def elimina_opera(self, id_: int) -> None:
        return self.__model.elimina_opera(id_)

    def get_genere(self, id_: int) -> Optional[Genere]:
        return self.__model.get_genere(id_)

    def get_generi(self) -> list[Genere]:
        return self.__model.get_generi()

    def elimina_genere(self, id_: int) -> None:
        return self.__model.elimina_genere(id_)

    def get_regie_by_opera(self, id_: int) -> list[Regia]:
        return self.__model.get_regie_by_opera(id_)

    def display_opere(self, layout: QVBoxLayout) -> None:
        """
        Visualizza a schermo alcune informazioni delle opere salvate ed assegna a
        ciascuna pulsanti per visualizzarle in dettaglio, modificarle o eliminarle.

        :param layout: layout dove saranno caricate tutte le opere
        """
        # Si spera che il layout contenga un label con un messaggio di errore.
        lista_vuota_error = layout.itemAt(0).widget()  # type: QLabel #type:ignore

        if not self.get_opere():
            lista_vuota_error.show()
            return

        for opera in self.get_opere():
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
            self.__info_section.aggiungi_widget_al_layout(cur_opera, layout)

            # Funzione di elimina per l'opera
            def on_si(id_: int) -> None:
                """Prova di eliminare l'istanza d'opera

                :param id_: id dell'opera da elimina
                """
                try:
                    self.elimina_opera(id_)
                except OggettoInUsoException as exc:
                    cur_opera.annulla_elimina()
                    self.__mostra_errore(
                        self.__info_section,
                        "Opera in uso",
                        f"Si è verificato un errore: {exc}",
                    )
                else:
                    self.__info_section.refresh_page()

            cur_opera.eliminaConfermata.connect(  # type:ignore
                on_si
            )

    def display_generi(self, layout: QVBoxLayout) -> None:
        """
        Visualizza a schermo le informazioni dei generi salvati ed assegna a ciascuno
        pulsanti per modificarli o eliminarli.

        :param layout: layout dove saranno caricate tutti i generi
        """
        # Si spera che il layout contenga un label con un messaggio di errore.
        lista_vuota_error = layout.itemAt(0).widget()  # type:QLabel # type:ignore

        if not self.get_generi():
            lista_vuota_error.show()
            return

        for genere in self.get_generi():
            cur_genere = GenereDisplay(genere)

            # Setup della pagina di modifica dei generi
            cur_genere.modificaRequest.connect(  # type:ignore
                self.modifica_genere
            )

            # Aggiungi cur_genere al layout di ListaOpere
            self.__info_section.aggiungi_widget_al_layout(cur_genere, layout)

            # Funzione di elimina per il genere
            def on_si(id_: int) -> None:
                """Prova di eliminare l'istanza d'opera

                :param id_: id dell'opera da elimina
                """
                try:
                    self.elimina_genere(id_)
                except OggettoInUsoException as exc:
                    cur_genere.annulla_elimina()
                    self.__mostra_errore(
                        self.__info_section,
                        "Genere in uso",
                        f"Si è verificato un errore: {exc}",
                    )
                else:
                    self.__info_section.refresh_page()

            cur_genere.eliminaConfermata.connect(  # type:ignore
                on_si
            )

    def visualizza_opera(self, id_: int) -> None:
        """
        Carica la pagina `VisualizzaOperaView` con i dati relativi all'opera indicata.

        :param id_: id dell'opera da visualizzare
        """
        LISTA_REGIE_VUOTA = "Al momento, non vi sono regie per questa opera."

        # Copia dell'opera da visualizzare
        cur_opera = self.get_opera(id_)
        if not cur_opera:
            self.__mostra_errore(
                self.__info_section,
                "Opera inesistente",
                f"Non è presente nessun'opera con id {id_}.",
            )
            return

        # Ottieni la pagina VisualizzaOperaView
        cur_page = self.__visualizza_opera_view

        # Setup pagina
        self.clear_layout_regie(cur_page.layout_regie)
        cur_page.layout_regie.addWidget(cur_page.label_lista_regie)
        cur_page.lista_vuota_error.setText("")

        cur_page.label_nome.setText(f"{cur_opera.get_nome()}")
        cur_page.label_librettista.setText(f"Libretto di {cur_opera.get_librettista()}")
        cur_page.label_compositore.setText(
            f"Musica composta da {cur_opera.get_compositore()}"
        )

        cur_genere = self.get_genere(cur_opera.get_id_genere())
        if not cur_genere:
            self.__mostra_errore(
                self.__info_section,
                "Genere inesistente",
                f"Non è presente nessun genere con id {cur_opera.get_id_genere()}.",
            )
            return

        cur_page.label_genere.setText(f"Genere: {cur_genere.get_nome()}")

        cur_page.label_atti.setText(f"Numero di atti: {cur_opera.get_numero_atti()}")
        cur_page.label_prima_rappresentazione.setText(
            "È stata rappresentata per prima volta il "
            + f"{cur_opera.get_data_prima_rappresentazione().strftime("%d/%m/%y")} "
            + f"nel teatro {cur_opera.get_teatro_prima_rappresentazione()}"
        )
        cur_page.label_trama.setText(f"{cur_opera.get_trama()}")

        lista_regie = self.get_regie_by_opera(cur_opera.get_id())
        if not lista_regie:
            cur_page.lista_vuota_error.setText(LISTA_REGIE_VUOTA)

        for r in lista_regie:
            self.display_regia(r, cur_page.layout_regie)

        # Apri la pagina
        self.goToPageRequest.emit("visualizza_opera", True)

    def display_regia(self, r: Regia, layout: QVBoxLayout) -> None:
        """Visualizza a schermo alcune informazioni della regia.

        :param r: regia da mostrare
        :param layout: layout in cui sarà mostrata la regia"""
        widget_regia = QWidget()
        widget_regia.setObjectName("Container")
        layout_regia = QVBoxLayout(widget_regia)

        titolo = QLabel(f"{r.get_titolo()}")
        titolo.setObjectName("Header2")
        titolo.setAlignment(Qt.AlignmentFlag.AlignLeft)

        regista = QLabel(f"Regista: {r.get_regista()}")
        regista.setObjectName("Paragraph")

        anno = QLabel(f"Anno di produzione: {r.get_anno_produzione()}")
        anno.setObjectName("Paragraph")

        layout_regia.addWidget(titolo)
        layout_regia.addWidget(regista)
        layout_regia.addWidget(anno)
        layout_regia.addStretch()

        layout.addWidget(widget_regia)

    def clear_layout_regie(self, layout: QVBoxLayout) -> None:
        """Pulisce il layout delle regie.

        :param layout: layout in cui sono state caricate le regie"""
        # Siccome il layout solo contiene dei widget, non è necessario rimuovere dei layout.
        if layout:
            while layout.count():
                item = layout.takeAt(0)
                assert item is not None
                widget = item.widget()

                if widget:
                    widget.setParent(None)
                #     continue

                # child_layout = item.layout()
                # if child_layout:
                #     self.clear_layout_regie(child_layout)

    def nuova_opera(self) -> None:
        """
        Carica la pagina `NuovaOperaView`, dove l'utente può inserire i dati necessari per
        creare un'opera.
        """
        # Ottieni la pagina NuovaOperaView
        from view.info.nuova_opera import NuovaOperaView

        cur_page_dict: dict[str, Optional[QWidget]] = {"value": None}
        self.getNavPageRequest.emit("nuova_opera", cur_page_dict)
        cur_page: Optional[QWidget] = cur_page_dict.get("value")

        if not isinstance(cur_page, NuovaOperaView):
            self.__mostra_errore(
                self.__info_section,
                "Pagina non trovata",
                "Si è verificato un errore: Non è stato trovata la pagina 'nuova_opera'. "
                + f"Type trovato: {type(cur_page)}",
            )
            return

        # Setup pagina
        cur_page.nome.setText("")
        cur_page.trama.setText("")

        cur_page.setup_genere_combobox(self.get_generi())
        cur_page.genere.setCurrentIndex(0)

        cur_page.compositore.setText("")
        cur_page.librettista.setText("")
        cur_page.atti.setValue(0)
        cur_page.data.setDate(QDate.currentDate())
        cur_page.teatro.setText("")
        cur_page.input_error.setText("")

        # Apri la pagina
        self.goToPageRequest.emit("nuova_opera", True)

    def modifica_opera(self, id_: int) -> None:
        """
        Carica la pagina `ModificaOperaView`, con i dati dell'opera indicata inseriti nei
        campo di input.

        :param id_: id dell'opera da modificare
        """
        # Copia dell'opera da modificare
        cur_opera = self.get_opera(id_)
        if not cur_opera:
            self.__mostra_errore(
                self.__info_section,
                "Opera inesistente",
                f"Non è presente nessun'opera con id {id_}.",
            )
            return

        # Ottieni la pagina ModificaOperaView
        from view.info.modifica_opera import ModificaOperaView

        cur_page_dict: dict[str, Optional[QWidget]] = {"value": None}
        self.getNavPageRequest.emit("modifica_opera", cur_page_dict)
        cur_page: Optional[QWidget] = cur_page_dict.get("value")

        if not isinstance(cur_page, ModificaOperaView):
            self.__mostra_errore(
                self.__info_section,
                "Pagina non trovata",
                "Si è verificato un errore: Non è stato trovata la pagina 'modifica_opera'. "
                + f"Type trovato: {type(cur_page)}",
            )
            return

        # Salva l'id dell'opera da modificare nella pagina
        cur_page.cur_id_opera = id_

        # Setup pagina
        cur_page.nome.setText(cur_opera.get_nome())
        cur_page.trama.setText(cur_opera.get_trama())

        cur_page.setup_genere_combobox(self.get_generi())
        cur_id_genere = cur_opera.get_id_genere()
        index = cur_page.genere.findData(cur_id_genere)
        if index >= 0:
            cur_page.genere.setCurrentIndex(index)

        cur_page.compositore.setText(cur_opera.get_compositore())
        cur_page.librettista.setText(cur_opera.get_librettista())
        cur_page.atti.setValue(cur_opera.get_numero_atti())
        cur_page.data.setDate(cur_opera.get_data_prima_rappresentazione())
        cur_page.teatro.setText(cur_opera.get_teatro_prima_rappresentazione())

        # Apri la pagina
        self.goToPageRequest.emit("modifica_opera", True)

    def nuovo_genere(self) -> None:
        """
        Carica la pagina `NuovoGenereView`, dove l'utente può inserire i dati necessari per
        creare un genere.
        """
        # Ottieni la pagina NuovoGenereView
        from view.info.nuovo_genere import NuovoGenereView

        cur_page_dict: dict[str, Optional[QWidget]] = {"value": None}
        self.getNavPageRequest.emit("nuovo_genere", cur_page_dict)
        cur_page: Optional[QWidget] = cur_page_dict.get("value")

        if not isinstance(cur_page, NuovoGenereView):
            self.__mostra_errore(
                self.__info_section,
                "Pagina non trovata",
                "Si è verificato un errore: Non è stato trovata la pagina 'nuovo_genere'. "
                + f"Type trovato: {type(cur_page)}",
            )
            return

        # Setup pagina
        cur_page.nome.setText("")
        cur_page.descrizione.setText("")
        cur_page.input_error.setText("")

        # Apri la pagina
        self.goToPageRequest.emit("nuovo_genere", True)

    def modifica_genere(self, id_: int) -> None:
        """
        Carica la pagina `ModificaGenereView`, con i dati del genere indicato inseriti nei
        campo di input.

        :param id_: id del genere da modificare
        """
        # Copia del genere da modificare
        cur_genere = self.get_genere(id_)
        if not cur_genere:
            self.__mostra_errore(
                self.__info_section,
                "Genere inesistente",
                f"Non è presente nessun genere con id {id_}.",
            )
            return

        # Ottieni la pagina ModificaGenereView
        from view.info.modifica_genere import ModificaGenereView

        cur_page_dict: dict[str, Optional[QWidget]] = {"value": None}
        self.getNavPageRequest.emit("modifica_genere", cur_page_dict)
        cur_page: Optional[QWidget] = cur_page_dict.get("value")

        if not isinstance(cur_page, ModificaGenereView):
            self.__mostra_errore(
                self.__info_section,
                "Pagina non trovata",
                "Si è verificato un errore: Non è stato trovata la pagina 'modifica_genere'. "
                + f"Type trovato: {type(cur_page)}",
            )
            return

        # Salva l'id del genere da modificare nella pagina
        cur_page.cur_id_genere = cur_genere.get_id()

        # Setup pagina
        cur_page.nome.setText(cur_genere.get_nome())
        cur_page.descrizione.setText(cur_genere.get_descrizione())

        # Apri la pagina
        self.goToPageRequest.emit("modifica_genere", True)

    # ------------------------- METODI PRIVATI -------------------------

    def __mostra_errore(self, widget: QWidget, titolo: str, testo: str) -> None:
        """Mostra un messaggio di errore all'utente.

        :param widget: parent widget delle finestra di errore
        :param titolo: titolo della finestra di errore
        :param testo: testo descrittivo
        """
        QMessageBox.critical(widget, titolo, testo)
