#!/usr/bin/env python3
"""
test_dcf_engine.py — Prova di riferimento del motore DCF.

CHE COSA PROVA
--------------
Ricostruisce da capo il modello dell'episodio 337 di The Bull su Bending Spoons e
lo confronta, valore per valore, con i numeri pubblicati:

  1. i trenta valori annuali dell'orizzonte esplicito   (tolleranza +/- 0,5 mln)
  2. i cinque aggregati                                  (tolleranza +/- 0,5 mln)
  3. il fair value per azione: 14,14                     (tolleranza +/- 0,01)
  4. tutte e venticinque le celle della sensibilita'     (tolleranza +/- 0,01)
  5. i nove casi limite: errori espliciti dove non esiste un numero
  6. la forma del percorso delle ipotesi: riscalatura degli incrementi,
     ripiego dichiarato, intervallo ammissibile

PERCHE' ESISTE
--------------
Un motore di valutazione sbagliato non si rompe: risponde. Restituisce un numero
plausibile, con la virgola al posto giusto, e nessuno se ne accorge finche' non lo
si confronta con un modello costruito da qualcun altro. Questa prova e' quel
confronto, e va rifatta a ogni modifica del motore.

I valori attesi sono **dati di ingresso della prova**, non risultati da adattare.
Se il motore non li produce, si corregge il motore: mai il valore atteso.

USO
---
    python3 test_dcf_engine.py

Uscita 0 se passa tutto, 1 se anche un solo controllo fallisce.
"""

import sys

# Il motore va importato senza lasciare __pycache__ dentro la skill: la cartella
# del plugin non deve contenere niente di temporaneo, e uno strumento di prova non
# deve sporcare cio' che prova.
sys.dont_write_bytecode = True

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from dcf_engine import (  # noqa: E402
    Bridge, DcfInputs, DcfError, MOTORE_VERSIONE,
    run_dcf, sensitivity,
    reverse_growth, reverse_g_terminal, reverse_wacc, reverse_margin,
)

TOLL_MLN = 0.5
TOLL_AZIONE = 0.01


# --------------------------------------------------------------------------- #
# Infrastruttura di conteggio
# --------------------------------------------------------------------------- #

class Prova:
    def __init__(self):
        self.passati = 0
        self.falliti = []

    def confronta(self, etichetta, atteso, ottenuto, tolleranza):
        ok = ottenuto is not None and abs(ottenuto - atteso) <= tolleranza
        if ok:
            self.passati += 1
        else:
            self.falliti.append((etichetta, atteso, ottenuto, tolleranza))
        return ok

    def afferma(self, etichetta, condizione, dettaglio=""):
        if condizione:
            self.passati += 1
        else:
            self.falliti.append((etichetta, "atteso", dettaglio or "non verificato", 0))
        return condizione

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
            print("  CONTROLLI FALLITI:")
            for etichetta, atteso, ottenuto, toll in self.falliti:
                if isinstance(atteso, float):
                    scarto = abs(ottenuto - atteso) if ottenuto is not None else float("nan")
                    print(f"    - {etichetta}")
                    print(f"        atteso   {atteso:>12.4f}   (tolleranza +/- {toll})")
                    print(f"        ottenuto {ottenuto if ottenuto is None else f'{ottenuto:>12.4f}'}")
                    print(f"        scarto   {scarto:>12.4f}")
                else:
                    print(f"    - {etichetta}: {ottenuto}")
            print()
            print("  Il motore NON e' allineato al modello di riferimento.")
            print("  Si corregge il motore, mai il valore atteso.")
            return 1
        print()
        print("  Il motore riproduce il modello di riferimento in ogni sua parte.")
        return 0


# --------------------------------------------------------------------------- #
# 3.1 · Gli input della prova
# --------------------------------------------------------------------------- #

