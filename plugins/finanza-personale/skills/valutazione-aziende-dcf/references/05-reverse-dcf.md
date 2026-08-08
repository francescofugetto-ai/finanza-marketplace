# 05 · Il reverse DCF — che cosa il prezzo sta già scontando

I quattro file precedenti costruiscono un valore partendo dalle ipotesi. Questo
file rovescia la freccia: prende il **prezzo di mercato come dato** e chiede quali
ipotesi lo renderebbero corretto.

È lo stesso modello, letto al contrario. Ed è quasi sempre la domanda più utile
delle due.

---

## 1 · Perché è più informativo del fair value

Il fair value ha un difetto strutturale: **è il risultato delle ipotesi di chi lo
calcola.** Chi lo riceve deve fidarsi di sei o sette giudizi che non ha fatto, e
di fronte a un numero che dista il 60% dal prezzo la reazione onesta è
«evidentemente ho ipotesi diverse dalle sue» — che è vera, e che chiude la
conversazione.

Il reverse DCF non ha quel difetto, perché **non chiede di credere a niente.**
Dice: *ecco che cosa devi credere per giustificare il prezzo che vedi.* Il
risultato non è un giudizio, è una traduzione — e resta valido anche per chi non
condivide nessuna delle ipotesi di partenza.

Il confronto sul caso di riferimento, con il prezzo a **35,93** e il fair value
base a **14,14**:

| Formulazione | Che cosa comunica |
|---|---|
| «vale 14,14, il prezzo è 35,93» | che chi ha fatto il conto e il mercato non sono d'accordo |
| «a 35,93 il prezzo sconta ricavi che si moltiplicano per **dieci** in cinque anni» | un'affermazione verificabile sul mondo, non sul modello |

La seconda frase si può contestare guardando l'azienda, il mercato e i
concorrenti. La prima si può contestare solo guardando il foglio di calcolo.
**È la differenza fra una tesi e un'opinione.**

C'è poi una seconda ragione, più pratica: il reverse DCF è ciò che regge il
riesame leggero della manutenzione. A ipotesi invariate, con il solo prezzo
aggiornato, dieci minuti bastano a rispondere a *«che cosa sta scontando oggi il
mercato, rispetto a tre mesi fa?»*. Vedi `references/08-manutenzione-e-batch.md`.

---

## 2 · Le quattro domande, e le quattro funzioni

Il motore risolve una variabile alla volta, tenendo **tutte le altre ferme**, e
cercando il valore che porta il fair value esattamente sul prezzo di mercato.

| Funzione | Risolve | La domanda in italiano |
|---|---|---|
| `reverse_growth` | crescita dei ricavi, **uniforme** sui cinque anni | quanto deve crescere il fatturato |
| `reverse_margin` | margine EBIT del quinto anno | quanto deve diventare redditizia |
| `reverse_g_terminal` | crescita perpetua | quanto deve durare il vantaggio |
| `reverse_wacc` | costo del capitale | che rendimento sta chiedendo chi compra oggi |

Tutte restituiscono una struttura `ReverseResult` con due campi soli: `value`, in
punti percentuali, e `motivo`, una riga di testo. Quando `value` è `None` il
`motivo` dice perché, ed è quello che va nel report — **mai un numero al suo
posto**.

### Perché la crescita risolta è uniforme

`reverse_growth` non scala il percorso `[106, 30, 22, 16, 12]` di un fattore: lo
sostituisce con **cinque valori uguali**. La ragione è d'uso, non di matematica.
Il numero serve a essere detto a voce — *«il prezzo sconta il 58% l'anno per
cinque anni»* — e un percorso non uniforme non si riassume in una cifra sola.
Chi vuole ragionare sul percorso ha già la tabella per anno del calcolo diretto.

---

## 3 · L'ordine in cui si risolvono

L'ordine non è indifferente: le quattro risposte non hanno la stessa leggibilità
e non reggono lo stesso peso in una discussione.

**Primo, `reverse_growth`.** È la variabile che chiunque sa giudicare. «Questa
azienda deve crescere del 58% l'anno per cinque anni» si valuta guardando il
fatturato dei concorrenti, la dimensione del mercato, la storia dell'azienda
stessa. Non serve sapere che cos'è un WACC.

**Secondo, `reverse_margin`.** Stessa qualità, un gradino più tecnica. Si giudica
contro il margine del concorrente più redditizio del settore, che è un dato
pubblico.

**Terzo, `reverse_g_terminal`.** Utile ma insidiosa: la crescita perpetua è un
numero piccolo e sembra innocuo, mentre è quello che decide l'83% del valore.
Va sempre accompagnata dal confronto con il tasso privo di rischio — vedi
`references/04-valore-terminale.md`.

