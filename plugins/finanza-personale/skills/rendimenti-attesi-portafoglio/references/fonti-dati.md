# Protocollo dati — dove si prende ogni numero

Regola generale: **prima cerco live, poi chiedo**. Non chiedere all'utente ciò che è pubblicamente verificabile; non inventare ciò che non è verificabile. Ogni numero entra nel calcolo con **fonte + data del dato**.

> **Il KID non serve quasi mai.** Il KID/KIID riporta profilo di rischio, costi e scenari regolamentari: **non** riporta dividend yield, yield to maturity né duration. I dati che servono stanno nel **factsheet mensile** dell'indice o dell'emittente. Il KID serve solo come conferma dei costi.

---

## 1. Azioni — dividend yield

### 1.1 Fonte primaria: factsheet mensile dell'indice MSCI (pubblico, PDF)

Contiene il blocco **FUNDAMENTALS** con `Div Yld (%)`, `P/E`, `P/E Fwd`, `P/BV`, aggiornato a fine mese. È la fonte usata in `[TB-339]`.

Pattern URL (verificato funzionante): `https://www.msci.com/documents/10199/255599/msci-<nome-indice>-net.pdf`

| Indice | Slug tipico | Note |
|---|---|---|
| MSCI ACWI | `msci-acwi-net` | il factsheet ACWI riporta **anche** World ed Emerging Markets sulla stessa pagina |
| MSCI World | (incluso nel factsheet ACWI) | |
| MSCI Emerging Markets | (incluso nel factsheet ACWI) | |
| MSCI USA | cerca "MSCI USA Index factsheet" | |
| MSCI World ex USA | cerca "MSCI World ex USA Index factsheet" | |
| MSCI EMU / Europe | cerca per nome | |

Se il pattern non risolve: ricerca web `MSCI <indice> Index factsheet <mese anno>` e prendi il PDF su `msci.com`.

**Esempio verificato (30/06/2026)** — MSCI ACWI: Div Yld **1,57%**, P/E 23,64, P/E Fwd 17,78, P/BV 3,86; MSCI World: **1,52%**; MSCI Emerging Markets: **1,93%**. Pesi paese ACWI: USA 63,63%, Giappone 5,0%, Taiwan 3,33%, UK 3,03%, Canada 2,93%.

### 1.2 Fonte alternativa: pagina prodotto dell'emittente

iShares/BlackRock, Vanguard, Amundi, SPDR, Xtrackers pubblicano su ogni pagina prodotto: `Rapporto P/E`, `Rapporto P/B`, `Distribution Yield` / `12m Trailing Yield`, TER, replica, AUM, numero di titoli.

⚠️ **Trappola**: sugli ETF **ad accumulazione** il "distribution yield" può essere assente o fuorviante. Preferire sempre il **dividend yield dell'indice**, non quello del veicolo.

⚠️ **Seconda trappola**: `12m trailing yield` è **retrospettivo**; il DY di factsheet dell'indice è **corrente**. Non mischiarli fra gambe diverse.

### 1.3 Fonte di fallback: earnings yield da P/E

Se il DY non è recuperabile ma il P/E sì, si può ragionare in **earnings yield** `E/P = 1/(P/E)` con un payout ratio dichiarato. È un ripiego: **dichiararlo** e non presentarlo come equivalente.

### 1.4 Crescita `g`

- **Preferita**: CMA che dichiari la crescita **reale per azione** (AQR, Research Affiliates, JPM LTCMA). Cerca `AQR capital market assumptions <anno>` / `Research Affiliates Asset Allocation Interactive`.
- **Default prudente**: 1-2 pt reali (ancora storica mercati sviluppati).
- **Set usato in `[TB-339]`, lug-2026** (*time-sensitive*): USA 2,7% · sviluppati ex-USA 2,5% · EM 2,6% (AQR).
- **Mai** estrapolare la crescita recente.

---

## 2. Obbligazioni — YTW, duration, qualità

### 2.1 Fonte primaria: factsheet dell'ETF (PDF dell'emittente)

Blocco `Characteristics` con: `Yield to worst`, `Average coupon`, `Average maturity`, **`Average duration`**, `Average quality`, `Number of bonds`, distribuzione per scadenza e per rating.

- **Vanguard**: `https://fund-docs.vanguard.com/<NOME_FONDO>_<id>_EU_INT_UK_EN.pdf` — recuperabile via ricerca `<nome ETF> Vanguard factsheet`.
- **iShares/BlackRock**: pagina prodotto → sezione "Portfolio Characteristics" e link "Fact Sheet".
- **Amundi / Xtrackers / SPDR**: pagina prodotto → factsheet mensile.

**Esempio verificato (30/06/2026)** — Vanguard EUR Eurozone Government Bond UCITS ETF (Acc), `IE00BH04GL39`, indice Bloomberg Euro Aggregate: Treasury: **YTW 3,11%**, cedola media 2,6%, **scadenza media 8,6 anni**, **duration 7,0 anni**, 520 titoli, qualità media A+, OCF 0,07%. Composizione: Francia 23,7%, Italia 22,0%, Germania 19,1%, Spagna 14,1%. Rating: AAA 23,4% / AA 6,7% / A 46,3% / BBB 23,4%.

