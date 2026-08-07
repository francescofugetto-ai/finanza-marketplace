#!/usr/bin/env python3
"""
dcf_engine.py — Motore di calcolo deterministico per la valutazione di aziende
                con il metodo dei flussi di cassa scontati (DCF).

SCOPO
-----
Calcola, da INPUT GIA' VERIFICATI (bilancio dell'ultimo esercizio chiuso, ipotesi
di crescita e margine, tasso di sconto, ponte verso l'equity), quello che serve a
dire quanto vale un'azienda e con quali assunzioni:

  - la tabella anno per anno dell'orizzonte esplicito: ricavi, EBIT, NOPAT,
    reinvestimento, FCFF, valore attuale del FCFF
  - il valore terminale con la formula di Gordon corretta per il ROIC, e il suo
    valore attuale
  - l'Enterprise Value
  - il ponte verso l'equity **riga per riga**, perche' il report lo mostra come
    cascata e non come numero unico
  - il fair value per azione e l'upside rispetto al prezzo di mercato
  - la matrice di sensibilita' del fair value a WACC e crescita perpetua
  - i quattro risolutori inversi (reverse DCF): quale crescita, quale g perpetua,
    quale WACC, quale margine il prezzo di mercato sta gia' scontando

COPIA MADRE — NON DUPLICARE A MANO
---------------------------------
Questo file e' la **copia autoritativa** del motore. La dottrina che implementa
(orizzonte esplicito di cinque anni, reinvestimento da sales-to-capital, valore
terminale corretto per il ROIC, ponte verso l'equity) vive nelle reference di
questa skill: il codice sta accanto alla dottrina che applica.

Versione corrente del motore: vedi la costante MOTORE_VERSIONE definita sotto,
subito dopo gli import. E' una vera variabile di modulo, leggibile con
`import dcf_engine; dcf_engine.MOTORE_VERSIONE`, cosi' che un controllo
automatico possa leggerla senza interpretare un commento.

QUESTO SCRIPT NON SCARICA DATI. Non conosce ticker, bilanci o prezzi correnti:
li riceve come argomenti, dopo che sono stati verificati sulle fonti autoritative
(relazione finanziaria annuale, comunicati dell'emittente, book del broker).
Non legge file, non stampa, non apre connessioni: input -> output. Non inventare
input.

CONVENZIONI E LIMITI (dichiarati, non nascosti)
-----------------------------------------------
  - Unita': gli importi sono in milioni di valuta, il prezzo per azione e' in
    unita' di valuta, le azioni in milioni. Il motore non converte valute: tutti
    gli importi devono essere gia' nella stessa valuta del prezzo di mercato.
  - Percentuali: si passano in **punti percentuali** (22 significa 22%, non 0,22).
    L'unica eccezione e' `sales_to_capital`, che e' un rapporto puro.
  - Orizzonte esplicito **fisso a cinque anni**. Non e' un parametro: e' una
    scelta di dottrina, perche' oltre il quinto anno le ipotesi puntuali valgono
    meno del valore terminale che le assorbe. Le liste `growth` e `ebit_margin`
    devono quindi avere lunghezza 5, e se non ce l'hanno il motore solleva un
    errore invece di indovinare.
  - Flussi di fine anno, scontati a periodi interi: `pv[t] = fcff[t] / (1+wacc)^t`.
    Nessuna convenzione di meta' anno. E' l'ipotesi piu' conservativa e la piu'
    facile da confrontare con i modelli pubblicati.
  - Reinvestimento derivato dai ricavi incrementali via `sales_to_capital`, non
    dalla somma di capex, ammortamenti e variazione di circolante. E' la forma
    che rende esplicito il legame fra crescita e capitale che la finanzia: una
    crescita senza reinvestimento e' un pasto gratis, e qui non si puo' scrivere.
  - Valore terminale con il fattore `(1 - g/ROIC)`, che **cambia con g**: a g=2%
    e ROIC=20% vale 0,90, a g=5% vale 0,75. Non e' una costante da calcolare una
    volta e riusare nella matrice di sensibilita'.
  - Nessun arrotondamento intermedio. Si arrotonda solo alla presentazione.
  - Gli allarmi (§ALLARMI) sono **dati, non eccezioni**: il calcolo prosegue e li
    restituisce. Gli errori veri, invece, fermano il calcolo: un DCF che
    restituisce un numero dove non ne esiste uno e' peggio di un DCF che non
    risponde.
  - I risolutori inversi lavorano per bisezione dentro limiti di plausibilita'
    dichiarati. Fuori da quei limiti restituiscono `None` e la ragione scritta a
    parole: **mai un numero inventato**.
"""

