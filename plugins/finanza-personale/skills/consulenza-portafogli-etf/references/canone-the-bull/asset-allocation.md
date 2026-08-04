# Canone The Bull — Asset Allocation (struttura, pesi, diversificazione, strumenti)

Fonti: `[TB-268]` portafoglio da zero · `[TB-303]` Choi/Merton/capitale umano · `[TB-306]` intervista a Choi (capitale umano rischioso, due-asset, volatility laundering) · `[TB-307]` diversificazione · `[TB-318]` tre-gambe / tre portafogli modello.

## Le tre strade all'asset allocation `[TB-268]`

1. **Lazy portfolio** — pre-impacchettato e tenuto a vita (60/40, Golden Butterfly, All Weather, Market portfolio). Rispettabilissimo ma poco personalizzabile.
2. **Asset allocation dinamica** — regola che adatta il portafoglio a indicatori macro (valutazioni, tassi) + criteri soggettivi (tolleranza, orizzonte). **Default di Spada** se capisci due-tre cose di finanza.
3. **Goal-based investing** — parte dagli obiettivi e ricostruisce a ritroso il portafoglio come somma di **sotto-portafogli/bucket** per scopo. Più intuitivo per il risparmiatore comune (si ragiona su *probabilità di fallire un obiettivo*, non su volatilità/Sharpe). Consacrato dai financial planner.

## Goal-based: esempio canonico `[TB-268]`

Famiglia modello (2 adulti ~36 anni, 2 figli; reddito netto 4.583 €/mese; reverse budgeting; **fondo emergenza = 6 mesi di spese *fisse*** su conto deposito svincolabile). Allocazione per obiettivo:
- **Casa più grande (5-7 anni)** → **30% azioni / 70% obbligazioni**.
- **Università figli (13-16 anni)** → **60/40**.
- **Semi-FIRE (25 anni)** → **85/15** (meno aggressivo del possibile perché è anche il core flessibile del patrimonio).
- **Blend finale**: ~**62/38** (poi + alternativi). La pianificazione **va aggiornata** avvicinandosi ai target (più conservativa); due venti a favore: realizzare un obiettivo libera flussi per gli altri; reddito che cresce nel tempo.

## Choi / Merton — quanto in azioni `[TB-303]`

- **La decisione più importante = quota azionaria.** Formula di **Merton** (per chi vive solo del portafoglio): quota azioni ∝ **(rendimento reale atteso − risk-free) / (varianza × γ)**. Direttamente proporzionale all'extra-rendimento atteso, inversamente alla varianza e al **coefficiente di avversione al rischio γ**. Esempio: ACWI, rendimento reale atteso 4,5%, risk-free reale 1,5%, dev.std 15% (var 0,0225) → (0,045−0,015)/(0,0225×γ).
- **Capitale umano (Choi)**: la formula diventa Merton **× (1 + capitale umano / capitale finanziario)**. Più il finanziario è piccolo rispetto all'umano → più azioni; e viceversa. Sconto del reddito futuro per rischio: bond-like ~3%, mixed (HY) ~5%, rischioso (equity) 7-8%. PV con la formula classica `Reddito/(1+sconto)^anno`.
- **γ (gamma)**: nella versione rigorosa, riflette la velocità con cui cala l'utilità marginale (esperimento della scommessa testa/croce sul reddito → "equivalente certo" rivela il γ). Nella **euristica di Spada** (regola di Merton semplificata, dal libro *Investire senza dubbi*), γ = media ponderata di **tolleranza** (quanto sopporti i cali), **capacità** (orizzonte) e **necessità** di rischio (quanto serve per gli obiettivi). Calibrazione utile **γ tra 2 e 4-5**: sotto 2 escono quote >100%, sopra 5 quasi nessuna differenza. Con premi al rischio 3-6% e γ 2-4 → portafogli **30-100% azioni** (dove cade la maggioranza).
- **Caveat sul "100% azioni" della formula di Choi**: (1) tieni l'indicazione di fondo (considera capitale totale, spesso siamo iper-conservativi per i motivi sbagliati); (2) il modello assume nessun vincolo di liquidità e solo ottimizzazione del consumo di vita → **gli obiettivi reali di breve-medio termine vanno gestiti ad hoc** (se vuoi la casa tra 5 anni, 100% azioni non va bene); (3) è ottimizzazione media-varianza (Markowitz→Merton): impostazioni alternative tipo **Risk Parity** investono meno in azioni; (4) suggerisce quote azionarie basse in pensione, ma Kitces/Pfau propongono un **glide path azionario crescente** in pensione (rischio di sequenza + inflazione).

