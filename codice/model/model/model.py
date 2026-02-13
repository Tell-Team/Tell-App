from dataclasses import dataclass
import itertools
from model.organizzazione.occupazione import Occupazione
from model.gestori.gestore_occupazioni import GestoreOccupazioni
from model.organizzazione.prenotazione import Prenotazione
from model.gestori.gestore_prenotazioni import GestorePrenotazioni
from model.organizzazione.prezzo import Prezzo
from model.gestori.gestore_prezzi import GestorePrezzi
from model.gestori.gestore_posti import GestorePosti
from model.organizzazione.posto import Posto
from model.gestori.gestore_sezioni import GestoreSezioni
from model.organizzazione.sezione import Sezione
from model.gestori.gestore_eventi import GestoreEventi
from model.organizzazione.evento import Evento
from model.gestori.gestore_accounts import GestoreAccounts
from model.account.account import Account, Ruolo
from model.gestori.gestore_generi import GestoreGeneri
from model.gestori.gestore_opere import GestoreOpere
from model.gestori.gestore_spettacoli import GestoreSpettacoli
from model.pianificazione.genere import Genere
from model.pianificazione.opera import Opera
from model.pianificazione.spettacolo import Spettacolo
from model.pianificazione.regia import Regia
from model.exceptions import (
    AzioneIncongruenteException,
    DatoIncongruenteException,
    IdInesistenteException,
    OggettoInUsoException,
)
from pickle import load, dump
from typing import Optional
import os


@dataclass(frozen=True)
class DettagliSezione:
    sezione: Sezione
    posti: list[Posto]


@dataclass(frozen=True)
class DettagliPrenotazione:
    spettacolo: Spettacolo
    evento: Evento
    sezioni: list[DettagliSezione]


