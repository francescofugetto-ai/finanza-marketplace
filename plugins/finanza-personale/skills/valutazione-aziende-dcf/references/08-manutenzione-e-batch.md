# 08 · Manutenzione e comando in serie — le due velocità, e i quattro divieti

Una valutazione non è un documento che si produce: è una posizione che si tiene
aggiornata. Questo file dice a quale ritmo, con quale profondità, e che cosa il
comando di manutenzione **non** deve fare.

Il rischio da cui difende è preciso e ha una forma seducente: *«do in pasto a
Claude i bilanci di tutte le aziende dei miei ETF»*. Non è un problema di potenza
di calcolo. È che **una valutazione che non hai letto non è tua, e un numero che
non è tuo non ti serve a niente.**

---

## 1 · Il perimetro, prima del ritmo

| Regola | Valore |
|---|---|
| Nucleo di aziende seguite | **8–12** |
| Rivalutazione piena | **una al mese** — 1-2 ore la prima volta, 30-40 minuti gli aggiornamenti |
| Riesame leggero | **dieci minuti** l'una, in serie |
| Regola anti-accumulo | **non si aggiunge un'azienda senza toglierne una** |

Il numero 8-12 non è una capienza tecnica: è quante aziende una persona sola può
conoscere abbastanza da accorgersi quando un'ipotesi smette di reggere. Sopra
quella soglia il nucleo diventa un archivio, e un archivio non produce lucidità.

La regola anti-accumulo è quella che si viola per prima, perché togliere sembra
una perdita. Toglierne una significa dichiarare che non la si segue più: il record
resta nel registro, con i suoi numeri, marcato come non più mantenuto. È
informazione, non cancellazione.

---

## 2 · Le due velocità

È la traduzione operativa della regola di scadenza: **prezzo e ipotesi scadono a
velocità diverse.**

| | **Riesame leggero** | **Rivalutazione piena** |
|---|---|---|
| Quando scatta | oltre **90 giorni** dall'ultimo | nuova annuale pubblicata, evento rilevante, o oltre **12 mesi** |
| Che cosa cambia | **solo il prezzo** | le ipotesi si rifanno da capo |
| Che cosa produce | reverse DCF a ipotesi invariate | fair value, scenari, sensibilità, report completo |
| Quanto costa | dieci minuti | 30 minuti - 2 ore |
| Chi lo fa | **il comando, per tutte, in serie** | va **in coda**, una al mese |

**Il prezzo non si conserva mai.** Non è uno stato del sistema: è un fatto con
un'ora sopra. Il campo `prezzo_alla_data` del registro è **storia**, e non si
riusa mai per un confronto successivo — si riprende sempre il prezzo al momento,
dichiarando CAMPO.

**Le ipotesi scadono per evento**, non per calendario. Il tetto dei 12 mesi non è
il criterio principale: è la rete di sicurezza sotto i quattro eventi
(nuova annuale, acquisizione rilevante, guidance rivista, movimento materiale del
tasso privo di rischio). Un'azienda che pubblica l'annuale a marzo va rivalutata a
marzo, non l'anno dopo.

**I 90 giorni sono la soglia del riesame, non della scadenza.** Sono la distanza
oltre la quale il prezzo di riferimento è abbastanza vecchio da non dire più
niente, ma le ipotesi sono ancora quelle di prima. Il riesame leggero esiste
proprio per separare le due cose: aggiorna ciò che si muove in fretta senza
toccare ciò che si muove piano.

### La regola dell'apertura

> **Prima di fare una valutazione nuova si riapre quella vecchia e si scrive che
> cosa è cambiato nelle ipotesi.**

È l'append-only applicato al pensiero, e va rispettata anche quando è scomoda —
specialmente quando è scomoda. Nel registro il collegamento lo tiene il meccanismo
di supersessione che il registro ha già: la valutazione nuova dichiara
`supersedes: ["<id della precedente>"]`, e `kb.py` scrive `superato_da` sul record
superato. **Non esiste un campo `supera`, e non va inventato:** un terzo campo con
la stessa semantica terrebbe due verità sulla stessa catena, e la prima a cedere
sarebbe quella che conta — una valutazione superata mostrata come `CORRENTE`.

Fra due anni la cosa di valore non sarà il fair value. Sarà vedere che a gennaio
si assumeva +15% e a dicembre +8%, e doversi spiegare perché.