from __future__ import annotations
from dataclasses import dataclass, field, replace
from typing import Optional

# ─── versione del motore ───────────────────────────────────────────────────
# Vera variabile di modulo, non una riga dentro il commento: un controllo
# automatico deve poterla leggere da programma.
MOTORE_VERSIONE = "1.0"

# Orizzonte esplicito. Costante di dottrina, non parametro: vedi le convenzioni.
ORIZZONTE_ANNI = 5

# Limiti di plausibilita' dei risolutori inversi, in punti percentuali.
LIMITI_CRESCITA = (-20.0, 100.0)
LIMITI_G_TERMINALE = (0.0, None)      # l'estremo alto e' wacc - MARGINE_G_WACC
LIMITI_WACC = (4.0, 25.0)
LIMITI_MARGINE = (0.0, 60.0)
MARGINE_G_WACC = 0.5                  # g non puo' avvicinarsi al WACC oltre questo

# Bisezione: tolleranza sul prezzo per azione e numero massimo di iterazioni.
TOLLERANZA_PREZZO = 0.0001
MAX_ITERAZIONI = 200

# Soglie degli allarmi.
SOGLIA_SBC = 5.0                      # % dei ricavi
SOGLIA_TV_DOMINANTE = 0.85            # quota del pv_TV sull'Enterprise Value
SOGLIA_PARTECIPAZIONI = 0.10          # quota sull'Enterprise Value


class DcfError(ValueError):
    """Errore di input o di ipotesi che rende il calcolo privo di significato.

    E' un'eccezione e non un allarme perche' non esiste un numero corretto da
    restituire: proseguire vorrebbe dire consegnare un risultato che sembra
    valido e non lo e'.
    """


# --------------------------------------------------------------------------- #
# Strutture di input
# --------------------------------------------------------------------------- #

@dataclass
class Bridge:
    """Il ponte dall'Enterprise Value all'equity. Tutte le voci opzionali, a zero
    se assenti, tutte in milioni e con segno gia' deciso dal campo (si passano
    sempre come importi positivi).

    `accounting_standard` non e' un dettaglio anagrafico: decide se
    `lease_liabilities` sia una voce legittima o un doppio conteggio.
    """
    cash_and_securities: float = 0.0        # +
    non_consolidated_stakes: float = 0.0    # +
    total_debt: float = 0.0                 # −
    lease_liabilities: float = 0.0          # −  solo IFRS
    pension_deficit: float = 0.0            # −  netto d'imposta
    minority_interests: float = 0.0         # −
    employee_options_value: float = 0.0     # −
    accounting_standard: str = "IFRS"       # "IFRS" | "US_GAAP"


@dataclass
class DcfInputs:
    """Gli input del modello. Le percentuali in punti percentuali (vedi le
    convenzioni in testa al file)."""
    revenue_base: float                     # $ mln, ultimo esercizio chiuso
    year_base: int                          # es. 2025
    growth: list                            # 5 float, % anno per anno
    ebit_margin: list                       # 5 float, % anno per anno
    tax_rate: float                         # %
    wacc: float                             # %
    g_terminal: float                       # %
    roic_terminal: float                    # %
    sales_to_capital: float                 # rapporto puro
    diluted_shares: float                   # mln
    bridge: Bridge = field(default_factory=Bridge)
    market_price: float = 0.0               # 0 se non quotata
    # Opzionali, servono solo agli allarmi: assenti, l'allarme non si accende.
    sbc: Optional[float] = None             # $ mln, stock-based compensation
    risk_free: Optional[float] = None       # %, il tasso usato per costruire il WACC