def input_base(**modifiche):
    """Il caso Bending Spoons dell'episodio 337. `total_debt` e' il debito netto,
    unica voce del ponte."""
    base = dict(
        revenue_base=1310.0,
        year_base=2025,
        growth=[106.0, 30.0, 22.0, 16.0, 12.0],
        ebit_margin=[22.0, 26.0, 29.0, 31.0, 33.0],
        tax_rate=27.0,
        wacc=10.0,
        g_terminal=3.0,
        roic_terminal=20.0,
        sales_to_capital=3.0,
        diluted_shares=630.0,
        market_price=35.93,
        bridge=Bridge(total_debt=3600.0, accounting_standard="US_GAAP"),
    )
    base.update(modifiche)
    return DcfInputs(**base)


# --------------------------------------------------------------------------- #
# 3.2 · Scenario base — valori annuali e aggregati
# --------------------------------------------------------------------------- #

ANNI = [2026, 2027, 2028, 2029, 2030]

ATTESI_ANNUALI = [
    ("Ricavi",          "revenue",      [2698.6, 3508.2, 4280.0, 4964.8, 5560.5]),
    ("EBIT",            "ebit",         [593.7, 912.1, 1241.2, 1539.1, 1835.0]),
    ("NOPAT",           "nopat",        [433.4, 665.9, 906.1, 1123.5, 1339.5]),
    ("Reinvestimento",  "reinvestment", [462.9, 269.9, 257.3, 228.3, 198.6]),
    ("FCFF",            "fcff",         [-29.5, 396.0, 648.8, 895.3, 1140.9]),
    ("PV del FCFF",     "pv",           [-26.8, 327.3, 487.5, 611.5, 708.4]),
]

ATTESI_AGGREGATI = [
    ("PV flussi espliciti",        "pv_explicit",      2107.8),
    ("Valore terminale (al 2030)", "terminal_value",  16753.8),
    ("PV valore terminale",        "pv_terminal",     10402.8),
    ("Enterprise Value",           "enterprise_value", 12510.6),
    ("Equity value",               "equity_value",     8910.6),
]


def prova_scenario_base(p: Prova):
    p.titolo("1 · SCENARIO BASE — tabella dell'orizzonte esplicito")

    r = run_dcf(input_base())

    intestazione = f"  {'Voce':<18}" + "".join(f"{a:>12}" for a in ANNI) + "   esito"
    print()
    print(intestazione)
    print("  " + "-" * (len(intestazione) - 2))

    for etichetta, campo, attesi in ATTESI_ANNUALI:
        ottenuti = [getattr(riga, campo) for riga in r.years]
        esiti = [
            p.confronta(f"{etichetta} {anno}", att, ott, TOLL_MLN)
            for anno, att, ott in zip(ANNI, attesi, ottenuti)
        ]
        segno = "ok" if all(esiti) else "KO"
        print(f"  {etichetta:<18}" + "".join(f"{v:>12.1f}" for v in ottenuti) + f"   {segno}")

    print()
    print(f"  Trenta valori annuali, tolleranza +/- {TOLL_MLN} mln.")

    p.titolo("2 · SCENARIO BASE — aggregati e fair value")
    print()
    print(f"  {'Aggregato':<30}{'atteso':>14}{'ottenuto':>14}{'scarto':>12}   esito")
    print("  " + "-" * 82)

    for etichetta, campo, atteso in ATTESI_AGGREGATI:
        ottenuto = getattr(r, campo)
        ok = p.confronta(etichetta, atteso, ottenuto, TOLL_MLN)
        print(f"  {etichetta:<30}{atteso:>14.1f}{ottenuto:>14.1f}"
              f"{abs(ottenuto - atteso):>12.2f}   {'ok' if ok else 'KO'}")

    ok = p.confronta("Fair value per azione", 14.14, r.fair_value_per_share, TOLL_AZIONE)
    print(f"  {'Fair value per azione':<30}{14.14:>14.2f}{r.fair_value_per_share:>14.2f}"
          f"{abs(r.fair_value_per_share - 14.14):>12.4f}   {'ok' if ok else 'KO'}")

    print()
    print(f"  Prezzo di mercato 35,93 -> upside {r.upside * 100:+.1f}%")
    print(f"  Il ponte, riga per riga:")
    for riga in r.bridge_lines:
        print(f"    {riga.voce:<44}{riga.importo:>12.1f}{riga.cumulato:>14.1f}")
    if r.alarms:
        print()
        print(f"  Allarmi emessi: {', '.join(r.alarms)}")
        for nota in r.notes:
            print(f"    - {nota}")


