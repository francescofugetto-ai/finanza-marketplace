# 01 · Estrazione dei dati — dove stanno le voci, e dove sono le trappole

Questo file risponde a una domanda sola: **da quale riga di quale documento esce
ogni singolo input del modello.** Se un numero non ha una riga e un documento, non
è un dato: è un ricordo.

---

## 1 · La gerarchia delle fonti

Tre livelli, in quest'ordine. Non si scende di livello finché quello sopra è
disponibile.

| # | Fonte | Che cosa dà | Modalità |
|---|---|---|---|
| 1 | **Documento caricato** — la relazione finanziaria **annuale** | tutti gli input tranne il prezzo | BANCO |
| 2 | **SEC EDGAR** via server MCP, dati XBRL ufficiali | gli stessi, verificabili contro l'URL del deposito | BANCO |
| 3 | **Ricerca web** | **solo** il prezzo di mercato | CAMPO |

Il principio che regge questa gerarchia: **un metodo esterno è un problema, un
trasporto dati esterno no.** Un server che legge EDGAR porta un numero pubblico,
confrontabile con il documento originale; il metodo resta interamente qui dentro.

**Il prezzo è l'unico input che non sta in bilancio**, e non esiste una fonte
gratuita e affidabile per prenderlo in modo verificabile. Quindi: si prende al
momento, si scrive con data e ora, e il report dichiara **CAMPO**. Meglio
dichiarare CAMPO che avere l'illusione di BANCO su un dato fragile.

**Il prezzo non si conserva mai.** Non si riusa quello di una valutazione
precedente, nemmeno di due settimane prima. Si riprende, sempre.

---

## 2 · La regola dell'annuale

> **Si usa la relazione annuale. Mai la trimestrale.**

Non è pignoleria: una trimestrale manca di tre cose che servono davvero.

**Manca la serie storica.** Il rapporto fra ricavi incrementali e capitale
investito — che nel motore si chiama `sales_to_capital` — si stima guardando come
si sono mossi insieme ricavi e capitale su tre o cinque anni. Da un trimestre non
si stima: si indovina.

**Manca il capex normalizzato.** *Capex* sta per *capital expenditure*, la spesa
per investimenti in immobilizzazioni. È stagionale e a scatti: un trimestre alto
non significa un anno alto, e un trimestre basso non significa che l'azienda abbia
smesso di investire.

**Manca lo scadenzario del debito.** Le note al bilancio annuale dicono quanto
debito scade e quando. La trimestrale dà il saldo, che è il numero meno
informativo dei tre.

C'è però un uso legittimo della trimestrale, ed è **accorgersi che è successo
qualcosa**: un'acquisizione, un cambio di guidance, un salto del capex. In quel
caso la trimestrale è il campanello, non la fonte. Il paragrafo seguente lo mostra
con un caso reale.

---

## 3 · Le quattro trappole di Alphabet, primo trimestre 2026

Questo caso è nella skill per una ragione precisa: **contiene tutte e quattro le
trappole insieme**, ed è stato scelto come stress test proprio per quello. È anche
la dimostrazione pratica del paragrafo precedente — le trappole si vedono nella
trimestrale, ma per gestirle serve l'annuale.

### Trappola 1 · L'utile gonfiato da guadagni che non sono cassa

Nel conto economico compare la voce **OI&E**, *Other Income and Expense*, che
raccoglie ciò che non è operativo. In quel trimestre conteneva **36,9 miliardi di
plusvalenze non realizzate** su partecipazioni: rivalutazioni di quote in altre
società, non incassi.

*Non realizzate* significa che nessuno ha venduto niente e nessun dollaro è
entrato. Se il prezzo di quelle partecipazioni scende, il trimestre dopo la stessa
voce sarà negativa della stessa natura.

**Come si evita:** si parte dall'**EBIT reported**, la riga *Income from
operations*, che sta **sopra** OI&E e non la include. La trappola scatta solo per
chi parte dall'utile netto o dall'utile ante imposte.

**Conseguenza sul motore:** `revenue_base` ed `ebit_margin` si costruiscono su
ricavi e risultato **operativi**. Le partecipazioni non spariscono dal modello —
rientrano nel ponte, come attivo separato, al §5.

### Trappola 2 · Il capex raddoppiato in un anno

La spesa per investimenti è passata da **17,2 a 35,7 miliardi** su base annua:
più che raddoppiata. È un fatto vero e rilevante, e va gestito, ma non nel modo
che verrebbe naturale.

Il motore **non usa il capex direttamente**. Usa `sales_to_capital`, cioè quanti
ricavi incrementali l'azienda ottiene per ogni unità di capitale investito, e da
lì ricava il reinvestimento con `reinvestment = (ricavi − ricavi precedenti) ÷
sales_to_capital`.

