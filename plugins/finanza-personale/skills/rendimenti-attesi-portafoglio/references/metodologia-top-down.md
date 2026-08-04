# Metodologia TOP-DOWN

Il rendimento atteso di lungo periodo si **estrae dai prezzi di oggi**, per gli asset che pagano flussi di cassa. Base dottrinale: `consulenza-portafogli-etf/references/canone-the-bull/rendimenti-attesi.md` `[TB-339]`; radice accademica: Ilmanen (*Expected Returns*, 2011; *Investing Amid Low Expected Returns*, 2022), Gordon, Fama.

---

## 1. Azioni

### 1.1 Formula base

```
E[r]_reale = DY + g + ΔV        con  ΔV ≡ 0  (per convenzione dichiarata)
E[r]_nom   = (1 + E[r]_reale) × (1 + π) − 1     ≈  E[r]_reale + π
```

| Termine | Cos'è | Come si ottiene | Natura |
|---|---|---|---|
| `DY` | dividend yield corrente dell'indice | **osservato** su factsheet | fatto |
| `g` | crescita **reale** degli utili/FCF **per azione** | **assunto**, con fonte e data | unica stima |
| `ΔV` | variazione dei multipli sull'orizzonte | **posto a 0** | scommessa rimossa |
| `π` | inflazione attesa nella **valuta dell'investitore** | osservata da breakeven/survey | quasi-fatto |

Usa la forma moltiplicativa quando la somma supera ~8% o quando π > 3%: la forma additiva sottostima.

**Perché ΔV = 0 e non un valore stimato.** Nessuno sa se fra dieci anni i multipli saranno più alti o più bassi; è l'unico termine mai previsto con costanza, ed è ciò che rende la correlazione stima-realizzato ~0,5 anziché ~1. Porlo a zero non è pigrizia: è **rimuovere la scommessa** dal calcolo. Se qualcuno vuole vedere l'effetto di un mean-reversion dei multipli, va mostrato come **scenario separato ed etichettato**, mai incorporato nel caso base.

> Formula dello scenario (solo se richiesto esplicitamente):
> `ΔV_annuo = (P/E_target / P/E_oggi)^(1/T) − 1`.
> Es. P/E fwd 21,4 → 17,0 su 10 anni ⇒ `(17,0/21,4)^0,1 − 1 = −2,27%/anno`. Etichettare come **assunzione forte**.

### 1.2 ⚠️ Convenzione: per-azione **oppure** aggregata. Mai entrambe

Due decomposizioni equivalenti, **non miscelabili**:

- **(A) per-azione** — `DY + g(EPS per azione)`. La `g` per azione **incorpora già** i buyback netti.
- **(B) aggregata** — `DY + NBY + g(utili aggregati)`, con `NBY` = net buyback yield (riacquisti − emissioni).

`DY + NBY + g(EPS per azione)` **conta due volte i buyback** ed è l'errore più comune in questo calcolo.

**Default della skill: convenzione (A)**, perché è quella delle stime AQR/CMA disponibili e quella usata in `[TB-339]`. Dichiararla sempre nel report.

**Corollario mercati emergenti** (`[TB-313]`): negli EM il saldo netto è storicamente in **emissione** (diluizione: nuove emissioni, controllo statale). Gli utili *aggregati* crescono molto più di quelli *per azione* — è la ragione per cui la Cina ha moltiplicato ×27 il PIL nominale in 30 anni sottoperformando l'MSCI World. **Non usare mai la crescita del PIL né gli utili aggregati come proxy di `g`.**

### 1.3 Come scegliere `g`

Ordine di preferenza:

1. **CMA di una casa che dichiara la crescita reale per azione** (AQR, Research Affiliates, JPM LTCMA). Cita casa, anno, mercato.
2. **Ancora storica**: **1-2 pt/anno reali** per azione nei mercati sviluppati. È il default prudente.
3. **Mai** l'estrapolazione della crescita recente: la fase post-Covid è eccezionale e proiettarla è "irrealistico e poco prudente" `[TB-339]`, coerente con `[TB-318]`.

Concessione ammessa: stime moderatamente sopra l'ancora storica (2,5-2,7%) sono difendibili se motivate dal miglioramento strutturale della qualità dei profitti (aziende meno capital-heavy, più profittevoli).