---

## 3 · Il comando di manutenzione

La frase tipo, data in chat nel progetto dedicato:

> *«Aggiorna se necessario le valutazioni delle 12 aziende più pesanti dell'ETF
> IE00BJ0KDR00»*

Il comando si esegue in autonomia, e **non produce dodici valutazioni.** Dodici
valutazioni piene sono dodici-ventiquattro ore di lavoro, saturerebbero il
contesto della sessione e violerebbero due regole già in vigore: la cadenza di una
al mese e il principio dell'§1.

Quello che produce è uno **scadenzario con azione differenziata**: un elenco di
stati, un pugno di riesami leggeri eseguiti davvero, e una coda ordinata.

---

## 4 · I passi, nell'ordine

### Passo 1 — Risolvi l'ETF

ISIN → nome ed emittente, con lo strumento `etf_anagrafica` del connettore
`finanza`. Esiste già e non richiede nulla di nuovo. Se il connettore non
risponde, si chiede all'utente e si dichiara **CAMPO**.

### Passo 2 — Ottieni le prime N posizioni, con degrado graduale

Tre livelli, **nell'ordine**, e si scende al successivo solo quando quello sopra
non è disponibile.

| Livello | Fonte | Modalità dichiarata |
|---|---|---|
| **1** | strumento `etf_holdings` del connettore, se esposto | **BANCO** |
| **2** | pagina o file di holdings dell'**emittente**, via web | **CAMPO** |
| **3** | si **chiede all'utente** | CAMPO, con la fonte indicata da lui |

**`etf_holdings` oggi non esiste.** Il connettore `finanza` non lo espone: è una
delle estensioni candidate di una fase successiva, e la fase successiva non è
questa. Il degrado è scritto così **fin da subito**, e la ragione è precisa:
quando lo strumento comparirà, la skill lo userà senza essere riscritta. È la
differenza fra una fase che *aggiunge* e una che *rifà*. Nel frattempo il
livello 2 funziona, dichiarando CAMPO.

Come si verifica il livello 1, in pratica: si guarda l'elenco degli strumenti
effettivamente esposti dal connettore nella sessione corrente. Se `etf_holdings`
c'è, si usa. Se non c'è, si scende — **senza commentare l'assenza come un guasto**,
perché non lo è.

Tre obblighi, validi a tutti e tre i livelli.

**Mai a memoria.** Le prime dieci posizioni di un ETF largo sembrano una cosa che
si sa. Non lo sono: cambiano, e cambiano senza dare segnali. Una lista ricostruita
a memoria è indistinguibile a occhio da una corretta, ed è il modo più diretto di
avvelenare tutto il resto del lavoro.

**Si riporta sempre la data delle holdings.** Sono aggiornate al giorno, non al
momento. Una lista vecchia di sei mesi non è sbagliata: è vecchia, e le due cose
si distinguono solo se la data c'è.

**Mai una lista parziale spacciata per completa.** Se si risolvono otto posizioni
su dodici, si dichiarano otto e si dice quali mancano. Vale la regola generale
della skill: un buco dichiarato vale più di un numero plausibile.

### Passo 3 — Interroga il registro

Con `scripts/scadenzario.py` (§6), **una volta sola per l'intero elenco**. Lo
script legge il registro e non scrive nulla.

### Passo 4 — Classifica in quattro stati

| Stato | Condizione | Azione |
|---|---|---|
| `MAI VALUTATA` | nessun record per quell'azienda | in coda |
| `SCADUTA` | oltre 12 mesi, o `ipotesi_valide_fino_a` superata, o evento maturato | in coda |
| `DA RIESAMINARE` | oltre 90 giorni, entro i 12 mesi | riesame leggero, **ora** |
| `CORRENTE` | entro i 90 giorni | riesame leggero, **ora** |

**Due dei tre criteri di `SCADUTA` li decide lo script, il terzo no.** I 12 mesi e
`ipotesi_valide_fino_a` sono date, e le confronta `scadenzario.py`. L'**evento
maturato** — nuova annuale, acquisizione, guidance rivista, movimento del tasso
privo di rischio — non sta nel registro e lo script non lo può sapere: lo accerta
la skill al passo 5, e quando è maturato porta a `SCADUTA` un'azienda che lo
script aveva dato per `CORRENTE`. Il declassamento si scrive con la ragione, come
tutto il resto.

