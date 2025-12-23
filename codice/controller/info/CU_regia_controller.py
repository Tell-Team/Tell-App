from typing import Optional, override

from controller.abstractController.abstractCUController import AbstractCUController

from model.model import Model
from model.pianificazione.regia import Regia
from model.exceptions import (
    DatoIncongruenteException,
    IdInesistenteException,
    IdOccupatoException,
)

from view.info.pagine.modifica_regia import ModificaRegiaView, NuovaRegiaView
from view.spettacoli.widgets.personaleDisplay import PersonaleDisplay
from view.messageView import MessageView


class CURegiaController(AbstractCUController):
    """Gestisce il salvataggio delle regie create e modificate.

    Segnali:
    - goBackRequest(): emesso per tornare alla pagina `VisualizzaOperaView`.
    """

    _view_nuova: NuovaRegiaView
    _view_modifica: ModificaRegiaView

    @override
    def __init__(
        self, model: Model, n_regia_v: NuovaRegiaView, m_regia_v: ModificaRegiaView
    ) -> None:
        if type(n_regia_v) is not NuovaRegiaView:
            raise TypeError("Atteso NuovaRegiaView per n_regia_v.")

        if type(m_regia_v) is not ModificaRegiaView:
            raise TypeError("Atteso ModificaRegiaView per m_regia_v.")

        super().__init__(model, n_regia_v, m_regia_v)

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    @override
    def _connect_signals(self) -> None:
        super()._connect_signals()

        # Aggiungi un interprete alla pagina NuovaRegiaView
        self._view_nuova.aggiungiInterprete.connect(  # type:ignore
            self.__aggiungi_interprete
        )
        # Aggiungi un tecnico alla pagina NuovaRegiaView
        self._view_nuova.aggiungiTecnico.connect(  # type:ignore
            self.__aggiungi_tecnico
        )
        # Display interpreti nella pagina NuovaRegiaView
        self._view_nuova.displayInterpreti.connect(  # type:ignore
            self.__display_interpreti
        )
        # # Display tecnici nella pagina NuovaRegiaView
        self._view_nuova.displayTecnici.connect(  # type:ignore
            self.__display_tecnici
        )

        # Aggiungi un interprete alla pagina NuovaRegiaView
        self._view_modifica.aggiungiInterprete.connect(  # type:ignore
            self.__aggiungi_interprete
        )
        # Aggiungi un tecnico alla pagina NuovaRegiaView
        self._view_modifica.aggiungiTecnico.connect(  # type:ignore
            self.__aggiungi_tecnico
        )
        # Display interpreti nella pagina ModificaRegiaView
        self._view_modifica.displayInterpreti.connect(  # type:ignore
            self.__display_interpreti
        )
        # # Display tecnici nella pagina ModificaRegiaView
        self._view_modifica.displayTecnici.connect(  # type:ignore
            self.__display_tecnici
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __get_regia(self, id_: int) -> Optional[Regia]:
        regia = self._model.get_spettacolo(id_)
        # Verifica che sia Regia e non nessuna (ipotetica) sottoclasse
        #   Usare not isinstance(regia, Regia) nel caso contrario.
        if type(regia) is not Regia:
            return None
        return regia
        # - Questa definizione dovrebbe esser parte del model

    def __aggiungi_regia(self, regia: Regia) -> None:
        self._model.aggiungi_spettacolo(regia)

    def __modifica_regia(self, regia_modificata: Regia) -> None:
        self._model.modifica_spettacolo(regia_modificata)

    def __aggiungi_interprete(
        self, pagina: NuovaRegiaView, nome: str, ruolo: str
    ) -> None:
        """Aggiunge un interprete alla lista_interpreti della pagina.

        :param pagina: pagina dove l'interprete sarà aggiunto
        :param nome: nome dell'interprete
        :param ruolo: ruolo dell'interprete"""
        # Verifiche che ci sia input
        if not nome or not ruolo:
            pagina.label_lista_interpreti_error.setText("Input non valido")
            return

        # Verifica che l'interprete non sia presente nella lista
        if nome in pagina.lista_interpreti.keys():
            pagina.label_lista_interpreti_error.setText("Interprete esistente")
            return

        pagina.lista_interpreti[nome] = ruolo
        pagina.aggiorna_pagina()

    def __aggiungi_tecnico(self, pagina: NuovaRegiaView, nome: str, posto: str) -> None:
        """Aggiunge un tecnico alla lista_tecnici della pagina.

        :param pagina: pagina dove il tecnico sarà aggiunto
        :param nome: nome del tecnico
        :param posto: posto del tecnico"""
        # Verifiche che ci sia input
        if not nome or not posto:
            pagina.label_lista_tecnici_error.setText("Input non valido")
            return

        # Verifica che il tecnico non sia presente nella lista
        if nome in pagina.lista_tecnici.keys():
            pagina.label_lista_tecnici_error.setText("Tecnico esistente")
            return

        pagina.lista_tecnici[nome] = posto
        pagina.aggiorna_pagina()

    def __display_interpreti(self, pagina: NuovaRegiaView) -> None:
        """Visualizza a schermo le informazioni degli interpreti salvati nella
        lista_interpreti della pagina ed assegna a ciascuno un pulsante di elimina.

        :param pagina: pagina dove saranno caricati gli interpreti
        """
        # Ottieni la lista interpreti (dict)
        interpreti = pagina.lista_interpreti

        # Verifica che il dict non sia vuoto
        if len(interpreti) == 0:
            pagina.label_lista_interpreti_vuota.show()
            return

        # Mostra tutti gli interpreti salvati a schermo
        for k, v in interpreti.items():
            cur_interprete = PersonaleDisplay(k, v)

            def elimina_interprete(nome: str) -> None:
                pagina.lista_interpreti.pop(nome)
                pagina.aggiorna_pagina()

            cur_interprete.eliminaRequest.connect(  # type:ignore
                elimina_interprete
            )

            pagina.aggiungi_widget_a_layout(
                cur_interprete, pagina.layout_lista_interpreti
            )

    def __display_tecnici(self, pagina: NuovaRegiaView) -> None:
        """Visualizza a schermo le informazioni dei tecnici salvati nella
        lista_tecnici della pagina ed assegna a ciascuno un pulsante di elimina.

        :param pagina: pagina dove saranno caricati i tecnici
        """
        # Ottieni la lista tecnici (dict)
        tecnici = pagina.lista_tecnici

        # Verifica che il dict non sia vuoto
        if len(tecnici) == 0:
            pagina.label_lista_tecnici_vuota.show()
            return

        # Mostra tutti i tecnici salvati a schermo
        for k, v in tecnici.items():
            cur_tecnico = PersonaleDisplay(k, v)

            def elimina_interprete(nome: str) -> None:
                pagina.lista_tecnici.pop(nome)
                pagina.aggiorna_pagina()

            cur_tecnico.eliminaRequest.connect(  # type:ignore
                elimina_interprete
            )

            pagina.aggiungi_widget_a_layout(cur_tecnico, pagina.layout_lista_tecnici)

    @override
    def _inizia_salvataggio(self, is_new: bool) -> None:
        """Salva la regia creata o modificata nel `GestoreSpettacoli`.

        :param is_new: verifica se si deve creare una regia o modificare una esistente
        """
        CAMPI_NECESSARI = "<b>ATTENZIONE</b>: È necessario compilare i campi di input contrassegnati con *."

        if is_new:
            # Ottieni la pagina NuovaRegiaView
            cur_pagina = self._view_nuova

            # Ottieni l'input inserito
            titolo = cur_pagina.titolo.text()
            note = cur_pagina.note.toPlainText()
            interpreti = cur_pagina.lista_interpreti
            tecnici = cur_pagina.lista_tecnici
            regista = cur_pagina.regista.text()
            anno = cur_pagina.anno.value()
            id_opera = cur_pagina.opera.currentData()

            # Tenta di creare la nuova opera
            try:
                nuova_regia = Regia(
                    regista, anno, id_opera, titolo, note, interpreti, tecnici
                )
            except DatoIncongruenteException as exc:
                # E' stato trovato un campo con input non valido
                cur_pagina.show_input_error(CAMPI_NECESSARI)
                MessageView.mostra_errore(
                    cur_pagina, "Input non valido", f"Si è verificato un errore: {exc}"
                )
            else:
                cur_pagina.show_input_error("")

                try:
                    self.__aggiungi_regia(nuova_regia)
                except IdOccupatoException as exc:
                    # Esiste già una regia con quell'id
                    MessageView.mostra_errore(
                        cur_pagina,
                        "ID Regia occupata",
                        f"Si è verificato un errore: {exc}",
                    )
                else:
                    self.goBackRequest.emit()
        elif not is_new:
            # Ottieni la pagina ModificaRegiaView
            cur_pagina = self._view_modifica

            # Crea una copia della regia originale
            copia_regia: Optional[Regia] = self.__get_regia(cur_pagina.cur_id_regia)
            if not isinstance(copia_regia, Regia):
                # Non esiste regia con l'id salvata nella pagina
                MessageView.mostra_errore(
                    cur_pagina,
                    "Errore nel salvataggio",
                    f"Non è presente nessuna regia con id {cur_pagina.cur_id_regia}. "
                    + "Impossibile effettuare le modifiche.",
                )
                return

            # Ottieni l'input inserito
            titolo = cur_pagina.titolo.text()
            note = cur_pagina.note.toPlainText()
            interpreti = cur_pagina.lista_interpreti
            tecnici = cur_pagina.lista_tecnici
            regista = cur_pagina.regista.text()
            anno = cur_pagina.anno.value()
            id_opera = cur_pagina.opera.currentData()

            # Tenta di modificare la regia
            try:
                copia_regia.set_titolo(titolo)
                copia_regia.set_note(note)
                copia_regia.set_interpreti(interpreti)
                copia_regia.set_tecnici(tecnici)
                copia_regia.set_regista(regista)
                copia_regia.set_anno_produzione(anno)
                copia_regia.set_id_opera(id_opera)
            except DatoIncongruenteException as exc:
                cur_pagina.show_input_error(CAMPI_NECESSARI)
                MessageView.mostra_errore(
                    cur_pagina, "Input non valido", f"Si è verificato un errore: {exc}"
                )
            else:
                cur_pagina.show_input_error("")

                try:
                    self.__modifica_regia(copia_regia)
                except IdInesistenteException as exc:
                    # Non esiste una regia con quell'id
                    MessageView.mostra_errore(
                        cur_pagina,
                        "ID Regia insesistente",
                        f"Si è verificato un errore: {exc}",
                    )
                else:
                    self.goBackRequest.emit()
