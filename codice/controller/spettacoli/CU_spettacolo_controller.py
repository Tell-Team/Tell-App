from typing import Optional, override

from core.controller import AbstractCUController

from model.model import Model
from model.pianificazione.spettacolo import Spettacolo
from model.exceptions import (
    DatoIncongruenteException,
    IdInesistenteException,
    IdOccupatoException,
)

from view.spettacoli.pagine import ModificaSpettacoloView, NuovoSpettacoloView
from view.spettacoli.widgets import PersonaleDisplay

from view.utils import PopupMessage


class CUSpettacoloController(AbstractCUController):
    """Gestisce il salvataggio degli spettacoli creati e modificati.

    Segnali:
    - goBackRequest(): emesso per tornare alla pagina `SpettacoliSectionView`.
    """

    _view_nuova: NuovoSpettacoloView
    _view_modifica: ModificaSpettacoloView

    @override
    def __init__(
        self,
        model: Model,
        n_spettacolo_v: NuovoSpettacoloView,
        m_spettacolo_v: ModificaSpettacoloView,
    ) -> None:
        if type(n_spettacolo_v) is not NuovoSpettacoloView:
            raise TypeError("Atteso NuovoSpettacoloView per n_spettacolo_v.")

        if type(m_spettacolo_v) is not ModificaSpettacoloView:
            raise TypeError("Atteso ModificaSpettacoloView per m_spettacolo_v.")

        super().__init__(model, n_spettacolo_v, m_spettacolo_v)

    # ------------------------- COLLEGAMENTO DEI SEGNALI -------------------------

    @override
    def _connect_signals(self) -> None:
        super()._connect_signals()

        # Aggiungi un interprete alla pagina NuovoSpettacoloView
        self._view_nuova.aggiungiInterprete.connect(  # type:ignore
            self.__aggiungi_interprete
        )
        # Aggiungi un tecnico alla pagina NuovoSpettacoloView
        self._view_nuova.aggiungiTecnico.connect(  # type:ignore
            self.__aggiungi_tecnico
        )
        # Display interpreti nella pagina NuovoSpettacoloView
        self._view_nuova.displayInterpreti.connect(  # type:ignore
            self.__display_interpreti
        )
        # # Display tecnici nella pagina NuovoSpettacoloView
        self._view_nuova.displayTecnici.connect(  # type:ignore
            self.__display_tecnici
        )

        # Aggiungi un interprete alla pagina ModificaSpettacoloView
        self._view_modifica.aggiungiInterprete.connect(  # type:ignore
            self.__aggiungi_interprete
        )
        # Aggiungi un tecnico alla pagina ModificaSpettacoloView
        self._view_modifica.aggiungiTecnico.connect(  # type:ignore
            self.__aggiungi_tecnico
        )
        # Display interpreti nella pagina ModificaSpettacoloView
        self._view_modifica.displayInterpreti.connect(  # type:ignore
            self.__display_interpreti
        )
        # # Display tecnici nella pagina ModificaSpettacoloView
        self._view_modifica.displayTecnici.connect(  # type:ignore
            self.__display_tecnici
        )

    # ------------------------- METODI DEL CONTROLLER -------------------------

    def __get_spettacolo(self, id_: int) -> Optional[Spettacolo]:
        return self._model.get_spettacolo(id_)

    def __aggiungi_spettacolo(self, spettacolo: Spettacolo) -> None:
        self._model.aggiungi_spettacolo(spettacolo)

    def __modifica_spettacolo(self, spettacolo_modificato: Spettacolo) -> None:
        self._model.modifica_spettacolo(spettacolo_modificato)

    def __aggiungi_interprete(
        self, pagina: NuovoSpettacoloView, nome: str, ruolo: str
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

    def __aggiungi_tecnico(
        self, pagina: NuovoSpettacoloView, nome: str, posto: str
    ) -> None:
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

    def __display_interpreti(self, pagina: NuovoSpettacoloView) -> None:
        """Visualizza a schermo le informazioni degli interpreti salvati nella
        lista_interpreti della pagina ed assegna a ciascuno un pulsante di elimina.

        :param pagina: pagina dove saranno caricati gli interpreti
        """
        # Ottieni la lista interpreti (dict)
        interpreti = pagina.lista_interpreti

        # Verifica che il dict non sia vuoto
        if len(interpreti) == 0:
            pagina.layout_lista_interpreti.if_lista_vuota()
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

            pagina.layout_lista_interpreti.aggiungi_list_item(cur_interprete)

    def __display_tecnici(self, pagina: NuovoSpettacoloView) -> None:
        """Visualizza a schermo le informazioni dei tecnici salvati nella
        lista_tecnici della pagina ed assegna a ciascuno un pulsante di elimina.

        :param pagina: pagina dove saranno caricati i tecnici
        """
        # Ottieni la lista tecnici (dict)
        tecnici = pagina.lista_tecnici

        # Verifica che il dict non sia vuoto
        if len(tecnici) == 0:
            pagina.layout_lista_tecnici.if_lista_vuota()
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

            pagina.layout_lista_tecnici.aggiungi_list_item(cur_tecnico)

    @override
    def _inizia_salvataggio(self, is_new: bool) -> None:
        """Salva lo spettacolo creato o modificato nel `GestoreSpettacoli`.

        :param is_new: verifica se si deve creare uno spettacolo o modificare uno esistente
        """
        CAMPI_NECESSARI = "<b>ATTENZIONE</b>: È necessario compilare i campi di input contrassegnati con *."

        if is_new:
            # Ottieni la pagina NuovoSpettacoloView
            cur_pagina = self._view_nuova

            # Ottieni l'input inserito
            titolo = cur_pagina.titolo.text()
            note = cur_pagina.note.toPlainText()
            interpreti = cur_pagina.lista_interpreti
            tecnici = cur_pagina.lista_tecnici

            # Tenta di creare il nuovo spettacolo
            try:
                nuovo_spettacolo = Spettacolo(titolo, note, interpreti, tecnici)
            except DatoIncongruenteException as exc:
                # È stato trovato un campo con input non valido
                cur_pagina.show_input_error(CAMPI_NECESSARI)
                PopupMessage.mostra_errore(
                    cur_pagina, "Input non valido", f"Si è verificato un errore: {exc}"
                )
            else:
                cur_pagina.show_input_error("")

                try:
                    self.__aggiungi_spettacolo(nuovo_spettacolo)
                except IdOccupatoException as exc:
                    # Esiste già uno spettacolo con quell'id
                    PopupMessage.mostra_errore(
                        cur_pagina,
                        "ID Spettacolo occupata",
                        f"Si è verificato un errore: {exc}",
                    )
                else:
                    self.goBackRequest.emit()
        elif not is_new:
            # Ottieni la pagina ModificaSpettacoloView
            cur_pagina = self._view_modifica

            # Crea una copia dello spettacolo originale
            copia_spettacolo: Optional[Spettacolo] = self.__get_spettacolo(
                cur_pagina.cur_id_spettacolo
            )
            if not isinstance(copia_spettacolo, Spettacolo):
                # Non esiste spettacolo con l'id salvata nella pagina
                PopupMessage.mostra_errore(
                    cur_pagina,
                    "Errore nel salvataggio",
                    f"Non è presente nessuno spettacolo con id {cur_pagina.cur_id_spettacolo}. "
                    + "Impossibile effettuare le modifiche.",
                )
                return

            # Ottieni l'input inserito
            titolo = cur_pagina.titolo.text()
            note = cur_pagina.note.toPlainText()
            interpreti = cur_pagina.lista_interpreti
            tecnici = cur_pagina.lista_tecnici

            # Tenta di modificare lo spettacolo
            try:
                copia_spettacolo.set_titolo(titolo)
                copia_spettacolo.set_note(note)
                copia_spettacolo.set_interpreti(interpreti)
                copia_spettacolo.set_tecnici(tecnici)
            except DatoIncongruenteException as exc:
                cur_pagina.show_input_error(CAMPI_NECESSARI)
                PopupMessage.mostra_errore(
                    cur_pagina, "Input non valido", f"Si è verificato un errore: {exc}"
                )
            else:
                cur_pagina.show_input_error("")

                try:
                    self.__modifica_spettacolo(copia_spettacolo)
                except IdInesistenteException as exc:
                    # Non esiste uno spettacolo con quell'id
                    PopupMessage.mostra_errore(
                        cur_pagina,
                        "ID Spettacolo insesistente",
                        f"Si è verificato un errore: {exc}",
                    )
                else:
                    self.goBackRequest.emit()
