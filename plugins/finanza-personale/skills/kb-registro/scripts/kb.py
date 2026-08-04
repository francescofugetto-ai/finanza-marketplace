#!/usr/bin/env python3
"""
kb.py — registro decisionale della knowledge base finanziaria.

Nessuna dipendenza esterna. Sorgente di verita: KB_ROOT/ledger.jsonl (append-only).

Uso:
  kb.py init                                   crea la struttura in KB_ROOT
  kb.py add --file record.json                 valida e appende un record
  kb.py add --stdin                            idem, leggendo da stdin
  kb.py stato [--soggetto X] [--out FILE]      rigenera la vista (STATO-ATTUALE.md,
                                               oppure STATO-<soggetto>.md con --soggetto)
  kb.py query [filtri]                         interroga il registro (output compatto)
  kb.py scaduti                                record time-sensitive oltre scadenza ancora 'vigente'
  kb.py audit [--mesi 12]                      conteggio verdetti + guardia anti-deriva
  kb.py viste                                  rigenera TUTTE le viste in un colpo
  kb.py grafo [--out graph.json]               esporta il grafo delle relazioni

KB_ROOT: variabile d'ambiente, oppure --kb, oppure la cartella corrente.
"""

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta

LEDGER = "ledger.jsonl"
STATO = "STATO-ATTUALE.md"


def nome_vista(soggetto=None):
    """Nome del file della vista.

    Con --soggetto il file prende il nome del soggetto. Serve a mantenere la
    promessa della separazione dei mandati: finche' tutte le viste finivano in
    STATO-ATTUALE.md, generare quella dei genitori dopo quella di un cliente
    sovrascriveva la prima, e nel progetto sbagliato finiva il soggetto
    sbagliato senza che nulla lo segnalasse. Il nome del file e' l'unico
    punto in cui quell'errore diventa visibile prima del caricamento.
    """
    if not soggetto:
        return STATO
    pulito = re.sub(r"[^A-Za-z0-9._-]", "-", str(soggetto)).strip("-") or "senza-nome"
    return f"STATO-{pulito}.md"

VERDETTI = ("AZIONE", "OSSERVATO", "CONTESTO", "RUMORE")
TIPI = ("action-plan", "revisione-pac", "distillato", "dossier", "canone", "nota",
        "snapshot")
STATI = ("vigente", "superato", "scaduto", "archiviato")


# ---------------------------------------------------------------- utilities

def kb_root(args):
    root = getattr(args, "kb", None) or os.environ.get("KB_ROOT") or os.getcwd()
    return os.path.abspath(root)


def parse_date(s, field):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        raise ValueError(f"campo '{field}': data non valida ({s!r}), atteso AAAA-MM-GG")


def load(root):
    path = os.path.join(root, LEDGER)
    if not os.path.exists(path):
        return []
    out = []
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError as e:
                sys.exit(f"ledger.jsonl riga {n}: JSON non valido — {e}")
    out.sort(key=lambda r: (r.get("data", ""), r.get("id", "")))
    return out


def save(root, records):
    path = os.path.join(root, LEDGER)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False, sort_keys=False) + "\n")
    os.replace(tmp, path)


def effective_state(rec, today=None):
    """Stato reale al giorno d'oggi: 'scaduto' vince su 'vigente' se la data e' passata."""
    today = today or date.today()
    st = rec.get("stato", "vigente")
    if st != "vigente":
        return st
    scade = rec.get("scade")
    if scade and parse_date(scade, "scade") < today:
        return "scaduto"
    return "vigente"


def active_constraints(records, today=None):
    """Vincoli ancora attivi, con il record che li ha generati."""
    today = today or date.today()
    out = []
    for r in records:
        if effective_state(r, today) != "vigente":
            continue
        for v in r.get("vincoli", []) or []:
            sc = v.get("scade")
            if sc and parse_date(sc, "vincoli.scade") < today:
                continue
            out.append((r, v))
    return out


def fmt_num(v):
    """Numeri leggibili nella vista, senza fingere precisione che non c'e'."""
    if v is None:
        return "—"
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return str(v)
    if float(v).is_integer() and abs(v) < 1e6:
        return f"{int(v):,}".replace(",", ".")
    if abs(v) >= 1000:
        return f"{v:,.2f}".replace(",", "~").replace(".", ",").replace("~", ".")
    return f"{v:g}".replace(".", ",")


