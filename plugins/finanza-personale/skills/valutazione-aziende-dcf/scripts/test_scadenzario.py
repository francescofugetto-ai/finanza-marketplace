#!/usr/bin/env python3
"""
test_scadenzario.py — Prova di riferimento dello scadenzario delle valutazioni.

CHE COSA PROVA
--------------
I sette casi chiesti dal piano (§11.5) e dalla reference
`references/08-manutenzione-e-batch.md` §6, piu' quelli che discendono dalle
regole gia' decise:

  1. i quattro stati: mai valutata · 30 giorni · 120 giorni · 400 giorni
  2. scaduta per `ipotesi_valide_fino_a` pur restando sotto i 365 giorni
  3. la catena di tre record collegati dai campi di supersessione del registro
     (`supersedes` e `superato_da`), dove vince l'ultimo della catena e NON il
     piu' recente per data
  4. i bordi delle due soglie, giorno per giorno
  5. gli errori espliciti: file inesistente, registro corrotto, campi mancanti o
     malformati, catene rotte, e i due campi di catena che si contraddicono
  6. che lo script non scriva niente, da nessuna parte

I DATI SONO COSTRUITI QUI DENTRO
--------------------------------
Nessuna riga di questa prova legge `kb-finanza/`. I registri di prova nascono in
una cartella temporanea, vengono usati e spariscono con lei: il registro vero e'
in sola lettura anche per la prova che verifica che lo scadenzario lo legga in
sola lettura.

PERCHE' ESISTE
--------------
Uno scadenzario sbagliato non si rompe: risponde CORRENTE. Un campo dimenticato,
una catena letta per data invece che per supersessione, un registro che non si e'
riusciti ad aprire — tutti e tre finiscono nello stesso modo, cioe' in un elenco
di aziende che sembrano a posto. Questa prova esiste per rendere rumorosi quei
tre silenzi.

USO
---
    python3 test_scadenzario.py

Uscita 0 se passa tutto, 1 se anche un solo controllo fallisce.
"""

import sys

# Lo scadenzario va importato senza lasciare __pycache__ dentro la skill: la
# cartella del plugin non deve contenere niente di temporaneo, e uno strumento di
# prova non deve sporcare cio' che prova.
sys.dont_write_bytecode = True

import json  # noqa: E402
import tempfile  # noqa: E402
from datetime import date, timedelta  # noqa: E402
from pathlib import Path  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))

from scadenzario import (  # noqa: E402
    SCADENZARIO_VERSIONE, ScadenzarioError,
    CORRENTE, DA_RIESAMINARE, MAI_VALUTATA, SCADUTA,
    scadenzario, ultima_della_catena, valutazioni, leggi_registro,
)

# Data di riferimento fissa: una prova che dipende dal giorno in cui gira non e'
# una prova. Tutte le date dei record di prova sono costruite a ritroso da qui.
OGGI = date(2026, 8, 8)


# --------------------------------------------------------------------------- #
# Infrastruttura di conteggio
# --------------------------------------------------------------------------- #

class Prova:
    def __init__(self):
        self.passati = 0
        self.falliti = []

    def afferma(self, etichetta, condizione, dettaglio=""):
        if condizione:
            self.passati += 1
            print(f"  ok   {etichetta}")
        else:
            self.falliti.append((etichetta, dettaglio))
            print(f"  KO   {etichetta}")
            if dettaglio:
                print(f"       -> {dettaglio}")
        return condizione

    def uguale(self, etichetta, atteso, ottenuto):
        return self.afferma(etichetta, atteso == ottenuto,
                            f"atteso {atteso!r}, ottenuto {ottenuto!r}")

    def errore(self, etichetta, funzione, atteso_nel_messaggio=""):
        """Verifica che la chiamata sollevi ScadenzarioError, e che il messaggio
        dica di che cosa si tratta: un errore muto e' meta' errore."""
        try:
            esito = funzione()
        except ScadenzarioError as ex:
            testo = str(ex)
            ok = (len(testo) > 20
                  and atteso_nel_messaggio.casefold() in testo.casefold())
            self.afferma(etichetta, ok, f"messaggio: {testo}")
            if ok:
                print(f"       -> {testo[:150]}")
            return
        except Exception as ex:  # noqa: BLE001 — qui e' esattamente cio' che si prova
            self.afferma(etichetta, False,
                         f"sollevata {type(ex).__name__} invece di ScadenzarioError: {ex}")
            return
        self.afferma(etichetta, False,
                     f"nessun errore sollevato, e' stato restituito {esito!r}")

    def titolo(self, testo):
        print()
        print("=" * 74)
        print("  " + testo)
        print("=" * 74)

    def riepilogo(self):
        totale = self.passati + len(self.falliti)
        print()
        print("=" * 74)
        print(f"  ESITO — {self.passati} controlli superati su {totale}")
        print("=" * 74)
        if self.falliti:
            print()
            for etichetta, dettaglio in self.falliti:
                print(f"  FALLITO  {etichetta}")
                if dettaglio:
                    print(f"           {dettaglio}")
            return 1
        return 0


