# 00 · Dottrina della valutazione — prezzo, valore e la domanda giusta

**Entry point della skill.** Prima di aprire un bilancio, prima di scegliere un
tasso di sconto, si legge questo file. Contiene il perché; gli altri contengono
il come.

---

## 1 · Le due cose che non sono la stessa cosa

Il **prezzo** è quanto qualcuno ha pagato l'ultima volta. È un fatto: sta sul
book del broker, ha un orario, non si discute.

Il **valore** è quanto vale l'azienda date certe ipotesi su quanta cassa
produrrà, per quanto tempo, e con quanta incertezza. Non è un fatto: è il
risultato di un ragionamento, e cambia se cambia il ragionamento.

Confonderli produce due errori speculari, entrambi molto comuni.

| Errore | Come suona | Perché è un errore |
|---|---|---|
| Il prezzo *è* il valore | «il mercato sconta già tutto, non c'è niente da capire» | rende impossibile domandarsi *che cosa* stia scontando, che è l'unica domanda utile |
| Il valore *è* un fatto | «questa azienda vale 14,14 dollari» | nasconde che quel numero è la conseguenza di sei o sette ipotesi, ognuna discutibile |

La posizione di questa skill è la terza: **il valore è una funzione delle
ipotesi, e il lavoro consiste nel rendere quelle ipotesi visibili**, non nel
produrre un numero.

> **La frase da tenere a mente.**
> La domanda giusta non è *«quanto vale»*. È ***«con quali ipotesi»***.

---

## 2 · I tre ingredienti, e nient'altro

Qualunque valutazione di un'attività che produce reddito — un'azienda, un
immobile in affitto, un titolo di Stato — poggia su tre sole cose.

1. **Quanta cassa produce.** Non quanto fattura, non quanto dichiara di
   guadagnare: quanta cassa resta libera dopo aver pagato tutto ciò che serve a
   tenere in piedi e a far crescere l'attività.
2. **Per quanto tempo, e crescendo di quanto.** Una cassa che cresce del 3%
   l'anno per sempre vale molto più della stessa cassa ferma.
3. **Con quanta incertezza.** Più il flusso è incerto, più chi lo compra pretende
   un rendimento alto per accettarlo — e quindi meno paga oggi per averlo.

Il **DCF** — *discounted cash flow*, flussi di cassa scontati — è semplicemente
il modo di mettere insieme questi tre ingredienti in un numero. «Scontare»
significa riportare a oggi una somma futura: mille euro fra cinque anni valgono
meno di mille euro adesso, e quanto meno dipende dal terzo ingrediente.

### Il bar di Mario

Mario ha un bar. Vuole venderlo e chiede quanto vale.

Non si guarda quanto ha pagato l'arredamento, e nemmeno quanto ha incassato in
totale. Si guarda **quanto resta in tasca a Mario a fine anno**, dopo aver pagato
il caffè, l'affitto, il barista e le tasse: mettiamo 40.000 euro.

Poi tre domande, nell'ordine.

- *Quella cifra crescerà?* Se in strada apriranno uffici nuovi, forse. Se sta per
  aprire un bar dall'altra parte della piazza, forse no.
- *Per quanto tempo?* Il contratto d'affitto scade fra sei anni ed è rinnovabile,
  ma non è garantito.
- *Quanto è sicura?* Un bar dipende da una via, da un affitto, da una persona.
  Non è un titolo di Stato.

Se pretendo il 12% l'anno per accettare questo rischio, e i 40.000 euro restano
stabili, il bar vale grosso modo `40.000 ÷ 0,12 ≈ 333.000` euro. Se pretendessi
l'8%, varrebbe `40.000 ÷ 0,08 = 500.000`. **Stessa cassa, stesso bar, mezzo
milione contro trecentotrentamila**: la differenza è tutta nel terzo ingrediente.

Un'azienda quotata è il bar di Mario con tre complicazioni — più righe di
bilancio, più anni da stimare, e un prezzo che si forma ogni giorno in pubblico.
La struttura del ragionamento è identica.

---

## 3 · Perché la cassa e non l'utile

L'**utile netto** è il numero in fondo al conto economico. Sembra la risposta
ovvia alla domanda «quanto guadagna», e non lo è, per tre ragioni.

**Primo: l'utile contiene cose che non sono cassa.** Gli ammortamenti sono un
costo che non esce dal conto corrente. Le rivalutazioni di partecipazioni sono un
guadagno che non entra. Su Alphabet, nel primo trimestre 2026, la voce *Other
Income & Expense* conteneva **36,9 miliardi di plusvalenze non realizzate** su
partecipazioni: soldi che nessuno ha incassato, che hanno gonfiato l'utile e che
non hanno niente a che vedere con la capacità del motore di produrre cassa.