def fmt_pct(v):
    """Accetta sia 0.486 sia 48.6 e rende sempre una percentuale."""
    if v is None:
        return "—"
    try:
        x = float(v)
    except (TypeError, ValueError):
        return str(v)
    if abs(x) <= 1.0:
        x *= 100
    return f"{x:.1f}%".replace(".", ",")


def dedup_vincoli(coppie):
    """Un vincolo confermato da piu' documenti e' UN vincolo, non tre.

    Prima la vista elencava una riga per ogni record che lo citava: il sigillo
    compariva due volte con descrizioni diverse, e chi leggeva doveva decidere
    quale valesse. Ora vince la formulazione del record piu' recente e si conta
    quante volte e' stato confermato — che e' un'informazione utile, non rumore.
    """
    per_nome = {}
    for r, v in coppie:
        nome = (v.get("nome") or "").strip().lower() or id(v)
        prec = per_nome.get(nome)
        if prec is None or (r["data"], r["id"]) > (prec[0]["data"], prec[0]["id"]):
            per_nome[nome] = (r, v, (prec[2] + 1) if prec else 1)
        else:
            per_nome[nome] = (prec[0], prec[1], prec[2] + 1)
    return sorted(per_nome.values(), key=lambda x: (x[1].get("scade") or "9999", x[0]["id"]))


def open_triggers(records, today=None):
    today = today or date.today()
    out = []
    for r in records:
        if effective_state(r, today) != "vigente":
            continue
        for t in r.get("trigger", []) or []:
            out.append((r, t))
    return out


# ---------------------------------------------------------------- validation

REQUIRED = ("id", "data", "layer", "soggetto", "tipo", "titolo", "file",
            "verdetto", "decisione", "classe", "scade", "tag", "condivisibile")


def validate(rec, existing_ids):
    errs = []
    for f in REQUIRED:
        if f not in rec:
            errs.append(f"campo obbligatorio mancante: '{f}'")
    if errs:
        return errs

    if rec["id"] in existing_ids:
        errs.append(f"id duplicato: {rec['id']}")
    try:
        parse_date(rec["data"], "data")
    except ValueError as e:
        errs.append(str(e))

    if rec["layer"] not in ("dottrina", "mandato"):
        errs.append("layer deve essere 'dottrina' o 'mandato'")
    if rec["tipo"] not in TIPI:
        errs.append(f"tipo non ammesso: {rec['tipo']} (ammessi: {', '.join(TIPI)})")
    if rec["verdetto"] not in VERDETTI and rec["verdetto"] is not None:
        errs.append(f"verdetto non ammesso: {rec['verdetto']}")
    if rec["classe"] not in ("timeless", "time-sensitive"):
        errs.append("classe deve essere 'timeless' o 'time-sensitive'")

    if rec["classe"] == "time-sensitive" and not rec.get("scade"):
        errs.append("classe 'time-sensitive' richiede 'scade' (regola anti-forecast-zombie)")
    if rec.get("scade"):
        try:
            parse_date(rec["scade"], "scade")
        except ValueError as e:
            errs.append(str(e))

    if rec["verdetto"] == "AZIONE" and not (rec.get("vincoli") or rec.get("trigger")):
        errs.append("verdetto AZIONE senza alcun 'vincolo' o 'trigger' datato: "
                    "se non e' scrivibile con soglia e data, non era un'azione")

    if not isinstance(rec.get("decisione"), str) or "\n" in rec.get("decisione", ""):
        errs.append("'decisione' deve essere una stringa su una sola riga")
    if not rec.get("tag"):
        errs.append("almeno un tag e' obbligatorio")

    if rec["layer"] == "dottrina" and rec.get("condivisibile") is not True:
        errs.append("layer 'dottrina' implica condivisibile=true")

    for t in rec.get("trigger", []) or []:
        if not t.get("soglia") or not t.get("riverifica"):
            errs.append(f"trigger senza soglia o data di riverifica: {t}")

    for sid in rec.get("supersedes", []) or []:
        if sid not in existing_ids:
            errs.append(f"supersedes punta a un id inesistente: {sid}")

    # --- posizioni: lo snapshot del portafoglio come dato di prima classe ----
    #
    # Finche' lo snapshot stava nelle istruzioni di progetto, andava riscritto a
    # mano a ogni movimento e invecchiava in silenzio. Qui e' un record datato
    # come tutti gli altri: la vista lo rende, la data e' quella del record, e
    # una versione superata si chiude con `supersedes` invece di essere
    # sovrascritta senza traccia.
    pos = rec.get("posizioni")
    if pos is not None:
        if not isinstance(pos, list) or not pos:
            errs.append("'posizioni' deve essere una lista non vuota")
        else:
            somma = 0.0
            for i, x in enumerate(pos):
                if not isinstance(x, dict):
                    errs.append(f"posizioni[{i}] non e' un oggetto"); continue
                for campo in ("gamba", "isin", "peso"):
                    if x.get(campo) in (None, ""):
                        errs.append(f"posizioni[{i}] manca '{campo}'")
                isin = str(x.get("isin", ""))
                if isin and not isin_ben_formato(isin):
                    errs.append(f"posizioni[{i}] ISIN malformato: {isin}")
                try:
                    somma += float(x.get("peso") or 0)
                except (TypeError, ValueError):
                    errs.append(f"posizioni[{i}] peso non numerico: {x.get('peso')}")
            # I pesi devono chiudere: un portafoglio che somma a 0,93 non e' un
            # portafoglio, e' una tabella con una riga dimenticata.
            if abs(somma - 1.0) > 0.005 and abs(somma - 100.0) > 0.5:
                errs.append(
                    f"i pesi delle posizioni sommano a {somma:.4f}: devono chiudere "
                    f"a 1.0 (frazioni) o a 100 (percentuali), tolleranza 0,5 pt")
        if rec.get("tipo") != "snapshot":
            errs.append("un record con 'posizioni' deve avere tipo='snapshot'")
        if rec.get("classe") != "time-sensitive" or not rec.get("scade"):
            errs.append(
                "uno snapshot e' time-sensitive per definizione: serve 'classe':"
                "'time-sensitive' e una data 'scade' (la data oltre la quale va "
                "richiesto un aggiornamento, non oltre la quale il portafoglio sparisce)")
    elif rec.get("tipo") == "snapshot":
        errs.append("tipo='snapshot' richiede il campo 'posizioni'")
    return errs