Le due soglie sono a **estremi inclusi**: a 90 giorni esatti si è ancora
`CORRENTE`, a 91 si passa a `DA RIESAMINARE`; a 365 esatti `DA RIESAMINARE`, a 366
`SCADUTA`. `ipotesi_valide_fino_a` è l'**ultimo giorno valido**: quel giorno la
valutazione regge ancora, dal successivo no.

Ogni stato porta **una riga di motivo**. «`SCADUTA` — ultima valutazione 14 luglio
2025, 390 giorni» è uno stato; «`SCADUTA`» da solo è un'etichetta.

### Passo 5 — Esegui i riesami leggeri

Su `DA RIESAMINARE` e `CORRENTE`, in serie. Per ciascuna: **prezzo nuovo**, con
data e ora, dichiarato CAMPO; poi il **reverse DCF a ipotesi rigorosamente
invariate**, riaprendo gli input dal record precedente.

Anche su `CORRENTE`, e non è una svista: costa dieci minuti, e il prezzo di una
valutazione di due mesi fa è comunque il prezzo di due mesi fa.

**La promozione.** Se il nuovo prezzo esce dall'intervallo di fair value dei tre
scenari oltre una soglia dichiarata nel record, l'azienda viene **promossa a
rivalutazione piena** e messa in coda. La promozione non è una valutazione: è
l'annotazione che le ipotesi vecchie stanno reggendo un prezzo che non avevano
previsto.

**La soglia va letta dal record, non decisa qui.** Se il record non ne porta una,
lo si dichiara e non si promuove — meglio un criterio mancante e dichiarato che
una soglia inventata al momento, diversa a ogni esecuzione.

### Passo 6 — Metti in coda

`SCADUTA` e `MAI VALUTATA`, ordinate per **peso nell'ETF** decrescente, ciascuna
con una data indicativa secondo la cadenza di una al mese.

La coda è un piano, non un impegno: la data indicativa serve a vedere che una
posizione al 6% del peso è in attesa da otto mesi. È esattamente il tipo di cosa
che si perde senza un elenco scritto.

### Passo 7 — Produci l'aggregato qualitativo

Due sole informazioni, entrambe vincolate da `references/07-ponte-etf.md`:

- **quale quota del peso dell'ETF è coperta** da valutazioni correnti;
- **come si distribuiscono** le posizioni coperte fra *aspettative modeste ·
  esigenti · eroiche*.

Nella forma della tabella di prezzatura implicita del `07` §2: riga per riga,
**nessuna riga di totale**, la data delle holdings in testa. E la riga esplicita
che chiude il quadro:

> Da questo quadro non segue nessuna indicazione su pesi, ingressi o uscite. Non
> esiste un fair value di questo ETF, e nessuno è stato calcolato.

### Passo 8 — Scrivi il record nel registro

Un record di manutenzione, che è la memoria dell'esecuzione: senza, la prossima
sessione non sa quando è stata l'ultima.

Il registro ha una **lista chiusa di tipi**, e `valutazione` non è fra questi. Si
registra quindi come `tipo: "dossier"` con `"valutazione"` e `"manutenzione"` fra
i **tag** — è il meccanismo che il registro già usa per discriminare, e lo
scadenzario può interrogare per tag. Vedi `kb-registro/references/SCHEMA.md`.

Contenuto minimo: ISIN e nome dell'ETF, **data delle holdings** e livello di
degrado usato (1, 2 o 3), elenco delle aziende con lo stato e il motivo, i riesami
leggeri eseguiti con il prezzo e l'ora, le eventuali promozioni con la ragione, la
coda ordinata, il percorso del documento prodotto.

---

## 5 · I quattro divieti del comando

Espliciti, e senza eccezioni.

**Mai sommare i fair value.** Non esiste un fair value di un ETF — vedi
`references/07-ponte-etf.md` §2, regola 1. Il comando tocca più aziende
contemporaneamente ed è quindi il punto del sistema in cui la tentazione di
aggregare è massima. È il motivo per cui il divieto è ripetuto qui.

**Mai produrre un'indicazione su pesi, tilt, ingressi o uscite.** Nemmeno come
osservazione in coda, nemmeno al condizionale, nemmeno se richiesta
esplicitamente nella stessa chat. Se la richiesta arriva, si risponde che è
un'altra sessione e un'altra skill.