# --------------------------------------------------------------------------- #
# 3.3 · Matrice di sensibilita' — tutte e 25 le celle
# --------------------------------------------------------------------------- #

WACC_LIST = [8.0, 9.0, 10.0, 11.0, 12.0]
G_LIST = [2.0, 2.5, 3.0, 4.0, 5.0]

ATTESI_SENSIBILITA = [
    [20.02, 21.47, 23.21, 27.98, 35.86],
    [15.87, 16.82, 17.92, 20.75, 24.96],
    [12.78, 13.42, 14.14, 15.94, 18.43],
    [10.39, 10.83, 11.33, 12.52, 14.08],
    [8.48, 8.80, 9.15, 9.96, 10.98],
]


def prova_sensibilita(p: Prova):
    p.titolo("3 · MATRICE DI SENSIBILITA' — 25 celle, fair value per azione")

    matrice = sensitivity(input_base(), WACC_LIST, G_LIST)

    # Il backslash sta fuori dall'f-string: dentro e' illegale fino a Python 3.11.
    intestazione = "WACC \\ g"

    print()
    print(f"  {intestazione:<10}" + "".join(f"{g:>11.1f}%" for g in G_LIST))
    print("  " + "-" * 70)

    for i, w in enumerate(WACC_LIST):
        celle = []
        for j, g in enumerate(G_LIST):
            atteso = ATTESI_SENSIBILITA[i][j]
            ottenuto = matrice[i][j]
            ok = p.confronta(f"sensibilita' WACC {w}% / g {g}%", atteso, ottenuto, TOLL_AZIONE)
            celle.append(f"{ottenuto:>10.2f}{'' if ok else '!'}" if ottenuto is not None else f"{'None':>10}!")
        print(f"  {w:<9.0f}%" + "".join(f"{c:>12}" for c in celle))

    print()
    print(f"  Venticinque celle, tolleranza +/- {TOLL_AZIONE}. Ogni cella e' un DCF")
    print("  rifatto da capo: cambia il WACC dell'orizzonte esplicito e cambia il")
    print("  fattore (1 - g/ROIC), che a g=2% vale 0,90 e a g=5% vale 0,75.")


# --------------------------------------------------------------------------- #
# 3.4 · Casi limite
# --------------------------------------------------------------------------- #