**Secondo: l'utile non vede il capitale che serve a crescere.** Un'azienda che
cresce del 30% deve comprare server, assumere, finanziare crediti verso clienti.
Quei soldi escono davvero, ma non passano dal conto economico come costo: passano
dallo stato patrimoniale. Un modello che si ferma all'utile fa apparire la
crescita gratis, e la crescita non è mai gratis.

**Terzo: l'utile è più facile da modellare.** Non è un difetto tecnico, è un
difetto di incentivi: l'utile è il numero su cui si misurano i bonus.

Questa skill parte quindi dall'**EBIT** — *earnings before interest and taxes*,
il risultato operativo prima degli interessi e delle imposte — e da lì costruisce
il flusso disponibile per tutti i finanziatori dell'azienda:

```
EBIT
  × (1 − aliquota fiscale)        = NOPAT, l'utile operativo netto d'imposta
  − reinvestimento                = il capitale che la crescita richiede
  = FCFF                          il flusso di cassa disponibile per l'impresa
```

**FCFF** sta per *free cash flow to the firm*: la cassa che resta a disposizione
di **tutti** quelli che hanno messo soldi nell'azienda — azionisti e creditori
insieme. È la scelta che rende il modello indipendente da quanto debito ha
l'azienda: la struttura finanziaria entra dopo, nel ponte verso l'equity, e non
si mescola con la valutazione dell'attività operativa.

Nel motore questi tre passaggi si chiamano `ebit`, `nopat`, `reinvestment` e
`fcff`, e sono i campi di ogni riga della tabella annuale.

---

## 4 · Che cosa fa il motore, e che cosa fa chi lo usa

La divisione del lavoro è netta, ed è la ragione per cui il motore esiste.

| | Chi decide | Che cosa |
|---|---|---|
| **Le ipotesi** | tu, con Claude | crescita, margini, aliquota, tasso di sconto, crescita perpetua, ROIC a regime |
| **L'aritmetica** | `scripts/dcf_engine.py` | moltiplicazioni, attualizzazioni, valore terminale, ponte, sensibilità |

Un modello linguistico che moltiplica margini e attualizza flussi su cinque anni
sbaglia, e **sbaglia in silenzio**: il numero che produce ha la virgola al posto
giusto e nessun campanello suona. Il motore toglie di mezzo quella classe di
errori per intero. Non toglie di mezzo l'altra — le ipotesi sbagliate — e non
pretende di farlo: quelle restano un giudizio, e il resto di questa cartella
serve a renderlo difendibile.

Il motore, coerentemente, si rifiuta di rispondere dove non esiste una risposta
corretta. Se il costo del capitale non supera la crescita perpetua solleva un
errore invece di restituire un numero; se un risolutore inverso non trova
soluzione dentro i limiti di plausibilità restituisce `None` con la ragione
scritta a parole. **Un buco dichiarato vale più di un numero plausibile.**

---

## 5 · Che cosa non si valuta mai così

Il DCF non è universale. Applicarlo dove non regge non produce un numero
impreciso: produce un numero privo di significato, che però *sembra* preciso.
Sono cinque casi, e vanno riconosciuti prima di cominciare, non dopo.

**Le banche e le assicurazioni.** Per una banca il debito non è un modo di
finanziarsi: è la materia prima. La distinzione fra capitale operativo e
finanziario, su cui tutto il modello poggia, semplicemente non esiste. Si
valutano con metodi propri, basati sul patrimonio e non sul flusso operativo.

**Le aziende senza ricavi.** Una biotech prima dell'approvazione di un farmaco
non ha una serie storica da cui partire: ogni numero del modello sarebbe
un'assunzione su un'assunzione. Il DCF diventa un modo elaborato di scrivere
un'opinione.

**Le aziende in dissesto.** Se la sopravvivenza a due anni è in dubbio, il valore
non dipende dal flusso di cassa a regime ma dall'esito di una ristrutturazione.
Il metodo giusto è un altro: probabilità di scenari, non attualizzazione.

**Le società cicliche al picco o al fondo del ciclo.** Prendere il margine
dell'ultimo esercizio e proiettarlo cinque anni avanti significa proiettare il
punto del ciclo in cui ci si trova. Serve una normalizzazione sul ciclo intero,
ed è un lavoro diverso.

**Le holding che valgono per quello che possiedono.** Se il valore sta nelle
partecipazioni e non nell'attività operativa, si sommano le parti — non si
sconta un flusso che non è il motore del valore.

