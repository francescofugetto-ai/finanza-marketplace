# 02 · Le ipotesi — crescita, margini, reinvestimento, ROIC

I dati del file precedente sono fatti: stanno in un documento, si verificano.
Quello che segue **non sono fatti**. Sono giudizi, e il valore di tutta la
valutazione dipende da quanto sono difendibili.

Da qui in avanti vale la frase del `00-dottrina-valutazione.md`: la domanda non è
*quanto vale*, è *con quali ipotesi*.

---

## 1 · Le cinque ipotesi, e quanto pesano

| Ipotesi | Campo del motore | Quanto muove il risultato |
|---|---|---|
| Crescita dei ricavi, anno per anno | `growth` | molto |
| Percorso del margine operativo | `ebit_margin` | molto |
| Efficienza del capitale | `sales_to_capital` | poco |
| Ritorno sul capitale a regime | `roic_terminal` | medio |
| Crescita perpetua e costo del capitale | `g_terminal`, `wacc` | moltissimo — vedi `03-tasso-di-sconto.md` e `04-valore-terminale.md` |

Due avvertenze subito, perché cambiano il modo di lavorare.

**Non tutte le ipotesi meritano lo stesso tempo.** Un'ora passata a rifinire
`sales_to_capital` di un decimo vale molto meno di dieci minuti passati a
chiedersi se il costo del capitale sia 9% o 11%. Il §4 lo mostra con i numeri.

**Le ipotesi non sono indipendenti.** Una crescita alta con margini in forte
espansione e capitale invariato descrive un'azienda che non esiste. Il §6 dà tre
controlli di coerenza.

---

## 2 · La crescita dei ricavi — `growth`

Cinque valori, uno per anno, in punti percentuali. `growth[0]` è la crescita del
primo anno rispetto a `revenue_base`. Nel caso di riferimento:
`[106, 30, 22, 16, 12]` — un'azienda che raddoppia i ricavi il primo anno per
un'acquisizione, e poi decelera.

Tre fonti, in ordine di affidabilità.

**Lo storico.** Il tasso composto degli ultimi tre e cinque anni. Non si proietta
tale e quale — è la fotografia del passato, non una previsione — ma dà l'ordine di
grandezza e, soprattutto, dice se la crescita è stata regolare o a scatti.

**La guidance dell'azienda.** Vale per il primo anno, al massimo il secondo. Oltre
è marketing. Va usata sapendo che chi la scrive ha un interesse a che sia
raggiungibile: è un numero **prudenzialmente ottimista**, formula che sembra un
ossimoro e descrive bene la cosa.

**La dimensione del mercato.** È il controllo di sanità mentale, e si fa in un
verso solo: si prende la crescita ipotizzata, si porta al quinto anno, e si guarda
che quota di mercato implicherebbe. Se il risultato è che l'azienda arriva al 40%
di un mercato in cui oggi ha il 3%, l'ipotesi non è aggressiva: è un'altra
azienda.

### La decelerazione non è pessimismo, è aritmetica

Una crescita che resta al 30% per cinque anni moltiplica i ricavi per 3,7. Al
sesto anno, nel valore terminale, quella stessa azienda dovrà crescere per sempre
al 3%. Il salto fra il quinto e il sesto anno è violento, e non ha nessuna
giustificazione economica: è solo il punto in cui finisce il foglio di calcolo.

Il percorso di `growth` deve quindi **atterrare** verso `g_terminal`, non
schiantarcisi. Nel caso di riferimento si scende da 106 a 12, e il valore
terminale parte da 3: la discontinuità c'è ancora, ma è ragionevole.

**Errore da non fare:** mettere cinque valori uguali. Un'azienda che cresce
esattamente al 18% per cinque anni non esiste, e quel profilo piatto è quasi
sempre il segno che nessuno ha pensato agli anni intermedi.

---

## 3 · Il percorso dei margini — `ebit_margin`

Cinque valori, il margine operativo di ciascun anno, in punti percentuali. È il
rapporto fra EBIT e ricavi, e nel motore diventa `ebit[t] = revenue[t] ×
ebit_margin[t]`.

Il punto di partenza è il margine **reported** dell'ultimo esercizio, calcolato al
§4 del file precedente. Da lì si costruisce un percorso, e la domanda a cui il
percorso risponde è: *che cosa fa salire o scendere il margine, e quando smette di
farlo?*

Le tre leve legittime:

- **Scala.** I costi fissi si spalmano su ricavi maggiori. È la leva più
  credibile, ed è anche quella che si esaurisce.
- **Mix.** Prodotti a margine più alto pesano di più. Va sostenuta con un dato,
  non con un'intenzione.
- **Efficienza operativa.** È la più abusata: «miglioreremo l'efficienza» senza un
  meccanismo è un modo di scrivere «vorrei un margine più alto».

Nel caso di riferimento il percorso è `[22, 26, 29, 31, 33]`: sale di 11 punti in
cinque anni, con incrementi decrescenti — 4, 3, 2, 2. Il profilo che decelera è
quasi sempre più difendibile di uno lineare, perché i primi punti di margine sono
i più facili.