Un capex che raddoppia dice una cosa sola, ed è una domanda: **quel capitale sta
comprando crescita futura, o sta solo mantenendo la posizione?** Se compra
crescita, il rapporto `sales_to_capital` resta stabile e i ricavi futuri saliranno
di conseguenza. Se serve a difendersi, il rapporto peggiora — servono più
investimenti per gli stessi ricavi — e va abbassato.

**Come si sbaglia:** alzare la crescita dei ricavi *e* lasciare
`sales_to_capital` al valore storico. Così l'aumento del capex non compare da
nessuna parte, e la crescita torna a essere gratis.

### Trappola 3 · La cassa netta

Alphabet ha più cassa e attività finanziarie che debito. Il **ponte** dall'valore
dell'impresa al valore per gli azionisti, che di solito **sottrae**, qui
**aggiunge**.

Chi scrive nel modello un «debito netto» come numero unico e positivo, per
abitudine, sottrae un valore che andava sommato — e sbaglia due volte l'importo.

**Nel motore:** non esiste un campo «debito netto». Esistono le voci separate del
`bridge` (§5). Quando la somma delle voci positive supera quella delle negative,
`equity_value` risulta maggiore di `enterprise_value` e scatta l'allarme
`CASSA_NETTA`. L'allarme non è un errore: è una descrizione.

### Trappola 4 · Le tre classi di azioni

Alphabet ha azioni di classe A, B e C, con diritti di voto diversi. Il campo
`diluted_shares` vuole il **totale di tutte le classi, su base diluita** — cioè
comprensivo delle azioni che verranno emesse per i piani di incentivazione già
assegnati.

Prendere solo la classe più scambiata gonfia il valore per azione di una
percentuale enorme, e l'errore non si vede: il risultato resta un numero
plausibile.

**Controllo veloce**, ed è quello che rende evidente la coerenza: le
partecipazioni non consolidate di Alphabet valgono **106.946 milioni**, e sono
state descritte come circa **8,7 dollari per azione**. Il rapporto implica circa
**12.290 milioni di azioni** — l'ordine di grandezza del totale delle tre classi,
non di una sola. Se il conto delle azioni non regge una verifica di questo tipo, è
sbagliato.

---

## 4 · Dal conto economico agli input del motore

Le voci che servono sono cinque, e stanno tutte nelle prime righe.

| Voce di bilancio | US GAAP (10-K) | IFRS | Campo del motore |
|---|---|---|---|
| Ricavi | *Revenues* / *Total net sales* | *Ricavi delle vendite e prestazioni* | `revenue_base` |
| Risultato operativo | *Income from operations* | *Risultato operativo* / *EBIT* | base di `ebit_margin` |
| Aliquota effettiva | *Effective tax rate* nelle note | nota sulle imposte | `tax_rate` |
| Azioni diluite | *Diluted weighted-average shares* | *Numero medio di azioni diluito* | `diluted_shares` |
| Compensi in azioni | *Stock-based compensation* | *Pagamenti basati su azioni* | `sbc` (opzionale) |

**`revenue_base` è dell'ultimo esercizio chiuso**, non della somma degli ultimi
quattro trimestri e non di una stima dell'anno in corso. `year_base` è l'anno di
quell'esercizio: nel caso di riferimento, `revenue_base = 1310` e
`year_base = 2025`.

**L'aliquota effettiva, non quella nominale.** L'aliquota nominale è quella di
legge; quella effettiva è imposte pagate diviso utile ante imposte, ed è l'unica
che descrive quanto l'azienda paga davvero. Nel caso di riferimento vale 27%, e si
passa al motore come `tax_rate = 27.0` — in punti percentuali, non come 0,27.

**`sbc` è opzionale e serve solo a un allarme.** I compensi in azioni sono **già
dentro l'EBIT**, spalmati fra costo del venduto, ricerca e sviluppo e costi
commerciali: il modello che parte dall'EBIT non li sta ignorando. Il campo esiste
perché quando superano il 5% dei ricavi scatta `SBC_ELEVATA`, che segnala una
diluizione rilevante da tenere d'occhio nel conto delle azioni. Su Alphabet:
**6.751 su 109.896 = 6,1%**, l'allarme scatta. Su Coca-Cola siamo intorno all'1%,
non scatta.

---

## 5 · Dallo stato patrimoniale al ponte

Il ponte porta dal valore dell'attività operativa al valore che spetta agli
azionisti. **Non è un numero: è un elenco di voci con il loro segno**, e il motore
lo restituisce riga per riga proprio perché nel report va mostrato come cascata.

| Campo di `Bridge` | Segno | Dove si legge |
|---|---|---|
| `cash_and_securities` | **+** | *Cash and cash equivalents* + *Marketable securities*, attivo corrente |
| `non_consolidated_stakes` | **+** | *Non-marketable securities* / partecipazioni, a valore di libro |
| `total_debt` | **−** | debito finanziario corrente + non corrente, **non** i debiti commerciali |
| `lease_liabilities` | **−** | passività per leasing — **solo IFRS**, vedi sotto |
| `pension_deficit` | **−** | disavanzo dei fondi pensione, al netto dell'effetto fiscale |
| `minority_interests` | **−** | interessenze di terzi nel patrimonio netto |
| `employee_options_value` | **−** | valore delle opzioni in circolazione, dalle note |
| `accounting_standard` | — | `"IFRS"` oppure `"US_GAAP"` |