class Model:
    def __init__(self, db_path: Optional[str]):
        """Throws: DatoIncongruenteException"""
        if db_path is None:
            self.set_db_path("./db/")
        else:
            self.set_db_path(db_path)

        try:
            self.__carica_accounts()
            Account.set_next_id(self.__gestore_accounts.get_max_id() + 1)
        except FileNotFoundError:
            self.__gestore_accounts = GestoreAccounts()

        try:
            self.__carica_generi()
            Genere.set_next_id(self.__gestore_generi.get_max_id() + 1)
        except FileNotFoundError:
            self.__gestore_generi = GestoreGeneri()

        try:
            self.__carica_opere()
            Opera.set_next_id(self.__gestore_opere.get_max_id() + 1)
        except FileNotFoundError:
            self.__gestore_opere = GestoreOpere()

        try:
            self.__carica_spettacoli()
            Spettacolo.set_next_id(self.__gestore_spettacoli.get_max_id() + 1)
        except FileNotFoundError:
            self.__gestore_spettacoli = GestoreSpettacoli()

        try:
            self.__carica_eventi()
            Evento.set_next_id(self.__gestore_eventi.get_max_id() + 1)
        except FileNotFoundError:
            self.__gestore_eventi = GestoreEventi()

        try:
            self.__carica_sezioni()
            Sezione.set_next_id(self.__gestore_sezioni.get_max_id() + 1)
        except FileNotFoundError:
            self.__gestore_sezioni = GestoreSezioni()

        try:
            self.__carica_posti()
            Posto.set_next_id(self.__gestore_posti.get_max_id() + 1)
        except FileNotFoundError:
            self.__gestore_posti = GestorePosti()

        try:
            self.__carica_prezzi()
            Prezzo.set_next_id(self.__gestore_prezzi.get_max_id() + 1)
        except FileNotFoundError:
            self.__gestore_prezzi = GestorePrezzi()

        try:
            self.__carica_prenotazioni()
            Prenotazione.set_next_id(self.__gestore_prenotazioni.get_max_id() + 1)
        except FileNotFoundError:
            self.__gestore_prenotazioni = GestorePrenotazioni()

        try:
            self.__carica_occupazioni()
            Occupazione.set_next_id(self.__gestore_occupazioni.get_max_id() + 1)
        except FileNotFoundError:
            self.__gestore_occupazioni = GestoreOccupazioni()

    # DB Path
    def set_db_path(self, db_path: str):
        """Throws: DatoIncongruenteException"""
        if not os.path.exists(db_path):
            os.makedirs(db_path)
        else:
            if not os.path.isdir(db_path):
                raise DatoIncongruenteException(
                    "Il percorso specificato per il salvataggio dei dati dell'applicazione non è valido (non è una cartella)."
                )

        self.__db_path = db_path

    # Caricamenti
    def __carica_accounts(self):
        with open(os.path.join(self.__db_path, "accounts.pkl"), "rb") as f:
            self.__gestore_accounts: GestoreAccounts = load(f)

    def __carica_generi(self):
        with open(os.path.join(self.__db_path, "generi.pkl"), "rb") as f:
            self.__gestore_generi: GestoreGeneri = load(f)

    def __carica_opere(self):
        with open(os.path.join(self.__db_path, "opere.pkl"), "rb") as f:
            self.__gestore_opere: GestoreOpere = load(f)

    def __carica_spettacoli(self):
        with open(os.path.join(self.__db_path, "spettacoli.pkl"), "rb") as f:
            self.__gestore_spettacoli: GestoreSpettacoli = load(f)

    def __carica_eventi(self):
        with open(os.path.join(self.__db_path, "eventi.pkl"), "rb") as f:
            self.__gestore_eventi: GestoreEventi = load(f)

    def __carica_sezioni(self):
        with open(os.path.join(self.__db_path, "sezioni.pkl"), "rb") as f:
            self.__gestore_sezioni: GestoreSezioni = load(f)

    def __carica_posti(self):
        with open(os.path.join(self.__db_path, "posti.pkl"), "rb") as f:
            self.__gestore_posti: GestorePosti = load(f)

    def __carica_prezzi(self):
        with open(os.path.join(self.__db_path, "prezzi.pkl"), "rb") as f:
            self.__gestore_prezzi: GestorePrezzi = load(f)

    def __carica_prenotazioni(self):
        with open(os.path.join(self.__db_path, "prenotazioni.pkl"), "rb") as f:
            self.__gestore_prenotazioni: GestorePrenotazioni = load(f)

    def __carica_occupazioni(self):
        with open(os.path.join(self.__db_path, "occupazioni.pkl"), "rb") as f:
            self.__gestore_occupazioni: GestoreOccupazioni = load(f)

    # Salvataggi
    def __salva_accounts(self):
        with open(os.path.join(self.__db_path, "accounts.pkl"), "wb") as f:
            dump(self.__gestore_accounts, f)

    def __salva_generi(self):
        with open(os.path.join(self.__db_path, "generi.pkl"), "wb") as f:
            dump(self.__gestore_generi, f)

    def __salva_opere(self):
        with open(os.path.join(self.__db_path, "opere.pkl"), "wb") as f:
            dump(self.__gestore_opere, f)

    def __salva_spettacoli(self):
        with open(os.path.join(self.__db_path, "spettacoli.pkl"), "wb") as f:
            dump(self.__gestore_spettacoli, f)

    def __salva_eventi(self):
        with open(os.path.join(self.__db_path, "eventi.pkl"), "wb") as f:
            dump(self.__gestore_eventi, f)

    def __salva_sezioni(self):
        with open(os.path.join(self.__db_path, "sezioni.pkl"), "wb") as f:
            dump(self.__gestore_sezioni, f)

    def __salva_posti(self):
        with open(os.path.join(self.__db_path, "posti.pkl"), "wb") as f:
            dump(self.__gestore_posti, f)

    def __salva_prezzi(self):
        with open(os.path.join(self.__db_path, "prezzi.pkl"), "wb") as f:
            dump(self.__gestore_prezzi, f)

    def __salva_prenotazioni(self):
        with open(os.path.join(self.__db_path, "prenotazioni.pkl"), "wb") as f:
            dump(self.__gestore_prenotazioni, f)

    def __salva_occupazioni(self):
        with open(os.path.join(self.__db_path, "occupazioni.pkl"), "wb") as f:
            dump(self.__gestore_occupazioni, f)

    # Stato
    def __spettacolo_in_programma(self, spettacolo: Spettacolo) -> bool:
        return any(
            map(
                lambda e: e.attivo(), self.get_eventi_by_spettacolo(spettacolo.get_id())
            )
        )

    # Getters
    #   ACCOUNTS
    def get_account(self, id_: int) -> Optional[Account]:
        return self.__gestore_accounts.get_account(id_)

    def get_accounts(self) -> list[Account]:
        return self.__gestore_accounts.get_accounts()

    #   GENERI
    def get_genere(self, id_: int) -> Optional[Genere]:
        return self.__gestore_generi.get_genere(id_)

    def get_generi(self) -> list[Genere]:
        return self.__gestore_generi.get_generi()

    #   OPERE
    def get_opera(self, id_: int) -> Optional[Opera]:
        return self.__gestore_opere.get_opera(id_)

    def get_opere(self) -> list[Opera]:
        return self.__gestore_opere.get_opere()

    def get_opere_by_nome(self, nome: str) -> list[Opera]:
        return self.__gestore_opere.get_opere_by_nome(nome)

    #   SPETTACOLI
    def get_spettacolo(self, id_: int) -> Optional[Spettacolo]:
        return self.__gestore_spettacoli.get_spettacolo(id_)

    def get_spettacoli(self) -> list[Spettacolo]:
        return self.__gestore_spettacoli.get_spettacoli()

    def get_spettacoli_in_programma(self) -> list[Spettacolo]:
        return list(
            filter(
                lambda s: self.__spettacolo_in_programma(s),
                self.get_spettacoli(),
            )
        )

    def get_spettacoli_in_programma_by_titolo(self, titolo: str) -> list[Spettacolo]:
        titolo_lower = titolo.lower()
        return list(
            filter(
                lambda s: self.__spettacolo_in_programma(s)
                and titolo_lower in s.get_titolo().lower(),
                self.get_spettacoli(),
            )
        )

    def get_spettacoli_by_titolo(self, titolo: str) -> list[Spettacolo]:
        return self.__gestore_spettacoli.get_spettacoli_by_titolo(titolo)

    #   REGIE
    def get_regie_by_opera(self, id_: int) -> list[Regia]:
        return self.__gestore_spettacoli.get_regie_by_opera(id_)

    #   EVENTI
    def get_evento(self, id_: int) -> Optional[Evento]:
        return self.__gestore_eventi.get_evento(id_)

    def get_eventi(self) -> list[Evento]:
        return self.__gestore_eventi.get_eventi()

    def get_eventi_by_spettacolo(self, id_: int) -> list[Evento]:
        return self.__gestore_eventi.get_eventi_by_spettacolo(id_)

    #   SEZIONI
    def get_sezione(self, id_: int) -> Optional[Sezione]:
        return self.__gestore_sezioni.get_sezione(id_)

    def get_sezioni(self) -> list[Sezione]:
        return self.__gestore_sezioni.get_sezioni()

    def get_sezioni_e_file_e_posti_disponibili(
        self, id_evento: int
    ) -> list[tuple[Sezione, list[tuple[str, list[Posto]]]]]:
        """Throws: IdInesistenteException"""
        evento = self.get_evento(id_evento)
        if evento is None:
            raise IdInesistenteException(
                f"Non esiste nessun evento con id {id_evento}."
            )
        id_spettacolo = evento.get_id_spettacolo()

        ids_sezioni_con_prezzo = set(
            map(
                lambda p: p.get_id_sezione(),
                self.__gestore_prezzi.get_prezzi_by_spettacolo(id_spettacolo),
            )
        )
        ids_posti_occupati = list(
            map(
                lambda o: o.get_id_posto(),
                self.__gestore_occupazioni.get_occupazioni_by_evento(id_evento),
            )
        )

        posti_disponibili = sorted(
            list(
                filter(
                    lambda p: p.get_id_sezione() in ids_sezioni_con_prezzo
                    and p.get_id() not in ids_posti_occupati,
                    self.get_posti(),
                )
            ),
            key=lambda p: self.get_sezione(p.get_id_sezione()).get_nome(),  # type: ignore
        )

        sezioni_e_file_e_posti_disponibili: list[
            tuple[Sezione, list[tuple[str, list[Posto]]]]
        ] = list()

        for id_sezione, posti_sezione in itertools.groupby(
            posti_disponibili, lambda p: p.get_id_sezione()
        ):
            sezione: Sezione = self.get_sezione(id_sezione)  # type: ignore

            file_e_posti_disponibili: list[tuple[str, list[Posto]]] = list()

            lista_posti_sezione: list[Posto] = sorted(
                list(posti_sezione), key=lambda p: p.get_fila()
            )
            for fila, posti_fila in itertools.groupby(
                lista_posti_sezione, lambda p: p.get_fila()
            ):
                file_e_posti_disponibili.append(
                    (fila, sorted(list(posti_fila), key=lambda p: p.get_numero()))
                )

            sezioni_e_file_e_posti_disponibili.append(
                (sezione, file_e_posti_disponibili)
            )

        return sezioni_e_file_e_posti_disponibili

    #   POSTI
    def get_posto(self, id_: int) -> Optional[Posto]:
        return self.__gestore_posti.get_posto(id_)

    def get_posti(self) -> list[Posto]:
        return self.__gestore_posti.get_posti()

    def get_posti_by_sezione(self, id_: int) -> list[Posto]:
        return self.__gestore_posti.get_posti_by_sezione(id_)

    #   PREZZI
    def get_prezzo(self, id_: int) -> Optional[Prezzo]:
        return self.__gestore_prezzi.get_prezzo(id_)

    def get_prezzo_by_spettacolo_e_sezione(
        self, id_spettacolo: int, id_sezione: int
    ) -> Optional[Prezzo]:
        return self.__gestore_prezzi.get_prezzo_by_spettacolo_e_sezione(
            id_spettacolo, id_sezione
        )

    def get_prezzi_by_spettacolo(self, id_spettacolo: int) -> list[Prezzo]:
        return self.__gestore_prezzi.get_prezzi_by_spettacolo(id_spettacolo)

    #   PRENOTAZIONI
    def get_prenotazione(self, id_: int) -> Optional[Prenotazione]:
        return self.__gestore_prenotazioni.get_prenotazione(id_)

    def get_prenotazioni(self) -> list[Prenotazione]:
        return self.__gestore_prenotazioni.get_prenotazioni()

    def get_prenotazioni_by_nominativo(self, nominativo: str) -> list[Prenotazione]:
        return self.__gestore_prenotazioni.get_prenotazioni_by_nominativo(nominativo)

    def ammontare_totale_prenotazione(self, id_prenotazione: int) -> float:
        ammontare_totale = 0.0

        for o in self.__gestore_occupazioni.get_occupazioni_by_prenotazione(
            id_prenotazione
        ):
            evento: Evento = self.get_evento(o.get_id_evento())  # type: ignore
            posto: Posto = self.get_posto(o.get_id_posto())  # type: ignore
            prezzo: Prezzo = self.get_prezzo_by_spettacolo_e_sezione(  # type: ignore
                evento.get_id_spettacolo(), posto.get_id_sezione()
            )
            ammontare_totale += prezzo.get_ammontare()

        return ammontare_totale

    def get_dettagli_prenotazione(self, id_prenotazione: int) -> DettagliPrenotazione:
        occupazioni = self.get_occupazioni_by_prenotazione(id_prenotazione)

        evento: Evento = self.get_evento(occupazioni[0].get_id_evento())  # type: ignore
        spettacolo: Spettacolo = self.get_spettacolo(evento.get_id_spettacolo())  # type: ignore

        posti_occupati: list[Posto] = []
        for o in occupazioni:
            posto: Posto = self.get_posto(o.get_id_posto())  # type: ignore
            posti_occupati.append(posto)

        posti_occupati.sort(
            key=lambda p: self.get_sezione(p.get_id_sezione()).get_nome()  # type: ignore
        )
        lista_dettagli_sezioni: list[DettagliSezione] = []
        for id_sezione, posti_sezione in itertools.groupby(
            posti_occupati, lambda p: p.get_id_sezione()
        ):
            sezione: Sezione = self.get_sezione(id_sezione)  # type: ignore

            lista_dettagli_sezioni.append(
                DettagliSezione(
                    sezione, sorted(list(posti_sezione), key=lambda p: p.get_numero())
                )
            )

        dettagli_prenotazione = DettagliPrenotazione(
            spettacolo, evento, lista_dettagli_sezioni
        )
        return dettagli_prenotazione

    #   OCCUPAZIONI
    def get_occupazione(self, id_: int) -> Optional[Occupazione]:
        return self.__gestore_occupazioni.get_occupazione(id_)

    def get_occupazioni_by_prenotazione(
        self, id_prenotazione: int
    ) -> list[Occupazione]:
        return self.__gestore_occupazioni.get_occupazioni_by_prenotazione(
            id_prenotazione
        )

    # Validazione
    def __valida_opera(self, opera: Opera):
        """Throws: IdInesistenteException"""
        if not self.__gestore_generi.ha_genere(opera.get_id_genere()):
            raise IdInesistenteException(
                f"Non è presente nessun genere con id {opera.get_id_genere()}."
            )

    def __valida_regia(self, regia: Regia) -> Opera:
        """Throws: IdInesistenteException"""
        opera = self.get_opera(regia.get_id_opera())
        if opera is None:
            raise IdInesistenteException(
                f"Non è presente nessun'opera con id {regia.get_id_opera()}."
            )

        return opera

    def __valida_evento(self, evento: Evento):
        """Throws: IdInesistenteException"""
        if not self.__gestore_spettacoli.ha_spettacolo(evento.get_id_spettacolo()):
            raise IdInesistenteException(
                f"Non è presente nessuno spettacolo con id {evento.get_id_spettacolo()}."
            )

    def __valida_posto(self, posto: Posto):
        """Throws: IdInesistenteException"""
        if not self.__gestore_sezioni.ha_sezione(posto.get_id_sezione()):
            raise IdInesistenteException(
                f"Non è presente nessuna sezione con id {posto.get_id_sezione()}."
            )

    def __valida_prezzo(self, prezzo: Prezzo):
        """Throws: IdInesistenteException"""
        if not self.__gestore_spettacoli.ha_spettacolo(prezzo.get_id_spettacolo()):
            raise IdInesistenteException(
                f"Non è presente nessuno spettacolo con id {prezzo.get_id_spettacolo()}."
            )

        if not self.__gestore_sezioni.ha_sezione(prezzo.get_id_sezione()):
            raise IdInesistenteException(
                f"Non è presente nessuna sezione con id {prezzo.get_id_sezione()}."
            )

    def __valida_occupazione(self, occupazione: Occupazione):
        """Throws: IdInesistenteException, AzioneIncongruenteException"""
        if not self.__gestore_eventi.ha_evento(occupazione.get_id_evento()):
            raise IdInesistenteException(
                f"Non è presente nessun evento con id {occupazione.get_id_evento()}."
            )

        if not self.__gestore_posti.ha_posto(occupazione.get_id_posto()):
            raise IdInesistenteException(
                f"Non è presente nessun posto con id {occupazione.get_id_posto()}."
            )

        if not self.__gestore_prenotazioni.ha_prenotazione(
            occupazione.get_id_prenotazione()
        ):
            raise IdInesistenteException(
                f"Non è presente nessuna prenotazione con id {occupazione.get_id_prenotazione()}."
            )

        evento: Evento = self.get_evento(occupazione.get_id_evento())  # type: ignore
        id_spettacolo = evento.get_id_spettacolo()
        posto: Posto = self.get_posto(occupazione.get_id_posto())  # type: ignore
        id_sezione = posto.get_id_sezione()

        if (
            self.__gestore_prezzi.get_prezzo_by_spettacolo_e_sezione(
                id_spettacolo, id_sezione
            )
            is None
        ):
            raise AzioneIncongruenteException(
                "La sezione contenente il posto selezionato non ha un prezzo specificato per lo spettacolo selezionato."
            )

    # Login
    def login(self, username: str, password: str) -> int:
        """Throws: CredenzialiErrateException"""
        return self.__gestore_accounts.login(username, password)

    # Modificatori
    #   ACCOUNTS
    def aggiungi_account(self, account: Account, agent_id: int):
        """Throws: OccupatoException, PermessiInsufficientiException, IdOccupatoException, IdInesistenteException"""
        self.__gestore_accounts.aggiungi_account(account, agent_id)
        self.__salva_accounts()

    def elimina_account(self, id_: int, agent_id: int):
        """Throws: IdInesistenteException, PermessiInsufficientiException"""
        self.__gestore_accounts.elimina_account(id_, agent_id)
        self.__salva_accounts()

    def cambia_password(
        self,
        account_id: int,
        password_corrente: str,
        nuova_password: str,
        agent_id: int,
    ):
        """Throws: PermessiInsufficientiException, CredenzialiErrateException, DatoIncongruenteException, IdInesistenteException"""
        self.__gestore_accounts.cambia_password(
            account_id, password_corrente, nuova_password, agent_id
        )
        self.__salva_accounts()

    def cambia_ruolo(self, account_id: int, nuovo_ruolo: Ruolo, agent_id: int):
        """Throws: PermessiInsufficientiException, IdInesistenteException"""
        self.__gestore_accounts.cambia_ruolo(account_id, nuovo_ruolo, agent_id)
        self.__salva_accounts()

    #   GENERI
    def aggiungi_genere(self, genere: Genere):
        """Throws: IdOccupatoException, OccupatoException"""
        self.__gestore_generi.aggiungi_genere(genere)
        self.__salva_generi()

    def elimina_genere(self, id_: int):
        """Throws: OggettoInUsoException, IdInesistenteException"""
        if self.__gestore_opere.genere_in_uso(id_):
            raise OggettoInUsoException("Il genere è ancora legato ad una o più opere.")

        self.__gestore_generi.elimina_genere(id_)
        self.__salva_generi()

    def modifica_genere(self, genere_modificato: Genere):
        """Throws: IdInesistenteException, OccupatoException"""
        self.__gestore_generi.modifica_genere(genere_modificato)
        self.__salva_generi()

    #   OPERE
    def aggiungi_opera(self, opera: Opera):
        """Throws: IdInesistenteException, IdOccupatoException, OccupatoException"""
        self.__valida_opera(opera)

        self.__gestore_opere.aggiungi_opera(opera)
        self.__salva_opere()

    def elimina_opera(self, id_: int):
        """Throws: OggettoInUsoException, IdInesistenteException"""
        if self.__gestore_spettacoli.opera_in_uso(id_):
            raise OggettoInUsoException("L'opera è ancora legata ad una o più regie.")

        self.__gestore_opere.elimina_opera(id_)
        self.__salva_opere()

    def modifica_opera(self, opera_modificata: Opera):
        """Throws: IdInesistenteException, OccupatoException"""
        self.__valida_opera(opera_modificata)

        opera_da_modificare = self.get_opera(opera_modificata.get_id())
        nome_modificato = False
        if opera_da_modificare is not None:
            nome_modificato = (
                opera_modificata.get_nome() != opera_da_modificare.get_nome()
            )

        self.__gestore_opere.modifica_opera(opera_modificata)
        if nome_modificato:
            for r in self.get_regie_by_opera(opera_modificata.get_id()):
                r.set_titolo(opera_modificata.get_nome())
                self.modifica_spettacolo(r)

        self.__salva_opere()
        self.__salva_spettacoli()

    #   SPETTACOLI
    def aggiungi_spettacolo(self, spettacolo: Spettacolo):
        """Throws: IdInesistenteException, IdOccupatoException"""
        if type(spettacolo) is Regia:
            opera = self.__valida_regia(spettacolo)
            spettacolo.set_titolo(opera.get_nome())

        self.__gestore_spettacoli.aggiungi_spettacolo(spettacolo)
        self.__salva_spettacoli()

    def elimina_spettacolo(self, id_: int):
        """Throws: OggettoInUsoException, IdInesistenteException"""
        if self.__gestore_eventi.spettacolo_in_uso(id_):
            raise OggettoInUsoException(
                "Lo spettacolo è ancora legato ad uno o più eventi."
            )

        self.__elimina_prezzi_by_spettacolo(id_)
        self.__gestore_spettacoli.elimina_spettacolo(id_)
        self.__salva_spettacoli()

    def modifica_spettacolo(self, spettacolo_modificato: Spettacolo):
        """Throws: IdInesistenteException"""
        if type(spettacolo_modificato) is Regia:
            self.__valida_regia(spettacolo_modificato)

        self.__gestore_spettacoli.modifica_spettacolo(spettacolo_modificato)
        self.__salva_spettacoli()

    #   EVENTI
    def aggiungi_evento(self, evento: Evento):
        """Throws: IdInesistenteException, IdOccupatoException, OccupatoException"""
        self.__valida_evento(evento)

        self.__gestore_eventi.aggiungi_evento(evento)
        self.__salva_eventi()

    def elimina_evento(self, id_: int):
        """Throws: OggettoInUsoException, IdInesistenteException"""
        if self.__gestore_occupazioni.evento_in_uso(id_):
            raise OggettoInUsoException(
                "L'evento è ancora legato ad una o più occupazioni."
            )

        self.__gestore_eventi.elimina_evento(id_)
        self.__salva_eventi()

    def modifica_evento(self, evento_modificato: Evento):
        """Throws: IdInesistenteException, OccupatoException"""
        self.__valida_evento(evento_modificato)

        self.__gestore_eventi.modifica_evento(evento_modificato)
        self.__salva_eventi()

    #   SEZIONI
    def aggiungi_sezione(self, sezione: Sezione):
        """Throws: IdOccupatoException, OccupatoException"""
        self.__gestore_sezioni.aggiungi_sezione(sezione)
        self.__salva_sezioni()

    def elimina_sezione(self, id_: int):
        """Throws: OggettoInUsoException, IdInesistenteException"""
        if self.__gestore_posti.sezione_in_uso(id_):
            raise OggettoInUsoException(
                "La sezione è ancora legata ad uno o più posti."
            )

        self.__elimina_prezzi_by_sezione(id_)
        self.__gestore_sezioni.elimina_sezione(id_)
        self.__salva_sezioni()

    def modifica_sezione(self, sezione_modificata: Sezione):
        """Throws: IdInesistenteException, OccupatoException"""
        self.__gestore_sezioni.modifica_sezione(sezione_modificata)
        self.__salva_sezioni()

    #   POSTI
    def aggiungi_posto(self, posto: Posto):
        """Throws: IdInesistenteException, IdOccupatoException, OccupatoException"""
        self.__valida_posto(posto)

        self.__gestore_posti.aggiungi_posto(posto)
        self.__salva_posti()

    def elimina_posto(self, id_: int):
        """Throws: OggettoInUsoException, IdInesistenteException"""
        if self.__gestore_occupazioni.posto_in_uso(id_):
            raise OggettoInUsoException(
                "Il posto è ancora legato ad una o più occupazioni."
            )

        self.__gestore_posti.elimina_posto(id_)
        self.__salva_posti()

    def modifica_posto(self, posto_modificato: Posto):
        """Throws: IdInesistenteException, OccupatoException"""
        self.__valida_posto(posto_modificato)

        self.__gestore_posti.modifica_posto(posto_modificato)
        self.__salva_posti()

    #   PREZZI
    def aggiungi_prezzo(self, prezzo: Prezzo):
        """Throws: IdInesistenteException, IdOccupatoException, OccupatoException"""
        self.__valida_prezzo(prezzo)

        self.__gestore_prezzi.aggiungi_prezzo(prezzo)
        self.__salva_prezzi()

    def elimina_prezzo(self, id_: int):
        """Throws: IdInesistenteException"""
        self.__gestore_prezzi.elimina_prezzo(id_)
        self.__salva_prezzi()

    def __elimina_prezzi_by_spettacolo(self, id_spettacolo: int):
        self.__gestore_prezzi.elimina_prezzi_by_spettacolo(id_spettacolo)
        self.__salva_prezzi()

    def __elimina_prezzi_by_sezione(self, id_sezione: int):
        self.__gestore_prezzi.elimina_prezzi_by_sezione(id_sezione)
        self.__salva_prezzi()

    def modifica_prezzo(self, prezzo_modificato: Prezzo):
        """Throws: IdInesistenteException, OccupatoException"""
        self.__valida_prezzo(prezzo_modificato)

        self.__gestore_prezzi.modifica_prezzo(prezzo_modificato)
        self.__salva_prezzi()

    #   PRENOTAZIONI
    def aggiungi_prenotazione(self, prenotazione: Prenotazione):
        """Throws: IdOccupatoException"""
        self.__gestore_prenotazioni.aggiungi_prenotazione(prenotazione)
        self.__salva_prenotazioni()

    def __elimina_occupazioni_by_prenotazione(self, id_prenotazione: int):
        self.__gestore_occupazioni.elimina_occupazioni_by_prenotazione(id_prenotazione)
        self.__salva_occupazioni()

    def elimina_prenotazione(self, id_: int):
        """Throws: IdInesistenteException"""
        self.__elimina_occupazioni_by_prenotazione(id_)
        self.__gestore_prenotazioni.elimina_prenotazione(id_)
        self.__salva_prenotazioni()

    def segna_prenotazione_come_pagata(self, id_: int):
        """Throws: AzioneIncongruenteException, IdInesistenteException"""
        self.__gestore_prenotazioni.segna_come_pagata(id_)
        self.__salva_prenotazioni()

    def segna_prenotazione_come_non_pagata(self, id_: int):
        """Throws: AzioneIncongruenteException, IdInesistenteException"""
        self.__gestore_prenotazioni.segna_come_non_pagata(id_)
        self.__salva_prenotazioni()

    #   OCCUPAZIONI
    def aggiungi_occupazione(self, occupazione: Occupazione):
        """Throws: IdInesistenteException, AzioneIncongruenteException, IdOccupatoException, OccupatoException"""
        self.__valida_occupazione(occupazione)

        self.__gestore_occupazioni.aggiungi_occupazione(occupazione)
        self.__salva_occupazioni()

    def elimina_occupazione(self, id_: int):
        """Throws: IdInesistenteException"""
        self.__gestore_occupazioni.elimina_occupazione(id_)
        self.__salva_occupazioni()

    def modifica_occupazione(self, occupazione_modificata: Occupazione):
        """Throws: IdInesistenteException, AzioneIncongruenteException, OccupatoException"""
        self.__valida_occupazione(occupazione_modificata)

        self.__gestore_occupazioni.modifica_occupazione(occupazione_modificata)
        self.__salva_occupazioni()
