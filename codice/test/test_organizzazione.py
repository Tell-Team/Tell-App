from datetime import date, datetime
import shutil
import unittest

from model.pianificazione.genere import Genere
from model.pianificazione.opera import Opera
from model.pianificazione.regia import Regia
from model.exceptions import (
    DatoIncongruenteException,
    IdInesistenteException,
    IdOccupatoException,
)
from model.organizzazione.evento import Evento
from model.pianificazione.spettacolo import Spettacolo
from model.model import Model


DATA_ORA_FUTURO = datetime(2970, 1, 1, 0, 0, 0)
ID_NON_ESISTENTE = 777
STR_NON_VUOTA = "BCNRFF"
DATA = date(2009, 4, 13)


class TestTell(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.__model = Model("./test_db/")

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

        # GET LISTA SPETTACOLI in programma
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
        r3 = Regia(
            STR_NON_VUOTA,
            0,
            o.get_id(),
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            dict(),
            dict(),
        )
        self.__model.aggiungi_spettacolo(r3)
        e4 = Evento(datetime.now(), r2.get_id())
        self.__model.aggiungi_evento(e4)
        e5 = Evento(DATA_ORA_FUTURO, r3.get_id())
        self.__model.aggiungi_evento(e5)
        self.assertEqual(self.__model.get_spettacoli_in_programma(), [r3])
        print("Passato GET LISTA SPETTACOLI in programma")

        r3_ = self.__model.get_spettacoli_in_programma()[0]
        r3_.set_titolo(STR_NON_VUOTA + STR_NON_VUOTA)
        r3 = self.__model.get_spettacoli_in_programma()[0]
        self.assertEqual(r3.get_note(), r3_.get_note())
        self.assertNotEqual(r3.get_titolo(), r3_.get_titolo())
        print("Passato GET LISTA SPETTACOLI in programma side effect")
        # TODO
        # self.__model._Model__gestore_eventi.elimina_evento(e5.get_id())  # type: ignore
        # self.__model._Model__gestore_eventi.elimina_evento(e4.get_id())  # type: ignore
        self.__model.elimina_evento(e5.get_id())
        self.__model.elimina_evento(e4.get_id())
        self.__model.elimina_spettacolo(r3.get_id())
        self.__model.elimina_spettacolo(r2.get_id())
        self.__model.elimina_spettacolo(r.get_id())
        self.__model.elimina_opera(o.get_id())
        self.__model.elimina_genere(g.get_id())

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
