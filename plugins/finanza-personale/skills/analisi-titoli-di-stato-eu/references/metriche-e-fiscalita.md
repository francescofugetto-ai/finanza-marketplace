# Metriche e fiscalità dei titoli di Stato area euro

Come si passa da un prezzo verificato a un **rendimento netto e reale** utilizzabile, e come si misurano rischio-tasso (duration, convexity) e rendimento di carry/roll-down. Usa `scripts/bond_math.py` per i calcoli deterministici — non rifare l'aritmetica a mano.

## Indice
1. Prezzo secco, rateo, tel-quel
2. YTM lordo (meccanica e assunti)
3. Fiscalità: 12,5% / 26%, white-list, scarto vs plusvalenza, minus/plus, bollo
4. YTM netto e YTM reale
5. Duration modificata e convexity
6. Carry e roll-down
7. Casi speciali: BOT/zero-coupon, CCTeu variabili, inflation-linked
8. Uso dello script

---

## 1. Prezzo secco, rateo, tel-quel

- **Prezzo secco (clean):** quotazione "pulita", senza interessi maturati. È quello quotato sul mercato.
- **Rateo (accrued):** cedola maturata e non ancora incassata, proporzionale ai giorni dall'ultimo stacco. Per i BTP la convenzione è **Actual/Actual ICMA**.
- **Prezzo tel-quel (dirty):** `secco + rateo`. È quello che **paghi davvero** e su cui si calcola lo YTM.

Il rateo si paga a chi vende (ha maturato quella cedola) e si recupera al successivo stacco: non è un costo, ma va incluso nel prezzo di acquisto effettivo e nel calcolo del rendimento.

## 2. YTM lordo (yield to maturity)

Lo YTM è il **tasso interno di rendimento (IRR)** che eguaglia il prezzo tel-quel al valore attuale di tutti i flussi futuri (cedole + rimborso). Si risolve numericamente (nello script, per bisezione robusta).

**Assunti da dichiarare sempre:**
- **Reinvestimento delle cedole allo stesso YTM.** Si realizza solo se le cedole vengono reinvestite a quel tasso. Per i titoli del mandato (vita residua ~2-5 anni, cedole basse) l'impatto è **trascurabile**; per cedole alte e vita lunga va segnalato.
- **Detenzione a scadenza.** Lo YTM è l'esito *se tieni a scadenza*. Se vendi prima, l'esito dipende dal prezzo di vendita (rischio-prezzo).
- **Nessun default.** Presuppone il rimborso alla pari.