C'è poi un sesto caso, che non è un'esclusione ma un avvertimento: **le aziende
molto giovani e in crescita fortissima**. Il DCF si può fare, ma il valore
terminale finirà per pesare quasi tutto, e allora il modello non sta dicendo
molto sui cinque anni espliciti: sta dicendo quello che si crede dell'azienda fra
sei anni e oltre. È legittimo, purché sia dichiarato. Il motore emette in questi
casi l'allarme `TV_DOMINANTE`.

---

## 6 · L'incertezza è il risultato, non il disturbo

L'episodio 337 di The Bull ha valutato la stessa azienda tre volte, con ipotesi
tutte difendibili, e ha ottenuto **3,93 · 14,14 · 36,27 dollari per azione**. Fra
il minimo e il massimo c'è un fattore nove.

La lettura sbagliata è: «allora il metodo non serve a niente».

La lettura giusta è: **quel fattore nove è il risultato**. Dice che il prezzo di
quel titolo non è governato da ciò che l'azienda ha fatto, ma da ciò che si crede
farà — e misura quanto poco basta, in termini di ipotesi, per spostare il valore
da un terzo del prezzo al doppio. Un investitore che lo sa è in una posizione
diversa da uno che ha in mano solo il prezzo.

Da qui discendono tre regole di forma, che valgono per tutta la skill.

1. **Un fair value non si consegna mai da solo.** Va sempre accompagnato dalle
   ipotesi che lo generano e dalla matrice di sensibilità, che mostra quanto si
   muove al variare del costo del capitale e della crescita perpetua.
2. **La matrice non è un abbellimento.** Sul caso di riferimento, cambiare il
   costo del capitale dall'8% al 12% porta il fair value da **23,21 a 9,15**: meno
   60%, a ipotesi operative identiche. È il fatto più informativo dell'intero
   esercizio.
3. **Il numero singolo, isolato, viene letto come un obiettivo di prezzo** —
   qualunque avvertenza lo accompagni. Per questo nel registro condiviso il fair
   value compare solo come intervallo con gli scenari affiancati.

---

## 7 · Il confine — che cosa questo lavoro non decide

Questa è la regola più importante del file, e non è una regola tecnica.

> **Il lavoro di valutazione può cambiare quanto ti aspetti e quanto rischio sai
> di correre. Non può cambiare i pesi.**

Il motivo sta nella dottrina generale, in `metodo-fiduciario/SKILL.md`:
l'anti-timing è fra le regole non negoziabili. Spostare peso da uno strumento a
un altro perché un DCF dice che certe aziende sono care **è market timing basato
sulle valutazioni**, con tre aggravanti:

- l'incertezza di misura vista al §6 non regge una decisione sui pesi;
- l'errore non si annulla sommando aziende diverse, perché le ipotesi che lo
  generano sono correlate fra loro (il costo del capitale è lo stesso per tutte);
- il segnale «i grandi titoli americani sono cari» suona da oltre un decennio, e
  chi lo ha seguito ha pagato quel giudizio ogni singolo anno.

Che cosa **può** legittimamente fare l'output di questo lavoro:

| Sì | No |
|---|---|
| rivedere il rendimento atteso di un blocco, con motivazione tracciata | cambiare un peso di portafoglio |
| fissare un vincolo di consapevolezza sul drawdown atteso, con data | generare un trigger automatico di ribilanciamento |
| fissare un tetto di concentrazione deciso *ex ante* | entrare in una sessione di allocazione, PAC o profilazione |

**Zona grigia, dichiarata come tale**: dirigere i nuovi flussi del piano di
accumulo sulla base di una valutazione è una forma morbida della stessa
scommessa. Più difendibile del vendere, ma è timing. Se la si vuole ammettere, va
scritta prima come regola con soglia numerica e data — mai decisa caso per caso
guardando l'ultimo report.

---

## 8 · Il resto della cartella

| File | Risponde a |
|---|---|
| `01-estrazione-dati.md` | dove stanno i numeri, e quali trappole contengono |
| `02-ipotesi.md` | come si costruiscono crescita, margini, reinvestimento e ROIC |
| `03-tasso-di-sconto.md` | come si costruisce il costo del capitale, e perché muove tutto |
| `04-valore-terminale.md` | come si tratta il pezzo che pesa più di tutti gli altri |
| `05-reverse-dcf.md` | come si legge che cosa il prezzo sta già scontando |
| `06-verdetto-e-linguaggio.md` | come si scrive il risultato, e che cosa non si scrive mai |
| `07-ponte-etf.md` | come questo lavoro entra — e non entra — nel portafoglio |

L'ordine di lettura è quello di scrittura. Chi salta il `02` e arriva al `03` si
trova a scegliere un tasso di sconto senza sapere che cosa sta scontando.
