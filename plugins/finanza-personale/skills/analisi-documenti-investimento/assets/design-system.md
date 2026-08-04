# Design system del report — significato e uso

Il template è in `assets/template-report.html`. Questo file dice **quando** usare cosa e **perché**. Regola madre: l'estetica deve assomigliare al sample (`report_ft_portfolio`). **Sfondo sempre chiaro** (l'utente odia i report scuri). Font **Inter**. Larghezza colonna 820px. Output = **un singolo file HTML** nella cartella di output dell'ambiente (`metodo-fiduciario` §10), poi condivisione del file.

## I colori hanno un significato — non decorano

Usa l'accento **in base al contenuto**, mai a caso:

| Colore | Token | Significato | Dove |
|---|---|---|---|
| Blu | `--accent-blue` | informazione, concetto, termine tecnico, serie neutra | `term-box`, `box-accent`, `g-term`, `concept-title`, serie 1 dei grafici |
| Verde | `--accent-green` | positivo, forza, on-track, esito favorevole, "best" | `box-success`, cella `.best`, pill verde |
| Ambra | `--accent-amber` | cautela, watch, limite, attenzione | `box-warn`, pill ambra |
| Rosso | `--accent-red` | rischio, debolezza, esito negativo, "worst" | `box-danger`, cella `.worst`, pill rossa |
| Viola | `--accent-purple` | fattoriale / serie speciale / terza serie | barre fattoriali, pill viola, 3ª serie grafici |

Coerenza grafici↔testo: se nel testo il Value è "ambra" e il Growth "blu", **negli stessi colori** vanno le serie del grafico e le pill. Mai un verde su una cosa negativa.

## Quando usare quale componente

- **`glossary-grid`** — apertura della modalità A. Spiega **ogni** termine tecnico che comparirà (P/E, EPS, LHS/RHS, Sharpe, duration…), 1 riga, con micro-esempio numerico. È il requisito esplicito dell'utente: "spiegami i termini tecnici".
- **`term-box`** — definizione singola messa in risalto nel flusso del testo (quando un termine va spiegato lì dove appare).
- **`stat-row`** — 2-5 numeri-chiave di sintesi (valore portafoglio, P/E indice, gap performance, TER…). Colpo d'occhio.
- **box semantici** — una frase che è un giudizio: forza→`success`, cautela→`warn`, rischio→`danger`, nota neutra/concetto→`accent`. **Non** incatenarne troppi di fila; alternali col testo.
- **`chart-wrap` + Chart.js** — quando un numero si capisce meglio visto. Legenda **HTML custom** (la legenda nativa di Chart.js è disattivata). Line per serie temporali, bar per confronti/scenari, fan-chart per Monte Carlo. Niente sfondo scuro nel canvas.
- **`etf-card`** — schede sintetiche degli strumenti (modalità B): nome, ISIN/ruolo, TER, AUM, replica, acc/dist.
- **`table.cmp`** — la **tabella di confronto** della modalità B: una riga per criterio, una colonna per strumento + benchmark. Evidenzia con `.best`/`.worst` la cella migliore/peggiore **di ogni riga** (così l'occhio legge i vincitori). Numeri con classe `.num` (tabular-nums incolonna).
- **`factor-row` / `top10-bar`** — barre orizzontali per esposizione geografica, peso fattori, top-10 holdings, overlap.
- **`scenario-grid`** — 2-4 scenari (base / revisione / rotazione / stress) con esito atteso per asset.
- **`concept-box` + `example-box`** — didattica: concetto + esempio numerico concreto. Usa quando spieghi un meccanismo (es. come il tasso di sconto muove il prezzo).
- **`conclusion-box`** — il blocco finale: in modalità A "Cosa significa per il tuo portafoglio", in modalità B "Verdetto". Lista di take azionabili con freccia.
- **`action-list`** — checklist operativa numerata (importo €, strumento, scadenza), se ci sono azioni concrete.
- **`footer-note`** — fonti citate + data + "dati di mercato da verificare live" + nota che non è consulenza personalizzata (se la skill è usata in modo universale).
- **`report-sep`** — separa più report nello stesso file (es. "Report 1 — articolo", "Report 2 — impatto portafoglio"), come nel sample.

## Errori da evitare

- Sfondo scuro o canvas scuro. **Mai.**
- Colore senza significato (verde "perché sta bene").
- Tabelle senza evidenziazione best/worst: diventano muri di numeri.
- Glossario assente in modalità A quando ci sono sigle/termini.
- Legenda nativa Chart.js attiva (usa quella HTML, più pulita e coerente col font).
- Inventare dati per riempire un grafico/tabella: se un numero non c'è, **lascia il buco e dichiaralo** (vedi `fonti-e-dati.md`).