**Quarto, `reverse_wacc`.** È la più tecnica e la meno adatta a essere detta a
voce, ma è la più onesta di tutte, perché non parla dell'azienda: parla di chi
compra. Un WACC implicito basso significa che il mercato sta chiedendo poco
rendimento per accettare quel rischio.

**Regola di forma:** nel report condiviso si porta **la prima**, al massimo le
prime due. Le altre due restano nel registro interno. Non per semplificare — per
non consegnare quattro numeri che sembrano quattro conferme indipendenti quando
sono quattro letture della stessa distanza.

---

## 4 · Il caso di riferimento, per intero

Ipotesi identiche a quelle del calcolo diretto. Prezzo di mercato **35,93**, fair
value base **14,14**, quindi un prezzo che sta **2,5 volte** sopra.

| Variabile | Ipotesi del modello | Valore che giustifica 35,93 |
|---|---|---|
| Crescita ricavi | `[106, 30, 22, 16, 12]` | **57,97% l'anno**, per cinque anni |
| Margine EBIT al quinto anno | 33% | **nessuna soluzione** sotto il 60% |
| Crescita perpetua | 3% | **7,72%** |
| Costo del capitale | 10% | **6,58%** |

Le quattro righe lette come si devono leggere:

**La crescita.** Il 57,97% composto porta i ricavi da 1.310 a **12.886** milioni
in cinque anni: quasi **dieci volte**, contro le 4,2 volte del modello base. Non
è un'ipotesi aggressiva, è un'azienda diversa.

**Il margine.** Il risolutore restituisce `None`, e il motivo dice: *nessuna
soluzione fra 0 e 60. Su tutto l'intervallo plausibile il fair value resta sotto
il prezzo di mercato.* Verificato: portando il margine del quinto anno al **60%**
— un livello che quasi nessuna azienda al mondo sostiene — il fair value arriva a
**30,13**, ancora sotto il prezzo. **La redditività, da sola, non basta a
giustificare quel prezzo qualunque valore le si dia.** È il risultato più forte
dei quattro, e si ottiene solo perché il motore si rifiuta di allargare i limiti.

**La crescita perpetua.** Il 7,72% supera qualunque tasso privo di rischio in
dollari. Un'azienda che cresce del 7,72% per sempre supera in fretta l'economia
in cui vive: l'ipotesi non è ottimista, è impossibile.

**Il costo del capitale.** Il 6,58% è il rendimento che chi compra a 35,93 sta
implicitamente accettando per il rischio di questa azienda — meno di quanto si
pretenderebbe da un indice azionario largo.

### Lo stesso esercizio con il prezzo sotto il fair value

Per mostrare che il metodo non è costruito per dire sempre «caro». Stesse
ipotesi, prezzo ipotetico **12,00** invece di 35,93:

| Variabile | Valore che giustifica 12,00 |
|---|---|
| Crescita ricavi | 31,47% l'anno |
| Margine EBIT al quinto anno | 29,62% |
| Crescita perpetua | 1,30% |
| Costo del capitale | 10,74% |

Quattro numeri tutti modesti rispetto alle ipotesi del modello, e tutti dentro
l'intervallo del già visto. La lettura è simmetrica e altrettanto netta: a quel
prezzo il mercato non sta chiedendo niente di straordinario all'azienda.

---

## 5 · Dal numero alla frase

La frase del reverse DCF è **il titolo del report condiviso** (`06` §3). Ha una
forma fissa, e la forma serve a impedire che diventi una raccomandazione.

```
A <prezzo>, alla data <data>, il prezzo sta scontando <ipotesi in parole>.
```

Tre vincoli, tutti e tre necessari.

**Il prezzo compare, con la data.** Senza prezzo la frase diventa una previsione;
senza data diventa vera per sempre, che è peggio.

**Il verbo è «sta scontando».** Non «richiede», non «implica che dovrà»: quelli
sono verbi che spostano l'affermazione dal mercato all'azienda. Il reverse DCF
descrive il prezzo, non l'azienda.

**Nessuna conclusione attaccata in coda.** *«…sta scontando il 58% l'anno per
cinque anni, che pare improbabile»* non è più una traduzione: è un giudizio, e ha
già cambiato registro. L'improbabilità la valuta chi legge, con i termini di
paragone che il report gli mette a disposizione al paragrafo successivo.

Tre esempi, dal caso di riferimento.