# --------------------------------------------------------------------------- #
# Strutture di output
# --------------------------------------------------------------------------- #

@dataclass
class YearRow:
    """Una riga della tabella dell'orizzonte esplicito."""
    year: int
    revenue: float
    ebit: float
    nopat: float
    reinvestment: float
    fcff: float
    discount_factor: float
    pv: float


@dataclass
class BridgeLine:
    """Una riga della cascata dall'Enterprise Value all'equity."""
    voce: str
    importo: float        # gia' col segno con cui entra nella somma
    cumulato: float       # totale progressivo dopo questa riga


@dataclass
class DcfResult:
    years: list                   # list[YearRow]
    pv_explicit: float
    terminal_value: float         # al termine dell'orizzonte, non attualizzato
    pv_terminal: float
    enterprise_value: float
    bridge_lines: list            # list[BridgeLine]
    equity_value: float
    fair_value_per_share: float
    upside: Optional[float]       # frazione (0,15 = +15%); None se prezzo assente
    alarms: list                  # list[str], sigle
    notes: list                   # list[str], testo leggibile


@dataclass
class ReverseResult:
    """Esito di un risolutore inverso. `value` e' `None` quando dentro i limiti
    di plausibilita' non esiste soluzione: in quel caso `motivo` dice perche',
    e non si restituisce nessun numero."""
    value: Optional[float]        # in punti percentuali
    motivo: str


# --------------------------------------------------------------------------- #
# Validazione
# --------------------------------------------------------------------------- #

def _valida(inputs: DcfInputs) -> None:
    """Solleva DcfError sui casi in cui non esiste un risultato corretto."""
    for nome, lista in (("growth", inputs.growth), ("ebit_margin", inputs.ebit_margin)):
        if len(lista) != ORIZZONTE_ANNI:
            raise DcfError(
                f"la lista '{nome}' ha {len(lista)} elementi, ne servono "
                f"esattamente {ORIZZONTE_ANNI}: l'orizzonte esplicito e' fisso a "
                f"cinque anni e il motore non completa ne' taglia le ipotesi mancanti"
            )

    if inputs.wacc <= inputs.g_terminal:
        raise DcfError(
            f"wacc ({inputs.wacc}%) <= g_terminal ({inputs.g_terminal}%): la formula "
            f"di Gordon non ha significato e restituirebbe un valore negativo o "
            f"infinito. Un'azienda non puo' crescere per sempre piu' del costo del "
            f"capitale che la finanzia"
        )

    if inputs.roic_terminal == 0:
        raise DcfError("roic_terminal a zero: il fattore (1 - g/ROIC) non e' definito")

    if inputs.sales_to_capital == 0:
        raise DcfError(
            "sales_to_capital a zero: il reinvestimento non e' definito. Se la "
            "crescita non richiede capitale va dichiarato esplicitamente, non "
            "ottenuto per divisione per zero"
        )

    if inputs.diluted_shares <= 0:
        raise DcfError("diluted_shares deve essere positivo per calcolare un valore per azione")

    std = inputs.bridge.accounting_standard
    if std not in ("IFRS", "US_GAAP"):
        raise DcfError(
            f"accounting_standard '{std}' non riconosciuto: ammessi 'IFRS' e 'US_GAAP'"
        )
    if std == "US_GAAP" and inputs.bridge.lease_liabilities > 0:
        raise DcfError(
            "accounting_standard 'US_GAAP' con lease_liabilities > 0: in US GAAP il "
            "costo del leasing operativo e' gia' dentro l'EBIT, quindi sottrarre di "
            "nuovo il debito da leasing nel ponte e' un doppio conteggio"
        )


