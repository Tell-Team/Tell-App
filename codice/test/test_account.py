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
from model.model.model import Model


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
        account = Account(STR_NON_VUOTA, PASSWORD_CONFORME, Ruolo.BIGLIETTERIA)
        self.assertFalse(account.controlla_password("12345678"))
        self.assertTrue(account.controlla_password(PASSWORD_CONFORME))
        print("Passato CONTROLLO PASSWORD")

        # CAMBIO PASSWORD
        self.assertRaises(
            DatoIncongruenteException,
            account.cambia_password,
            PASSWORD_CONFORME,
            "1234567",
            Account(STR_NON_VUOTA, PASSWORD_CONFORME, Ruolo.AMMINISTRATORE),
        )
        print("Passato CAMBIO PASSWORD DatoIncongruente")

        self.assertRaises(
            CredenzialiErrateException,
            account.cambia_password,
            "12345678",
            PASSWORD_CONFORME,
            Account(STR_NON_VUOTA, PASSWORD_CONFORME, Ruolo.AMMINISTRATORE),
        )
        print("Passato CAMBIO PASSWORD CredenzialiErrate")

        account.cambia_password(
            PASSWORD_CONFORME,
            "12345678",
            Account(STR_NON_VUOTA, PASSWORD_CONFORME, Ruolo.AMMINISTRATORE),
        )
        self.assertFalse(account.controlla_password(PASSWORD_CONFORME))
        self.assertTrue(account.controlla_password("12345678"))
        print("Passato CAMBIO PASSWORD")

        # CAMBIO RUOLO
        self.assertRaises(
            PermessiInsufficientiException,
            account.cambia_ruolo,
            Ruolo.AMMINISTRATORE,
            account,
        )
        print("Passato CAMBIO RUOLO PermessiInsufficienti")

        account.cambia_ruolo(
            Ruolo.AMMINISTRATORE,
            Account(STR_NON_VUOTA, PASSWORD_CONFORME, Ruolo.AMMINISTRATORE),
        )
        self.assertEqual(account.get_ruolo(), Ruolo.AMMINISTRATORE)
        print("Passato CAMBIO RUOLO")

    def test_model_accounts(self):
        print("\n### MODEL ACCOUNTS ###")

        # PRESENZA ADMIN
        admin = self.__model.get_accounts()[0]
        assert admin is not None
        self.assertEqual(admin.get_username(), "admin")
        self.assertEqual(admin.get_ruolo(), Ruolo.AMMINISTRATORE)
        self.assertTrue(admin.controlla_password("00000000"))
        print("Passato PRESENZA ADMIN")

        # AGGIUNGI
        account = Account(STR_NON_VUOTA, PASSWORD_CONFORME, Ruolo.BIGLIETTERIA)
        self.__model.aggiungi_account(account, admin.get_id())
        self.assertRaises(
            IdOccupatoException, self.__model.aggiungi_account, account, admin.get_id()
        )
        print("Passato AGGIUNGI IdOccupato")

        account2 = Account(STR_NON_VUOTA * 2, PASSWORD_CONFORME, Ruolo.BIGLIETTERIA)
        self.assertRaises(
            IdInesistenteException,
            self.__model.aggiungi_account,
            account2,
            ID_NON_ESISTENTE,
        )
        print("Passato AGGIUNGI IdInesistente")

        self.assertRaises(
            PermessiInsufficientiException,
            self.__model.aggiungi_account,
            account2,
            account.get_id(),
        )
        print("Passato AGGIUNGI PermessiInsufficienti")

        account3 = Account(STR_NON_VUOTA, PASSWORD_CONFORME, Ruolo.BIGLIETTERIA)
        self.assertRaises(
            OccupatoException,
            self.__model.aggiungi_account,
            account3,
            admin.get_id(),
        )
        print("Passato AGGIUNGI UsernameOccupato")

        # GET
        account_ = self.__model.get_account(account.get_id())
        assert account_ is not None
        self.assertEqual(account_, account)
        print("Passato GET")

        account_.set_username(account_.get_username() + STR_NON_VUOTA)
        account = self.__model.get_account(account.get_id())
        assert account is not None
        self.assertTrue(account.controlla_password(account_._Account__password))  # type: ignore
        self.assertNotEqual(account.get_username(), account_.get_username())
        print("Passato GET side effect")

        # GET LISTA
        account2 = Account(STR_NON_VUOTA * 2, PASSWORD_CONFORME, Ruolo.BIGLIETTERIA)
        self.__model.aggiungi_account(account2, admin.get_id())
        self.assertEqual(self.__model.get_accounts(), [admin, account, account2])
        print("Passato GET LISTA")

        account2_ = self.__model.get_accounts()[2]
        account2_.set_username(account2_.get_username() + STR_NON_VUOTA)
        account2 = self.__model.get_accounts()[2]
        self.assertTrue(account2.controlla_password(account2_._Account__password))  # type: ignore
        self.assertNotEqual(account2.get_username(), account2_.get_username())
        print("Passato GET LISTA side effect")

        # LOGIN
        self.assertRaises(
            CredenzialiErrateException,
            self.__model.login,
            account.get_username(),
            "12345678",
        )
        print("Passato LOGIN password errata")

        self.assertRaises(
            CredenzialiErrateException, self.__model.login, "user", "12345678"
        )
        print("Passato LOGIN username inesistente")

        self.assertEqual(self.__model.login("admin", "00000000"), admin.get_id())
        print("Passato LOGIN")

        # CAMBIO PASSWORD
        self.assertRaises(
            IdInesistenteException,
            self.__model.cambia_password,
            ID_NON_ESISTENTE,
            PASSWORD_CONFORME,
            PASSWORD_CONFORME,
            admin.get_id(),
        )
        print("Passato CAMBIO PASSWORD IdInesistente")

        # CAMBIO RUOLO
        self.assertRaises(
            IdInesistenteException,
            self.__model.cambia_ruolo,
            ID_NON_ESISTENTE,
            Ruolo.AMMINISTRATORE,
            admin.get_id(),
        )
        print("Passato CAMBIO RUOLO IdNonEsistente (target)")

        self.assertRaises(
            IdInesistenteException,
            self.__model.cambia_ruolo,
            account.get_id(),
            Ruolo.AMMINISTRATORE,
            ID_NON_ESISTENTE,
        )
        print("Passato CAMBIO RUOLO IdNonEsistente (agent)")

        # CARICA
        self.__model._Model__carica_accounts()  # type: ignore
        self.assertEqual(self.__model.get_accounts(), [admin, account, account2])
        print("Passato CARICA")

        # ELIMINA
        self.assertRaises(
            IdInesistenteException,
            self.__model.elimina_account,
            ID_NON_ESISTENTE,
            admin.get_id(),
        )
        print("Passato ELIMINA IdInesistente (target)")

        self.assertRaises(
            IdInesistenteException,
            self.__model.elimina_account,
            account.get_id(),
            ID_NON_ESISTENTE,
        )
        print("Passato ELIMINA IdInesistente (agent)")

        self.assertRaises(
            PermessiInsufficientiException,
            self.__model.elimina_account,
            account.get_id(),
            account2.get_id(),
        )
        print("Passato ELIMINA PermessiInsufficienti")

        self.__model.elimina_account(account.get_id(), admin.get_id())
        self.assertEqual(self.__model.get_accounts(), [admin, account2])
        print("Passato ELIMINA")

    def tearDown(self) -> None:
        super().tearDown()

        shutil.rmtree("./test_db/")


if __name__ == "__main__":
    unittest.main()