### Il tetto va dichiarato

Prima di scrivere il quinto valore, va risposta una domanda: **qual è il margine
massimo plausibile per questo settore, e perché questa azienda dovrebbe
raggiungerlo?** Se il margine finale supera quello del concorrente più redditizio
del settore, serve una spiegazione esplicita nel report. Non è vietato: è vietato
farlo senza dirlo.

---

## 4 · L'efficienza del capitale — `sales_to_capital`

Un solo numero, un rapporto puro, **non** una percentuale. Dice quanti ricavi
incrementali l'azienda ottiene per ogni unità di capitale investito. Nel caso di
riferimento vale `3`: ogni euro investito produce tre euro di ricavi in più.

Il motore lo usa così:

```
reinvestment[t] = (revenue[t] − revenue[t−1]) ÷ sales_to_capital
fcff[t]         = nopat[t] − reinvestment[t]
```

È il meccanismo che impedisce alla crescita di essere gratis. Nel primo anno del
caso di riferimento produce un risultato che vale la pena guardare:

| | 2026 |
|---|---|
| Ricavi | 2.698,6 |
| NOPAT | 433,4 |
| Reinvestimento | **462,9** |
| **FCFF** | **−29,5** |

Il flusso del primo anno è **negativo**. L'azienda guadagna 433 e ne deve
investire 463 per sostenere il raddoppio dei ricavi. Non è un errore del modello:
è la descrizione corretta di che cosa costa crescere del 106%. Un modello che
producesse un flusso positivo lì avrebbe dimenticato il capitale.

### Come si stima

Si guarda la storia: variazione dei ricavi divisa per l'investimento netto in
capitale — capex meno ammortamenti, più la variazione del capitale circolante —
su tre o cinque anni. Il valore medio è il punto di partenza; la dispersione fra
gli anni dice quanto fidarsi della media.

Riferimenti di ordine di grandezza, da usare come controllo e mai come default:
il software gira su valori alti, l'industria pesante su valori bassi, la
distribuzione nel mezzo. Un valore fuori scala rispetto al settore va motivato.

### Quanto pesa davvero

Poco, ed è utile saperlo per non spenderci tempo. Rifacendo il caso di riferimento
con `sales_to_capital = 2` invece di 3 — cioè peggiorando di un terzo l'efficienza
del capitale, che è un'ipotesi molto diversa:

| | `sales_to_capital = 3` | `sales_to_capital = 2` |
|---|---|---|
| PV dei flussi espliciti | 2.107,8 | 1.549,7 |
| Valore terminale attualizzato | 10.402,8 | 10.402,8 |
| **Fair value per azione** | **14,14** | **13,26** |

Meno 6%. Il motivo è che il reinvestimento agisce **solo sui cinque anni
espliciti**: il valore terminale, che pesa oltre l'80% del totale, ha un suo
meccanismo di reinvestimento indipendente, derivato da `g_terminal` e
`roic_terminal` — è il tema di `04-valore-terminale.md`.

**Morale operativa:** `sales_to_capital` va stimato con onestà e senza ansia. Il
tempo va speso sul costo del capitale.

---

## 5 · Il ritorno sul capitale a regime — `roic_terminal`

**ROIC** sta per *return on invested capital*: quanto rende il capitale
complessivamente investito nell'azienda, calcolato come NOPAT diviso capitale
investito. Nel motore è un solo numero, in punti percentuali, e serve **soltanto**
al valore terminale.

Nel caso di riferimento vale `20`, e produce il fattore `1 − g/ROIC = 1 − 3/20 =
0,85`: nel mondo a regime, l'85% del NOPAT è libero e il 15% torna dentro
l'azienda per sostenere la crescita perpetua del 3%.

Tre criteri per sceglierlo.

**Il ROIC storico dell'azienda**, se ha una storia lunga e stabile. È il punto di
partenza.

**Il costo del capitale come pavimento concettuale.** Un ROIC a regime *inferiore*
al `wacc` descrive un'azienda che distrugge valore crescendo: è possibile, ed è
un'affermazione forte che va scritta nel report, non lasciata implicita in un
campo.

**La convergenza competitiva.** Un ROIC molto alto attira concorrenti. Su un
orizzonte perpetuo, mantenere il 40% richiede una barriera che va nominata: un
brevetto, un effetto rete, un marchio. Se non si sa nominarla, il valore va
abbassato.

---

## 6 · Tre controlli di coerenza fra le ipotesi

Vanno fatti prima di lanciare il calcolo, perché il motore non li può fare al
posto di chi scrive: sono giudizi, non violazioni di regole.

**Primo — crescita alta e margini in salita insieme.** È possibile, ma è la
combinazione più ottimista che esista: significa vendere molto di più e guadagnare
di più su ogni unità venduta. Se ci sono entrambe, il report deve dire perché.