# --------------------------------------------------------------------------- #
# Il calcolo, pezzo per pezzo
# --------------------------------------------------------------------------- #

def _tabella_esplicita(inputs: DcfInputs) -> list:
    """Le cinque righe dell'orizzonte esplicito. Nessun arrotondamento."""
    tax = inputs.tax_rate / 100.0
    wacc = inputs.wacc / 100.0

    righe = []
    revenue_prec = inputs.revenue_base
    for t in range(1, ORIZZONTE_ANNI + 1):
        crescita = inputs.growth[t - 1] / 100.0
        margine = inputs.ebit_margin[t - 1] / 100.0

        revenue = revenue_prec * (1.0 + crescita)
        ebit = revenue * margine
        nopat = ebit * (1.0 - tax)
        reinvest = (revenue - revenue_prec) / inputs.sales_to_capital
        fcff = nopat - reinvest
        fattore = (1.0 + wacc) ** t

        righe.append(YearRow(
            year=inputs.year_base + t,
            revenue=revenue,
            ebit=ebit,
            nopat=nopat,
            reinvestment=reinvest,
            fcff=fcff,
            discount_factor=fattore,
            pv=fcff / fattore,
        ))
        revenue_prec = revenue

    return righe


def _valore_terminale(inputs: DcfInputs, ebit_finale: float) -> tuple:
    """Gordon corretto per il ROIC. Ritorna (TV al termine, TV attualizzato).

    Il fattore (1 - g/ROIC) e' la quota di NOPAT che NON va reinvestita per
    sostenere la crescita perpetua: dipende da g, e va ricalcolato ogni volta che
    g cambia. E' il punto in cui una matrice di sensibilita' si sbaglia piu'
    facilmente, perche' il fattore sembra una costante del modello e non lo e'.
    """
    tax = inputs.tax_rate / 100.0
    wacc = inputs.wacc / 100.0
    g = inputs.g_terminal / 100.0
    roic = inputs.roic_terminal / 100.0

    quota_non_reinvestita = 1.0 - g / roic
    tv = ebit_finale * (1.0 + g) * (1.0 - tax) * quota_non_reinvestita / (wacc - g)
    pv_tv = tv / (1.0 + wacc) ** ORIZZONTE_ANNI
    return tv, pv_tv


def _ponte(inputs: DcfInputs, enterprise_value: float) -> tuple:
    """La cascata dall'Enterprise Value all'equity, riga per riga.

    Ritorna (righe, equity_value). Le voci a zero restano nella cascata: una riga
    a zero dichiarata vale piu' di una riga assente, che il lettore non sa se sia
    zero o dimenticata.
    """
    b = inputs.bridge

    def meno(x: float) -> float:
        """Cambia segno tenendo lo zero positivo: una riga a zero si stampa '0,0'
        e non '-0,0', che in una cascata sembra un errore di segno."""
        return -x if x != 0 else 0.0

    voci = [
        ("Enterprise Value", enterprise_value),
        ("+ cassa e titoli negoziabili", b.cash_and_securities),
        ("+ partecipazioni non consolidate", b.non_consolidated_stakes),
        ("- debito finanziario totale", meno(b.total_debt)),
        ("- passivita' per leasing", meno(b.lease_liabilities)),
        ("- deficit pensionistico (netto d'imposta)", meno(b.pension_deficit)),
        ("- interessi di minoranza", meno(b.minority_interests)),
        ("- valore delle opzioni ai dipendenti", meno(b.employee_options_value)),
    ]

    righe, cumulato = [], 0.0
    for voce, importo in voci:
        cumulato += importo
        righe.append(BridgeLine(voce=voce, importo=importo, cumulato=cumulato))

    return righe, cumulato