| | Frase |
|---|---|
| **Corretta** | «A 35,93 dollari, al 7 agosto 2026, il prezzo sta scontando ricavi in crescita del 58% l'anno per cinque anni — quasi dieci volte il fatturato attuale.» |
| **Corretta** | «A 35,93 dollari, al 7 agosto 2026, nessun livello di redditività entro il 60% di margine operativo giustifica il prezzo: la scommessa è tutta sui volumi, non sui margini.» |
| **Sbagliata** | «Il titolo sconta ipotesi eroiche e ha un downside del 61%.» — *downside* è un target price travestito, *eroiche* è un giudizio nel titolo, e manca il prezzo con la data. |

L'elenco completo delle formule vietate è in
`references/06-verdetto-e-linguaggio.md`.

---

## 6 · I quattro limiti, e perché non si allargano

I risolutori cercano dentro limiti dichiarati, e fuori da quelli restituiscono
`None`.

| Variabile | Intervallo | Perché quel confine |
|---|---|---|
| Crescita ricavi | −20% … +100% | oltre il raddoppio annuo per cinque anni si esce dal dominio della stima |
| Margine EBIT | 0% … 60% | il 60% è già oltre il migliore di quasi ogni settore |
| Crescita perpetua | 0% … `wacc` − 0,5 | avvicinandosi al WACC il valore esplode e qualunque prezzo è giustificabile |
| Costo del capitale | 4% … 25% | sotto il 4% non si sta più scontando un rischio azionario |

**Il limite non è un dettaglio tecnico della bisezione.** È l'affermazione che
oltre quel valore l'ipotesi non è più credibile. Allargarlo per «ottenere un
numero» significa esattamente il contrario di ciò che il reverse DCF serve a
fare: si otterrebbe una crescita del 250% l'anno, che non è una risposta ma un
modo elaborato di scrivere *nessuna risposta*.

Il motore, coerentemente, non allarga mai l'intervallo da solo. Se agli estremi
la funzione non cambia segno restituisce `None` con la ragione scritta a parole,
e quella ragione **è** il risultato da riportare. Vale la regola generale della
skill: un buco dichiarato vale più di un numero plausibile.

---

## 7 · Che cosa il reverse DCF non dice

Quattro fraintendimenti, tutti frequenti.

**Non dice che il prezzo è sbagliato.** Dice che cosa il prezzo assume. Se
l'assunzione è plausibile, il prezzo è giustificato — e il reverse DCF ha appena
prodotto un risultato altrettanto utile, solo meno appariscente.

**Non dice quando.** Nessuna delle quattro risposte contiene un tempo. Un prezzo
che sconta ipotesi eroiche può scontarle per anni, e chi ha scommesso contro il
segnale «i grandi titoli americani sono cari» lo ha pagato ogni singolo anno per
oltre un decennio. Vedi `references/00-dottrina-valutazione.md` §7.

**Non isola davvero una variabile.** Ogni funzione tiene ferme le altre tre, ma
nella realtà si muovono insieme: un'azienda che cresce del 58% non ha lo stesso
costo del capitale di una che cresce del 12%. **I quattro numeri non si sommano e
non si combinano.** Ciascuno risponde a «se questa fosse l'unica cosa a cambiare»,
e va detto nel report quando i quattro vengono mostrati insieme.

**Non sostituisce il calcolo diretto.** Serve il fair value, con i suoi scenari e
la sua matrice di sensibilità, perché è da lì che si vede *quanto* le ipotesi
implicite distano da quelle esplicite. Il reverse DCF senza il diretto è una
frase senza termine di paragone.

---

## 8 · Riepilogo

```
reverse_growth ....... crescita uniforme 5 anni.  Limiti  -20% .. +100%
reverse_margin ....... margine EBIT anno 5.       Limiti    0% ..   60%
reverse_g_terminal ... crescita perpetua.         Limiti    0% .. wacc-0,5
reverse_wacc ......... costo del capitale.        Limiti    4% ..   25%
```

Cinque cose da ricordare.

1. **È la domanda più utile**, perché non chiede a chi legge di credere alle
   ipotesi di chi calcola.
2. **L'ordine è crescita → margine → crescita perpetua → costo del capitale**, dal
   più leggibile al più tecnico. Nel report condiviso si porta il primo.
3. **`None` è un risultato**, e spesso il più forte: sul caso di riferimento dice
   che nessun margine plausibile giustifica il prezzo.
4. **La frase ha una forma fissa**: prezzo, data, «sta scontando», nessuna
   conclusione in coda.
5. **I quattro numeri non si combinano.** Sono quattro letture della stessa
   distanza, non quattro conferme indipendenti.

Il file successivo, `references/06-verdetto-e-linguaggio.md`, prende questa frase
e stabilisce come si scrive tutto il resto intorno — e soprattutto che cosa non si
scrive mai.
