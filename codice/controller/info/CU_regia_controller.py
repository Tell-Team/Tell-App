from typing import Optional, override

from core.controller import AbstractCUController

from model.model import Model
from model.pianificazione.regia import Regia, Spettacolo
from model.exceptions import (
    DatoIncongruenteException,
    IdInesistenteException,
    IdOccupatoException,
)

from view.info.pagine import ModificaRegiaView, NuovaRegiaView
from view.spettacoli.widgets import PersonaleDisplay

from view.utils import PopupMessage


class CURegiaController(AbstractCUController):
    """Gestisce il salvataggio delle regie create e modificate.

    Segnali
    ---
    - `goBackRequest()`: emesso per tornare alla pagina `VisualizzaOperaView`.
    """

    _view_nuova: NuovaRegiaView
    _view_modifica: ModificaRegiaView

    def __init__(
        self, model: Model, n_regia_v: NuovaRegiaView, m_regia_v: ModificaRegiaView
    ):
        if type(n_regia_v) is not NuovaRegiaView:
            raise TypeError("Atteso NuovaRegiaView per n_regia_v.")
        if type(m_regia_v) is not ModificaRegiaView:
            raise TypeError("Atteso ModificaRegiaView per m_regia_v.")

        super().__init__(model, n_regia_v, m_regia_v)

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    @override
    def _connect_signals(self) -> None:
        super()._connect_signals()

        for pagina in (self._view_nuova, self._view_modifica):
            pagina.aggiungiInterprete.connect(  # type:ignore
                self.__aggiungi_interprete
            )
            pagina.aggiungiTecnico.connect(  # type:ignore
                self.__aggiungi_tecnico
            )
            pagina.displayInterpreti.connect(  # type:ignore
                self.__display_interpreti
            )
            pagina.displayTecnici.connect(  # type:ignore
                self.__display_tecnici
            )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __get_spettacolo(self, id_: int) -> Optional[Spettacolo]:
        return self._model.get_spettacolo(id_)

    def __aggiungi_regia(self, regia: Regia) -> None:
        self._model.aggiungi_spettacolo(regia)

    def __modifica_regia(self, regia_modificata: Regia) -> None:
        self._model.modifica_spettacolo(regia_modificata)

    def __aggiungi_interprete(
        self, pagina: NuovaRegiaView, nome: str, ruolo: str
    ) -> None:
        """Aggiunge un interprete alla `lista_interpreti` della pagina.

        :param pagina: pagina dove l'interprete sarà aggiunto
        :param nome: nome dell'interprete
        :param ruolo: ruolo dell'interprete
        """
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
        """Aggiunge un tecnico alla `lista_tecnici` della pagina.

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
        """Mostra a schermo le informazioni degli interpreti salvati nella
        `lista_interpreti` della pagina ed assegna a ciascuno un pulsante di elimina.

        :param pagina: pagina dove saranno caricati gli interpreti
        """
        # Ottieni la lista interpreti (dict)
        interpreti = pagina.lista_interpreti

        # Verifica che il dict non sia vuoto
        if len(interpreti) == 0:
            pagina.layout_lista_interpreti.mostra_msg_lista_vuota()
            return

        # Mostra tutti gli interpreti salvati a schermo
        for nome, ruolo in interpreti.items():
            current_interprete = PersonaleDisplay(nome, ruolo)

            def elimina_interprete(nome: str) -> None:
                pagina.lista_interpreti.pop(nome)
                pagina.aggiorna_pagina()

            current_interprete.eliminaRequest.connect(  # type:ignore
                elimina_interprete
            )

            pagina.layout_lista_interpreti.aggiungi_list_item(current_interprete)

    def __display_tecnici(self, pagina: NuovaRegiaView) -> None:
        """Mostra a schermo le informazioni dei tecnici salvati nella
        `lista_tecnici` della pagina ed assegna a ciascuno un pulsante di elimina.

        :param pagina: pagina dove saranno caricati i tecnici
        """
        # Ottieni la lista tecnici (dict)
        tecnici = pagina.lista_tecnici

        # Verifica che il dict non sia vuoto
        if len(tecnici) == 0:
            pagina.layout_lista_tecnici.mostra_msg_lista_vuota()
            return

        # Mostra tutti i tecnici salvati a schermo
        for nome, posto in tecnici.items():
            current_tecnico = PersonaleDisplay(nome, posto)

            def elimina_interprete(nome: str) -> None:
                pagina.lista_tecnici.pop(nome)
                pagina.aggiorna_pagina()

            current_tecnico.eliminaRequest.connect(  # type:ignore
                elimina_interprete
            )

            pagina.layout_lista_tecnici.aggiungi_list_item(current_tecnico)

    @override
    def _inizia_salvataggio(self, is_new: bool) -> None:
        """Salva la regia creata o modificata nel `GestoreSpettacoli`.

        :param is_new: verifica se si deve creare una regia o modificare una esistente
        """
        CAMPI_NECESSARI = "<b>ATTENZIONE</b>: È necessario compilare i campi di input contrassegnati con *."

        if is_new:
            current_pagina = self._view_nuova

            # Ottieni l'input inserito
            titolo = current_pagina.titolo.text()
            note = current_pagina.note.toPlainText()
            interpreti = current_pagina.lista_interpreti
            tecnici = current_pagina.lista_tecnici
            regista = current_pagina.regista.text()
            anno = current_pagina.anno.value()
            id_opera = current_pagina.opera.currentData()

            # Tenta di creare la nuova regia
            try:
                nuova_regia = Regia(
                    regista, anno, id_opera, titolo, note, interpreti, tecnici
                )
            except DatoIncongruenteException as exc:
                # È stato trovato un campo con input non valido
                current_pagina.mostra_msg_input_error(CAMPI_NECESSARI)
                PopupMessage.mostra_errore(
                    current_pagina,
                    "Input non valido",
                    f"Si è verificato un errore: {exc}",
                )
            else:
                current_pagina.mostra_msg_input_error("")

                try:
                    self.__aggiungi_regia(nuova_regia)
                except IdOccupatoException as exc:
                    # Esiste già una regia con quell'id
                    PopupMessage.mostra_errore(
                        current_pagina,
                        "ID Regia occupata",
                        f"Si è verificato un errore: {exc}",
                    )
                else:
                    self.goBackRequest.emit()
        elif not is_new:
            current_pagina = self._view_modifica

            # Crea una copia della regia originale
            copia_regia = self.__get_spettacolo(current_pagina.id_current_regia)
            if not isinstance(copia_regia, Regia):
                # Non esiste regia con l'id salvata nella pagina
                PopupMessage.mostra_errore(
                    current_pagina,
                    "Errore nel salvataggio",
                    f"Non è presente nessuna regia con id {current_pagina.id_current_regia}. "
                    + "Impossibile effettuare le modifiche.",
                )
                return

            # Ottieni l'input inserito
            titolo = current_pagina.titolo.text()
            note = current_pagina.note.toPlainText()
            interpreti = current_pagina.lista_interpreti
            tecnici = current_pagina.lista_tecnici
            regista = current_pagina.regista.text()
            anno = current_pagina.anno.value()
            id_opera = current_pagina.opera.currentData()

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
                current_pagina.mostra_msg_input_error(CAMPI_NECESSARI)
                PopupMessage.mostra_errore(
                    current_pagina,
                    "Input non valido",
                    f"Si è verificato un errore: {exc}",
                )
            else:
                current_pagina.mostra_msg_input_error("")

                try:
                    self.__modifica_regia(copia_regia)
                except IdInesistenteException as exc:
                    # Non esiste una regia con quell'id
                    PopupMessage.mostra_errore(
                        current_pagina,
                        "ID Regia insesistente",
                        f"Si è verificato un errore: {exc}",
                    )
                else:
                    self.goBackRequest.emit()
