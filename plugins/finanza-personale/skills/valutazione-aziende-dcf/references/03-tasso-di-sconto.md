# 03 · Il tasso di sconto — la leva che muove tutto

Se si dovesse dedicare tempo a una sola ipotesi, sarebbe questa. Non perché sia la
più difficile, ma perché è quella a cui il risultato è più sensibile — e perché è
la più facile da scegliere per abitudine, prendendo il numero che si è usato
l'ultima volta.

---

## 1 · Che cos'è, davvero

Il **WACC** — *weighted average cost of capital*, costo medio ponderato del
capitale — viene spesso presentato come «il costo che l'azienda sostiene per
finanziarsi». È vero e fuorviante insieme, perché suggerisce che sia un fatto
aziendale da leggere in bilancio.

La lettura utile è l'altra, ed è speculare:

> **Il WACC è il rendimento che chi mette i soldi pretende per accettare il
> rischio di questa azienda.**

Costo per chi riceve, rendimento per chi dà: stesso numero, due punti di vista. La
seconda formulazione è quella giusta per valutare, perché rende esplicito che il
tasso **non descrive l'azienda**: descrive che cosa si pretende da lei. Due
persone che valutano la stessa azienda con lo stesso bilancio possono
legittimamente usare tassi diversi, ed è il motivo per cui il numero finale è
un'opinione argomentata e non una misura.

Nel motore, `wacc` è un **input in punti percentuali**, già costruito. Il motore
non lo calcola e non ha alcun modo di verificarlo: si limita a usarlo per scontare
i flussi e per il valore terminale. Costruirlo è il lavoro di questo file.

---

## 2 · Come si costruisce

Due componenti, pesate per quanto capitale arriva da ciascuna fonte.

```
WACC = quota di equity × costo dell'equity
     + quota di debito × costo del debito × (1 − aliquota fiscale)
```

Il costo del debito è moltiplicato per `(1 − aliquota)` perché gli interessi sono
deducibili: lo Stato ne paga una parte. Il costo dell'equity no, e questo da solo
spiega perché il debito «costa meno» — con l'avvertenza che ne aumenta il rischio,
e quindi alza il costo dell'equity.

### Il costo dell'equity

```
costo dell'equity = tasso privo di rischio
                  + beta × premio per il rischio azionario
                  + premio specifico
```

**Il tasso privo di rischio.** Il rendimento di un titolo di Stato considerato
privo di rischio di credito, con scadenza lunga — convenzionalmente dieci anni.

*Va preso nella valuta dei flussi.* Un'azienda americana che fattura in dollari si
sconta sul Treasury decennale, non sul Bund: scontare flussi in dollari con un
tasso in euro mescola due valute e due inflazioni attese, e l'errore non si vede
perché il risultato resta un numero plausibile.

**Lo dà lo strumento `risk_free` del connettore `finanza`, ed è BANCO.** Copre
entrambe le valute — il dollaro dal Tesoro USA, l'euro dalla curva AAA dell'area
euro della BCE — e la valuta è un **argomento della chiamata**, non una scelta
lasciata a chi legge. Ogni risposta porta valore, fonte, data dell'osservazione e
scostamento dalla data richiesta. *Fino all'agosto 2026 il connettore era
euro-centrico e questo file diceva che non bastava: non è più vero.*

**Una nota di convenzione.** Il CMT è quotato in composizione **semestrale**
(bond-equivalent), il tasso euro in composizione **annuale**. La conversione è
`(1 + t/2)² − 1` e su 4,70 vale **+5,5 punti base** (4,7552). Lo strumento la
dichiara in ogni risposta ma **non produce il numero convertito**, di proposito:
la conversione chiude uno solo dei due scarti — resta quello fra par yield e
zero-coupon, che dipende dalla forma dell'intera curva — e un numero convertito
farebbe sembrare confrontabili due grandezze che non lo sono.

### Il numero dello strumento e quello dei siti finanziari non coincidono

E non coincideranno mai. **È una proprietà della costruzione, non un errore**, e
va saputa prima di vedere i due numeri affiancati.

| | CMT del Tesoro (lo strumento) | decennale dei siti finanziari |
|---|---|---|
| che cos'è | un punto **interpolato a dieci anni esatti** sulla curva par | un **titolo vero**, con vita residua di ~9,9 anni |
| da dove viene | quotazioni indicative lato denaro sui titoli di ultima emissione, rilevate dalla Fed di New York | quotazione di mercato |
| quando | **chiusura delle 15:30 ET** | tempo reale |

Il Tesoro lo dichiara: le quotazioni CMT *possono non coincidere con il rendimento
esatto di nessun titolo specifico*, perché la curva fornisce un rendimento a dieci
anni esatti anche quando nessun titolo in circolazione ha esattamente dieci anni di
vita residua.

