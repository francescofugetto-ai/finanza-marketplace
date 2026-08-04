# Template dell'output (analisi titoli di Stato)

Struttura da usare per la proposta/analisi. Tono: consulente cinico-professionale, diretto, senza entusiasmo da marketing; spiega le **funzioni** e i **numeri netti**, non i prodotti. In chat per la discussione; **HTML** nello stile del template di progetto (kicker, box colorati con bordo sinistro, tabelle `.cmp`, action-list numerata, conclusion-box.verdict — vedi istruzioni di progetto §8.2) solo se è un deliverable formale. `.docx` (Calibri, A4, header/footer, tabelle color-coded navy/teal/amber/rosso/verde) resta disponibile solo su richiesta esplicita di un file Word.

Adatta le sezioni al compito: per l'analisi di **un singolo titolo** bastano 1-4 e 7-9; per una **proposta di ladder** servono tutte.

```
# Analisi titoli di Stato — [etichetta investitore / obiettivo]

## 1. Cosa è stato chiesto e come rientra nel mandato
[1-3 righe: la domanda, e il collegamento al mandato preservazione/decumulo + cap di perdita del mandato, citato con il suo valore letto dalla vista.]

## 2. Titoli analizzati (ISIN VERIFICATI)
Tabella con dati verificati (mai a memoria). Marca "da verificare" ciò che non lo è.

| Titolo | ISIN (fonte) | Emittente / WL | Scadenza | Cedola | Prezzo secco | Rateo | Lotto |
|--------|--------------|----------------|----------|--------|--------------|-------|-------|
| …      | … (BorsaIT+btpfacile) | IT / WL✓ | gg/mm/aaaa | …% | … | … | … |

## 3. Rendimenti NETTI e rischio-tasso
Sempre al netto (12,5%/26% + bollo + scarto) e, dove possibile, reale. Fonte dei numeri: script bond_math.py su input verificati.

| Titolo | YTM lordo | YTM netto (12,5%) | YTM reale* | Dur. mod. | Convexity | Carry+roll |
|--------|-----------|-------------------|-----------|-----------|-----------|------------|
| …      | …%        | …%                | …%        | … anni    | …         | …          |

*reale = netto deflazionato con inflazione attesa dichiarata: [ipotesi e fonte].

## 4. Fiscalità (esplicita)
- Aliquota applicata e perché (white-list → 12,5%; include Bund/OAT/Bonos).
- Utile a scadenza / scarto / eventuale minus e compensabilità.
- Bollo 0,20%/anno (neutro nel confronto con ETF, comunque sottratto).

## 5. Contesto macro & curva (cornice, non timing)
[3-6 righe: regime tassi BCE/Fed, forma della curva, spread BTP-Bund, break-even
inflazione. Cita solo dati presenti nei report/fonti; esplicita che NON è timing.]

## 6. Collocazione nella ladder / cash-flow matching
[Quale flusso copre, come si incastra nelle scadenze esistenti, diversificazione
d'emittente, glide-path, rischio di reinvestimento al roll.]

## 7. Scenario avverso vs cap di perdita
| Scenario | Effetto MtM sui titoli | Effetto sul totale | Entro il cap di perdita del mandato? |
|----------|------------------------|--------------------|-----------------|
| Tassi +100 bps | … | … | … |
| Tassi +200 bps | … | … | … |
| Spread BTP-Bund +150 bps (solo IT) | … | … | … |
[Distingui MtM potenziale (tenuto a scadenza) da perdita realizzata.]

## 8. Regola di monitoraggio
- Da ignorare: Var % giornaliero del book (rumore su titoli tenuti a scadenza).
- Da osservare: merito di credito, scadenze in arrivo, relative value netto, nuovi bisogni, cambi fiscali.
- Frequenza: almeno annuale + check a ogni scadenza/nuovo bisogno.

## 9. Conclusione operativa e domande aperte
- Raccomandazione (tenere / comprare quale scadenza / switch), con il trade-off esplicito.
- Dati ancora da verificare prima di operare.
- [Se rilevante] segnalazione al livello di progetto (es. quota monetaria 26% → CCTeu/BTP breve 12,5%), senza decidere l'allocazione da soli.

## 10. Disclaimer
Materiale educativo e di ragionamento, non consulenza finanziaria personalizzata ai
sensi di legge né raccomandazione di investimento. Investire comporta rischio di perdere
capitale; i rendimenti passati non predicono quelli futuri. Verificare sempre KID/prospetto,
condizioni del broker e fiscalità. La decisione finale spetta all'investitore e al revisore umano.
```

## Promemoria di qualità prima di consegnare
- ISIN **verificati** su ≥2 fonti; scadenza e cedola coerenti.
- Rendimenti **netti** (e reali dove possibile); nessun lordo spacciato per netto; aliquota giusta.
- Distinzione **held-to-maturity vs vendita** chiara; il MtM non è spacciato per perdita realizzata.
- Scenario avverso (tassi **e** spread) confrontato col **cap di perdita**.
- Curva/roll usati per **scegliere il punto**, non per il timing.
- Numeri **verificati o marcati da verificare**; quote/totali che chiudono.
- Chiuso con le **domande aperte**, non con buchi riempiti a memoria.