**Sensitivity obbligatoria**: rigira sempre con `g ± 1 pt` e mostra il range. È l'unica assunzione del modello: se il risultato non regge a ±1 pt di crescita, il risultato non regge.

### 1.4 Valuta — correzione assente nella fonte, obbligatoria qui

DY e `g` sono in **valuta locale/USD**. L'investitore è in **EUR**.

- **In termini reali la stima è ~valuta-neutra.** Sotto PPP relativa, la deriva attesa del cambio compensa il differenziale d'inflazione: `E[ΔFX] ≈ π_EUR − π_estera`. Su 10 anni è l'assunzione difendibile di default (nessuno stima la deriva valutaria a 10 anni meglio di zero).
- **Quindi**: calcola in **reale** e converti in nominale aggiungendo **l'inflazione dell'area euro**, non quella USA.
- `[TB-339]` aggiunge 2,5% (Cleveland Fed, inflazione **USA**) a tutti i mercati. Per un investitore in euro **è la variabile sbagliata**: va usata l'attesa d'inflazione **euro** (SPF BCE / swap 5y5y). Errore tipico 0,2-0,5 pt.
- Il **rischio** di cambio resta e non sparisce: non è nel rendimento *atteso*, è nella **volatilità**. Va detto e va nella Monte Carlo, non qui.
- Non applicare mai una copertura implicita all'azionario: sull'equity il canone non copre il cambio.

---

## 2. Obbligazioni

### 2.1 Formula base (ETF a duration costante)

```
E[r]_nom_locale = YTW + roll_down − perdita_attesa_credito
E[r]_nom_EUR    = E[r]_nom_locale + carry_di_copertura      (solo se EUR-hedged)
E[r]_reale      = (1 + E[r]_nom_EUR) / (1 + π_EUR) − 1
```

**Validità**: su orizzonte ≈ **duration di Macaulay**, non scadenza media. Sono numeri diversi (Vanguard Euro Aggregate Treasury al 30/06/2026: scadenza media 8,6 anni, **duration 7,0**). È il punto in cui l'effetto prezzo e l'effetto reinvestimento si compensano. Oltre la duration riemerge il rischio di reinvestimento; sotto, domina il rischio prezzo.

**Metrica**: **yield to worst** se il paniere contiene callable; YTM se non li contiene (per i governativi euro coincidono).

**Potenza del metodo**: lo yield di partenza spiega **~89-90%** della varianza dei rendimenti realizzati nei 5-10 anni successivi. Qui il top-down non è "più robusto": è quasi deterministico.

### 2.2 Roll-down

Su una curva positivamente inclinata, un portafoglio a duration costante guadagna un extra rotolando lungo la curva:

```
roll_down ≈ (y_scadenza_n − y_scadenza_(n−1)) × duration_modificata
```

- **Default prudente: 0.** Includilo solo se hai i due punti di curva. Con curva piatta è ~0; con curva **invertita è negativo**.
- Ordine di grandezza tipico su curva normale: +0,1 / +0,4 pt.

### 2.3 Perdita attesa da credito — assente nella fonte, obbligatoria qui

Lo YTW **non è** il rendimento atteso di un paniere con rischio di credito: è il rendimento *promesso*. Sottrarre la perdita attesa:

```
perdita_attesa ≈ tasso_default_annuo × (1 − tasso_recupero)
```