**Mai valutare più di un'azienda per intero nella stessa sessione.** Il comando
produce riesami leggeri e una coda. Se una rivalutazione piena serve subito, si
apre una sessione dedicata a quella sola azienda.

**Mai stimare le holdings di un ETF a memoria.** Se nessuno dei tre livelli del
passo 2 risolve, il comando si ferma e lo dice. Un elenco inventato di posizioni
si propaga silenziosamente in ogni passo successivo, e nessun controllo a valle lo
intercetta.

---

## 6 · `scadenzario.py`

Script deterministico, **sola lettura**, nessuna dipendenza esterna. Sta in
`scripts/scadenzario.py`, accanto al motore, e si invoca come gli altri script del
sistema:

```
python3 scadenzario.py --registro <KB_ROOT>/ledger.jsonl \
                       --aziende "Alphabet" MSFT "Bending Spoons" \
                       [--oggi AAAA-MM-GG] [--riesame 90] [--scadenza 365] [--json]
```

**Input:** percorso del registro, elenco di aziende — nome, ticker o ISIN
indifferentemente, perché chi interroga per ISIN deve ottenere il record e non un
`MAI VALUTATA` falso —, data odierna, soglie: di default **90 giorni** per il
riesame e **365** per la scadenza piena.

**Output**, per ciascuna azienda: ultima valutazione trovata con data e
identificativo, giorni trascorsi, `ipotesi_valide_fino_a`, esercizio di
riferimento usato, lo stato fra i quattro, e il **motivo dello stato in una riga**.

**Dove le trova.** Una valutazione nel registro è un record `tipo: "dossier"` con
`"valutazione"` fra i tag (passo 8). I campi propri della valutazione —
`azienda`, `ticker`, `isin`, `esercizio_di_riferimento`, `ipotesi_valide_fino_a`
— lo schema del registro **non li conosce e non li valida**: li valida questo
script, ed è il motivo per cui la validazione qui è severa. È l'unico posto in cui
viene fatta.

Quattro regole di comportamento, tutte pensate contro un errore specifico.

**Vince l'ultima della catena, non la più recente per data.** Se un'azienda compare
più volte nel registro, la catena si costruisce con i **campi di supersessione del
registro**: `supersedes` (lista di id, la dichiara il record nuovo, punta
all'indietro) e `superato_da` (id singolo o `null`, lo scrive `kb.py` sul record
superato insieme a `stato: "superato"`). È diverso dall'ordinamento per data, e la
differenza emerge quando un record vecchio viene inserito dopo — cosa che succede
quando si recupera una valutazione arretrata.

> **Non esiste un campo `supera`.** La catena delle valutazioni è la stessa catena
> di supersessione di tutti gli altri documenti del registro, e si legge dai due
> campi che `kb.py` già scrive. Un campo in più con la stessa semantica
> significherebbe due verità sulla stessa catena, con nessuno a tenerle allineate.

Nella catena di un'azienda, `supersedes` elenca **solo** valutazioni della stessa
azienda, e **al massimo una**: la storia di un'azienda è lineare. Un id fuori da
quell'insieme, o due predecessori, fermano lo scadenzario.

**Registro illeggibile o percorso inesistente → errore esplicito.** Mai un elenco
vuoto spacciato per «nessuna valutazione trovata». Sono due situazioni opposte:
una dice che non c'è niente da aggiornare, l'altra che non si sa niente. Per la
stessa ragione un `MAI VALUTATA` dichiara nel motivo **quante** valutazioni il
registro conteneva in tutto: zero letto è diverso da zero perché non si è letto.

**`ipotesi_valide_fino_a` o i campi di catena mancanti o malformati → errore.** Una
data di scadenza assente **non si legge mai come «nessuna scadenza»**: mostrerebbe
tutto come `CORRENTE` proprio quando non lo è, ed è il modo peggiore in cui questo
strumento possa sbagliare. `supersedes` e `superato_da` devono esserci entrambi —
`kb.py` li scrive sempre, anche vuoti, quindi un record che ne è privo non è
passato di lì: assente, «non lo so» diventerebbe «non è superato». Allo stesso modo
si ferma su una catena rotta — anello che punta a un id inesistente, `superato_da`
che punta a un id inesistente, due catene scollegate sulla stessa azienda, due
record che superano lo stesso record, una valutazione che ne supera due, catena
chiusa ad anello: in nessuno di questi casi esiste un'ultima valutazione, e non la
si indovina.

