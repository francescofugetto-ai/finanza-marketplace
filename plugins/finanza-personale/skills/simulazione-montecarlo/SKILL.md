---
name: simulazione-montecarlo
description: "Simula portafogli/PAC con Monte Carlo, anche multi-asset correlati: capitale futuro lordo/netto/reale, percentili, P(obiettivo). Esegue uno script Python e produce un report HTML con fan-chart."
---

# Simulazione Monte Carlo per portafogli

Stima la distribuzione del capitale futuro di un portafoglio o di un PAC e la **probabilità di centrare un obiettivo** (es. acconto casa a una data, target pensione). Non è una previsione: è la mappa probabilistica dei futuri possibili date assunzioni **esplicite**. Output: **report HTML** con l'estetica della skill `analisi-documenti-investimento` (sfondo chiaro, Inter, colori semantici) + **fan-chart** lordo/netto/reale + gauge P(obiettivo).

## Workflow

1. **Raccogli gli input** (o proponi default *dichiarati* da `references/assunzioni.md`, mai inventati di nascosto):
   PIC iniziale, PAC e passo (mensile/annuale), orizzonte, TER/costi, **inflazione**, ed eventuale **obiettivo** (importo + anno + se è in € di oggi). Per il **rischio/rendimento** due strade: (a) **multi-asset** (consigliata) — passa `assets` (lista di `{name, weight, exp_return, volatility, ter}`) + `correlation` (matrice NxN) + `rebalance` (`annual`/`none`/N): il motore simula gli asset **separatamente con shock correlati** e ricava la vol di portafoglio (più bassa della media pesata); (b) **aggregata** — un solo `exp_return`/`volatility` di portafoglio. Per lo scenario di stress, alza le correlazioni.
   **Se il portafoglio è già definito, gli `exp_return` per asset arrivano dalla skill `rendimenti-attesi-portafoglio`** (calcolo top-down datato, netto TER e bollo), non dalla tabella di default: quella è il fallback. Le tasse restano fuori dal motore e si applicano a parte (vedi guardrail).
2. **Scrivi il config JSON** e **esegui il motore**:
   `python3 scripts/montecarlo.py config.json results.json`
   (campi, default ed esempio multi-asset in `references/assunzioni.md` e in testa allo script; modello in `references/metodologia.md`). Non fare i calcoli a mano: li fa lo script, vettorizzato.
3. **Gira più scenari** quando c'è un obiettivo: almeno **prudente** e **ottimista** (es. rendimento −1,5 pt, inflazione +0,5 pt) e confronta P(obiettivo). Una probabilità che regge solo nello scenario roseo è un alert.
4. **Genera il report**: parti da `assets/report-montecarlo.html`, **inietta il JSON** di `results.json` al posto del placeholder `const MC = {...}`, riempi i marcatori FILL (titolo, interpretazione, take azionabili, data/fonti delle assunzioni). Il fan-chart e la tabella si popolano da soli dai dati.
5. **Ricontrolla prima di consegnare**: assunzioni mostrate in chiaro, numeri coerenti, colori del verdetto coerenti con P(obiettivo) (verde ≥75%, ambra ≥50%, rosso <50%), nessun dato inventato. Poi salva l'HTML nella **cartella di output dell'ambiente** (vedi `metodo-fiduciario` §10) e condividi il file.

## Composabilità

- Con `consulenza-portafogli-etf`: per i **pesi**, il **profilo** e gli **obiettivi** dell'utente (Bucket A casa con la sua data, Bucket B pensione). Usa la stessa disciplina "assunzioni time-sensitive".
- Con `rendimenti-attesi-portafoglio`: per gli **`exp_return` per asset**, calcolati top-down e datati, e per gli **scenari** (base = top-down; prudente = minimo delle CMA; ottimista = massimo). È la fonte preferita dei parametri di rendimento; la tabella di `assunzioni.md` resta il fallback dichiarato. La volatilità e le correlazioni restano assunzioni di questa skill.
- Con `analisi-documenti-investimento`: questa skill è il **motore** dietro le "proiezioni di Monte Carlo" della modalità B (confronto strumenti). Il report condivide design system e fan-chart.

## Guardrail (non negoziabili)

- **Non inventare.** Le assunzioni sono input espliciti e **mostrate nel report**. Se l'utente non le fornisce, proponi i default di `assunzioni.md` *dichiarandoli come assunzioni*, non come dati.
- **Pianificazione, non profezia.** Dichiara sempre i limiti (code grasse, correlazioni che vanno a 1 nelle crisi, rischio comportamentale). La banda p10–p90 non è il caso peggiore.
- **Reale per gli obiettivi.** Per casa/pensione ragiona sullo strato **netto-netto** (potere d'acquisto). Le **tasse** (26% / 12,5%) non sono nel motore: applicale a parte e dillo.
- **Prudenza nelle assunzioni**: meglio sottostimare il rendimento e sovrastimare la vol. `exp_return` ottimista falsa tutto (garbage in, garbage out).
- **Niente consiglio personalizzato travestito**: se manca il profilo, resta sulla simulazione e i suoi numeri.

## File della skill

- `scripts/montecarlo.py` — motore: config JSON → results JSON (bande, terminale, P(obiettivo), money multiple, shortfall).
- `references/metodologia.md` — modello, tre strati, metriche, limiti.
- `references/assunzioni.md` — assunzioni di mercato di partenza + disciplina.
- `assets/report-montecarlo.html` — template report (fan-chart con toggle, gauge obiettivo, tabella percentili).