> Nota di lettura: al 31/05/2026 lo stesso fondo riportava YTM 3,12% e scadenza media ~9 anni — i valori citati nell'episodio. Il dato si muove ogni mese: **rieseguire, non riusare**.

### 2.2 Differenziale per la copertura del cambio (panieri EUR-hedged)

Serve `r_breve_EUR − r_breve_valuta_estera`:
- **€STR**: BCE, statistiche sui tassi di riferimento.
- **SOFR**: Federal Reserve Bank of New York.
- In alternativa, **preferibile**: se l'emittente pubblica lo *yield to maturity hedged* della classe EUR-hedged, usa direttamente quello.

### 2.3 Perdita attesa da credito

Studi annuali sui default: **Moody's Annual Default Study**, **S&P Global Ratings Default, Transition and Recovery**. Ricerca: `corporate default rate recovery rate <anno> annual study`. In assenza, usa gli ordini di grandezza di `metodologia-top-down.md` §2.3 **dichiarandoli come ordini di grandezza**.

### 2.4 Singoli titoli di Stato

→ skill `analisi-titoli-di-stato-eu` (YTM netto, scarto d'emissione, rateo, bollo, verifica ISIN a tolleranza zero). Non duplicare qui il calcolo.

---

## 3. Inflazione attesa

**Per un investitore in euro serve l'attesa d'inflazione dell'area euro**, non quella USA (errore di `[TB-339]`, che usa la Cleveland Fed per tutti).

| Fonte | Cosa dà | Nota |
|---|---|---|
| **BCE — Survey of Professional Forecasters (SPF)** | attese a 1/2/5 anni e **long-term** | fonte primaria per l'area euro |
| **BCE — swap d'inflazione 5y5y forward** | attesa di mercato a lungo | market-based, reattivo |
| **Breakeven** BTP€i / OAT€i vs nominali di pari scadenza | attesa di mercato euro | contaminato dal premio di liquidità |
| **Cleveland Fed — 10-Year Expected Inflation** | attesa **USA** | usare **solo** per stime in USD |

Se le fonti divergono, prendi l'intervallo e usa il punto centrale, dichiarandolo. Ordine di grandezza da `[TB-339]`: 2,5% (USA). Il canone avverte che nel regime attuale *"3% is the new 2%"* (`[TB-331]`): **giri anche uno scenario a 2,5-3%**.

---

## 4. Capital market assumptions (bottom-up)

Ricerca per casa, ogni volta: `<casa> capital market assumptions <anno>` / `<casa> long-term capital market assumptions`.

Per **ciascuna** registra: casa · data di pubblicazione · orizzonte · **valuta** · **geometrico o aritmetico** · assunzione di inflazione. Senza questi cinque campi la stima non è confrontabile (vedi `metodologia-bottom-up.md` §3).

Fonti aggiuntive euro-native o trasparenti: **Vanguard VCMM** (versione area euro), **Research Affiliates** (gratuito, metodo esplicito), **Damodaran** (ERP implicito mensile).

---

## 5. Costi e fiscalità

| Dato | Fonte |
|---|---|
| **TER** | pagina prodotto emittente (autoritativa) · justETF/extraETF (comodo, da confermare) |
| **Tracking difference** | trackingdifferences.com o confronto NAV-vs-indice sul factsheet |
| **ISIN, replica, Acc/Dist, domicilio, AUM** | pagina prodotto emittente |
| **Quota governativa white-list** di un ETF obbligazionario | comunicazione periodica dell'emittente o dell'intermediario — **non deducibile dalla composizione**, va richiesta/verificata |
| **Bollo 0,20%** / IVAFE | normativa vigente; verificare in Legge di Bilancio corrente |
| **Condizioni broker** (PAC gratuito, lista zero commissioni) | sito del broker, **verifica live** |

---

## 6. Cosa chiedere all'utente (e solo questo)

Chiedi **solo** ciò che non è pubblico:

1. **I pesi target** del portafoglio e la classificazione delle gambe (o gli ISIN, da cui ricavo il resto).
2. **L'orizzonte** in anni e il **broker** (per i costi di transazione e il regime fiscale).
3. Per gambe in **singoli titoli**: ISIN, prezzo di carico, quantità (per lo YTM effettivo).
4. Un **KID/factsheet in allegato** *solo se* la fonte live non è raggiungibile — capita con alcuni emittenti dietro form o con pagine JS-only.
5. Se preferisce un'assunzione di `g` o di inflazione **diversa** dal default (e con quale motivazione).

Non chiedere: ISIN dei benchmark (sono fissi, vedi `benchmark-e-confronto.md`), dividend yield, YTM, duration, TER, CMA. **Quelli li recupero io.**

---

## 7. Quando un dato non si trova

Ordine di escalation:
1. Riprova con fonte alternativa (§1.2, §2.1).
2. Usa un **proxy dichiarato** (es. MSCI World al posto di MSCI World ex USA) e scrivi che è un proxy.
3. Usa un **default dichiarato** dalla tabella di `simulazione-montecarlo/references/assunzioni.md`, marcandolo come assunzione e non come dato.
4. Se nulla funziona: **`n/d` esplicito**, escludi la gamba dal calcolo, riduci la copertura dichiarata e chiedi il factsheet all'utente.

**Mai** riempire un buco con un numero plausibile. Un rendimento atteso sbagliato di mezzo punto sposta il piano di risparmio di anni.