Tutte le voci si passano come **importi positivi**: è il campo a decidere il
segno. E tutte hanno valore di default zero, così una voce assente non va
dichiarata — ma una voce dimenticata non si distingue da una voce a zero, ed è il
motivo per cui la cascata mostra anche le righe nulle.

### Il leasing dipende dal principio contabile

È la sottigliezza che il motore protegge con un errore esplicito.

**In IFRS 16** il canone di leasing viene scomposto in due pezzi: ammortamento del
diritto d'uso e interessi passivi. Gli interessi stanno **sotto** l'EBIT, quindi
l'EBIT è al lordo della componente finanziaria del leasing → la passività va
sottratta nel ponte, e `lease_liabilities` si valorizza.

**In US GAAP** il leasing operativo resta un costo unico dentro l'EBIT. Sottrarre
anche la passività nel ponte significherebbe contare due volte lo stesso impegno.

Per questo, se `accounting_standard` vale `"US_GAAP"` e `lease_liabilities` è
maggiore di zero, `run_dcf` **solleva un errore** invece di calcolare. Non è una
scortesia: è l'unico modo perché un doppio conteggio non passi in silenzio.

### Il debito finanziario non è tutto il passivo

`total_debt` comprende obbligazioni emesse, finanziamenti bancari, commercial
paper — la parte corrente e quella oltre l'esercizio. **Non** comprende i debiti
verso fornitori, i risconti passivi, i fondi rischi: sono passività operative, già
riflesse nel capitale circolante e quindi già dentro il flusso.

### Le partecipazioni non consolidate valgono davvero

Sono quote in società che l'azienda non controlla e che quindi **non compaiono nel
flusso di cassa operativo**. Su Alphabet valgono 106.946 milioni, circa 8,7 dollari
per azione: ignorarle significa sottovalutare l'azienda esattamente di quella
cifra.

Sono iscritte a **valore di libro**, che per una quota rilevante può essere molto
lontano dal valore reale — in entrambe le direzioni. Quando superano il 10%
dell'enterprise value il motore emette `PARTECIPAZIONI_RILEVANTI`, che è un invito
a dichiarare quel limite nel report, non a correggere il numero di nascosto.

---

## 6 · Il prezzo, e il numero di azioni

`market_price` è l'unico input in modalità CAMPO. Si scrive con **data e ora**,
perché è l'unico che cambia mentre si lavora. Se l'azienda non è quotata si passa
`0`, e il motore restituisce `upside = None`: non zero, non un valore inventato —
niente, perché senza prezzo l'upside non esiste.

`diluted_shares` va in **milioni**, coerentemente con gli importi. Merita una
verifica in più: nel caso di riferimento il documento parlava di **635 milioni**
di azioni, ma il modello ne usava **630**, e la differenza sposta il fair value di
circa l'1%. Non è un errore grave — è il tipo di scarto che va **notato e
dichiarato**, non appianato in silenzio. La prova di riferimento usa 630 perché
deve riprodurre quel modello, non perché 630 sia più giusto di 635.

---

## 7 · Checklist di estrazione

Prima di passare a `02-ipotesi.md`, questi campi devono essere compilati e avere
ognuno la propria riga di provenienza.

```
Dal conto economico dell'ultimo esercizio chiuso
  [ ] revenue_base .......... ricavi, $ mln
  [ ] year_base ............. anno di quell'esercizio
  [ ] EBIT reported ......... per calibrare il primo ebit_margin
  [ ] tax_rate .............. aliquota EFFETTIVA, %
  [ ] sbc ................... opzionale, solo per l'allarme

Dallo stato patrimoniale, stessa data
  [ ] cash_and_securities ....... +
  [ ] non_consolidated_stakes ... +
  [ ] total_debt ................ −  solo finanziario
  [ ] lease_liabilities ......... −  solo se IFRS
  [ ] pension_deficit ........... −  netto d'imposta
  [ ] minority_interests ........ −
  [ ] employee_options_value .... −
  [ ] accounting_standard ....... "IFRS" | "US_GAAP"

Dalle note
  [ ] diluted_shares ........ mln, TUTTE le classi

Da fonte esterna, in CAMPO
  [ ] market_price .......... con data e ora
```

Le quattro domande di controllo, prima di procedere:

1. L'EBIT che sto usando è **reported**, o è una metrica *adjusted*?
2. Il conto delle azioni comprende **tutte le classi**?
3. Il principio contabile è coerente con la voce `lease_liabilities`?
4. C'è una voce del ponte che ho lasciato a zero **perché è zero**, o perché non
   l'ho cercata?

La quarta è quella che si salta.
