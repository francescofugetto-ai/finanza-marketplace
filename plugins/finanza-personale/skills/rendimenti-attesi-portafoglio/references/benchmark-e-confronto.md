# Benchmark e regole di confronto

Il rendimento atteso in assoluto dice poco. La domanda utile è: **rispetto a cosa?** — cioè, cosa sto guadagnando o pagando, in rendimento atteso, per il tilt che ho scelto rispetto all'alternativa semplice.

---

## 1. Set di benchmark canonico

Fisso, verificato, non da chiedere all'utente. **Riverificare ISIN/TER prima di ogni uso**: cambiano.

| Ruolo | Strumento | ISIN | TER | Note (verificate) |
|---|---|---|---|---|
| **Benchmark azionario globale** | iShares MSCI ACWI UCITS ETF USD (Acc) | `IE00B6R52259` | 0,20% | indice **MSCI ACWI**, 2.461 titoli, 23 DM + 24 EM, ~85% dell'investibile globale; replica fisica a campionamento; accumulazione; domicilio Irlanda; AUM ~30 mld € |
| **Benchmark azionario USA** | iShares Core S&P 500 UCITS ETF USD (Acc) | `IE00B5BMR087` | 0,07% | indice **S&P 500**, 504 titoli; replica fisica **totale**; accumulazione; domicilio Irlanda; AUM ~131 mld €; tracking difference storica **negativa** (ha battuto il TER) |
| **Benchmark obbligazionario** | Vanguard EUR Eurozone Government Bond UCITS ETF (Acc) | `IE00BH04GL39` | 0,07% | indice **Bloomberg Euro Aggregate: Treasury**, ~520 titoli governativi area euro, scadenze > 1 anno; accumulazione; domicilio Irlanda; AUM ~4 mld € |

### ⚠️ Due precisazioni sul benchmark obbligazionario

1. **È un "Treasury", non un "Aggregate" pieno.** L'indice contiene **solo governativi** dell'area euro: niente corporate IG, niente covered. È una scelta legittima e coerente (è lo stesso indice usato in `[TB-339]`), ma il nome "Euro Aggregate" può ingannare. Un portafoglio con gamba corporate IG viene confrontato con un benchmark **solo governativo**: il delta incorpora anche il premio al credito. Dichiararlo.
2. **Duration ≠ scadenza media.** Al 30/06/2026: scadenza media **8,6 anni**, duration **7,0 anni**. L'orizzonte di validità della stima è la **duration** (7 anni), non la scadenza. Se l'orizzonte dell'investitore è 25 anni, la stima resta il miglior punto di partenza ma va detto che oltre la duration riemerge il rischio di reinvestimento.

### Sostituzioni ammesse (dichiarandole)

- Se il portafoglio ha **duration obbligazionaria molto diversa** (es. gamba a 1-3 anni), affianca un secondo benchmark obbligazionario di duration comparabile: altrimenti si confronta rischio-tasso diverso.
- Se il portafoglio è **100% azionario**, i benchmark diventano 100% ACWI e 100% S&P 500.
- Se la gamba obbligazionaria è in **singoli BTP**, il benchmark ETF resta valido come termine di paragone, ma va segnalato che il portafoglio ha rischio emittente concentrato mentre il benchmark è diversificato su ~520 titoli (`[TB-187]`).

---

## 2. Regola di costruzione

```
1. Classifica ogni gamba:  equity | bond | non_computable
2. copertura        = Σ pesi(equity) + Σ pesi(bond)
3. w_E              = Σ pesi(equity) / copertura
   w_B              = Σ pesi(bond)   / copertura
4. Benchmark 1 (globale) = w_E × ACWI        + w_B × Euro Agg Treasury
   Benchmark 2 (USA)     = w_E × S&P 500     + w_B × Euro Agg Treasury
5. Calcola tutti e tre con LO STESSO set di assunzioni
```

**"Lo stesso set" significa**: stessa data dei dati · stessa `g` per mercato · stessa inflazione attesa · stesso trattamento del cambio · stessa fiscalità · stesso orizzonte · **TER propri di ciascuno** (i benchmark portano il proprio TER: è parte del confronto).