def _allarmi(inputs: DcfInputs, pv_tv: float, enterprise_value: float,
             equity_value: float) -> tuple:
    """Gli allarmi sono dati, non eccezioni: il calcolo e' gia' finito quando
    arrivano qui. Ritorna (sigle, note leggibili)."""
    sigle, note = [], []

    if inputs.sbc is not None and inputs.revenue_base > 0:
        quota = inputs.sbc / inputs.revenue_base * 100.0
        if quota > SOGLIA_SBC:
            sigle.append("SBC_ELEVATA")
            note.append(
                f"SBC dichiarata pari al {quota:.1f}% dei ricavi (soglia {SOGLIA_SBC:.0f}%): "
                f"e' un costo reale per l'azionista, verifica che sia dentro l'EBIT e che "
                f"le azioni siano contate su base diluita"
            )

    if enterprise_value != 0 and pv_tv / enterprise_value > SOGLIA_TV_DOMINANTE:
        quota = pv_tv / enterprise_value * 100.0
        sigle.append("TV_DOMINANTE")
        note.append(
            f"il valore terminale pesa il {quota:.1f}% dell'Enterprise Value (soglia "
            f"{SOGLIA_TV_DOMINANTE * 100:.0f}%): la valutazione dipende quasi tutta da "
            f"cio' che accade dopo l'orizzonte esplicito, non dalle ipotesi dei cinque anni"
        )

    if inputs.risk_free is not None and inputs.g_terminal > inputs.risk_free:
        sigle.append("G_SOPRA_RISK_FREE")
        note.append(
            f"g_terminal ({inputs.g_terminal}%) supera il tasso privo di rischio "
            f"({inputs.risk_free}%): un'azienda che cresce per sempre piu' dell'economia "
            f"in cui vive finisce per coincidere con l'economia. Damodaran pone qui il tetto"
        )

    if equity_value > enterprise_value:
        sigle.append("CASSA_NETTA")
        note.append(
            "il ponte e' positivo netto: l'azienda ha piu' cassa e attivita' finanziarie "
            "che debito, quindi l'equity value supera l'Enterprise Value"
        )

    if (enterprise_value != 0
            and inputs.bridge.non_consolidated_stakes / enterprise_value > SOGLIA_PARTECIPAZIONI):
        quota = inputs.bridge.non_consolidated_stakes / enterprise_value * 100.0
        sigle.append("PARTECIPAZIONI_RILEVANTI")
        note.append(
            f"le partecipazioni non consolidate valgono il {quota:.1f}% dell'Enterprise Value "
            f"(soglia {SOGLIA_PARTECIPAZIONI * 100:.0f}%): sono iscritte a valore di libro, che "
            f"per una quota rilevante puo' essere molto lontano dal valore reale"
        )

    return sigle, note


# --------------------------------------------------------------------------- #
# API principale
# --------------------------------------------------------------------------- #

def run_dcf(inputs: DcfInputs) -> DcfResult:
    """Il calcolo completo: tabella per anno, valore terminale, Enterprise Value,
    ponte dettagliato, fair value per azione, upside e allarmi.

    Solleva DcfError sugli input che non ammettono un risultato corretto.
    """
    _valida(inputs)

    righe = _tabella_esplicita(inputs)
    pv_explicit = sum(r.pv for r in righe)

    tv, pv_tv = _valore_terminale(inputs, righe[-1].ebit)
    enterprise_value = pv_explicit + pv_tv

    bridge_lines, equity_value = _ponte(inputs, enterprise_value)
    fair_value = equity_value / inputs.diluted_shares

    # market_price a zero significa "non quotata": l'upside non esiste, e non si
    # sostituisce con zero. None e' l'unica risposta onesta.
    upside = (fair_value / inputs.market_price - 1.0) if inputs.market_price > 0 else None

    sigle, note = _allarmi(inputs, pv_tv, enterprise_value, equity_value)

    return DcfResult(
        years=righe,
        pv_explicit=pv_explicit,
        terminal_value=tv,
        pv_terminal=pv_tv,
        enterprise_value=enterprise_value,
        bridge_lines=bridge_lines,
        equity_value=equity_value,
        fair_value_per_share=fair_value,
        upside=upside,
        alarms=sigle,
        notes=note,
    )


