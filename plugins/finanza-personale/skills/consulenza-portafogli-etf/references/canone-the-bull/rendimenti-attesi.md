# Canone The Bull — Rendimenti attesi (tema trasversale)

Fonti: `[TB-339]` "Quanto renderanno i tuoi investimenti nei prossimi 10 anni?" (luglio 2026) — script + PDF *Grafici e Takeaway principali*.
Rimandi: `[TB-222]`, `[TB-241]` (prezzo = flussi scontati) · `[TB-288]` (buyback/emissioni) · `[TB-313]` (diluizione EM) · `[TB-318]` (valutazioni alte → aspettative, non attesa) · `[TB-303, TB-306]` (Merton/Choi: il premio atteso è un *input* della quota azionaria).

> **Perché questo file è trasversale e non un pilastro.** Il rendimento atteso non è un mattoncino: è il **parametro** che entra nella quota azionaria (Merton), nella Monte Carlo, nella P(obiettivo) e nella conversazione sulle aspettative. Sta accanto a `inflazione.md`, non accanto a `P3`/`P4`.
>
> **Implementazione operativa: skill separata.** Formule, protocollo dati, script e report vivono nella skill `rendimenti-attesi-portafoglio`. Qui c'è la **dottrina**: perché si fa, quale metodo prevale, cosa NON si può stimare, che uso se ne fa.

---

## 1. La domanda e le due strade `[TB-339]`

"Quanto renderà investire nei prossimi dieci anni" è **il numero su cui poggia tutto il resto della vita finanziaria**: quanto risparmiare ogni mese, a che età smettere di lavorare, quanto prelevare da vecchi. Prevedere con precisione è impossibile; **decidere in base ad aspettative largamente sbagliate è un disastro annunciato**.

Due strade per stimarlo:

- **BOTTOM-UP** — le *capital market assumptions* delle grandi case (BlackRock, Amundi, J.P. Morgan, Capital Group, Schwab). Partono da aziende, settori, scenari macro. **È previsione dalla prima all'ultima riga.**
- **TOP-DOWN** — teoria economica applicata ai **prezzi di oggi**: si estrae il rendimento implicito dai flussi di cassa osservabili. Funziona **solo** per asset che pagano flussi (azioni e obbligazioni).

**Tesi canonica: il top-down è più robusto.** Tre motivi (timeless):

1. **Il pezzo più grande del rendimento è un fatto, non una previsione.** Il dividend yield di oggi e lo yield to maturity di oggi sono lì, **osservabili**. Il bottom-up li deve indovinare.
2. **L'unico pezzo stimato — la crescita — è piccolo e stabile.** I tassi di crescita degli utili variano lentamente: sbagliare la crescita di un punto intero (che è tanto) sposta poco il risultato su dieci anni. Il grosso è ancorato allo yield di partenza.
3. **Non richiede opinioni forti da validare.** Non serve avere ragione sull'Iran, sulla Fed, sull'AI. *"Il metodo funziona proprio perché non prova a essere intelligente. È umile. E in finanza, l'umiltà rende."*

Riferimento accademico: **Antti Ilmanen** (AQR), *Expected Returns* (2011) e *Investing Amid Low Expected Returns* (2022). Ancora storica: **Fama** — prezzi alti rispetto ai dividendi ⇒ rendimenti futuri inferiori; prezzi bassi ⇒ superiori.

---

## 2. Formula azionaria (timeless) `[TB-339]`

Un'azione è **una pretesa su contante futuro**. Il rendimento di lungo periodo non può che venire da tre pezzi:

```
E[r] reale  =  DY  +  g  +  ΔV
```

