#!/usr/bin/env python3
"""
bond_math.py — Motore di calcolo deterministico per titoli di Stato area euro.

SCOPO
-----
Calcola, da INPUT GIA' VERIFICATI (prezzo, cedola, scadenza, prezzo di carico),
le metriche che servono a valutare un titolo di Stato singolo tenuto a scadenza:

  - rateo (accrued interest) e prezzo tel-quel (dirty)
  - YTM lordo (IRR sul prezzo tel-quel)
  - duration modificata e convexity
  - YTM NETTO (imposta sostitutiva 12,5% su cedole e scarto/plusvalenza per
    white-list; bollo 0,20%/anno; opzione 26% per confronto con strumenti non
    white-list, es. corporate o ETF trattati forfettariamente)
  - YTM reale (netto di un'inflazione attesa dichiarata)

COPIA MADRE — NON DUPLICARE A MANO
---------------------------------
Questo file è la **copia autoritativa** del motore di calcolo. La logica fiscale
che implementa (12,5% white-list, bollo, scarto, rateo) è dottrina di questa
skill e vive in `references/metriche-e-fiscalita.md`: il codice sta accanto alla
dottrina che applica.

Il connettore MCP `finanza` ne tiene una copia **generata**, non sorgente, e la
verifica per impronta a ogni esecuzione dei suoi test. Se modifichi questo file:

  1. incrementa MOTORE_VERSIONE qui sotto;
  2. nel connettore esegui `python3 bin/finanza allinea --applica`, che
     riallinea la copia e ti mostra quali numeri sono cambiati.

Se le due copie divergono, i test del connettore falliscono: la divergenza è
rumorosa per costruzione, non silenziosa.

Versione corrente del motore: vedi la costante MOTORE_VERSIONE definita
sotto, subito dopo gli import. E' una vera variabile di modulo, leggibile
con `import bond_math; bond_math.MOTORE_VERSIONE`.

QUESTO SCRIPT NON SCARICA DATI. Non conosce ISIN, prezzi o rendimenti correnti:
li riceve come argomenti, dopo che sono stati verificati sulle fonti autoritative
(Borsa Italiana, btpfacile, MOT/EuroTLX, KID/prospetto). Non inventare input.

CONVENZIONI E LIMITI (dichiarati, non nascosti)
-----------------------------------------------
  - Day-count: Actual/Actual ICMA. Il rateo si calcola sui giorni EFFETTIVI del
    periodo cedolare reale (181/182/184 giorni secondo i mesi attraversati), non
    su un periodo convenzionale di 365,25/freq giorni. Gli stessi estremi di
    periodo collocano i flussi nel tempo per il calcolo dello YTM, così che la
    convenzione sia una sola in tutto il motore. Per l'importo esatto in fase di
    ordine vale comunque il valore del book/dell'intermediario.
  - Frequenza cedolare: default 2 (BTP/Bund/OAT/Bonos pagano cedole semestrali).
    BOT sono zero-coupon (usare coupon=0). CCTeu sono a tasso variabile: lo YTM
    "a scadenza" non è definito ex-ante (dipende dall'Euribor futuro) -> per i
    variabili questo script NON è appropriato, va usato il rendimento a
    prezzo/margine, non un YTM fisso.
  - Fiscalità plusvalenza: per un titolo comprato SOTTO la pari, l'utile a
    scadenza (100 - prezzo di carico) è tassato al 12,5% per i titoli
    white-list. La ripartizione esatta fra SCARTO DI EMISSIONE (reddito di
    capitale, NON compensabile con minusvalenze) e PLUSVALENZA (reddito diverso,
    compensabile) dipende dal prezzo di EMISSIONE e la calcola il sostituto
    d'imposta: qui si applica il 12,5% sull'intero utile a scadenza e si segnala
    il caveat. Se comprato SOPRA la pari, a scadenza c'è una minusvalenza
    (reddito diverso, compensabile): nessuna imposta sull'utile, il rendimento
    resta guidato dalle cedole.
  - Bollo: 0,20%/anno sul controvalore di deposito. Qui è approssimato come uno
    haircut annuo di 0,20 punti sul rendimento (base 100). Colpisce ALLO STESSO
    MODO bond singoli ed ETF: è neutro nel confronto singolo-vs-ETF, ma va
    comunque sottratto dal rendimento netto assoluto.
  - Il reinvestimento delle cedole allo YTM è l'assunto implicito dell'YTM.
    Per bond a bassa cedola e vita residua breve (<5 anni) l'impatto è
    trascurabile; per cedole alte e vita lunga va dichiarato come assunto.
"""

