from datetime import date, datetime
import shutil
import unittest

from model.organizzazione.posto import Posto
from model.organizzazione.sezione import Sezione
from model.pianificazione.genere import Genere
from model.pianificazione.opera import Opera
from model.pianificazione.regia import Regia
from model.exceptions import (
    DatoIncongruenteException,
    IdInesistenteException,
    IdOccupatoException,
    OccupatoException,
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

        e2 = Evento(e.get_data_ora(), s.get_id())
        self.assertRaises(OccupatoException, self.__model.aggiungi_evento, e2)
        print("Passato AGGIUNGI Occupato")

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

        # GET LISTA by spettacolo
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
        r3_.set_titolo(r3_.get_titolo() + STR_NON_VUOTA)
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
        e.set_data_ora(e2.get_data_ora())
        self.assertRaises(OccupatoException, self.__model.modifica_evento, e)
        print("Passato MODIFICA Occupato")

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

    # ### SEZIONI ###
    def test_sezione(self):
        print("\n### SEZIONE ###")

        # CONGRUENZA nome
        self.assertRaises(DatoIncongruenteException, Sezione, " ", STR_NON_VUOTA)
        print("Passato CONGRUENZA nome")

        # CONGRUENZA descrizione
        self.assertRaises(DatoIncongruenteException, Sezione, STR_NON_VUOTA, " ")
        print("Passato CONGRUENZA descrizione")

    def test_model_sezioni(self):
        print("\n### MODEL SEZIONI ###")

        # AGGIUNGI
        s = Sezione(STR_NON_VUOTA, STR_NON_VUOTA)
        self.__model.aggiungi_sezione(s)
        self.assertRaises(IdOccupatoException, self.__model.aggiungi_sezione, s)
        print("Passato AGGIUNGI IdOccupato")

        s2 = Sezione(s.get_nome(), STR_NON_VUOTA)
        self.assertRaises(OccupatoException, self.__model.aggiungi_sezione, s2)
        print("Passato AGGIUNGI Occupato")

        # GET
        s_ = self.__model.get_sezione(s.get_id())
        if s_ is None:
            raise Exception()
        self.assertEqual(s_, s)
        print("Passato GET")

        s_.set_nome(s_.get_nome() + STR_NON_VUOTA)
        s = self.__model.get_sezione(s.get_id())
        if s is None:
            raise Exception()
        self.assertEqual(s.get_descrizione(), s_.get_descrizione())
        self.assertNotEqual(s.get_nome(), s_.get_nome())
        print("Passato GET side effect")

        # GET LISTA
        s2 = Sezione(STR_NON_VUOTA * 2, STR_NON_VUOTA)
        self.__model.aggiungi_sezione(s2)
        self.assertEqual(self.__model.get_sezioni(), [s, s2])
        print("Passato GET LISTA")

        s2_ = self.__model.get_sezioni()[1]
        s2_.set_nome(s2_.get_nome() + STR_NON_VUOTA)
        s2 = self.__model.get_sezioni()[1]
        self.assertEqual(s2.get_descrizione(), s2_.get_descrizione())
        self.assertNotEqual(s2.get_nome(), s2_.get_nome())
        print("Passato GET LISTA side effect")

        # MODIFICA
        s3 = Sezione(STR_NON_VUOTA * 3, STR_NON_VUOTA)
        self.assertRaises(IdInesistenteException, self.__model.modifica_sezione, s3)
        print("Passato MODIFICA IdInesistente")

        s = self.__model.get_sezione(s.get_id())
        if s is None:
            raise Exception()
        s.set_nome(s2.get_nome())
        self.assertRaises(OccupatoException, self.__model.modifica_sezione, s)
        print("Passato MODIFICA Occupato")

        s.set_nome(s.get_nome() + STR_NON_VUOTA * 3)
        self.__model.modifica_sezione(s)
        s_ = self.__model.get_sezione(s.get_id())
        if s_ is None:
            raise Exception()
        self.assertEqual(s_, s)
        print("Passato MODIFICA")

        # CARICA
        self.__model._Model__carica_sezioni()  # type: ignore
        self.assertEqual(self.__model.get_sezioni(), [s, s2])
        print("Passato CARICA")

        # # ELIMINA
        # self.assertRaises(
        #     IdInesistenteException, self.__model.elimina_genere, ID_NON_ESISTENTE
        # )
        # print("Passato ELIMINA IdInesistente")

        # o = Opera(
        #     STR_NON_VUOTA,
        #     STR_NON_VUOTA,
        #     STR_NON_VUOTA,
        #     1,
        #     DATA,
        #     STR_NON_VUOTA,
        #     STR_NON_VUOTA,
        #     g.get_id(),
        # )
        # self.__model.aggiungi_opera(o)
        # self.assertRaises(
        #     OggettoInUsoException, self.__model.elimina_genere, g.get_id()
        # )
        # print("Passato ELIMINA OggettoInUso")
        # self.__model.elimina_opera(o.get_id())

        # self.__model.elimina_genere(g.get_id())
        # self.assertEqual(self.__model.get_generi(), [g2])
        # print("Passato ELIMINA")

    # ### POSTI ###
    def test_posto(self):
        print("\n### POSTO ###")

        # CONGRUENZA numero
        self.assertRaises(
            DatoIncongruenteException,
            Posto,
            0,
            0,
        )
        print("Passato CONGRUENZA numero")

        # CONGRUENZA id_sezione
        self.assertRaises(
            DatoIncongruenteException,
            Posto,
            1,
            -1,
        )
        print("Passato CONGRUENZA id_sezione")

    def test_model_posto(self):
        print("\n### MODEL POSTO ###")

        # AGGIUNGI
        p = Posto(1, ID_NON_ESISTENTE)
        self.assertRaises(IdInesistenteException, self.__model.aggiungi_posto, p)
        print("Passato AGGIUNGI IdInesistente")

        s = Sezione(STR_NON_VUOTA, STR_NON_VUOTA)
        self.__model.aggiungi_sezione(s)
        p = Posto(1, s.get_id())
        self.__model.aggiungi_posto(p)
        p.set_numero(p.get_numero() + 1)
        self.assertRaises(IdOccupatoException, self.__model.aggiungi_posto, p)
        print("Passato AGGIUNGI IdOccupato")
        p.set_numero(p.get_numero() - 1)

        p2 = Posto(p.get_numero(), s.get_id())
        self.assertRaises(OccupatoException, self.__model.aggiungi_posto, p2)
        print("Passato AGGIUNGI Occupato")

        # GET
        p_ = self.__model.get_posto(p.get_id())
        if p_ is None:
            raise Exception()
        self.assertEqual(p_, p)
        print("Passato GET")

        p_.set_numero(p_.get_numero() + 1)
        p = self.__model.get_posto(p.get_id())
        if p is None:
            raise Exception()
        self.assertEqual(p.get_id_sezione(), p_.get_id_sezione())
        self.assertNotEqual(p.get_numero(), p_.get_numero())
        print("Passato GET side effect")

        # GET LISTA
        p2 = Posto(2, s.get_id())
        self.__model.aggiungi_posto(p2)
        self.assertEqual(self.__model.get_posti(), [p, p2])
        print("Passato GET LISTA")

        p2_ = self.__model.get_posti()[1]
        p2_.set_numero(p2_.get_numero() + 1)
        p2 = self.__model.get_posti()[1]
        self.assertEqual(p2.get_id_sezione(), p2_.get_id_sezione())
        self.assertNotEqual(p2.get_numero(), p2_.get_numero())
        print("Passato GET LISTA side effect")

        # GET LISTA by sezione
        s2 = Sezione(STR_NON_VUOTA * 4, STR_NON_VUOTA)
        self.__model.aggiungi_sezione(s2)
        p3 = Posto(3, s2.get_id())
        self.__model.aggiungi_posto(p3)
        self.assertEqual(self.__model.get_posti_by_sezione(s.get_id()), [p, p2])
        print("Passato GET LISTA by sezione")

        p2_ = self.__model.get_posti_by_sezione(s.get_id())[1]
        p2_.set_numero(p2_.get_numero() + 1)
        p2 = self.__model.get_posti_by_sezione(s.get_id())[1]
        self.assertEqual(p2.get_id_sezione(), p2_.get_id_sezione())
        self.assertNotEqual(p2.get_numero(), p2_.get_numero())
        print("Passato GET LISTA by sezione side effect")
        # TODO
        # self.__model._Model__gestore_posti.elimina_posto(p3.get_id())  # type: ignore
        # self.__model._Model__gestore_sezioni.elimina_sezione(s2.get_id())  # type: ignore
        self.__model.elimina_posto(p3.get_id())
        self.__model.elimina_sezione(s2.get_id())

        # MODIFICA
        p3 = Posto(4, ID_NON_ESISTENTE)
        self.assertRaises(IdInesistenteException, self.__model.modifica_posto, p3)
        print("Passato MODIFICA IdInesistente")

        p = self.__model.get_posto(p.get_id())
        if p is None:
            raise Exception()
        p.set_numero(p2.get_numero())
        self.assertRaises(OccupatoException, self.__model.modifica_posto, p)
        print("Passato MODIFICA Occupato")

        p.set_numero(p.get_numero() + 3)
        self.__model.modifica_posto(p)
        p_ = self.__model.get_posto(p.get_id())
        if p_ is None:
            raise Exception()
        self.assertEqual(p_, p)
        print("Passato MODIFICA")

        # CARICA
        self.__model._Model__carica_posti()  # type: ignore
        self.assertEqual(self.__model.get_posti(), [p, p2])
        print("Passato CARICA")

        # TODO
        # # ELIMINA
        # self.assertRaises(
        #     IdInesistenteException, self.__model.elimina_spettacolo, ID_NON_ESISTENTE
        # )
        # print("Passato ELIMINA IdInesistente")

        # e = posto(datetime.now(), r.get_id())
        # self.__model.aggiungi_posto(e)
        # self.assertRaises(
        #     OggettoInUsoException, self.__model.elimina_spettacolo, r.get_id()
        # )
        # print("Passato ELIMINA OggettoInUso")
        # # TODO
        # # self.__model._Model__gestore_posti.elimina_posto(e.get_id())  # type: ignore
        # self.__model.elimina_posto(e.get_id())

        # self.__model.elimina_spettacolo(r.get_id())
        # self.assertEqual(self.__model.get_spettacoli(), [r2])
        # print("Passato ELIMINA")

    def tearDown(self) -> None:
        super().tearDown()

        shutil.rmtree("./test_db/")


if __name__ == "__main__":
    unittest.main()
