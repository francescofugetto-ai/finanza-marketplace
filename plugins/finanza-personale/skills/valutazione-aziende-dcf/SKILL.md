---
name: valutazione-aziende-dcf
description: "Valuta SINGOLE AZIENDE QUOTATE con il metodo dei flussi di cassa scontati (DCF): fair value in tre scenari, matrice di sensibilità WACC × crescita perpetua, ponte esplicito voce per voce da enterprise value a equity value, e reverse DCF — quali ipotesi di crescita, margine, crescita perpetua e costo del capitale il prezzo di mercato stia già scontando. Usala quando si valuta un'azienda quotata o se ne calcola il valore intrinseco, si legge una relazione annuale (mai una trimestrale) ai fini della valutazione, si chiede «che cosa sta prezzando il mercato a questo prezzo» o «con quali ipotesi si giustifica questa quotazione», si riapre o si aggiorna una valutazione già fatta, oppure si dà il comando di manutenzione «aggiorna se necessario le valutazioni delle N aziende più pesanti dell'ETF <ISIN>» — che produce uno scadenzario con azione differenziata, non N valutazioni. NON si attiva per: allocazione di portafoglio e asset allocation, ribilanciamento, scelta o confronto fra ETF, allocazione di un PAC o di un versamento straordinario, profilazione di un investitore o di un cliente, rendimento atteso di un portafoglio, titoli di Stato, valutazione di asset che non siano azioni di società (criptovalute, materie prime, oro, immobili: il metodo qui è il DCF su flussi di cassa d'impresa, e su quelli non si applica), distillazione di articoli, newsletter o notizie. Quelle restano rispettivamente a consulenza-portafogli-etf (quanto e su quale asset class), rendimenti-attesi-portafoglio (quanto rende l'insieme a dieci anni), analisi-titoli-di-stato-eu (bond singoli) e analisi-documenti-investimento (fonti, e valutazione di uno strumento rispetto allo scopo). Non entra nelle sessioni di allocazione, non decide mai pesi di portafoglio e non genera trigger di ribilanciamento."
---

# Valutazione di aziende quotate — DCF e reverse DCF

Skill operativa per valutare **singole aziende quotate** con i flussi di cassa
scontati, e per leggere al contrario che cosa il prezzo di mercato stia già
scontando.

Il suo scopo non è produrre un numero. È **rendere visibili le ipotesi** che
stanno dietro un prezzo — le proprie e quelle del mercato — e tenerle aggiornate
nel tempo.

> **La domanda giusta non è «quanto vale». È «con quali ipotesi».**

Eredita postura, modalità BANCO/CAMPO, gerarchia delle fonti e disciplina
anti-timing da `metodo-fiduciario/SKILL.md`, che resta l'entry point del sistema.
La dottrina di questa skill è in `references/00-dottrina-valutazione.md`, da
leggere **prima** di aprire un bilancio.

## Il confine, prima di tutto il resto

Questa skill è la sola del sistema che può entrare in conflitto con l'anti-timing.
Il confine è quindi la prima cosa, non l'ultima.

> **Il lavoro di valutazione può cambiare quanto ti aspetti e quanto rischio sai
> di correre. Non può cambiare i pesi.**

- **Non entra** nelle sessioni di allocazione, PAC, ribilanciamento o
  profilazione. Se una vista del registro segnala una valutazione scaduta durante
  una revisione mensile, lo si annota e **si apre una sessione separata**.
- **Non produce** indicazioni su pesi, tilt, ingressi o uscite, in nessuna forma,
  nemmeno al condizionale e nemmeno se richieste esplicitamente.
- **Il suo output alimenta due cose e due sole**: le aspettative
  (`rendimenti-attesi-portafoglio`, come strato di contesto, mai come sostituto
  del top-down `DY + g`) e i vincoli di consapevolezza a registro.
- **Vive in un progetto dedicato**, «Valutazioni aziende», perché non appartiene a
  nessun mandato: il registro archivia questi documenti per *azienda*, non per
  *soggetto*.

Le regole per esteso, con le tre categorie qualitative e la zona grigia dei flussi
del PAC, sono in `references/07-ponte-etf.md`.

## Identità e principi guida

1. **Le ipotesi le sceglie chi valuta, l'aritmetica la fa lo script.** Un modello
   linguistico che moltiplica margini e attualizza flussi su cinque anni sbaglia,
   e sbaglia in silenzio. Nessun numero del modello si calcola a mano nella
   risposta: si passa da `scripts/dcf_engine.py`.
