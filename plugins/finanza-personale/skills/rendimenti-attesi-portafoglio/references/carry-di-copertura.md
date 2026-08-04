# Carry di copertura, indici governativi e orizzonte di validità

Tre correzioni che si applicano alla gamba obbligazionaria **prima** di confrontarla con qualunque benchmark. Nessuna delle tre è opzionale: ognuna, se omessa, produce un errore nella stessa direzione — sovrastima del rendimento atteso.

---

## 1 · Carry di copertura valutaria

**Il problema.** Lo YTM (o YTW) pubblicato da un indice o da un emittente per un fondo obbligazionario globale è quello **in valuta locale**: è la somma dei rendimenti dei titoli sottostanti nelle rispettive valute. Un investitore in euro che compra la classe **EUR-hedged** non incassa quel numero. Incassa quel numero **più il differenziale dei tassi a breve** fra euro e le valute coperte, che è il costo (o il ricavo) della copertura a termine.

**La formula.**

```
E[r] in euro ≈ YTM_locale + (r_breve_EUR − r_breve_valuta_estera)
```

Il termine fra parentesi è il **carry di copertura**. Deriva dalla parità coperta dei tassi d'interesse: il forward valutario incorpora il differenziale, quindi la copertura trasferisce all'investitore la differenza fra i due tassi a breve, non il rendimento nominale del titolo estero.

**Il segno conta.** Con €STR **sotto** i tassi a breve della valuta estera, il termine è **negativo**: la copertura costa. È il caso tipico degli ultimi anni per un investitore euro esposto al dollaro. Ignorarlo su un Global Aggregate sovrastima quella gamba di **circa 1,5-2 punti percentuali** — su un portafoglio 80/20 sono ~0,3-0,4 punti di rendimento atteso complessivo, cioè un ordine di grandezza superiore a qualunque differenza di TER che stiamo abituati a discutere.

**Come si applica, in ordine di preferenza.**

1. **Se l'emittente pubblica lo *yield to maturity hedged*** (alcuni factsheet lo espongono esplicitamente, spesso come *hedged yield* o *yield in EUR*), usa quello e **dichiara la fonte**. È il dato migliore perché incorpora la struttura effettiva dei contratti forward del fondo.
2. **Altrimenti costruiscilo**: prendi il tasso a breve dell'area euro (€STR) e il tasso a breve della valuta prevalente nell'indice, entrambi con data, e sottrai. Per un indice multi-valuta usa i pesi valutari del factsheet; se non li hai, usa la valuta dominante e **dichiara l'approssimazione**.
3. **Se non hai né l'uno né gli altri**: non stimare a sentimento. Scrivi `n/d` sul carry, riporta il rendimento **in valuta locale marcandolo come tale**, e dichiara che il numero in euro sarà inferiore. Un numero dichiarato incompleto è utilizzabile; un numero completo e sbagliato no.

**Errore da non fare.** Il carry di copertura **non** è la variazione attesa del cambio. Non si stima con una view sull'EUR/USD, non si "media a zero perché nel lungo termine il cambio torna". È un costo contrattuale osservabile oggi nella curva a breve delle due valute.

---

## 2 · Indice governativo puro ≠ aggregate pieno

Il benchmark obbligazionario canonico (**Bloomberg Euro Aggregate Treasury**, `IE00BH04GL39`) è un indice **solo governativo**: duration ~7 anni, scadenza media ~8,6.

Due conseguenze operative.

- **Se il portafoglio ha una gamba corporate**, il delta rispetto a questo benchmark **incorpora anche il premio al credito** — cioè una parte del "vantaggio" misurato non è abilità di selezione, è rischio in più. Va detto in chiaro nel report, non lasciato implicito nel numero.
- **Se la duration della gamba reale è molto diversa da ~7 anni** — una ladder corta, un monetario, o all'estremo opposto un portafoglio di lunghi — il confronto mette a fianco **rischi-tasso diversi**. In quel caso affianca un secondo benchmark di duration comparabile e presenta entrambi. Confrontare uno YTM a duration 2 con uno a duration 7 e concludere qualcosa sull'abilità è un errore di categoria.

---

## 3 · Orizzonte di validità: duration di Macaulay, non scadenza media

La stima `YTW + roll-down − perdita attesa da credito ± carry` è valida su un orizzonte pari alla **duration di Macaulay** del paniere, non alla sua **scadenza media**. Sono due numeri diversi e su un paniere con cedole non banali divergono in modo materiale.

La ragione è che alla duration di Macaulay l'effetto prezzo e l'effetto reinvestimento si compensano: è il punto di **immunizzazione**. È anche l'orizzonte su cui si costruisce una *ladder* per una passività datata.

**Roll-down.** Default **0** se non hai due punti di curva su cui misurarlo. **Negativo se la curva è invertita** — un roll-down positivo assunto per abitudine su curva invertita è un errore di segno, non di taglia.

**Reinvestimento delle cedole.** Lo YTM assume implicitamente il reinvestimento allo YTM stesso. Per titoli con **vita residua sotto i 5 anni e cedole basse** l'impatto è trascurabile: dichiaralo e passa oltre, non gonfiare la cosa. Per cedole alte e vita lunga, invece, l'assunto va nominato esplicitamente fra le ipotesi.

---

## 4 · Bottom-up: il range è osservato, non inventato

Quando costruisci gli scenari a partire dalle capital market assumptions, **scenario prudente = minimo delle CMA ricomposte** e **ottimista = massimo**. È un intervallo **osservato** fra case che pubblicano numeri, non un ±x% convenzionale applicato al top-down.

La differenza non è estetica: un ±1,5 pt inventato dice quanto sei prudente tu; il minimo e il massimo delle CMA dicono quanto **non è d'accordo il mercato delle previsioni**, che è l'unica misura onesta dell'incertezza disponibile. Prima di usarle verifica **valuta, orizzonte e convenzione geometrica/aritmetica**: sono tipicamente in USD e in aritmetica, e un numero così non si confronta con un top-down in euro geometrico senza conversione dichiarata.

---

## 5 · Checklist della gamba obbligazionaria

- [ ] Lo YTM usato è **hedged** oppure il carry è stato **calcolato e sottratto**, con fonte e data dei due tassi a breve?
- [ ] Il segno del carry è coerente con il differenziale corrente (negativo se €STR è sotto il tasso estero)?
- [ ] Il roll-down è 0 in assenza di due punti di curva, e **negativo** se la curva è invertita?
- [ ] L'orizzonte dichiarato è la **duration di Macaulay**, non la scadenza media?
- [ ] Se c'è gamba corporate, il premio al credito nel delta vs benchmark governativo è stato **nominato**?
- [ ] Se la duration reale diverge molto da ~7 anni, è stato affiancato un **secondo benchmark** comparabile?
- [ ] Il range bottom-up è min/max **osservati** fra le CMA, non uno scarto convenzionale?
