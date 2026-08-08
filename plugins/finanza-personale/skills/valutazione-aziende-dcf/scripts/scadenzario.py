#!/usr/bin/env python3
"""
scadenzario.py — Interroga il registro decisionale e dice, azienda per azienda,
                 se la sua valutazione e' ancora buona.

SCOPO
-----
E' il passo 3 del comando di manutenzione (`references/08-manutenzione-e-batch.md`
§4). Riceve il percorso del registro e un elenco di aziende o ticker, e restituisce
per ciascuna:

  - l'ultima valutazione trovata, con data e identificativo
  - i giorni trascorsi da quella data
  - `ipotesi_valide_fino_a`
  - l'esercizio di riferimento usato
  - lo stato fra i quattro: MAI VALUTATA · SCADUTA · DA RIESAMINARE · CORRENTE
  - il motivo dello stato, in una riga

Che cosa se ne fa la skill sta nel `08`: riesame leggero su CORRENTE e
DA RIESAMINARE, coda su SCADUTA e MAI VALUTATA. Qui non c'e' niente di tutto
questo: questo file classifica e basta.

SOLA LETTURA — SENZA ECCEZIONI
------------------------------
Lo script apre il registro in lettura e non scrive nulla, da nessuna parte, in
nessun ramo di esecuzione. Non ci sono `open(..., "w")`, non si creano cartelle,
non si tocca `kb-finanza/`. Il record del passo 8 lo scrive la skill attraverso
`kb-registro`, mai lo scadenzario. Nessuna dipendenza esterna: solo libreria
standard.

DOVE VIVONO LE VALUTAZIONI NEL REGISTRO
---------------------------------------
Il registro ha una **lista chiusa di tipi** e `valutazione` non e' fra questi. Una
valutazione e' quindi un record `tipo: "dossier"` con `"valutazione"` fra i `tag`
(vedi `08` §4 passo 8 e `kb-registro/references/SCHEMA.md`). Oltre ai campi dello
schema porta i campi della valutazione — `azienda`, `ticker`, `isin`,
`esercizio_di_riferimento`, `ipotesi_valide_fino_a`, `supera` — che lo schema
**non valida**, perche' non li conosce. Li valida questo file, ed e' il motivo
per cui la validazione qui e' severa: e' l'unico punto in cui viene fatta.

I QUATTRO MODI DI SBAGLIARE, E COME SONO CHIUSI
-----------------------------------------------
  1. **Un elenco vuoto spacciato per «nessuna valutazione».** Registro assente,
     illeggibile o malformato -> `ScadenzarioError`, mai una risposta. Sono due
     situazioni opposte: «non c'e' niente da aggiornare» e «non si sa niente».
     Un MAI VALUTATA lo si scrive solo dopo aver letto il registro davvero, e il
     motivo dice quante valutazioni conteneva.
  2. **Una data mancante letta come «nessuna scadenza».** `ipotesi_valide_fino_a`
     assente o malformata -> errore. E' il fallimento peggiore possibile, perche'
     mostrerebbe tutto come CORRENTE proprio quando non lo e'.
  3. **La piu' recente per data scambiata per l'ultima.** La catena si costruisce
     seguendo `supera`, non ordinando per `data`. La differenza emerge quando si
     recupera una valutazione arretrata: il record inserito dopo e' piu' recente
     di calendario ma sta in mezzo alla catena, e non e' lui a valere.
  4. **Una catena rotta risolta a intuito.** Anello mancante, due teste, ciclo,
     record orfano: nessuno di questi si indovina, tutti sollevano un errore.

CONVENZIONI E LIMITI (dichiarati, non nascosti)
-----------------------------------------------
  - Le soglie sono in **giorni interi**: 90 per il riesame, 365 per la scadenza
    piena. Sono estremi inclusi: a 90 giorni esatti si e' ancora CORRENTE, a 91
    si passa a DA RIESAMINARE; a 365 esatti DA RIESAMINARE, a 366 SCADUTA.
  - `ipotesi_valide_fino_a` e' l'**ultimo giorno valido**: nel giorno stesso la
    valutazione regge ancora, dal successivo e' SCADUTA. Vince sui giorni
    trascorsi, perche' e' una scadenza dichiarata dall'analista e non una soglia
    di calendario.
  - Il confronto per azienda avviene su `azienda`, `ticker` e `isin`, ignorando
    maiuscole e spazi ai bordi. L'`isin` non e' nell'elenco del piano ma vale la
    stessa cosa: chi lo passa deve ottenere il record, non un MAI VALUTATA falso.
  - La catena segue **solo** `supera`. I campi `supersedes` e `superato_da` dello
    schema del registro non vengono letti: sono il meccanismo generale di
    supersessione fra documenti, `supera` e' il collegamento fra valutazioni
    della stessa azienda, e mescolarli darebbe due verita' sulla stessa catena.
  - Il registro viene letto **una volta sola** per l'intero elenco di aziende.
  - Tutti i record di valutazione presenti vengono validati, non solo quelli
    delle aziende richieste. Limitare la validazione al sottoinsieme che combacia
    sarebbe circolare: e' proprio il campo con cui si combacia a poter mancare, e
    un record scartato in silenzio e' un anello di catena perso.

USO
---
    python3 scadenzario.py --registro kb-finanza/ledger.jsonl \\
                           --aziende "Alphabet" GOOGL "Bending Spoons" \\
                           [--oggi 2026-08-08] [--riesame 90] [--scadenza 365] [--json]

Uscita 0 se la lettura e' andata a buon fine (qualunque siano gli stati),
1 con un messaggio su stderr se il registro non e' interrogabile.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Optional

# ─── versione dello strumento ──────────────────────────────────────────────
# Vera variabile di modulo, non una riga dentro il commento: un controllo
# automatico deve poterla leggere da programma.
SCADENZARIO_VERSIONE = "1.0"

# Soglie di default, in giorni. Estremi inclusi (vedi le convenzioni).
SOGLIA_RIESAME = 90
SOGLIA_SCADENZA = 365

# Come si riconosce una valutazione nel registro.
TIPO_VALUTAZIONE = "dossier"
TAG_VALUTAZIONE = "valutazione"

# I quattro stati. Sono stringhe e non un enum perche' finiscono cosi' come sono
# nel documento e nel record di manutenzione: un solo posto in cui sono scritti.
MAI_VALUTATA = "MAI VALUTATA"
SCADUTA = "SCADUTA"
DA_RIESAMINARE = "DA RIESAMINARE"
CORRENTE = "CORRENTE"

# Campi su cui si riconosce l'azienda richiesta.
CAMPI_IDENTITA = ("azienda", "ticker", "isin")

MESI = ("gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno",
        "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre")


class ScadenzarioError(ValueError):
    """Il registro non e' interrogabile, oppure lo e' in modo ambiguo.

    E' un'eccezione e non uno stato perche' non esiste una risposta corretta da
    restituire. Uno stato dice qualcosa sull'azienda; qui non si sa niente, e le
    due cose non vanno confuse in un elenco vuoto.
    """


# --------------------------------------------------------------------------- #
# Formattazione
# --------------------------------------------------------------------------- #

def _in_lettere(d: date) -> str:
    """La data come si legge in una riga di motivo: '14 luglio 2025'."""
    return f"{d.day} {MESI[d.month - 1]} {d.year}"


def _giorni(quanti: int) -> str:
    """'1 giorno' / 'N giorni'. Una riga di motivo si legge a voce."""
    return "1 giorno" if quanti == 1 else f"{quanti} giorni"


# --------------------------------------------------------------------------- #
# Strutture di output
# --------------------------------------------------------------------------- #

@dataclass
class Esito:
    """La risposta per una singola azienda richiesta.

    `richiesta` e' la stringa passata da chi chiama, non il nome canonico del
    record: chi legge deve poter ricollegare la riga alla sua domanda anche
    quando ha interrogato per ticker e il record porta il nome esteso.
    """
    richiesta: str
    stato: str
    motivo: str
    id_ultima: Optional[str] = None
    data_ultima: Optional[date] = None
    giorni: Optional[int] = None
    ipotesi_valide_fino_a: Optional[date] = None
    esercizio_di_riferimento: Optional[object] = None
    azienda: Optional[str] = None
    catena: list = field(default_factory=list)   # id dal piu' vecchio al piu' recente


# --------------------------------------------------------------------------- #
# Lettura del registro
# --------------------------------------------------------------------------- #

def leggi_registro(percorso) -> list:
    """Tutti i record del registro, nell'ordine in cui stanno nel file.

    Solleva ScadenzarioError se il percorso non esiste, non e' un file, non si
    riesce a leggere o contiene una riga che non e' un oggetto JSON. Non esiste
    un ramo che restituisca una lista vuota per un registro che non si e'
    riusciti a leggere.
    """
    p = Path(percorso)

    if not p.exists():
        raise ScadenzarioError(
            f"registro non trovato: {p}. Non e' la stessa cosa di un registro "
            f"vuoto: qui non si sa niente, e non si puo' dire che nessuna azienda "
            f"sia stata valutata"
        )
    if not p.is_file():
        raise ScadenzarioError(f"il percorso del registro non e' un file: {p}")

    try:
        testo = p.read_text(encoding="utf-8")
    except OSError as ex:
        raise ScadenzarioError(f"registro illeggibile ({p}): {ex}")
    except UnicodeDecodeError as ex:
        raise ScadenzarioError(f"registro non decodificabile in UTF-8 ({p}): {ex}")

    records = []
    for n, riga in enumerate(testo.splitlines(), 1):
        riga = riga.strip()
        if not riga:
            continue
        try:
            rec = json.loads(riga)
        except json.JSONDecodeError as ex:
            raise ScadenzarioError(f"{p.name} riga {n}: JSON non valido — {ex}")
        if not isinstance(rec, dict):
            raise ScadenzarioError(
                f"{p.name} riga {n}: la riga non e' un oggetto JSON ma {type(rec).__name__}"
            )
        records.append(rec)

    return records


# --------------------------------------------------------------------------- #
# Validazione dei record di valutazione
# --------------------------------------------------------------------------- #

def _etichetta(rec: dict) -> str:
    """Come si nomina un record nei messaggi d'errore, anche se gli manca l'id."""
    ident = rec.get("id")
    return f"record '{ident}'" if isinstance(ident, str) and ident.strip() else "un record senza id"


def _data_obbligatoria(rec: dict, campo: str, spiegazione: str) -> date:
    """La data di un campo che deve esserci. Assente o malformata -> errore."""
    if campo not in rec:
        raise ScadenzarioError(f"{_etichetta(rec)}: manca il campo '{campo}'. {spiegazione}")
    valore = rec[campo]
    if not isinstance(valore, str) or not valore.strip():
        raise ScadenzarioError(
            f"{_etichetta(rec)}: il campo '{campo}' e' {valore!r}, non una data. {spiegazione}"
        )
    try:
        return datetime.strptime(valore.strip(), "%Y-%m-%d").date()
    except ValueError:
        raise ScadenzarioError(
            f"{_etichetta(rec)}: il campo '{campo}' vale {valore!r}, che non e' una data "
            f"AAAA-MM-GG valida. {spiegazione}"
        )


def _valida_valutazione(rec: dict) -> None:
    """I quattro requisiti di un record di valutazione, tutti obbligatori.

    Lo schema del registro non li conosce e non li controlla: se non li controlla
    questo file, non li controlla nessuno.
    """
    ident = rec.get("id")
    if not isinstance(ident, str) or not ident.strip():
        raise ScadenzarioError(
            "un record di valutazione e' senza 'id': senza identificativo non puo' "
            "stare in una catena, e il campo 'supera' degli altri non potrebbe puntarlo"
        )

    _data_obbligatoria(rec, "data", "E' la data della valutazione, da cui si contano i giorni.")

    _data_obbligatoria(
        rec, "ipotesi_valide_fino_a",
        "Senza, la valutazione risulterebbe CORRENTE per sempre: una data mancante "
        "non si legge mai come 'nessuna scadenza', perche' e' il modo piu' rapido di "
        "mostrare come buono un lavoro che non lo e' piu'."
    )

    if "supera" not in rec:
        raise ScadenzarioError(
            f"{_etichetta(rec)}: manca il campo 'supera'. Deve esserci sempre, valorizzato "
            f"con l'id della valutazione precedente sulla stessa azienda oppure a null se "
            f"e' la prima: assente, non si distingue una prima valutazione da un anello "
            f"di catena dimenticato"
        )
    supera = rec["supera"]
    if supera is not None and (not isinstance(supera, str) or not supera.strip()):
        raise ScadenzarioError(
            f"{_etichetta(rec)}: il campo 'supera' vale {supera!r}. Ammessi solo null "
            f"(prima valutazione) o l'id del record precedente"
        )

    if not any(str(rec.get(c) or "").strip() for c in CAMPI_IDENTITA):
        raise ScadenzarioError(
            f"{_etichetta(rec)}: nessuno dei campi {', '.join(CAMPI_IDENTITA)} e' valorizzato. "
            f"Un record di valutazione che non dice di quale azienda parla non e' "
            f"associabile a nessuna richiesta"
        )


def valutazioni(records: list) -> list:
    """I soli record di valutazione, validati uno per uno.

    Il filtro e' `tipo: "dossier"` piu' il tag `valutazione`: e' il meccanismo che
    il registro gia' usa per discriminare, deciso perche' la lista dei tipi e'
    chiusa e non si allarga per un vantaggio semantico.
    """
    scelti = []
    for rec in records:
        if rec.get("tipo") != TIPO_VALUTAZIONE:
            continue
        tag = rec.get("tag") or []
        if not isinstance(tag, list) or TAG_VALUTAZIONE not in tag:
            continue
        _valida_valutazione(rec)
        scelti.append(rec)
    return scelti


# --------------------------------------------------------------------------- #
# La catena
# --------------------------------------------------------------------------- #

def _identita(rec: dict) -> set:
    """Le chiavi con cui il record risponde a una richiesta, normalizzate."""
    chiavi = set()
    for campo in CAMPI_IDENTITA:
        valore = str(rec.get(campo) or "").strip().casefold()
        if valore:
            chiavi.add(valore)
    return chiavi


def ultima_della_catena(records: list) -> tuple:
    """L'ultimo record della catena costruita seguendo `supera`, e la catena.

    Ritorna `(record, [id dal piu' vecchio al piu' recente])`.

    **Non e' il piu' recente per data, ed e' il punto di questa funzione.** La
    testa della catena e' il record che nessun altro dichiara di superare. Se le
    teste sono zero (la catena si chiude ad anello), piu' di una (due catene
    scollegate), o se un anello punta a un id che non esiste, non c'e' un ultimo:
    c'e' un registro incoerente, e si solleva un errore invece di scegliere.
    """
    per_id = {r["id"]: r for r in records}
    if len(per_id) != len(records):
        visti, doppi = set(), set()
        for r in records:
            if r["id"] in visti:
                doppi.add(r["id"])
            visti.add(r["id"])
        raise ScadenzarioError(
            f"id duplicato fra le valutazioni della stessa azienda: {', '.join(sorted(doppi))}"
        )

    superato_da = {}
    for r in records:
        precedente = r.get("supera")
        if precedente is None:
            continue
        if precedente not in per_id:
            raise ScadenzarioError(
                f"record '{r['id']}': il campo 'supera' punta a '{precedente}', che fra le "
                f"valutazioni di questa azienda non esiste. La catena e' rotta e l'ultima "
                f"valutazione non e' determinabile"
            )
        if precedente in superato_da:
            raise ScadenzarioError(
                f"due record dichiarano di superare '{precedente}': '{superato_da[precedente]}' "
                f"e '{r['id']}'. La catena si biforca e non esiste un ultimo anello"
            )
        superato_da[precedente] = r["id"]

    teste = [r for r in records if r["id"] not in superato_da]
    if not teste:
        raise ScadenzarioError(
            "nessuna valutazione senza successore: la catena costruita con 'supera' si "
            "chiude ad anello. Non esiste un ultimo record"
        )
    if len(teste) > 1:
        nomi = ", ".join(sorted(f"'{t['id']}'" for t in teste))
        raise ScadenzarioError(
            f"per la stessa azienda ci sono {len(teste)} catene scollegate, con teste {nomi}. "
            f"Manca un 'supera' fra loro, e quale sia l'ultima valutazione non si indovina"
        )

    testa = teste[0]
    catena, corrente = [], testa
    while corrente is not None:
        catena.append(corrente["id"])
        precedente = corrente.get("supera")
        corrente = per_id[precedente] if precedente else None

    if len(catena) != len(records):
        fuori = sorted(set(per_id) - set(catena))
        raise ScadenzarioError(
            f"{len(fuori)} valutazioni di questa azienda restano fuori dalla catena "
            f"({', '.join(fuori)}): sono collegate ad anello fra loro e non risalgono alla testa"
        )

    catena.reverse()
    return testa, catena


# --------------------------------------------------------------------------- #
# Lo stato
# --------------------------------------------------------------------------- #

def _classifica(rec: dict, oggi: date, riesame: int, scadenza: int) -> tuple:
    """Lo stato dell'ultima valutazione e il motivo, in una riga.

    Ritorna `(stato, motivo, data, giorni, valide_fino_a)`.
    """
    data_val = _data_obbligatoria(rec, "data", "")
    valide = _data_obbligatoria(rec, "ipotesi_valide_fino_a", "")

    if data_val > oggi:
        raise ScadenzarioError(
            f"record '{rec['id']}': la valutazione e' datata {_in_lettere(data_val)}, dopo la "
            f"data di riferimento {_in_lettere(oggi)}. I giorni trascorsi sarebbero negativi e "
            f"lo stato risulterebbe CORRENTE per costruzione"
        )

    giorni = (oggi - data_val).days
    quando = f"ultima valutazione {_in_lettere(data_val)}, {_giorni(giorni)}"

    scaduta_per_ipotesi = valide < oggi
    scaduta_per_eta = giorni > scadenza

    if scaduta_per_ipotesi and scaduta_per_eta:
        motivo = (f"{quando}, oltre i {scadenza} giorni, e ipotesi valide fino al "
                  f"{_in_lettere(valide)}, superate da {_giorni((oggi - valide).days)}")
        stato = SCADUTA
    elif scaduta_per_ipotesi:
        motivo = (f"ipotesi valide fino al {_in_lettere(valide)}, superate da "
                  f"{_giorni((oggi - valide).days)}, pur essendo la valutazione di soli "
                  f"{_giorni(giorni)} — la scadenza dichiarata vince sui {scadenza} giorni")
        stato = SCADUTA
    elif scaduta_per_eta:
        motivo = (f"{quando}, oltre i {scadenza} giorni della rivalutazione piena; "
                  f"ipotesi valide fino al {_in_lettere(valide)}")
        stato = SCADUTA
    elif giorni > riesame:
        motivo = (f"{quando}, oltre i {riesame} giorni del riesame leggero e entro i "
                  f"{scadenza} della rivalutazione piena")
        stato = DA_RIESAMINARE
    else:
        motivo = (f"{quando}, entro i {riesame} giorni; ipotesi valide fino al "
                  f"{_in_lettere(valide)}")
        stato = CORRENTE

    return stato, motivo, data_val, giorni, valide


# --------------------------------------------------------------------------- #
# API principale
# --------------------------------------------------------------------------- #

def scadenzario(percorso, aziende, oggi: Optional[date] = None,
                riesame: int = SOGLIA_RIESAME,
                scadenza: int = SOGLIA_SCADENZA) -> list:
    """Lo stato di ciascuna azienda richiesta, nell'ordine in cui e' stata chiesta.

    `aziende` e' un elenco di nomi o ticker. `oggi` di default e' la data odierna
    di sistema; passarla esplicitamente rende l'esito riproducibile, ed e' il modo
    in cui la prova di riferimento lo verifica.

    Solleva ScadenzarioError se il registro non e' leggibile, se un record di
    valutazione e' malformato o se una catena e' incoerente.
    """
    if oggi is None:
        oggi = date.today()

    if riesame <= 0 or scadenza <= 0:
        raise ScadenzarioError("le soglie si esprimono in giorni interi positivi")
    if scadenza <= riesame:
        raise ScadenzarioError(
            f"soglia di scadenza ({scadenza} giorni) non oltre quella di riesame "
            f"({riesame}): lo stato DA RIESAMINARE non potrebbe mai verificarsi, e "
            f"il riesame leggero sparirebbe senza dirlo"
        )

    richieste = [str(a).strip() for a in aziende if str(a).strip()]
    if not richieste:
        raise ScadenzarioError(
            "nessuna azienda richiesta: un elenco vuoto in ingresso produrrebbe un "
            "elenco vuoto in uscita, che si legge come 'niente da aggiornare'"
        )

    tutte = valutazioni(leggi_registro(percorso))

    esiti = []
    for richiesta in richieste:
        chiave = richiesta.casefold()
        trovati = [r for r in tutte if chiave in _identita(r)]

        if not trovati:
            esiti.append(Esito(
                richiesta=richiesta,
                stato=MAI_VALUTATA,
                motivo=(f"nessun record di valutazione per «{richiesta}» nel registro, che "
                        f"e' stato letto e ne contiene {len(tutte)} in tutto"),
            ))
            continue

        ultima, catena = ultima_della_catena(trovati)
        stato, motivo, data_val, giorni, valide = _classifica(ultima, oggi, riesame, scadenza)

        if len(catena) > 1:
            motivo += f"; ultima di una catena di {len(catena)} valutazioni"

        esiti.append(Esito(
            richiesta=richiesta,
            stato=stato,
            motivo=motivo,
            id_ultima=ultima["id"],
            data_ultima=data_val,
            giorni=giorni,
            ipotesi_valide_fino_a=valide,
            esercizio_di_riferimento=ultima.get("esercizio_di_riferimento"),
            azienda=ultima.get("azienda") or ultima.get("ticker"),
            catena=catena,
        ))

    return esiti


# --------------------------------------------------------------------------- #
# Riga di comando
# --------------------------------------------------------------------------- #

def _come_testo(esiti: list, oggi: date, riesame: int, scadenza: int) -> str:
    righe = [
        "=" * 74,
        "  SCADENZARIO DELLE VALUTAZIONI",
        f"  data di riferimento {_in_lettere(oggi)} · soglie: riesame {riesame} giorni, "
        f"scadenza {scadenza}",
        "=" * 74,
    ]
    for e in esiti:
        righe.append("")
        intestazione = e.richiesta
        if e.azienda and e.azienda.strip().casefold() != e.richiesta.casefold():
            intestazione += f"  ({e.azienda})"
        righe.append(intestazione)
        righe.append(f"  stato     {e.stato} — {e.motivo}")
        if e.id_ultima:
            righe.append(f"  record    {e.id_ultima}")
            esercizio = e.esercizio_di_riferimento
            righe.append(
                f"  ipotesi   valide fino al {_in_lettere(e.ipotesi_valide_fino_a)} · "
                f"esercizio di riferimento {esercizio if esercizio is not None else 'non dichiarato'}"
            )
            if len(e.catena) > 1:
                righe.append(f"  catena    {' -> '.join(e.catena)}")
    righe.append("")
    return "\n".join(righe)


def _come_json(esiti: list) -> str:
    def riga(e: Esito) -> dict:
        return {
            "richiesta": e.richiesta,
            "azienda": e.azienda,
            "stato": e.stato,
            "motivo": e.motivo,
            "id_ultima": e.id_ultima,
            "data_ultima": e.data_ultima.isoformat() if e.data_ultima else None,
            "giorni": e.giorni,
            "ipotesi_valide_fino_a": (e.ipotesi_valide_fino_a.isoformat()
                                      if e.ipotesi_valide_fino_a else None),
            "esercizio_di_riferimento": e.esercizio_di_riferimento,
            "catena": e.catena,
        }
    return json.dumps([riga(e) for e in esiti], ensure_ascii=False, indent=2)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        description="Scadenzario delle valutazioni: legge il registro e classifica "
                    "ogni azienda nei quattro stati. Sola lettura."
    )
    p.add_argument("--registro", required=True, help="percorso del ledger.jsonl")
    p.add_argument("--aziende", required=True, nargs="+",
                   help="nomi, ticker o ISIN delle aziende da classificare")
    p.add_argument("--oggi", help="data di riferimento AAAA-MM-GG (default: oggi)")
    p.add_argument("--riesame", type=int, default=SOGLIA_RIESAME,
                   help=f"soglia del riesame leggero in giorni (default {SOGLIA_RIESAME})")
    p.add_argument("--scadenza", type=int, default=SOGLIA_SCADENZA,
                   help=f"soglia della rivalutazione piena in giorni (default {SOGLIA_SCADENZA})")
    p.add_argument("--json", action="store_true", help="uscita in JSON invece che a video")
    args = p.parse_args(argv)

    if args.oggi:
        try:
            oggi = datetime.strptime(args.oggi.strip(), "%Y-%m-%d").date()
        except ValueError:
            sys.exit(f"scadenzario: --oggi vale {args.oggi!r}, che non e' una data AAAA-MM-GG")
    else:
        oggi = date.today()

    try:
        esiti = scadenzario(args.registro, args.aziende, oggi=oggi,
                            riesame=args.riesame, scadenza=args.scadenza)
    except ScadenzarioError as ex:
        # Un errore non e' uno stato: non si stampa una tabella parziale accanto.
        sys.exit(f"scadenzario: {ex}")

    print(_come_json(esiti) if args.json else _come_testo(esiti, oggi, args.riesame, args.scadenza))
    return 0


if __name__ == "__main__":
    sys.exit(main())
