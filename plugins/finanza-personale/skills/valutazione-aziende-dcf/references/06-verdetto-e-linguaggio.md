# 06 · Il verdetto e il linguaggio — che cosa si scrive, e che cosa non si scrive mai

Tutti i file precedenti servono a produrre un risultato difendibile. Questo file
serve a **non rovinarlo nella consegna**.

Non è una questione di stile. Un fair value accompagnato da quattro scenari e da
una matrice di sensibilità, se introdotto dalla frase «il titolo è
sopravvalutato», è stato letto come un consiglio di vendita prima che il lettore
arrivasse alla seconda riga. La forma non è il vestito del contenuto: in questa
materia **è** il contenuto.

C'è anche una ragione esterna, ed è bene averla presente. In Italia la consulenza
finanziaria a titolo professionale è riservata a soggetti abilitati, e la
diffusione di raccomandazioni di investimento è disciplinata anche quando è
gratuita. La forma decisa qui — scenari e ipotesi, mai un voto — non è prudenza
generica: è la ragione per cui questo lavoro resta materiale di analisi.

---

## 1 · La forma del verdetto

Il verdetto di una valutazione **non è un giudizio sul titolo**. È una
descrizione della distanza fra due cose: le ipotesi che il prezzo sconta e le
ipotesi che si è disposti a difendere.

Ha tre pezzi, sempre nello stesso ordine.

```
1. la frase del reverse DCF ......... che cosa il prezzo sta scontando
2. il termine di paragone ........... contro che cosa si misura quell'ipotesi
3. che cosa la falsificherebbe ...... i due o tre indicatori da guardare
```

Il terzo pezzo è quello che si dimentica, ed è quello che rende il documento
riutilizzabile fra sei mesi. Un verdetto senza indicatori di falsificazione è una
posizione, non un'analisi: non c'è modo di sapere se aveva ragione.

Esempio completo, dal caso di riferimento.

> A 35,93 dollari, al 7 agosto 2026, il prezzo sta scontando ricavi in crescita
> del 58% l'anno per cinque anni — quasi dieci volte il fatturato attuale.
> L'azienda è cresciuta del 106% nell'ultimo esercizio, ma per acquisizione; il
> concorrente più grande del settore cresce intorno al 25%.
> Da guardare: il tasso di crescita organica nelle prossime due trimestrali, e se
> il margine operativo tiene il 22% mentre i ricavi salgono.

Nessun voto, nessun obiettivo di prezzo, nessun orizzonte temporale — e chi legge
sa esattamente che cosa pensare e che cosa controllare.

---

## 2 · I due registri

Sono decisi dal parametro `registro` del template, non dall'umore di chi scrive.
Il calcolo è **identico**: cambia solo che cosa viene mostrato.

| | **interno** | **condiviso** |
|---|---|---|
| Per chi | te | genitori, amici, un cliente che ha chiesto di un titolo |
| Fair value puntuale | sì | **no** |
| Fair value | numero singolo, con la matrice | **solo come intervallo**, con i tre scenari affiancati |
| Ipotesi grezze | tutte | le tre motivazioni, non i quindici campi |
| Le quattro risposte del reverse DCF | tutte e quattro | **la prima**, al massimo le prime due |
| Titolo del documento | nome dell'azienda e data | **la frase del reverse DCF** |
| Matrice di sensibilità | sì | sì — è ciò che impedisce di leggere il range come una promessa |

La regola che genera tutte le righe della colonna di destra è una sola:

> **Un numero singolo viene letto come un obiettivo di prezzo, qualunque
> avvertenza ci sia sotto.**

Non è pessimismo sul lettore. È che il numero è la cosa più facile da ricordare
di un documento di sei pagine, e sei mesi dopo è l'unica cosa che resta. Un
intervallo con tre scenari affiancati resiste a quella compressione; «14,14» no.

**Il registro condiviso non è una versione semplificata.** Non si tolgono la
sensibilità, gli allarmi o le trappole contabili: quelli restano tutti. Si toglie
solo ciò che può essere scambiato per un'istruzione.