### Esempio svolto

Portafoglio: 20% ex-USA · 40% USA · 10% EM · 30% BTP · (0% non computabile)
→ copertura 100% · `w_E = 0,70` · `w_B = 0,30`
→ **Benchmark 1**: 70% `IE00B6R52259` + 30% `IE00BH04GL39`
→ **Benchmark 2**: 70% `IE00B5BMR087` + 30% `IE00BH04GL39`

Se lo stesso portafoglio avesse 10% di oro (e quindi 18/36/9/27), la copertura scenderebbe a **90%** e i benchmark si costruirebbero sui pesi **rinormalizzati** (70/30), dichiarando che il confronto vale sul 90% del portafoglio.

---

## 3. Come si legge il delta — quattro letture, non una

### 3.1 Delta annuo (punti percentuali)
`Δ = E[r]_portafoglio − E[r]_benchmark`. È il titolo, ma da solo è fuorviante: 0,3 pt sembrano nulla.

### 3.2 Delta in capitale terminale — **obbligatorio**
```
Δ_montante = (1 + r_p)^T / (1 + r_b)^T − 1
```
È qui che il numero diventa una decisione. Riferimenti: 2 pt/anno di differenza valgono **−17,5%** di montante su 10 anni e **−38,2%** su 25.

### 3.3 Delta di rischio — **obbligatorio quando si confronta con l'S&P 500**
Il benchmark USA è **100% concentrato su un paese**, con il **rendimento atteso top-down più basso** fra i grandi mercati (il DY USA è il più basso: si compra il flusso più caro) ma con la **dispersione bottom-up più alta** (6,1%-8,5% fra le case). Un portafoglio globale che "perde" 0,2 pt contro l'S&P 500 sul bottom-up non sta perdendo: sta comprando diversificazione geografica a un prezzo. **Non presentare mai il delta vs S&P 500 come "batto/non batto"**: è un confronto fra due profili di rischio diversi, ed è precisamente il tipo di lettura che genera home bias e recency bias (canone, principio 11).

### 3.4 Delta di costo e di gestibilità
TER medio ponderato, numero di strumenti da ribilanciare, costi di transazione del PAC, attrito fiscale del ribilanciamento (le minusvalenze da ETF non compensano le plusvalenze da ETF). Un tilt che vale +0,15 pt teorici e costa +0,20 pt di TER e complessità **è una perdita**.

---

## 4. Tabella di sintesi del report

| | Top-down | Bottom-up (media) | Bottom-up (range) | Montante ×T |
|---|---|---|---|---|
| **Portafoglio proposto** | | | | |
| **Benchmark 1 — ACWI + Euro Agg Treasury** | | | | |
| **Benchmark 2 — S&P 500 + Euro Agg Treasury** | | | | |
| **Δ vs Benchmark 1** | | | | |
| **Δ vs Benchmark 2** | | | | |

Sotto la tabella, sempre: **copertura %**, **data dei dati**, **`g` assunta con fonte**, **π assunta con fonte**, **orizzonte**, **valuta base**, **convenzione**.

---

## 5. Cosa il confronto NON autorizza

- **Non autorizza a inseguire il benchmark che oggi ha la stima più alta.** Il top-down oggi favorisce sistematicamente i mercati a DY più alto (ex-USA, EM): è meccanica, non è una previsione che l'ex-USA batterà gli USA. `[TB-339]`: *"non significa che gli USA debbano per forza andare peggio, ma che oggi partono da valutazioni più esigenti."*
- **Non autorizza il market timing.** Correlazione ~0,5 sulle azioni: significativa, insufficiente.
- **Non autorizza a cambiare allocazione fuori dalla regola di ribilanciamento** scritta in FASE 5. Se il delta suggerisce una mossa, quella mossa si valuta alla **prossima revisione strutturale**, non oggi perché il numero è uscito così.
- **Non autorizza ad alzare l'azionario per colmare uno shortfall**: gerarchia del conflitto **C-L** — risparmio → orizzonte → obiettivo → *solo in ultimo* γ.
