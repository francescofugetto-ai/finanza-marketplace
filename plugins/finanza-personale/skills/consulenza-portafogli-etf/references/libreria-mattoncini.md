# Libreria di mattoncini (ETF per gamba)

Menu di **categorie** e **esempi noti** di strumenti per ciascun pilastro. È un punto di partenza, NON una raccomandazione d'acquisto.

> ⚠️ **Dati da verificare LIVE al momento dell'uso** per ogni strumento citato, perché cambiano e non vanno mai inventati:
> - **ISIN** esatto e **ticker** sulla borsa di riferimento (es. Borsa Italiana / Xetra);
> - **TER** corrente;
> - **politica:** accumulazione (Acc) vs distribuzione (Dist);
> - **replica:** fisica (totale/campionamento) vs sintetica;
> - **domicilio** (di norma Irlanda/Lussemburgo per efficienza fiscale UCITS) e **dimensione/liquidità** (AUM);
> - **spread bid-ask** medio (proxy di liquidità ed efficienza operativa);
> - **disponibilità a costo zero / nel PAC** sul broker dell'investitore.
>
> Se non puoi verificare un dato, dichiaralo e indica la fonte (KID, prospetto, sito emittente, justETF, sito del broker). **Non riportare ISIN o TER a memoria.**

## Criteri di selezione (validi per ogni gamba)
Soglie preferenziali da applicare e verificare; se un candidato non le rispetta, segnalalo e motiva l'eventuale deroga.
- **Indice** ampio e riconosciuto.
- **TER minimo:** **< 0,20%** per ETF che replicano **solo indici globali/core**; per gamme più specialistiche (fattoriali, settoriali, obbligazionari specifici) accetta TER più alti solo se giustificati dalla funzione.
- **Struttura UCITS**, domiciliato in UE.
- **Accumulazione** (in fase di accumulo).
- **Replica fisica** (totale o a campionamento), preferita alla sintetica.
- **Spread bid-ask** contenuto: indicativamente **< 0,02%** (proxy di liquidità ed efficienza in negoziazione).
- **Dimensione (AUM): > 500 mln €** (riduce il rischio di chiusura/fusione del fondo e migliora la liquidità).
- **Coerenza col broker:** **possibilmente dalla lista a 0 commissioni** (es. lista "ETF a costo zero" FINECO se il broker è FINECO), per acquisto e PAC gratuiti.
- Obiettivo complessivo: **TER medio ponderato di portafoglio basso** e portafoglio gestibile.

## Pilastro 2 — Liquidità di emergenza investita
- **ETF monetario euro** (overnight/€STR) — bassa volatilità, alta liquidità.
- **ETF governativo area euro a brevissima scadenza** (0–1 / 1–3 anni) — duration molto corta.
- Alternativa non-ETF: **conto deposito svincolabile**.

## Pilastro 3 — Azionario globale (core)
- **Mondo in 1 ETF:** indice **FTSE All-World** (include large+mid e mercati emergenti) o **MSCI ACWI**; in alternativa **MSCI World** (solo sviluppati, da affiancare eventualmente a un emergenti).
- **Scomposizione "pro" (esempio coerente con un tilt verso gli emergenti):**
  - Azionario **USA** (es. MSCI USA / S&P 500),
  - Azionario **World ex USA** (sviluppati ex-USA),
  - Azionario **Mercati Emergenti**.
  Pesi scelti per ottenere l'esposizione geografica voluta; verifica che la somma non crei sovrapposizioni o buchi (es. paesi di confine sviluppati/emergenti).
- **Tilt fattoriale (jolly, ≥~33% dell'azionario):** versioni **World Value** e **World Momentum** (o multifactor). Da usare solo secondo le regole del jolly in `architettura-5-pilastri.md`.
- **Min Vol (difensivo, alternativo non aggiuntivo):** **MSCI World Minimum Volatility** — sostituisce una quota dell'azionario tradizionale, non si somma sopra; attenzione ai doppioni con i settori difensivi.

## Pilastro 4 — Obbligazionario (condizionale)
- **Goal-based, scadenza nota:** **bond singolo** governativo area euro (o IG di qualità) con maturità vicina alla data dell'obiettivo; in alternativa ETF a **scadenza target** (target maturity).
- **Stabilità generale:**
  - **Euro Aggregate** (govt+corporate IG in euro), oppure
  - **Global Aggregate EUR-hedged** (copertura del cambio in euro: per l'investitore in euro è quasi sempre la scelta corretta sull'obbligazionario in valuta estera).
- **Liquidità/ribilanciamento:** **governativo euro a breve termine (1–3 anni)**, duration corta.
- Evita di usare un **IG corporate lungo** come se fosse "liquidità difensiva": è un ruolo diverso.

## Pilastro 5 — Oro / commodities
- **Oro fisico:** **ETC su oro fisico** (replica fisica, allocato). Ricorda l'esposizione al dollaro per chi è in euro; esistono versioni con copertura del cambio (valuta costo/beneficio).
- **Commodities ampie:** ETF su panieri diversificati di materie prime (energia, metalli, agricoltura). Solo se coerente col profilo; aiuto concentrato in shock energetico-geopolitici.

## Strategie alternative (approfondimento difensivo, near-exit)
Per chi approfondisce la resilienza anticrisi (vedi documento "ETF Italia"):
- **Managed Futures / Trend Following** — payoff scollegato dal premio al rischio azionario/obbligazionario; per investitori europei l'offerta è limitata (verifica disponibilità, costi e domicilio dello strumento al momento dell'uso). Richiede di tollerare anni di rendimenti piatti/negativi nei mercati laterali. Strumento avanzato, non per tutti i profili.

## Nota broker (verifica condizioni correnti)
Le condizioni dei broker italiani cambiano: chiedi sempre quale broker userà l'investitore e **verifica live** piani tariffari, ETF a costo zero, gratuità del PAC e sconti legati all'età. Broker comuni in area euro/IT: **FINECO, Scalable Capital, Directa, Trade Republic**. Non dare per acquisite condizioni "a memoria": confermale prima di costruire il piano costi.

**Checklist di confronto broker (verifica per ciascuno):**
1. **ETF a costo zero**: c'è una lista? Gli strumenti scelti sono dentro?
2. **PAC gratuito** sugli ETF scelti?
3. **Canone/condizioni per età**: eventuali agevolazioni under-X; costo per la fascia d'età dell'investitore.
4. **Regime fiscale**: amministrato (tasse gestite dall'intermediario, più semplice per neofiti) vs dichiarativo (l'investitore gestisce la dichiarazione)? È spesso il fattore decisivo per chi parte.
5. **Domicilio del conto** (IT vs estero) e implicazioni (es. quadro RW, dichiarativo).
6. **Costi di transazione** oltre il PAC e spread operativi.
Per un neofita la **semplicità fiscale** pesa spesso più del centesimo di commissione risparmiato.