def sensitivity(inputs: DcfInputs, wacc_list: list, g_list: list) -> list:
    """Matrice del fair value per azione: WACC sulle righe, g perpetua sulle
    colonne, entrambi in punti percentuali.

    Ogni cella e' un DCF completo rifatto da capo, non una correzione del caso
    base: cambiando il WACC cambiano anche i valori attuali dell'orizzonte
    esplicito, e cambiando g cambia il fattore (1 - g/ROIC).

    Le celle in cui il WACC non supera g valgono `None`: li' non esiste un
    numero, e scriverne uno sarebbe peggio che lasciare il buco.
    """
    matrice = []
    for w in wacc_list:
        riga = []
        for g in g_list:
            try:
                r = run_dcf(replace(inputs, wacc=w, g_terminal=g))
                riga.append(r.fair_value_per_share)
            except DcfError:
                riga.append(None)
        matrice.append(riga)
    return matrice


# --------------------------------------------------------------------------- #
# Risolutori inversi (reverse DCF)
# --------------------------------------------------------------------------- #

def _bisezione(f, lo: float, hi: float, etichetta: str) -> ReverseResult:
    """Bisezione su f(x) = fair_value(x) - market_price, dentro [lo, hi].

    Se agli estremi la funzione non cambia segno, la soluzione non sta dentro i
    limiti di plausibilita': si restituisce None con la ragione. Non si allarga
    l'intervallo, perche' il limite non e' un dettaglio tecnico della bisezione —
    e' l'affermazione che oltre quel valore l'ipotesi non e' piu' credibile.
    """
    try:
        f_lo, f_hi = f(lo), f(hi)
    except DcfError as ex:
        return ReverseResult(None, f"{etichetta}: agli estremi il modello non e' definito ({ex})")

    if f_lo is None or f_hi is None:
        return ReverseResult(None, f"{etichetta}: manca il prezzo di mercato, non c'e' niente da azzerare")

    if f_lo * f_hi > 0:
        verso = "sopra" if f_lo > 0 else "sotto"
        return ReverseResult(
            None,
            f"{etichetta}: nessuna soluzione fra {lo:g} e {hi:g}. Su tutto l'intervallo "
            f"plausibile il fair value resta {verso} il prezzo di mercato, quindi il prezzo "
            f"non sta scontando un valore credibile di questa variabile"
        )

    for _ in range(MAX_ITERAZIONI):
        mid = (lo + hi) / 2.0
        f_mid = f(mid)
        if abs(f_mid) < TOLLERANZA_PREZZO:
            return ReverseResult(mid, f"{etichetta}: convergenza a {mid:.4f}")
        if f_lo * f_mid < 0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid

    mid = (lo + hi) / 2.0
    return ReverseResult(mid, f"{etichetta}: {MAX_ITERAZIONI} iterazioni, scarto residuo entro l'intervallo")


def _scarto(inputs: DcfInputs):
    """Costruisce f(x) = fair_value(x) - market_price a partire da una funzione
    che sa come applicare x agli input."""
    prezzo = inputs.market_price

    def costruisci(applica):
        def f(x):
            if prezzo <= 0:
                return None
            return run_dcf(applica(x)).fair_value_per_share - prezzo
        return f

    return costruisci


def _senza_prezzo(inputs: DcfInputs, etichetta: str) -> Optional[ReverseResult]:
    """Il controllo comune a tutti i risolutori: senza prezzo non c'e' upside da
    azzerare, quindi non c'e' nemmeno una domanda da porre."""
    if inputs.market_price <= 0:
        return ReverseResult(
            None,
            f"{etichetta}: market_price assente o a zero. Il reverse DCF chiede "
            f"'cosa sta scontando il prezzo': senza prezzo la domanda non esiste"
        )
    return None