def prova_casi_limite(p: Prova):
    p.titolo("4 · CASI LIMITE — dove non esiste un numero, non deve uscirne uno")
    print()

    def errore_atteso(etichetta, costruisci):
        try:
            costruisci()
        except DcfError as ex:
            p.afferma(etichetta, True)
            print(f"  ok   {etichetta}")
            print(f"         -> {str(ex)[:96]}")
            return
        except Exception as ex:          # eccezione sbagliata: e' comunque un difetto
            p.afferma(etichetta, False, f"sollevata {type(ex).__name__} invece di DcfError")
            print(f"  KO   {etichetta}: sollevata {type(ex).__name__}, attesa DcfError")
            return
        p.afferma(etichetta, False, "nessun errore sollevato, ha restituito un numero")
        print(f"  KO   {etichetta}: nessun errore, ha restituito un numero")

    errore_atteso("wacc = g_terminal -> errore esplicito",
                  lambda: run_dcf(input_base(wacc=3.0, g_terminal=3.0)))

    errore_atteso("wacc < g_terminal -> errore esplicito",
                  lambda: run_dcf(input_base(wacc=2.0, g_terminal=3.0)))

    # Stessa famiglia dei due precedenti, dall'altro lato della formula: qui il
    # fattore (1 - g/ROIC) va a zero o sotto, e il valore terminale con lui. Il
    # motore restituiva un numero plausibile e sbagliato; ora si ferma.
    errore_atteso("roic_terminal = g_terminal -> errore esplicito",
                  lambda: run_dcf(input_base(roic_terminal=3.0, g_terminal=3.0)))

    errore_atteso("roic_terminal < g_terminal -> errore esplicito",
                  lambda: run_dcf(input_base(roic_terminal=2.0, g_terminal=3.0)))

    errore_atteso("growth di lunghezza != 5 -> errore esplicito",
                  lambda: run_dcf(input_base(growth=[10.0, 10.0, 10.0])))

    errore_atteso("US_GAAP con lease_liabilities > 0 -> errore esplicito",
                  lambda: run_dcf(input_base(
                      bridge=Bridge(total_debt=3600.0, lease_liabilities=500.0,
                                    accounting_standard="US_GAAP"))))

    # market_price = 0: il calcolo procede, upside None, nessuna divisione per zero
    print()
    try:
        r = run_dcf(input_base(market_price=0.0))
        ok = (r.upside is None and abs(r.fair_value_per_share - 14.14) <= TOLL_AZIONE)
        p.afferma("market_price = 0 -> calcolo ok, upside None", ok,
                  f"upside={r.upside}, fair_value={r.fair_value_per_share}")
        print(f"  {'ok' if ok else 'KO'}   market_price = 0 -> fair value "
              f"{r.fair_value_per_share:.2f}, upside {r.upside}")
    except Exception as ex:
        p.afferma("market_price = 0 -> calcolo ok, upside None", False, repr(ex))
        print(f"  KO   market_price = 0: sollevata {type(ex).__name__}")

    # Ponte con cassa netta, alla Alphabet: equity > enterprise value, allarme acceso
    r = run_dcf(input_base(
        bridge=Bridge(cash_and_securities=95000.0, total_debt=12000.0,
                      accounting_standard="US_GAAP")))
    ok = (r.equity_value > r.enterprise_value and "CASSA_NETTA" in r.alarms)
    p.afferma("ponte con cassa netta -> equity > EV e allarme CASSA_NETTA", ok,
              f"equity={r.equity_value:.1f}, ev={r.enterprise_value:.1f}, allarmi={r.alarms}")
    print(f"  {'ok' if ok else 'KO'}   ponte con cassa netta -> equity {r.equity_value:,.0f} > "
          f"EV {r.enterprise_value:,.0f}, allarmi {r.alarms}")

    # Risolutore inverso senza soluzione plausibile: None + motivazione, mai un numero
    esito = reverse_growth(input_base(market_price=500.0))
    ok = (esito.value is None and len(esito.motivo) > 20)
    p.afferma("risolutore inverso senza soluzione -> None + motivazione", ok,
              f"value={esito.value}")
    print(f"  {'ok' if ok else 'KO'}   reverse_growth a prezzo 500 -> value={esito.value}")
    print(f"         -> {esito.motivo[:96]}")


# --------------------------------------------------------------------------- #
# Prova di coerenza dei risolutori inversi
# --------------------------------------------------------------------------- #

