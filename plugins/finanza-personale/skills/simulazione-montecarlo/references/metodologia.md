# Metodologia della simulazione

Lo script `scripts/montecarlo.py` simula migliaia di traiettorie del capitale e ne restituisce la distribuzione. **Non è una previsione**: è la mappa dei futuri possibili dati certi parametri. Cambi i parametri, cambia tutto — per questo le assunzioni vanno sempre mostrate in chiaro.

## Modello

- **Campionamento per periodo** (default mensile, `periods_per_year=12`; annuale con `=1`). Per ogni periodo e ogni traiettoria si estrae un rendimento casuale.
- **Distribuzione**: `lognormal` (default) — il capitale non va sotto zero e la composizione è moltiplicativa; oppure `t` di Student (`dist:"t"`, `t_df`) per **code più grasse** (crash più frequenti del normale). I parametri annui (rendimento atteso `exp_return`, volatilità `volatility`) sono convertiti in parametri log per-periodo in modo che il rendimento semplice atteso annuo resti coerente (correzione −½σ²: la **mediana** sta sotto la media, ed è giusto così — è il *volatility drag*).
- **Versamenti**: PIC iniziale (`initial`) + PAC ricorrente (`contribution`), con crescita annua opzionale (`contribution_growth`, es. aumenti salariali). Timing `begin`/`end` del periodo.
- **Sequence-of-returns risk**: catturato naturalmente, perché l'ordine dei rendimenti conta quando ci sono versamenti/prelievi.
- **Shock condivisi**: lordo e netto usano gli **stessi shock casuali** (cambia solo il drift), così la differranza tra i due strati è puro effetto-costi, non rumore.

## I tre strati di output

1. **Lordo** — rendimento `exp_return` pieno.
2. **Netto costi** — `exp_return − TER` (il TER come drag annuo), e ogni versamento ridotto di `entry_cost`. È il rendimento che incassi davvero prima delle tasse.
3. **Netto-netto (reale)** — lo strato netto **deflazionato per l'inflazione** (`/(1+inflazione)^t`): il **potere d'acquisto di oggi**. È lo strato su cui ragionare per obiettivi reali (casa, pensione): 300k tra 25 anni non sono 300k di oggi.

> Le tasse sul capital gain (26% / 12,5% titoli di Stato) **non** sono nel motore: applicale a parte sul guadagno, perché dipendono da realizzo, minus/plus e strumento. Dichiaralo nel report.

## Metriche restituite

- **Bande percentili annuali** (p5/p10/p25/p50/p75/p90/p95) per i tre strati → alimentano il **fan-chart**.
- **Distribuzione terminale** (a `goal_year` o fine orizzonte) per i tre strati.
- **Money multiple netto** (terminale/versato) — sempre definito, anche col PAC. Il **CAGR** è restituito **solo per il PIC puro** (senza PAC), perché con versamenti ricorrenti il CAGR da capitale iniziale non ha senso (usa il money multiple o, se serve un tasso, un IRR money-weighted calcolato a parte).
- **P(obiettivo)** = quota di scenari in cui il capitale a `goal_year` ≥ `goal`. Su base **reale** se `real_goal:true` (obiettivo in € di oggi), altrimenti nominale. Più `prob_miss` e **shortfall mediano** se l'obiettivo non è centrato.
- **Probabilità di perdita reale** = quota di scenari in cui il terminale reale < totale versato (sobrio promemoria del volatility drag + inflazione).

## Lettura corretta e limiti (dichiarali sempre)

- La banda p10–p90 è dove cade l'**80%** degli esiti; **non** è il caso peggiore (il 10% va sotto p10, e le code reali sono peggiori del modello).
- **I rendimenti passati non garantiscono i futuri.** Le assunzioni di rendimento/vol/inflazione sono input, non verità: vanno discusse e aggiornate.
- Il modello **non** cattura: volatility clustering, correlazioni che vanno a 1 nelle crisi, regimi macro, autocorrelazione, costi di transazione variabili, comportamento dell'investitore (il rischio numero uno: vendere nel panico).
- Per code grasse usa `dist:"t"` (single-asset). Le **correlazioni che vanno a 1 nelle crisi** non sono modellate dinamicamente: puoi però stressarle a mano alzando i coefficienti della matrice in uno scenario dedicato.
- **Garbage in, garbage out**: un `exp_return` troppo ottimista falsa tutto. Meglio assunzioni prudenti (vedi `assunzioni.md`).

## Modalità multi-asset (asset correlati separatamente)

Se nel config c'è `assets` (lista) il motore simula ogni asset **separatamente** con shock **correlati**, invece di un unico rendimento/vol di portafoglio.

- **Input**: `assets` = lista di `{name, weight, exp_return, volatility, ter}`; `correlation` = matrice NxN dei coefficienti; `rebalance` = `"annual"` (default) | `"none"` (drift/buy-and-hold) | intero (ogni N periodi).
- **Shock correlati**: si estraggono shock normali standard e si correlano con la **decomposizione di Cholesky** della matrice (`L` tale che `L·Lᵀ = correlazione`). Ogni asset usa i propri parametri log per-periodo; lordo e netto condividono gli **stessi** shock. Se la matrice non è semidefinita positiva, viene corretta col **clipping degli autovalori** (e segnalato in `warnings`).
- **Versamenti e ribilanciamento**: il PAC è ripartito sui pesi target; col ribilanciamento, a fine periodo i pesi tornano al target (vende ciò che è salito, compra ciò che è sceso — il "rebalancing premium"); con `"none"` i pesi driftano.
- **Costi**: `ter` **per asset** (core 0,1-0,2%, satelliti 0,4-0,6%).
- **Output extra**: `portfolio_implied` con rendimento/vol **impliciti** di portafoglio calcolati analiticamente (`vol = √(wᵀ Σ w)`, con `Σ = diag(σ)·corr·diag(σ)`), la **media pesata delle vol** e il **risparmio di volatilità** dovuto alla diversificazione (correlazioni < 1 → vol di portafoglio < media pesata). Più l'echo di `assets`/`correlation`. Lo schema principale (bande/terminale/goal) resta identico al single-asset.
- **Limite onesto**: lo shock multivariato è gaussiano (niente `t` multivariata); le correlazioni sono statiche. Per il rischio "tutto crolla insieme" usa uno scenario con correlazioni alzate.
