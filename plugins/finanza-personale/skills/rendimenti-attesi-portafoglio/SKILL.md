---
name: rendimenti-attesi-portafoglio
description: "Stima il rendimento atteso a 10 anni di un portafoglio con metodo top-down (DY+g per le azioni, YTW+roll-down per i bond) e bottom-up (capital market assumptions), al netto di TER, bollo e fisco italiano, e lo confronta con benchmark a pari peso (MSCI ACWI, S&P 500, Euro Aggregate Treasury). Produce un report HTML."
---

# Rendimenti attesi di portafoglio (top-down + bottom-up)

Risponde a **una sola domanda**: *quanto è ragionevole aspettarsi da questo portafoglio nei prossimi ~10 anni?* — e la risponde con numeri **osservabili oggi**, non con previsioni macro.

Serve a tre cose, in quest'ordine di importanza:
1. **Tarare le aspettative** dell'investitore (e del consulente) prima che lo faccia il mercato.
2. **Alimentare le decisioni di allocazione**: il premio atteso `(μ − r_f)` è l'input della quota azionaria (Merton/Choi) e l'`exp_return` della Monte Carlo.
3. **Confrontare** l'allocazione proposta con benchmark a pari peso, per capire cosa si sta guadagnando o pagando in termini di rendimento atteso — e quanto vale in **capitale terminale**.

Dottrina di riferimento: `consulenza-portafogli-etf/references/canone-the-bull/rendimenti-attesi.md` `[TB-339]`. Questa skill è l'**implementazione**: non ripete la dottrina, la esegue.

## Quando si attiva

- Costruzione **ex novo** di un portafoglio (FASE 3-bis del workflow di `consulenza-portafogli-etf`).
- **Rivalutazione** dell'asset allocation di un portafoglio esistente.
- **Ristrutturazione del PAC** che cambia i pesi (nuovo tilt).
- Domanda diretta: *"quanto rende X?"*, *"conviene più A o B?"*, *"il mio portafoglio batte l'ACWI?"*.
- Prima di ogni **Monte Carlo**, per fornirne i parametri.

Non si attiva per: valutare un singolo ETF contro i competitor (→ `analisi-documenti-investimento` modalità B), analizzare un singolo titolo di Stato (→ `analisi-titoli-di-stato-eu`), o costruire l'allocazione (→ `consulenza-portafogli-etf`).

## Workflow

1. **Raccogli i pesi** del portafoglio e classifica ogni gamba in tre categorie: `equity`, `bond`, `non_computable`. Se il portafoglio non è ancora definito, fermati: questa skill misura, non alloca.
2. **Raccogli i dati di input** seguendo `references/fonti-dati.md` — che dice *esattamente* dove si prende ogni numero e in che ordine di priorità. **Prima cerca live**, poi chiedi. Se un dato non è verificabile: `n/d` esplicito, mai un numero plausibile.
3. **Calcola il top-down** con `references/metodologia-top-down.md`. Non fare i conti a mano: `python3 scripts/rendimenti_attesi.py config.json results.json`.
4. **Calcola il bottom-up** con `references/metodologia-bottom-up.md` (CMA correnti ricomposte sugli stessi pesi) e **misura la dispersione** fra le case.
5. **Costruisci i benchmark** a pari peso con `references/benchmark-e-confronto.md` e calcolali con lo **stesso identico set di assunzioni** (stessa data, stessa `g`, stessa inflazione, stessa fiscalità).
6. **Genera il report** partendo da `assets/report-rendimenti-attesi.html`, iniettando `results.json`.
7. **Auto-verifica** con la checklist in fondo a questo file, poi salva nella **cartella di output dell'ambiente** (vedi `metodo-fiduciario` §10) e condividi il file.

## I quattro numeri (mai uno solo)

Ogni output riporta **sempre** questi quattro, affiancati e con la stessa metodologia:

| # | Cosa | Ruolo |
|---|---|---|
| 1 | **Top-down** del portafoglio | Stima **primaria**. È un fatto osservabile + una piccola assunzione. |
| 2 | **Bottom-up** ricomposto sugli stessi pesi | **Controllo incrociato** + misura dell'incertezza (dispersione fra case). |
| 3 | **Benchmark globale**: quota azionaria su **MSCI ACWI** + quota obbligazionaria su **Euro Aggregate Treasury** | Costo/beneficio del tilt geografico rispetto al mercato. |
| 4 | **Benchmark USA**: quota azionaria su **S&P 500** + quota obbligazionaria su **Euro Aggregate Treasury** | Costo/beneficio rispetto all'alternativa concentrata. |

Ogni numero va dato in **quattro strati**: lordo reale → lordo nominale → netto costi (TER + bollo) → netto fisco al termine. E il delta vs benchmark va espresso **anche in capitale terminale** sull'orizzonte reale dell'investitore.

## Guardrail (non negoziabili)