**Misurato l'11 agosto 2026: 3 punti base** — 4,70% dallo strumento contro 4,73%
letto a mano da un sito. Con verifica incrociata sulla **H.15 della Federal
Reserve**, che ripubblica gli stessi CMT: **venti valori confrontati** (10Y, 5Y, 2Y
e 30Y per il 4, 5, 6, 7 e 10 agosto), **tutti coincidenti al centesimo**. Il CMT
dello strumento è confermato da una seconda fonte; il 4,73 non compare in nessuno
dei due, e il massimo del mese era 4,72.

**Quanto pesano 3 punti base.** Con la regola del §3 — un punto di WACC vale circa
il 20% del valore — valgono circa lo **0,6%**. Non cambiano una conclusione, e
questo è precisamente il motivo per cui la discrepanza va spiegata invece che
inseguita: **senza questa riga, ogni volta che si guarda prima un sito e poi lo
strumento si pensa che uno dei due sia rotto.**

> Il difetto non era il 4,73. Era che **4,73 non portava con sé da dove veniva.**
> Chi usa il numero di un sito deve dichiarare la fonte e l'ora; chi usa lo
> strumento ha una fonte, una data e un metodo.

**Il premio per il rischio azionario** — *equity risk premium*, ERP. Quanto in più
del titolo di Stato si pretende per accettare il rischio di essere azionista
invece che creditore. Damodaran ne pubblica mensilmente una stima *implicita*,
ricavata dai prezzi correnti dell'indice e non dalle medie storiche: si prende il
valore **alla data della valutazione** e si scrive quella data nel report. Un ERP
di un anno fa non è una stima prudente, è una stima vecchia.

**Il beta.** Quanto il titolo si muove rispetto al mercato: 1 significa in linea,
1,5 più mosso, 0,7 meno. Si usa il beta di settore, non quello calcolato sul
singolo titolo, che è instabile e dipende dalla finestra scelta.

**Il premio specifico.** L'aggiunta per rischi che il beta non cattura:
concentrazione della clientela, dipendenza da poche persone, rischio paese,
governance. Va **nominato**, non messo a occhio. «Premio specifico +1,5 punti per
concentrazione dei ricavi sui primi tre clienti» è un'ipotesi; «+1,5 per
prudenza» è un modo di far tornare il numero.

---

## 3 · Perché è la leva che muove tutto

Qui i numeri, presi dalla matrice di sensibilità del caso di riferimento, con la
crescita perpetua tenuta ferma al 3% e **tutte le ipotesi operative identiche** —
stessa crescita, stessi margini, stesso reinvestimento.

| WACC | Fair value per azione | Variazione rispetto al 10% |
|---|---|---|
| 8% | 23,21 | +64% |
| 9% | 17,92 | +27% |
| **10%** | **14,14** | — |
| 11% | 11,33 | −20% |
| 12% | 9,15 | −35% |

Dall'8% al 12% il valore passa da 23,21 a 9,15: **meno 61%**, senza che nessuno
abbia cambiato una sola ipotesi sull'azienda. In quell'intorno, **ogni punto di
costo del capitale vale circa il 20% del valore**.

### Perché le aziende in crescita soffrono i rialzi dei tassi

Questa è l'osservazione più utile del file, e non ha niente a che vedere con il
sentiment di mercato: è **pura aritmetica**.

Il valore attuale di un flusso è `flusso ÷ (1 + wacc)^t`. L'esponente `t` è il
numero di anni. Più il flusso è lontano, più il denominatore cresce, più il
rialzo del tasso lo colpisce.

Confronto diretto, con un tasso che sale dall'8% al 12%:

| Quando arriva il flusso | Fattore all'8% | Fattore al 12% | Perdita di valore attuale |
|---|---|---|---|
| Fra 1 anno | 1,080 | 1,120 | −3,6% |
| Fra 5 anni | 1,469 | 1,762 | −16,6% |
| Fra 10 anni | 2,159 | 3,106 | −30,5% |
| Fra 20 anni | 4,661 | 9,646 | −51,7% |

Un'azienda matura ha i flussi vicini: perde poco. Un'azienda in forte crescita ha
i flussi lontani — anzi, nel caso di riferimento il flusso del primo anno è
addirittura **negativo**, e tutto il valore sta nel valore terminale e negli anni
finali. Perde molto.

Quando si legge che «i titoli growth soffrono i rialzi dei tassi», questa tabella
è il meccanismo. Non è una preferenza degli investitori: è dove sono collocati i
flussi nel tempo.

---

## 4 · Il tasso non è un punto: è un intervallo

Da qui discende la regola di forma di questo file.

> **Non si consegna mai un fair value calcolato su un solo WACC.**

Il motivo non è la prudenza generica. È che il costo dell'equity è costruito con
tre stime — ERP, beta, premio specifico — ognuna con la propria incertezza. Un
intervallo di più o meno un punto sul WACC non è pessimismo: è una descrizione
onesta di quanto si sa.

Il motore lo rende immediato:

```python
sensitivity(inputs, wacc_list, g_list)
```

Restituisce la matrice del fair value per azione: il **WACC sulle righe**, la
crescita perpetua sulle **colonne**. La matrice canonica del caso di riferimento
usa `[8, 9, 10, 11, 12]` e `[2, 2.5, 3, 4, 5]`.

Due cose che il motore fa e vanno sapute.

**Ogni cella è un DCF rifatto da capo**, non una correzione del caso centrale.
Cambiando il WACC cambiano anche i valori attuali dei cinque anni espliciti, non
solo il valore terminale. Una matrice costruita ritoccando solo la coda sarebbe
sbagliata di parecchio.

**Le celle in cui il WACC non supera la crescita perpetua valgono `None`.** Lì non
esiste un numero, e il motore lascia il buco invece di riempirlo. È lo stesso
principio dell'errore su `wacc ≤ g_terminal`: vedi `04-valore-terminale.md`.

### Come si legge la matrice

Non cella per cella. Si guardano tre cose.

1. **L'ampiezza.** Nel caso di riferimento si va da 8,48 a 35,86: un fattore
   quattro dentro ipotesi tutte difendibili. È questo il risultato, prima ancora
   del valore centrale.
2. **Dove cade il prezzo di mercato.** A 35,93, il prezzo sta **fuori** dalla
   matrice, sopra l'angolo più generoso. Significa che il prezzo richiede ipotesi
   più spinte di qualunque combinazione considerata plausibile — un'informazione
   molto più netta di «il fair value è 14,14».
3. **La pendenza.** Quanto rapidamente il valore cambia lungo le righe dice quanto
   la valutazione dipende dal tasso, e quindi quanta parte del lavoro andava
   speso lì.

---

## 5 · Il campo `risk_free` — che cosa fa e che cosa non fa

**Da non confondere con lo strumento omonimo del connettore** (§2): quello
*restituisce* il tasso, questo è un **campo di input del motore** in cui si scrive
il numero che quello ha restituito.

Nel motore esiste un campo `risk_free`, opzionale, in punti percentuali. **Non
entra nel calcolo del WACC**: il WACC arriva già costruito. Serve a una cosa sola.

Quando `g_terminal` supera `risk_free`, il motore emette l'allarme
`G_SOPRA_RISK_FREE`. La ragione sta in `04-valore-terminale.md`: un'azienda che
cresce per sempre più dell'economia in cui vive finisce per coincidere con
l'economia. Il tasso privo di rischio è il riferimento pratico che Damodaran
propone come tetto.

Il campo è opzionale, e la conseguenza è esplicita: **se non lo si valorizza,
l'allarme non può scattare**. Non scatta perché non c'è niente con cui
confrontare, non perché la crescita perpetua sia ragionevole. Vale la pena
compilarlo sempre — è lo stesso numero già usato per costruire il costo
dell'equity al §2.

---

## 6 · Gli errori ricorrenti

**Riusare il WACC della valutazione precedente.** È l'errore più comune e il più
silenzioso: il tasso privo di rischio si muove, l'ERP si muove, e il numero resta
lì. Se fra due valutazioni della stessa azienda il WACC non è cambiato, va
verificato che sia una scelta e non una dimenticanza.

**Usare il costo del debito che l'azienda paga oggi.** Serve il costo a cui si
finanzierebbe **adesso**, non la cedola media di obbligazioni emesse cinque anni
fa in un altro regime di tassi.

**Scontare flussi in una valuta con un tasso in un'altra.** Già visto al §2. Se
l'azienda fattura in più valute, il riferimento è la valuta prevalente, e la
scelta va dichiarata.

**Aggiungere un premio specifico per compensare ipotesi operative ottimiste.** È
un doppio conteggio mascherato da prudenza: si alza la crescita e poi si alza il
tasso per «bilanciare». Il risultato è un numero che sembra ragionevole e di cui
nessuna delle due componenti è difendibile da sola. Se la crescita è troppo alta,
si abbassa la crescita.

**Cercare il WACC che fa tornare il prezzo di mercato.** Con una differenza
importante: farlo *di nascosto* è la peggiore delle tarature all'indietro; farlo
**esplicitamente** è invece uno strumento legittimo e informativo — si chiama
reverse DCF, ha una funzione dedicata nel motore, `reverse_wacc`, e un file suo:
`05-reverse-dcf.md`. La differenza fra i due casi è tutta nel dichiararlo.

---

## 7 · Riepilogo

```
wacc ......... float, %, INPUT già costruito. Il motore non lo verifica.
risk_free .... float, %, opzionale. Serve SOLO all'allarme G_SOPRA_RISK_FREE.
```

Tre regole:

1. **La valuta del tasso privo di rischio è quella dei flussi.**
2. **Ogni componente del tasso ha una fonte e una data**, l'ERP in particolare.
3. **Mai un solo valore**: la matrice di sensibilità fa parte del risultato, non
   è un allegato.