# --------------------------------------------------------------------------- #
# Costruzione dei dati di prova
# --------------------------------------------------------------------------- #

def giorni_fa(quanti: int) -> str:
    return (OGGI - timedelta(days=quanti)).isoformat()


def fra_giorni(quanti: int) -> str:
    return (OGGI + timedelta(days=quanti)).isoformat()


def valutazione(ident, azienda, data, valide_fino_a, supersedes=None, ticker=None,
                esercizio=2025, **extra):
    """Un record di valutazione come lo scrive la skill: `tipo: dossier` con il
    tag `valutazione`, piu' i campi che lo schema del registro non conosce.

    `supersedes` e `superato_da` sono invece campi del registro, non della skill:
    qui il primo si passa, il secondo lo mette `collega()` — esattamente come nel
    registro vero, dove il record nuovo dichiara chi supera e `kb.py` scrive il
    verso opposto su quello vecchio.
    """
    rec = {
        "id": ident,
        "data": data,
        "layer": "dottrina",
        "soggetto": "-",
        "tipo": "dossier",
        "titolo": f"Valutazione DCF — {azienda}",
        "file": f"reports/valutazioni/{ident}.html",
        "verdetto": None,
        "decisione": f"Valutazione DCF di {azienda} al {data}",
        "classe": "time-sensitive",
        "scade": valide_fino_a,
        "stato": "vigente",
        "supersedes": list(supersedes or []),
        "superato_da": None,
        "vincoli": [],
        "trigger": [],
        "tag": ["valutazione", "dcf"],
        "numeri": {},
        "condivisibile": False,
        # I campi della valutazione, fuori dallo schema del registro.
        "azienda": azienda,
        "ticker": ticker,
        "esercizio_di_riferimento": esercizio,
        "ipotesi_valide_fino_a": valide_fino_a,
    }
    rec.update(extra)
    return rec


def collega(records):
    """Chiude la catena come fa `kb.py` quando il record nuovo entra nel registro.

    `kb.py` (`cmd_add`) scorre il `supersedes` del record che sta inserendo e su
    ciascun record superato scrive `superato_da` e `stato: "superato"`. Qui si fa
    la stessa cosa, e per la stessa ragione: una prova costruita con record che
    non passerebbero mai da `kb.py` proverebbe qualcos'altro.

    I casi che devono restare **incoerenti** non passano di qui: li costruiscono
    a mano, ed e' il punto.
    """
    per_id = {r["id"]: r for r in records}
    for r in records:
        for prec in r["supersedes"]:
            if prec in per_id:
                per_id[prec]["superato_da"] = r["id"]
                per_id[prec]["stato"] = "superato"
    return records


def rumore():
    """Record che non sono valutazioni e che lo scadenzario deve ignorare senza
    inciampare: un dossier senza il tag, un tipo diverso col tag giusto."""
    return [
        {"id": "2026-01-02-dossier-generico", "data": "2026-01-02", "tipo": "dossier",
         "tag": ["genitori", "decumulo"], "titolo": "Dossier senza tag valutazione"},
        {"id": "2026-01-03-distillato", "data": "2026-01-03", "tipo": "distillato",
         "tag": ["valutazione", "the-bull"], "titolo": "Distillato col tag ma tipo diverso"},
    ]