- **Non è una previsione.** È l'ordine di grandezza implicito nei prezzi di oggi, con la variazione delle valutazioni posta a zero *per convenzione dichiarata*. Correlazione storica con il realizzato ~0,5 sulle azioni, ~90% di varianza spiegata sui bond. **Sufficiente per pianificare, insufficiente per il market timing** — e va detto in ogni report.
- **Non innesca mosse tattiche.** Un rendimento atteso basso non è un segnale di uscita, di sospensione del PAC o di sovrappeso. Se la stima spinge verso una mossa, nominala come tentazione e riconducila alla regola (`analisi-macro.md` §regola d'oro). Se emerge uno shortfall si applica la gerarchia del conflitto **C-L**: **risparmio → orizzonte → obiettivo → *solo in ultimo* γ**. Mai "più azioni perché servono i soldi".
- **Oro, commodities, managed futures, cripto: fuori dal calcolo.** Nessun flusso da scontare ⇒ nessuna stima top-down possibile (principio 12 del canone). Si **rinormalizza** sui pesi computabili e si dichiara sempre la **% di copertura**. Sul residuo, al massimo una banda di scenario, mai un punto.
- **Mai inventare un input.** DY, YTW, duration, TER, quota governativa white-list: si verificano live sulla fonte primaria e si riporta **data del dato**. Meglio `n/d` che un numero plausibile.
- **Una sola convenzione per volta** — per-azione *oppure* aggregata (mai `DY + NBY + g_per_azione`: doppio conteggio); geometrica *oppure* aritmetica; una sola valuta base.
- **Dichiara sempre**: data dei dati, `g` assunta con fonte, inflazione assunta con fonte, orizzonte, base valutaria, convenzione, % di copertura.
- Materiale **educativo e di ragionamento**, non consulenza personalizzata ai sensi di legge né raccomandazione. Il capitale può ridursi.

## Composabilità

- **Con `consulenza-portafogli-etf`** — è la sua **FASE 3-bis**. Il canone (`rendimenti-attesi.md`) dà il *perché*; questa skill il *come*. I pesi arrivano dalla FASE 3, il risultato entra nella FASE 5 (output) e nel dossier di FASE 6.
- **Con `simulazione-montecarlo`** — le fornisce gli `exp_return` **per asset** invece della tabella di default. Regola: il top-down alimenta lo scenario base; il **minimo** delle CMA bottom-up alimenta lo scenario prudente; il **massimo** l'ottimista. La volatilità e le correlazioni restano input della Monte Carlo (questa skill non le stima).
- **Con `analisi-titoli-di-stato-eu`** — per le gambe in **singoli titoli di Stato** (BTP, Bund, BOT) il rendimento atteso è lo **YTM netto a scadenza** calcolato lì, non una stima: importalo e trattalo come input certo se il titolo è tenuto a scadenza.
- **Con `analisi-documenti-investimento`** — design system del report (sfondo chiaro, Inter, colori semantici) e modalità A per distillare le CMA appena pubblicate.

## File della skill

- `references/metodologia-top-down.md` — formule azioni e bond, i quattro strati (reale/nominale/netto costi/netto fisco), valuta, aggregazione di portafoglio, correzione geometrica.
- `references/metodologia-bottom-up.md` — capital market assumptions: quali case, come ricomporle sui pesi, dispersione, trappole (valuta, orizzonte, geometrico vs aritmetico, bias commerciale).
- `references/fonti-dati.md` — **dove si prende ogni numero**, con pattern di URL, priorità delle fonti, cosa chiedere all'utente e cosa no.
- `references/benchmark-e-confronto.md` — set di benchmark canonico, regole di costruzione, come si legge il delta.
- `references/carry-di-copertura.md` — **gamba obbligazionaria**: carry di copertura valutaria (formula, segno, ordine di preferenza delle fonti), indice governativo puro contro aggregate con credito, orizzonte pari alla duration di Macaulay, reinvestimento delle cedole, range bottom-up osservato.
- `scripts/rendimenti_attesi.py` — motore: config JSON → results JSON. Include `--selftest`.
- `assets/report-rendimenti-attesi.html` — template del report.

## Auto-verifica prima di consegnare

1. Ogni input numerico ha **fonte e data**? Nessun numero a memoria?
2. La **convenzione** (per-azione vs aggregata) è dichiarata e non mischiata?
3. La **% di copertura** è dichiarata e gli asset non stimabili sono esclusi, non azzerati?
4. Portafoglio e benchmark usano lo **stesso** set di assunzioni (data, `g`, π, fisco, orizzonte)?
5. I **quattro strati** ci sono (lordo reale, lordo nominale, netto costi, netto fisco)?
6. Il delta è espresso **anche in capitale terminale**, non solo in punti annui?
7. La **divergenza top-down/bottom-up** è quantificata e — se > ~1,5 pt — spiegata, non mediata?
8. C'è la **sensitivity su `g`** (±1 pt) e su π?
9. Il report dice esplicitamente che **non è una previsione** e che **non giustifica market timing**?
10. Nessuna riga suggerisce di alzare l'azionario per raggiungere un obiettivo (violazione di **C-L**)?