from __future__ import annotations
import calendar
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional

# ─── versione del motore ───────────────────────────────────────────────────
# Vera variabile di modulo, non una riga dentro il commento: il controllo di
# allineamento del connettore MCP deve poterla leggere da programma.
MOTORE_VERSIONE = "1.1"



# --------------------------------------------------------------------------- #
# Utilità
# --------------------------------------------------------------------------- #

def _year_fraction_periods(settle: date, maturity: date, freq: int) -> float:
    """APPROSSIMATA e NON PIU' USATA da analyze_bond: conservata solo per
    compatibilità con eventuali richiami esterni.

    Usa un periodo convenzionale di 365,25/freq giorni. Il motore usa ora
    `_periodo_cedolare`, che lavora sulle date reali: non introdurre di nuovo
    questa funzione nel percorso di calcolo, o si torna ad avere due modi diversi
    di misurare la stessa cosa.
    """
    days = (maturity - settle).days
    period_days = 365.25 / freq
    return days / period_days


def _aggiungi_mesi(d: date, mesi: int) -> date:
    """Sposta una data di N mesi tenendo il giorno, o l'ultimo giorno del mese."""
    anno = d.year + (d.month - 1 + mesi) // 12
    mese = (d.month - 1 + mesi) % 12 + 1
    giorno = min(d.day, calendar.monthrange(anno, mese)[1])
    return date(anno, mese, giorno)


def _periodo_cedolare(settle: date, last_coupon: date, freq: int) -> tuple[date, date]:
    """Estremi (inizio, fine) del periodo cedolare che contiene `settle`.

    `fine` è la data della prossima cedola. Se `last_coupon` è più vecchia di un
    periodo intero (data stantia passata da chi chiama), si avanza finché il
    periodo contiene davvero la data di regolamento, invece di produrre un rateo
    superiore a una cedola intera.
    """
    passo = max(1, int(round(12 / freq)))
    inizio = last_coupon
    fine = _aggiungi_mesi(inizio, passo)
    for _ in range(400):                      # limite di sicurezza
        if fine > settle:
            break
        inizio, fine = fine, _aggiungi_mesi(fine, passo)
    return inizio, fine


def build_cashflows(coupon_rate_pct: float, n_periods: float, freq: int):
    """
    Costruisce i flussi (t in periodi cedolari, importo su nominale 100).
    L'ultimo periodo può essere frazionario: si genera il coupon a ogni periodo
    intero e il rimborso 100 all'istante finale n_periods.
    """
    c = coupon_rate_pct / freq  # cedola per periodo su nominale 100
    flows = []
    k = 1
    # numero di cedole intere ancora da incassare
    whole = int(round(n_periods)) if abs(n_periods - round(n_periods)) < 1e-6 else int(n_periods)
    # genera cedole ai tempi frazionari coerenti con la scadenza:
    # t_ultimo = n_periods; le cedole cadono a n_periods-1, n_periods-2, ...
    times = []
    t = n_periods
    while t > 1e-9:
        times.append(t)
        t -= 1.0
    times = sorted(times)
    for t in times:
        flows.append((t, c))
    # aggiunge il rimborso del nominale all'ultimo flusso
    if flows:
        t_last, amt = flows[-1]
        flows[-1] = (t_last, amt + 100.0)
    else:
        flows.append((n_periods, 100.0 + c))
    return flows


def price_from_yield(flows, y_per_period: float) -> float:
    """Prezzo tel-quel dato un rendimento per periodo."""
    return sum(cf / (1.0 + y_per_period) ** t for t, cf in flows)


def solve_ytm(dirty_price: float, flows, freq: int) -> float:
    """YTM annuo (nominale, composto freq volte) via bisezione robusta."""
    lo, hi = -0.5 / freq, 1.0 / freq  # rendimento per periodo
    f_lo = price_from_yield(flows, lo) - dirty_price
    f_hi = price_from_yield(flows, hi) - dirty_price
    # espande il bracket se necessario
    tries = 0
    while f_lo * f_hi > 0 and tries < 60:
        hi *= 1.5
        f_hi = price_from_yield(flows, hi) - dirty_price
        tries += 1
    for _ in range(200):
        mid = (lo + hi) / 2
        f_mid = price_from_yield(flows, mid) - dirty_price
        if abs(f_mid) < 1e-10:
            break
        if f_lo * f_mid < 0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    y_per = (lo + hi) / 2
    return y_per * freq  # annualizzato (nominale)


