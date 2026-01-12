from model.pianificazione.spettacolo import Spettacolo
from model.organizzazione.evento import Evento
from model.model import Model
from model.account.account import Account, Ruolo
from model.pianificazione.genere import Genere
from model.pianificazione.opera import Opera
from model.pianificazione.regia import Regia
from model.exceptions import (
    CredenzialiErrateException,
    DatoIncongruenteException,
    IdOccupatoException,
    IdInesistenteException,
    OggettoInUsoException,
    AccountInesistenteException,
    PermessiInsufficientiException,
    UsernameOccupatoException,
)
from datetime import date, datetime
import unittest
import shutil


PASSWORD_CONFORME = "lavacheapologist"
STR_NON_VUOTA = "BCNRFF"
DATA = date(2009, 4, 13)
DATA_ORA_FUTURO = datetime(2970, 1, 1, 0, 0, 0)
ID_NON_ESISTENTE = 777


class TestTell(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.__model = Model("./test_db/")

    # ### ACCOUNTS ###
    def test_account(self):
        print("\n### ACCOUNT ###")

        # CONGRUENZA username
        self.assertRaises(
            DatoIncongruenteException, Account, " ", STR_NON_VUOTA, Ruolo.BIGLIETTERIA
        )
        print("Passato CONGRUENZA username")

        # CONGRUENZA password
        self.assertRaises(
            DatoIncongruenteException, Account, STR_NON_VUOTA, "", Ruolo.BIGLIETTERIA
        )
        self.assertRaises(
            DatoIncongruenteException,
            Account,
            STR_NON_VUOTA,
            "1234567",
            Ruolo.BIGLIETTERIA,
        )
        print("Passato CONGRUENZA password")

        # CONTROLLO PASSWORD
        a = Account(STR_NON_VUOTA, PASSWORD_CONFORME, Ruolo.BIGLIETTERIA)
        self.assertFalse(a.controlla_password("12345678"))
        self.assertTrue(a.controlla_password(PASSWORD_CONFORME))
        print("Passato CONTROLLO PASSWORD")

        # CAMBIO PASSWORD
        self.assertRaises(
            DatoIncongruenteException, a.cambia_password, PASSWORD_CONFORME, "1234567"
        )
        self.assertRaises(
            CredenzialiErrateException,
            a.cambia_password,
            "12345678",
            PASSWORD_CONFORME,
        )
        a.cambia_password(PASSWORD_CONFORME, "12345678")
        self.assertFalse(a.controlla_password(PASSWORD_CONFORME))
        self.assertTrue(a.controlla_password("12345678"))
        print("Passato CAMBIO PASSWORD")

        # CAMBIO RUOLO
        self.assertRaises(
            PermessiInsufficientiException, a.cambia_ruolo, Ruolo.AMMINISTRATORE, a
        )
        print("Passato CAMBIO RUOLO PermessiInsufficienti")

        a.cambia_ruolo(
            Ruolo.AMMINISTRATORE,
            Account(STR_NON_VUOTA, PASSWORD_CONFORME, Ruolo.AMMINISTRATORE),
        )
        self.assertEqual(a.get_ruolo(), Ruolo.AMMINISTRATORE)
        print("Passato CAMBIO RUOLO")

    def test_model_accounts(self):
        print("\n### MODEL ACCOUNTS ###")

        admin_id = int(self.__model._Model__gestore_accounts._GestoreAccounts__lista_accounts[0].get_id())  # type: ignore
        admin = self.__model.get_account(admin_id)
        if admin is None:
            raise Exception()

        # AGGIUNGI
        a = Account(STR_NON_VUOTA, PASSWORD_CONFORME, Ruolo.BIGLIETTERIA)
        self.__model.aggiungi_account(a, admin_id)
        self.assertRaises(
            IdOccupatoException, self.__model.aggiungi_account, a, admin_id
        )
        print("Passato AGGIUNGI IdOccupato")
        a2 = Account(
            STR_NON_VUOTA + STR_NON_VUOTA, PASSWORD_CONFORME, Ruolo.BIGLIETTERIA
        )
        self.assertRaises(
            IdInesistenteException,
            self.__model.aggiungi_account,
            a2,
            ID_NON_ESISTENTE,
        )
        print("Passato AGGIUNGI IdInesistente")
        self.assertRaises(
            PermessiInsufficientiException,
            self.__model.aggiungi_account,
            a2,
            a.get_id(),
        )
        print("Passato AGGIUNGI PermessiInsufficienti")
        a3 = Account(STR_NON_VUOTA, PASSWORD_CONFORME, Ruolo.BIGLIETTERIA)
        self.assertRaises(
            UsernameOccupatoException,
            self.__model.aggiungi_account,
            a3,
            admin_id,
        )
        print("Passato AGGIUNGI UsernameOccupato")

        # GET
        a_ = self.__model.get_account(a.get_id())
        if a_ is None:
            raise Exception()
        self.assertEqual(a_, a)
        print("Passato GET")

        a_.set_username(STR_NON_VUOTA + STR_NON_VUOTA)
        a = self.__model.get_account(a.get_id())
        if a is None:
            raise Exception()
        self.assertTrue(a.controlla_password(a_._Account__password))  # type: ignore
        self.assertNotEqual(a.get_username(), a_.get_username())
        print("Passato GET side effect")

        # PRESENZA ADMIN
        ad = self.__model.get_account(admin_id)
        if ad is None:
            raise Exception()
        self.assertEqual(ad.get_username(), "admin")
        self.assertEqual(ad.get_ruolo(), Ruolo.AMMINISTRATORE)
        self.assertTrue(ad.controlla_password("00000000"))
        print("Passato PRESENZA ADMIN")

        # GET LISTA
        a2 = Account(
            STR_NON_VUOTA + STR_NON_VUOTA, PASSWORD_CONFORME, Ruolo.BIGLIETTERIA
        )
        self.__model.aggiungi_account(a2, admin_id)
        self.assertEqual(self.__model.get_accounts(), [admin, a, a2])
        print("Passato GET LISTA")

        a2_ = self.__model.get_accounts()[2]
        a2_.set_username(STR_NON_VUOTA + STR_NON_VUOTA + STR_NON_VUOTA)
        a2 = self.__model.get_accounts()[2]
        self.assertTrue(a2.controlla_password(a2_._Account__password))  # type: ignore
        self.assertNotEqual(a2.get_username(), a2_.get_username())
        print("Passato GET LISTA side effect")

        # LOGIN
        self.assertRaises(
            CredenzialiErrateException, self.__model.login, a.get_username(), "12345678"
        )
        print("Passato LOGIN CredenzialiErrate")

        self.assertRaises(
            AccountInesistenteException, self.__model.login, "user", "12345678"
        )
        print("Passato LOGIN AccountInesistente")

        self.assertEqual(self.__model.login("admin", "00000000"), admin_id)
        print("Passato LOGIN")

        # CAMBIO PASSWORD
        self.assertRaises(
            IdInesistenteException,
            self.__model.cambia_password,
            ID_NON_ESISTENTE,
            PASSWORD_CONFORME,
            PASSWORD_CONFORME,
        )
        print("Passato CAMBIO PASSWORD IdInesistente")

        # CAMBIO RUOLO
        self.assertRaises(
            IdInesistenteException,
            self.__model.cambia_ruolo,
            ID_NON_ESISTENTE,
            Ruolo.AMMINISTRATORE,
            admin_id,
        )
        print("Passato CAMBIO RUOLO IdNonEsistente (target)")

        self.assertRaises(
            IdInesistenteException,
            self.__model.cambia_ruolo,
            a.get_id(),
            Ruolo.AMMINISTRATORE,
            ID_NON_ESISTENTE,
        )
        print("Passato CAMBIO RUOLO IdNonEsistente (agent)")

        # CARICA
        self.__model._Model__carica_accounts()  # type: ignore
        self.assertEqual(self.__model.get_accounts(), [admin, a, a2])
        print("Passato CARICA")

        # ELIMINA
        self.assertRaises(
            IdInesistenteException,
            self.__model.elimina_account,
            ID_NON_ESISTENTE,
            admin_id,
        )
        print("Passato ELIMINA IdInesistente (target)")

        self.assertRaises(
            IdInesistenteException,
            self.__model.elimina_account,
            a.get_id(),
            ID_NON_ESISTENTE,
        )
        print("Passato ELIMINA IdInesistente (agent)")

        self.assertRaises(
            PermessiInsufficientiException,
            self.__model.elimina_account,
            a.get_id(),
            a2.get_id(),
        )
        print("Passato ELIMINA PermessiInsufficienti")

        self.__model.elimina_account(a.get_id(), admin_id)
        self.assertEqual(self.__model.get_accounts(), [admin, a2])
        print("Passato ELIMINA")

    # ### GENERI ###
    def test_genere(self):
        print("\n### GENERE ###")

        # CONGRUENZA nome
        self.assertRaises(DatoIncongruenteException, Genere, " ", STR_NON_VUOTA)
        print("Passato CONGRUENZA nome")

        # CONGRUENZA descrizione
        self.assertRaises(DatoIncongruenteException, Genere, STR_NON_VUOTA, " ")
        print("Passato CONGRUENZA descrizione")

    def test_model_generi(self):
        print("\n### MODEL GENERI ###")

        # AGGIUNGI
        g = Genere(STR_NON_VUOTA, STR_NON_VUOTA)
        self.__model.aggiungi_genere(g)
        self.assertRaises(IdOccupatoException, self.__model.aggiungi_genere, g)
        print("Passato AGGIUNGI IdOccupato")

        # GET
        g_ = self.__model.get_genere(g.get_id())
        if g_ is None:
            raise Exception()
        self.assertEqual(g_, g)
        print("Passato GET")

        g_.set_nome(STR_NON_VUOTA + STR_NON_VUOTA)
        g = self.__model.get_genere(g.get_id())
        if g is None:
            raise Exception()
        self.assertEqual(g.get_descrizione(), g_.get_descrizione())
        self.assertNotEqual(g.get_nome(), g_.get_nome())
        print("Passato GET side effect")

        # GET LISTA
        g2 = Genere(STR_NON_VUOTA, STR_NON_VUOTA)
        self.__model.aggiungi_genere(g2)
        self.assertEqual(self.__model.get_generi(), [g, g2])
        print("Passato GET LISTA")

        g2_ = self.__model.get_generi()[1]
        g2_.set_nome(STR_NON_VUOTA + STR_NON_VUOTA)
        g2 = self.__model.get_generi()[1]
        self.assertEqual(g2.get_descrizione(), g2_.get_descrizione())
        self.assertNotEqual(g2.get_nome(), g2_.get_nome())
        print("Passato GET LISTA side effect")

        # MODIFICA
        g3 = Genere(STR_NON_VUOTA, STR_NON_VUOTA)
        self.assertRaises(IdInesistenteException, self.__model.modifica_genere, g3)
        print("Passato MODIFICA IdInesistente")

        g = self.__model.get_genere(g.get_id())
        if g is None:
            raise Exception()
        g.set_nome(STR_NON_VUOTA + STR_NON_VUOTA)
        self.__model.modifica_genere(g)
        g_ = self.__model.get_genere(g.get_id())
        if g_ is None:
            raise Exception()
        self.assertEqual(g_, g)
        print("Passato MODIFICA")

        # CARICA
        self.__model._Model__carica_generi()  # type: ignore
        self.assertEqual(self.__model.get_generi(), [g, g2])
        print("Passato CARICA")

        # ELIMINA
        self.assertRaises(
            IdInesistenteException, self.__model.elimina_genere, ID_NON_ESISTENTE
        )
        print("Passato ELIMINA IdInesistente")

        o = Opera(
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            1,
            DATA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            g.get_id(),
        )
        self.__model.aggiungi_opera(o)
        self.assertRaises(
            OggettoInUsoException, self.__model.elimina_genere, g.get_id()
        )
        print("Passato ELIMINA OggettoInUso")
        self.__model.elimina_opera(o.get_id())

        self.__model.elimina_genere(g.get_id())
        self.assertEqual(self.__model.get_generi(), [g2])
        print("Passato ELIMINA")

    # ### OPERE ###
    def test_opera(self):
        print("\n### OPERA ###")

        # CONGRUENZA nome
        self.assertRaises(
            DatoIncongruenteException,
            Opera,
            " ",
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            1,
            DATA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            0,
        )
        print("Passato CONGRUENZA nome")

        # CONGRUENZA compositore
        self.assertRaises(
            DatoIncongruenteException,
            Opera,
            STR_NON_VUOTA,
            " ",
            STR_NON_VUOTA,
            1,
            DATA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            0,
        )
        print("Passato CONGRUENZA compositore")

        # CONGRUENZA librettista
        self.assertRaises(
            DatoIncongruenteException,
            Opera,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            " ",
            1,
            DATA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            0,
        )
        print("Passato CONGRUENZA librettista")

        # CONGRUENZA numero_atti
        self.assertRaises(
            DatoIncongruenteException,
            Opera,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            0,
            DATA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            0,
        )
        self.assertRaises(
            DatoIncongruenteException,
            Opera,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            -1,
            DATA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            0,
        )
        print("Passato CONGRUENZA numero_atti")

        # CONGRUENZA teatro_prima_rappresentazione
        self.assertRaises(
            DatoIncongruenteException,
            Opera,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            1,
            DATA,
            " ",
            STR_NON_VUOTA,
            0,
        )
        print("Passato CONGRUENZA teatro_prima_rappresentazione")

        # CONGRUENZA trama
        self.assertRaises(
            DatoIncongruenteException,
            Opera,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            1,
            DATA,
            STR_NON_VUOTA,
            " ",
            0,
        )
        print("Passato CONGRUENZA trama")

        # CONGRUENZA id_genere
        self.assertRaises(
            DatoIncongruenteException,
            Opera,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            1,
            DATA,
            STR_NON_VUOTA,
            " ",
            -1,
        )
        print("Passato CONGRUENZA id_genere")

    def test_model_opere(self):
        print("\n### MODEL OPERE ###")

        # AGGIUNGI
        o = Opera(
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            1,
            DATA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            ID_NON_ESISTENTE,
        )
        self.assertRaises(IdInesistenteException, self.__model.aggiungi_opera, o)
        print("Passato AGGIUNGI IdInesistente")

        g = Genere(STR_NON_VUOTA, STR_NON_VUOTA)
        self.__model.aggiungi_genere(g)
        o = Opera(
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            1,
            DATA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            g.get_id(),
        )
        self.__model.aggiungi_opera(o)
        self.assertRaises(IdOccupatoException, self.__model.aggiungi_opera, o)
        print("Passato AGGIUNGI IdOccupato")

        # GET
        o_ = self.__model.get_opera(o.get_id())
        if o_ is None:
            raise Exception()
        self.assertEqual(o_, o)
        print("Passato GET")

        o_.set_nome(STR_NON_VUOTA + STR_NON_VUOTA)
        o = self.__model.get_opera(o.get_id())
        if o is None:
            raise Exception()
        self.assertEqual(o.get_compositore(), o_.get_compositore())
        self.assertNotEqual(o.get_nome(), o_.get_nome())
        print("Passato GET side effect")

        # GET LISTA
        o2 = Opera(
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            1,
            DATA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            g.get_id(),
        )
        self.__model.aggiungi_opera(o2)
        self.assertEqual(self.__model.get_opere(), [o, o2])
        print("Passato GET LISTA")

        o2_ = self.__model.get_opere()[1]
        o2_.set_nome(STR_NON_VUOTA + STR_NON_VUOTA)
        o2 = self.__model.get_opere()[1]
        self.assertEqual(o2.get_compositore(), o2_.get_compositore())
        self.assertNotEqual(o2.get_nome(), o2_.get_nome())
        print("Passato GET LISTA side effect")

        # GET LISTA by nome
        o3 = Opera(
            STR_NON_VUOTA + STR_NON_VUOTA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            1,
            DATA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            g.get_id(),
        )
        self.__model.aggiungi_opera(o3)
        o4 = Opera(
            "other",
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            1,
            DATA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            g.get_id(),
        )
        self.__model.aggiungi_opera(o4)
        self.assertEqual(self.__model.get_opere_by_nome(STR_NON_VUOTA), [o, o2, o3])
        print("Passato GET LISTA by nome")

        o2_ = self.__model.get_opere_by_nome(STR_NON_VUOTA)[1]
        o2_.set_nome(STR_NON_VUOTA + STR_NON_VUOTA)
        o2 = self.__model.get_opere_by_nome(STR_NON_VUOTA)[1]
        self.assertEqual(o2.get_compositore(), o2_.get_compositore())
        self.assertNotEqual(o2.get_nome(), o2_.get_nome())
        print("Passato GET LISTA by nome side effect")
        self.__model.elimina_opera(o3.get_id())
        self.__model.elimina_opera(o4.get_id())

        # MODIFICA
        o3 = Opera(
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            1,
            DATA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            g.get_id(),
        )
        self.assertRaises(IdInesistenteException, self.__model.modifica_opera, o3)
        print("Passato MODIFICA IdInesistente")

        o = self.__model.get_opera(o.get_id())
        if o is None:
            raise Exception()
        o.set_nome(STR_NON_VUOTA + STR_NON_VUOTA)
        self.__model.modifica_opera(o)
        o_ = self.__model.get_opera(o.get_id())
        if o_ is None:
            raise Exception()
        self.assertEqual(o_, o)
        print("Passato MODIFICA")

        # CARICA
        self.__model._Model__carica_opere()  # type: ignore
        self.assertEqual(self.__model.get_opere(), [o, o2])
        print("Passato CARICA")

        # ELIMINA
        self.assertRaises(
            IdInesistenteException, self.__model.elimina_opera, ID_NON_ESISTENTE
        )
        print("Passato ELIMINA IdInesistente")

        r = Regia(
            STR_NON_VUOTA, 0, o.get_id(), STR_NON_VUOTA, STR_NON_VUOTA, dict(), dict()
        )
        self.__model.aggiungi_spettacolo(r)
        self.assertRaises(OggettoInUsoException, self.__model.elimina_opera, o.get_id())
        print("Passato ELIMINA OggettoInUso")
        # self.__model._Model__gestore_spettacoli._GestoreSpettacoli__lista_spettacoli = (  # type: ignore
        #     []
        # )
        self.__model.elimina_spettacolo(r.get_id())

        self.__model.elimina_opera(o.get_id())
        self.assertEqual(self.__model.get_opere(), [o2])
        print("Passato ELIMINA")

    # ### REGIE & SPETTACOLI ###
    def test_regia(self):
        print("\n### REGIA ###")

        # CONGRUENZA regista
        self.assertRaises(
            DatoIncongruenteException,
            Regia,
            " ",
            0,
            0,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            dict(),
            dict(),
        )
        print("Passato CONGRUENZA regista")

        # CONGRUENZA anno_produzione
        self.assertRaises(
            DatoIncongruenteException,
            Regia,
            STR_NON_VUOTA,
            -1,
            0,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            dict(),
            dict(),
        )
        print("Passato CONGRUENZA anno_produzione")

        # CONGRUENZA id_opera
        self.assertRaises(
            DatoIncongruenteException,
            Regia,
            STR_NON_VUOTA,
            0,
            -1,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            dict(),
            dict(),
        )
        print("Passato CONGRUENZA id_opera")

        # CONGRUENZA titolo
        self.assertRaises(
            DatoIncongruenteException,
            Regia,
            STR_NON_VUOTA,
            0,
            0,
            " ",
            STR_NON_VUOTA,
            dict(),
            dict(),
        )
        print("Passato CONGRUENZA titolo")

        # CONGRUENZA note
        self.assertRaises(
            DatoIncongruenteException,
            Regia,
            STR_NON_VUOTA,
            0,
            0,
            STR_NON_VUOTA,
            " ",
            dict(),
            dict(),
        )
        print("Passato CONGRUENZA note")

        # CONGRUENZA interpreti
        self.assertRaises(
            DatoIncongruenteException,
            Regia,
            STR_NON_VUOTA,
            0,
            0,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            dict([(" ", STR_NON_VUOTA)]),
            dict(),
        )
        self.assertRaises(
            DatoIncongruenteException,
            Regia,
            STR_NON_VUOTA,
            0,
            0,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            dict([(STR_NON_VUOTA, " ")]),
            dict(),
        )
        print("Passato CONGRUENZA interpreti")

        # CONGRUENZA tecnici
        self.assertRaises(
            DatoIncongruenteException,
            Regia,
            STR_NON_VUOTA,
            0,
            0,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            dict(),
            dict([(" ", STR_NON_VUOTA)]),
        )
        self.assertRaises(
            DatoIncongruenteException,
            Regia,
            STR_NON_VUOTA,
            0,
            0,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            dict(),
            dict([(STR_NON_VUOTA, " ")]),
        )
        print("Passato CONGRUENZA tecnici")

    def test_model_regie(self):
        print("\n### MODEL REGIE ###")

        # AGGIUNGI
        r = Regia(
            STR_NON_VUOTA,
            0,
            ID_NON_ESISTENTE,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            dict(),
            dict(),
        )
        self.assertRaises(IdInesistenteException, self.__model.aggiungi_spettacolo, r)
        print("Passato AGGIUNGI IdInesistente")

        g = Genere(STR_NON_VUOTA, STR_NON_VUOTA)
        self.__model.aggiungi_genere(g)
        o = Opera(
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            1,
            DATA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            g.get_id(),
        )
        self.__model.aggiungi_opera(o)
        r = Regia(
            STR_NON_VUOTA,
            0,
            o.get_id(),
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            dict(),
            dict(),
        )
        self.__model.aggiungi_spettacolo(r)
        self.assertRaises(IdOccupatoException, self.__model.aggiungi_spettacolo, r)
        print("Passato AGGIUNGI IdOccupato")

        # GET
        r_: Regia | None = self.__model.get_spettacolo(r.get_id())  # type: ignore
        if r_ is None:
            raise Exception()
        self.assertEqual(r_, r)
        print("Passato GET")

        r_.set_titolo(STR_NON_VUOTA + STR_NON_VUOTA)
        r: Regia | None = self.__model.get_spettacolo(r.get_id())  # type: ignore
        if r is None:
            raise Exception()
        self.assertEqual(r.get_note(), r_.get_note())
        self.assertNotEqual(r.get_titolo(), r_.get_titolo())
        print("Passato GET side effect")

        # GET LISTA
        r2 = Regia(
            STR_NON_VUOTA,
            0,
            o.get_id(),
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            dict(),
            dict(),
        )
        self.__model.aggiungi_spettacolo(r2)
        self.assertEqual(self.__model.get_spettacoli(), [r, r2])
        print("Passato GET LISTA")

        r2_ = self.__model.get_spettacoli()[1]
        r2_.set_titolo(STR_NON_VUOTA + STR_NON_VUOTA)
        r2 = self.__model.get_spettacoli()[1]
        self.assertEqual(r2.get_note(), r2_.get_note())
        self.assertNotEqual(r2.get_titolo(), r2_.get_titolo())
        print("Passato GET LISTA side effect")

        # GET LISTA by titolo
        r3 = Regia(
            STR_NON_VUOTA,
            0,
            o.get_id(),
            STR_NON_VUOTA + STR_NON_VUOTA,
            STR_NON_VUOTA,
            dict(),
            dict(),
        )
        self.__model.aggiungi_spettacolo(r3)
        r4 = Regia(
            STR_NON_VUOTA,
            0,
            o.get_id(),
            "other",
            STR_NON_VUOTA,
            dict(),
            dict(),
        )
        self.__model.aggiungi_spettacolo(r4)
        self.assertEqual(
            self.__model.get_spettacoli_by_titolo(STR_NON_VUOTA), [r, r2, r3]
        )
        print("Passato GET LISTA by titolo")

        r2_ = self.__model.get_spettacoli_by_titolo(STR_NON_VUOTA)[1]
        r2_.set_titolo(STR_NON_VUOTA + STR_NON_VUOTA)
        r2 = self.__model.get_spettacoli_by_titolo(STR_NON_VUOTA)[1]
        self.assertEqual(r2.get_note(), r2_.get_note())
        self.assertNotEqual(r2.get_titolo(), r2_.get_titolo())
        print("Passato GET LISTA by titolo side effect")
        self.__model.elimina_spettacolo(r3.get_id())
        self.__model.elimina_spettacolo(r4.get_id())

        # GET LISTA by opera
        o2 = Opera(
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            1,
            DATA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            g.get_id(),
        )
        self.__model.aggiungi_opera(o2)
        r3 = Regia(
            STR_NON_VUOTA,
            0,
            o2.get_id(),
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            dict(),
            dict(),
        )
        self.__model.aggiungi_spettacolo(r3)
        self.assertEqual(self.__model.get_regie_by_opera(o.get_id()), [r, r2])
        print("Passato GET LISTA by opera")

        r2_ = self.__model.get_regie_by_opera(o.get_id())[1]
        r2_.set_titolo(STR_NON_VUOTA + STR_NON_VUOTA)
        r2 = self.__model.get_regie_by_opera(o.get_id())[1]
        self.assertEqual(r2.get_note(), r2_.get_note())
        self.assertNotEqual(r2.get_titolo(), r2_.get_titolo())
        print("Passato GET LISTA by opera side effect")
        self.__model.elimina_spettacolo(r3.get_id())
        self.__model.elimina_opera(o2.get_id())

        # MODIFICA
        r3 = Regia(
            STR_NON_VUOTA,
            0,
            ID_NON_ESISTENTE,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            dict(),
            dict(),
        )
        self.assertRaises(IdInesistenteException, self.__model.modifica_spettacolo, r3)
        print("Passato MODIFICA IdInesistente")

        r: Regia | None = self.__model.get_spettacolo(r.get_id())  # type: ignore
        if r is None:
            raise Exception()
        r.set_titolo(STR_NON_VUOTA + STR_NON_VUOTA)
        self.__model.modifica_spettacolo(r)
        r_: Regia | None = self.__model.get_spettacolo(r.get_id())  # type: ignore
        if r_ is None:
            raise Exception()
        self.assertEqual(r_, r)
        print("Passato MODIFICA")

        # CARICA
        self.__model._Model__carica_spettacoli()  # type: ignore
        self.assertEqual(self.__model.get_spettacoli(), [r, r2])
        print("Passato CARICA")

        # ELIMINA
        self.assertRaises(
            IdInesistenteException, self.__model.elimina_spettacolo, ID_NON_ESISTENTE
        )
        print("Passato ELIMINA IdInesistente")

        e = Evento(datetime.now(), r.get_id())
        self.__model.aggiungi_evento(e)
        self.assertRaises(
            OggettoInUsoException, self.__model.elimina_spettacolo, r.get_id()
        )
        print("Passato ELIMINA OggettoInUso")
        # TODO
        # self.__model._Model__gestore_eventi.elimina_evento(e.get_id())  # type: ignore
        self.__model.elimina_evento(e.get_id())

        self.__model.elimina_spettacolo(r.get_id())
        self.assertEqual(self.__model.get_spettacoli(), [r2])
        print("Passato ELIMINA")

    # ### EVENTI ###
    def test_evento(self):
        print("\n### EVENTO ###")

        # CONGRUENZA id_spettacolo
        self.assertRaises(
            DatoIncongruenteException,
            Evento,
            datetime.now(),
            -1,
        )
        print("Passato CONGRUENZA id_spettacolo")

        # ATTIVO
        e = Evento(datetime.now(), 0)
        self.assertFalse(e.attivo())
        e.set_data_ora(DATA_ORA_FUTURO)
        self.assertTrue(e.attivo())
        print("Passato ATTIVO")

    def test_model_evento(self):
        print("\n### MODEL EVENTO ###")

        # AGGIUNGI
        e = Evento(datetime.now(), ID_NON_ESISTENTE)
        self.assertRaises(IdInesistenteException, self.__model.aggiungi_evento, e)
        print("Passato AGGIUNGI IdInesistente")

        s = Spettacolo(STR_NON_VUOTA, STR_NON_VUOTA, dict(()), dict(()))
        self.__model.aggiungi_spettacolo(s)
        e = Evento(datetime.now(), s.get_id())
        self.__model.aggiungi_evento(e)
        self.assertRaises(IdOccupatoException, self.__model.aggiungi_evento, e)
        print("Passato AGGIUNGI IdOccupato")

        # GET
        e_ = self.__model.get_evento(e.get_id())
        if e_ is None:
            raise Exception()
        self.assertEqual(e_, e)
        print("Passato GET")

        e_.set_data_ora(DATA_ORA_FUTURO)
        e = self.__model.get_evento(e.get_id())
        if e is None:
            raise Exception()
        self.assertEqual(e.get_id_spettacolo(), e_.get_id_spettacolo())
        self.assertNotEqual(e.get_data_ora(), e_.get_data_ora())
        print("Passato GET side effect")

        # GET LISTA
        e2 = Evento(datetime.now(), s.get_id())
        self.__model.aggiungi_evento(e2)
        self.assertEqual(self.__model.get_eventi(), [e, e2])
        print("Passato GET LISTA")

        e2_ = self.__model.get_eventi()[1]
        e2_.set_data_ora(DATA_ORA_FUTURO)
        e2 = self.__model.get_eventi()[1]
        self.assertEqual(e2.get_id_spettacolo(), e2_.get_id_spettacolo())
        self.assertNotEqual(e2.get_data_ora(), e2_.get_data_ora())
        print("Passato GET LISTA side effect")

        # GET LISTA by opera
        s2 = Spettacolo(STR_NON_VUOTA, STR_NON_VUOTA, dict(()), dict(()))
        self.__model.aggiungi_spettacolo(s2)
        e3 = Evento(datetime.now(), s2.get_id())
        self.__model.aggiungi_evento(e3)
        self.assertEqual(self.__model.get_eventi_by_spettacolo(s.get_id()), [e, e2])
        print("Passato GET LISTA by spettacolo")

        e2_ = self.__model.get_eventi_by_spettacolo(s.get_id())[1]
        e2_.set_data_ora(DATA_ORA_FUTURO)
        e2 = self.__model.get_eventi_by_spettacolo(s.get_id())[1]
        self.assertEqual(e2.get_id_spettacolo(), e2_.get_id_spettacolo())
        self.assertNotEqual(e2.get_data_ora(), e2_.get_data_ora())
        print("Passato GET LISTA by spettacolo side effect")
        # TODO
        # self.__model._Model__gestore_eventi.elimina_evento(e3.get_id())  # type: ignore
        self.__model.elimina_evento(e3.get_id())
        self.__model.elimina_spettacolo(s2.get_id())

        # MODIFICA
        e3 = Evento(datetime.now(), ID_NON_ESISTENTE)
        self.assertRaises(IdInesistenteException, self.__model.modifica_evento, e3)
        print("Passato MODIFICA IdInesistente")

        e = self.__model.get_evento(e.get_id())
        if e is None:
            raise Exception()
        e.set_data_ora(DATA_ORA_FUTURO)
        self.__model.modifica_evento(e)
        e_ = self.__model.get_evento(e.get_id())
        if e_ is None:
            raise Exception()
        self.assertEqual(e_, e)
        print("Passato MODIFICA")

        # CARICA
        self.__model._Model__carica_eventi()  # type: ignore
        self.assertEqual(self.__model.get_eventi(), [e, e2])
        print("Passato CARICA")

        # TODO
        # # ELIMINA
        # self.assertRaises(
        #     IdInesistenteException, self.__model.elimina_spettacolo, ID_NON_ESISTENTE
        # )
        # print("Passato ELIMINA IdInesistente")

        # e = Evento(datetime.now(), r.get_id())
        # self.__model.aggiungi_evento(e)
        # self.assertRaises(
        #     OggettoInUsoException, self.__model.elimina_spettacolo, r.get_id()
        # )
        # print("Passato ELIMINA OggettoInUso")
        # # TODO
        # # self.__model._Model__gestore_eventi.elimina_evento(e.get_id())  # type: ignore
        # self.__model.elimina_evento(e.get_id())

        # self.__model.elimina_spettacolo(r.get_id())
        # self.assertEqual(self.__model.get_spettacoli(), [r2])
        # print("Passato ELIMINA")

    def tearDown(self) -> None:
        super().tearDown()

        shutil.rmtree("./test_db/")


if __name__ == "__main__":
    unittest.main()