def isin_ben_formato(v):
    """Formato + cifra di controllo (Luhn su base 36). Stessa regola del connettore:
    intercetta un ISIN trascritto male prima che entri in una vista."""
    s = re.sub(r"[\s.\-]", "", str(v)).upper()
    if not re.match(r"^[A-Z]{2}[A-Z0-9]{9}[0-9]$", s):
        return False
    cifre = "".join(str(int(c, 36)) if c.isalpha() else c for c in s[:-1])
    tot, raddoppia = 0, True
    for c in reversed(cifre):
        n = int(c)
        if raddoppia:
            n *= 2
            if n > 9:
                n -= 9
        tot += n
        raddoppia = not raddoppia
    return (10 - tot % 10) % 10 == int(s[-1])


# ---------------------------------------------------------------- commands

def cmd_init(args):
    root = kb_root(args)
    for d in ("reports",):
        os.makedirs(os.path.join(root, d), exist_ok=True)
    path = os.path.join(root, LEDGER)
    if not os.path.exists(path):
        open(path, "w", encoding="utf-8").close()
    print(f"KB inizializzata in {root}")


def cmd_add(args):
    root = kb_root(args)
    raw = sys.stdin.read() if args.stdin else open(args.file, encoding="utf-8").read()
    try:
        rec = json.loads(raw)
    except json.JSONDecodeError as e:
        sys.exit(f"record non e' JSON valido: {e}")

    records = load(root)
    ids = {r["id"] for r in records}
    errs = validate(rec, ids)
    if errs:
        print("RECORD RIFIUTATO:", file=sys.stderr)
        for e in errs:
            print("  - " + e, file=sys.stderr)
        sys.exit(1)

    rec.setdefault("stato", "vigente")
    rec.setdefault("supersedes", [])
    rec.setdefault("superato_da", None)
    rec.setdefault("vincoli", [])
    rec.setdefault("trigger", [])
    rec.setdefault("numeri", {})

    by_id = {r["id"]: r for r in records}
    for sid in rec["supersedes"]:
        by_id[sid]["stato"] = "superato"
        by_id[sid]["superato_da"] = rec["id"]

    records.append(rec)
    save(root, records)
    print(f"registrato: {rec['id']}  ({rec['tipo']} · {rec['verdetto'] or '—'})")
    if rec["supersedes"]:
        print("  supera: " + ", ".join(rec["supersedes"]))
    print("  ora rigenera la vista:  kb.py stato")