def scrivi(cartella: Path, nome: str, records) -> Path:
    percorso = cartella / nome
    with open(percorso, "w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    return percorso


def uno(percorso, richiesta, **kw):
    """Lo scadenzario per una sola azienda, con la data di riferimento fissa."""
    return scadenzario(percorso, [richiesta], oggi=OGGI, **kw)[0]


# --------------------------------------------------------------------------- #
# 1 · I quattro stati
# --------------------------------------------------------------------------- #

def prova_quattro_stati(p, tmp: Path):
    p.titolo("1 · I QUATTRO STATI")

    registro = scrivi(tmp, "stati.jsonl", rumore() + [
        valutazione("val-corrente", "Alphabet", giorni_fa(30), fra_giorni(335),
                    ticker="GOOGL"),
        valutazione("val-riesame", "Microsoft", giorni_fa(120), fra_giorni(245),
                    ticker="MSFT"),
        valutazione("val-scaduta", "Adobe", giorni_fa(400), fra_giorni(30),
                    ticker="ADBE"),
    ])

    e = uno(registro, "Nvidia")
    p.uguale("azienda mai valutata -> MAI VALUTATA", MAI_VALUTATA, e.stato)
    p.afferma("MAI VALUTATA dichiara che il registro e' stato letto davvero",
              "3" in e.motivo and "registro" in e.motivo, e.motivo)
    p.afferma("MAI VALUTATA non porta un id ne' una data inventati",
              e.id_ultima is None and e.data_ultima is None and e.giorni is None)

    e = uno(registro, "Alphabet")
    p.uguale("valutazione di 30 giorni -> CORRENTE", CORRENTE, e.stato)
    p.uguale("giorni trascorsi = 30", 30, e.giorni)
    p.uguale("id dell'ultima valutazione", "val-corrente", e.id_ultima)
    p.uguale("esercizio di riferimento riportato", 2025, e.esercizio_di_riferimento)
    p.afferma("il motivo sta su una riga sola", "\n" not in e.motivo, repr(e.motivo))
    p.afferma("il motivo dice la data e i giorni",
              "30 giorni" in e.motivo and "luglio 2026" in e.motivo, e.motivo)

    e = uno(registro, "Microsoft")
    p.uguale("valutazione di 120 giorni -> DA RIESAMINARE", DA_RIESAMINARE, e.stato)
    p.uguale("giorni trascorsi = 120", 120, e.giorni)
    p.afferma("il motivo cita la soglia dei 90 giorni", "90 giorni" in e.motivo, e.motivo)

    e = uno(registro, "Adobe")
    p.uguale("valutazione di 400 giorni -> SCADUTA", SCADUTA, e.stato)
    p.uguale("giorni trascorsi = 400", 400, e.giorni)
    p.afferma("il motivo cita la soglia dei 365 giorni", "365 giorni" in e.motivo, e.motivo)

    e = uno(registro, "GOOGL")
    p.afferma("si trova anche interrogando per ticker",
              e.stato == CORRENTE and e.id_ultima == "val-corrente", f"{e.stato} {e.id_ultima}")
    e = uno(registro, "  msft  ")
    p.afferma("il confronto ignora maiuscole e spazi ai bordi",
              e.id_ultima == "val-riesame", str(e.id_ultima))

    esiti = scadenzario(registro, ["Adobe", "Nvidia", "Alphabet"], oggi=OGGI)
    p.uguale("l'ordine delle risposte e' quello della richiesta",
             ["Adobe", "Nvidia", "Alphabet"], [x.richiesta for x in esiti])

    p.uguale("i record che non sono valutazioni non entrano nel conteggio",
             3, len(valutazioni(leggi_registro(registro))))


# --------------------------------------------------------------------------- #
# 2 · La scadenza dichiarata vince sui giorni
# --------------------------------------------------------------------------- #

def prova_ipotesi_valide_fino_a(p, tmp: Path):
    p.titolo("2 · SCADUTA PER `ipotesi_valide_fino_a` SOTTO I 365 GIORNI")

    registro = scrivi(tmp, "ipotesi.jsonl", [
        # 100 giorni: per calendario sarebbe DA RIESAMINARE. Ma l'analista aveva
        # dichiarato che le ipotesi valevano fino a 10 giorni fa.
        valutazione("val-ipotesi-scadute", "Ferrari", giorni_fa(100), giorni_fa(10),
                    ticker="RACE"),
        # 30 giorni, ipotesi scadute proprio ieri: nemmeno CORRENTE lo salva.
        valutazione("val-ipotesi-ieri", "Enel", giorni_fa(30), giorni_fa(1)),
        # ipotesi valide fino a oggi: oggi e' l'ultimo giorno valido, regge ancora.
        valutazione("val-ipotesi-oggi", "Eni", giorni_fa(30), OGGI.isoformat()),
    ])

    e = uno(registro, "Ferrari")
    p.uguale("100 giorni ma ipotesi superate -> SCADUTA", SCADUTA, e.stato)
    p.uguale("i giorni trascorsi restano quelli veri", 100, e.giorni)
    p.afferma("il motivo attribuisce la scadenza alle ipotesi, non ai giorni",
              "ipotesi valide fino al" in e.motivo and "100 giorni" in e.motivo, e.motivo)

    e = uno(registro, "Enel")
    p.uguale("30 giorni ma ipotesi superate ieri -> SCADUTA", SCADUTA, e.stato)

    e = uno(registro, "Eni")
    p.uguale("ipotesi valide fino a oggi -> ancora CORRENTE", CORRENTE, e.stato)


# --------------------------------------------------------------------------- #
# 3 · La catena
# --------------------------------------------------------------------------- #

def prova_catena(p, tmp: Path):
    p.titolo("3 · LA CATENA DI TRE RECORD, COSTRUITA COI CAMPI DEL REGISTRO")

    # Tre valutazioni della stessa azienda. L'ordine della catena e' A -> B -> C,
    # ma per DATA il piu' recente e' B: e' il caso del recupero di una valutazione
    # arretrata, inserita dopo ma piu' vecchia di quella che la supera.
    #
    #   A  val-a   434 giorni fa   supersedes: []           superato_da: val-b
    #   B  val-b    19 giorni fa   supersedes: [val-a]      superato_da: val-c
    #                                                       <- il piu' recente per data
    #   C  val-c    99 giorni fa   supersedes: [val-b]      superato_da: null
    #                                                       <- l'ultimo della catena
    #
    # Gli stati sono scelti diversi apposta: leggere per data darebbe CORRENTE
    # (19 giorni), leggere la catena da' DA RIESAMINARE (99 giorni). Se la regola
    # fosse sbagliata, questo controllo non potrebbe passare per caso.
    catena = collega([
        valutazione("val-a", "Bending Spoons", giorni_fa(434), giorni_fa(69)),
        valutazione("val-b", "Bending Spoons", giorni_fa(19), fra_giorni(346),
                    supersedes=["val-a"]),
        valutazione("val-c", "Bending Spoons", giorni_fa(99), fra_giorni(266),
                    supersedes=["val-b"]),
    ])
    # Anche l'ordine delle righe nel file e' fuorviante di proposito: l'ultima
    # riga del file e' quella che NON deve vincere.
    registro = scrivi(tmp, "catena.jsonl", [catena[2], catena[0], catena[1]])

    e = uno(registro, "Bending Spoons")
    p.uguale("vince l'ultimo della catena, non il piu' recente per data",
             "val-c", e.id_ultima)
    p.uguale("lo stato e' quello dell'ultimo della catena", DA_RIESAMINARE, e.stato)
    p.uguale("i giorni sono quelli dell'ultimo della catena", 99, e.giorni)
    p.uguale("la catena e' ricostruita dal piu' vecchio al piu' recente",
             ["val-a", "val-b", "val-c"], e.catena)
    p.afferma("il motivo dichiara che c'e' una catena", "catena di 3" in e.motivo, e.motivo)

    ultima, ids = ultima_della_catena(catena)
    p.afferma("ultima_della_catena e' indipendente dall'ordine in ingresso",
              ultima["id"] == "val-c" and ids == ["val-a", "val-b", "val-c"], str(ids))

    ultima, _ = ultima_della_catena(list(reversed(catena)))
    p.uguale("...e anche dall'ordine inverso", "val-c", ultima["id"])

    # Le due direzioni sono entrambe lette: se lo scadenzario guardasse solo
    # `supersedes`, un `superato_da` che nessuno conferma passerebbe inosservato.
    p.afferma("i record di prova sono collegati in tutte e due le direzioni",
              catena[0]["superato_da"] == "val-b"
              and catena[1]["superato_da"] == "val-c"
              and catena[2]["superato_da"] is None,
              str([r["superato_da"] for r in catena]))
    p.afferma("il record superato porta anche `stato: superato`, come lo scrive kb.py",
              catena[0]["stato"] == "superato" and catena[2]["stato"] == "vigente",
              str([r["stato"] for r in catena]))

    # Una sola valutazione e' una catena di uno.
    registro = scrivi(tmp, "catena-uno.jsonl", [
        valutazione("val-sola", "Bending Spoons", giorni_fa(434), fra_giorni(30))])
    e = uno(registro, "Bending Spoons")
    p.uguale("una valutazione sola e' una catena di uno", ["val-sola"], e.catena)
    p.afferma("con una sola valutazione il motivo non parla di catene",
              "catena" not in e.motivo, e.motivo)

    # Due aziende diverse non si contaminano: la catena si costruisce dentro
    # l'azienda richiesta, non sull'intero registro.
    registro = scrivi(tmp, "catena-due-aziende.jsonl", catena + [
        valutazione("val-x", "Adobe", giorni_fa(10), fra_giorni(355)),
    ])
    e = uno(registro, "Adobe")
    p.afferma("le valutazioni di un'altra azienda non entrano nella catena",
              e.id_ultima == "val-x" and e.catena == ["val-x"], str(e.catena))


# --------------------------------------------------------------------------- #
# 4 · I bordi delle soglie
# --------------------------------------------------------------------------- #

def prova_bordi(p, tmp: Path):
    p.titolo("4 · I BORDI DELLE DUE SOGLIE")

    registro = scrivi(tmp, "bordi.jsonl", [
        valutazione("b-89", "B89", giorni_fa(89), fra_giorni(200)),
        valutazione("b-90", "B90", giorni_fa(90), fra_giorni(200)),
        valutazione("b-91", "B91", giorni_fa(91), fra_giorni(200)),
        valutazione("b-365", "B365", giorni_fa(365), fra_giorni(200)),
        valutazione("b-366", "B366", giorni_fa(366), fra_giorni(200)),
        valutazione("b-oggi", "BOGGI", OGGI.isoformat(), fra_giorni(200)),
    ])

    for nome, atteso in (("B89", CORRENTE), ("B90", CORRENTE), ("B91", DA_RIESAMINARE),
                         ("B365", DA_RIESAMINARE), ("B366", SCADUTA), ("BOGGI", CORRENTE)):
        p.uguale(f"bordo {nome} -> {atteso}", atteso, uno(registro, nome).stato)

    # Soglie personalizzate: chi le passa deve vederle applicate davvero.
    e = uno(registro, "B89", riesame=30, scadenza=60)
    p.uguale("con soglie 30/60 una valutazione di 89 giorni e' SCADUTA", SCADUTA, e.stato)
    e = uno(registro, "B365", riesame=400, scadenza=800)
    p.uguale("con soglie 400/800 una valutazione di 365 giorni e' CORRENTE", CORRENTE, e.stato)


# --------------------------------------------------------------------------- #
# 5 · Gli errori espliciti
# --------------------------------------------------------------------------- #

def prova_errori(p, tmp: Path):
    p.titolo("5 · ERRORI ESPLICITI, MAI UN ELENCO VUOTO")

    p.errore("file inesistente -> errore",
             lambda: scadenzario(tmp / "non-esiste.jsonl", ["Alphabet"], oggi=OGGI),
             "non trovato")

    p.errore("percorso che e' una cartella -> errore",
             lambda: scadenzario(tmp, ["Alphabet"], oggi=OGGI),
             "non e' un file")

    corrotto = tmp / "corrotto.jsonl"
    corrotto.write_text('{"id": "val-1", "tipo": "dossier"\nnon-json\n', encoding="utf-8")
    p.errore("riga non-JSON nel registro -> errore",
             lambda: scadenzario(corrotto, ["Alphabet"], oggi=OGGI),
             "JSON non valido")

    non_oggetto = tmp / "non-oggetto.jsonl"
    non_oggetto.write_text('["questo", "e", "un", "elenco"]\n', encoding="utf-8")
    p.errore("riga JSON che non e' un oggetto -> errore",
             lambda: scadenzario(non_oggetto, ["Alphabet"], oggi=OGGI),
             "non e' un oggetto JSON")

    # --- i due campi che lo schema del registro non valida ------------------
    senza_data_ipotesi = valutazione("val-1", "Alphabet", giorni_fa(30), fra_giorni(300))
    del senza_data_ipotesi["ipotesi_valide_fino_a"]
    r = scrivi(tmp, "senza-ipotesi.jsonl", [senza_data_ipotesi])
    p.errore("`ipotesi_valide_fino_a` mancante -> errore, MAI 'nessuna scadenza'",
             lambda: scadenzario(r, ["Alphabet"], oggi=OGGI),
             "ipotesi_valide_fino_a")

    r = scrivi(tmp, "ipotesi-nulla.jsonl", [
        valutazione("val-1", "Alphabet", giorni_fa(30), None)])
    p.errore("`ipotesi_valide_fino_a` a null -> errore",
             lambda: scadenzario(r, ["Alphabet"], oggi=OGGI),
             "ipotesi_valide_fino_a")

    r = scrivi(tmp, "ipotesi-malformata.jsonl", [
        valutazione("val-1", "Alphabet", giorni_fa(30), "31/12/2026")])
    p.errore("`ipotesi_valide_fino_a` malformata -> errore",
             lambda: scadenzario(r, ["Alphabet"], oggi=OGGI),
             "AAAA-MM-GG")

    senza_supersedes = valutazione("val-1", "Alphabet", giorni_fa(30), fra_giorni(300))
    del senza_supersedes["supersedes"]
    r = scrivi(tmp, "senza-supersedes.jsonl", [senza_supersedes])
    p.errore("`supersedes` mancante -> errore",
             lambda: scadenzario(r, ["Alphabet"], oggi=OGGI),
             "supersedes")

    non_lista = valutazione("val-1", "Alphabet", giorni_fa(30), fra_giorni(300))
    non_lista["supersedes"] = "val-0"
    r = scrivi(tmp, "supersedes-non-lista.jsonl", [non_lista])
    p.errore("`supersedes` che non e' una lista -> errore",
             lambda: scadenzario(r, ["Alphabet"], oggi=OGGI),
             "non e' una lista")

    r = scrivi(tmp, "supersedes-malformato.jsonl", [
        valutazione("val-1", "Alphabet", giorni_fa(30), fra_giorni(300), supersedes=[7])])
    p.errore("`supersedes` che contiene qualcosa che non e' un id -> errore",
             lambda: scadenzario(r, ["Alphabet"], oggi=OGGI),
             "non e' l'id di un record")

    senza_superato_da = valutazione("val-1", "Alphabet", giorni_fa(30), fra_giorni(300))
    del senza_superato_da["superato_da"]
    r = scrivi(tmp, "senza-superato-da.jsonl", [senza_superato_da])
    p.errore("`superato_da` mancante -> errore",
             lambda: scadenzario(r, ["Alphabet"], oggi=OGGI),
             "superato_da")

    superato_da_rotto = valutazione("val-1", "Alphabet", giorni_fa(30), fra_giorni(300))
    superato_da_rotto["superato_da"] = 7
    r = scrivi(tmp, "superato-da-malformato.jsonl", [superato_da_rotto])
    p.errore("`superato_da` che non e' un id -> errore",
             lambda: scadenzario(r, ["Alphabet"], oggi=OGGI),
             "superato_da")

    r = scrivi(tmp, "data-malformata.jsonl", [
        valutazione("val-1", "Alphabet", "2026-13-45", fra_giorni(300))])
    p.errore("`data` malformata -> errore",
             lambda: scadenzario(r, ["Alphabet"], oggi=OGGI),
             "'data'")

    r = scrivi(tmp, "data-futura.jsonl", [
        valutazione("val-1", "Alphabet", fra_giorni(3), fra_giorni(300))])
    p.errore("valutazione datata dopo la data di riferimento -> errore",
             lambda: scadenzario(r, ["Alphabet"], oggi=OGGI),
             "datata")

    senza_nome = valutazione("val-1", None, giorni_fa(30), fra_giorni(300))
    senza_nome["ticker"] = None
    senza_nome["isin"] = None
    r = scrivi(tmp, "senza-nome.jsonl", [senza_nome])
    p.errore("valutazione senza azienda, ticker ne' isin -> errore",
             lambda: scadenzario(r, ["Alphabet"], oggi=OGGI),
             "azienda")

    # --- le catene rotte ----------------------------------------------------
    r = scrivi(tmp, "anello-mancante.jsonl", [
        valutazione("val-1", "Alphabet", giorni_fa(30), fra_giorni(300),
                    supersedes=["val-che-non-esiste"])])
    p.errore("`supersedes` che punta a un id inesistente -> errore",
             lambda: scadenzario(r, ["Alphabet"], oggi=OGGI),
             "catena e' rotta")

    orfano = valutazione("val-1", "Alphabet", giorni_fa(30), fra_giorni(300))
    orfano["superato_da"] = "val-che-non-esiste"
    r = scrivi(tmp, "superato-da-nel-vuoto.jsonl", [orfano])
    p.errore("`superato_da` che punta a un id inesistente -> errore, mai CORRENTE",
             lambda: scadenzario(r, ["Alphabet"], oggi=OGGI),
             "catena e' rotta")

    r = scrivi(tmp, "due-teste.jsonl", [
        valutazione("val-1", "Alphabet", giorni_fa(300), fra_giorni(60)),
        valutazione("val-2", "Alphabet", giorni_fa(30), fra_giorni(300))])
    p.errore("due valutazioni scollegate della stessa azienda -> errore",
             lambda: scadenzario(r, ["Alphabet"], oggi=OGGI),
             "catene scollegate")

    # Biforcazione come la lascerebbe il registro: `kb.py` scrive `superato_da`
    # sul superato ogni volta, quindi l'ultimo inserito sovrascrive il primo e
    # resta una sola delle due dichiarazioni.
    biforcata = [
        valutazione("val-1", "Alphabet", giorni_fa(300), fra_giorni(60)),
        valutazione("val-2", "Alphabet", giorni_fa(60), fra_giorni(300), supersedes=["val-1"]),
        valutazione("val-3", "Alphabet", giorni_fa(30), fra_giorni(300), supersedes=["val-1"]),
    ]
    biforcata[0]["superato_da"] = "val-3"
    r = scrivi(tmp, "biforcazione.jsonl", biforcata)
    p.errore("due record che superano lo stesso record -> errore",
             lambda: scadenzario(r, ["Alphabet"], oggi=OGGI),
             "si biforca")

    r = scrivi(tmp, "anello-chiuso.jsonl", collega([
        valutazione("val-1", "Alphabet", giorni_fa(300), fra_giorni(60),
                    supersedes=["val-2"]),
        valutazione("val-2", "Alphabet", giorni_fa(30), fra_giorni(300),
                    supersedes=["val-1"])]))
    p.errore("catena che si chiude ad anello -> errore",
             lambda: scadenzario(r, ["Alphabet"], oggi=OGGI),
             "anello")

    r = scrivi(tmp, "supersedes-doppio.jsonl", collega([
        valutazione("val-1", "Alphabet", giorni_fa(300), fra_giorni(60)),
        valutazione("val-2", "Alphabet", giorni_fa(200), fra_giorni(60)),
        valutazione("val-3", "Alphabet", giorni_fa(30), fra_giorni(300),
                    supersedes=["val-1", "val-2"])]))
    p.errore("una valutazione che ne supera due sulla stessa azienda -> errore",
             lambda: scadenzario(r, ["Alphabet"], oggi=OGGI),
             "catena lineare")

    r = scrivi(tmp, "id-duplicato.jsonl", [
        valutazione("val-1", "Alphabet", giorni_fa(300), fra_giorni(60)),
        valutazione("val-1", "Alphabet", giorni_fa(30), fra_giorni(300))])
    p.errore("id duplicato fra le valutazioni della stessa azienda -> errore",
             lambda: scadenzario(r, ["Alphabet"], oggi=OGGI),
             "id duplicato")

    # --- i due campi di catena che si contraddicono -------------------------
    #
    # `kb.py` li scrive nella stessa operazione, quindi discordano solo se il
    # registro e' stato toccato a mano. Il modo sbagliato di cavarsela sarebbe
    # fidarsi di uno dei due: in meta' dei casi mostrerebbe come CORRENTE una
    # valutazione superata, in silenzio. Sono le tre forme possibili.
    r = scrivi(tmp, "incoerenza-solo-supersedes.jsonl", [
        valutazione("val-1", "Alphabet", giorni_fa(300), fra_giorni(60)),
        valutazione("val-2", "Alphabet", giorni_fa(30), fra_giorni(300),
                    supersedes=["val-1"])])
    p.errore("val-2 supera val-1 ma val-1 non lo dichiara -> errore, non CORRENTE su val-1",
             lambda: scadenzario(r, ["Alphabet"], oggi=OGGI),
             "si contraddicono")

    solo_avanti = valutazione("val-1", "Alphabet", giorni_fa(300), fra_giorni(60))
    solo_avanti["superato_da"] = "val-2"
    r = scrivi(tmp, "incoerenza-solo-superato-da.jsonl", [
        solo_avanti,
        valutazione("val-2", "Alphabet", giorni_fa(30), fra_giorni(300))])
    p.errore("val-1 si dichiara superato da val-2 ma val-2 non lo elenca -> errore",
             lambda: scadenzario(r, ["Alphabet"], oggi=OGGI),
             "si contraddicono")

    discordi = valutazione("val-1", "Alphabet", giorni_fa(300), fra_giorni(60))
    discordi["superato_da"] = "val-3"
    r = scrivi(tmp, "incoerenza-discordi.jsonl", [
        discordi,
        valutazione("val-2", "Alphabet", giorni_fa(60), fra_giorni(300),
                    supersedes=["val-1"]),
        valutazione("val-3", "Alphabet", giorni_fa(30), fra_giorni(300))])
    p.errore("i due campi indicano due successori diversi -> errore",
             lambda: scadenzario(r, ["Alphabet"], oggi=OGGI),
             "si contraddicono")

    # --- ingresso incoerente ------------------------------------------------
    buono = scrivi(tmp, "buono.jsonl", [
        valutazione("val-1", "Alphabet", giorni_fa(30), fra_giorni(300))])

    p.errore("elenco di aziende vuoto -> errore, non un elenco vuoto in uscita",
             lambda: scadenzario(buono, [], oggi=OGGI),
             "nessuna azienda richiesta")
    p.errore("elenco di sole stringhe vuote -> errore",
             lambda: scadenzario(buono, ["", "   "], oggi=OGGI),
             "nessuna azienda richiesta")
    p.errore("soglia di scadenza non oltre quella di riesame -> errore",
             lambda: scadenzario(buono, ["Alphabet"], oggi=OGGI, riesame=90, scadenza=90),
             "riesame")
    p.errore("soglie non positive -> errore",
             lambda: scadenzario(buono, ["Alphabet"], oggi=OGGI, riesame=0),
             "giorni interi positivi")


# --------------------------------------------------------------------------- #
# 6 · Registro leggibile ma senza valutazioni, e sola lettura
# --------------------------------------------------------------------------- #

def prova_vuoto_e_sola_lettura(p, tmp: Path):
    p.titolo("6 · REGISTRO SENZA VALUTAZIONI, E SOLA LETTURA")

    vuoto = scrivi(tmp, "vuoto.jsonl", [])
    e = uno(vuoto, "Alphabet")
    p.uguale("registro esistente e vuoto -> MAI VALUTATA, non un errore",
             MAI_VALUTATA, e.stato)
    p.afferma("il motivo distingue 'letto e vuoto' da 'non letto'",
              "0 in tutto" in e.motivo, e.motivo)

    solo_rumore = scrivi(tmp, "solo-rumore.jsonl", rumore())
    e = uno(solo_rumore, "Alphabet")
    p.uguale("registro con soli record di altro tipo -> MAI VALUTATA",
             MAI_VALUTATA, e.stato)

    # --- la prova che lo script non scrive ----------------------------------
    cartella = tmp / "sola-lettura"
    cartella.mkdir()
    registro = scrivi(cartella, "ledger.jsonl", collega([
        valutazione("val-1", "Alphabet", giorni_fa(300), fra_giorni(60)),
        valutazione("val-2", "Alphabet", giorni_fa(30), fra_giorni(300),
                    supersedes=["val-1"]),
    ]))
    prima_byte = registro.read_bytes()
    prima_mtime = registro.stat().st_mtime_ns
    prima_elenco = sorted(x.name for x in cartella.iterdir())

    scadenzario(registro, ["Alphabet", "Nvidia"], oggi=OGGI)

    p.afferma("il registro non e' stato modificato", registro.read_bytes() == prima_byte)
    p.afferma("il registro non e' stato riscritto identico",
              registro.stat().st_mtime_ns == prima_mtime,
              "la data di modifica e' cambiata: qualcuno ha aperto il file in scrittura")
    p.uguale("nessun file nuovo nella cartella del registro",
             prima_elenco, sorted(x.name for x in cartella.iterdir()))

    # Nessun __pycache__ nella cartella degli script: sys.dont_write_bytecode e'
    # impostato in testa, ma va verificato invece che dato per fatto.
    scripts = Path(__file__).resolve().parent
    p.afferma("nessun __pycache__ nella cartella degli script",
              not (scripts / "__pycache__").exists(),
              "e' stato scritto bytecode dentro il plugin")


# --------------------------------------------------------------------------- #

def main():
    print("=" * 74)
    print("  PROVA DI RIFERIMENTO DELLO SCADENZARIO")
    print(f"  scadenzario versione {SCADENZARIO_VERSIONE}")
    print(f"  data di riferimento fissa: {OGGI.isoformat()}")
    print("  dati di prova costruiti qui dentro — kb-finanza non viene mai aperta")
    print("=" * 74)

    p = Prova()
    with tempfile.TemporaryDirectory(prefix="scadenzario-prova-") as cartella:
        tmp = Path(cartella)
        prova_quattro_stati(p, tmp)
        prova_ipotesi_valide_fino_a(p, tmp)
        prova_catena(p, tmp)
        prova_bordi(p, tmp)
        prova_errori(p, tmp)
        prova_vuoto_e_sola_lettura(p, tmp)

    sys.exit(p.riepilogo())


if __name__ == "__main__":
    main()
