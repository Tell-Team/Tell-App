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
from model.model.model import Model


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
        evento = Evento(DATA_ORA_PASSATO, 0)
        self.assertFalse(evento.attivo())
        evento.set_data_ora(DATA_ORA_FUTURO)
        self.assertTrue(evento.attivo())
        print("Passato ATTIVO")

    def test_model_evento(self):
        print("\n### MODEL EVENTO ###")

        # AGGIUNGI
        evento = Evento(DATA_ORA_PASSATO, ID_NON_ESISTENTE)
        self.assertRaises(IdInesistenteException, self.__model.aggiungi_evento, evento)
        print("Passato AGGIUNGI IdInesistente")

        spettacolo = Spettacolo(STR_NON_VUOTA, STR_NON_VUOTA, dict(), dict())
        self.__model.aggiungi_spettacolo(spettacolo)
        evento = Evento(DATA_ORA_PASSATO, spettacolo.get_id())
        self.__model.aggiungi_evento(evento)
        self.assertRaises(IdOccupatoException, self.__model.aggiungi_evento, evento)
        print("Passato AGGIUNGI IdOccupato")

        evento2 = Evento(evento.get_data_ora(), spettacolo.get_id())
        self.assertRaises(OccupatoException, self.__model.aggiungi_evento, evento2)
        print("Passato AGGIUNGI Occupato")

        # GET
        evento_ = self.__model.get_evento(evento.get_id())
        assert evento_ is not None
        self.assertEqual(evento_, evento)
        print("Passato GET")

        evento_.set_data_ora(DATA_ORA_FUTURO)
        evento = self.__model.get_evento(evento.get_id())
        assert evento is not None
        self.assertEqual(evento.get_id_spettacolo(), evento_.get_id_spettacolo())
        self.assertNotEqual(evento.get_data_ora(), evento_.get_data_ora())
        print("Passato GET side effect")

        # GET LISTA
        evento2 = Evento(datetime.now(), spettacolo.get_id())
        self.__model.aggiungi_evento(evento2)
        self.assertEqual(self.__model.get_eventi(), [evento, evento2])
        print("Passato GET LISTA")

        evento2_ = self.__model.get_eventi()[1]
        evento2_.set_data_ora(DATA_ORA_FUTURO)
        evento2 = self.__model.get_eventi()[1]
        self.assertEqual(evento2.get_id_spettacolo(), evento2_.get_id_spettacolo())
        self.assertNotEqual(evento2.get_data_ora(), evento2_.get_data_ora())
        print("Passato GET LISTA side effect")

        # GET LISTA by spettacolo
        spettacolo2 = Spettacolo(STR_NON_VUOTA, STR_NON_VUOTA, dict(), dict())
        self.__model.aggiungi_spettacolo(spettacolo2)
        evento3 = Evento(DATA_ORA_PASSATO, spettacolo2.get_id())
        self.__model.aggiungi_evento(evento3)
        self.assertEqual(
            self.__model.get_eventi_by_spettacolo(spettacolo.get_id()),
            [evento, evento2],
        )
        print("Passato GET LISTA by spettacolo")

        evento2_ = self.__model.get_eventi_by_spettacolo(spettacolo.get_id())[1]
        evento2_.set_data_ora(DATA_ORA_FUTURO)
        evento2 = self.__model.get_eventi_by_spettacolo(spettacolo.get_id())[1]
        self.assertEqual(evento2.get_id_spettacolo(), evento2_.get_id_spettacolo())
        self.assertNotEqual(evento2.get_data_ora(), evento2_.get_data_ora())
        print("Passato GET LISTA by spettacolo side effect")
        self.__model.elimina_evento(evento3.get_id())
        self.__model.elimina_spettacolo(spettacolo2.get_id())

        # GET LISTA SPETTACOLI in programma
        genere = Genere(STR_NON_VUOTA, STR_NON_VUOTA)
        self.__model.aggiungi_genere(genere)
        opera = Opera(
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            1,
            DATA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            genere.get_id(),
        )
        self.__model.aggiungi_opera(opera)
        regia = Regia(
            STR_NON_VUOTA,
            0,
            opera.get_id(),
            STR_NON_VUOTA,
            dict(),
            dict(),
        )
        self.__model.aggiungi_spettacolo(regia)
        regia2 = Regia(
            STR_NON_VUOTA,
            0,
            opera.get_id(),
            STR_NON_VUOTA,
            dict(),
            dict(),
        )
        self.__model.aggiungi_spettacolo(regia2)
        regia3 = Regia(
            STR_NON_VUOTA,
            0,
            opera.get_id(),
            STR_NON_VUOTA,
            dict(),
            dict(),
        )
        self.__model.aggiungi_spettacolo(regia3)
        evento4 = Evento(DATA_ORA_PASSATO, regia2.get_id())
        self.__model.aggiungi_evento(evento4)
        evento5 = Evento(DATA_ORA_FUTURO, regia3.get_id())
        self.__model.aggiungi_evento(evento5)
        self.assertEqual(self.__model.get_spettacoli_in_programma(), [regia3])
        print("Passato GET LISTA SPETTACOLI in programma")

        regia3_ = self.__model.get_spettacoli_in_programma()[0]
        regia3_.set_titolo(regia3_.get_titolo() + STR_NON_VUOTA)
        regia3 = self.__model.get_spettacoli_in_programma()[0]
        self.assertEqual(regia3.get_note(), regia3_.get_note())
        self.assertNotEqual(regia3.get_titolo(), regia3_.get_titolo())
        print("Passato GET LISTA SPETTACOLI in programma side effect")
        self.__model.elimina_evento(evento5.get_id())
        self.__model.elimina_evento(evento4.get_id())
        self.__model.elimina_spettacolo(regia3.get_id())
        self.__model.elimina_spettacolo(regia2.get_id())
        self.__model.elimina_spettacolo(regia.get_id())
        self.__model.elimina_opera(opera.get_id())
        self.__model.elimina_genere(genere.get_id())

        # MODIFICA
        evento3 = Evento(DATA_ORA_PASSATO, ID_NON_ESISTENTE)
        self.assertRaises(IdInesistenteException, self.__model.modifica_evento, evento3)
        print("Passato MODIFICA IdInesistente")

        evento = self.__model.get_evento(evento.get_id())
        assert evento is not None
        evento.set_data_ora(evento2.get_data_ora())
        self.assertRaises(OccupatoException, self.__model.modifica_evento, evento)
        print("Passato MODIFICA Occupato")

        evento.set_data_ora(DATA_ORA_FUTURO)
        self.__model.modifica_evento(evento)
        evento_ = self.__model.get_evento(evento.get_id())
        assert evento_ is not None
        self.assertEqual(evento_, evento)
        print("Passato MODIFICA")

        # CARICA
        self.__model._Model__carica_eventi()  # type: ignore
        self.assertEqual(self.__model.get_eventi(), [evento, evento2])
        print("Passato CARICA")

        # ELIMINA
        self.assertRaises(
            IdInesistenteException, self.__model.elimina_evento, ID_NON_ESISTENTE
        )
        print("Passato ELIMINA IdInesistente")

        sezione = Sezione(STR_NON_VUOTA, STR_NON_VUOTA)
        self.__model.aggiungi_sezione(sezione)
        self.__model.aggiungi_prezzo(
            Prezzo(FLOAT_NONZERO, spettacolo.get_id(), sezione.get_id())
        )
        posto = Posto(STR_NON_VUOTA, 1, sezione.get_id())
        self.__model.aggiungi_posto(posto)
        prenotazione = Prenotazione(STR_NON_VUOTA, DATA_ORA_PASSATO)
        self.__model.aggiungi_prenotazione(prenotazione)
        occupazione = Occupazione(
            evento.get_id(), posto.get_id(), prenotazione.get_id()
        )
        self.__model.aggiungi_occupazione(occupazione)
        self.assertRaises(
            OggettoInUsoException, self.__model.elimina_evento, evento.get_id()
        )
        print("Passato ELIMINA OggettoInUso")

        self.__model.elimina_occupazione(occupazione.get_id())
        self.__model.elimina_evento(evento.get_id())
        self.assertEqual(self.__model.get_eventi(), [evento2])
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
        sezione = Sezione(STR_NON_VUOTA, STR_NON_VUOTA)
        self.__model.aggiungi_sezione(sezione)
        self.assertRaises(IdOccupatoException, self.__model.aggiungi_sezione, sezione)
        print("Passato AGGIUNGI IdOccupato")

        sezione2 = Sezione(sezione.get_nome(), STR_NON_VUOTA)
        self.assertRaises(OccupatoException, self.__model.aggiungi_sezione, sezione2)
        print("Passato AGGIUNGI Occupato")

        # GET
        sezione_ = self.__model.get_sezione(sezione.get_id())
        assert sezione_ is not None
        self.assertEqual(sezione_, sezione)
        print("Passato GET")

        sezione_.set_nome(sezione_.get_nome() + STR_NON_VUOTA)
        sezione = self.__model.get_sezione(sezione.get_id())
        assert sezione is not None
        self.assertEqual(sezione.get_descrizione(), sezione_.get_descrizione())
        self.assertNotEqual(sezione.get_nome(), sezione_.get_nome())
        print("Passato GET side effect")

        # GET LISTA
        sezione2 = Sezione(STR_NON_VUOTA * 2, STR_NON_VUOTA)
        self.__model.aggiungi_sezione(sezione2)
        self.assertEqual(self.__model.get_sezioni(), [sezione, sezione2])
        print("Passato GET LISTA")

        sezione2_ = self.__model.get_sezioni()[1]
        sezione2_.set_nome(sezione2_.get_nome() + STR_NON_VUOTA)
        sezione2 = self.__model.get_sezioni()[1]
        self.assertEqual(sezione2.get_descrizione(), sezione2_.get_descrizione())
        self.assertNotEqual(sezione2.get_nome(), sezione2_.get_nome())
        print("Passato GET LISTA side effect")

        # GET SEZIONI E FILE E POSTI DISPONIBILI
        spettacolo = Spettacolo(STR_NON_VUOTA, STR_NON_VUOTA, dict(), dict())
        self.__model.aggiungi_spettacolo(spettacolo)
        spettacolo2 = Spettacolo(STR_NON_VUOTA, STR_NON_VUOTA, dict(), dict())
        self.__model.aggiungi_spettacolo(spettacolo2)

        evento = Evento(DATA_ORA_PASSATO, spettacolo.get_id())
        self.__model.aggiungi_evento(evento)
        evento2 = Evento(DATA_ORA_PASSATO, spettacolo2.get_id())
        self.__model.aggiungi_evento(evento2)

        prenotazione = Prenotazione(STR_NON_VUOTA, DATA_ORA_PASSATO)
        self.__model.aggiungi_prenotazione(prenotazione)

        # sezione: sezione senza prezzi
        posto11 = Posto(STR_NON_VUOTA, 1, sezione.get_id())
        self.__model.aggiungi_posto(posto11)

        # sezione2: sezione con prezzo per un altro spettacolo
        self.__model.aggiungi_prezzo(
            Prezzo(FLOAT_NONZERO, spettacolo2.get_id(), sezione2.get_id())
        )

        posto21 = Posto(STR_NON_VUOTA, 1, sezione2.get_id())
        self.__model.aggiungi_posto(posto21)

        # sezione3: sezione disponibile
        sezione3 = Sezione(STR_NON_VUOTA * 3, STR_NON_VUOTA)
        self.__model.aggiungi_sezione(sezione3)
        self.__model.aggiungi_prezzo(
            Prezzo(FLOAT_NONZERO, spettacolo.get_id(), sezione3.get_id())
        )
        self.__model.aggiungi_prezzo(
            Prezzo(FLOAT_NONZERO, spettacolo2.get_id(), sezione3.get_id())
        )

        #   posto31: posto disponibile in fila STR_NON_VUOTA
        posto31 = Posto(STR_NON_VUOTA, 1, sezione3.get_id())
        self.__model.aggiungi_posto(posto31)
        #   p32: posto occupato per un altro evento in fila STR_NON_VUOTA*2
        posto32 = Posto(STR_NON_VUOTA * 2, 2, sezione3.get_id())
        self.__model.aggiungi_posto(posto32)
        occupazione32 = Occupazione(
            evento2.get_id(), posto32.get_id(), prenotazione.get_id()
        )
        self.__model.aggiungi_occupazione(occupazione32)
        #   p33: posto occupato per questo evento
        posto33 = Posto(STR_NON_VUOTA, 3, sezione3.get_id())
        self.__model.aggiungi_posto(posto33)
        occupazione33 = Occupazione(
            evento.get_id(), posto33.get_id(), prenotazione.get_id()
        )
        self.__model.aggiungi_occupazione(occupazione33)

        # sezione4: sezione vuota
        sezione4 = Sezione(STR_NON_VUOTA * 4, STR_NON_VUOTA)
        self.__model.aggiungi_sezione(sezione4)
        self.__model.aggiungi_prezzo(
            Prezzo(FLOAT_NONZERO, spettacolo.get_id(), sezione4.get_id())
        )

        # sezione5: sezione occupata
        sezione5 = Sezione(STR_NON_VUOTA * 5, STR_NON_VUOTA)
        self.__model.aggiungi_sezione(sezione5)
        self.__model.aggiungi_prezzo(
            Prezzo(FLOAT_NONZERO, spettacolo.get_id(), sezione5.get_id())
        )

        #   posto51: posto occupato per questo evento
        posto51 = Posto(STR_NON_VUOTA, 1, sezione5.get_id())
        self.__model.aggiungi_posto(posto51)
        occupazione51 = Occupazione(
            evento.get_id(), posto51.get_id(), prenotazione.get_id()
        )
        self.__model.aggiungi_occupazione(occupazione51)

        #   posto52: posto occupato per questo evento
        posto52 = Posto(STR_NON_VUOTA, 2, sezione5.get_id())
        self.__model.aggiungi_posto(posto52)
        occupazione52 = Occupazione(
            evento.get_id(), posto52.get_id(), prenotazione.get_id()
        )
        self.__model.aggiungi_occupazione(occupazione52)

        self.assertRaises(
            IdInesistenteException,
            self.__model.get_sezioni_e_file_e_posti_disponibili,
            ID_NON_ESISTENTE,
        )
        print("Passato GET SEZIONI E FILE E POSTI DISPONIBILI IdInesistente")

        self.assertEqual(
            self.__model.get_sezioni_e_file_e_posti_disponibili(evento.get_id()),
            [(sezione3, [(STR_NON_VUOTA, [posto31]), (STR_NON_VUOTA * 2, [posto32])])],
        )
        print("Passato GET SEZIONI E FILE E POSTI DISPONIBILI")

        sezione3_ = self.__model.get_sezioni_e_file_e_posti_disponibili(
            evento.get_id()
        )[0][0]
        sezione3_.set_nome(sezione3_.get_nome() + STR_NON_VUOTA)
        sezione3 = self.__model.get_sezioni_e_file_e_posti_disponibili(evento.get_id())[
            0
        ][0]
        self.assertEqual(sezione3.get_descrizione(), sezione3_.get_descrizione())
        self.assertNotEqual(sezione3.get_nome(), sezione3_.get_nome())
        print("Passato GET SEZIONI E FILE E POSTI DISPONIBILI side effect sezione")

        posto31_ = self.__model.get_sezioni_e_file_e_posti_disponibili(evento.get_id())[
            0
        ][1][0][1][0]
        posto31_.set_numero(posto31_.get_numero() + 1)
        p31 = self.__model.get_sezioni_e_file_e_posti_disponibili(evento.get_id())[0][
            1
        ][0][1][0]
        self.assertEqual(p31.get_id_sezione(), posto31_.get_id_sezione())
        self.assertNotEqual(p31.get_numero(), posto31_.get_numero())
        print("Passato GET SEZIONI E FILE E POSTI DISPONIBILI side effect posto")
        self.__model.elimina_occupazione(occupazione32.get_id())
        self.__model.elimina_occupazione(occupazione33.get_id())
        self.__model.elimina_occupazione(occupazione51.get_id())
        self.__model.elimina_occupazione(occupazione52.get_id())
        self.__model.elimina_posto(posto11.get_id())
        self.__model.elimina_posto(posto31.get_id())
        self.__model.elimina_posto(posto32.get_id())
        self.__model.elimina_posto(posto33.get_id())
        self.__model.elimina_posto(posto51.get_id())
        self.__model.elimina_posto(posto52.get_id())
        self.__model.elimina_sezione(sezione3.get_id())
        self.__model.elimina_sezione(sezione4.get_id())
        self.__model.elimina_sezione(sezione5.get_id())

        # MODIFICA
        sezione3 = Sezione(STR_NON_VUOTA * 3, STR_NON_VUOTA)
        self.assertRaises(
            IdInesistenteException, self.__model.modifica_sezione, sezione3
        )
        print("Passato MODIFICA IdInesistente")

        sezione = self.__model.get_sezione(sezione.get_id())
        assert sezione is not None
        sezione.set_nome(sezione2.get_nome())
        self.assertRaises(OccupatoException, self.__model.modifica_sezione, sezione)
        print("Passato MODIFICA Occupato")

        sezione.set_nome(sezione.get_nome() + STR_NON_VUOTA * 3)
        self.__model.modifica_sezione(sezione)
        sezione_ = self.__model.get_sezione(sezione.get_id())
        assert sezione_ is not None
        self.assertEqual(sezione_, sezione)
        print("Passato MODIFICA")

        # CARICA
        self.__model._Model__carica_sezioni()  # type: ignore
        self.assertEqual(self.__model.get_sezioni(), [sezione, sezione2])
        print("Passato CARICA")

        # ELIMINA
        self.assertRaises(
            IdInesistenteException, self.__model.elimina_sezione, ID_NON_ESISTENTE
        )
        print("Passato ELIMINA IdInesistente")

        posto = Posto(STR_NON_VUOTA, 1, sezione.get_id())
        self.__model.aggiungi_posto(posto)
        self.assertRaises(
            OggettoInUsoException, self.__model.elimina_sezione, sezione.get_id()
        )
        print("Passato ELIMINA OggettoInUso")
        self.__model.elimina_posto(posto.get_id())

        self.__model.elimina_sezione(sezione.get_id())
        self.assertEqual(self.__model.get_sezioni(), [sezione2])
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
        posto = Posto(STR_NON_VUOTA, 1, ID_NON_ESISTENTE)
        self.assertRaises(IdInesistenteException, self.__model.aggiungi_posto, posto)
        print("Passato AGGIUNGI IdInesistente")

        sezione = Sezione(STR_NON_VUOTA, STR_NON_VUOTA)
        self.__model.aggiungi_sezione(sezione)
        posto = Posto(STR_NON_VUOTA, 1, sezione.get_id())
        self.__model.aggiungi_posto(posto)
        posto.set_numero(posto.get_numero() + 1)
        self.assertRaises(IdOccupatoException, self.__model.aggiungi_posto, posto)
        print("Passato AGGIUNGI IdOccupato")
        posto.set_numero(posto.get_numero() - 1)

        posto2 = Posto(posto.get_fila(), posto.get_numero(), sezione.get_id())
        self.assertRaises(OccupatoException, self.__model.aggiungi_posto, posto2)
        print("Passato AGGIUNGI Occupato")

        # GET
        posto_ = self.__model.get_posto(posto.get_id())
        assert posto_ is not None
        self.assertEqual(posto_, posto)
        print("Passato GET")

        posto_.set_numero(posto_.get_numero() + 1)
        posto = self.__model.get_posto(posto.get_id())
        assert posto is not None
        self.assertEqual(posto.get_id_sezione(), posto_.get_id_sezione())
        self.assertNotEqual(posto.get_numero(), posto_.get_numero())
        print("Passato GET side effect")

        # GET LISTA
        posto2 = Posto(STR_NON_VUOTA * 2, 2, sezione.get_id())
        self.__model.aggiungi_posto(posto2)
        self.assertEqual(self.__model.get_posti(), [posto, posto2])
        print("Passato GET LISTA")

        posto2_ = self.__model.get_posti()[1]
        posto2_.set_numero(posto2_.get_numero() + 1)
        posto2 = self.__model.get_posti()[1]
        self.assertEqual(posto2.get_id_sezione(), posto2_.get_id_sezione())
        self.assertNotEqual(posto2.get_numero(), posto2_.get_numero())
        print("Passato GET LISTA side effect")

        # GET LISTA by sezione
        sezione2 = Sezione(STR_NON_VUOTA * 4, STR_NON_VUOTA)
        self.__model.aggiungi_sezione(sezione2)
        posto3 = Posto(STR_NON_VUOTA * 3, 3, sezione2.get_id())
        self.__model.aggiungi_posto(posto3)
        self.assertEqual(
            self.__model.get_posti_by_sezione(sezione.get_id()), [posto, posto2]
        )
        print("Passato GET LISTA by sezione")

        posto2_ = self.__model.get_posti_by_sezione(sezione.get_id())[1]
        posto2_.set_numero(posto2_.get_numero() + 1)
        posto2 = self.__model.get_posti_by_sezione(sezione.get_id())[1]
        self.assertEqual(posto2.get_id_sezione(), posto2_.get_id_sezione())
        self.assertNotEqual(posto2.get_numero(), posto2_.get_numero())
        print("Passato GET LISTA by sezione side effect")
        self.__model.elimina_posto(posto3.get_id())
        self.__model.elimina_sezione(sezione2.get_id())

        # MODIFICA
        posto4 = Posto(STR_NON_VUOTA * 4, 4, ID_NON_ESISTENTE)
        self.assertRaises(IdInesistenteException, self.__model.modifica_posto, posto4)
        print("Passato MODIFICA IdInesistente")

        posto = self.__model.get_posto(posto.get_id())
        assert posto is not None
        posto.set_fila(posto2.get_fila())
        posto.set_numero(posto2.get_numero())
        self.assertRaises(OccupatoException, self.__model.modifica_posto, posto)
        print("Passato MODIFICA Occupato")

        posto.set_numero(posto.get_numero() + 3)
        self.__model.modifica_posto(posto)
        posto_ = self.__model.get_posto(posto.get_id())
        assert posto_ is not None
        self.assertEqual(posto_, posto)
        print("Passato MODIFICA")

        # CARICA
        self.__model._Model__carica_posti()  # type: ignore
        self.assertEqual(self.__model.get_posti(), [posto, posto2])
        print("Passato CARICA")

        # ELIMINA
        self.assertRaises(
            IdInesistenteException, self.__model.elimina_posto, ID_NON_ESISTENTE
        )
        print("Passato ELIMINA IdInesistente")

        spettacolo = Spettacolo(STR_NON_VUOTA, STR_NON_VUOTA, dict(), dict())
        self.__model.aggiungi_spettacolo(spettacolo)
        self.__model.aggiungi_prezzo(
            Prezzo(FLOAT_NONZERO, spettacolo.get_id(), sezione.get_id())
        )
        evento = Evento(DATA_ORA_PASSATO, spettacolo.get_id())
        self.__model.aggiungi_evento(evento)
        prenotazione = Prenotazione(STR_NON_VUOTA, DATA_ORA_PASSATO)
        self.__model.aggiungi_prenotazione(prenotazione)
        occupazione = Occupazione(
            evento.get_id(), posto.get_id(), prenotazione.get_id()
        )
        self.__model.aggiungi_occupazione(occupazione)
        self.assertRaises(
            OggettoInUsoException, self.__model.elimina_posto, posto.get_id()
        )
        print("Passato ELIMINA OggettoInUso")

        self.__model.elimina_occupazione(occupazione.get_id())
        self.__model.elimina_posto(posto.get_id())
        self.assertEqual(self.__model.get_posti(), [posto2])
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
        spettacolo = Spettacolo(STR_NON_VUOTA, STR_NON_VUOTA, dict(), dict())
        self.__model.aggiungi_spettacolo(spettacolo)
        sezione = Sezione(STR_NON_VUOTA, STR_NON_VUOTA)
        self.__model.aggiungi_sezione(sezione)

        prezzo = Prezzo(FLOAT_NONZERO, ID_NON_ESISTENTE, sezione.get_id())
        self.assertRaises(IdInesistenteException, self.__model.aggiungi_prezzo, prezzo)
        print("Passato AGGIUNGI IdInesistente spettacolo")

        prezzo = Prezzo(FLOAT_NONZERO, spettacolo.get_id(), ID_NON_ESISTENTE)
        self.assertRaises(IdInesistenteException, self.__model.aggiungi_prezzo, prezzo)
        print("Passato AGGIUNGI IdInesistente sezione")

        prezzo = Prezzo(FLOAT_NONZERO, spettacolo.get_id(), sezione.get_id())
        self.__model.aggiungi_prezzo(prezzo)
        self.assertRaises(IdOccupatoException, self.__model.aggiungi_prezzo, prezzo)
        print("Passato AGGIUNGI IdOccupato")

        prezzo2 = Prezzo(FLOAT_NONZERO, spettacolo.get_id(), sezione.get_id())
        self.assertRaises(OccupatoException, self.__model.aggiungi_prezzo, prezzo2)
        print("Passato AGGIUNGI Occupato")

        # GET
        prezzo_ = self.__model.get_prezzo(prezzo.get_id())
        assert prezzo_ is not None
        self.assertEqual(prezzo_, prezzo)
        print("Passato GET")

        prezzo_.set_ammontare(prezzo_.get_ammontare() + FLOAT_NONZERO)
        prezzo = self.__model.get_prezzo(prezzo.get_id())
        assert prezzo is not None
        self.assertEqual(prezzo.get_id_spettacolo(), prezzo_.get_id_spettacolo())
        self.assertNotEqual(prezzo.get_ammontare(), prezzo_.get_ammontare())
        print("Passato GET side effect")

        # GET BY SPETTACOLO E SEZIONE
        spettacolo2 = Spettacolo(STR_NON_VUOTA * 2, STR_NON_VUOTA, dict(), dict())
        self.__model.aggiungi_spettacolo(spettacolo2)
        sezione2 = Sezione(STR_NON_VUOTA * 2, STR_NON_VUOTA)
        self.__model.aggiungi_sezione(sezione2)
        prezzo2 = Prezzo(FLOAT_NONZERO, spettacolo2.get_id(), sezione.get_id())
        self.__model.aggiungi_prezzo(prezzo2)
        prezzo3 = Prezzo(FLOAT_NONZERO, spettacolo.get_id(), sezione2.get_id())
        self.__model.aggiungi_prezzo(prezzo3)
        prezzo_ = self.__model.get_prezzo_by_spettacolo_e_sezione(
            prezzo.get_id_spettacolo(), prezzo.get_id_sezione()
        )
        assert prezzo_ is not None
        self.assertEqual(prezzo_, prezzo)
        print("Passato GET BY SPETTACOLO E SEZIONE")

        prezzo_.set_ammontare(prezzo_.get_ammontare() + FLOAT_NONZERO)
        prezzo = self.__model.get_prezzo_by_spettacolo_e_sezione(
            prezzo.get_id_spettacolo(), prezzo.get_id_sezione()
        )
        assert prezzo is not None
        self.assertEqual(prezzo.get_id_spettacolo(), prezzo_.get_id_spettacolo())
        self.assertNotEqual(prezzo.get_ammontare(), prezzo_.get_ammontare())
        print("Passato GET BY SPETTACOLO E SEZIONE side effect")

        # GET LISTA BY SPETTACOLO
        self.assertEqual(
            self.__model.get_prezzi_by_spettacolo(spettacolo.get_id()),
            [prezzo, prezzo3],
        )
        print("Passato GET LISTA BY SPETTACOLO")

        prezzo3_ = self.__model.get_prezzi_by_spettacolo(spettacolo.get_id())[1]
        prezzo3_.set_ammontare(prezzo3_.get_ammontare() + FLOAT_NONZERO)
        prezzo3 = self.__model.get_prezzi_by_spettacolo(spettacolo.get_id())[1]
        self.assertEqual(prezzo3.get_id_spettacolo(), prezzo3_.get_id_spettacolo())
        self.assertNotEqual(prezzo3.get_ammontare(), prezzo3_.get_ammontare())
        print("Passato GET LISTA BY SPETTACOLO side effect")

        # MODIFICA
        prezzo4 = Prezzo(FLOAT_NONZERO, spettacolo2.get_id(), sezione2.get_id())
        self.assertRaises(IdInesistenteException, self.__model.modifica_prezzo, prezzo4)
        print("Passato MODIFICA IdInesistente")

        prezzo = self.__model.get_prezzo(prezzo.get_id())
        assert prezzo is not None
        prezzo.set_id_sezione(prezzo3.get_id_sezione())
        self.assertRaises(OccupatoException, self.__model.modifica_prezzo, prezzo)
        print("Passato MODIFICA Occupato")

        prezzo.set_id_sezione(sezione.get_id())
        prezzo.set_ammontare(prezzo.get_ammontare() + FLOAT_NONZERO)
        self.__model.modifica_prezzo(prezzo)
        prezzo_ = self.__model.get_prezzo(prezzo.get_id())
        assert prezzo_ is not None
        self.assertEqual(prezzo_, prezzo)
        print("Passato MODIFICA")

        # CARICA
        self.__model._Model__carica_prezzi()  # type: ignore
        self.assertEqual(
            self.__model._Model__gestore_prezzi._GestorePrezzi__lista_prezzi,  # type: ignore
            [prezzo, prezzo2, prezzo3],
        )
        print("Passato CARICA")

        # ELIMINA
        self.assertRaises(
            IdInesistenteException, self.__model.elimina_prezzo, ID_NON_ESISTENTE
        )
        print("Passato ELIMINA IdInesistente")

        self.__model.elimina_prezzo(prezzo.get_id())
        self.assertEqual(self.__model._Model__gestore_prezzi._GestorePrezzi__lista_prezzi, [prezzo2, prezzo3])  # type: ignore
        print("Passato ELIMINA")

        # ELIMINA BY SPETTACOLO
        prezzo = Prezzo(FLOAT_NONZERO, spettacolo.get_id(), sezione.get_id())
        self.__model.aggiungi_prezzo(prezzo)
        prezzo4 = Prezzo(FLOAT_NONZERO, spettacolo2.get_id(), sezione2.get_id())
        self.__model.aggiungi_prezzo(prezzo4)
        self.__model.elimina_spettacolo(spettacolo.get_id())
        self.assertEqual(self.__model._Model__gestore_prezzi._GestorePrezzi__lista_prezzi, [prezzo2, prezzo4])  # type: ignore
        print("Passato ELIMINA BY SPETTACOLO")

        # ELIMINA BY SEZIONE
        self.__model.aggiungi_spettacolo(spettacolo)
        prezzo = Prezzo(FLOAT_NONZERO, spettacolo.get_id(), sezione.get_id())
        self.__model.aggiungi_prezzo(prezzo)
        prezzo3 = Prezzo(FLOAT_NONZERO, spettacolo.get_id(), sezione2.get_id())
        self.__model.aggiungi_prezzo(prezzo3)
        self.__model.elimina_sezione(sezione.get_id())
        self.assertEqual(self.__model._Model__gestore_prezzi._GestorePrezzi__lista_prezzi, [prezzo4, prezzo3])  # type: ignore
        print("Passato ELIMINA BY SEZIONE")

    # ### PRENOTAZIONI ###
    def test_prenotazione(self):
        print("\n### PRENOTAZIONE ###")

        # CONGRUENZA nominativo
        self.assertRaises(DatoIncongruenteException, Prenotazione, " ", STR_NON_VUOTA)
        print("Passato CONGRUENZA nominativo")

        # CONGRUENZA segna_come_pagata
        prenotazione = Prenotazione(STR_NON_VUOTA, DATA_ORA_PASSATO)
        prenotazione.segna_come_pagata()
        self.assertRaises(AzioneIncongruenteException, prenotazione.segna_come_pagata)

        # CONGRUENZA segna_come_non_pagata
        prenotazione.segna_come_non_pagata()
        self.assertRaises(
            AzioneIncongruenteException, prenotazione.segna_come_non_pagata
        )

    def test_model_prenotazioni(self):
        print("\n### MODEL PRENOTAZIONI ###")

        # AGGIUNGI
        prenotazione = Prenotazione(STR_NON_VUOTA, DATA_ORA_PASSATO)
        self.__model.aggiungi_prenotazione(prenotazione)
        self.assertRaises(
            IdOccupatoException, self.__model.aggiungi_prenotazione, prenotazione
        )
        print("Passato AGGIUNGI IdOccupato")

        # GET
        prenotazione_ = self.__model.get_prenotazione(prenotazione.get_id())
        assert prenotazione_ is not None
        self.assertEqual(prenotazione_, prenotazione)
        print("Passato GET")

        prenotazione_.set_nominativo(prenotazione_.get_nominativo() + STR_NON_VUOTA)
        prenotazione = self.__model.get_prenotazione(prenotazione.get_id())
        assert prenotazione is not None
        self.assertEqual(
            prenotazione.get_data_ora_registrazione(),
            prenotazione_.get_data_ora_registrazione(),
        )
        self.assertNotEqual(
            prenotazione.get_nominativo(), prenotazione_.get_nominativo()
        )
        print("Passato GET side effect")

        # GET LISTA
        prenotazione2 = Prenotazione(STR_NON_VUOTA * 2, DATA_ORA_PASSATO)
        self.__model.aggiungi_prenotazione(prenotazione2)
        self.assertEqual(self.__model.get_prenotazioni(), [prenotazione, prenotazione2])
        print("Passato GET LISTA")

        prenotazione2_ = self.__model.get_prenotazioni()[1]
        prenotazione2_.set_nominativo(prenotazione2_.get_nominativo() + STR_NON_VUOTA)
        prenotazione2 = self.__model.get_prenotazioni()[1]
        self.assertEqual(
            prenotazione2.get_data_ora_registrazione(),
            prenotazione2_.get_data_ora_registrazione(),
        )
        self.assertNotEqual(
            prenotazione2.get_nominativo(), prenotazione2_.get_nominativo()
        )
        print("Passato GET LISTA side effect")

        # GET LISTA BY NOMINATIVO
        prenotazione3 = Prenotazione("other", DATA_ORA_PASSATO)
        self.__model.aggiungi_prenotazione(prenotazione3)
        self.assertEqual(
            self.__model.get_prenotazioni_by_nominativo(STR_NON_VUOTA),
            [prenotazione, prenotazione2],
        )
        print("Passato GET LISTA BY NOMINATIVO")
        self.__model.elimina_prenotazione(prenotazione3.get_id())

        prenotazione2_ = self.__model.get_prenotazioni_by_nominativo(STR_NON_VUOTA * 2)[
            0
        ]
        prenotazione2_.set_nominativo(prenotazione2_.get_nominativo() + STR_NON_VUOTA)
        prenotazione2 = self.__model.get_prenotazioni_by_nominativo(STR_NON_VUOTA * 2)[
            0
        ]
        self.assertEqual(
            prenotazione2.get_data_ora_registrazione(),
            prenotazione2_.get_data_ora_registrazione(),
        )
        self.assertNotEqual(
            prenotazione2.get_nominativo(), prenotazione2_.get_nominativo()
        )
        print("Passato GET LISTA BY NOMINATIVO side effect")

        # AMMONTARE TOTALE PRENOTAZIONE
        sezione1 = Sezione(STR_NON_VUOTA, STR_NON_VUOTA)
        self.__model.aggiungi_sezione(sezione1)
        posto1 = Posto(STR_NON_VUOTA, 1, sezione1.get_id())
        self.__model.aggiungi_posto(posto1)
        spettacolo1 = Spettacolo(STR_NON_VUOTA, STR_NON_VUOTA, dict(), dict())
        self.__model.aggiungi_spettacolo(spettacolo1)
        prezzo1 = Prezzo(FLOAT_NONZERO, spettacolo1.get_id(), sezione1.get_id())
        self.__model.aggiungi_prezzo(prezzo1)
        evento1 = Evento(DATA_ORA_FUTURO, spettacolo1.get_id())
        self.__model.aggiungi_evento(evento1)
        occupazione1 = Occupazione(
            evento1.get_id(), posto1.get_id(), prenotazione.get_id()
        )
        self.__model.aggiungi_occupazione(occupazione1)

        sezione2 = Sezione(STR_NON_VUOTA * 2, STR_NON_VUOTA)
        self.__model.aggiungi_sezione(sezione2)
        posto2 = Posto(STR_NON_VUOTA, 2, sezione2.get_id())
        self.__model.aggiungi_posto(posto2)
        prezzo2 = Prezzo(FLOAT_NONZERO, spettacolo1.get_id(), sezione2.get_id())
        self.__model.aggiungi_prezzo(prezzo2)
        occupazione2 = Occupazione(
            evento1.get_id(), posto2.get_id(), prenotazione.get_id()
        )
        self.__model.aggiungi_occupazione(occupazione2)

        self.assertEqual(
            self.__model.ammontare_totale_prenotazione(prenotazione.get_id()),
            FLOAT_NONZERO + FLOAT_NONZERO,
        )
        print("Passato AMMONTARE TOTALE PRENOTAZIONE")

        # CARICA
        self.__model._Model__carica_prenotazioni()  # type: ignore
        self.assertEqual(self.__model.get_prenotazioni(), [prenotazione, prenotazione2])
        print("Passato CARICA")

        # ELIMINA
        self.assertRaises(
            IdInesistenteException, self.__model.elimina_prenotazione, ID_NON_ESISTENTE
        )
        print("Passato ELIMINA IdInesistente")

        self.__model.elimina_prenotazione(prenotazione.get_id())
        self.assertEqual(self.__model.get_prenotazioni(), [prenotazione2])
        print("Passato ELIMINA")

        # SEGNA COME PAGATA
        self.assertRaises(
            IdInesistenteException,
            self.__model.segna_prenotazione_come_pagata,
            ID_NON_ESISTENTE,
        )
        print("Passato SEGNA COME PAGATA IdInesistente")

        self.__model.segna_prenotazione_come_pagata(prenotazione2.get_id())
        print("Passato SEGNA COME PAGATA")

        self.assertRaises(
            AzioneIncongruenteException,
            self.__model.segna_prenotazione_come_pagata,
            prenotazione2.get_id(),
        )
        print("Passato SEGNA COME PAGATA AzioneIncongruente")

        # SEGNA COME NON PAGATA
        self.assertRaises(
            IdInesistenteException,
            self.__model.segna_prenotazione_come_non_pagata,
            ID_NON_ESISTENTE,
        )
        print("Passato SEGNA COME NON PAGATA IdInesistente")

        self.__model.segna_prenotazione_come_non_pagata(prenotazione2.get_id())
        print("Passato SEGNA COME NON PAGATA")

        self.assertRaises(
            AzioneIncongruenteException,
            self.__model.segna_prenotazione_come_non_pagata,
            prenotazione2.get_id(),
        )
        print("Passato SEGNA COME NON PAGATA AzioneIncongruente")

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
        spettacolo = Spettacolo(STR_NON_VUOTA, STR_NON_VUOTA, dict(), dict())
        self.__model.aggiungi_spettacolo(spettacolo)
        evento = Evento(DATA_ORA_PASSATO, spettacolo.get_id())
        self.__model.aggiungi_evento(evento)
        sezione = Sezione(STR_NON_VUOTA, STR_NON_VUOTA)
        self.__model.aggiungi_sezione(sezione)
        self.__model.aggiungi_prezzo(
            Prezzo(FLOAT_NONZERO, spettacolo.get_id(), sezione.get_id())
        )
        posto = Posto(STR_NON_VUOTA, 1, sezione.get_id())
        self.__model.aggiungi_posto(posto)
        prenotazione = Prenotazione(STR_NON_VUOTA, DATA_ORA_PASSATO)
        self.__model.aggiungi_prenotazione(prenotazione)

        occupazione = Occupazione(
            ID_NON_ESISTENTE, posto.get_id(), prenotazione.get_id()
        )
        self.assertRaises(
            IdInesistenteException, self.__model.aggiungi_occupazione, occupazione
        )
        print("Passato AGGIUNGI IdInesistente evento")

        occupazione = Occupazione(
            evento.get_id(), ID_NON_ESISTENTE, prenotazione.get_id()
        )
        self.assertRaises(
            IdInesistenteException, self.__model.aggiungi_occupazione, occupazione
        )
        print("Passato AGGIUNGI IdInesistente posto")

        occupazione = Occupazione(evento.get_id(), posto.get_id(), ID_NON_ESISTENTE)
        self.assertRaises(
            IdInesistenteException, self.__model.aggiungi_occupazione, occupazione
        )
        print("Passato AGGIUNGI IdInesistente prenotazione")

        spettacolo2 = Spettacolo(STR_NON_VUOTA, STR_NON_VUOTA, dict(), dict())
        self.__model.aggiungi_spettacolo(spettacolo2)
        evento2 = Evento(DATA_ORA_PASSATO, spettacolo2.get_id())
        self.__model.aggiungi_evento(evento2)
        occupazione = Occupazione(
            evento2.get_id(), posto.get_id(), prenotazione.get_id()
        )
        self.assertRaises(
            AzioneIncongruenteException, self.__model.aggiungi_occupazione, occupazione
        )
        print("Passato AGGIUNGI AzioneIncogruente")
        self.__model.elimina_evento(evento2.get_id())
        self.__model.elimina_spettacolo(spettacolo2.get_id())

        occupazione = Occupazione(
            evento.get_id(), posto.get_id(), prenotazione.get_id()
        )
        self.__model.aggiungi_occupazione(occupazione)
        self.assertRaises(
            IdOccupatoException, self.__model.aggiungi_occupazione, occupazione
        )
        print("Passato AGGIUNGI IdOccupato")

        occupazione2 = Occupazione(
            evento.get_id(), posto.get_id(), prenotazione.get_id()
        )
        self.assertRaises(
            OccupatoException, self.__model.aggiungi_occupazione, occupazione2
        )
        print("Passato AGGIUNGI Occupato")

        # GET
        occupazione_ = self.__model.get_occupazione(occupazione.get_id())
        assert occupazione_ is not None
        self.assertEqual(occupazione_, occupazione)
        print("Passato GET")

        spettacolo2 = Spettacolo(STR_NON_VUOTA, STR_NON_VUOTA, dict(), dict())
        self.__model.aggiungi_spettacolo(spettacolo2)
        evento2 = Evento(DATA_ORA_PASSATO, spettacolo2.get_id())
        self.__model.aggiungi_evento(evento2)
        self.__model.aggiungi_prezzo(
            Prezzo(FLOAT_NONZERO, spettacolo2.get_id(), sezione.get_id())
        )
        occupazione_.set_id_evento(evento2.get_id())
        occupazione = self.__model.get_occupazione(occupazione.get_id())
        assert occupazione is not None
        self.assertEqual(occupazione.get_id_posto(), occupazione_.get_id_posto())
        self.assertNotEqual(occupazione.get_id_evento(), occupazione_.get_id_evento())
        print("Passato GET side effect")

        # GET LISTA BY PRENOTAZIONE
        occupazione2 = Occupazione(
            evento2.get_id(), posto.get_id(), prenotazione.get_id()
        )
        self.__model.aggiungi_occupazione(occupazione2)
        posto2 = Posto(STR_NON_VUOTA * 2, 1, sezione.get_id())
        self.__model.aggiungi_posto(posto2)
        prenotazione2 = Prenotazione(STR_NON_VUOTA, DATA_ORA_PASSATO)
        self.__model.aggiungi_prenotazione(prenotazione2)
        occupazione3 = Occupazione(
            evento2.get_id(), posto2.get_id(), prenotazione2.get_id()
        )
        self.__model.aggiungi_occupazione(occupazione3)
        self.assertEqual(
            self.__model.get_occupazioni_by_prenotazione(prenotazione.get_id()),
            [occupazione, occupazione2],
        )
        print("Passato GET LISTA BY PRENOTAZIONE")

        occupazione2_ = self.__model.get_occupazioni_by_prenotazione(
            prenotazione.get_id()
        )[1]
        occupazione2_.set_id_prenotazione(occupazione3.get_id_prenotazione())
        occupazione2 = self.__model.get_occupazioni_by_prenotazione(
            prenotazione.get_id()
        )[1]
        self.assertEqual(occupazione2.get_id_evento(), occupazione2_.get_id_evento())
        self.assertNotEqual(
            occupazione2.get_id_prenotazione(), occupazione2_.get_id_prenotazione()
        )
        print("Passato GET LISTA BY PRENOTAZIONE side effect")
        self.__model.elimina_occupazione(occupazione2.get_id())
        self.__model.elimina_occupazione(occupazione3.get_id())
        self.__model.elimina_posto(posto2.get_id())
        self.__model.elimina_prenotazione(prenotazione2.get_id())

        # MODIFICA
        occupazione3 = Occupazione(
            evento2.get_id(), posto.get_id(), prenotazione.get_id()
        )
        self.assertRaises(
            IdInesistenteException, self.__model.modifica_occupazione, occupazione3
        )
        print("Passato MODIFICA IdInesistente")

        occupazione2 = Occupazione(
            evento2.get_id(), posto.get_id(), prenotazione.get_id()
        )
        self.__model.aggiungi_occupazione(occupazione2)
        occupazione = self.__model.get_occupazione(occupazione.get_id())
        assert occupazione is not None
        occupazione.set_id_evento(occupazione2.get_id_evento())
        self.assertRaises(
            OccupatoException, self.__model.modifica_occupazione, occupazione
        )
        print("Passato MODIFICA Occupato")

        spettacolo3 = Spettacolo(STR_NON_VUOTA, STR_NON_VUOTA, dict(), dict())
        self.__model.aggiungi_spettacolo(spettacolo3)
        self.__model.aggiungi_prezzo(
            Prezzo(FLOAT_NONZERO, spettacolo3.get_id(), sezione.get_id())
        )
        evento3 = Evento(DATA_ORA_PASSATO, spettacolo3.get_id())
        self.__model.aggiungi_evento(evento3)
        occupazione.set_id_evento(evento3.get_id())
        self.__model.modifica_occupazione(occupazione)
        occupazione_ = self.__model.get_occupazione(occupazione.get_id())
        assert occupazione_ is not None
        self.assertEqual(occupazione_, occupazione)
        print("Passato MODIFICA")

        # CARICA
        self.__model._Model__carica_occupazioni()  # type: ignore
        self.assertEqual(
            self.__model._Model__gestore_occupazioni._GestoreOccupazioni__lista_occupazioni,  # type: ignore
            [occupazione, occupazione2],
        )
        print("Passato CARICA")

        # ELIMINA
        self.assertRaises(
            IdInesistenteException, self.__model.elimina_occupazione, ID_NON_ESISTENTE
        )
        print("Passato ELIMINA IdInesistente")

        self.__model.elimina_occupazione(occupazione.get_id())
        self.assertEqual(self.__model._Model__gestore_occupazioni._GestoreOccupazioni__lista_occupazioni, [occupazione2])  # type: ignore
        print("Passato ELIMINA")

        # ELIMINA BY PRENOTAZIONE
        prenotazione2 = Prenotazione(STR_NON_VUOTA, DATA_ORA_PASSATO)
        self.__model.aggiungi_prenotazione(prenotazione2)
        occupazione3 = Occupazione(
            evento.get_id(), posto.get_id(), prenotazione2.get_id()
        )
        self.__model.aggiungi_occupazione(occupazione3)
        occupazione4 = Occupazione(
            evento3.get_id(), posto.get_id(), prenotazione2.get_id()
        )
        self.__model.aggiungi_occupazione(occupazione4)
        self.__model.elimina_prenotazione(prenotazione2.get_id())
        self.assertEqual(self.__model._Model__gestore_occupazioni._GestoreOccupazioni__lista_occupazioni, [occupazione2])  # type: ignore
        print("Passato ELIMINA BY PRENOTAZIONE")

    def tearDown(self) -> None:
        super().tearDown()

        shutil.rmtree("./test_db/")


if __name__ == "__main__":
    unittest.main()