def _fmt_rec(r, today):
    v = r.get("verdetto") or "—"
    sc = f" · scade {r['scade']}" if r.get("scade") else ""
    return (f"- [{r['data']}] ({r['tipo']}/{v}) {r['titolo']}\n"
            f"  → {r['decisione']}{sc}\n"
            f"  id: {r['id']}" + (f" · file: {r['file']}" if r.get("file") else ""))


def cmd_query(args):
    root = kb_root(args)
    today = date.today()
    recs = load(root)
    out = []
    for r in recs:
        st = effective_state(r, today)
        if args.vigenti and st != "vigente":
            continue
        if args.soggetto and r.get("soggetto") != args.soggetto and r.get("layer") != "dottrina":
            continue
        if args.layer and r.get("layer") != args.layer:
            continue
        if args.tipo and r.get("tipo") != args.tipo:
            continue
        if args.verdetto and r.get("verdetto") != args.verdetto:
            continue
        if args.tag and not set(args.tag) & set(r.get("tag", [])):
            continue
        if args.dal and r["data"] < args.dal:
            continue
        if args.al and r["data"] > args.al:
            continue
        out.append(r)

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return
    if not out:
        print("nessun record corrisponde ai filtri.")
        return
    print(f"{len(out)} record\n")
    for r in out:
        print(_fmt_rec(r, today))
        print()


def cmd_scaduti(args):
    root = kb_root(args)
    today = date.today()
    recs = load(root)
    stale = [r for r in recs
             if r.get("stato") == "vigente" and r.get("scade")
             and parse_date(r["scade"], "scade") < today]
    soon = [r for r in recs
            if effective_state(r, today) == "vigente" and r.get("scade")
            and today <= parse_date(r["scade"], "scade") <= today + timedelta(days=60)]

    if stale:
        print(f"SCADUTI ma ancora marcati 'vigente' ({len(stale)}):")
        for r in stale:
            print(f"  - {r['id']} — scaduto il {r['scade']} — {r['titolo']}")
        print("\n  Vanno chiusi: o si rinnova la scadenza con un nuovo record, o si accetta che")
        print("  la tesi sia decaduta. Un forecast che sopravvive alla sua data e' rumore.\n")
    else:
        print("nessun record scaduto rimasto aperto.\n")

    if soon:
        print(f"In scadenza nei prossimi 60 giorni ({len(soon)}):")
        for r in soon:
            print(f"  - {r['id']} — {r['scade']} — {r['titolo']}")

    for r, v in active_constraints(recs, today):
        sc = v.get("scade")
        if sc and today <= parse_date(sc, "v") <= today + timedelta(days=60):
            print(f"  ! vincolo in scadenza: {v['nome']} ({sc}) da {r['id']}")


def cmd_audit(args):
    root = kb_root(args)
    today = date.today()
    cutoff = (today - timedelta(days=30 * args.mesi)).isoformat()
    recs = [r for r in load(root) if r["data"] >= cutoff]

    per_verdetto = Counter(r.get("verdetto") or "—" for r in recs)
    per_soggetto = Counter(r.get("soggetto") for r in recs)
    print(f"Finestra: ultimi {args.mesi} mesi (dal {cutoff}) — {len(recs)} documenti\n")
    print("Per verdetto:")
    for k in list(VERDETTI) + ["—"]:
        if per_verdetto.get(k):
            print(f"  {k:10s} {per_verdetto[k]:3d}")
    print("\nPer soggetto:")
    for k, n in per_soggetto.most_common():
        print(f"  {str(k):20s} {n:3d}")

    azioni = per_verdetto.get("AZIONE", 0)
    print()
    if azioni > 2:
        print(f"⚠ GUARDIA ANTI-DERIVA: {azioni} verdetti AZIONE in {args.mesi} mesi.")
        print("  L'ipotesi da privilegiare e' che il filtro si sia allentato, non che il")
        print("  mondo sia cambiato. Rileggi i test di persistenza dei documenti sopra soglia")
        print("  e verifica quale test avrebbe dovuto fermarli.")
    else:
        print(f"Verdetti AZIONE: {azioni} — entro la soglia (max 2 per finestra). Il filtro tiene.")

    ripetuti = Counter()
    for r in recs:
        for t in r.get("tag", []):
            ripetuti[t] += 1
    caldi = [(t, n) for t, n in ripetuti.most_common(5) if n >= 3]
    if caldi:
        print("\nTemi ricorrenti (≥3 occorrenze): una tesi che torna non e' piu' forte, e' piu' prezzata.")
        for t, n in caldi:
            print(f"  {t}: {n}")


