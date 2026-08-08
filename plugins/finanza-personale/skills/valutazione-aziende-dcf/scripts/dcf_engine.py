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
MOTORE_VERSIONE = "1.1"

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
    e non si restituisce nessun numero.

    `grandezza` dice **che cosa** misura `value`, perche' non e' la stessa cosa
    per tutti e quattro: dove l'ipotesi e' un punto d'arrivo (un margine, un
    tasso) `value` e' quel punto; dove l'ipotesi e' un percorso di crescita
    `value` e' l'invariante economica — il CAGR implicito dei ricavi — e non uno
    dei tassi annui, che dipendono dalla forma scelta e non dal modello.

    `percorso` e' l'ipotesi anno per anno che realizza la soluzione: serve a
    mostrarla e a rimetterla nel motore per riverificarla. E' un'**illustrazione**
    della grandezza, non il risultato.

    `dettagli` porta le grandezze derivate che il report pubblica accanto a
    `value` (per la crescita: i ricavi finali impliciti).
    """
    value: Optional[float]        # in punti percentuali
    motivo: str
    grandezza: str = ""
    percorso: Optional[list] = None      # list[float], l'ipotesi anno per anno
    dettagli: Optional[dict] = None


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

    if inputs.roic_terminal <= inputs.g_terminal:
        raise DcfError(
            f"roic_terminal ({inputs.roic_terminal}%) <= g_terminal "
            f"({inputs.g_terminal}%): il tasso di reinvestimento g/ROIC diventa "
            f"maggiore o uguale a 1, quindi il fattore (1 - g/ROIC) e' zero o "
            f"negativo e il flusso di cassa terminale va a zero o sotto. E' lo "
            f"stesso caso degenere di wacc <= g_terminal: un'azienda non puo' "
            f"crescere per sempre piu' di quanto renda il capitale che la finanzia. "
            f"Il motore si ferma invece di restituire un valore terminale nullo o "
            f"negativo, che sarebbe un numero plausibile e sbagliato"
        )

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

    Le celle in cui il modello non e' definito valgono `None`: li' non esiste un
    numero, e scriverne uno sarebbe peggio che lasciare il buco. Sono i due casi
    degeneri che `_valida` blocca — WACC che non supera g, e ROIC terminale che
    non supera g — piu' qualunque altro errore di validazione.
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

def _coefficienti_di_forma(valori: list) -> tuple:
    """I coefficienti `c[i]` che descrivono come si muove un percorso di ipotesi
    quando se ne cerca il valore finale. Ritorna `(c, nota)`.

    **Riscalatura degli incrementi sopra il valore ancorato.** Il primo anno resta
    fermo — e' quasi gia' noto, non e' la variabile in gioco — e gli scarti
    `d[i] = valori[i] - valori[0]` vengono moltiplicati per il fattore che porta
    l'ultimo anno all'obiettivo. Quindi `c[i] = d[i] / d[-1]`, e il percorso vale
    `valori[0] + c[i] * (obiettivo - valori[0])`.

    E' la forma che risponde alla domanda giusta: *tenendo ferma l'idea di **come**
    cambia questa grandezza, a quale **livello** deve arrivare*. L'interpolazione
    lineare cambia insieme livello e forma, quindi il risultato non e' piu'
    attribuibile al solo livello, e il percorso su cui e' calcolato non e' quello
    che ha scritto chi ha fatto le ipotesi.

    **Il ripiego.** Il fattore e' indefinito quando `d[-1] == 0`, cioe' quando
    l'ultimo anno coincide con quello ancorato. Sono due situazioni diverse e la
    nota le distingue: il percorso davvero piatto (nessuna forma da conservare) e
    il percorso che *torna al punto di partenza* (una forma c'e', ma non e'
    raggiungibile riscalando). In entrambi i casi si ripiega sui coefficienti
    dell'interpolazione lineare, e **lo si dichiara**: un ripiego silenzioso e' il
    modo peggiore di essere corretti.
    """
    ancora = valori[0]
    d = [x - ancora for x in valori]
    n = len(valori)

    if d[-1] == 0.0:
        c = [i / (n - 1) for i in range(n)]
        if all(x == 0.0 for x in d):
            nota = ("percorso piatto: la forma non porta informazione, ripiegato "
                    "sull'interpolazione lineare")
        else:
            nota = ("il valore dell'ultimo anno coincide con quello ancorato: la forma "
                    "esiste ma non e' riscalabile, ripiegato sull'interpolazione lineare")
        return c, nota

    return [x / d[-1] for x in d], ""


def _intervallo_ammissibile(ancora: float, c: list, lo: float, hi: float) -> tuple:
    """L'insieme degli obiettivi per cui **ogni anno mosso** resta dentro [lo, hi].

    Ogni `percorso[i](T) = ancora + c[i] * (T - ancora)` e' affine in `T`, quindi
    ogni vincolo `lo <= percorso[i](T) <= hi` e' una disuguaglianza lineare e
    l'insieme ammissibile e' un **intervallo, calcolabile in forma chiusa**. Si
    calcola invece di sperare che un controllo a campione lo intercetti.

    Non e' un formalismo: su un percorso quasi piatto (`d[-1] = 0,001`) senza
    questo taglio la riscalatura produce margini al 4560% e un fair value che non
    significa niente. Con il taglio, l'intervallo collassa da solo attorno
    all'ancora e il risolutore dice onestamente che non c'e' spazio.

    Gli anni che il risolutore **non muove** (`c[i] == 0`) non sono vincolati:
    quello ancorato e' un dato di bilancio, non un'ipotesi in cerca, e non tocca
    al reverse DCF contestarlo.
    """
    a, b = lo, hi
    for ci in c:
        if ci == 0.0:
            continue
        x = (lo - ancora) / ci + ancora
        y = (hi - ancora) / ci + ancora
        a, b = max(a, min(x, y)), min(b, max(x, y))
    return a, b


def _bisezione(f, lo: float, hi: float, etichetta: str) -> ReverseResult:
    """Bisezione su f(x) = fair_value(x) - market_price, dentro [lo, hi].

    Se agli estremi la funzione non cambia segno, la soluzione non sta dentro i
    limiti di plausibilita': si restituisce None con la ragione. Non si allarga
    l'intervallo, perche' il limite non e' un dettaglio tecnico della bisezione —
    e' l'affermazione che oltre quel valore l'ipotesi non e' piu' credibile.

    **Prima di bisecare si controlla che la funzione sia monotona**, confrontando
    il verso della pendenza ai due estremi. La bisezione presuppone la monotonia:
    su una funzione con un massimo interno trova una radice e non vede l'altra, e
    pubblicherebbe *«il prezzo sta scontando il X%»* mentre i valori compatibili
    sono due. Peggio: con un massimo interno i due estremi possono stare **dalla
    stessa parte** del prezzo mentre in mezzo ci sono due soluzioni, e la risposta
    «nessuna soluzione» sarebbe falsa.
    """
    if hi <= lo:
        return ReverseResult(
            None,
            f"{etichetta}: non resta nessun intervallo ammissibile ({lo:g} .. {hi:g}). "
            f"Fuori da questo intervallo il percorso uscirebbe dai limiti di "
            f"plausibilita' in uno degli anni intermedi"
        )

    try:
        f_lo, f_hi = f(lo), f(hi)
    except DcfError as ex:
        return ReverseResult(None, f"{etichetta}: agli estremi il modello non e' definito ({ex})")

    if f_lo is None or f_hi is None:
        return ReverseResult(None, f"{etichetta}: manca il prezzo di mercato, non c'e' niente da azzerare")

    # Monotonia: il verso della pendenza ai due estremi deve essere lo stesso.
    # Intercetta il massimo (o minimo) interno, che e' il caso economicamente
    # significativo — non ogni patologia immaginabile: una funzione con due
    # estremi interni puo' avere lo stesso verso ai bordi. E' un controllo a
    # basso costo su un difetto reale, non una dimostrazione.
    passo = (hi - lo) * 1e-3
    try:
        pend_lo = f(lo + passo) - f_lo
        pend_hi = f_hi - f(hi - passo)
        if pend_lo * pend_hi < 0:
            return ReverseResult(
                None,
                f"{etichetta}: esistono piu' valori compatibili con questo prezzo. "
                f"Fra {lo:g} e {hi:g} il fair value non e' monotono — sale e poi scende "
                f"(o viceversa) — quindi la domanda 'quale valore sta scontando il "
                f"prezzo' non ha una risposta sola, e darne una sarebbe sceglierne "
                f"arbitrariamente una delle due"
            )
    except DcfError:
        pass          # non decidibile qui: decidono i controlli sugli estremi

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


def _cagr_ricavi(inputs: DcfInputs, percorso: list) -> tuple:
    """(CAGR implicito in punti percentuali, ricavi dell'ultimo anno) dato un
    percorso di crescita. E' l'invariante economica del reverse sulla crescita."""
    r = inputs.revenue_base
    for g in percorso:
        r *= (1.0 + g / 100.0)
    cagr = ((r / inputs.revenue_base) ** (1.0 / len(percorso)) - 1.0) * 100.0
    return cagr, r


def _rifinisci(esito: ReverseResult, valori: list, percorso, nota_forma: str,
               grandezza: str, converti=None) -> ReverseResult:
    """Completa l'esito di un risolutore che muove un percorso: allega il
    percorso risolto, la nota permanente sulla forma, e l'eventuale nota sul
    fattore negativo. Le note stanno **davanti** alla motivazione tecnica, e ci
    stanno anche quando il risolutore converge: un ripiego dichiarato solo in
    caso di fallimento sarebbe dichiarato proprio quando serve di meno.

    `converti`, se presente, trasforma l'obiettivo risolto nella grandezza da
    pubblicare (per la crescita: il CAGR implicito) e restituisce anche i
    dettagli derivati.
    """
    note = [nota_forma] if nota_forma else []
    risolto = esito.value
    p = dettagli = None
    valore = risolto

    if risolto is not None:
        p = percorso(risolto)
        d_finale = valori[-1] - valori[0]
        if d_finale != 0.0 and (risolto - valori[0]) / d_finale < 0:
            note.append("l'obiettivo sta dall'altra parte del valore ancorato: la forma "
                        "del percorso e' conservata e specchiata")
        if converti is not None:
            valore, dettagli = converti(p, risolto)

    motivo = " | ".join(note + [esito.motivo]) if note else esito.motivo
    return ReverseResult(valore, motivo, grandezza=grandezza, percorso=p, dettagli=dettagli)


def reverse_growth(inputs: DcfInputs) -> ReverseResult:
    """Che cosa il prezzo sta assumendo sui ricavi.

    **La grandezza pubblicata e' il CAGR implicito dei ricavi**, con i ricavi
    finali impliciti accanto; il percorso anno per anno resta visibile come
    illustrazione. Non e' una scelta di gusto: quattro modi ragionevoli di far
    variare il percorso danno tassi annui che vanno dal 41,7% al 62,9% — oltre
    venti punti — e ricavi finali fra 12.647 e 12.886 milioni, cioe' mezzo punto
    di CAGR. **Il modello e' guidato dai ricavi cumulati, non dalla forma**, e
    pubblicare il tasso annuo significherebbe pubblicare l'unica grandezza che
    dipende da una convenzione nostra invece che dal mercato.

    Il percorso si muove per riscalatura degli incrementi (vedi
    `_coefficienti_di_forma`) con il **primo anno ancorato**. Nel caso di
    riferimento il primo anno e' il 106% del 2026, che non e' una tendenza ma
    l'ingresso a regime di due acquisizioni: spalmarlo su cinque anni, come
    faceva la versione uniforme, distrugge il significato dell'ipotesi e produce
    una frase che nessuno ha mai assunto.
    """
    fermo = _senza_prezzo(inputs, "reverse_growth")
    if fermo:
        return fermo

    ancora = inputs.growth[0]
    c, nota = _coefficienti_di_forma(inputs.growth)
    lo, hi = _intervallo_ammissibile(ancora, c, LIMITI_CRESCITA[0], LIMITI_CRESCITA[1])
    percorso = lambda x: [ancora + ci * (x - ancora) for ci in c]  # noqa: E731

    f = _scarto(inputs)(lambda x: replace(inputs, growth=percorso(x)))
    esito = _bisezione(f, lo, hi, "reverse_growth")

    def converti(p, risolto):
        cagr, ricavi = _cagr_ricavi(inputs, p)
        return cagr, {"ricavi_finali": ricavi,
                      "ricavi_base": inputs.revenue_base,
                      "crescita_ultimo_anno": risolto,
                      "anno_finale": inputs.year_base + ORIZZONTE_ANNI}

    return _rifinisci(esito, inputs.growth, percorso, nota,
                      "CAGR implicito dei ricavi", converti)


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
    esito = _bisezione(f, LIMITI_G_TERMINALE[0], hi, "reverse_g_terminal")
    return replace(esito, grandezza="crescita perpetua implicita")


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
    esito = _bisezione(f, lo, LIMITI_WACC[1], "reverse_wacc")
    return replace(esito, grandezza="costo del capitale implicito")


def reverse_margin(inputs: DcfInputs) -> ReverseResult:
    """Il margine EBIT del quinto anno che azzera l'upside.

    Il primo anno resta **ancorato** al dato osservato e gli anni intermedi si
    muovono per **riscalatura degli incrementi** (vedi `_coefficienti_di_forma`):
    la forma del miglioramento che hai scritto viene conservata, e a cambiare e'
    solo il livello d'arrivo. Con il percorso di riferimento `22 · 26 · 29 · 31 ·
    33`, cercando un margine finale del 45% si ottiene `22 · 30,36 · 36,64 ·
    40,82 · 45` — concavo come l'originale — invece della rampa a passo costante
    `22 · 27,75 · 33,5 · 39,25 · 45` che dava l'interpolazione lineare.

    **Qui la grandezza pubblicata resta il valore risolto**, al contrario di
    `reverse_growth`: un margine e' un punto d'arrivo, non un tasso annuo, e
    infatti fra le tre convenzioni possibili (lineare, riscalata, traslata) il
    margine risolto varia dell'1-9% contro il 42% del tasso di crescita.
    """
    fermo = _senza_prezzo(inputs, "reverse_margin")
    if fermo:
        return fermo

    ancora = inputs.ebit_margin[0]
    c, nota = _coefficienti_di_forma(inputs.ebit_margin)
    lo, hi = _intervallo_ammissibile(ancora, c, LIMITI_MARGINE[0], LIMITI_MARGINE[1])
    percorso = lambda x: [ancora + ci * (x - ancora) for ci in c]  # noqa: E731

    f = _scarto(inputs)(lambda x: replace(inputs, ebit_margin=percorso(x)))
    esito = _bisezione(f, lo, hi, "reverse_margin")

    return _rifinisci(esito, inputs.ebit_margin, percorso, nota,
                      "margine EBIT dell'ultimo anno esplicito")