Non confondere lo YTM con la **cedola** (tasso nominale sul valore facciale) né con il **rendimento immediato** (cedola/prezzo): a prezzi diversi da 100 sono numeri diversi. Su un titolo comprato **sotto la pari**, lo YTM > cedola (c'è il pull-to-par); **sopra la pari**, YTM < cedola.

## 3. Fiscalità

### Aliquote
- **12,5%** (imposta sostitutiva) su **titoli di Stato italiani** e **titoli di Stato di Paesi white-list** (D.Lgs. 239/1996; white-list DM 4/9/1996 e succ.), oltre a sovranazionali equiparati. **Include** i governativi di **Germania (Bund), Francia (OAT), Spagna (Bonos)** e degli altri Paesi white-list: **non è un privilegio solo dei BTP**. È l'errore più comune da intercettare.
- **26%** su tutto il resto: obbligazioni corporate, ETF/OICR armonizzati, e in generale gli strumenti non white-list.

Verifica la white-list se hai il minimo dubbio sull'emittente; i major EU sovereign (IT, DE, FR, ES) e l'Italia stessa sono white-list.

### Componenti tassate su un titolo tenuto a scadenza
1. **Cedole** → reddito di capitale, 12,5% (white-list). **Non compensabili** con minusvalenze pregresse.
2. **Scarto di emissione** = differenza tra il valore di rimborso (100) e il **prezzo di emissione**, maturata pro rata temporis → reddito di capitale, 12,5%. **Non compensabile.**
3. **Plusvalenza/minusvalenza** = differenza tra prezzo di acquisto e prezzo di vendita/rimborso, **al netto** della quota di scarto già maturata → reddito diverso, 12,5% (white-list) sulla plus; la **minus è compensabile** entro il 4° anno successivo con altri redditi diversi.

Conseguenza operativa: su un titolo comprato **molto sotto la pari** (nel portafoglio: Bund a ~88, BTP a ~93-95), l'utile a scadenza `(100 − prezzo di carico)` è grande e tassato al **12,5%**. La ripartizione esatta scarto/plusvalenza dipende dal **prezzo di emissione** e la calcola il **sostituto d'imposta** (il broker in regime amministrato): ai fini della stima usa il 12,5% sull'intero utile e segnala il caveat. Se comprato **sopra la pari**, a scadenza c'è una **minusvalenza** (compensabile), nessuna imposta sull'utile in conto capitale.

> **Nota su minus/plus (leva per il decumulo):** poiché la plusvalenza da prezzo è *reddito diverso* compensabile, in un portafoglio con più titoli si può gestire il *timing* delle realizzazioni per compensare minus e plus entro i 4 anni. Lo scarto e le cedole (redditi di capitale) **non** si compensano. Segnala questa asimmetria quando rilevante; il calcolo esatto lo fa l'intermediario.

### Bollo titoli
**0,20%/anno** (2‰) sul controvalore di deposito, addebitato pro-quota dall'intermediario. **Colpisce identicamente bond singoli ed ETF** → è **neutro** nel confronto singolo-vs-ETF, ma va **comunque sottratto** dal rendimento netto assoluto. Nello script è approssimato come haircut di 0,20 punti annui sul rendimento.

### Confronto fiscale bond singolo vs ETF governativo (sintesi)
- **Bond singolo white-list:** 12,5% **pieno e certo** su cedole e utile a scadenza; nessun TER; scadenza definita.
- **ETF governativo white-list:** l'utile è *reddito di capitale* tassato al **26%**, con **riduzione** della base imponibile al **48,08%** sulla **quota-parte** attribuibile ai titoli white-list (26% × 48,08% ≈ 12,5% *effettivo* su quella quota). Ma: dipende dal corretto reporting del fondo, si applica **solo** alla quota white-list (non a roll/tracking/altre componenti), e l'ETF ha **TER** e **duration perpetua**. Anche l'ETF paga il bollo 0,20%.

Morale: per un ETF governativo euro *puro* la fiscalità è *vicina* al 12,5% effettivo, ma il singolo elimina la dipendenza dal pass-through, il TER e l'incertezza della scadenza. Il vantaggio del singolo è **certezza + semplicità + nessun TER + maturità definita**, non un divario di 13,5 punti su tutto (affermarlo sarebbe sbagliato: non farlo).

## 4. YTM netto e YTM reale

- **YTM netto (white-list):** ricalcola l'IRR sui **flussi netti** — cedole ×(1−0,125), rimborso 100 − 0,125×max(0, 100−prezzo di carico) — e sottrai il bollo (0,20 p.a.). Lo fa lo script.
- **YTM netto 26%:** stessa cosa con 0,26 — utile solo per confronto con strumenti non white-list.
- **YTM reale:** deflaziona il netto con l'**inflazione attesa dichiarata** (es. HICP atteso): `(1+netto)/(1+inflazione) − 1`. **È il numero che conta** per un mandato di preservazione del potere d'acquisto. Dichiara sempre l'ipotesi d'inflazione usata (fonte: break-even di mercato, consensus BCE).

## 5. Duration modificata e convexity

- **Duration di Macaulay:** vita media finanziaria (media dei tempi dei flussi, pesata per il valore attuale).
- **Duration modificata (`D_mod`):** `Macaulay / (1+y)`; approssima la sensibilità del prezzo ai tassi: `ΔP% ≈ −D_mod × Δy`. Es. `D_mod = 4` → +100 bps ≈ −4%.
- **Convexity (`C`):** correzione del second'ordine: `ΔP% ≈ −D_mod×Δy + ½×C×(Δy)²`. È **positiva** per i bond plain vanilla → attenua le perdite sui rialzi e amplifica i guadagni sui cali (per +200 bps la perdita è **meno** del doppio di quella a +100 bps). Su vite brevi (2-5 anni) è piccola ma va inclusa negli scenari ±200 bps.
- **DV01/PVBP:** variazione di valore in € per −1 bp; utile per sommare il rischio-tasso dell'intera ladder (aggrega i DV01 dei singoli).

Regola operativa del mandato: la duration di ciascun titolo **riflette l'orizzonte del flusso** che copre, non una vista sui tassi. La duration *aggregata* della gamba difensiva va tenuta coerente col cap di perdita (verifica con lo scenario ±100/±200 bps).

## 6. Carry e roll-down

Il rendimento atteso di breve di tenere un bond, a curva invariata, ha due pezzi:
- **Carry** = cedola/rateo che matura (il rendimento "che scorre" per il solo passare del tempo).
- **Roll-down** = guadagno di prezzo perché, invecchiando, il titolo "scivola" verso scadenze a rendimento più basso su una **curva inclinata positivamente** (roll-down positivo). Su curva piatta il roll-down è ~nullo; su curva **invertita** è **negativo** (scivoli verso rendimenti più alti → prezzo giù).

**Carry + roll-down** è la bussola per scegliere *dove* sulla curva piazzare un nuovo acquisto a parità di orizzonte del flusso: si preferisce il tratto con miglior carry+roll netto **per unità di duration/rischio**, senza per questo allungare la scadenza oltre il bisogno (sarebbe market timing). Vedi `curva-e-contesto.md`.

## 7. Casi speciali

- **BOT / zero-coupon:** nessuna cedola; il rendimento è tutto scarto (100 − prezzo). Nello script: `coupon=0`. Tassazione 12,5% sullo scarto. Duration ≈ vita residua.
- **CCTeu (tasso variabile, Euribor 6m + spread):** **NON** hanno uno YTM fisso ex-ante (dipende dall'Euribor futuro). Duration ≈ 0 (si resetta a ogni cedola) → prezzo molto stabile. Valuta col **rendimento a prezzo/margine**, non con un IRR fisso. Funzione: parcheggio a bassa volatilità con tassazione **12,5%** — alternativa white-list a un ETF monetario (26%). Non usare lo script YTM-fisso per i CCTeu.
- **Inflation-linked (BTP€i, BTP Italia):** capitale e cedole rivalutati con l'inflazione (HICP ex-tabacco per i BTP€i; FOI per i BTP Italia). Tenuti a scadenza **bloccano i flussi reali** (cosa che un IL-*ETF* non fa). Prezzo scontato al **tasso reale**: se i tassi reali salgono, il prezzo scende **nonostante** l'inflazione (persi >15% degli IL euro mar-ott 2022). Confronto con un nominale via **break-even inflation**: conviene l'IL solo se l'inflazione *realizzata* supera quella *prezzata*. Dettagli in `strumenti-ammessi-e-confronto.md`.

## 8. Uso dello script

```
from scripts.bond_math import analyze_bond, price_shock
from datetime import date

r = analyze_bond(
    clean_price=94.60,          # VERIFICATO sul book
    coupon_rate_pct=1.35,       # cedola annua %
    settle=date(2026, 7, 4),
    maturity=date(2030, 4, 1),  # VERIFICATO
    last_coupon=date(2026, 4, 1),
    purchase_price=93.845,      # prezzo di carico (per la fiscalità)
    freq=2,                     # BTP: semestrale
    inflation_pct=2.0,          # ipotesi HICP dichiarata
)
# r.ytm_gross, r.ytm_net_whitelist, r.ytm_real, r.mod_duration, r.convexity, r.notes
print(price_shock(r.mod_duration, r.convexity, 200))  # shock +200 bps
```

Lo script **riceve input già verificati** e non scarica nulla. Se non hai un input verificato, non inventarlo: dichiaralo come mancante.
