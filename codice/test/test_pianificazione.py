from datetime import date, datetime
import shutil
import unittest

from model.pianificazione.spettacolo import Spettacolo
from model.exceptions import (
    DatoIncongruenteException,
    IdInesistenteException,
    IdOccupatoException,
    OccupatoException,
    OggettoInUsoException,
)
from model.organizzazione.evento import Evento
from model.pianificazione.genere import Genere
from model.pianificazione.opera import Opera
from model.pianificazione.regia import Regia
from model.model.model import Model


STR_NON_VUOTA = "BCNRFF"
DATA_ORA_PASSATO = datetime(1904, 6, 16, 8)
ID_NON_ESISTENTE = 777
DATA = date(2009, 4, 13)


class TestTell(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.__model = Model("./test_db/")

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
        genere = Genere(STR_NON_VUOTA, STR_NON_VUOTA)
        self.__model.aggiungi_genere(genere)
        self.assertRaises(IdOccupatoException, self.__model.aggiungi_genere, genere)
        print("Passato AGGIUNGI IdOccupato")

        genere2 = Genere(genere.get_nome(), STR_NON_VUOTA)
        self.assertRaises(OccupatoException, self.__model.aggiungi_genere, genere2)
        print("Passato AGGIUNGI Occupato")

        # GET
        genere_ = self.__model.get_genere(genere.get_id())
        assert genere_ is not None
        self.assertEqual(genere_, genere)
        print("Passato GET")

        genere_.set_nome(genere_.get_nome() + STR_NON_VUOTA)
        genere = self.__model.get_genere(genere.get_id())
        assert genere is not None
        self.assertEqual(genere.get_descrizione(), genere_.get_descrizione())
        self.assertNotEqual(genere.get_nome(), genere_.get_nome())
        print("Passato GET side effect")

        # GET LISTA
        genere2 = Genere(STR_NON_VUOTA * 2, STR_NON_VUOTA)
        self.__model.aggiungi_genere(genere2)
        self.assertEqual(self.__model.get_generi(), [genere, genere2])
        print("Passato GET LISTA")

        genere2_ = self.__model.get_generi()[1]
        genere2_.set_nome(genere2_.get_nome() + STR_NON_VUOTA)
        genere2 = self.__model.get_generi()[1]
        self.assertEqual(genere2.get_descrizione(), genere2_.get_descrizione())
        self.assertNotEqual(genere2.get_nome(), genere2_.get_nome())
        print("Passato GET LISTA side effect")

        # MODIFICA
        genere3 = Genere(STR_NON_VUOTA * 3, STR_NON_VUOTA)
        self.assertRaises(IdInesistenteException, self.__model.modifica_genere, genere3)
        print("Passato MODIFICA IdInesistente")

        genere = self.__model.get_genere(genere.get_id())
        assert genere is not None
        genere.set_nome(genere2.get_nome())
        self.assertRaises(OccupatoException, self.__model.modifica_genere, genere)
        print("Passato MODIFICA Occupato")

        genere.set_nome(genere.get_nome() + STR_NON_VUOTA * 3)
        self.__model.modifica_genere(genere)
        genere_ = self.__model.get_genere(genere.get_id())
        assert genere_ is not None
        self.assertEqual(genere_, genere)
        print("Passato MODIFICA")

        # CARICA
        self.__model._Model__carica_generi()  # type: ignore
        self.assertEqual(self.__model.get_generi(), [genere, genere2])
        print("Passato CARICA")

        # ELIMINA
        self.assertRaises(
            IdInesistenteException, self.__model.elimina_genere, ID_NON_ESISTENTE
        )
        print("Passato ELIMINA IdInesistente")

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
        self.assertRaises(
            OggettoInUsoException, self.__model.elimina_genere, genere.get_id()
        )
        print("Passato ELIMINA OggettoInUso")
        self.__model.elimina_opera(opera.get_id())

        self.__model.elimina_genere(genere.get_id())
        self.assertEqual(self.__model.get_generi(), [genere2])
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
        opera = Opera(
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            1,
            DATA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            ID_NON_ESISTENTE,
        )
        self.assertRaises(IdInesistenteException, self.__model.aggiungi_opera, opera)
        print("Passato AGGIUNGI IdInesistente")

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
        self.assertRaises(IdOccupatoException, self.__model.aggiungi_opera, opera)
        print("Passato AGGIUNGI IdOccupato")

        opera2 = Opera(
            opera.get_nome(),
            opera.get_compositore(),
            STR_NON_VUOTA,
            1,
            DATA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            genere.get_id(),
        )
        self.assertRaises(OccupatoException, self.__model.aggiungi_opera, opera2)
        print("Passato AGGIUNGI Occupato")

        # GET
        opera_ = self.__model.get_opera(opera.get_id())
        assert opera_ is not None
        self.assertEqual(opera_, opera)
        print("Passato GET")

        opera_.set_nome(opera_.get_nome() + STR_NON_VUOTA)
        opera = self.__model.get_opera(opera.get_id())
        assert opera is not None
        self.assertEqual(opera.get_compositore(), opera_.get_compositore())
        self.assertNotEqual(opera.get_nome(), opera_.get_nome())
        print("Passato GET side effect")

        # GET LISTA
        opera2 = Opera(
            STR_NON_VUOTA * 2,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            1,
            DATA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            genere.get_id(),
        )
        self.__model.aggiungi_opera(opera2)
        self.assertEqual(self.__model.get_opere(), [opera, opera2])
        print("Passato GET LISTA")

        opera2_ = self.__model.get_opere()[1]
        opera2_.set_nome(opera2_.get_nome() + STR_NON_VUOTA)
        opera2 = self.__model.get_opere()[1]
        self.assertEqual(opera2.get_compositore(), opera2_.get_compositore())
        self.assertNotEqual(opera2.get_nome(), opera2_.get_nome())
        print("Passato GET LISTA side effect")

        # GET LISTA by nome
        opera3 = Opera(
            STR_NON_VUOTA * 3,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            1,
            DATA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            genere.get_id(),
        )
        self.__model.aggiungi_opera(opera3)
        opera4 = Opera(
            "other",
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            1,
            DATA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            genere.get_id(),
        )
        self.__model.aggiungi_opera(opera4)
        self.assertEqual(
            self.__model.get_opere_by_nome(STR_NON_VUOTA), [opera, opera2, opera3]
        )
        print("Passato GET LISTA by nome")

        opera2_ = self.__model.get_opere_by_nome(STR_NON_VUOTA)[1]
        opera2_.set_nome(opera2_.get_nome() + STR_NON_VUOTA)
        opera2 = self.__model.get_opere_by_nome(STR_NON_VUOTA)[1]
        self.assertEqual(opera2.get_compositore(), opera2_.get_compositore())
        self.assertNotEqual(opera2.get_nome(), opera2_.get_nome())
        print("Passato GET LISTA by nome side effect")
        self.__model.elimina_opera(opera3.get_id())
        self.__model.elimina_opera(opera4.get_id())

        # MODIFICA
        opera3 = Opera(
            STR_NON_VUOTA * 3,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            1,
            DATA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            genere.get_id(),
        )
        self.assertRaises(IdInesistenteException, self.__model.modifica_opera, opera3)
        print("Passato MODIFICA IdInesistente")

        opera = self.__model.get_opera(opera.get_id())
        assert opera is not None
        opera.set_nome(opera2.get_nome())
        self.assertRaises(OccupatoException, self.__model.modifica_opera, opera)
        print("Passato MODIFICA Occupato")

        opera.set_nome(opera.get_nome() + STR_NON_VUOTA * 3)
        self.__model.modifica_opera(opera)
        opera_ = self.__model.get_opera(opera.get_id())
        assert opera_ is not None
        self.assertEqual(opera_, opera)
        print("Passato MODIFICA")

        # CARICA
        self.__model._Model__carica_opere()  # type: ignore
        self.assertEqual(self.__model.get_opere(), [opera, opera2])
        print("Passato CARICA")

        # ELIMINA
        self.assertRaises(
            IdInesistenteException, self.__model.elimina_opera, ID_NON_ESISTENTE
        )
        print("Passato ELIMINA IdInesistente")

        regia = Regia(STR_NON_VUOTA, 0, opera.get_id(), STR_NON_VUOTA, dict(), dict())
        self.__model.aggiungi_spettacolo(regia)
        self.assertRaises(
            OggettoInUsoException, self.__model.elimina_opera, opera.get_id()
        )
        print("Passato ELIMINA OggettoInUso")
        self.__model.elimina_spettacolo(regia.get_id())

        self.__model.elimina_opera(opera.get_id())
        self.assertEqual(self.__model.get_opere(), [opera2])
        print("Passato ELIMINA")

    # ### SPETTACOLI E REGIE ###
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
            dict(),
            dict(),
        )
        print("Passato CONGRUENZA id_opera")

        # CONGRUENZA interpreti
        self.assertRaises(
            DatoIncongruenteException,
            Regia,
            STR_NON_VUOTA,
            0,
            0,
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
            dict([(STR_NON_VUOTA, " ")]),
            dict(),
        )
        print("Passato CONGRUENZA interpreti")

        # CONGRUENZA musicisti_e_direttori_artistici
        self.assertRaises(
            DatoIncongruenteException,
            Regia,
            STR_NON_VUOTA,
            0,
            0,
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
            dict(),
            dict([(STR_NON_VUOTA, " ")]),
        )
        print("Passato CONGRUENZA musicisti_e_direttori_artistici")

    def test_model_spettacoli_e_regie(self):
        print("\n### MODEL SPETTEACOLI E REGIE ###")

        # AGGIUNGI
        regia = Regia(
            STR_NON_VUOTA,
            0,
            ID_NON_ESISTENTE,
            STR_NON_VUOTA,
            dict(),
            dict(),
        )
        self.assertRaises(
            IdInesistenteException, self.__model.aggiungi_spettacolo, regia
        )
        print("Passato AGGIUNGI IdInesistente")

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
        self.assertRaises(IdOccupatoException, self.__model.aggiungi_spettacolo, regia)
        print("Passato AGGIUNGI IdOccupato")

        # GET
        regia_: Regia | None = self.__model.get_spettacolo(regia.get_id())  # type: ignore
        assert regia_ is not None
        self.assertEqual(regia_, regia)
        print("Passato GET")

        regia_.set_titolo(regia_.get_titolo() + STR_NON_VUOTA)
        regia: Regia | None = self.__model.get_spettacolo(regia.get_id())  # type: ignore
        assert regia is not None
        self.assertEqual(regia.get_note(), regia_.get_note())
        self.assertNotEqual(regia.get_titolo(), regia_.get_titolo())
        print("Passato GET side effect")

        # GET LISTA
        regia2 = Regia(
            STR_NON_VUOTA,
            0,
            opera.get_id(),
            STR_NON_VUOTA,
            dict(),
            dict(),
        )
        self.__model.aggiungi_spettacolo(regia2)
        self.assertEqual(self.__model.get_spettacoli(), [regia, regia2])
        print("Passato GET LISTA")

        regia2_ = self.__model.get_spettacoli()[1]
        regia2_.set_titolo(regia2_.get_titolo() + STR_NON_VUOTA)
        regia2 = self.__model.get_spettacoli()[1]
        self.assertEqual(regia2.get_note(), regia2_.get_note())
        self.assertNotEqual(regia2.get_titolo(), regia2_.get_titolo())
        print("Passato GET LISTA side effect")

        # GET LISTA by titolo
        spettacolo = Spettacolo("other", "", dict(), dict())
        self.__model.aggiungi_spettacolo(spettacolo)
        spettacolo2 = Spettacolo("other", "", dict(), dict())
        self.__model.aggiungi_spettacolo(spettacolo2)
        self.assertEqual(
            self.__model.get_spettacoli_by_titolo("other"), [spettacolo, spettacolo2]
        )
        print("Passato GET LISTA by titolo")

        spettacolo2_ = self.__model.get_spettacoli_by_titolo("other")[1]
        spettacolo2_.set_titolo(spettacolo2_.get_titolo() + STR_NON_VUOTA)
        spettacolo2 = self.__model.get_spettacoli_by_titolo("other")[1]
        self.assertEqual(spettacolo2.get_note(), spettacolo2_.get_note())
        self.assertNotEqual(spettacolo2.get_titolo(), spettacolo2_.get_titolo())
        print("Passato GET LISTA by titolo side effect")
        self.__model.elimina_spettacolo(spettacolo.get_id())
        self.__model.elimina_spettacolo(spettacolo2.get_id())

        # GET LISTA by opera
        opera2 = Opera(
            STR_NON_VUOTA * 2,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            1,
            DATA,
            STR_NON_VUOTA,
            STR_NON_VUOTA,
            genere.get_id(),
        )
        self.__model.aggiungi_opera(opera2)
        regia3 = Regia(
            STR_NON_VUOTA,
            0,
            opera2.get_id(),
            STR_NON_VUOTA,
            dict(),
            dict(),
        )
        self.__model.aggiungi_spettacolo(regia3)
        self.assertEqual(
            self.__model.get_regie_by_opera(opera.get_id()), [regia, regia2]
        )
        print("Passato GET LISTA by opera")

        regia2_ = self.__model.get_regie_by_opera(opera.get_id())[1]
        regia2_.set_titolo(regia2_.get_titolo() + STR_NON_VUOTA)
        regia2 = self.__model.get_regie_by_opera(opera.get_id())[1]
        self.assertEqual(regia2.get_note(), regia2_.get_note())
        self.assertNotEqual(regia2.get_titolo(), regia2_.get_titolo())
        print("Passato GET LISTA by opera side effect")
        self.__model.elimina_spettacolo(regia3.get_id())
        self.__model.elimina_opera(opera2.get_id())

        # MODIFICA
        regia3 = Regia(
            STR_NON_VUOTA,
            0,
            ID_NON_ESISTENTE,
            STR_NON_VUOTA,
            dict(),
            dict(),
        )
        self.assertRaises(
            IdInesistenteException, self.__model.modifica_spettacolo, regia3
        )
        print("Passato MODIFICA IdInesistente")

        regia: Regia | None = self.__model.get_spettacolo(regia.get_id())  # type: ignore
        assert regia is not None
        regia.set_titolo(regia.get_titolo() + STR_NON_VUOTA * 3)
        self.__model.modifica_spettacolo(regia)
        regia_: Regia | None = self.__model.get_spettacolo(regia.get_id())  # type: ignore
        assert regia_ is not None
        self.assertEqual(regia_, regia)
        print("Passato MODIFICA")

        # CARICA
        self.__model._Model__carica_spettacoli()  # type: ignore
        self.assertEqual(self.__model.get_spettacoli(), [regia, regia2])
        print("Passato CARICA")

        # ELIMINA
        self.assertRaises(
            IdInesistenteException, self.__model.elimina_spettacolo, ID_NON_ESISTENTE
        )
        print("Passato ELIMINA IdInesistente")

        evento = Evento(DATA_ORA_PASSATO, regia.get_id())
        self.__model.aggiungi_evento(evento)
        self.assertRaises(
            OggettoInUsoException, self.__model.elimina_spettacolo, regia.get_id()
        )
        print("Passato ELIMINA OggettoInUso")
        self.__model.elimina_evento(evento.get_id())

        self.__model.elimina_spettacolo(regia.get_id())
        self.assertEqual(self.__model.get_spettacoli(), [regia2])
        print("Passato ELIMINA")

    def tearDown(self) -> None:
        super().tearDown()

        shutil.rmtree("./test_db/")


if __name__ == "__main__":
    unittest.main()