def cmd_stato(args):
    root = kb_root(args)
    today = date.today()
    recs = load(root)
    vig = [r for r in recs if effective_state(r, today) == "vigente"]

    tutti_soggetti = sorted({r["soggetto"] for r in vig if r["layer"] == "mandato"})
    soggetti = list(tutti_soggetti)
    if args.soggetto:
        soggetti = [s for s in soggetti if s == args.soggetto]
        if not soggetti:
            # Una vista vuota e' peggio di nessuna vista: caricata in un progetto
            # sembra "nessun vincolo attivo" invece di "soggetto sbagliato".
            noti = ", ".join(tutti_soggetti) or "(nessuno)"
            sys.exit(
                f"errore: nessun record vigente di livello 'mandato' per il soggetto "
                f"'{args.soggetto}'.\n"
                f"       soggetti presenti nel registro: {noti}\n"
                f"       non scrivo una vista vuota: verrebbe letta come "
                f"'nessun vincolo attivo'."
            )

    L = []
    L.append("# Stato attuale della knowledge base")
    L.append("")
    L.append(f"> Vista **generata** da `kb.py stato` il {today.isoformat()}. Non modificare a mano.")
    if args.soggetto:
        L.append(">")
        L.append(f"> **Ambito: soggetto `{args.soggetto}`.** Questa vista contiene il livello "
                 f"`dottrina` e il solo mandato di `{args.soggetto}`. Non caricarla in un "
                 f"progetto che riguarda un altro soggetto.")
    L.append("> Contiene solo cio' che e' **vigente oggi**: i record superati o scaduti sono")
    L.append("> nel registro, non qui. Per il dettaglio storico: `kb.py query`.")
    L.append("")
    L.append(f"Registro: {len(recs)} documenti · {len(vig)} vigenti · "
             f"{len(recs) - len(vig)} superati/scaduti/archiviati")
    L.append("")

    # --- dottrina, leggibile da tutti i progetti
    dott = [r for r in vig if r["layer"] == "dottrina"]
    L.append("---")
    L.append("")
    L.append("## Livello dottrina — leggibile da qualunque progetto")
    L.append("")
    if not dott:
        L.append("_Nessun record di dottrina._")
    for r in sorted(dott, key=lambda r: r["data"], reverse=True):
        L.append(f"- **{r['titolo']}** ({r['data']}, `{r['id']}`)  ")
        L.append(f"  {r['decisione']}  ")
        L.append(f"  tag: {', '.join(r.get('tag', []))}")
    L.append("")

    # --- mandati
    for s in soggetti:
        rs = [r for r in vig if r["layer"] == "mandato" and r["soggetto"] == s]
        L.append("---")
        L.append("")
        L.append(f"## Mandato: {s}")
        L.append("")
        L.append("> Sezione **riservata a questo soggetto**. Non usarla in un progetto diverso.")
        L.append("")

        # --- snapshot: la fonte unica dei numeri di portafoglio ------------
        #
        # Si guarda l'INTERO registro, non solo i record ancora "vigenti" per
        # data. Uno snapshot oltre la sua data di rinfresco non deve sparire
        # dalla vista: sparendo, il progetto non direbbe "questi numeri sono
        # vecchi" ma "non ho numeri", e la differenza fra le due cose e' tutta.
        # Restano fuori solo quelli chiusi a mano (superati o archiviati).
        snaps = [r for r in recs
                 if r["layer"] == "mandato" and r["soggetto"] == s
                 and r.get("posizioni")
                 and r.get("stato", "vigente") == "vigente"
                 and not r.get("superato_da")]
        L.append("### Snapshot del portafoglio — fonte unica dei numeri")
        L.append("")
        if not snaps:
            L.append("> **Nessuno snapshot registrato per questo soggetto.**")
            L.append("> Non ricostruire i pesi da report allegati o da conversazioni "
                     "precedenti: chiedi lo snapshot corrente e registralo con "
                     "`kb.py add`.")
            L.append("")
        else:
            snap = sorted(snaps, key=lambda r: (r["data"], r["id"]), reverse=True)[0]
            eta = (today - parse_date(snap["data"], "data")).days
            rinfresco = snap.get("scade")
            oltre = bool(rinfresco and parse_date(rinfresco, "scade") < today)
            L.append(f"**Aggiornato al {snap['data']}** · {eta} giorni fa · "
                     f"origine `{snap['id']}`"
                     + (f" · da rinfrescare entro {rinfresco}" if rinfresco else ""))
            L.append("")
            if oltre:
                L.append(f"> **SNAPSHOT SCADUTO** — doveva essere rinfrescato entro "
                         f"{rinfresco} e ha {eta} giorni. I numeri qui sotto sono "
                         f"l'ultima fotografia nota, **non la situazione corrente**. "
                         f"Dichiaralo in apertura del documento e chiedi i numeri "
                         f"aggiornati prima di quantificare un impatto, proporre "
                         f"un'operazione o calcolare un rendimento atteso.")
                L.append("")
            elif eta > 45:
                L.append(f"> Lo snapshot ha {eta} giorni: usabile, ma dichiara la data "
                         f"in apertura del documento.")
                L.append("")
            tot = snap.get("totali") or {}
            if tot:
                righe = []
                for k, etichetta in (("valore_mercato_eur", "Valore di mercato"),
                                     ("carico_eur", "Carico"),
                                     ("pl_eur", "P&L"),
                                     ("pl_pct", "P&L %")):
                    if tot.get(k) is not None:
                        righe.append(f"{etichetta} **{fmt_num(tot[k])}**")
                if righe:
                    L.append(" · ".join(righe))
                    L.append("")
            L.append("| Gamba | ISIN | Ticker | Quote | Valore | Peso |")
            L.append("|---|---|---|---:|---:|---:|")
            for x in snap["posizioni"]:
                L.append(
                    f"| {x.get('gamba','')} | `{x.get('isin','')}` | "
                    f"{x.get('ticker','') or '—'} | {fmt_num(x.get('quote'))} | "
                    f"{fmt_num(x.get('valore_eur'))} | {fmt_pct(x.get('peso'))} |")
            L.append("")
            agg = snap.get("aggregati") or {}
            if agg:
                L.append("Aggregati: " + " · ".join(
                    f"{k.replace('_',' ')} **{fmt_num(v)}**" for k, v in agg.items()))
                L.append("")
            piano = snap.get("piano") or {}
            if piano:
                testa = []
                if piano.get("importo_mensile_eur") is not None:
                    testa.append(f"**{fmt_num(piano['importo_mensile_eur'])} EUR/mese**")
                if piano.get("giorno"):
                    testa.append(f"esecuzione il {piano['giorno']}")
                L.append("**Piano di accumulo** — " + " · ".join(testa) if testa
                         else "**Piano di accumulo**")
                L.append("")
                if piano.get("righe"):
                    L.append("| Strumento | ISIN | Quote | Importo |")
                    L.append("|---|---|---:|---:|")
                    for x in piano["righe"]:
                        L.append(f"| {x.get('gamba','')} | `{x.get('isin','')}` | "
                                 f"{fmt_num(x.get('quote'))} | "
                                 f"{fmt_num(x.get('importo_eur'))} |")
                    L.append("")
                if piano.get("note"):
                    L.append(f"> {piano['note']}")
                    L.append("")
            if len(snaps) > 1:
                L.append(f"_Nel registro ci sono {len(snaps)} snapshot vigenti per questo "
                         f"soggetto: qui e' reso il piu' recente. Chiudi i superati con "
                         f"`supersedes`._")
                L.append("")

        vincoli = dedup_vincoli(active_constraints(rs, today))
        L.append("### Vincoli attivi")
        L.append("")
        if not vincoli:
            L.append("_Nessun vincolo attivo._")
        else:
            L.append("| Vincolo | Descrizione | Scade | Origine |")
            L.append("|---|---|---|---|")
            for r, v, n_conf in vincoli:
                conferme = f" · confermato {n_conf}x" if n_conf > 1 else ""
                L.append(f"| **{v.get('nome','—')}** | {v.get('descrizione','')} | "
                         f"{v.get('scade') or 'nessuna'} | `{r['id']}`{conferme} |")
        L.append("")

        trig = open_triggers(rs, today)
        L.append("### Trigger aperti")
        L.append("")
        if not trig:
            L.append("_Nessun trigger aperto._")
        else:
            L.append("| Cosa osservare | Soglia | Fonte | Riverifica | Origine |")
            L.append("|---|---|---|---|---|")
            for r, t in trig:
                L.append(f"| {t.get('cosa','')} | {t.get('soglia','')} | {t.get('fonte','')} | "
                         f"{t.get('riverifica','')} | `{r['id']}` |")
        L.append("")

        L.append("### Ultimi record vigenti")
        L.append("")
        for r in sorted(rs, key=lambda r: r["data"], reverse=True)[:8]:
            v = r.get("verdetto") or "—"
            L.append(f"- `{r['data']}` **{r['titolo']}** — {v}  ")
            L.append(f"  → {r['decisione']}  ")
            if r.get("file"):
                L.append(f"  file: `{r['file']}` · id: `{r['id']}`")
            else:
                L.append(f"  id: `{r['id']}`")
        L.append("")

        # I numeri restano attribuiti al record che li ha prodotti, con la sua
        # data. Fonderli tutti in un dizionario unico produceva una tabella in
        # cui `peso_usa` compariva una volta sola, con il valore dell'ultimo
        # record che l'aveva scritto e senza dire quando: due misure della
        # stessa grandezza a due date diverse si sovrascrivevano in silenzio.
        con_numeri = [r for r in sorted(rs, key=lambda r: r["data"], reverse=True)
                      if r.get("numeri")][:3]
        if con_numeri:
            L.append("### Numeri registrati, per documento")
            L.append("")
            for r in con_numeri:
                L.append(f"**{r['data']}** · `{r['id']}`  ")
                L.append("  " + " · ".join(
                    f"{k}: {fmt_num(v)}" for k, v in r["numeri"].items()))
                L.append("")
            L.append("_Storico completo: `kb.py query --soggetto "
                     f"{s} --vigenti`._")
            L.append("")

    L.append("---")
    L.append("")
    L.append("## Igiene")
    L.append("")
    stale = [r for r in recs if r.get("stato") == "vigente" and r.get("scade")
             and parse_date(r["scade"], "scade") < today]
    L.append(f"- record scaduti ancora aperti nel registro: **{len(stale)}** "
             f"(chiudili con `kb.py scaduti`)")
    anno = [r for r in recs if r["data"] >= (today - timedelta(days=365)).isoformat()]
    az = sum(1 for r in anno if r.get("verdetto") == "AZIONE")
    L.append(f"- verdetti AZIONE negli ultimi 12 mesi: **{az}** "
             + ("— **oltre soglia**, sospetta deriva del filtro" if az > 2 else "— entro soglia"))
    L.append("")

    out = os.path.join(root, getattr(args, "out", None) or nome_vista(args.soggetto))
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    ambito = f"soggetto '{args.soggetto}'" if args.soggetto else "tutti i mandati"
    print(f"scritto {out}  ({len(vig)} record vigenti, {len(soggetti)} mandati, {ambito})")
    if args.soggetto:
        print(f"  vista filtrata: caricala SOLO nel progetto di '{args.soggetto}'.")