## Choi — l'intervista: capitale umano rischioso e minimalismo a due asset `[TB-306]`

Approfondisce `[TB-303]` e in un punto **diverge** dalla dottrina The Bull. Datapoint che muovono una decisione:

- **Lineage rigorosa.** Merton 1969 (nessun reddito) → Merton 1971 (reddito da lavoro *privo di rischio*: il capitale umano è un enorme *bond* senza rischio; ricchezza totale = risparmi + PV dei salari scontati al risk-free → applicando la formula 1969 alla ricchezza totale, il portafoglio *finanziario* ottimale diventa più azionario, fino al 100%) → CGM 2005 (reddito *rischioso*). **Ancora empirica**: correlazione crescita-salari / azionario ≈ 0 per la famiglia mediana → il capitale umano rischioso **si comporta ancora come un grande bond** e attrae verso più azioni. È il fondamento del profilo aggressivo per giovani con reddito stabile e poco correlato.
- **Perché è un'*approssimazione*.** CGM non fornisce formula chiusa: risolve numericamente e mostra grafici per pochi set di parametri → inapplicabile al singolo. Choi-Liu-Liu risolvono migliaia di versioni CGM, **estraggono i tassi di sconto** del capitale umano e li approssimano con funzioni semplici → il foglio di calcolo. *Scarto dall'ottimo*: **non ho certezza su questo dato** — il transcript riporta 0,06% (TB-303) e 0,6% (TB-306): verifica sul paper *Practical Finance: An Approximate Solution to Lifecycle Portfolio Choice* (Choi, Liu, Liu, 2025).
- **γ — raffinamenti sull'elicitazione.** Scala teorica **1-10** (10 = livello "patologico"; oltre è pura preferenza). Esperimento dell'equivalente certo (testa 100k / croce 50k; neutrale al rischio → indifferenza a 75k; più avverso → punto di indifferenza più basso → γ da tabella). Tre avvertenze: la sensibilità dell'output a γ è **feature, non bug**; la differenza di allocazione **γ=1→2 ≫ γ=9→10**; **effetti di framing** (Kahneman) → lo stesso soggetto dà γ diversi secondo come poni la domanda → elicitazione rumorosa, da triangolare. Armonizza (non supera) la banda pratica di Spada **γ 2-4/5** di §Choi-Merton.
- **Risparmio: livellare i consumi vs livellare il tasso.** Vista accademica (utilità marginale decrescente): livella i *consumi* → nei 20 anni risparmia poco, nei picchi 40-50 risparmia molto. Vista finanza personale: livella il *tasso di risparmio* (~10-15% sempre). Choi riconosce merito a entrambe (interesse composto e "risparmio come muscolo" spingono a iniziare subito). Sfuma — non contraddice — il reverse budgeting (principio 1): la disciplina resta, ma la *quota* ottimale di risparmio varia con età e capitale umano.
- **Minimalismo a due asset (divergenza → C-J).** Choi è azioni + risk-free, senza oro/commodities/REIT/immobili: *equity premium puzzle* sì, **nessun** premio strutturale documentato per gli altri; **volatility laundering** sugli illiquidi (prezzi = stime, non prezzi di mercato). Tensione con la terza gamba The Bull: vedi registro conflitti **C-J**.
- **Limiti dichiarati dall'autore** (rinforzano i caveat di `[TB-303]`): il modello ottimizza **solo il consumo di vita**, tutto perfettamente aggiustabile; impegni non aggiustabili (casa, istruzione figli, business, FIRE datato) **non sono nel modello** → è un **ancoraggio mentale**, non l'allocazione finale. Conferma la separazione dal goal-based (`[TB-268]`).
- **Uso operativo dello strumento — adattamento euro OBBLIGATORIO.** Il Google Sheet è **parametrizzato USA**: σ azionaria **18,5% hardcoded** (Merton share in *log return*: `(ln(1+μ) − ln(1+r_f)) / (γ·σ²)`); μ reale default **5%**; r_f reale default **2%** (la guida suggerisce ~2,5% da TIPS 30y, dic-2025); **Social Security ≈ 40%** dell'ultimo salario; pensionamento **66**; traiettoria reddituale del *college graduate* USA (tab "Wage imputed"); fisco 401(k)/Roth. **Per l'area euro trasferiscono solo il metodo e il tab "Full inputs"** (redditi annui **netti, reali**, inseriti a mano fino a ~100 anni); il tab "Wage imputed" e lo scaffolding SS/TIPS non sono trasferibili. Per un ordine di grandezza euro-nativo **non replicare i tassi fittati USA**: usa il metodo trasparente di §Choi-Merton (PV dei redditi a **3% bond-like / 5% mixed / 7-8% equity-like** secondo la natura del reddito, poi Merton × (1 + CU/CF)), dichiarandolo **ancora/ordine di grandezza**, non output di un ottimizzatore. Link allo strumento: sito di James Choi / descrizione dell'episodio The Bull — **verificare live** (non riporto un URL non verificato).