def prova_reverse(p: Prova):
    """I quattro risolutori non hanno valori pubblicati da confrontare — l'episodio
    non li riporta, e inventarne uno significherebbe tarare il motore su un numero
    scelto da noi. Si prova quindi l'unica cosa verificabile:

      - se il risolutore restituisce un valore, quel valore rimesso dentro il
        motore deve riportare il fair value **esattamente sul prezzo di mercato**;
      - se restituisce `None`, l'affermazione «non c'e' soluzione plausibile» va
        **verificata**, non creduta: si valuta il modello ai due estremi
        dell'intervallo e si controlla che il prezzo cada davvero fuori.

    Il secondo caso e' quello che si presenta su `reverse_margin` con questi
    input, ed e' un risultato di merito: al prezzo di 35,93 nessun margine EBIT
    entro il 60% basta, da solo, a giustificare la valutazione.
    """
    p.titolo("5 · RISOLUTORI INVERSI — coerenza, non valori di riferimento")
    print()

    base = input_base()
    prezzo = base.market_price

    from dataclasses import replace
    from dcf_engine import (LIMITI_CRESCITA, LIMITI_WACC, LIMITI_MARGINE,
                            LIMITI_G_TERMINALE, MARGINE_G_WACC,
                            _coefficienti_di_forma, _intervallo_ammissibile)

    # I due risolutori che muovono un percorso vengono riverificati rimettendo
    # dentro il motore il **percorso che il motore stesso ha restituito**, non
    # una copia della sua logica ricostruita qui: una prova che reimplementa
    # cio' che prova puo' concordare con un'implementazione sbagliata.
    def estremi_percorso(valori, limiti):
        c, _ = _coefficienti_di_forma(valori)
        return _intervallo_ammissibile(valori[0], c, limiti[0], limiti[1]), c

    (lim_g, _cg) = estremi_percorso(base.growth, LIMITI_CRESCITA)
    (lim_m, _cm) = estremi_percorso(base.ebit_margin, LIMITI_MARGINE)

    def con_percorso(campo, c, valori):
        ancora = valori[0]
        return lambda x: replace(base, **{campo: [ancora + ci * (x - ancora) for ci in c]})

    casi = [
        ("reverse_growth", reverse_growth,
         con_percorso("growth", _cg, base.growth), lim_g, "% CAGR ricavi"),
        ("reverse_g_terminal", reverse_g_terminal,
         lambda x: replace(base, g_terminal=x),
         (LIMITI_G_TERMINALE[0], base.wacc - MARGINE_G_WACC), "% perpetua"),
        ("reverse_wacc", reverse_wacc,
         lambda x: replace(base, wacc=x),
         (max(LIMITI_WACC[0], base.g_terminal + MARGINE_G_WACC), LIMITI_WACC[1]),
         "% di costo del capitale"),
        ("reverse_margin", reverse_margin,
         con_percorso("ebit_margin", _cm, base.ebit_margin), lim_m,
         "% di margine EBIT al 2030"),
    ]

    for nome, funzione, applica, limiti, unita in casi:
        esito = funzione(base)

        if esito.value is not None:
            # Se il risolutore ha restituito un percorso, e' quello che si
            # rimette dentro: `value` puo' essere una grandezza derivata (per
            # la crescita e' il CAGR implicito, non un parametro del modello).
            dentro = (replace(base, growth=esito.percorso)
                      if nome == "reverse_growth" and esito.percorso
                      else replace(base, ebit_margin=esito.percorso)
                      if nome == "reverse_margin" and esito.percorso
                      else applica(esito.value))
            riverifica = run_dcf(dentro).fair_value_per_share
            ok = p.confronta(f"{nome}: la soluzione riporta il fair value sul prezzo",
                             prezzo, riverifica, TOLL_AZIONE)
            print(f"  {'ok' if ok else 'KO'}   {nome:<20}{esito.value:>8.2f} {unita:<26}"
                  f"-> fair value {riverifica:.2f} contro prezzo {prezzo:.2f}")
            if esito.percorso:
                print(f"         percorso: {' · '.join(f'{x:.1f}' for x in esito.percorso)}"
                      f"   ({esito.grandezza})")
            continue

        # Nessuna soluzione dichiarata: si verifica che sia vero, valutando il
        # modello ai due estremi. Il prezzo deve cadere fuori dall'intervallo
        # dei fair value ottenibili, altrimenti il risolutore ha mancato una
        # soluzione che esisteva — che e' un difetto, non una risposta prudente.
        lo, hi = limiti
        fv_lo = run_dcf(applica(lo)).fair_value_per_share
        fv_hi = run_dcf(applica(hi)).fair_value_per_share
        basso, alto = min(fv_lo, fv_hi), max(fv_lo, fv_hi)
        ok = (not (basso <= prezzo <= alto)) and len(esito.motivo) > 20
        p.afferma(f"{nome}: il 'None' e' verificato agli estremi dell'intervallo", ok,
                  f"fair value fra {basso:.2f} e {alto:.2f}, prezzo {prezzo:.2f}")
        print(f"  {'ok' if ok else 'KO'}   {nome:<20}{'None':>8} {unita:<26}"
              f"-> fair value fra {basso:.2f} e {alto:.2f}, prezzo {prezzo:.2f} fuori intervallo")
        print(f"         -> {esito.motivo[:96]}")


# --------------------------------------------------------------------------- #
# Come si muove il percorso delle ipotesi
# --------------------------------------------------------------------------- #