**I due campi di catena che si contraddicono → errore.** `kb.py` li scrive nella
stessa operazione, quindi discordano solo se il registro è stato modificato a mano.
Le tre forme: A dice di essere superato da B ma B non elenca A; B elenca A ma A non
dichiara nulla; i due indicano successori diversi. Fidarsi di uno dei due
significherebbe, in metà dei casi, mostrare come `CORRENTE` una valutazione
superata — in silenzio, che è esattamente ciò contro cui è scritto questo script.

**Nessuna scrittura.** Lo script legge e basta. Il record del passo 8 lo scrive la
skill attraverso il registro, non lo scadenzario.

La prova di riferimento (`scripts/test_scadenzario.py` — il numero dei controlli
lo stampa lui stesso alla fine, e per questo non è ripetuto qui) verifica:
azienda mai valutata; valutazione di 30 giorni (`CORRENTE`); di 120 giorni
(`DA RIESAMINARE`); di 400 giorni (`SCADUTA`); scaduta per
`ipotesi_valide_fino_a` pur restando sotto i 365 giorni; catena di tre record
collegati da `supersedes`/`superato_da`, dove vince l'ultimo della catena e non il
più recente per data; file inesistente → errore. Più i bordi delle due soglie
giorno per giorno, i campi mancanti o malformati, le forme di catena rotta, le tre
forme di contraddizione fra i due campi, e la verifica che dopo l'esecuzione il
registro sia **byte per byte** quello di prima. I registri di prova nascono dentro
il test in una cartella temporanea: `kb-finanza/` non viene mai aperta, nemmeno in
lettura.

---

## 7 · Che cosa arriva dal connettore, e che cosa no

| Dato | Fonte oggi | Modalità |
|---|---|---|
| Anagrafica dell'ETF | `etf_anagrafica` del connettore | BANCO |
| Holdings dell'ETF | pagina dell'emittente, via web | **CAMPO**, con la data delle holdings |
| Bilanci | documento caricato, o EDGAR via MCP di terzi | BANCO se documento, altrimenti dichiarato |
| Prezzo di mercato | web, con data e ora | **CAMPO, sempre** |
| Tasso privo di rischio | web (Treasury per il dollaro) | dichiarato |

Due note che evitano due errori opposti.

**Il prezzo resta CAMPO per scelta, non per mancanza.** Le fonti gratuite sono
scraping non ufficiale o vincolate a uso non commerciale: uno strumento che le
avvolgesse darebbe l'**illusione di BANCO** su un numero non verificato alla
fonte, che è peggio di dichiarare CAMPO.

**La skill funziona a connettore spento.** In quel caso l'anagrafica dell'ETF si
chiede all'utente, tutto è CAMPO, e il documento si intitola *nota* e non
*report* — è la regola generale di `metodo-fiduciario/SKILL.md` §2, che vale anche
qui.

---

## 8 · Riepilogo

```
90 giorni ....... riesame leggero: solo prezzo + reverse DCF, ipotesi ferme
12 mesi ......... rivalutazione piena, in coda, una al mese
evento .......... nuova annuale, acquisizione, guidance, risk-free: piena, subito
8-12 aziende .... nucleo fisso. Non si aggiunge senza togliere.
```

Cinque cose da ricordare.

1. **Il comando non produce N valutazioni**: produce uno scadenzario, qualche
   riesame leggero eseguito davvero, e una coda.
2. **Le holdings hanno tre livelli di degrado e una data.** `etf_holdings` oggi
   non esiste, e il degrado è scritto lo stesso.
3. **Il prezzo non si conserva mai**; le ipotesi scadono per evento, non per
   calendario.
4. **Prima di rifare una valutazione si riapre la precedente** e si scrive che
   cosa è cambiato.
5. **I quattro divieti** — non sommare, non indicare pesi, non valutare più di
   un'azienda per intero, non ricostruire holdings a memoria.

È l'ultimo file della cartella. Chi arriva qui ha letto il perché
(`references/00-dottrina-valutazione.md`), il come
(`references/01-estrazione-dati.md` … `references/05-reverse-dcf.md`), la forma
(`references/06-verdetto-e-linguaggio.md`) e il confine
(`references/07-ponte-etf.md`).
