from PyQt6.QtCore import QDate

from controller.context import AppContext, NavigationController

from model.pianificazione.opera import Opera
from model.pianificazione.genere import Genere
from model.pianificazione.regia import Regia  ### TESTING ###

from model.exceptions import IdInesistenteException


class InfoController:
    def __init__(self, app_context: AppContext):
        self.__model = app_context.model
        self.__nav = app_context.nav

    def get_nav(self) -> NavigationController:
        return self.__nav

    def get_opere(self) -> list[Opera]:
        return self.__model.get_opere()

    def get_generi(self) -> list[Genere]:
        return self.__model.get_generi()

    ### TESTING ###
    def get_regie(self) -> list[Regia]:
        return self.__model.get_regie()

    ### TESTING ###
    def get_regie_by_opera(self, id_: int) -> list[Regia]:
        return self.__model.get_regie_by_opera(id_)

    def visualizza_opera(self, id_: int):
        """
        Assegna i dati necessari dell'opera, relativa all'`id_`, nella pagina `VisualizzaOpera`.
        """
        # # Get opera da modificare
        cur_opera = next((o for o in self.get_opere() if o.get_id() == id_), None)
        if not cur_opera:
            raise IdInesistenteException("ID Opera non trovata nella lista opere.")

        # # Get pagina salvata nel NavigationController
        from view.info.visualizza_opera import VisualizzaOpera

        cur_page = self.__nav.get_pages().get("visualizza_opera")
        assert isinstance(cur_page, VisualizzaOpera)

        # # Setup pagina
        cur_page.label_nome.setText(f"{cur_opera.get_nome()}")
        cur_page.label_librettista.setText(f"Libretto di {cur_opera.get_librettista()}")
        cur_page.label_compositore.setText(
            f"Musica composta da {cur_opera.get_compositore()}"
        )

        cur_genere = next(
            (g for g in self.get_generi() if g.get_id() == cur_opera.get_id_genere()),
            None,
        )
        if not cur_genere:
            raise IdInesistenteException("ID Genere non trovata nella lista generi.")

        cur_page.label_genere.setText(f"Genere: {cur_genere.get_nome()}")

        cur_page.label_atti.setText(f"Numero di atti: {cur_opera.get_numero_atti()}")
        cur_page.label_prima_rappresentazione.setText(
            f"È stata rappresentata per prima volta il {cur_opera.get_data_prima_rappresentazione().strftime("%d/%m/%y")} nel teatro {cur_opera.get_teatro_prima_rappresentazione()}"
        )

        # # Apri la pagina VisualizzaOpera
        self.__nav.go_to("visualizza_opera", save_history=True)

    def nuova_opera(self):
        """
        Carica la pagina `FormularioNuovaOpera`, dove l'utente può cancellare l'operazione tornando
        dietro utilizando `cancella_opera(is_new=True)` o confermare la creazione, chiamando altro
        metodo `salva_opera()`, che verifica la correttezza dei dati, crea l'istanza di `Opera` e la
        salva nella lista di opere. I campi di input vengono riscritti prima di visualizzare la
        pagina.
        """
        # # Get pagina salvata nel NavigationController
        from view.info.nuova_opera import FormNuovaOpera

        cur_page = self.__nav.get_pages().get("nuova_opera")
        assert isinstance(cur_page, FormNuovaOpera)

        # # Setup default values
        cur_page.input_nome.setText("")
        cur_page.input_trama.setText("")
        cur_page.input_genere.setCurrentIndex(0)
        cur_page.input_compositore.setText("")
        cur_page.input_librettista.setText("")
        cur_page.input_atti.setValue(0)
        cur_page.input_data.setDate(QDate(1999, 1, 1))
        cur_page.input_teatro.setText("")

        # # Apri pagina FormNuovaOpera
        self.__nav.go_to("nuova_opera", save_history=True)

    def modifica_opera(self, id_: int):
        """
        Carica la pagina `FormularioModificaOpera`, con i dati dell'opera relativa all'`id_` inseriti
        nei campo di input. Il pulsante Conferma chiama la stessa funzione `salva_opera(is_new=False)`,
        ma usando altra opzione che permette di modificare i dati dell'opera esistente e salvare regie
        (necessarie per salvare la modifica) grazie ad una attributo `cur_id_opera` della clase, mentre
        che il pulsante Cancella chiama `cancella_opera(is_new=False)`, elimininando le regie non salvate
        e poi tornando dietro senza far cambi nell'opera.
        """
        # Get opera da modificare
        cur_opera = next((o for o in self.get_opere() if o.get_id() == id_), None)
        if not cur_opera:
            raise IdInesistenteException("ID Opera non trovata nella lista opere.")

        from view.info.modifica_opera import FormModificaOpera

        cur_page = self.__nav.get_pages().get("modifica_opera")
        assert isinstance(cur_page, FormModificaOpera)

        cur_page.cur_id_opera = id_

        # Setup values
        cur_page.input_nome.setText(cur_opera.get_nome())
        cur_page.input_trama.setText(cur_opera.get_trama())

        cur_genere = next(
            (g for g in self.get_generi() if g.get_id() == cur_opera.get_id_genere()),
            None,
        )
        if not cur_genere:
            raise IdInesistenteException("ID Genere non trovata nella lista generi.")

        index = cur_page.input_genere.findData(cur_genere.get_nome())

        if index != -1:
            cur_page.input_genere.setCurrentIndex(index)

        cur_page.input_compositore.setText(cur_opera.get_compositore())
        cur_page.input_librettista.setText(cur_opera.get_librettista())
        cur_page.input_atti.setValue(cur_opera.get_numero_atti())
        cur_page.input_data.setDate(cur_opera.get_data_prima_rappresentazione())
        cur_page.input_teatro.setText(cur_opera.get_teatro_prima_rappresentazione())

        # # Apri la pagina FormModificaOpera
        self.__nav.go_to("modifica_opera", save_history=True)

    def cancella_opera(self, is_new: bool = True):
        """
        Elimina tutte le modifiche fatte nei campi di input, e se l'opera è stata già creata,
        cancella tutti i cambi fatti sulla lista di regie relativi all'opera corrente. Questo include:
        - Eliminazioni di regie della lista;
        - Modifiche sulle istanze;
        - Creazione di nuove istanze.
        """
        if not is_new:
            from view.info.modifica_opera import FormModificaOpera

            cur_page = self.__nav.get_pages().get("modifica_opera")
            assert isinstance(cur_page, FormModificaOpera)

            cur_id_opera = cur_page.cur_id_opera
            real_lista_regie = self.get_regie_by_opera(cur_id_opera)

            temp_cur_regie = cur_page.temp_cur_regie

            for re in cur_page.temp_regie_eliminate:
                for r in real_lista_regie:
                    if re.get_id() == r.get_id():
                        temp_cur_regie.append(re)
            cur_page.temp_regie_eliminate = []

            for r in temp_cur_regie:
                for id_, regista_, anno_ in cur_page.temp_regie_modificate:
                    if r.get_id() == id_:
                        r.set_regista(regista_)
                        r.set_anno_produzione(anno_)
            cur_page.temp_regie_modificate = []

            cur_page.temp_regie_nuove = []

        self.__nav.go_back()

    def salva_opera(self, is_new: bool = True):
        if not is_new:
            ...
            # El modo is_new=False debe incluir un bloque de código para reemplazar, remover y agregar
            # las nuevas regie de la opera.

        # bloque de código para guardar el resto de atributos de la opera
        # Debo también guarda la ID con un bloque if is_new: ... ???

    def nuovo_genere(self):
        """
        Carica la pagina `FormularioNuovoGenere`, dove l'utente può cancellare l'operazione tornando
        dietro utilizando `cancella_genere()` o confermare la creazione, chiamando altro
        metodo `salva_opera()`, che verifica la correttezza dei dati, crea l'istanza di `Genere` e la
        salva nella lista di generi. I campi di input vengono riscritti prima di visualizzare la
        pagina.
        """
        # Get pagina salvata nel NavigationController
        from view.info.nuovo_genere import FormNuovoGenere

        cur_page = self.__nav.get_pages().get("nuovo_genere")
        assert isinstance(cur_page, FormNuovoGenere)

        # Setup default values
        cur_page.input_nome.setText("")
        cur_page.input_descrizione.setText("")

        # Apri la pagina FormNuovoGenere
        self.__nav.go_to("nuovo_genere", save_history=True)

    def modifica_genere(self, id_: int):
        """
        Carica la pagina `FormularioModificaGenere`, con i dati del genere relativo all'`id_` inseriti
        nei campo di input. Il pulsante Conferma chiama la stessa funzione `salva_genere(is_new=False)`,
        usando un'opzione che permette di modificare i dati del genere esistente e salvarli grazie ad
        una attributo `cur_id_genere` della clase, mentre che il pulsante Cancella chiama
        `cancella_genere()`, tornando dietro senza far cambi nel genere.
        """
        # Get genere da modificare
        cur_genere = next((g for g in self.get_generi() if g.get_id() == id_), None)
        if not cur_genere:
            raise IdInesistenteException("ID Genere non trovata nella lista generi.")

        # Get pagina salvata nel NavigationController
        from view.info.modifica_genere import FormModificaGenere

        cur_page = self.__nav.get_pages().get("modifica_genere")
        assert isinstance(cur_page, FormModificaGenere)

        # ID utilizato quando si Conferma la modifica
        cur_page.cur_id_genere = id_

        # Setup values
        cur_page.input_nome.setText(cur_genere.get_nome())
        cur_page.input_descrizione.setText(cur_genere.get_descrizione())

        # # Apri la pagina FormModificaGenere
        self.__nav.go_to("modifica_genere", save_history=True)

    def cancella_genere(self):
        """
        Chiama il metodo `go_back()` del `NavigationController`. Non ha bisogno di riscrivere
        i campi di input perché le funzioni `crea_genere()` e `modifica_genere()` si caricano di
        farlo.
        """
        self.__nav.go_back()

    ### TESTING ###
    def nuova_regia(self, id_opera: int):
        # Get pagina salvata nel NavigationController
        from view.info.nuova_regia import FormNuovaRegia

        cur_page = self.__nav.get_pages().get("nuova_regia")
        assert isinstance(cur_page, FormNuovaRegia)

        # Setup default values
        cur_page.cur_id_opera = id_opera
        cur_page.input_regista.setText("")
        cur_page.input_anno.setValue(0)

        # Apri la pagina FormNuovoGenere
        self.__nav.go_to("nuova_regia", save_history=True)

    ### TESTING ###
    def modifica_regia(self, id_: int, id_opera: int):
        # Get genere da modificare
        cur_regia = next(
            (r for r in self.get_regie_by_opera(id_opera) if r.get_id() == id_), None
        )
        if not cur_regia:
            raise IdInesistenteException("ID Regia non trovata nella lista regie.")

        # Get pagina salvata nel NavigationController
        from view.info.modifica_regia import FormModificaRegia

        cur_page = self.__nav.get_pages().get("modifica_regia")
        assert isinstance(cur_page, FormModificaRegia)

        # ID utilizato quando si Conferma la modifica
        cur_page.cur_id_regia = id_

        # Setup values
        cur_page.input_regista.setText(cur_regia.get_regista())
        cur_page.input_anno.setValue(cur_regia.get_anno_produzione())

        # # Apri la pagina FormModificaGenere
        self.__nav.go_to("modifica_genere", save_history=True)

    ### TESTING ###
    def cancella_regia(self):
        """
        Chiama il metodo `go_back()` del `NavigationController`. Non ha bisogno di riscrivere
        i campi di input perché le funzioni `crea_regia()` e `modifica_regia()` si caricano di
        farlo.
        """
        self.__nav.go_back()