2. **Ogni ipotesi porta una riga di motivazione** nella forma
   *numero · fonte · meccanismo*. Se non ci sta in una riga, di solito è perché
   non c'è. Vedi `references/02-ipotesi.md` §8.
3. **Si parte dall'EBIT reported.** Mai da EBITDA, mai da metriche *adjusted*. La
   stock-based compensation non si ri-aggiunge mai, e si usano le azioni diluite.
4. **Si usa la relazione annuale, mai la trimestrale.** Una trimestrale non porta
   la serie storica, il capex normalizzato né lo scadenzario del debito.
5. **Il prezzo è sempre CAMPO.** Si riprende al momento, si scrive con data e ora,
   e non si conserva mai per un confronto successivo.
6. **L'incertezza è il risultato, non il disturbo.** Un fair value non si consegna
   mai da solo: sempre con le ipotesi che lo generano e con la matrice di
   sensibilità.
7. **Un buco dichiarato vale più di un numero plausibile.** Dove non esiste una
   risposta corretta, il motore solleva un errore o restituisce `None` con la
   ragione scritta: quella ragione **è** il risultato da riportare.

## Guardrail (non negoziabile)

- Materiale **informativo e di metodo**, non consulenza finanziaria
  personalizzata. In Italia la consulenza a titolo professionale è riservata a
  soggetti abilitati, e la diffusione di raccomandazioni è disciplinata anche
  quando è gratuita.
- **Mai inventare** una voce di bilancio, un prezzo, un numero di azioni, una
  lista di holdings. Se un dato non c'è, si dichiara e non si procede su quella
  riga.
- **Mai un voto, un obiettivo di prezzo, un'etichetta secca o un orizzonte
  temporale.** L'elenco esplicito delle frasi vietate è in
  `references/06-verdetto-e-linguaggio.md` §3, e vale in entrambi i registri.
- **Mai sommare fair value** di aziende diverse. Non esiste il fair value di un
  ETF.
- **Mai valutare più di un'azienda per intero** nella stessa sessione.
- **Una valutazione che non hai letto non è tua.** Il nucleo è di **8-12 aziende**,
  una rivalutazione piena al mese, e non si aggiunge un'azienda senza toglierne
  una.

## Workflow sequenziale OBBLIGATORIO

Non saltare fasi. Il passo 7 è quello che salta più facilmente ed è quello che
distingue il sistema da un foglio di calcolo.

```
PASSO 1  Ammissibilità (la skill puo' rifiutare, ed e' un risultato)
   ↓
PASSO 2  Estrazione dati — documento > EDGAR via MCP > web solo per il prezzo
   ↓
PASSO 3  Ipotesi in tre scenari, ognuna con una riga di motivazione
   ↓
PASSO 4  Calcolo con dcf_engine.py — nessun numero fatto a mano
   ↓
PASSO 5  Sensibilita' — matrice WACC × crescita perpetua
   ↓
PASSO 6  Reverse DCF — «a questo prezzo il mercato sta scontando X, Y, Z»
   ↓
PASSO 7  Report HTML + record nel registro
```

### PASSO 1 — Ammissibilità

La skill **rifiuta** i casi in cui il flusso di cassa disponibile per l'impresa
non funziona: banche e assicurazioni; società in perdita senza un percorso
credibile al margine; biotech e pre-revenue, dove il valore è opzionalità;
aziende in dissesto; cicliche al picco o al fondo del ciclo senza
normalizzazione; holding il cui valore sta nelle partecipazioni e non
nell'attività operativa.

**Un rifiuto dichiarato vale più di un numero finto.** Il caso da segnalare e non
rifiutare è l'azienda giovane in fortissima crescita: il DCF si può fare, ma il
valore terminale peserà quasi tutto e va detto. Motivi e casi in
`references/00-dottrina-valutazione.md` §5.

### PASSO 2 — Estrazione dei dati

Gerarchia: **documento caricato** (relazione annuale) → **SEC EDGAR** via MCP di
terzi → **web** solo per il prezzo e per il tasso privo di rischio. Ogni voce
porta fonte e data. Se il prezzo viene dal web — e viene sempre dal web — il
documento dichiara **CAMPO in testa**.

Segui `references/01-estrazione-dati.md`: dove stanno le voci in US GAAP e in
IFRS, come si legge il ponte del debito dallo stato patrimoniale, e le quattro
trappole verificate (plusvalenze non realizzate nell'*Other Income & Expense*,
capex raddoppiato in un anno, cassa netta invece di debito netto, classi di azioni
multiple).