Ordini di grandezza indicativi (**verificare live**, es. rapporti annuali Moody's/S&P):

| Segmento | Perdita attesa annua indicativa |
|---|---|
| Governativi area euro core (DE, NL, AT, FI) | ~0 |
| Governativi area euro periferici (IT, ES, PT) | ~0 sul default, **ma** rischio spread/ridenominazione non prezzabile come perdita attesa (`[TB-187]`: 2011, spread +570 bps) |
| Corporate IG | ~0,05-0,15 pt |
| High Yield | ~2-3 pt |
| Debito emergente in valuta forte | ~0,5-1,5 pt |

Se non la sottrai su un paniere HY, stai sovrastimando di 2-3 punti.

### 2.4 Copertura del cambio — assente nella fonte, obbligatoria qui

Per un paniere in valuta estera **coperto in EUR** (es. Global Aggregate EUR-hedged, il default del canone `[TB-318]`), lo YTM pubblicato è quello **locale**. Il rendimento in euro è, per parità coperta dei tassi d'interesse:

```
E[r]_EUR ≈ YTM_locale + (r_breve_EUR − r_breve_valuta_estera)
```

Con €STR sotto i tassi USA, coprire un paniere in USD **costa** il differenziale: un Global Aggregate con YTM locale 4,5% e differenziale −1,7 pt rende in euro ~2,8%, **non 4,5%**. Ignorarlo sovrastima di 1,5-2 punti — l'errore più grosso possibile su questa gamba.

Fonti del differenziale: tassi overnight/forward BCE (€STR) e Fed (SOFR), o direttamente lo *yield to maturity hedged* se l'emittente lo pubblica (alcuni lo fanno: preferirlo).

**Paniere non coperto in valuta estera**: non si stima e non si propone — il canone lo esclude (`P4` §sintesi: il movimento valutario domina e annulla la funzione difensiva).

### 2.5 Singoli titoli di Stato

Se la gamba è in **singoli BTP/Bund tenuti a scadenza**, il rendimento non è una stima: è lo **YTM netto** al prezzo d'acquisto. Delegare a `analisi-titoli-di-stato-eu` (che gestisce imposta 12,5%, scarto d'emissione, rateo, bollo) e importarlo come input certo.

---

## 3. I quattro strati (obbligatori nel report)

```
STRATO 1  lordo reale        = DY + g              |  YTW_reale
STRATO 2  lordo nominale     = strato 1 + π        |  YTW + roll − credito ± hedge
STRATO 3  netto costi        = strato 2 − TER − bollo 0,20%
STRATO 4  netto fisco        = tassazione applicata AL TERMINE sul guadagno
```

### 3.1 Costi: sottrazione annua

- **TER**: sottrazione diretta dal rendimento annuo. Usa la **tracking difference** se disponibile — spesso più bassa del TER (es. iShares Core S&P 500: TER 0,07%, TD storica **negativa**).
- **Bollo/IVAFE 0,20% annuo**: è un'imposta **patrimoniale** sul controvalore, quindi **sottrae 0,20 punti pieni** dal rendimento annuo, non lo 0,20% del guadagno. Su un bond al 3,11% erode oltre il **6%** del rendimento. Va sempre in conto.

### 3.2 Fisco: **al termine**, non annuo

Errore diffuso: moltiplicare il rendimento annuo per `(1 − aliquota)`. È sbagliato in accumulo: la plusvalenza è tassata **alla realizzazione**, quindi l'imposta è **differita** e nel frattempo capitalizza anche la quota che poi andrà al fisco.

```
montante_lordo   = (1 + r_netto_costi)^T
montante_netto   = 1 + (montante_lordo − 1) × (1 − aliquota)
r_netto_annuo    = montante_netto^(1/T) − 1
```

Aliquote Italia (verificare vigenza; base: art. 44 e 67 TUIR — DPR 917/1986; D.Lgs. 461/1997; DL 66/2014 art. 3):
- **ETF armonizzati UCITS**: 26%. Redditi da OICR: i proventi positivi sono **redditi di capitale**, le perdite **redditi diversi** ⇒ asimmetria nota, le minusvalenze da ETF non compensano le plusvalenze da ETF (compensabili solo con redditi diversi: azioni, obbligazioni, certificati). **Segnalarlo sempre**: è un costo fiscale implicito che va nel confronto fra un portafoglio multi-ETF ribilanciato per vendita e uno ribilanciato per versamento.
- **Titoli di Stato white-list ed equiparati**: **12,5%**, ottenuti tramite abbattimento della base imponibile al 48,08%.
- **ETF obbligazionari con quota governativa white-list**: aliquota effettiva **mista**, proporzionale alla quota — l'ETF/intermediario dichiara periodicamente la percentuale. Per un ETF 100% governativo area euro l'effettiva tende a 12,5%. **Non darlo per scontato**: verificare la quota dichiarata.