**Secondo — crescita alta e capitale invariato.** Se `growth` sale ma
`sales_to_capital` resta al valore storico, si sta assumendo che l'azienda cresca
con la stessa efficienza di sempre pur andando più veloce. Va verificato contro il
capex: è esattamente la trappola 2 di `01-estrazione-dati.md`.

**Terzo — il quinto anno contro il valore terminale.** Il margine e la crescita
del quinto anno sono il punto da cui parte il mondo a regime. Se al quinto anno il
margine è 33% e in perpetuo si assume implicitamente lo stesso, va bene; se il
quinto anno è un picco, il valore terminale sta capitalizzando un picco per
sempre.

---

## 7 · La regola sui compensi in azioni

È la regola su cui si sbaglia più spesso, e vale la pena scriverla per intero.

> **Si parte sempre dall'EBIT reported. Mai da EBITDA. Mai da metriche
> *adjusted*. La SBC non si ri-aggiunge mai. Si usano le azioni diluite.**

**Il malinteso.** Molti modelli «correggono» il flusso ri-aggiungendo i compensi
in azioni, perché non sono un'uscita di cassa. Il ragionamento sembra solido ed è
sbagliato: i compensi in azioni **sono un costo reale per l'azionista esistente**,
che paga in diluizione invece che in contanti. Ri-aggiungerli significa fingere
che il lavoro dei dipendenti sia gratis.

**Dove si apre davvero il buco.** Non partendo dall'EBIT — lì la SBC è già dentro,
distribuita fra costo del venduto, ricerca e sviluppo e costi commerciali. Il buco
si apre partendo da:

- **EBITDA**, che esclude gli ammortamenti e spesso viene presentato già al lordo
  della SBC;
- **il flusso di cassa operativo**, dove la SBC è ri-aggiunta per costruzione,
  essendo un costo non monetario;
- **le metriche *adjusted* non-GAAP**, che escludono la SBC quasi sempre — ed è il
  motivo principale per cui esistono.

**Il campo `sbc`** serve solo all'allarme `SBC_ELEVATA`, che scatta oltre il 5% dei
ricavi. Taratura verificata: Alphabet **6.751 su 109.896 = 6,1%** → scatta;
Coca-Cola intorno all'1% → non scatta. L'allarme non corregge niente: dice che la
diluizione è rilevante e che il conto di `diluted_shares` va guardato due volte.

---

## 8 · La motivazione in una riga

Ogni ipotesi va accompagnata da **una riga** che la rende difendibile. Non un
paragrafo: una riga. Il vincolo di lunghezza non è estetico — se non ci sta in una
riga, di solito è perché non c'è.

Una motivazione difendibile ha tre pezzi: **il numero, la fonte, il meccanismo.**

| | Esempio |
|---|---|
| **Difendibile** | «Crescita 2027 al 30%: guidance aziendale 28-32%, coerente con il portafoglio ordini già acquisito.» |
| **Difendibile** | «Margine a regime 33%: pari al concorrente più redditizio del settore, raggiunto per effetto scala sui costi fissi già sostenuti.» |
| **Non difendibile** | «Crescita 2027 al 30%: il settore è in forte espansione.» — nessun numero, nessuna fonte, nessun meccanismo. |
| **Non difendibile** | «Margine a regime 33%: prudenziale.» — prudenziale rispetto a che cosa? |

Il test finale è **la prova del contrario**: se la stessa riga, con il numero
cambiato, suonasse ugualmente convincente, allora non è una motivazione. «Crescita
al 30% perché il settore è in espansione» funziona identica al 20% e al 40%, e
quindi non dice niente.

Queste righe non sono decorazione del report. Sono ciò che rende possibile la
regola di manutenzione: **prima di rifare una valutazione si riapre la
precedente e si scrive che cosa è cambiato nelle ipotesi.** Fra due anni la cosa
di valore non sarà il fair value — sarà vedere che a gennaio si assumeva +15% e a
dicembre +8%, e doversi spiegare perché.

---

## 9 · Riepilogo dei campi

```
growth ............. [5 float, %]   percorso decrescente che atterra verso g_terminal
ebit_margin ........ [5 float, %]   percorso con incrementi decrescenti, tetto dichiarato
tax_rate ........... float, %       EFFETTIVA, dalle note
sales_to_capital ... float, puro    dallo storico; pesa poco, non spenderci ore
roic_terminal ...... float, %       solo per il valore terminale; barriera nominabile
sbc ................ float, opz.    solo per l'allarme oltre il 5% dei ricavi
```

Le liste `growth` e `ebit_margin` devono avere **esattamente cinque elementi**. Se
ne hanno un numero diverso il motore solleva un errore invece di completare o
tagliare: un orizzonte incompleto è un'ipotesi mancante, e le ipotesi mancanti non
si indovinano.

Le due ipotesi che restano — `wacc` e `g_terminal` — sono in
`03-tasso-di-sconto.md` e `04-valore-terminale.md`. Sono quelle che muovono di
più, ed è per questo che hanno un file ciascuna.