def cmd_viste(args):
    """Rigenera la vista globale e una vista per ogni soggetto con mandato.

    Esiste per una ragione sola: la disciplina che dipende dal ricordarsi di
    eseguire due comandi diversi non regge tre mesi. Un comando solo, che scrive
    tutti i file e stampa dove sono andati, regge.
    """
    root = kb_root(args)
    recs = load(root)
    today = date.today()
    vig = [r for r in recs if effective_state(r, today) == "vigente"]
    soggetti = sorted({r["soggetto"] for r in vig if r["layer"] == "mandato"})

    class _A:
        pass

    scritti = []
    a = _A(); a.kb = getattr(args, "kb", None); a.soggetto = None; a.out = None
    cmd_stato(a); scritti.append(nome_vista(None))
    for s in soggetti:
        a = _A(); a.kb = getattr(args, "kb", None); a.soggetto = s; a.out = None
        cmd_stato(a); scritti.append(nome_vista(s))

    print()
    print(f"{len(scritti)} viste rigenerate in {root}:")
    for f in scritti:
        print(f"  {f}")
    if soggetti:
        print()
        print("Carica in ogni progetto SOLO la vista del suo soggetto.")
        print("La riga di ambito in testa al file dice a chi appartiene: se non")
        print("corrisponde al progetto che hai aperto, hai caricato il file sbagliato.")