**E non è nemmeno facoltativo: si producono sempre tutti e due.** Non è una
scelta da fare caso per caso in base a chi leggerà — nel momento in cui la si
fa, si è già deciso che quella valutazione a qualcuno non si mostra. Ogni
valutazione deve esistere **anche in una forma mostrabile a terzi**: è la stessa
disciplina del fair value, spostata dal numero al documento. Il record nel
registro porta il percorso del **condiviso**, mai quello dell'interno — un
record condivisibile non contiene puntatori a materiale che non lo è.

---

## 3 · Elenco esplicito delle frasi vietate

Vietate in **entrambi** i registri, salvo dove indicato. L'elenco è chiuso nel
senso che non ammette eccezioni caso per caso; è aperto nel senso che una formula
nuova che produce lo stesso effetto è vietata anche se non compare qui.

### A · Voti e giudizi sintetici

| Vietato | Perché | Che cosa si scrive invece |
|---|---|---|
| «buy», «sell», «hold», «comprare», «vendere», «tenere» | è una raccomandazione operativa | *«a questo prezzo il mercato sta scontando…»* |
| «accumulare», «alleggerire», «sovrappesare», «sottopesare» | idem, travestito da linguaggio di portafoglio | *«l'ipotesi implicita è più esigente di quella storica»* |
| «outperform», «underperform», «neutral» | voto da casa d'analisi | — non ha sostituto: si toglie |
| «conviction alta», «alta convinzione» | trasforma l'incertezza in fiducia | *«la sensibilità al costo del capitale è alta/bassa»* |
| «il mio giudizio è positivo» | il documento non esprime giudizi sul titolo | *«le ipotesi implicite sono dentro/fuori il già osservato»* |

### B · Obiettivi di prezzo, dichiarati o mascherati

| Vietato | Perché | Che cosa si scrive invece |
|---|---|---|
| «target price», «prezzo obiettivo» | è la cosa che questo lavoro non produce | *«fair value dello scenario base, con le ipotesi X, Y, Z»* |
| «vale 14,14 dollari» | il valore non è una proprietà dell'azienda | *«con queste ipotesi il modello restituisce 14,14»* |
| «upside del 40%», «downside del 61%» | un target price in percentuale | *«il prezzo sta 2,5 volte sopra lo scenario base»* |
| «ha spazio per salire fino a…» | previsione di prezzo | — si toglie |
| «potenziale di rivalutazione» | idem, in tono istituzionale | — si toglie |
| il fair value come numero isolato, nel registro **condiviso** | viene letto come obiettivo | l'intervallo con i tre scenari affiancati |

**Il multiplo non è più innocente della percentuale.** *«Il prezzo sta 2,5 volte
sopra lo scenario base»* e *«upside del 154%»* dicono la stessa identica cosa:
cambia la cornice, non il contenuto. Il multiplo si preferisce perché non ha la
forma di un obiettivo raggiungibile, ma il presidio vero non è il formato — è la
frase intorno.

> **Il multiplo non si lascia mai da solo.** Ovunque compaia, nella stessa frase
> o in quella immediatamente successiva, va detto **che cosa il mercato sta
> assumendo** per arrivarci.

Non *«il prezzo sta 2,5 volte sopra lo scenario base»* e a capo, ma *«il prezzo
sta 2,5 volte sopra lo scenario base: a quel livello sta scontando ricavi in
crescita del 58% l'anno per cinque anni»*. Il numero da solo è una distanza; la
distanza con l'ipotesi accanto è un'affermazione verificabile sul mondo.

### C · Etichette secche

