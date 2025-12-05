from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QDate, pyqtSignal, QObject
from typing import Optional
from functools import partial

from model.model import Model
from model.pianificazione.opera import Opera
from model.pianificazione.genere import Genere
from model.pianificazione.regia import Regia  # Necessario per VisualizzaOpera.
from model.exceptions import (
    IdInesistenteException,
    OggettoInUsoException,
)

from view.info.info_section import InfoSectionView
from view.info.visualizza_opera import OperaView


class InfoController(QObject):
    navigation_go_back = pyqtSignal()
    navigation_go_to = pyqtSignal(str, bool)
    navigation_section_go_to = pyqtSignal(str)
    navigation_get_page = pyqtSignal(str, dict)

    def __init__(
        self,
        model: Model,
        info_s: InfoSectionView,
        opera_v: OperaView,
    ):
        super().__init__()
        self.__model = model
        self.__info_section = info_s
        self.__visualizza_opera_view = opera_v
        self._connect_signals()

    def _connect_signals(self):
        # INFO SECTION
        self.__info_section.btn_logout.clicked.connect(  # type:ignore
            lambda: self.navigation_go_back.emit()  # - Account ancora non implemetati
        )

        self.__info_section.btn_sezione_spettacoli.clicked.connect(  # type:ignore
            lambda: self.navigation_section_go_to.emit("spettacoli_section")
        )

        self.__info_section.btn_sezione_info.setEnabled(False)

        self.__info_section.btn_sezione_account.clicked.connect(  # type:ignore
            lambda: self.navigation_section_go_to.emit("account_section")
            # - Account ancora non implemetati
        )

        self.__info_section.request_display_opere.connect(  # type:ignore
            self.display_opere
        )

        self.__info_section.request_display_generi.connect(  # type:ignore
            self.display_generi
        )

        # OPERA
        # Crea una Opera
        self.__info_section.btn_nuova_opera.clicked.connect(  # type:ignore
            self.nuova_opera
        )

        # Visualizza Opera
        self.__visualizza_opera_view.btn_torna_dietro.clicked.connect(  # type:ignore
            lambda: self.navigation_go_back.emit()
        )

        # GENERI
        # Crea un Genere
        self.__info_section.btn_nuovo_genere.clicked.connect(  # type:ignore
            self.nuovo_genere
        )

    def get_opera(self, id_: int) -> Optional[Opera]:
        return self.__model.get_opera(id_)

    def get_opere(self) -> list[Opera]:
        return self.__model.get_opere()

    def get_genere(self, id_: int) -> Optional[Genere]:
        return self.__model.get_genere(id_)

    def get_generi(self) -> list[Genere]:
        return self.__model.get_generi()

    def get_regie_by_opera(self, id_: int) -> list[Regia]:
        return self.__model.get_regie_by_opera(id_)

    #
    #
    #

    def display_opere(self, layout: QVBoxLayout):
        lista_vuota_error = layout.itemAt(0).widget()  # type:QLabel # type:ignore

        if not self.get_opere():
            lista_vuota_error.show()
            return

        for opera in self.get_opere():
            # Labels
            nome = QLabel(f"{opera.get_nome()}")
            nome.setObjectName("Header2")

            librettista = QLabel(f"Libretto di {opera.get_librettista()}")
            librettista.setObjectName("Paragraph")

            compositore = QLabel(f"Musica di {opera.get_compositore()}")
            compositore.setObjectName("Paragraph")

            # Pulsanti
            btn_visualizza = QPushButton("Maggior info")
            btn_visualizza.setObjectName("SmallButton")
            btn_visualizza.clicked.connect(  # type:ignore
                partial(self.visualizza_opera, opera.get_id())
            )

            btn_modifica = QPushButton("Modifica")
            btn_modifica.setObjectName("SmallButton")
            btn_modifica.clicked.connect(  # type:ignore
                partial(self.modifica_opera, opera.get_id())
            )

            pulsanti = QWidget()
            layout_btn = QHBoxLayout(pulsanti)
            layout_btn.addWidget(btn_visualizza)
            layout_btn.addWidget(btn_modifica)
            layout_btn.addStretch()

            # Layout
            cur_opera = QWidget()
            cur_opera.setObjectName("Container")
            layout_cur_opera = QVBoxLayout(cur_opera)

            layout_cur_opera.addWidget(nome)
            layout_cur_opera.addWidget(librettista)
            layout_cur_opera.addWidget(compositore)
            layout_cur_opera.addWidget(pulsanti)

            layout.addWidget(cur_opera)

    def display_generi(self, layout: QVBoxLayout):
        lista_vuota_error = layout.itemAt(0).widget()  # type:QLabel # type:ignore

        if not self.get_generi():
            lista_vuota_error.show()
            return

        for genere in self.get_generi():
            id_ = genere.get_id()

            # Labels
            nome = QLabel(f"{genere.get_nome()}")
            nome.setObjectName("Header2")

            descrizione = QLabel(f"{genere.get_descrizione()}")
            descrizione.setObjectName("Paragraph")
            descrizione.setWordWrap(True)

            # Pulsanti Modifica-Elimina
            btn_modifica = QPushButton("Modifica")
            btn_modifica.setObjectName("SmallButton")
            btn_modifica.clicked.connect(  # type:ignore
                partial(self.modifica_genere, genere.get_id())
            )

            btn_elimina = QPushButton("Elimina")
            btn_elimina.setObjectName("SmallButton")

            pulsanti = QWidget()
            temp_layout_btn = QHBoxLayout(pulsanti)
            temp_layout_btn.addWidget(btn_modifica)
            temp_layout_btn.addWidget(btn_elimina)
            temp_layout_btn.addStretch()

            # Errore: Genere in uso
            label_error = QLabel("Errore: Questo genere è in uso.")
            label_error.setObjectName("SubHeader")
            label_error.setStyleSheet(
                label_error.styleSheet() + "#SubHeader { color:red; }"
            )
            label_error.hide()
            temp_layout_btn.addWidget(label_error)

            # Pannello di eliminazione
            domanda = QLabel("Sicuro di eliminare?")

            btn_si = QPushButton("Sì")
            btn_si.setObjectName("SmallButton")

            btn_no = QPushButton("No")
            btn_no.setObjectName("SmallButton")

            conferma_elimina = QWidget()
            layout_conferma = QHBoxLayout(conferma_elimina)
            layout_conferma.addWidget(domanda)
            layout_conferma.addWidget(btn_si)
            layout_conferma.addWidget(btn_no)
            conferma_elimina.hide()

            # Layout
            current_genere = QWidget()
            current_genere.setObjectName("Container")
            layout_cur_genere = QVBoxLayout(current_genere)

            layout_cur_genere.addWidget(nome)
            layout_cur_genere.addWidget(descrizione)
            layout_cur_genere.addWidget(pulsanti)
            layout_cur_genere.addWidget(conferma_elimina)

            layout.addWidget(current_genere)

            def on_elimina(
                pulsanti_widget: QWidget = pulsanti,
                conferma_elimina_widget: QWidget = conferma_elimina,
            ):
                pulsanti_widget.hide()
                conferma_elimina_widget.show()

            def on_no(
                pulsanti_widget: QWidget = pulsanti,
                conferma_elimina_widget: QWidget = conferma_elimina,
                label_error_widget: QLabel = label_error,
            ):
                conferma_elimina_widget.hide()
                pulsanti_widget.show()
                label_error_widget.hide()

            def on_si(
                id_genere: int = id_,
                pulsanti_widget: QWidget = pulsanti,
                conferma_elimina_widget: QWidget = conferma_elimina,
                label_error_widget: QLabel = label_error,
            ):
                if not self.elimina_genere(id_genere):
                    # Se non si può eliminare, mostra un messaggio d'errore che viene nascosto
                    #   dopo qualunque chiamata di refresh_page() oppure se si tenta di eliminare
                    #   una seconda volta ma cancellando col pulsante No.
                    conferma_elimina_widget.hide()
                    pulsanti_widget.show()
                    label_error_widget.show()
                else:
                    self.__info_section.refresh_page()

            btn_elimina.clicked.connect(  # type:ignore
                partial(on_elimina, pulsanti, conferma_elimina)
            )
            btn_no.clicked.connect(  # type:ignore
                partial(on_no, pulsanti, conferma_elimina, label_error)
            )
            btn_si.clicked.connect(  # type:ignore
                partial(on_si, id_, pulsanti, conferma_elimina, label_error)
            )

    def visualizza_opera(self, id_: int):
        """
        Assegna i dati necessari dell'opera, relativa all'`id_`, nella pagina `OperaView`.
        """

        LISTA_VUOTA = "Al momento, non vi sono regie per questa opera."

        # Get opera da visualizzare
        cur_opera = self.get_opera(id_)
        if not cur_opera:
            raise IdInesistenteException(f"Non e' presente nessun'opera con id {id_}.")

        # Get pagina salvata nel NavigationController
        from view.info.visualizza_opera import OperaView

        cur_page_dict: dict[str, QWidget | None] = {"value": None}
        self.navigation_get_page.emit("visualizza_opera", cur_page_dict)
        cur_page = cur_page_dict.get("value")

        if not isinstance(cur_page, OperaView):
            raise TypeError(f"cur_page deve essere OperaView, trovata {type(cur_page)}")

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
            raise IdInesistenteException(
                f"Non e' presente nessun genere con id {cur_opera.get_id_genere()}."
            )

        cur_page.label_genere.setText(f"Genere: {cur_genere.get_nome()}")

        cur_page.label_atti.setText(f"Numero di atti: {cur_opera.get_numero_atti()}")
        cur_page.label_prima_rappresentazione.setText(
            f"È stata rappresentata per prima volta il {cur_opera.get_data_prima_rappresentazione().strftime("%d/%m/%y")} nel teatro {cur_opera.get_teatro_prima_rappresentazione()}"
        )
        cur_page.label_trama.setText(f"{cur_opera.get_trama()}")

        lista_regie = self.get_regie_by_opera(cur_opera.get_id())
        if not lista_regie:
            cur_page.lista_vuota_error.setText(LISTA_VUOTA)

        for r in lista_regie:
            self.display_regia(r, cur_page.layout_regie)

        # Apri la pagina OperaView
        self.navigation_go_to.emit("visualizza_opera", True)

    def display_regia(self, r: Regia, layout: QVBoxLayout):
        temp_regia = QWidget()
        temp_regia.setObjectName("Container")
        temp_layout = QVBoxLayout(temp_regia)

        titolo = QLabel(f"{r.get_titolo()}")
        titolo.setObjectName("Header2")
        titolo.setAlignment(Qt.AlignmentFlag.AlignLeft)

        regista = QLabel(f"Regista: {r.get_regista()}")
        regista.setObjectName("Paragraph")

        anno = QLabel(f"Anno di produzione: {r.get_anno_produzione()}")
        anno.setObjectName("Paragraph")

        temp_layout.addWidget(titolo)
        temp_layout.addWidget(regista)
        temp_layout.addWidget(anno)
        temp_layout.addStretch()

        layout.addWidget(temp_regia)

    def clear_layout_regie(self, layout: QVBoxLayout):
        if layout:
            while layout.count():
                item = layout.takeAt(0)
                assert item is not None
                widget = item.widget()

                if widget:
                    widget.setParent(None)
                # Non c'è un else per eliminare sottolayouts perché non è necessario.
                # - Se quella lista regie permette di modificare o eliminare le regie, allora
                #   sì dovrei aggiungere un modo di eliminare layouts

    def nuova_opera(self):
        """
        Carica la pagina `NuovaOperaView`, dove l'utente può cancellare l'operazione tornando dietro
        utilizzando il pulsante Cancella, chiamando `cancella_opera()` o confermare la creazione
        pulsando Conferma, chiamando altro metodo `salva_opera()`, che verifica la correttezza dei
        dati, crea l'istanza di `Opera` e la salva nella lista di opere. I campi di input vengono
        riscritti prima di visualizzare la pagina.
        """
        # Get pagina salvata nel NavigationController
        from view.info.nuova_opera import NuovaOperaView

        cur_page_dict: dict[str, QWidget | None] = {"value": None}
        self.navigation_get_page.emit("nuova_opera", cur_page_dict)
        cur_page = cur_page_dict.get("value")

        if not isinstance(cur_page, NuovaOperaView):
            raise TypeError(
                f"cur_page deve essere NuovaOperaView, trovata {type(cur_page)}"
            )

        # Setup default values
        cur_page.nome.setText("")
        cur_page.trama.setText("")

        lista_nomi: list[str] = []
        for g in self.get_generi():
            lista_nomi.append(g.get_nome())
        cur_page.set_genere_combobox(lista_nomi)
        cur_page.genere.setCurrentIndex(0)

        cur_page.compositore.setText("")
        cur_page.librettista.setText("")
        cur_page.atti.setValue(0)
        cur_page.data.setDate(QDate(1999, 1, 1))
        cur_page.teatro.setText("")
        cur_page.input_error.setText("")

        # Apri pagina NuovaOperaView
        self.navigation_go_to.emit("nuova_opera", True)

    def modifica_opera(self, id_: int):
        """
        Carica la pagina `ModificaOperaView`, con i dati dell'opera relativa all'`id_` inseriti
        nei campo di input. Il pulsante Conferma chiama la stessa funzione `salva_opera(is_new=False)`,
        ma usando altra opzione che permette di modificare i dati dell'opera esistente grazie ad
        un'attributo `cur_id_opera` della classe, mentre che il pulsante Cancella
        chiama `cancella_opera()`, tornando dietro senza far nessun cambio nell'istanza.
        """
        # Get opera da modificare
        cur_opera = self.get_opera(id_)
        if not cur_opera:
            raise IdInesistenteException(f"Non e' presente nessun'opera con id {id_}.")

        # Get pagina salvata nel NavigationController
        from view.info.modifica_opera import ModificaOperaView

        cur_page_dict: dict[str, QWidget | None] = {"value": None}
        self.navigation_get_page.emit("modifica_opera", cur_page_dict)
        cur_page = cur_page_dict.get("value")

        if not isinstance(cur_page, ModificaOperaView):
            raise TypeError(
                f"cur_page deve essere ModificaOperaView, trovata {type(cur_page)}"
            )

        # ID utilizzato quando si Conferma la modifica
        cur_page.cur_id_opera = id_

        # Setup values
        cur_page.nome.setText(cur_opera.get_nome())
        cur_page.trama.setText(cur_opera.get_trama())

        lista_nomi: list[str] = []
        for g in self.get_generi():
            lista_nomi.append(g.get_nome())
        cur_page.set_genere_combobox(lista_nomi)

        cur_genere = self.get_genere(cur_opera.get_id_genere())
        if not cur_genere:
            raise IdInesistenteException(
                f"Non e' presente nessun genere con id {cur_opera.get_id_genere()}."
            )

        index = cur_page.genere.findText(cur_genere.get_nome())

        if index != -1:
            cur_page.genere.setCurrentIndex(index)

        cur_page.compositore.setText(cur_opera.get_compositore())
        cur_page.librettista.setText(cur_opera.get_librettista())
        cur_page.atti.setValue(cur_opera.get_numero_atti())
        cur_page.data.setDate(cur_opera.get_data_prima_rappresentazione())
        cur_page.teatro.setText(cur_opera.get_teatro_prima_rappresentazione())

        # Apri la pagina ModificaOperaView
        self.navigation_go_to.emit("modifica_opera", True)

    #
    #
    #

    def nuovo_genere(self):
        """
        Carica la pagina `NuovoGenereView`, dove l'utente può cancellare l'operazione tornando
        dietro utilizzando `cancella_genere()` o confermare la creazione, chiamando altro metodo
        `salva_genere()`, che verifica la correttezza dei dati, crea l'istanza di `Genere` e la
        salva nella lista di generi. I campi di input vengono riscritti prima di visualizzare la
        pagina.
        """
        # Get pagina salvata nel NavigationController
        from view.info.nuovo_genere import NuovoGenereView

        cur_page_dict: dict[str, QWidget | None] = {"value": None}
        self.navigation_get_page.emit("nuovo_genere", cur_page_dict)
        cur_page = cur_page_dict.get("value")

        if not isinstance(cur_page, NuovoGenereView):
            raise TypeError(
                f"cur_page deve essere NuovoGenereView, trovata {type(cur_page)}"
            )

        # Setup default values
        cur_page.nome.setText("")
        cur_page.descrizione.setText("")
        cur_page.input_error.setText("")

        # Apri la pagina NuovoGenereView
        self.navigation_go_to.emit("nuovo_genere", True)

    def modifica_genere(self, id_: int):
        """
        Carica la pagina `ModificaGenereView`, con i dati del genere relativo all'`id_` inseriti
        nei campo di input. Il pulsante Conferma chiama la stessa funzione `salva_genere(is_new=False)`,
        usando un'opzione che permette di modificare i dati del genere esistente e salvarli grazie ad
        una attributo `cur_id_genere` della clase, mentre che il pulsante Cancella chiama
        `cancella_genere()`, tornando dietro senza far cambi nel genere.
        """
        # Get genere da modificare
        cur_genere = self.get_genere(id_)
        if not cur_genere:
            raise IdInesistenteException(f"Non e' presente nessun genere con id {id_}.")

        # Get pagina salvata nel NavigationController
        from view.info.modifica_genere import ModificaGenereView

        cur_page_dict: dict[str, QWidget | None] = {"value": None}
        self.navigation_get_page.emit("modifica_genere", cur_page_dict)
        cur_page = cur_page_dict.get("value")

        if not isinstance(cur_page, ModificaGenereView):
            raise TypeError(
                f"cur_page deve essere ModificaGenereView, trovata {type(cur_page)}"
            )

        # ID utilizzato quando si Conferma la modifica
        cur_page.cur_id_genere = cur_genere.get_id()

        # Setup values
        cur_page.nome.setText(cur_genere.get_nome())
        cur_page.descrizione.setText(cur_genere.get_descrizione())

        # Apri la pagina ModificaGenereView
        self.navigation_go_to.emit("modifica_genere", True)

    def elimina_genere(self, id_: int) -> bool:
        try:
            self.__model.elimina_genere(id_)
        except OggettoInUsoException:
            return False

        return True