def cmd_grafo(args):
    root = kb_root(args)
    recs = load(root)
    today = date.today()
    nodes, edges = [], []
    tags = defaultdict(list)

    for r in recs:
        nodes.append({"id": r["id"], "tipo": "documento", "label": r["titolo"],
                      "data": r["data"], "layer": r["layer"], "soggetto": r["soggetto"],
                      "verdetto": r.get("verdetto"), "stato": effective_state(r, today)})
        for sid in r.get("supersedes", []) or []:
            edges.append({"from": r["id"], "to": sid, "rel": "supera"})
        for t in r.get("tag", []):
            tags[t].append(r["id"])
        for v in r.get("vincoli", []) or []:
            nid = f"vincolo:{v.get('nome')}"
            nodes.append({"id": nid, "tipo": "vincolo", "label": v.get("nome"),
                          "scade": v.get("scade"), "soggetto": r["soggetto"]})
            edges.append({"from": r["id"], "to": nid, "rel": "istituisce"})

    for t, ids in tags.items():
        nodes.append({"id": f"tag:{t}", "tipo": "tema", "label": t})
        for i in ids:
            edges.append({"from": i, "to": f"tag:{t}", "rel": "tratta"})

    seen, uniq = set(), []
    for n in nodes:
        if n["id"] in seen:
            continue
        seen.add(n["id"])
        uniq.append(n)

    out = args.out or os.path.join(root, "graph.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump({"generato": today.isoformat(), "nodes": uniq, "edges": edges},
                  fh, ensure_ascii=False, indent=2)
    print(f"scritto {out} — {len(uniq)} nodi, {len(edges)} archi")