### PASSO 3 — Le ipotesi, in tre scenari

Bear, base, bull. Ognuna con **una riga di motivazione**. Segui
`references/02-ipotesi.md` per crescita, percorso dei margini, `sales_to_capital`
e ROIC a regime; `references/03-tasso-di-sconto.md` per il costo del capitale,
che è la leva a cui il risultato è più sensibile; `references/04-valore-terminale.md`
per la crescita perpetua e il fattore `(1 − g/ROIC)`.

Il tasso privo di rischio va preso **nella valuta dei flussi**: un'azienda
americana si sconta sul Treasury, non sul Bund.

**Se si sta riaprendo una valutazione esistente**, prima di scrivere le ipotesi
nuove si apre la precedente e si scrive **che cosa è cambiato e perché**. È
l'append-only applicato al pensiero — vedi `references/08-manutenzione-e-batch.md` §2.

### PASSO 4 — Il calcolo

`scripts/dcf_engine.py`, funzione `run_dcf`. Restituisce la tabella per anno, il
valore terminale, l'enterprise value, il **ponte riga per riga**, il fair value
per azione, l'upside e gli allarmi.

Gli allarmi (`SBC_ELEVATA`, `TV_DOMINANTE`, `G_SOPRA_RISK_FREE`, `CASSA_NETTA`,
`PARTECIPAZIONI_RILEVANTI`) sono **dati, non eccezioni**: il calcolo prosegue e il
documento li mostra tutti. Un allarme taciuto è un difetto del documento.

Valorizza sempre i due campi opzionali `sbc` e `risk_free`: se restano vuoti i
rispettivi allarmi non possono scattare, e il silenzio non è un'assoluzione.

### PASSO 5 — La sensibilità

`sensitivity(inputs, wacc_list, g_list)`. Matrice canonica: WACC
`[8, 9, 10, 11, 12]` sulle righe, crescita perpetua `[2, 2.5, 3, 4, 5]` sulle
colonne. Fa parte del risultato, non è un allegato, e compare in **entrambi** i
registri.

Si legge in tre modi: l'ampiezza, dove cade il prezzo di mercato rispetto alla
matrice, e la pendenza lungo le righe.

### PASSO 6 — Il reverse DCF

Nell'ordine: `reverse_growth` → `reverse_margin` → `reverse_g_terminal` →
`reverse_wacc`. La frase ha una forma fissa —
*«A <prezzo>, alla data <data>, il prezzo sta scontando <ipotesi in parole>»* — e
diventa **il titolo del documento condiviso**.

`None` è un risultato, e spesso il più forte: significa che dentro i limiti di
plausibilità nessun valore di quella variabile giustifica il prezzo. Non si
allargano i limiti per ottenere un numero. Vedi `references/05-reverse-dcf.md`.

### PASSO 7 — Documento e registro

Il documento HTML usa `template-report.html` della cartella `assets/`, che riusa
integralmente il design system di `analisi-documenti-investimento/assets/design-system.md`.
Parametro `registro`: `interno` o `condiviso` — **cambia solo il rendering, mai il
calcolo**. Nel condiviso il fair value compare solo come intervallo con i tre
scenari affiancati.

**Si producono sempre tutti e due, non uno a scelta.** Una valutazione che esiste
solo nella forma interna non è finita: ogni valutazione deve esistere anche in una
forma mostrabile a terzi. Due file distinti, stesso calcolo — vedi
`references/06-verdetto-e-linguaggio.md` §2.

Poi il **record nel registro**, con `kb-registro`: azienda, ticker, esercizio di
riferimento, prezzo con data e ora, modalità, ipotesi dei tre scenari, intervallo
di fair value, frase del reverse DCF, allarmi, `ipotesi_valide_fino_a`, almeno un
trigger con soglia e data, percorso del documento, e — se esiste una valutazione
precedente sulla stessa azienda — `supersedes: ["<il suo id>"]`, che è il modo in
cui il registro collega la catena. A `superato_da` sul record vecchio ci pensa
`kb.py`: non si scrive a mano, e **non esiste nessun campo `supera`**. Formato e
vincoli in `kb-registro/references/SCHEMA.md`.

## Il comando di manutenzione

> *«Aggiorna se necessario le valutazioni delle 12 aziende più pesanti dell'ETF
> IE00BJ0KDR00»*