def duration_convexity(flows, y_per_period: float, freq: int):
    """Duration modificata (anni) e convexity (anni^2) sul prezzo tel-quel."""
    price = price_from_yield(flows, y_per_period)
    d_mac_periods = sum(t * cf / (1 + y_per_period) ** t for t, cf in flows) / price
    d_mac_years = d_mac_periods / freq
    d_mod_years = d_mac_years / (1 + y_per_period)
    conv_periods = sum(t * (t + 1) * cf / (1 + y_per_period) ** (t + 2) for t, cf in flows) / price
    conv_years = conv_periods / (freq ** 2)
    return d_mod_years, conv_years


# --------------------------------------------------------------------------- #
# API principale
# --------------------------------------------------------------------------- #

@dataclass
class BondResult:
    clean_price: float
    accrued: float
    dirty_price: float
    years_to_maturity: float
    ytm_gross: float           # %
    mod_duration: float        # anni
    convexity: float           # anni^2
    ytm_net_whitelist: float   # % (12,5% cedole+utile, al netto bollo)
    ytm_net_26: float          # % (26% forfettario, per confronto non-white-list)
    ytm_real: Optional[float]  # % (netto white-list, deflazionato) o None
    notes: list


def analyze_bond(
    clean_price: float,
    coupon_rate_pct: float,
    settle: date,
    maturity: date,
    last_coupon: date,
    purchase_price: Optional[float] = None,
    freq: int = 2,
    inflation_pct: Optional[float] = None,
    bollo_pct: float = 0.20,
) -> BondResult:
    """
    clean_price      : prezzo secco corrente (o di acquisto) su base 100 [VERIFICATO]
    coupon_rate_pct  : cedola ANNUA in % (es. 1.35). 0 per zero-coupon/BOT
    settle           : data di regolamento
    maturity         : data di scadenza
    last_coupon      : data ultima cedola staccata (per il rateo)
    purchase_price   : prezzo di carico per la fiscalità della plus/scarto;
                       se None usa clean_price
    freq             : cedole/anno (2 per BTP/Bund/OAT/Bonos; irrilevante se cedola 0)
    inflation_pct    : inflazione attesa annua per il rendimento reale (opzionale)
    bollo_pct        : bollo annuo (default 0,20)
    """
    notes = []
    if purchase_price is None:
        purchase_price = clean_price

    passo_mesi = max(1, int(round(12 / freq)))
    inizio_periodo, prossima_cedola = _periodo_cedolare(settle, last_coupon, freq)
    giorni_periodo = (prossima_cedola - inizio_periodo).days

    # --- rateo (accrued) — Actual/Actual ICMA ---
    giorni_maturati = max(0, (settle - inizio_periodo).days)
    frac = min(1.0, giorni_maturati / giorni_periodo) if giorni_periodo else 0.0
    accrued = (coupon_rate_pct / freq) * frac
    dirty = clean_price + accrued

    # --- tempo a scadenza in periodi cedolari (ICMA) ---
    # frazione del periodo corrente ancora da correre + periodi interi residui
    frazione_corrente = (
        (prossima_cedola - settle).days / giorni_periodo if giorni_periodo else 0.0
    )
    interi, cursore = 0, prossima_cedola
    for _ in range(2000):                     # limite di sicurezza
        if cursore >= maturity - timedelta(days=3):   # tolleranza fuori schema
            break
        cursore = _aggiungi_mesi(cursore, passo_mesi)
        interi += 1
    n_periods = frazione_corrente + interi
    years = (maturity - settle).days / 365.25

    # --- flussi e YTM lordo ---
    flows = build_cashflows(coupon_rate_pct, n_periods, freq)
    ytm_gross_ann = solve_ytm(dirty, flows, freq)
    y_per = ytm_gross_ann / freq

    # --- duration & convexity ---
    d_mod, conv = duration_convexity(flows, y_per, freq)

    # --- fiscalità: costruisce i flussi NETTI e ricalcola l'IRR ---
    gain = 100.0 - purchase_price  # utile/perdita in conto capitale a scadenza
    def net_ytm(tax_income: float, tax_gain: float) -> float:
        c_net = (coupon_rate_pct / freq) * (1 - tax_income)
        nf = []
        for t, cf in flows:
            base_coupon = coupon_rate_pct / freq
            redemption = cf - base_coupon if abs(cf - base_coupon - 100.0) < 1e-6 else 0.0
            amt = c_net
            if redemption:
                taxed_gain = max(0.0, gain) * tax_gain
                amt = c_net + 100.0 - taxed_gain
            nf.append((t, amt))
        y_net_ann = solve_ytm(dirty, nf, freq)
        # bollo come haircut annuo sul rendimento
        return y_net_ann - bollo_pct / 100.0

    ytm_net_wl = net_ytm(tax_income=0.125, tax_gain=0.125)
    ytm_net_26 = net_ytm(tax_income=0.26, tax_gain=0.26)

    ytm_real = None
    if inflation_pct is not None:
        ytm_real = ((1 + ytm_net_wl) / (1 + inflation_pct / 100.0) - 1) * 100

    if gain > 0:
        notes.append(
            "Comprato sotto la pari: utile a scadenza 12,5% (white-list). Split "
            "scarto/plusvalenza lo determina il sostituto d'imposta; qui 12,5% "
            "sull'intero utile."
        )
    elif gain < 0:
        notes.append(
            "Comprato sopra la pari: a scadenza minusvalenza (reddito diverso, "
            "compensabile entro 4 anni). Nessuna imposta sull'utile in conto capitale."
        )
    if coupon_rate_pct > 0 and years > 5:
        notes.append(
            "Vita residua > 5 anni: l'assunto di reinvestimento cedole allo YTM "
            "pesa; dichiaralo."
        )

    return BondResult(
        clean_price=clean_price,
        accrued=accrued,
        dirty_price=dirty,
        years_to_maturity=years,
        ytm_gross=ytm_gross_ann * 100,
        mod_duration=d_mod,
        convexity=conv,
        ytm_net_whitelist=ytm_net_wl * 100,
        ytm_net_26=ytm_net_26 * 100,
        ytm_real=ytm_real,
        notes=notes,
    )


