# Canone The Bull — P5b Fattoriale / Smart Beta

Fonte: `[TB-242]` "Perché investire in Value, Momentum e Quality (e come sono composti)". Rif. incrociato: `[TB-268]`.

## Cos'è l'investimento fattoriale `[TB-242]`

- Un **fattore** è una caratteristica sistematica comune a certi asset che spiegherebbe il loro rendimento atteso. Si parte dal capital asset pricing: il valore presente di un flusso di reddito futuro = flussi scontati per (1+r)^t, dove **r** è il tasso che compensa il rischio.
- **CAPM** (Sharpe, anni '60): rendimento atteso = risk-free + premio al rischio × **beta** (sensibilità al mercato). Più rischio → meno prezzo oggi → più rendimento atteso. Ma ~1/3 del mercato si comportava in modo **anomalo**.
- Dagli anni '90 (Fama, French, Jegadeesh, Titman, Carhart, Novy-Marx): modelli integrativi. I principali fattori:
  - **SIZE** — small cap rendono più delle large.
  - **VALUE** — prezzo basso vs valore patrimoniale rende più del Growth (prezzo alto).
  - **MOMENTUM** — chi è cresciuto di più negli ultimi 6-12 mesi tende a rendere di più nei 12 successivi.
  - **QUALITY** — alto ROE, basso debito, crescita stabile degli utili (evoluzione di Profitability/Investment di Fama-French).
  - **LOW VOLATILITY** — bassa volatilità rende di più (anomalia rispetto al CAPM).
- **5 criteri di Swedroe** perché un fattore sia "vero": **persistente, pervasivo** (mercati/settori/asset class), **robusto** (varie definizioni), **investibile**, **intuitivo** (spiegazione **risk-based** o **comportamentale**). Per ogni fattore esistono entrambe → probabilmente pesano entrambe. "*Per noi investitori, sticazzi quale sia il motivo. L'importante è che funzionino.*"
- **Non è gratis**: più rischio, lunghi periodi di **sottoperformance** vs mercato, e il fattore può smettere di funzionare a lungo o per sempre. "Se vuoi qualcosa in più, devi accettare sofferenza in più."

## Costruzione tecnica degli indici MSCI `[TB-242]`

- Gli ETF fattoriali sono **long-only** (sovrappesano, non shortano). Gli studi accademici usano portafogli **long-short**; ma anche la sola parte long porta extra-rendimento, e non-investire in una società equivale a esserne short per il suo peso nell'indice.
- **Z-score** sul **Parent Index** (MSCI World, ~1500 società dei Paesi sviluppati): a ogni società un punteggio in deviazioni standard sui criteri del fattore. Poi ordinamento per score × peso nell'indice di partenza.
  - **VALUE (Enhanced Value)**: Price/Book + Price/forward Earnings + EV/Cash Flow from Operations. "Enhanced" perché usa tre criteri e correzioni anti-concentrazione. ~400 componenti. Vincolo settoriale ~MSCI World.
  - **QUALITY (Sector Neutral)**: ROE + (basso) indebitamento + (bassa) variabilità degli utili a 5 anni. ~300 componenti. **Sector-neutral** (pesi settoriali ~MSCI World).
  - **MOMENTUM**: crescita di prezzo a 6 e 12 mesi, **risk-adjusted** (− risk-free locale, / deviazione standard settimanale a 3 anni), media dei due, esclusione z-score estremi. ~350 componenti. **Nessun vincolo settoriale.**
  - Ribilanciamento ogni **6 mesi**.

## Composizione attuale degli indici (al momento di TB-242) — *time-sensitive*

- **Quality**: il più concentrato e America-centrico, **~72% USA**; top-10 ~32% (Nvidia, Microsoft, Apple, Visa, Meta, Mastercard, Eli Lilly, Google, Netflix, ASML).
- **Momentum**: **57,6% USA** (11 pt sotto MSCI World); Germania 7,6%, Giappone 5,3%, Canada 5,2%; top-10 ~28% (Broadcom, Netflix, Berkshire, Visa, JPMorgan, Palantir, Walmart, Philip Morris, Costco, SAP) — **nessuna Magnifica 7** in top-10.
- **Value**: il più lontano dal market-cap, **37% USA**, Giappone 22,8%, UK 9,4%; società "vecchie" in business tradizionali (Cisco, Qualcomm, Micron, Intel, AT&T, Verizon, Toyota, British American Tobacco, Comcast, HSBC).
- **Implicazione**: i fattori "World" **ri-comprano** in gran parte large cap già nel core; Value è quello che diversifica davvero la geografia. Motivo per cui Spada preferì i **tre strumenti singoli** (controllo dell'allocation geografica).

## Perché VMQ (Value + Momentum + Quality) `[TB-242]`

- **Via negationis**: esclude Small Cap e Low Vol.
  - **No Small Cap**: (1) tecnico — indici fatti male (Russell 2000), front-running sui ribilanciamenti prevedibili; i buoni (Avantis, Dimensional) non ancora pienamente disponibili in Europa; (2) logico — il **private equity** drena le migliori small cap (restano private più a lungo), qualità del Russell 2000 in calo, utili giù dal 2021; (3) macro — "higher for longer" colpisce di più le piccole (costi di finanziamento sui margini).
  - **No Low Vol**: contraddice il CAPM (più rendimento risk-adjusted con basso beta), meno intuitivo, performance mediocre negli ultimi 10 anni (anche se funzionò nel 2022). Bias personale ammesso: "probabilmente dovrei, ma è una mia fissa". Funziona meglio long-short con leva.
- **Paper AQR (Asness, Frazzini, Israel, Moskowitz, 2015, *J. of Portfolio Management*)**: un portafoglio **equal-weight Value+Momentum+Quality** ha **~doppio Sharpe** di Value da solo (1963-2014, database Ken French). Benefici di miglior risk-adjusted return validi **anche long-only**. Invesco scelse VMQ per il suo multifattoriale.
- **Logiche di fondo**: Value = utili futuri sistematicamente sottostimati + alto tasso di sconto (percepite rischiose). Quality = preferenza per realtà speculative nei bull market ("flight to risk") sottoprezza la qualità. Momentum = autocorrelazione + bias comportamentali (endowment, sunk cost) → sotto/sovra-reazione.

## Quanto e come `[TB-242, TB-268]`

- **Soglia di rilevanza: ≥ ~1/3 dell'azionario.** Sotto è **rumore** (complessità + TER senza spostare il risultato). Spada: tilt a ~1/4 della quota azionaria, **obiettivo ~1/3 abbondante**.
- **Razionale del tilt**: il fattoriale porta più **rischio sistematico** → posso aumentare il rendimento atteso *o* alzando l'azionario *o* tenendo l'azionario più basso e aumentando la diversificazione. **Backtest 25 anni (dic 1998-dic 2024)**: 46% MSCI World + 24% VMQ + 23% bond governativi globali + 7% oro → **stesso rendimento del World (~7% CAGR) ma rischio nettamente inferiore** (dev. std ~10% vs 14,5%; max drawdown 38% vs 56%; **Sharpe 0,55 vs 0,44**). *Non sempre vero*: dal 2009 il 100% azionario ha reso ~3 pt/anno in più; dal 2000 al 2009 il contrario. Con le valutazioni USA attuali alte, Spada **vuole il miglior rendimento per il rischio assunto, non il miglior rendimento assoluto**.
- **Singoli vs multifattoriale**: vedi `00-principi-e-mappa.md` §C-B. Singoli = controllo geografico; multifattoriale (Invesco **IQSA**, lanciato 2019, ~+1%/anno sul World in 6 anni, integra anche crescita utili nel momentum) = più semplice, meno overlap. Spada con il senno di poi userebbe IQSA per i nuovi capitali (ma non switcha per non realizzare ~19%/anno di capital gain accumulato).
- **Due verità sui fattori**: (1) *non tutti possono investirci* — per ogni deviazione serve una controparte; investire in fattori = o prendi più rischio dell'investitore medio, o investi in cose che all'investitore medio non piacciono → "l'esperienza non sarà sempre piacevole"; (2) vale la pena **solo** se si è certi di mantenere un atteggiamento **sistematico a lungo termine** senza saltare di palo in frasca a ogni cambio di mercato.

<!-- VERSIONE FILE -->
**Episodi:** TB-242 (+ rif. TB-268). **Stato:** completo. **Time-sensitive:** le composizioni geografiche/top-10 degli indici sono fotografie datate (ribilanciate ogni 6 mesi).
