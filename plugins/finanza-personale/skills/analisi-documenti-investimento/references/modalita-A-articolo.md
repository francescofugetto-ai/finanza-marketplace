# Modalità A — Articolo / grafico

Obiettivo: prendere un articolo (e/o un grafico) e restituire un **mini-articolo** che lo legge, lo sviscera, lo spiega — termini tecnici inclusi — e ne traduce le conseguenze **per il portafoglio dell'utente**. Output: report HTML (design system).

## Workflow

1. **Leggi davvero la fonte.** PDF/HTML/testo allegato → estrai tesi, dati, numeri, citazioni rilevanti. Se è un link, fai web_fetch. **Non riassumere passivamente**: l'utente l'ha già letto, vuole che tu lo *spieghi e lo usi*. Rispetta il copyright: parafrasa, niente blocchi citati lunghi.
2. **Leggi il grafico.** Identifica assi (LHS/RHS), serie, unità, periodo, base index. Spiega cosa misura e cosa mostra il movimento. Se è uno screenshot, descrivi ciò che vedi davvero (non assumere dati non visibili). Se ricostruisci il grafico in Chart.js, usa **solo** i valori leggibili/dichiarati; se approssimi per illustrare, **dichiaralo**.
3. **Interpreta nel contesto.** Collega la tesi dell'articolo al quadro di mercato **alla data odierna** (cerca live i dati che servono: livelli indici, P/E forward, tassi, ecc.) e alla teoria finanziaria. Distingui fatto, stima di consensus e opinione dell'autore.
4. **Spiega i termini.** Glossario in testa (`glossary-grid`) per ogni sigla/termine (P/E, EPS, forward, LHS/RHS, breadth, multiplo…), 1 riga + micro-esempio numerico. Termini puntuali nel flusso → `term-box`. Meccanismi → `concept-box` + `example-box` con numeri.
5. **Impatto sul portafoglio.** Se conosci il portafoglio dell'utente (conversazione / istruzioni personali / screenshot / skill `consulenza-portafogli-etf`), chiudi con **cosa cambia per lui**: quali posizioni tocca la tesi, in che direzione, con che entità, e se richiede un'azione o è solo rumore. Usa il filtro del canone The Bull (no timing, fotogramma-vs-film, caro≠rischioso). Se il portafoglio non è noto, chiedilo una volta o resta sul generale dichiarandolo.
6. **Ricontrolla, poi consegna.** Verifica numeri, coerenza colori↔contenuto, termini spiegati, fonti citate, niente invenzioni. Poi scrivi l'HTML e fai `present_files`.

## Struttura tipica del report (modalità A)

- header (kicker fonte+data, headline, sottotitolo/autore)
- `glossary-grid` dei termini
- `stat-row` con 3-4 numeri chiave dell'articolo
- corpo: cosa dice l'articolo (parafrasato), cosa mostra il grafico (con `chart-wrap` ricostruito se utile), perché conta ora
- `concept-box`/`example-box` per i meccanismi; box semantici per i giudizi
- `conclusion-box` "Cosa significa per il tuo portafoglio" + eventuale `action-list`
- `footer-note` (fonte, data, "dati da verificare live")

## Errori da evitare

- Trasformarlo in un riassunto. Serve **interpretazione e uso**, non un compendio.
- Spiegare il grafico inventando i valori non leggibili.
- Saltare il collegamento al portafoglio quando il portafoglio è noto: è la parte di maggior valore.
- Dare per buona l'opinione dell'autore come fosse un fatto; nominare l'incertezza.