def reverse_growth(inputs: DcfInputs) -> ReverseResult:
    """La crescita dei ricavi **uniforme** sui cinque anni che azzera l'upside.

    Uniforme e non "scalata dal percorso attuale": il numero serve a essere
    detto a voce — «il prezzo sta scontando il 34% l'anno per cinque anni» — e un
    percorso non uniforme non si riassume in una cifra sola.
    """
    fermo = _senza_prezzo(inputs, "reverse_growth")
    if fermo:
        return fermo

    f = _scarto(inputs)(lambda x: replace(inputs, growth=[x] * ORIZZONTE_ANNI))
    return _bisezione(f, LIMITI_CRESCITA[0], LIMITI_CRESCITA[1], "reverse_growth")


def reverse_g_terminal(inputs: DcfInputs) -> ReverseResult:
    """La crescita perpetua che azzera l'upside.

    L'estremo alto non e' un numero fisso: e' il WACC meno mezzo punto, perche'
    avvicinandosi al WACC il valore terminale esplode e qualunque prezzo
    diventerebbe giustificabile.
    """
    fermo = _senza_prezzo(inputs, "reverse_g_terminal")
    if fermo:
        return fermo

    hi = inputs.wacc - MARGINE_G_WACC
    if hi <= LIMITI_G_TERMINALE[0]:
        return ReverseResult(
            None,
            f"reverse_g_terminal: con un WACC del {inputs.wacc}% non resta nessun "
            f"intervallo plausibile sotto il tetto di wacc - {MARGINE_G_WACC} punti"
        )

    f = _scarto(inputs)(lambda x: replace(inputs, g_terminal=x))
    return _bisezione(f, LIMITI_G_TERMINALE[0], hi, "reverse_g_terminal")


def reverse_wacc(inputs: DcfInputs) -> ReverseResult:
    """Il costo del capitale che azzera l'upside — cioe' il rendimento implicito
    che il mercato sta chiedendo a questa azienda."""
    fermo = _senza_prezzo(inputs, "reverse_wacc")
    if fermo:
        return fermo

    lo = max(LIMITI_WACC[0], inputs.g_terminal + MARGINE_G_WACC)
    if lo >= LIMITI_WACC[1]:
        return ReverseResult(
            None,
            f"reverse_wacc: con g_terminal al {inputs.g_terminal}% non resta nessun "
            f"intervallo plausibile sotto il tetto del {LIMITI_WACC[1]}%"
        )

    f = _scarto(inputs)(lambda x: replace(inputs, wacc=x))
    return _bisezione(f, lo, LIMITI_WACC[1], "reverse_wacc")


def reverse_margin(inputs: DcfInputs) -> ReverseResult:
    """Il margine EBIT del quinto anno che azzera l'upside.

    Il percorso degli anni intermedi viene ricostruito **lineare** fra il margine
    del primo anno, che resta ancorato al dato osservato, e il margine finale
    cercato: il primo anno e' quasi gia' noto e non e' la variabile in gioco,
    mentre e' il punto d'arrivo a cinque anni la vera ipotesi che il prezzo sta
    scontando.
    """
    fermo = _senza_prezzo(inputs, "reverse_margin")
    if fermo:
        return fermo

    ancora = inputs.ebit_margin[0]

    def percorso(finale: float) -> list:
        passi = ORIZZONTE_ANNI - 1
        return [ancora + (finale - ancora) * i / passi for i in range(ORIZZONTE_ANNI)]

    f = _scarto(inputs)(lambda x: replace(inputs, ebit_margin=percorso(x)))
    return _bisezione(f, LIMITI_MARGINE[0], LIMITI_MARGINE[1], "reverse_margin")