- **DY** — dividend yield iniziale (quanto l'azienda ti paga adesso, in proporzione a quanto la paghi).
- **g** — crescita **reale** degli utili/free cash flow **per azione**.
- **ΔV** — variazione delle valutazioni (l'"umore del mercato": euforia/paura).

**ΔV si pone deliberatamente a ZERO.** Non perché le valutazioni non cambieranno, ma perché nessuno sa se tra dieci anni il mercato sarà più caro o più economico: è una scommessa, e **la cosa più onesta è metterla a zero**, ripulendo la formula dal suo elemento più volatile. Più si allunga l'orizzonte, più l'umore si attenua e restano i fondamentali: *"nel breve contano come si gonfiano e sgonfiano i prezzi; su dieci anni contano quasi solo utili, dividendi e buyback."*

Per il nominale si aggiunge l'inflazione attesa: `E[r] nominale ≈ E[r] reale + π`.

**Il pregio della formula non è la precisione puntuale, ma la coerenza come *ordine di grandezza*** tra stima e risultato realizzato. Correlazione storica tra rendimento di partenza e rendimento realizzato ≈ **0,5** (`[TB-339]`, Ilmanen 2025): *"non abbastanza alta per fare market timing, ma decisamente alta per essere significativa e segnare il percorso di lungo termine."* La parte che sfugge è esattamente l'espansione/contrazione dei multipli — quella che nessuno ha mai previsto con costanza.

**Corollario anti-narrativa** (da usare con l'investitore): il metodo **non richiede** che i prezzi debbano sgonfiarsi. I multipli possono restare alti per sempre (più investitori retail, ETF che hanno demolito i costi). Ma **partendo da prezzi alti rispetto ai flussi distribuiti, il rendimento implicito è meccanicamente più basso**, *anche senza alcuna compressione del P/E*. È la stessa legge di `[TB-222]`/`[TB-241]` (prezzo su = rendimento atteso giù) vista dal lato del calcolo.

> **In questa prospettiva le azioni si valutano come obbligazioni: il rendimento di partenza spiega il grosso del rendimento atteso.** Coerente con `[TB-241]` ("le azioni sono fondamentalmente obbligazioni").

### 2-bis. Convenzione per-azione vs aggregata — la trappola del doppio conteggio ⚠️

Non è nell'episodio ma è **necessario** per non sbagliare il conto, ed è già implicito nel canone (`[TB-288]` buyback/emissioni, `[TB-313]` diluizione EM). Esistono due decomposizioni **equivalenti ma non miscelabili**:

- **(A) per-azione** — `DY + g(EPS per azione)`. La crescita per azione **incorpora già** l'effetto dei buyback netti.
- **(B) aggregata** — `DY + NBY + g(utili aggregati)`, dove NBY = net buyback yield (riacquisti − emissioni).

Sommare `DY + NBY + g(EPS per azione)` **conta due volte i buyback**. Le stime AQR usate in `[TB-339]` sono **crescita reale degli utili per azione** → convenzione **(A)**. Regola operativa: **dichiarare la convenzione e non mischiarla mai**.

Rilevanza pratica per i mercati emergenti (`[TB-313]`): negli EM il saldo netto è storicamente **emissione** (diluizione), quindi la crescita *aggregata* sovrastima molto quella *per azione*. Usare una stima di crescita per azione — non il PIL, non gli utili aggregati.

### 2-ter. Stima della crescita `g` — l'unico punto di assunzione

- **Ancora storica**: gli utili per azione sono cresciuti, al netto dell'inflazione, in un range di **1-2 punti percentuali all'anno** nei mercati sviluppati.
- Le crescite recenti sono state molto più elevate: **"è irrealistico e poco prudente proiettarle indefinitamente nel futuro"**. `[TB-339]` conferma qui il principio di `[TB-318]` sul non estrapolare la fase eccezionale post-Covid.
- Concessione ammessa: la qualità dei profitti è **strutturalmente migliorata** (aziende meno capital-heavy, meglio gestite, più profittevoli), quindi stime moderatamente superiori all'ancora storica sono difendibili.
- **Set AQR 2026 usato nell'episodio** (*time-sensitive*): USA **2,7%** · sviluppati ex-USA **2,5%** · emergenti **2,6%**.
- Disciplina: `g` è l'unica assunzione, quindi **va dichiarata con fonte e data** e sottoposta a sensitivity (±1 pt).

---

## 3. Formula obbligazionaria (timeless) `[TB-339]`

Per le obbligazioni **il metodo diventa quasi scientifico**:

```
E[r] nominale ≈ YTM (o YTW) iniziale  +  roll-down
```

- Vale per un **portafoglio a duration costante** (= un ETF obbligazionario), su un orizzonte coerente con la durata media del portafoglio.
- **Roll-down**: se i titoli non vengono portati a scadenza ma continuamente rinnovati e la curva non si inverte, l'esposizione a duration costante paga in media **un piccolo rendimento extra**.
- **Aritmetica del recupero** (già in `P4` §aritmetica, qui riformulata come *previsione*): quando i tassi salgono il prezzo scende oggi, ma **da quel momento le cedole si reinvestono a tassi più alti**, e le due cose si compensano intorno a un orizzonte pari alla durata media. *"Il prezzo può ballare nel mezzo, ma il punto d'arrivo è scritto nel punto di partenza."*

**Il dato da portarsi a casa**: sul mondo obbligazionario il rendimento di partenza spiega **circa il 90%** di quello che succede davvero nei dieci anni successivi (`R² ≈ 89%` sui rendimenti a 5 anni successivi, Bloomberg U.S. Aggregate, J.P. Morgan *Guide to the Markets*). *"È quasi deterministico. Il rendimento di partenza di un paniere di bond è quasi una profezia che si autoavvera, per pura matematica finanziaria."*

**Metrica corretta**: nei panieri con titoli callable si usa lo **yield to worst**, non lo yield to maturity. Lo YTW è una buona approssimazione del rendimento atteso **se l'orizzonte è coerente con la scadenza media del portafoglio**; non elimina la volatilità nel frattempo.

> **Precisazione tecnica (non nell'episodio, da applicare).** L'orizzonte di immunizzazione è la **duration di Macaulay**, non la scadenza media: sono due numeri diversi (es. Vanguard Euro Aggregate Treasury al 30/06/2026: scadenza media **8,6 anni**, duration **7,0 anni**). Usare la **duration** come orizzonte di validità della stima. Oltre la duration riemerge il rischio di reinvestimento.

**Perché le azioni sono meno precise delle obbligazioni**: *"un bond non può avere rendimento illimitato — alla scadenza viene rimborsato a 100, non a 150. Un'azione può andare a zero o crescere dell'800% in un anno."* Il range del rendimento atteso azionario è quindi strutturalmente più largo.

---

## 4. Cosa NON si può stimare `[TB-339]`

**Per oro, materie prime e altri asset puramente speculativi, stimare i rendimenti attesi è "letteralmente un tiro di dadi".** Manca il flusso di cassa da scontare.

È la stessa linea del **principio trasversale 12** (`[TB-241]`, `[TB-222]`): azioni e obbligazioni = *income-generating*, quindi stimabili; oro, commodities, Bitcoin, arte = speculativi, il valore dipende solo dall'aspettativa di apprezzamento.

**Conseguenza operativa non negoziabile:** oro, commodities, managed futures, crypto **escono dal calcolo top-down**. Il portafoglio si stima sulla **quota coperta** e si dichiara sempre la **percentuale di copertura**. Sul residuo si mostra al più una **banda di scenario**, mai una stima puntuale.
Nota: che le case d'investimento pubblichino un numero per l'oro (media bottom-up ~5,8% a lug-2026, solo 2 case su 5) **non lo rende stimabile**: è la loro opinione, non un rendimento implicito osservabile.

---

## 5. Perché il bottom-up ha meno rango `[TB-339]`

Non va buttato — ma va collocato.

- **Varianza opinion-dependent**: ogni casa prende posizione su fattori macro e formula stime di conseguenza. Sullo stesso S&P 500 a 10 anni: BlackRock **8,5%**, Schwab e Capital Group **6,1%** (lug-2026).
- **Bias commerciale, da nominare senza malignità**: *"le società di asset management vendono prodotti di investimento… ciascuna avrà qualche bias a seconda di dove sta puntando come strategia commerciale."*
- **Stessi temi, prescrizioni opposte**: BlackRock sovrappesa USA e infrastruttura AI e sottopesa i Treasury lunghi; Amundi è quasi speculare (neutrale USA, positiva Europa/Giappone/EM/oro); J.P. Morgan predica bilanciamento; Capital Group e Schwab guardano ex-USA. *"Gli outlook servono a capire gli scenari, non a ricevere istruzioni scolpite nella pietra."*
- **Coerenza maggiore sul fixed income** che sull'azionario: è più semplice stimare i governativi (§3).

**Uso legittimo del bottom-up**: capire i **rischi**, non farsi trovare impreparati, eventualmente decidere se inclinare un filo verso Europa o emergenti. **Non** per rispondere a "quanto renderà".

**Convergenza come validazione.** Le stime top-down non si discostano molto dalla media delle assumptions: è un **controllo incrociato**, non una coincidenza. Se le due strade divergono molto, la divergenza è essa stessa informazione (→ conflitto **C-K**).

---

## 6. Cosa farne — le tre mosse `[TB-339]`

1. **Tarare le aspettative.** *"Sappiamo tutti che per un secolo l'S&P 500 ha reso il 10% all'anno. Dal 2009 a oggi ha reso oltre il 16%. Per i prossimi 10-15 anni faremmo bene ad avere aspettative molto più modeste."* Quel 10% nasconde un pezzo grosso di **espansione delle valutazioni** difficilmente ripetibile. **6-7% non è una delusione: è realismo.** *"Chi pianifica il futuro su un dieci per cento all'anno si sta prendendo in giro."*
2. **Guardare lo yield, non l'umore.** Davanti a "i mercati saliranno / crolleranno", una sola domanda: **da quale rendimento di partenza sto comprando?** Il dividend yield, il rendimento a scadenza. *"Quello è il faro. Il resto, con affetto, è intrattenimento."*
3. **Adattare il piano finanziario.** Se il rendimento azionario atteso è basso rispetto al rischio richiesto → si può considerare più bond o altri asset. Se il rendimento del portafoglio non permette di raggiungere gli obiettivi → **aumentare il tasso di risparmio** e investire di più. (Sequenza corretta e gerarchia delle leve: conflitto **C-L**.)

> **Chiusura canonica:** *"Non un numero da credere sulla fiducia, ma un metodo che potete rifare voi, tra un anno, tra cinque, con i dati aggiornati. Perché i dati cambiano, ma la formula no."*
> Questo è ciò che rende `[TB-339]` **timeless**: la formula, non i numeri.

---

## 7. Esempio canonico di aggregazione `[TB-339]`

Portafoglio **70% MSCI ACWI + 30% Bloomberg Euro Aggregate Treasury**:
`0,70 × 6,7% + 0,30 × 3,0% = 5,6%` nominale atteso.

*"Non è un numero scritto nella pietra. Ma nel momento in cui formulo i miei piani finanziari devo fare assunzioni sul rendimento atteso e reagire di conseguenza."*

Media pesata semplice dei rendimenti di componente. Raffinamenti (bonus di ribilanciamento, conversione aritmetico/geometrico, valuta, fisco, TER): skill `rendimenti-attesi-portafoglio`.

---

## 8. Snapshot numerico luglio 2026 — **TIME-SENSITIVE, da rifare** ⏳

> Congelati qui **solo** come esempio svolto e ordine di grandezza. **Non riusarli**: il metodo va rieseguito con dati live (fonti in `rendimenti-attesi-portafoglio/references/fonti-dati.md`).

**Top-down** (MSCI factsheet 30/06/2026 + crescita AQR + inflazione 2,5%):

| Indice | DY | g reale | E[r] reale | +π | E[r] nominale |
|---|---|---|---|---|---|
| MSCI USA | 1,12% | 2,7% | 3,72%* | 2,5% | 6,22%* |
| MSCI World ex-USA | 2,56% | 2,5% | 5,06% | 2,5% | 7,56% |
| MSCI EM | 1,93% | 2,6% | 4,53% | 2,5% | 7,03% |
| **MSCI ACWI** | **1,57%** | **2,6%** | **4,17%** | **2,5%** | **6,67%** |

\* **Incoerenza aritmetica rilevata nella fonte**: 1,12 + 2,7 = **3,82**, non 3,72 (e quindi 6,32 nominale, non 6,22). Le altre tre righe tornano esatte. Scostamento 0,10 pt sulla sola riga USA — da verificare sul materiale originale prima di riusare la riga. *(Lo script parlato riporta poi numeri ancora diversi — "3,6% USA", "4,5% ex-USA ed EM", "globale sotto il 4%" — incompatibili con le slide: **prevalgono le slide**, che portano i dati MSCI e tornano su 3 righe su 4.)*

**Obbligazionario**: Vanguard EUR Eurozone Government Bond (Bloomberg Euro Aggregate Treasury), factsheet 31/05/2026 citato nell'episodio: YTM **3,12%**, scadenza media ~9 anni. *Aggiornamento verificato al 30/06/2026: YTW **3,11%**, cedola media 2,6%, scadenza media **8,6 anni**, duration **7,0 anni**, 520 titoli, qualità media A+.*

**Bottom-up** — capital market assumptions a 10 anni, lug-2026 (presumibilmente **nominali in USD** — da verificare per casa):

| Asset | BlackRock | J.P. Morgan | Amundi | Capital Group | Schwab | Media |
|---|---|---|---|---|---|---|
| S&P 500 | 8,5% | 6,7% | 6,5% | 6,1% | 6,1% | **6,8%** |
| Sviluppati ex-USA | 8,0% | 7,5% | 7,1% | 5,7% | 7,2% | **7,1%** |
| Emergenti | 7,3% | 7,8% | 7,2% | 6,5% | 7,1% | **7,2%** |
| US Treasury | 4,6% | 4,1% | 4,4% | 4,0% | 4,3% | **4,3%** |
| Sviluppati IG | 4,4% | 4,7% | 3,5% | 4,3% | 4,0% | **4,2%** |
| Debito EM | 5,2% | 6,7% | 5,4% | 6,6% | 6,2% | **6,0%** |
| Commodity | n.d. | 4,6% | n.d. | n.d. | n.d. | *4,6%* |
| Oro | n.d. | 5,5% | 6,0% | n.d. | n.d. | *5,8%* |

**Cross-check**: ricomponendo il bottom-up sui pesi ACWI (US 63,6% / dev ex-US ~25,3% / EM ~11,1%) si ottiene **6,92%**, contro **6,67%** top-down. Convergenza a **0,25 pt** — è il tipo di conferma che rende utilizzabile il top-down.

**Contesto macro dell'episodio** (deperibile, lug-2026): investimenti fissi USA trainati quasi interamente dall'AI (+7,9% componenti AI vs −3,4% tutto il resto); prime 10 aziende ≈ 40% dell'indice **sia** negli USA **sia** negli emergenti (3 titoli semiconduttori = 70% del rendimento EM dell'anno); valutazioni nella parte alta del range ventennale quasi ovunque (USA fwd P/E ~21,4, ~90° percentile; economici solo EM, Cina, Corea); inflazione 2026 caso base sopra il 3% in US/EZ/UK con code avverse molto peggiori (Amundi); in regime inflattivo oro e commodity storicamente sopra, Treasury e corporate sotto; preferenza quasi unanime per scadenze brevi-intermedie.

---

## 9. Interfacce con il resto del canone

| Dove | Cosa cambia |
|---|---|
| **Principio 2** (asset allocation = 80-90%) | Il **premio atteso** `(μ − r_f)` che entra in Merton smette di essere un'assunzione arbitraria: si **calcola** top-down. |
| **Principio 5** (rendimento geometrico) | La stima `DY+g` è un **composto**; la media pesata di composti va corretta per vol drag e bonus di ribilanciamento (skill dedicata). |
| **Principio 12** (investire vs speculare) | Diventa **operativo**: solo gli income-generating asset sono stimabili → separa la quota coperta dal calcolo. |
| `P3-azionario.md` | "Valutazioni alte → calibra le aspettative" acquisisce il **numero**, non solo il monito. |
| `P4-obbligazionario.md` | "Lo YTM iniziale è uno spoiler potente" acquisisce il **coefficiente** (R² ≈ 89-90%). |
| `asset-allocation.md` §Choi/Merton | μ non si tira a indovinare: input top-down, dichiarato e datato. |
| `inflazione.md` | π è un input esplicito della conversione reale→nominale; in regime "3% is the new 2%" cambia il nominale, **non** il reale. |
| `analisi-macro.md` | La Fase 2 acquisisce un output **quantitativo** oltre alla narrativa, restando **anti-timing**. |
| skill `simulazione-montecarlo` | `exp_return` per asset **si calcola**, non si pesca dalla tabella di default. |

<!-- VERSIONE FILE -->
**Episodi:** TB-339 (+ rif. TB-222, TB-241, TB-288, TB-303, TB-306, TB-313, TB-318). **Stato:** completo.
**Time-sensitive:** tutto il §8 (DY, g AQR, π, YTW/duration, tabella CMA, contesto macro lug-2026) — rieseguire, non riusare. Anche i **numeri citati in §5** come illustrazione della dispersione fra case (S&P 500 a 10 anni: 8,5% BlackRock vs 6,1% Schwab/Capital Group, lug-2026) sono deperibili: il *fenomeno* — le case divergono di oltre 2 punti sulla stessa asset class — è timeless; i valori no.
**Lacune note:** (1) incoerenza 0,10 pt sulla riga MSCI USA della fonte (§8) — verificare; (2) divergenza slide vs parlato sui rendimenti reali — prevalgono le slide; (3) base valutaria e convenzione geometrica/aritmetica delle CMA non dichiarate nella fonte — verificare casa per casa prima di confrontarle col top-down.
