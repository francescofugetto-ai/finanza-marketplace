# Modalità B — Valutazione di uno strumento (ETF / titolo)

Obiettivo: stabilire se uno strumento è **buono rispetto allo scopo dichiarato** e come si colloca contro i competitor e un benchmark. Output: report HTML di confronto (tabella best/worst, card strumenti, grafici a barre/torta, fan-chart Monte Carlo se richiesto), con verdetto e consiglio per l'investitore.

## Workflow

1. **Valuta/ottimizza il prompt.** Modalità augmentation: se lo scopo, i competitor o i criteri sono vaghi o migliorabili, proponi l'affinamento (1 riga) e procedi. Identifica chiaramente: strumento principale, **competitor**, **benchmark**, **scopo** (core vs satellite vs hedge…), **criteri**.
2. **Inquadra la tesi d'asset class** prima dei numeri. Es. small cap vs value vs EM vs azionario globale → attingi al canone The Bull via `consulenza-portafogli-etf` (scetticismo small cap, soglia fattoriale ≥1/3, value-tilt, tesi EM, "caro≠rischioso"). Lo strumento va giudicato **dentro** una tesi, non in astratto.
3. **Raccogli i dati oggettivi** (verifica live — vedi `fonti-e-dati.md`): ISIN, emittente, indice replicato, **TER**, **AUM**, replica (fisica/sintetica), domicilio (IE/LU), acc/dist, copertura valuta, **rendimenti storici** (1/3/5/10Y e per anno), **volatilità** e **Sharpe**, **max drawdown**, **esposizione geografica/settoriale**, **top holdings**, **overlap** col portafoglio esistente. Fonti: KIID/factsheet emittente, justETF, sito indice.
4. **Confronta in tabella unica.** `table.cmp`: una riga per criterio, una colonna per strumento + competitor + benchmark; evidenzia `.best`/`.worst` per riga. Affianca **pro e contro** sintetici e i **costi espliciti** (TER + eventuale spread/cambio).
5. **Proiezione attesa.** Se richiesta una stima forward, usa una **simulazione Monte Carlo** (assunzioni esplicite di rendimento atteso/vol/correlazioni; output lordo, netto-costi, netto-inflazione; percentili p10/p50/p90) e rappresentala col **fan-chart**. Componi con la skill Monte Carlo quando disponibile. **Dichiara le assunzioni**; non spacciare la mediana per certezza.
6. **Funzione nel portafoglio.** Il criterio decisivo non è "il migliore in assoluto" ma **"il migliore per quel ruolo nel suo portafoglio"**: cosa aggiunge in diversificazione/rendimento atteso/rischio rispetto a ciò che ha già, e se supera la **soglia di rilevanza** (un satellite sotto ~1/3 della sua classe è spesso rumore + TER + overlap).
7. **Bozza → ricontrollo → versione finale.** Stendi la comparazione, **rivàluta correggendo errori** (numeri, etichette, coerenza colori), poi produci l'HTML e il **verdetto + consiglio** per l'investitore. `present_files`.

## Criteri standard (adatta allo scopo)

Rendimento storico · rendimento atteso (Monte Carlo) · Sharpe · volatilità · max drawdown · **TER e costi totali** · AUM/liquidità · replica e domicilio · esposizione geografica/settoriale · overlap col portafoglio · **funzione/ruolo**. Suggerisci criteri aggiuntivi se pertinenti (es. tracking error, securities lending, prestito titoli, fiscalità armonizzato vs non).

## Struttura tipica del report (modalità B)

- header (strumento valutato + scopo)
- `stat-row` con i KPI dello strumento principale
- tesi d'asset class (box semantici + canone)
- `etf-grid` schede degli strumenti a confronto
- `table.cmp` confronto sui criteri (best/worst)
- barre esposizione geografica/fattoriale + `top10-bar` holdings/overlap
- `chart-wrap` rendimenti storici (line) e/o Monte Carlo (fan)
- `scenario-grid` se utile
- `conclusion-box` **Verdetto** + `action-list`
- `footer-note` (fonti, data, assunzioni Monte Carlo, "dati da verificare live")

## Errori da evitare

- Giudicare lo strumento in astratto invece che nel **ruolo** dentro quel portafoglio.
- Tabelle senza best/worst evidenziati.
- Monte Carlo senza assunzioni dichiarate, o mediana presentata come certezza.
- Inventare Sharpe/rendimenti/AUM non reperiti: meglio "n/d".
- Ignorare l'**overlap** (un nuovo ETF che ricompra ciò che già si ha non diversifica).