Si esegue in autonomia e **non produce dodici valutazioni**: produce uno
**scadenzario con azione differenziata**. Le due velocità sono i **90 giorni** del
riesame leggero — solo prezzo nuovo e reverse DCF a ipotesi invariate, eseguito
davvero, in serie — e i **12 mesi o l'evento** della rivalutazione piena, che va
in coda, una al mese.

Le holdings dell'ETF si ottengono con **degrado graduale**: strumento
`etf_holdings` del connettore se esposto (BANCO), altrimenti pagina dell'emittente
via web (CAMPO), altrimenti si chiede. `etf_holdings` **oggi non esiste**, ed è
scritto così apposta: quando arriverà, la skill non andrà riscritta.
**Mai a memoria**, e sempre con la data delle holdings.

Passi, divieti e `scadenzario.py` sono in `references/08-manutenzione-e-batch.md`.

## Self-review gate (prima di ogni consegna)

Procedi solo se tutte le risposte sono «sì».

1. Il caso è **ammissibile** al DCF, o il rifiuto è dichiarato con la ragione?
2. Ogni numero di bilancio ha **fonte e data**, e viene da una **relazione
   annuale**?
3. Il prezzo porta **data e ora**, e la modalità **CAMPO** è dichiarata in testa?
4. Ogni ipotesi ha **una riga di motivazione** con numero, fonte e meccanismo? La
   stessa riga, con il numero cambiato, suonerebbe diversa?
5. Il ponte verso l'equity è mostrato **voce per voce**, e
   `accounting_standard` è coerente con il trattamento dei leasing?
6. La **matrice di sensibilità** c'è, e c'è in entrambi i registri?
7. Il **reverse DCF** c'è, nella forma fissa, senza conclusioni attaccate in coda?
8. **Tutti** gli allarmi emessi dal motore sono nel documento, compresi quelli
   scomodi?
9. Ci sono i **due o tre indicatori** che falsificherebbero le ipotesi, con la
   soglia?
10. Nessuna frase dell'elenco vietato di `references/06-verdetto-e-linguaggio.md`
    §3? Estratta da sola, nessuna frase suonerebbe come un consiglio?
11. Nel registro **condiviso**: il fair value compare solo come intervallo, e il
    titolo è la frase del reverse DCF?
12. Il documento **non contiene** nessuna indicazione su pesi, ingressi o uscite?
13. Il **record** è stato scritto, con `ipotesi_valide_fino_a`, almeno un trigger e
    `supersedes` sull'id della valutazione precedente, se ne esiste una?

## Errori da intercettare e segnalare

- **Partire da EBITDA, dal flusso di cassa operativo o da metriche *adjusted***, e
  ri-aggiungere la stock-based compensation: è fingere che il lavoro dei
  dipendenti sia gratis.
- **Sottrarre le passività per leasing in US GAAP**: il costo del leasing
  operativo è già dentro l'EBIT, sottrarlo è doppio conteggio. Il motore lo
  blocca.
- **Dimenticare le partecipazioni non consolidate**, che sono un attivo separato e
  non compaiono nel flusso operativo.
- **Dimenticare il fattore `(1 − g/ROIC)`** nel valore terminale: vale +21% di
  valore. Calcolarlo una volta sola e riusarlo lungo la riga sbaglia le colonne
  esterne della sensibilità.
- **Riusare il WACC della valutazione precedente** senza verificare che sia una
  scelta e non una dimenticanza.
- **Alzare il tasso «per prudenza»** per compensare ipotesi operative ottimiste: è
  un doppio conteggio mascherato. Se la crescita è troppo alta, si abbassa la
  crescita.
- **Cercare di nascosto il valore che fa tornare il prezzo di mercato.** Farlo
  esplicitamente è il reverse DCF ed è legittimo; la differenza è tutta nel
  dichiararlo.
- **Consegnare un fair value da solo**, senza ipotesi e senza matrice.
- **Trattare il valore terminale dominante come un dettaglio**: sopra l'85% il
  modello sta parlando del sesto anno in poi, e va detto.
- **Usare una trimestrale** perché è più recente.
- **Ricostruire a memoria le prime posizioni di un ETF**: cambiano senza dare
  segnali.
- **Rispondere alla domanda «devo comprarlo?»** invece che a quella utile, «che
  cosa si sta comprando a questo prezzo».

## Rimandi alle altre skill