def price_shock(d_mod: float, conv: float, dy_bps: float) -> float:
    """Variazione % di prezzo per uno shock di rendimento in bps (con convexity)."""
    dy = dy_bps / 10000.0
    return (-d_mod * dy + 0.5 * conv * dy * dy) * 100


# --------------------------------------------------------------------------- #
# Self-test (esegui: python bond_math.py)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    print("=== SELF-TEST 1: par bond, cedola 5% semestrale, 5 anni ===")
    # a par, YTM deve ~ coincidere con la cedola (5%)
    r = analyze_bond(
        clean_price=100.0, coupon_rate_pct=5.0,
        settle=date(2026, 1, 1), maturity=date(2031, 1, 1),
        last_coupon=date(2026, 1, 1), freq=2,
    )
    print(f"YTM lordo  = {r.ytm_gross:.4f}%  (atteso ~5.00%)")
    print(f"Dur.mod    = {r.mod_duration:.3f} anni  (atteso ~4.3-4.5)")
    print(f"Convexity  = {r.convexity:.3f}")
    assert abs(r.ytm_gross - 5.0) < 0.05, "YTM par bond deve ~5%"
    assert 4.0 < r.mod_duration < 4.6, "duration fuori range atteso"

    print("\n=== SELF-TEST 2: zero-coupon (BOT-like) 1 anno a 97 ===")
    r2 = analyze_bond(
        clean_price=97.0, coupon_rate_pct=0.0,
        settle=date(2026, 1, 1), maturity=date(2027, 1, 1),
        last_coupon=date(2026, 1, 1), freq=1,
    )
    # rendimento lordo ~ (100/97 - 1) = 3.09%
    print(f"YTM lordo  = {r2.ytm_gross:.4f}%  (atteso ~3.09%)")
    print(f"YTM netto WL = {r2.ytm_net_whitelist:.4f}%  (12,5% su ~3 di utile - bollo)")
    assert abs(r2.ytm_gross - 3.09) < 0.15

    print("\n=== SELF-TEST 3: sconto profondo tipo Bund 0% ~88, ~5 anni ===")
    r3 = analyze_bond(
        clean_price=88.0, coupon_rate_pct=0.0,
        settle=date(2026, 2, 15), maturity=date(2031, 2, 15),
        last_coupon=date(2026, 2, 15), freq=1,
        purchase_price=88.06, inflation_pct=2.0,
    )
    print(f"YTM lordo    = {r3.ytm_gross:.4f}%")
    print(f"YTM netto WL = {r3.ytm_net_whitelist:.4f}%")
    print(f"YTM reale    = {r3.ytm_real:.4f}%  (deflazionato 2%)")
    print(f"Dur.mod      = {r3.mod_duration:.3f} anni")
    for n in r3.notes:
        print("  nota:", n)

    print("\n=== SELF-TEST 4: shock di prezzo per +100 e +200 bps ===")
    print(f"+100 bps -> {price_shock(r.mod_duration, r.convexity, 100):.2f}%")
    print(f"+200 bps -> {price_shock(r.mod_duration, r.convexity, 200):.2f}%")

    print("\nTutti i self-test passati.")