| Vietato | Perché | Che cosa si scrive invece |
|---|---|---|
| «sopravvalutata», «sottovalutata» | comprime sei ipotesi in una parola, e la parola suona definitiva | *«il prezzo sconta ipotesi più esigenti di quelle che si sanno difendere»* |
| «cara», «a sconto», «a buon mercato» | idem, più colloquiale e quindi più efficace | *«aspettative esigenti / modeste»*, con il termine di paragone |
| «occasione», «opportunità» | è un invito | — si toglie |
| «value trap», «bolla», «hype» | giudizio caricato che non esce dal modello | *«il valore terminale pesa il 91%: il modello sta parlando del sesto anno in poi»* |
| «il mercato sbaglia», «il mercato non ha capito» | presuppone di avere ragione | *«il prezzo sconta ipotesi che non si sanno difendere con i dati disponibili»* |
| «solido», «di qualità», «gioiello» | aggettivi che non hanno un campo nel modello | il ROIC storico, il margine, i numeri che stanno dietro l'aggettivo |

### D · Orizzonti temporali impliciti

| Vietato | Perché | Che cosa si scrive invece |
|---|---|---|
| «nel medio termine», «nel lungo periodo» | un orizzonte senza data è una promessa senza scadenza | — si toglie: il modello non produce tempi |
| «prima o poi il prezzo si allineerà» | non esce da nessun calcolo | *«il reverse DCF non dice quando, e non può»* |
| «quando il mercato se ne accorgerà» | idem, con una tesi di mercato in più | — si toglie |
| «già scontato dal mercato» come conclusione | usa il gergo per chiudere il discorso | *«a questo prezzo l'ipotesi implicita è…»* |

### E · Imperativi operativi

Tutta la categoria è vietata senza sostituto, perché la skill non produce
istruzioni. Nessun *«compra sotto X»*, *«aspetta un ritracciamento»*, *«entra
gradualmente»*, *«riduci l'esposizione»*, *«prendi profitto»*, *«non ha senso
comprare a questi prezzi»*.

Vale anche per la forma condizionale e per quella impersonale: *«si potrebbe
valutare un ingresso»* è un imperativo con un cappello.

### F · Certezza mascherata

| Vietato | Perché | Che cosa si scrive invece |
|---|---|---|
| «il fair value è 14,14» | il verbo essere trasforma un'ipotesi in un fatto | *«con queste ipotesi il fair value risulta 14,14»* |
| «i fondamentali dicono che…» | i bilanci non dicono niente da soli | *«i dati dell'ultimo esercizio sono X; l'ipotesi che ci costruisco sopra è Y»* |
| «il modello dimostra» | un modello non dimostra, calcola | *«il modello restituisce»* |
| «conservativo», «prudenziale» senza riferimento | prudente rispetto a che cosa? | *«sotto la guidance aziendale di 4 punti»* |
| «per prudenza ho alzato il WACC di 1,5 punti» | doppio conteggio mascherato — vedi `references/03-tasso-di-sconto.md` §6 | *«premio specifico +1,5 punti per concentrazione della clientela»* |

### G · Aggregazioni vietate

| Vietato | Perché |
|---|---|
| «la somma dei fair value delle prime dieci posizioni» | non esiste un fair value di un paniere: vedi `references/07-ponte-etf.md` |
| «l'ETF è sopravvalutato del 20%» | somma errori correlati e produce una precisione inesistente |
| «il portafoglio sconta una crescita media del…» | media di numeri che non sono commensurabili |

---

## 4 · Le tre categorie qualitative

Sono l'unica forma di sintesi ammessa, e sostituiscono tutte le etichette del
gruppo C. Descrivono **l'ipotesi implicita nel prezzo**, non il titolo.

| Categoria | Definizione operativa |
|---|---|
| **aspettative modeste** | il prezzo è giustificato da ipotesi pari o inferiori a quanto l'azienda ha già realizzato |
| **aspettative esigenti** | servono ipotesi sopra il proprio storico, ma dentro quanto un concorrente del settore ha davvero sostenuto |
| **aspettative eroiche** | servono ipotesi che nessun termine di paragone osservabile sostiene, oppure il risolutore non trova soluzione entro i limiti |

Tre proprietà volute.

**Sono ancorate a qualcosa di osservabile** — lo storico dell'azienda e il miglior
concorrente — non a una soglia numerica decisa a tavolino.

