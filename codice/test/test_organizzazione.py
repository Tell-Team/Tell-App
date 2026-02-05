from datetime import date, datetime
import shutil
import unittest

from model.organizzazione.prenotazione import Prenotazione
from model.organizzazione.occupazione import Occupazione
from model.organizzazione.prezzo import Prezzo
from model.organizzazione.posto import Posto
from model.organizzazione.sezione import Sezione
from model.pianificazione.genere import Genere
from model.pianificazione.opera import Opera
from model.pianificazione.regia import Regia
from model.exceptions import (
    AzioneIncongruenteException,
    DatoIncongruenteException,
    IdInesistenteException,
    IdOccupatoException,
    OccupatoException,
    OggettoInUsoException,
)
from model.organizzazione.evento import Evento
from model.pianificazione.spettacolo import Spettacolo
from model.model import Model


DATA_ORA_FUTURO = datetime(2970, 1, 1, 0, 0, 0)
DATA_ORA_PASSATO = datetime(1904, 6, 16, 8)
ID_NON_ESISTENTE = 777
STR_NON_VUOTA = "BCNRFF"
DATA = date(2009, 4, 13)
FLOAT_NONZERO = 1.30


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
            DATA_ORA_PASSATO,
            -1,
        )
        print("Passato CONGRUENZA id_spettacolo")

        # ATTIVO
        e = Evento(DATA_ORA_PASSATO, 0)
        self.assertFalse(e.attivo())
        e.set_data_ora(DATA_ORA_FUTURO)
        self.assertTrue(e.attivo())
        print("Passato ATTIVO")

    def test_model_evento(self):
        print("\n### MODEL EVENTO ###")

        # AGGIUNGI
        e = Evento(DATA_ORA_PASSATO, ID_NON_ESISTENTE)
        self.assertRaises(IdInesistenteException, self.__model.aggiungi_evento, e)
        print("Passato AGGIUNGI IdInesistente")

        s = Spettacolo(STR_NON_VUOTA, STR_NON_VUOTA, dict(), dict())
        self.__model.aggiungi_spettacolo(s)
        e = Evento(DATA_ORA_PASSATO, s.get_id())
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
        s2 = Spettacolo(STR_NON_VUOTA, STR_NON_VUOTA, dict(), dict())
        self.__model.aggiungi_spettacolo(s2)
        e3 = Evento(DATA_ORA_PASSATO, s2.get_id())
        self.__model.aggiungi_evento(e3)
        self.assertEqual(self.__model.get_eventi_by_spettacolo(s.get_id()), [e, e2])
        print("Passato GET LISTA by spettacolo")

        e2_ = self.__model.get_eventi_by_spettacolo(s.get_id())[1]
        e2_.set_data_ora(DATA_ORA_FUTURO)
        e2 = self.__model.get_eventi_by_spettacolo(s.get_id())[1]
        self.assertEqual(e2.get_id_spettacolo(), e2_.get_id_spettacolo())
        self.assertNotEqual(e2.get_data_ora(), e2_.get_data_ora())
        print("Passato GET LISTA by spettacolo side effect")
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
            dict(),
            dict(),
        )
        self.__model.aggiungi_spettacolo(r)
        r2 = Regia(
            STR_NON_VUOTA,
            0,
            o.get_id(),
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
            dict(),
            dict(),
        )
        self.__model.aggiungi_spettacolo(r3)
        e4 = Evento(DATA_ORA_PASSATO, r2.get_id())
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
        self.__model.elimina_evento(e5.get_id())
        self.__model.elimina_evento(e4.get_id())
        self.__model.elimina_spettacolo(r3.get_id())
        self.__model.elimina_spettacolo(r2.get_id())
        self.__model.elimina_spettacolo(r.get_id())
        self.__model.elimina_opera(o.get_id())
        self.__model.elimina_genere(g.get_id())

        # MODIFICA
        e3 = Evento(DATA_ORA_PASSATO, ID_NON_ESISTENTE)
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

        # ELIMINA
        self.assertRaises(
            IdInesistenteException, self.__model.elimina_evento, ID_NON_ESISTENTE
        )
        print("Passato ELIMINA IdInesistente")

        se = Sezione(STR_NON_VUOTA, STR_NON_VUOTA)
        self.__model.aggiungi_sezione(se)
        po = Posto(STR_NON_VUOTA, 1, se.get_id())
        self.__model.aggiungi_posto(po)
        pr = Prenotazione(STR_NON_VUOTA, DATA_ORA_PASSATO)
        self.__model.aggiungi_prenotazione(pr)
        o = Occupazione(e.get_id(), po.get_id(), pr.get_id())
        self.__model.aggiungi_occupazione(o)
        self.assertRaises(
            OggettoInUsoException, self.__model.elimina_evento, e.get_id()
        )
        print("Passato ELIMINA OggettoInUso")

        self.__model.elimina_occupazione(o.get_id())
        self.__model.elimina_evento(e.get_id())
        self.assertEqual(self.__model.get_eventi(), [e2])
        print("Passato ELIMINA")

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

        # GET SEZIONI E FILE E POSTI DISPONIBILI
        sp = Spettacolo(STR_NON_VUOTA, STR_NON_VUOTA, dict(), dict())
        self.__model.aggiungi_spettacolo(sp)
        sp2 = Spettacolo(STR_NON_VUOTA, STR_NON_VUOTA, dict(), dict())
        self.__model.aggiungi_spettacolo(sp2)

        e = Evento(DATA_ORA_PASSATO, sp.get_id())
        self.__model.aggiungi_evento(e)
        e2 = Evento(DATA_ORA_PASSATO, sp2.get_id())
        self.__model.aggiungi_evento(e2)

        pr = Prenotazione(STR_NON_VUOTA, DATA_ORA_PASSATO)
        self.__model.aggiungi_prenotazione(pr)

        # s: sezione senza prezzi
        p11 = Posto(STR_NON_VUOTA, 1, s.get_id())
        self.__model.aggiungi_posto(p11)

        # s2: sezione con prezzo per un altro spettacolo
        self.__model.aggiungi_prezzo(Prezzo(FLOAT_NONZERO, sp2.get_id(), s2.get_id()))

        p21 = Posto(STR_NON_VUOTA, 1, s2.get_id())
        self.__model.aggiungi_posto(p21)

        # s3: sezione disponibile
        s3 = Sezione(STR_NON_VUOTA * 3, STR_NON_VUOTA)
        self.__model.aggiungi_sezione(s3)
        self.__model.aggiungi_prezzo(Prezzo(FLOAT_NONZERO, sp.get_id(), s3.get_id()))

        #   p31: posto disponibile in fila STR_NON_VUOTA
        p31 = Posto(STR_NON_VUOTA, 1, s3.get_id())
        self.__model.aggiungi_posto(p31)
        #   p32: posto occupato per un altro evento in fila STR_NON_VUOTA*2
        p32 = Posto(STR_NON_VUOTA * 2, 2, s3.get_id())
        self.__model.aggiungi_posto(p32)
        o32 = Occupazione(e2.get_id(), p32.get_id(), pr.get_id())
        self.__model.aggiungi_occupazione(o32)
        #   p33: posto occupato per questo evento
        p33 = Posto(STR_NON_VUOTA, 3, s3.get_id())
        self.__model.aggiungi_posto(p33)
        o33 = Occupazione(e.get_id(), p33.get_id(), pr.get_id())
        self.__model.aggiungi_occupazione(o33)

        # s4: sezione vuota
        s4 = Sezione(STR_NON_VUOTA * 4, STR_NON_VUOTA)
        self.__model.aggiungi_sezione(s4)
        self.__model.aggiungi_prezzo(Prezzo(FLOAT_NONZERO, sp.get_id(), s4.get_id()))

        # s5: sezione occupata
        s5 = Sezione(STR_NON_VUOTA * 5, STR_NON_VUOTA)
        self.__model.aggiungi_sezione(s5)
        self.__model.aggiungi_prezzo(Prezzo(FLOAT_NONZERO, sp.get_id(), s5.get_id()))

        #   p51: posto occupato per questo evento
        p51 = Posto(STR_NON_VUOTA, 1, s5.get_id())
        self.__model.aggiungi_posto(p51)
        o51 = Occupazione(e.get_id(), p51.get_id(), pr.get_id())
        self.__model.aggiungi_occupazione(o51)

        #   p52: posto occupato per questo evento
        p52 = Posto(STR_NON_VUOTA, 2, s5.get_id())
        self.__model.aggiungi_posto(p52)
        o52 = Occupazione(e.get_id(), p52.get_id(), pr.get_id())
        self.__model.aggiungi_occupazione(o52)

        self.assertRaises(
            IdInesistenteException,
            self.__model.get_sezioni_e_file_e_posti_disponibili,
            ID_NON_ESISTENTE,
        )
        print("Passato GET SEZIONI E FILE E POSTI DISPONIBILI IdInesistente")

        self.assertEqual(
            self.__model.get_sezioni_e_file_e_posti_disponibili(e.get_id()),
            [(s3, [(STR_NON_VUOTA, [p31]), (STR_NON_VUOTA * 2, [p32])])],
        )
        print("Passato GET SEZIONI E FILE E POSTI DISPONIBILI")

        s3_ = self.__model.get_sezioni_e_file_e_posti_disponibili(e.get_id())[0][0]
        s3_.set_nome(s3_.get_nome() + STR_NON_VUOTA)
        s3 = self.__model.get_sezioni_e_file_e_posti_disponibili(e.get_id())[0][0]
        self.assertEqual(s3.get_descrizione(), s3_.get_descrizione())
        self.assertNotEqual(s3.get_nome(), s3_.get_nome())
        print("Passato GET SEZIONI E FILE E POSTI DISPONIBILI side effect sezione")

        p31_ = self.__model.get_sezioni_e_file_e_posti_disponibili(e.get_id())[0][1][0][
            1
        ][0]
        p31_.set_numero(p31_.get_numero() + 1)
        p31 = self.__model.get_sezioni_e_file_e_posti_disponibili(e.get_id())[0][1][0][
            1
        ][0]
        self.assertEqual(p31.get_id_sezione(), p31_.get_id_sezione())
        self.assertNotEqual(p31.get_numero(), p31_.get_numero())
        print("Passato GET SEZIONI E FILE E POSTI DISPONIBILI side effect posto")
        self.__model.elimina_occupazione(o32.get_id())
        self.__model.elimina_occupazione(o33.get_id())
        self.__model.elimina_occupazione(o51.get_id())
        self.__model.elimina_occupazione(o52.get_id())
        self.__model.elimina_posto(p11.get_id())
        self.__model.elimina_posto(p31.get_id())
        self.__model.elimina_posto(p32.get_id())
        self.__model.elimina_posto(p33.get_id())
        self.__model.elimina_posto(p51.get_id())
        self.__model.elimina_posto(p52.get_id())
        self.__model.elimina_sezione(s3.get_id())
        self.__model.elimina_sezione(s4.get_id())
        self.__model.elimina_sezione(s5.get_id())

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

        s.set_nome(s.get_nome() + STR_NON_VUOTA * 6)
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

        # ELIMINA
        self.assertRaises(
            IdInesistenteException, self.__model.elimina_sezione, ID_NON_ESISTENTE
        )
        print("Passato ELIMINA IdInesistente")

        p = Posto(STR_NON_VUOTA, 1, s.get_id())
        self.__model.aggiungi_posto(p)
        self.assertRaises(
            OggettoInUsoException, self.__model.elimina_sezione, s.get_id()
        )
        print("Passato ELIMINA OggettoInUso")
        self.__model.elimina_posto(p.get_id())

        self.__model.elimina_sezione(s.get_id())
        self.assertEqual(self.__model.get_sezioni(), [s2])
        print("Passato ELIMINA")

    # ### POSTI ###
    def test_posto(self):
        print("\n### POSTO ###")

        # CONGRUENZA fila
        self.assertRaises(
            DatoIncongruenteException,
            Posto,
            " ",
            1,
            0,
        )
        print("Passato CONGRUENZA fila")

        # CONGRUENZA numero
        self.assertRaises(
            DatoIncongruenteException,
            Posto,
            STR_NON_VUOTA,
            0,
            0,
        )
        print("Passato CONGRUENZA numero")

        # CONGRUENZA id_sezione
        self.assertRaises(
            DatoIncongruenteException,
            Posto,
            STR_NON_VUOTA,
            1,
            -1,
        )
        print("Passato CONGRUENZA id_sezione")

    def test_model_posto(self):
        print("\n### MODEL POSTO ###")

        # AGGIUNGI
        p = Posto(STR_NON_VUOTA, 1, ID_NON_ESISTENTE)
        self.assertRaises(IdInesistenteException, self.__model.aggiungi_posto, p)
        print("Passato AGGIUNGI IdInesistente")

        s = Sezione(STR_NON_VUOTA, STR_NON_VUOTA)
        self.__model.aggiungi_sezione(s)
        p = Posto(STR_NON_VUOTA, 1, s.get_id())
        self.__model.aggiungi_posto(p)
        p.set_numero(p.get_numero() + 1)
        self.assertRaises(IdOccupatoException, self.__model.aggiungi_posto, p)
        print("Passato AGGIUNGI IdOccupato")
        p.set_numero(p.get_numero() - 1)

        p2 = Posto(p.get_fila(), p.get_numero(), s.get_id())
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
        p2 = Posto(STR_NON_VUOTA * 2, 2, s.get_id())
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
        p3 = Posto(STR_NON_VUOTA * 3, 3, s2.get_id())
        self.__model.aggiungi_posto(p3)
        self.assertEqual(self.__model.get_posti_by_sezione(s.get_id()), [p, p2])
        print("Passato GET LISTA by sezione")

        p2_ = self.__model.get_posti_by_sezione(s.get_id())[1]
        p2_.set_numero(p2_.get_numero() + 1)
        p2 = self.__model.get_posti_by_sezione(s.get_id())[1]
        self.assertEqual(p2.get_id_sezione(), p2_.get_id_sezione())
        self.assertNotEqual(p2.get_numero(), p2_.get_numero())
        print("Passato GET LISTA by sezione side effect")
        self.__model.elimina_posto(p3.get_id())
        self.__model.elimina_sezione(s2.get_id())

        # MODIFICA
        p4 = Posto(STR_NON_VUOTA * 4, 4, ID_NON_ESISTENTE)
        self.assertRaises(IdInesistenteException, self.__model.modifica_posto, p4)
        print("Passato MODIFICA IdInesistente")

        p = self.__model.get_posto(p.get_id())
        if p is None:
            raise Exception()
        p.set_fila(p2.get_fila())
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

        # ELIMINA
        self.assertRaises(
            IdInesistenteException, self.__model.elimina_posto, ID_NON_ESISTENTE
        )
        print("Passato ELIMINA IdInesistente")

        sp = Spettacolo(STR_NON_VUOTA, STR_NON_VUOTA, dict(), dict())
        self.__model.aggiungi_spettacolo(sp)
        e = Evento(DATA_ORA_PASSATO, sp.get_id())
        self.__model.aggiungi_evento(e)
        pr = Prenotazione(STR_NON_VUOTA, DATA_ORA_PASSATO)
        self.__model.aggiungi_prenotazione(pr)
        o = Occupazione(e.get_id(), p.get_id(), pr.get_id())
        self.__model.aggiungi_occupazione(o)
        self.assertRaises(OggettoInUsoException, self.__model.elimina_posto, p.get_id())
        print("Passato ELIMINA OggettoInUso")

        self.__model.elimina_occupazione(o.get_id())
        self.__model.elimina_posto(p.get_id())
        self.assertEqual(self.__model.get_posti(), [p2])
        print("Passato ELIMINA")

    # ### PREZZI ###
    def test_prezzo(self):
        print("\n### PREZZO ###")

        # CONGRUENZA ammontare
        self.assertRaises(
            DatoIncongruenteException,
            Prezzo,
            -0.01,
            0,
            0,
        )
        print("Passato CONGRUENZA ammontare")

        # CONGRUENZA id_spettacolo
        self.assertRaises(
            DatoIncongruenteException,
            Prezzo,
            0.0,
            -1,
            0,
        )
        print("Passato CONGRUENZA id_spettacolo")

        # CONGRUENZA id_sezione
        self.assertRaises(
            DatoIncongruenteException,
            Prezzo,
            0.0,
            0,
            -1,
        )
        print("Passato CONGRUENZA id_sezione")

    def test_model_prezzi(self):
        print("\n### MODEL PREZZI ###")

        # AGGIUNGI
        sp = Spettacolo(STR_NON_VUOTA, STR_NON_VUOTA, dict(([])), dict(([])))
        self.__model.aggiungi_spettacolo(sp)
        se = Sezione(STR_NON_VUOTA, STR_NON_VUOTA)
        self.__model.aggiungi_sezione(se)

        p = Prezzo(FLOAT_NONZERO, ID_NON_ESISTENTE, se.get_id())
        self.assertRaises(IdInesistenteException, self.__model.aggiungi_prezzo, p)
        print("Passato AGGIUNGI IdInesistente spettacolo")

        p = Prezzo(FLOAT_NONZERO, sp.get_id(), ID_NON_ESISTENTE)
        self.assertRaises(IdInesistenteException, self.__model.aggiungi_prezzo, p)
        print("Passato AGGIUNGI IdInesistente sezione")

        p = Prezzo(FLOAT_NONZERO, sp.get_id(), se.get_id())
        self.__model.aggiungi_prezzo(p)
        self.assertRaises(IdOccupatoException, self.__model.aggiungi_prezzo, p)
        print("Passato AGGIUNGI IdOccupato")

        p2 = Prezzo(FLOAT_NONZERO, sp.get_id(), se.get_id())
        self.assertRaises(OccupatoException, self.__model.aggiungi_prezzo, p2)
        print("Passato AGGIUNGI Occupato")

        # GET
        p_ = self.__model.get_prezzo(p.get_id())
        if p_ is None:
            raise Exception()
        self.assertEqual(p_, p)
        print("Passato GET")

        p_.set_ammontare(p_.get_ammontare() + FLOAT_NONZERO)
        p = self.__model.get_prezzo(p.get_id())
        if p is None:
            raise Exception()
        self.assertEqual(p.get_id_spettacolo(), p_.get_id_spettacolo())
        self.assertNotEqual(p.get_ammontare(), p_.get_ammontare())
        print("Passato GET side effect")

        # GET BY SPETTACOLO E SEZIONE
        sp2 = Spettacolo(STR_NON_VUOTA * 2, STR_NON_VUOTA, dict(([])), dict(([])))
        self.__model.aggiungi_spettacolo(sp2)
        se2 = Sezione(STR_NON_VUOTA * 2, STR_NON_VUOTA)
        self.__model.aggiungi_sezione(se2)
        p2 = Prezzo(FLOAT_NONZERO, sp2.get_id(), se.get_id())
        self.__model.aggiungi_prezzo(p2)
        p3 = Prezzo(FLOAT_NONZERO, sp.get_id(), se2.get_id())
        self.__model.aggiungi_prezzo(p3)
        p_ = self.__model.get_prezzo_by_spettacolo_e_sezione(
            p.get_id_spettacolo(), p.get_id_sezione()
        )
        if p_ is None:
            raise Exception()
        self.assertEqual(p_, p)
        print("Passato GET BY SPETTACOLO E SEZIONE")

        p_.set_ammontare(p_.get_ammontare() + FLOAT_NONZERO)
        p = self.__model.get_prezzo_by_spettacolo_e_sezione(
            p.get_id_spettacolo(), p.get_id_sezione()
        )
        if p is None:
            raise Exception()
        self.assertEqual(p.get_id_spettacolo(), p_.get_id_spettacolo())
        self.assertNotEqual(p.get_ammontare(), p_.get_ammontare())
        print("Passato GET BY SPETTACOLO E SEZIONE side effect")

        # GET LISTA BY SPETTACOLO
        self.assertEqual(self.__model.get_prezzi_by_spettacolo(sp.get_id()), [p, p3])
        print("Passato GET LISTA BY SPETTACOLO")

        p3_ = self.__model.get_prezzi_by_spettacolo(sp.get_id())[1]
        p3_.set_ammontare(p3_.get_ammontare() + FLOAT_NONZERO)
        p3 = self.__model.get_prezzi_by_spettacolo(sp.get_id())[1]
        self.assertEqual(p3.get_id_spettacolo(), p3_.get_id_spettacolo())
        self.assertNotEqual(p3.get_ammontare(), p3_.get_ammontare())
        print("Passato GET LISTA BY SPETTACOLO side effect")

        # MODIFICA
        p4 = Prezzo(FLOAT_NONZERO, sp2.get_id(), se2.get_id())
        self.assertRaises(IdInesistenteException, self.__model.modifica_prezzo, p4)
        print("Passato MODIFICA IdInesistente")

        p = self.__model.get_prezzo(p.get_id())
        if p is None:
            raise Exception()
        p.set_id_sezione(p3.get_id_sezione())
        self.assertRaises(OccupatoException, self.__model.modifica_prezzo, p)
        print("Passato MODIFICA Occupato")

        p.set_id_sezione(se.get_id())
        p.set_ammontare(p.get_ammontare() + FLOAT_NONZERO)
        self.__model.modifica_prezzo(p)
        p_ = self.__model.get_prezzo(p.get_id())
        if p_ is None:
            raise Exception()
        self.assertEqual(p_, p)
        print("Passato MODIFICA")

        # CARICA
        self.__model._Model__carica_prezzi()  # type: ignore
        self.assertEqual(
            self.__model._Model__gestore_prezzi._GestorePrezzi__lista_prezzi,  # type: ignore
            [p, p2, p3],
        )
        print("Passato CARICA")

        # ELIMINA
        self.assertRaises(
            IdInesistenteException, self.__model.elimina_prezzo, ID_NON_ESISTENTE
        )
        print("Passato ELIMINA IdInesistente")

        self.__model.elimina_prezzo(p.get_id())
        self.assertEqual(self.__model._Model__gestore_prezzi._GestorePrezzi__lista_prezzi, [p2, p3])  # type: ignore
        print("Passato ELIMINA")

        # ELIMINA BY SPETTACOLO
        p = Prezzo(FLOAT_NONZERO, sp.get_id(), se.get_id())
        self.__model.aggiungi_prezzo(p)
        p4 = Prezzo(FLOAT_NONZERO, sp2.get_id(), se2.get_id())
        self.__model.aggiungi_prezzo(p4)
        self.__model.elimina_spettacolo(sp.get_id())
        self.assertEqual(self.__model._Model__gestore_prezzi._GestorePrezzi__lista_prezzi, [p2, p4])  # type: ignore
        print("Passato ELIMINA BY SPETTACOLO")

        # ELIMINA BY SEZIONE
        self.__model.aggiungi_spettacolo(sp)
        p = Prezzo(FLOAT_NONZERO, sp.get_id(), se.get_id())
        self.__model.aggiungi_prezzo(p)
        p3 = Prezzo(FLOAT_NONZERO, sp.get_id(), se2.get_id())
        self.__model.aggiungi_prezzo(p3)
        self.__model.elimina_sezione(se.get_id())
        self.assertEqual(self.__model._Model__gestore_prezzi._GestorePrezzi__lista_prezzi, [p4, p3])  # type: ignore
        print("Passato ELIMINA BY SEZIONE")

    # ### PRENOTAZIONI ###
    def test_prenotazione(self):
        print("\n### PRENOTAZIONE ###")

        # CONGRUENZA nominativo
        self.assertRaises(DatoIncongruenteException, Prenotazione, " ", STR_NON_VUOTA)
        print("Passato CONGRUENZA nominativo")

        # CONGRUENZA segna_come_pagata
        p = Prenotazione(STR_NON_VUOTA, DATA_ORA_PASSATO)
        p.segna_come_pagata()
        self.assertRaises(AzioneIncongruenteException, p.segna_come_pagata)

        # CONGRUENZA segna_come_non_pagata
        p.segna_come_non_pagata()
        self.assertRaises(AzioneIncongruenteException, p.segna_come_non_pagata)

    def test_model_prenotazioni(self):
        print("\n### MODEL PRENOTAZIONI ###")

        # AGGIUNGI
        p = Prenotazione(STR_NON_VUOTA, DATA_ORA_PASSATO)
        self.__model.aggiungi_prenotazione(p)
        self.assertRaises(IdOccupatoException, self.__model.aggiungi_prenotazione, p)
        print("Passato AGGIUNGI IdOccupato")

        # GET
        p_ = self.__model.get_prenotazione(p.get_id())
        if p_ is None:
            raise Exception()
        self.assertEqual(p_, p)
        print("Passato GET")

        p_.set_nominativo(p_.get_nominativo() + STR_NON_VUOTA)
        p = self.__model.get_prenotazione(p.get_id())
        if p is None:
            raise Exception()
        self.assertEqual(
            p.get_data_ora_registrazione(), p_.get_data_ora_registrazione()
        )
        self.assertNotEqual(p.get_nominativo(), p_.get_nominativo())
        print("Passato GET side effect")

        # GET LISTA
        p2 = Prenotazione(STR_NON_VUOTA * 2, DATA_ORA_PASSATO)
        self.__model.aggiungi_prenotazione(p2)
        self.assertEqual(self.__model.get_prenotazioni(), [p, p2])
        print("Passato GET LISTA")

        p2_ = self.__model.get_prenotazioni()[1]
        p2_.set_nominativo(p2_.get_nominativo() + STR_NON_VUOTA)
        p2 = self.__model.get_prenotazioni()[1]
        self.assertEqual(
            p2.get_data_ora_registrazione(), p2_.get_data_ora_registrazione()
        )
        self.assertNotEqual(p2.get_nominativo(), p2_.get_nominativo())
        print("Passato GET LISTA side effect")

        # GET LISTA BY NOMINATIVO
        p3 = Prenotazione("other", DATA_ORA_PASSATO)
        self.__model.aggiungi_prenotazione(p3)
        self.assertEqual(
            self.__model.get_prenotazioni_by_nominativo(STR_NON_VUOTA), [p, p2]
        )
        print("Passato GET LISTA BY NOMINATIVO")
        self.__model.elimina_prenotazione(p3.get_id())

        p2_ = self.__model.get_prenotazioni_by_nominativo(STR_NON_VUOTA * 2)[0]
        p2_.set_nominativo(p2_.get_nominativo() + STR_NON_VUOTA)
        p2 = self.__model.get_prenotazioni_by_nominativo(STR_NON_VUOTA * 2)[0]
        self.assertEqual(
            p2.get_data_ora_registrazione(), p2_.get_data_ora_registrazione()
        )
        self.assertNotEqual(p2.get_nominativo(), p2_.get_nominativo())
        print("Passato GET LISTA BY NOMINATIVO side effect")

        # MODIFICA
        p3 = Prenotazione(STR_NON_VUOTA * 3, DATA_ORA_PASSATO)
        self.assertRaises(
            IdInesistenteException, self.__model.modifica_prenotazione, p3
        )
        print("Passato MODIFICA IdInesistente")

        p.set_nominativo(p.get_nominativo() + STR_NON_VUOTA * 3)
        self.__model.modifica_prenotazione(p)
        p_ = self.__model.get_prenotazione(p.get_id())
        if p_ is None:
            raise Exception()
        self.assertEqual(p_, p)
        print("Passato MODIFICA")

        # CARICA
        self.__model._Model__carica_prenotazioni()  # type: ignore
        self.assertEqual(self.__model.get_prenotazioni(), [p, p2])
        print("Passato CARICA")

        # ELIMINA
        self.assertRaises(
            IdInesistenteException, self.__model.elimina_prenotazione, ID_NON_ESISTENTE
        )
        print("Passato ELIMINA IdInesistente")

        sp = Spettacolo(STR_NON_VUOTA, STR_NON_VUOTA, dict(), dict())
        self.__model.aggiungi_spettacolo(sp)
        e = Evento(DATA_ORA_PASSATO, sp.get_id())
        self.__model.aggiungi_evento(e)
        se = Sezione(STR_NON_VUOTA, STR_NON_VUOTA)
        self.__model.aggiungi_sezione(se)
        po = Posto(STR_NON_VUOTA, 1, se.get_id())
        self.__model.aggiungi_posto(po)
        o = Occupazione(e.get_id(), po.get_id(), p.get_id())
        self.__model.aggiungi_occupazione(o)
        self.assertRaises(
            OggettoInUsoException, self.__model.elimina_prenotazione, p.get_id()
        )
        print("Passato ELIMINA OggettoInUso")
        self.__model.elimina_occupazione(o.get_id())

        self.__model.elimina_prenotazione(p.get_id())
        self.assertEqual(self.__model.get_prenotazioni(), [p2])
        print("Passato ELIMINA")

    # ### OCCUPAZIONI ###
    def test_occupazione(self):
        print("\n### OCCUPAZIONE ###")

        # CONGRUENZA id_evento
        self.assertRaises(
            DatoIncongruenteException,
            Occupazione,
            -1,
            0,
            0,
        )
        print("Passato CONGRUENZA id_evento")

        # CONGRUENZA id_posto
        self.assertRaises(
            DatoIncongruenteException,
            Occupazione,
            0,
            -1,
            0,
        )
        print("Passato CONGRUENZA id_posto")

        # CONGRUENZA id_prenotazione
        self.assertRaises(
            DatoIncongruenteException,
            Occupazione,
            0,
            0,
            -1,
        )
        print("Passato CONGRUENZA id_prenotazione")

    def test_model_occupazioni(self):
        print("\n### MODEL OCCUPAZIONI ###")

        # AGGIUNGI
        sp = Spettacolo(STR_NON_VUOTA, STR_NON_VUOTA, dict(([])), dict(([])))
        self.__model.aggiungi_spettacolo(sp)
        e = Evento(DATA_ORA_PASSATO, sp.get_id())
        self.__model.aggiungi_evento(e)
        se = Sezione(STR_NON_VUOTA, STR_NON_VUOTA)
        self.__model.aggiungi_sezione(se)
        po = Posto(STR_NON_VUOTA, 1, se.get_id())
        self.__model.aggiungi_posto(po)
        pr = Prenotazione(STR_NON_VUOTA, DATA_ORA_PASSATO)
        self.__model.aggiungi_prenotazione(pr)

        o = Occupazione(ID_NON_ESISTENTE, po.get_id(), pr.get_id())
        self.assertRaises(IdInesistenteException, self.__model.aggiungi_occupazione, o)
        print("Passato AGGIUNGI IdInesistente evento")

        o = Occupazione(e.get_id(), ID_NON_ESISTENTE, pr.get_id())
        self.assertRaises(IdInesistenteException, self.__model.aggiungi_occupazione, o)
        print("Passato AGGIUNGI IdInesistente posto")

        o = Occupazione(e.get_id(), po.get_id(), ID_NON_ESISTENTE)
        self.assertRaises(IdInesistenteException, self.__model.aggiungi_occupazione, o)
        print("Passato AGGIUNGI IdInesistente prenotazione")

        o = Occupazione(e.get_id(), po.get_id(), pr.get_id())
        self.__model.aggiungi_occupazione(o)
        self.assertRaises(IdOccupatoException, self.__model.aggiungi_occupazione, o)
        print("Passato AGGIUNGI IdOccupato")

        o2 = Occupazione(e.get_id(), po.get_id(), pr.get_id())
        self.assertRaises(OccupatoException, self.__model.aggiungi_occupazione, o2)
        print("Passato AGGIUNGI Occupato")

        # GET
        o_ = self.__model.get_occupazione(o.get_id())
        if o_ is None:
            raise Exception()
        self.assertEqual(o_, o)
        print("Passato GET")

        sp2 = Spettacolo(STR_NON_VUOTA, STR_NON_VUOTA, dict(([])), dict(([])))
        self.__model.aggiungi_spettacolo(sp2)
        e2 = Evento(DATA_ORA_PASSATO, sp2.get_id())
        self.__model.aggiungi_evento(e2)
        o_.set_id_evento(e2.get_id())
        o = self.__model.get_occupazione(o.get_id())
        if o is None:
            raise Exception()
        self.assertEqual(o.get_id_posto(), o_.get_id_posto())
        self.assertNotEqual(o.get_id_evento(), o_.get_id_evento())
        print("Passato GET side effect")

        # MODIFICA
        o3 = Occupazione(e2.get_id(), po.get_id(), pr.get_id())
        self.assertRaises(IdInesistenteException, self.__model.modifica_occupazione, o3)
        print("Passato MODIFICA IdInesistente")

        o2 = Occupazione(e2.get_id(), po.get_id(), pr.get_id())
        self.__model.aggiungi_occupazione(o2)
        o = self.__model.get_occupazione(o.get_id())
        if o is None:
            raise Exception()
        o.set_id_evento(o2.get_id_evento())
        self.assertRaises(OccupatoException, self.__model.modifica_occupazione, o)
        print("Passato MODIFICA Occupato")

        sp3 = Spettacolo(STR_NON_VUOTA, STR_NON_VUOTA, dict(([])), dict(([])))
        self.__model.aggiungi_spettacolo(sp3)
        e3 = Evento(DATA_ORA_PASSATO, sp3.get_id())
        self.__model.aggiungi_evento(e3)
        o.set_id_evento(e3.get_id())
        self.__model.modifica_occupazione(o)
        o_ = self.__model.get_occupazione(o.get_id())
        if o_ is None:
            raise Exception()
        self.assertEqual(o_, o)
        print("Passato MODIFICA")

        # CARICA
        self.__model._Model__carica_occupazioni()  # type: ignore
        self.assertEqual(
            self.__model._Model__gestore_occupazioni._GestoreOccupazioni__lista_occupazioni,  # type: ignore
            [o, o2],
        )
        print("Passato CARICA")

        # ELIMINA
        self.assertRaises(
            IdInesistenteException, self.__model.elimina_occupazione, ID_NON_ESISTENTE
        )
        print("Passato ELIMINA IdInesistente")

        self.__model.elimina_occupazione(o.get_id())
        self.assertEqual(self.__model._Model__gestore_occupazioni._GestoreOccupazioni__lista_occupazioni, [o2])  # type: ignore
        print("Passato ELIMINA")

    def tearDown(self) -> None:
        super().tearDown()

        shutil.rmtree("./test_db/")


if __name__ == "__main__":
    unittest.main()