def prova_forma_del_percorso(p: Prova):
    """La semantica dei due risolutori che muovono un **percorso** e non un
    numero: riscalatura degli incrementi sopra il valore ancorato.

    Non e' un dettaglio di implementazione ma un'ipotesi di metodo, quindi va
    provata con la stessa severita' dei valori del modello. Il difetto che
    chiude: l'interpolazione lineare cambiava insieme **livello e forma**, cioe'
    calcolava la risposta su un percorso che non era quello scritto da chi ha
    fatto le ipotesi.
    """
    p.titolo("6 · FORMA DEL PERCORSO — riscalatura degli incrementi")
    print()

    from dcf_engine import _coefficienti_di_forma, _intervallo_ammissibile

    def percorso(valori, T):
        c, nota = _coefficienti_di_forma(valori)
        return [valori[0] + ci * (T - valori[0]) for ci in c], nota

    # 1 · il percorso di riferimento a un obiettivo noto, cinque numeri esatti
    atteso = [22.0, 30.36, 36.64, 40.82, 45.0]
    ottenuto, _ = percorso([22.0, 26.0, 29.0, 31.0, 33.0], 45.0)
    ok = all(abs(a - b) <= 0.01 for a, b in zip(atteso, ottenuto))
    p.afferma("riscalatura: 22·26·29·31·33 verso 45 -> 22·30,36·36,64·40,82·45", ok,
              " · ".join(f"{x:.2f}" for x in ottenuto))
    print(f"  {'ok' if ok else 'KO'}   forma concava conservata: "
          f"{' · '.join(f'{x:.2f}' for x in ottenuto)}")
    lineare = [22.0 + (45.0 - 22.0) * i / 4 for i in range(5)]
    ok = any(abs(a - b) > 0.5 for a, b in zip(lineare, ottenuto))
    p.afferma("riscalatura e interpolazione lineare danno percorsi diversi", ok)
    print(f"  {'ok' if ok else 'KO'}   la rampa lineare sarebbe stata: "
          f"{' · '.join(f'{x:.2f}' for x in lineare)}")

    # 2 · percorso piatto -> ripiego lineare DICHIARATO
    _, nota = percorso([25.0] * 5, 40.0)
    ok = "piatto" in nota and "lineare" in nota
    p.afferma("percorso piatto -> ripiego lineare dichiarato nella motivazione", ok, nota)
    print(f"  {'ok' if ok else 'KO'}   piatto -> {nota[:80]}")

    # 3 · percorso che TORNA al punto di partenza: d[-1] = 0 ma la forma esiste.
    #     E' il caso che sarebbe passato dal buco se il ripiego fosse agganciato
    #     a "tutti gli incrementi a zero" invece che a "l'ultimo incremento e' zero".
    _, nota2 = percorso([22.0, 26.0, 29.0, 31.0, 22.0], 40.0)
    ok = ("lineare" in nota2 and "piatto" not in nota2 and nota2 != nota)
    p.afferma("percorso che torna al punto di partenza -> ripiego, motivazione diversa",
              ok, nota2)
    print(f"  {'ok' if ok else 'KO'}   torna all'ancora -> {nota2[:80]}")

    # 4 · percorso non monotono: l'intervallo ammissibile si stringe, e agli
    #     estremi nessun anno esce dalla banda
    non_mono = [22.0, 35.0, 20.0, 28.0, 33.0]
    c, _ = _coefficienti_di_forma(non_mono)
    lo, hi = _intervallo_ammissibile(non_mono[0], c, 0.0, 60.0)
    ok = (lo > 0.0 and hi < 60.0)
    p.afferma("percorso non monotono -> intervallo ammissibile piu' stretto di [0;60]",
              ok, f"[{lo:.3f}; {hi:.3f}]")
    dentro = all(-1e-9 <= x <= 60.0 + 1e-9
                 for T in (lo, hi) for x in percorso(non_mono, T)[0])
    p.afferma("agli estremi dell'intervallo nessun anno esce da [0%; 60%]", dentro)
    print(f"  {'ok' if ok and dentro else 'KO'}   non monotono -> T in [{lo:.3f}; {hi:.3f}], "
          f"a T={hi:.3f}: {' · '.join(f'{x:.1f}' for x in percorso(non_mono, hi)[0])}")

    # 5 · quasi piatto: senza il taglio la riscalatura produce margini al 4560%
    quasi = [22.0, 26.0, 29.0, 31.0, 22.001]
    cq, _ = _coefficienti_di_forma(quasi)
    lq, hq = _intervallo_ammissibile(quasi[0], cq, 0.0, 60.0)
    fuori = percorso(quasi, hq + 0.5)[0]
    ok = (hq - lq < 0.1) and max(fuori) > 1000.0
    p.afferma("percorso quasi piatto -> intervallo collassato attorno all'ancora", ok,
              f"[{lq:.4f}; {hq:.4f}]")
    print(f"  {'ok' if ok else 'KO'}   quasi piatto -> T in [{lq:.3f}; {hq:.3f}]; "
          f"mezzo punto oltre il tetto si arriverebbe a {max(fuori):.0f}%")

    # 6 · fattore negativo: forma specchiata, e dichiarata
    esito = reverse_margin(input_base(market_price=5.0))
    ok = (esito.value is not None and esito.value < 22.0
          and "specchiata" in esito.motivo
          and esito.percorso is not None and esito.percorso[0] == 22.0
          and esito.percorso[4] < esito.percorso[0])
    p.afferma("obiettivo sotto l'ancora -> forma specchiata e dichiarata", ok,
              esito.motivo[:120])
    if esito.percorso:
        print(f"  {'ok' if ok else 'KO'}   prezzo 5,00 -> margine {esito.value:.2f}%, percorso "
              f"{' · '.join(f'{x:.1f}' for x in esito.percorso)}")
        print(f"         -> {esito.motivo[:100]}")

    # 7 · affinita': e' la condizione che rende valida la bisezione
    m = [22.0, 26.0, 29.0, 31.0, 33.0]
    campioni = [(T, run_dcf(input_base(ebit_margin=percorso(m, T)[0])).fair_value_per_share)
                for T in (5.0, 20.0, 35.0, 50.0)]
    pend = [(campioni[i + 1][1] - campioni[i][1]) / (campioni[i + 1][0] - campioni[i][0])
            for i in range(len(campioni) - 1)]
    ok = (max(pend) - min(pend)) < 1e-9
    p.afferma("il fair value e' affine nel margine obiettivo (bisezione valida)", ok,
              f"pendenze fra {min(pend):.9f} e {max(pend):.9f}")
    print(f"  {'ok' if ok else 'KO'}   pendenza costante a {pend[0]:.6f} "
          f"(scarto {max(pend) - min(pend):.2e})")

    # 8 · il primo anno della crescita resta ancorato al fatto assunto
    eg = reverse_growth(input_base())
    ok = (eg.percorso is not None and eg.percorso[0] == 106.0
          and eg.grandezza == "CAGR implicito dei ricavi"
          and eg.dettagli is not None and eg.dettagli["ricavi_finali"] > 12000.0)
    p.afferma("reverse_growth: anno 1 ancorato a 106%, pubblica il CAGR implicito", ok,
              f"value={eg.value}, percorso={eg.percorso}")
    print(f"  {'ok' if ok else 'KO'}   CAGR implicito {eg.value:.2f}%, ricavi "
          f"{eg.dettagli['anno_finale']} impliciti {eg.dettagli['ricavi_finali']:,.0f} mln")
    print(f"         percorso illustrativo: {' · '.join(f'{x:.1f}' for x in eg.percorso)}")

# --------------------------------------------------------------------------- #

def main():
    print("=" * 74)
    print("  PROVA DI RIFERIMENTO DEL MOTORE DCF")
    print(f"  motore versione {MOTORE_VERSIONE}")
    print("  modello: Bending Spoons, episodio 337 di The Bull")
    print("=" * 74)

    p = Prova()
    prova_scenario_base(p)
    prova_sensibilita(p)
    prova_casi_limite(p)
    prova_reverse(p)
    prova_forma_del_percorso(p)
    sys.exit(p.riepilogo())


if __name__ == "__main__":
    main()