- `metodo-fiduciario/SKILL.md` — postura, modalità BANCO/CAMPO, gerarchia delle
  fonti, anti-timing, checklist generale. **Entry point del sistema**; il §0.3
  porta la riga di confine di questa skill.
- `rendimenti-attesi-portafoglio/references/metodologia-top-down.md` — il metodo
  `DY + g` che questo lavoro **non sostituisce**. È il destinatario del ponte,
  come strato di contesto e con le quattro condizioni del
  `references/07-ponte-etf.md`.
- `consulenza-portafogli-etf/references/canone-the-bull/rendimenti-attesi.md` — la
  dottrina del rendimento atteso. La puntata sul DCF va aggiunta al canone come
  `[TB-337]` seguendo
  `consulenza-portafogli-etf/references/canone-the-bull/MANUTENZIONE.md`.
- `analisi-documenti-investimento/references/modalita-B-strumento.md` — il confine
  più sottile: quella modalità valuta **uno strumento rispetto a uno scopo**,
  questa skill valuta **un'azienda rispetto a un prezzo**.
- `analisi-titoli-di-stato-eu/SKILL.md` — i titoli di Stato singoli non passano
  mai di qui.
- `kb-registro/references/SCHEMA.md` — formato del record di chiusura.

## File di questa skill

- `references/00-dottrina-valutazione.md` — prezzo contro valore, i tre
  ingredienti, perché la cassa e non l'utile, che cosa non si valuta mai con un
  DCF. **Entry point della skill.**
- `references/01-estrazione-dati.md` — dove stanno le voci in US GAAP e in IFRS,
  la regola dell'annuale, il ponte dallo stato patrimoniale, le quattro trappole.
- `references/02-ipotesi.md` — crescita, percorso dei margini,
  `sales_to_capital`, ROIC a regime, la regola sulla stock-based compensation, la
  motivazione in una riga.
- `references/03-tasso-di-sconto.md` — come si costruisce il costo del capitale,
  perché è la leva che muove tutto, perché è un intervallo e non un punto.
- `references/04-valore-terminale.md` — Gordon con e senza ROIC, il vincolo
  `wacc > g`, perché `g` sta sotto il tasso privo di rischio, il TV dominante.
- `references/05-reverse-dcf.md` — le quattro domande e il loro ordine, i limiti
  di plausibilità, come si scrive la frase.
- `references/06-verdetto-e-linguaggio.md` — la forma del verdetto, i due
  registri, **l'elenco esplicito delle frasi vietate**, le tre categorie
  qualitative.
- `references/07-ponte-etf.md` — le regole restrittive verso il portafoglio, la
  tabella di prezzatura implicita, la zona grigia del PAC, la riga di confine.
- `references/08-manutenzione-e-batch.md` — le due velocità di aggiornamento, i
  passi del comando di manutenzione con il degrado graduale sulle holdings, i
  quattro divieti espliciti.
- `scripts/dcf_engine.py` — motore deterministico, nessuna dipendenza esterna,
  funzioni pure. **Copia madre unica**: non si duplica e non si rispecchia nel
  connettore. Riceve input già verificati e non scarica nulla.
- `scripts/test_dcf_engine.py` — prova di riferimento sul modello dell'episodio
  337: i valori annuali, gli aggregati, il fair value 14,14, tutte e 25 le celle
  della sensibilità e i casi limite. **Se non passa, non si valuta niente.**
- `scripts/scadenzario.py` — interroga il registro in **sola lettura** e classifica
  ogni azienda nei quattro stati, con il motivo in una riga. L'ultima valutazione è
  l'ultima della catena costruita con i campi di supersessione del registro,
  `supersedes` e `superato_da`, **non** la più recente per data. Registro assente o
  illeggibile, `ipotesi_valide_fino_a` o i campi di catena mancanti, catena rotta,
  i due campi che si contraddicono: **errore esplicito**, mai un elenco vuoto.
- `scripts/test_scadenzario.py` — prova di riferimento dello scadenzario: i quattro
  stati, i bordi delle soglie, la catena di tre record, i campi malformati, le
  contraddizioni fra i due campi di catena e la prova che il registro resti byte
  per byte quello di prima. Il conteggio dei controlli lo stampa il test stesso
  quando lo esegui: non è ripetuto qui, perché un numero scritto a mano mente
  al primo controllo aggiunto.
- `template-report.html` — nella cartella `assets/`. Le dodici sezioni del
  documento, parametro `registro` fra `interno` e `condiviso`.
