import shutil
import unittest

from model.account.account import Account, Ruolo
from model.exceptions import (
    CredenzialiErrateException,
    DatoIncongruenteException,
    IdInesistenteException,
    IdOccupatoException,
    PermessiInsufficientiException,
    OccupatoException,
)
from model.model import Model


STR_NON_VUOTA = "BCNRFF"
PASSWORD_CONFORME = "lavacheapologist"
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
            DatoIncongruenteException,
            a.cambia_password,
            PASSWORD_CONFORME,
            "1234567",
            Account(STR_NON_VUOTA, PASSWORD_CONFORME, Ruolo.AMMINISTRATORE),
        )
        self.assertRaises(
            CredenzialiErrateException,
            a.cambia_password,
            "12345678",
            PASSWORD_CONFORME,
            Account(STR_NON_VUOTA, PASSWORD_CONFORME, Ruolo.AMMINISTRATORE),
        )
        a.cambia_password(
            PASSWORD_CONFORME,
            "12345678",
            Account(STR_NON_VUOTA, PASSWORD_CONFORME, Ruolo.AMMINISTRATORE),
        )
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
        a2 = Account(STR_NON_VUOTA * 2, PASSWORD_CONFORME, Ruolo.BIGLIETTERIA)
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
            OccupatoException,
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

        a_.set_username(a_.get_username() + STR_NON_VUOTA)
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
        a2 = Account(STR_NON_VUOTA * 2, PASSWORD_CONFORME, Ruolo.BIGLIETTERIA)
        self.__model.aggiungi_account(a2, admin_id)
        self.assertEqual(self.__model.get_accounts(), [admin, a, a2])
        print("Passato GET LISTA")

        a2_ = self.__model.get_accounts()[2]
        a2_.set_username(a2_.get_username() + STR_NON_VUOTA)
        a2 = self.__model.get_accounts()[2]
        self.assertTrue(a2.controlla_password(a2_._Account__password))  # type: ignore
        self.assertNotEqual(a2.get_username(), a2_.get_username())
        print("Passato GET LISTA side effect")

        # LOGIN
        self.assertRaises(
            CredenzialiErrateException, self.__model.login, a.get_username(), "12345678"
        )
        print("Passato LOGIN password errata")

        self.assertRaises(
            CredenzialiErrateException, self.__model.login, "user", "12345678"
        )
        print("Passato LOGIN username inesistente")

        self.assertEqual(self.__model.login("admin", "00000000"), admin_id)
        print("Passato LOGIN")

        # CAMBIO PASSWORD
        self.assertRaises(
            IdInesistenteException,
            self.__model.cambia_password,
            ID_NON_ESISTENTE,
            PASSWORD_CONFORME,
            PASSWORD_CONFORME,
            admin_id,
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

    def tearDown(self) -> None:
        super().tearDown()

        shutil.rmtree("./test_db/")


if __name__ == "__main__":
    unittest.main()