# ---------------------------------------------------------------- cli

def main():
    p = argparse.ArgumentParser(description="Registro decisionale della KB finanziaria")
    p.add_argument("--kb", help="percorso KB_ROOT (default: $KB_ROOT o cartella corrente)")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init").set_defaults(fn=cmd_init)

    a = sub.add_parser("add")
    g = a.add_mutually_exclusive_group(required=True)
    g.add_argument("--file")
    g.add_argument("--stdin", action="store_true")
    a.set_defaults(fn=cmd_add)

    s = sub.add_parser("stato")
    s.add_argument("--soggetto")
    s.add_argument("--out", help="nome del file di destinazione (default: "
                                 "STATO-ATTUALE.md, o STATO-<soggetto>.md con --soggetto)")
    s.set_defaults(fn=cmd_stato)

    q = sub.add_parser("query")
    q.add_argument("--soggetto")
    q.add_argument("--layer", choices=["dottrina", "mandato"])
    q.add_argument("--tipo", choices=list(TIPI))
    q.add_argument("--verdetto", choices=list(VERDETTI))
    q.add_argument("--tag", nargs="+")
    q.add_argument("--dal")
    q.add_argument("--al")
    q.add_argument("--vigenti", action="store_true")
    q.add_argument("--json", action="store_true")
    q.set_defaults(fn=cmd_query)

    sub.add_parser("viste").set_defaults(fn=cmd_viste)

    sub.add_parser("scaduti").set_defaults(fn=cmd_scaduti)

    au = sub.add_parser("audit")
    au.add_argument("--mesi", type=int, default=12)
    au.set_defaults(fn=cmd_audit)

    gr = sub.add_parser("grafo")
    gr.add_argument("--out")
    gr.set_defaults(fn=cmd_grafo)

    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