Effetto netto: **il differimento vale**, e vale di più su orizzonti lunghi e rendimenti alti. Su 25 anni al 6% lordo, l'aliquota effettiva annua equivalente è sensibilmente sotto il 26% nominale — lo script lo calcola.

---

## 4. Aggregazione di portafoglio

### 4.1 Copertura e rinormalizzazione

```
copertura = Σ pesi(equity) + Σ pesi(bond)
peso_rinormalizzato_i = peso_i / copertura
E[r]_portafoglio = Σ peso_rinormalizzato_i × E[r]_i
```

**Dichiarare sempre la copertura.** Un portafoglio 70/15/15 con 15% di oro ha copertura **85%**: la stima vale su quell'85%, e va detto.

Sul residuo non stimabile: al più una **banda di scenario** su valori dichiarati (es. oro reale 0% / +2% / +4%) mostrata come sensitivity, **mai** come componente della stima puntuale. Il fatto che due case su cinque pubblichino un numero per l'oro non lo rende stimabile: è opinione, non rendimento implicito.

### 4.2 Media semplice vs correzione geometrica

Il default (e il metodo di `[TB-339]`) è la **media pesata semplice**: `Σ w_i × E[r]_i`. È l'headline number, ed è giusto tenerlo perché è quello riproducibile a mano.

Ma le stime `DY+g` e `YTW` sono rendimenti **composti (geometrici)**, e la media pesata di rendimenti geometrici **sottostima** il rendimento di un portafoglio ribilanciato fra asset imperfettamente correlati (bonus di ribilanciamento). Correzione di second'ordine, da mostrare accanto — **mai al posto** — dell'headline:

```
μ_i^arit ≈ g_i + σ_i²/2                     (da geometrico ad aritmetico)
μ_p^arit  = Σ w_i × μ_i^arit
σ_p²      = Σ_i Σ_j w_i w_j σ_i σ_j ρ_ij
g_p       ≈ μ_p^arit − σ_p²/2               (da aritmetico a geometrico)
bonus     = g_p − Σ w_i g_i                 (tipicamente +0,1 / +0,4 pt)
```

Richiede volatilità e matrice di correlazione: usa quelle di `simulazione-montecarlo/references/assunzioni.md`, dichiarandole come assunzioni. Se non le hai, **salta la correzione** e dichiara che l'headline è una media semplice (leggermente prudente).

> **Handoff canonico:** la via rigorosa non è raffinare la media a mano, è **passare gli `exp_return` per asset alla skill `simulazione-montecarlo`**, che simula gli asset separatamente con shock correlati e ribilanciamento e restituisce la distribuzione completa. Questa skill produce i **parametri**; quella produce la **distribuzione**.

### 4.3 Dal rendimento atteso al capitale terminale

Il delta annuo va **sempre** tradotto in montante, perché è lì che si vede se conta:

```
moltiplicatore = (1 + r_netto)^T
```

Riferimento mentale: **2 punti percentuali di differenza** (5% vs 3%) valgono **−17,5%** di capitale su 10 anni e **−38,2%** su 25. Nessuna differenza di rendimento atteso è "solo" qualche punto.

---

## 5. Errori da non commettere (checklist)

1. Mischiare convenzione per-azione e aggregata (doppio conteggio dei buyback).
2. Usare la crescita del **PIL** o degli **utili aggregati** come `g`, specie sugli EM.
3. Aggiungere l'inflazione **USA** a un portafoglio di un investitore **euro**.
4. Usare lo **YTM locale** di un paniere EUR-hedged senza il carry di copertura.
5. Usare **scadenza media** al posto della **duration** come orizzonte di validità.
6. Dimenticare la **perdita attesa da credito** su IG/HY/EM debt.
7. Applicare il fisco come **drag annuo** invece che alla realizzazione.
8. Dimenticare il **bollo 0,20%** (patrimoniale, non sul guadagno).
9. Attribuire un rendimento atteso a **oro/commodities/cripto**.
10. Confrontare portafoglio e benchmark con **assunzioni diverse** (data, `g`, π, fisco).
11. Confrontare un top-down **geometrico** con CMA **aritmetiche**.
12. Presentare il risultato come **previsione**, o usarlo per giustificare una mossa tattica.