## Diversificazione — la masterclass `[TB-307]`

- **Bassa correlazione ≠ correlazione negativa.** S&P 500 ~11%/anno, Treasury 5,6%, oro ~7% su 40 anni: tre strade diverse ma tutte verso l'alto. Se l'oro fosse *negativamente* correlato alle azioni avrebbe rendimento atteso negativo (come un ETF short, come un'assicurazione). Correlazione ~0 = metà volte stessa direzione, metà no.
- **Momenti in cui "tutto va giù insieme"**: 2022 (set: S&P −24%, bond −20%, oro −17%), 1994, 2001, 2008, 1973, crisi EM fine '90, Covid. L'oro spesso negativo nei primi giorni/settimane di uno shock.
- **Correlazione azioni-bond**: la negativa è stata l'**anomalia 1981-2021** (Campbell-Viceira; FMI feb-2026). Shock d'**offerta** (energia) → timori inflazione → rendimenti reali su → bond giù; shock **recessivi/da domanda** → bond su. Nelle **guerre** il rendimento reale dei bond è quasi sempre negativo (debito su, inflazione tollerata).
- **Cosa emerge**: (1) la diversificazione **non funziona nel breve** (non è fatta per giorno/settimana/mese/forse anno) — e "fallisce quando ne hai più bisogno" (Page & Panariello 2018); (2) le correlazioni **cambiano** in modo poco prevedibile → riformulare: "una certa diversificazione non funziona *in questo regime*, ma funziona in altri che ci sono stati e torneranno".
- **Perché diversificare (non-negoziabile) — tre motivazioni**:
  - **Epistemica**: ammettere di non conoscere il futuro; non trasformare il portafoglio in un'opinione assoluta sul mondo ("l'America vince sempre", "i bond proteggono sempre", "oro/bitcoin salverà tutto"). Costruire una struttura che non richieda di aver ragione su tutto e non collassi su un evento **left-tail**.
  - **Statistica**: asset con rendimenti/vol/correlazioni diverse migliorano, sul lungo, il rapporto rischio/rendimento o riducono profondità/frequenza dei drawdown.
  - **Comportamentale**: un portafoglio meno efficiente sulla carta ma **tollerabile** batte l'ottimo che ti fa vendere nel momento peggiore. La diversificazione aiuta **permanenza, continuità, disciplina**.
- **A cosa serve davvero**: evitare gli scenari **catastrofici** (un −50% richiede +100% e magari 13 anni di recupero vs 5 di un −30%). Un portafoglio diversificato (azioni+bond+oro) ha avuto **tempi di recupero inferiori alle singole asset class** che lo compongono, e **massimizza la probabilità di rendimento reale positivo su 10 anni** (cosa che nemmeno i bond garantiscono). Riduce la **dispersione** dei risultati nelle finestre rilevanti → "bilanciare crescita e accessibilità è il vero scopo dell'asset allocation".
- **Due errori opposti** `[TB-318]`: (1) **iper-diversificare** — ogni rischio che cancelli è un premio che perdi; l'obiettivo non è azzerare la volatilità ma ridurre la probabilità di un −30/40% nel momento peggiore; (2) **sovrastimare la tolleranza al rischio** — gli ultimi 3 anni sono stati rosei; essere davvero pronti a 2000-2002, 2007-2008, 2022, agli anni '70, e a **un decennio di zero rendimenti reali**. "Scoprire di aver sovrastimato la tolleranza durante un lungo bear market è un pessimo momento per la rivelazione."

## Cambio di regime e tre-gambe `[TB-318]`

- Dopo ~40 anni di globalizzazione/disinflazione, dal 2020-2022 il mondo è più frammentato: poco spazio fiscale, inflazione sopra target ("**3% is the new 2%**"), spesa militare, re-shoring, **fiscal dominance**. Sfavorevole alla "triade italiana" mattone-liquidità-BTP.
- **Il 60/40 non è morto** (vedi C-H), ma forse non più ottimale. Struttura preferita: **tre gambe** = equity globale + **obbligazioni IG** + **asset reali**.
- **Bond**: non è BTP, non è "reddito", non è "non perde mai". Nominali alta qualità (Global Aggregate hedged EUR o governativi euro) + (anni '70) **1/3 inflation-linked**.
- **Asset reali**: **oro** (debasement/geopolitica, vedi `P5a-oro.md`); **commodities** (Roll Select per il contango; vedi `P5a`); **managed futures** (DBMF; vedi `P5a`); **difesa + energy** (energy = settore a più bassa correlazione media col mercato; MSCI World Energy ~+1 pt/anno sul World su 30 anni, Aerospace&Defence ~+4 pt — ma **oggi cari**: difesa ~30× utili attesi vs World ~18×, energy ~20× → *oggi non li sceglierebbe partendo da zero*).

## I tre portafogli modello `[TB-318]`

- **Prudente** (orizzonte lungo ma sensibile alla volatilità di breve): **40-45% equity globale, 25-30% bond nominali, 10-15% inflation-linked, ~15% terza gamba reale** (es. metà oro / metà commodity). Rinuncia a un po' di crescita per stabilità comportamentale.
- **Medio** (tolleranza discreta, regge drawdown moderati): **60% equity, 15% nominali, 10% IL, 15% real asset**. Punto di equilibrio per molta platea retail: semplice, motore di crescita + gamba di stabilità + copertura di regime.
- **Aggressivo** (orizzonte molto lungo, ottima tolleranza, reddito stabile, compra durante i bear): **70% equity, 15% nominali, 15% oro-only** (oro perché su lungo termine ha reso più dei bond; commodities ~0). **È il portafoglio che Spada ha personalmente.**

## Strumenti citati (tickers, *time-sensitive* — verificare live) `[TB-268]`

> Da trattare come **mattoncini candidati con razionale**, non come "compra questo adesso". Verificare sempre ISIN/TER/replica/AUM/prezzo live (vedi `libreria-mattoncini.md`).

- **S&P 500**: SPDR `SP5A` (State Street, TER 0,03%).
- **Sviluppati ex-USA**: iShares `XUSE`.
- **Mercati emergenti**: Amundi `AEMM` (replica **sintetica**/swap; rischio controparte UCITS ≤10% → worst case ~0,6% del portafoglio).
- **Multifattoriale VMQ**: Invesco `IQSA`. Alternativa small-cap-value semi-attiva: Avantis (costo reale ~0,5%/anno).
- **Bond core**: Bloomberg **Global Aggregate EUR-hedged** ("il VWCE dei bond"; ~50% USA, eurozona <15%).
- **Inflation-linked EU**: Amundi `LYQ7` (dominato Francia/Italia; ~168 €/quota → scomodo per PAC mensili, meglio trimestrale).
- **Oro**: iShares `PPFB` (ETC).
- **Commodities**: iShares `IS39` (Bloomberg **Roll Select**).
- **Managed futures**: iMGP `DBMF`.
- **Lazy all-in-one**: Vanguard **LifeStrategy** (20-80% equity; market-cap, hedged bonds, auto-ribilanciato).

### Portafoglio modello "su misura" completo `[TB-268]`
56% azioni (18% S&P500 + 16% ex-USA + 6% EM + 17% multifattoriale globale → blend **50% USA / 40% sviluppati / 10% EM**, leggermente **contrarian/value-tilted** per la concentrazione Big Tech) · 34% bond (24% Global Aggregate hedged + 10% IL europei) · 10% alternativi (5% oro + 5% commodities). **Ribilanciare quando un peso varia 10-20% in relativo** rispetto al target.

## Broker `[TB-318]`

**Fineco** (sponsor; quello che Spada usa dal suo primo ETF): sotto i 30 anni PAC gratuiti; 800+ ETF (iShares, Amundi, Xtrackers, Fidelity, FAM) a zero commissioni; piano Replay per PAC (mensile/trimestrale/bimensile) su ETF/ETC/ETN.

<!-- VERSIONE FILE -->
**Episodi:** TB-268, TB-303, TB-306, TB-307, TB-318. **Stato:** completo. **Time-sensitive:** tickers/TER/prezzi, valutazioni settoriali, pesi dei tre portafogli legati al regime; **parametri del foglio Choi** (σ 18,5%, μ 5% reale, r_f 2% reale, SS 40%, pensionamento 66 — USA, dic-2025); scarto dall'ottimo del foglio (0,06% vs 0,6%, da verificare sul paper).