**Descrivono il prezzo, non l'azienda.** «Aspettative eroiche» non significa
«azienda cattiva»: spesso significa il contrario, un'azienda molto buona a un
prezzo che assume che resti tale.

**Non contengono un'azione.** Nessuna delle tre suggerisce che cosa fare, ed è
esattamente il motivo per cui esistono al posto di «cara» e «a buon mercato».

Il caso di riferimento a 35,93 sta in **eroiche**, e ci sta per il criterio più
netto dei due: `reverse_margin` non trova soluzione entro il 60%.

---

## 5 · Che cosa deve sempre comparire

Sette cose. La loro assenza è un difetto del documento, non una scelta di
sintesi.

1. **Il prezzo con data e ora**, e la modalità **CAMPO** dichiarata in testa: il
   prezzo arriva dal web, non dal connettore. Vale la regola di
   `metodo-fiduciario/SKILL.md` §2.
2. **L'esercizio di riferimento** — quale annuale è stata usata. Un fair value
   costruito su un bilancio di quattordici mesi fa non è sbagliato, è vecchio, e
   le due cose si distinguono solo se la data c'è.
3. **Le tre motivazioni**, una riga per scenario, nella forma numero-fonte-meccanismo
   di `references/02-ipotesi.md` §8.
4. **La matrice di sensibilità.** In entrambi i registri. È ciò che impedisce di
   leggere l'intervallo come una promessa.
5. **Tutti e cinque i controlli del motore, ognuno con il suo stato** — e sono
   tre, non due. Vedi §5-bis.
6. **Che cosa falsificherebbe le ipotesi** — due o tre indicatori, con la soglia.
7. **La chiusura fissa**: contenuto informativo, non consulenza finanziaria
   personalizzata.

---

## 5-bis · I tre stati di un allarme

Un allarme del motore non ha due stati, ne ha **tre**. Vale per tutti e cinque —
`SBC_ELEVATA`, `TV_DOMINANTE`, `G_SOPRA_RISK_FREE`, `CASSA_NETTA`,
`PARTECIPAZIONI_RILEVANTI` — e il documento li elenca tutti e cinque, sempre,
ognuno con il suo stato accanto.

| Stato | Che cosa significa | Quando |
|---|---|---|
| **scattato** | la soglia è stata superata | il motore ha restituito la sigla |
| **non scattato** | il controllo è girato e la soglia non è stata superata | tutti i dati che gli servono ci sono |
| **non valutabile** | il controllo **non è potuto girare**: manca un dato | il campo che gli serve è vuoto |

Il terzo stato è quello che esiste per una ragione precisa, ed è la stessa per
cui in `verifica.py` l'assenza di un interprete più vecchio dà GIALLO e non
VERDE:

> **Un controllo che non ha potuto girare non è un controllo superato.**
> Se lo si conta come «non scattato», il controllo diventa silenziosamente un
> no-op che dice «tutto bene». È un modo di fallire peggiore del non avere il
> controllo, perché consuma la fiducia che gli si dà.

I due campi opzionali del motore, `sbc` e `risk_free`, sono l'unico posto da cui
nasce oggi un «non valutabile»: se restano vuoti i rispettivi allarmi non possono
scattare. Si valorizzano sempre. Quando non si può — il dato non è nel bilancio,
o non è stato letto — lo stato è **non valutabile**, scritto nel documento, e non
si scrive «nessun allarme».

La frase «nessun allarme emesso» si può scrivere **solo** se tutti e cinque i
controlli sono girati davvero. Con anche uno solo in «non valutabile», la frase
onesta è: *«nessuno dei controlli che hanno potuto girare ha superato la propria
soglia»*, seguita da quali non hanno potuto girare e perché.

Un allarme taciuto resta ciò che era: l'unico modo di trasformare uno strumento
di controllo in un abbellimento.

---

## 6 · Il caso del cliente che chiede di un titolo

È l'unico caso in cui questo lavoro entra in un mandato di terzi, e ha una regola
propria perché è il punto in cui la forma cede più facilmente.

La risposta ha **una sola funzione**: spiegare che scommessa c'è dietro il prezzo,
e riportare al piano. Registro condiviso, sempre.

**Nel registro finiscono due record distinti, e devono restare separati.**

| | che cos'è | `layer` | `soggetto` | punta a |
|---|---|---|---|---|
| **la valutazione** | il lavoro sull'azienda | `dottrina` | `-` | il documento **condiviso** |
| **la traccia** | che quel giorno, a quel cliente, hai risposto su quel titolo | `mandato` | il cliente | lo stesso documento **condiviso** |

Sono due cose diverse: **la valutazione non appartiene a nessuno** — vale per
chiunque la legga, ed è per questo che è dottrina — mentre **la conversazione
appartiene a quel rapporto**, e dice che quel giorno, a quel cliente, hai
risposto su quel titolo. Un solo record che facesse le due cose renderebbe la
valutazione proprietà di un mandato, e la volta che lo stesso titolo servisse
per un altro soggetto non si saprebbe se riutilizzarla.

Entrambi puntano al documento **condiviso**: vale qui come ovunque, un record
condivisibile non contiene puntatori a materiale che non lo è. Il documento
interno resta sul disco, e non è indicizzato da nessuno dei due.

**Il rapporto normale è uno a molti**, non uno a uno: l'azienda si valuta una
volta, le conversazioni che la citano sono molte. Nel tempo più tracce di
mandato — soggetti diversi, date diverse — puntano alla **stessa** valutazione
di dottrina. Non è un caso limite da gestire: è la ragione per cui la
valutazione sta in dottrina e non dentro il primo mandato che l'ha richiesta.
Finché è corrente si riusa; quando scade si rivaluta **una volta sola**, e le
tracce successive puntano alla nuova.

Tre cose che non si fanno, in ordine di frequenza.

**Non si risponde alla domanda che è stata fatta se è «devo comprarlo?».** Si
risponde a quella utile, che è «che cosa si sta comprando a questo prezzo»,
dicendo esplicitamente che è un'altra domanda.

**Non si collega la risposta al portafoglio del cliente.** «Ne hai già l'8% via
ETF, quindi…» è già allocazione, ed è già l'altra skill.

**Non si lascia il numero da solo alla fine.** L'ultima riga di quel documento è
il rimando al piano, non il fair value.

---

## 7 · Prova di lettura, prima di consegnare

Quattro domande. Se anche una sola risposta è «sì», il documento va riscritto,
non ammorbidito.

1. Esiste **una sola frase** che, estratta e mandata per messaggio senza il
   resto, suonerebbe come un consiglio?
2. Il **numero più grande** del documento è il fair value? (Nel condiviso non
   deve nemmeno esserci come numero singolo.)
3. C'è un **aggettivo** che non ha dietro un campo del modello o un dato di
   bilancio?
4. Se il prezzo raddoppiasse domani, il documento risulterebbe **sbagliato**? Se
   sì, era una previsione — e questo lavoro non ne produce.

---

## 8 · Riepilogo

Cinque regole, e la prima le contiene tutte.

1. **Il documento descrive il prezzo, non l'azienda, e non contiene azioni.**
2. **Il numero singolo si consegna solo nel registro interno**, sempre con le
   ipotesi e la matrice.
3. **Le uniche etichette ammesse sono tre**: aspettative modeste, esigenti,
   eroiche — ancorate allo storico e al miglior concorrente.
4. **Nessun orizzonte temporale**, in nessuna forma: il modello non ne produce.
5. **Un allarme taciuto è un difetto**, non una semplificazione — e gli stati di
   un allarme sono **tre**: scattato, non scattato, non valutabile (§5-bis).

Il file successivo, `references/07-ponte-etf.md`, applica tutto questo al punto
più delicato: che cosa succede quando le aziende valutate stanno dentro un ETF
che si possiede.
