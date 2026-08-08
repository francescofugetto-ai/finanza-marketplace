# Changelog — finanza-personale

## 2026-08-08 — l'ottava skill: `valutazione-aziende-dcf`

Valutazione di singole aziende quotate con il metodo dei flussi di cassa
scontati. E' la prima skill che produce un **fair value**, cioe' il tipo di
numero che si presta piu' facilmente a essere letto come una raccomandazione:
buona parte di quello che segue esiste per impedirlo.

**La skill nuova**

- `valutazione-aziende-dcf/scripts/dcf_engine.py` — motore senza dipendenze
  esterne, versione 1.1. Tabella per anno, valore terminale con ROIC, ponte
  **riga per riga** da enterprise value a equity value, matrice di sensibilita'
  WACC × g, cinque allarmi. Quattro risolutori inversi.
- `scripts/test_dcf_engine.py` — prova di riferimento sul modello dell'episodio
  337: valori annuali, aggregati, fair value e tutte e 25 le celle della matrice.
- `scripts/scadenzario.py` + `scripts/test_scadenzario.py` — interroga il
  registro in **sola lettura** e classifica ogni azienda in quattro stati.
  Ricostruisce la catena delle valutazioni leggendo **entrambi** i campi di
  supersessione, e si ferma con un errore se si contraddicono: fidarsi di uno
  solo vorrebbe dire, in meta' dei casi, mostrare `CORRENTE` una valutazione
  superata.
- `references/00`-`08` — nove file di dottrina.
- `assets/template-report.html` — dodici sezioni, parametro `registro` fra
  `interno` e `condiviso`, che **cambia solo il rendering, mai il calcolo**.

**Le regole che il registro impone, e che ora sono scritte**

- Il record e' `tipo: "dossier"` con `"valutazione"` fra i `tag`: la lista dei
  tipi in `kb.py` e' chiusa e un tipo nuovo verrebbe rifiutato. Nessuna modifica
  a `kb.py` ne' a `SCHEMA.md`.
- `layer: "dottrina"` impone `condivisibile: true`. Quindi il record **puo'
  affiorare in un progetto cliente**, ed e' la ragione per cui non contiene mai
  un fair value nudo: il valore sta solo in `fair_value_range`, inseparabile
  dalle ipotesi e dalla data oltre la quale non vale piu'.
- **Un record condivisibile non contiene puntatori a materiale non
  condivisibile**: il record porta il percorso del documento **condiviso**, mai
  quello interno.
- Conseguenza, e regola: **una valutazione si produce sempre in entrambi i
  registri**. Ogni valutazione deve esistere anche in una forma mostrabile a
  terzi — la stessa disciplina del fair value, spostata dal numero al documento.
- Dove si archivia un documento, in generale: `layer mandato` →
  `reports/<soggetto>/<anno>/`, `layer dottrina` → `reports/<categoria>/<anno>/`,
  mai sotto un soggetto.

**File esistenti toccati**

- `metodo-fiduciario/SKILL.md` §0.3 — l'ottava skill nell'elenco e nell'ordine
  d'uso, piu' il blocco del confine: *il lavoro di valutazione puo' cambiare
  quanto ti aspetti e quanto rischio sai di correre, non puo' cambiare i pesi*.
  Il confine con la modalita' B di `analisi-documenti-investimento` e' separato
  **per domanda**, non per oggetto: «quanto vale questa azienda» contro «questo
  strumento serve al mio scopo».
- `README.md`, `marketplace.json`, `plugin.json` — otto skill, non sette. Nella
  riga dello schema della struttura il conteggio e' stato **tolto** invece che
  aggiornato: la tabella completa sta tre righe sopra.
- `06-verdetto-e-linguaggio.md` §2 e §6, `08-manutenzione-e-batch.md`,
  `valutazione-aziende-dcf/SKILL.md` — i due registri, i due record distinti nel
  caso del cliente (la valutazione e' dottrina, la traccia della risposta e'
  mandato: *la valutazione non appartiene a nessuno, la conversazione si'*), e i
  conteggi di controlli tolti dai testi, che ora rimandano all'output delle prove.

**Il canone The Bull: l'episodio 337 entra, ed e' il diciottesimo**

- `canone-the-bull/P3-azionario.md` — sezione nuova **«Valutare una singola
  azienda: il DCF in pratica»** `[TB-337]`: i tre ingredienti del valore, perche'
  la cassa e non l'utile, il FCFF che nel primo anno e' negativo perche' la
  crescita costa, il tasso di sconto come leva che sposta il fair value del 60%
  fra l'8% e il 12%, il valore terminale che pesa l'**83%** dell'enterprise
  value, e il ponte riga per riga fino ai 14,14 dollari per azione.
- La tesi e' andata in un file **pilastro esistente**, non in un file nuovo: il
  paragrafo «Il prezzo = utili futuri scontati» era gia' li', e l'episodio ne e'
  la continuazione operativa. La dottrina piena resta dove e' gia' distillata —
  i nove `references` di `valutazione-aziende-dcf` — perche' il canone si
  distilla una volta sola.
- `canone-the-bull/00-principi-e-mappa.md` — riga d'indice, mappa ai pilastri,
  pie' di pagina di versione a **18 episodi**, e la lacuna della fonte: dei tre
  fair value l'episodio pubblica le ipotesi **solo dello scenario centrale**.
  Bear e bull si citano come misura della dispersione, non si ricostruiscono a
  ritroso dal numero.
- Conflitto **C-M** nel registro: *«math is not an edge»* `[TB-222]` contro il
  costruire un DCF `[TB-337]`. Non e' una smentita, e' la dimostrazione — stessa
  azienda, ipotesi tutte difendibili, **3,93 · 14,14 · 36,27**. Il fattore nove
  non e' il fallimento del metodo, e' il suo risultato. Conseguenza vincolante,
  identica al confine gia' scritto nella skill: l'output puo' cambiare il
  rendimento atteso e la consapevolezza del rischio, **mai un peso di
  portafoglio**. L'anti-timing resta intatto.
- **Nessun principio trasversale nuovo.** Il principio 12 copriva gia' la tesi:
  TB-337 la quantifica, non la estende. Aggiungerne uno avrebbe duplicato.

**Il controllo di salute** (`verifica.py`, che vive fuori da questo repository)

- Gruppo **TEST** nuovo, separato da MOTORI: MOTORI verifica che i sorgenti
  compilino, TEST che si comportino bene. Le prove delle skill vengono eseguite
  davvero, e un motore che compila ma calcola male non passa piu'.
- I sorgenti vengono compilati anche con il **pavimento Python dichiarato**,
  3.11, e non solo con l'interprete piu' recente installato.
- Gruppo **RIPRISTINO** nuovo: i percorsi promessi come vie d'uscita dalla
  procedura anti-disastro devono esistere davvero.
- Regola che governa tutti i gialli: **un controllo che non ha potuto girare non
  e' un controllo superato**, e ogni giallo dice che cosa fare per chiuderlo.
- Il conteggio atteso degli episodi del canone passa a **18** con TB-337. Resta
  un numero scritto a mano di proposito, ed e' l'unica eccezione alla regola dei
  numeri calcolabili: il controllo confronta gia' pie' di pagina e righe di
  tabella fra loro, ma quei due si possono ridurre **insieme**, e allora un
  canone che perde un episodio passerebbe verde. La ragione e' scritta accanto
  alla costante.
- Con questo, **zero gialli**: 53 controlli, 53 verdi, sui tre interpreti.

## 2026-08-05 — due difetti emersi dalle prove sul campo

Nessuno dei due era un guasto: erano due modi in cui il sistema poteva dare una
risposta credibile ma sbagliata, in silenzio. Corretti entrambi.

**«Una casa non e' un intervallo»**

Alla prova del rendimento atteso, il cross-check bottom-up e' stato fatto con
**una sola casa CMA** invece delle cinque canoniche. La risposta lo ha
dichiarato — comportamento corretto — ma il risultato restava incompleto: con
una sola casa non esistono un minimo e un massimo, quindi non esiste l'intervallo
osservato che `metodo-fiduciario` §7 punto 2 prescrive. Esiste un secondo numero
puntuale, che e' un'altra cosa e vale molto meno.

La regola c'era gia': non era imperativa abbastanza nel punto in cui si esegue.

- `rendimenti-attesi-portafoglio/SKILL.md`: nuovo guardrail **«Una casa non e' un
  intervallo»**, con la formula esatta da scrivere nel report quando si usa una
  sola fonte, e il divieto di derivarne gli scenari prudente e ottimista. Due
  voci nuove nell'auto-verifica (7-bis, 7-ter).
- `references/metodologia-bottom-up.md` §2: riquadro che spiega perche' il numero
  di case non e' un dettaglio di completezza.
- `metodo-fiduciario` §7 punto 2: rimando alla regola operativa.

Nessuna soglia inventata, nessuna regola nuova: e' la definizione esistente di
«intervallo osservato», resa impossibile da saltare in silenzio.

**Il registro non si cerca a indovinare**

Sempre alla prova sul campo, non riuscendo a scrivere il record, la risposta ha
nominato un percorso (`/tmp/ciclo`) che non c'entrava niente con il registro
dell'utente. Il comportamento di fondo era corretto — modalita' degradata
dichiarata, record offerto — ma il percorso citato manda la conversazione nel
posto sbagliato.

Causa: `kb.py` ripiegava su `os.getcwd()` quando nessuno diceva dove fosse il
registro, quindi «il registro» diventava qualunque cartella capitasse.

- `kb.py`: `kb_root()` ora **verifica** che la cartella contenga davvero
  `ledger.jsonl`. Se non c'e', si ferma con uscita **2** e spiega i tre modi per
  indicare il percorso, piu' cosa fare quando non c'e' filesystem. `init` resta
  esentato, perche' la struttura la crea lui.
- `kb-registro/SKILL.md`: nuova sezione **«Dov'e' KB_ROOT, e cosa fare quando non
  c'e'»** — ordine di ricerca, divieto di nominare percorsi non verificati,
  formula esatta da usare in modalita' degradata, obbligo di consegnare il record
  nella risposta. Piu' una regola non negoziabile in §Quando si scrive.

Verificato: i sei comandi funzionano invariati sul registro reale, `init` crea la
struttura in una cartella nuova, e una `KB_ROOT` sbagliata ora si ferma invece di
inventare.


## 2026-08-04 — ricostruzione del sistema in versione unica

Il sistema era disperso fra cinque copie, con due file danneggiati e i due
repository su GitHub cancellati. Questa voce registra la ricostruzione.

**Causa accertata del comportamento erratico.** Un `git stash pop` andato male
aveva lasciato i marcatori di conflitto (`<<<<<<<`, `=======`, `>>>>>>>`)
**dentro** `metodo-fiduciario/SKILL.md` (dieci blocchi) e `kb-registro/scripts/kb.py`
(un blocco). Quei file sono stati salvati, pubblicati nel commit `d0111a1` («ver
2.0») e da lì scaricati da Claude: la skill che detta la dottrina conteneva dieci
punti in cui la stessa regola compariva due volte, in due formulazioni diverse.

**Versione scelta.** Tutti i file vengono dal commit locale `8732774`
(«Allineamento skill: metodo-fiduciario v4, snapshot nel registro, motore 1.1»),
che è pulito: zero marcatori. I dieci blocchi di conflitto sono stati aperti e
confrontati lato per lato: la versione pulita contiene sempre il lato più ricco.
Le quattro righe presenti solo nella versione scartata sono formulazioni
precedenti, tutte sostituite da versioni migliori.

**Registro.** `ledger.jsonl` era regredito da 8 a 4 record per una fusione
sbagliata (commit `f2056f4`). Ripristinato a 8 dal commit `d420f82`, compreso il
record `snapshot` del 25/07/2026 con posizioni, totali, aggregati e piano di
accumulo. Viste e `graph.json` rigenerati.

**Correzioni tecniche**

- `analisi-titoli-di-stato-eu/scripts/bond_math.py`: `MOTORE_VERSIONE` era scritto
  **dentro il commento iniziale**, quindi `bond_math.MOTORE_VERSIONE` non esisteva e
  nessun controllo automatico di versione poteva funzionare. Ora è una vera
  variabile di modulo, definita dopo gli import. Il commento rimanda alla costante.
  Nessun numero cambia: i sei vettori d'oro del connettore coincidono tutti.
- Blocco di allineamento del connettore MCP rigenerato. L'impronta dichiarata
  (`59fb45e1…`) non corrispondeva a **nessun** file esistente sul disco: il
  controllo di integrità confrontava con un file fantasma e quindi non poteva
  accorgersi di nulla. Nuova impronta `460195a7…`, verificata coerente col corpo.
- **Aggiunto `.gitignore`** in entrambi i repository. Mancava, e per questo le
  cartelle `__pycache__` con i file `.pyc` erano finite dentro Git: essendo
  binari, Git non sa fonderli e li dichiara in conflitto. Quattro dei sei
  conflitti che hanno bloccato la pubblicazione erano file `.pyc`.
- Rimandi fra skill resi espliciti. Sei riferimenti al canone erano scritti in
  forma abbreviata (`canone-the-bull/...`) e non risolvevano se il file veniva
  letto fuori dal suo contesto: due in `metodo-fiduciario`, quattro in
  `consulenza-portafogli-etf`. Ora tutti e 41 i rimandi relativi risolvono.
- `README.md`: la sezione «Aggiornamento» diceva di alzare `version` nel manifest,
  in contraddizione con la scelta deliberata di **non avere** quel campo. Corretta,
  con la motivazione e il riferimento alla documentazione ufficiale.
- Rimosse le quattro cartelle `__pycache__` e il segnaposto
  `_QUESTA-COPIA-NON-VA-USATA.md`.

**Verificato e invariato**

- rateo del BTP 1,70% 01/09/2051 al 04/08/2026: **0,7207** (patch Actual/Actual
  ICMA presente), YTM lordo 3,941%, duration modificata 18,53
- tutti e sei i vettori d'oro del connettore MCP
- canone The Bull: **17 episodi**, indice coerente con i file, ogni tag citato in
  almeno due file
- `metodo-fiduciario`: §0…§12, checklist di 20 voci, gerarchia a 5 gradini
- nessun campo `version` in `plugin.json` né nella voce di marketplace
- nessun percorso di output cablato, nessun percorso assoluto


## 2026-08-02

**Correzioni**

- `analisi-titoli-di-stato-eu/scripts/bond_math.py`: la copia madre era ferma a
  `MOTORE_VERSIONE 1.0` e senza la patch del rateo Actual/Actual ICMA, mentre la
  copia del connettore MCP era gia' alla 1.1. Le due producevano ratei diversi
  sullo stesso titolo (0,7261 contro 0,7207 su un BTP 1,7% 2051 al 04/08/2026) e
  il controllo di integrita' non se ne accorgeva, perche' l'impronta dichiarata
  nel blocco di allineamento puntava a un terzo file. La 1.1 diventa la copia
  madre; il blocco del connettore e' stato rigenerato con l'impronta corretta.
- `kb-registro/scripts/kb.py`: `stato --soggetto X` scriveva **sempre**
  `STATO-ATTUALE.md`, quindi generare la vista di un soggetto sovrascriveva
  quella del soggetto precedente. Ora scrive `STATO-<soggetto>.md`, la vista
  porta in testa l'ambito, ed e' stato aggiunto `--out`. Un soggetto senza
  record vigenti di livello `mandato` ora **fallisce** invece di produrre una
  vista vuota: una vista vuota, caricata in un progetto, si legge come "nessun
  vincolo attivo".
- `simulazione-montecarlo/scripts/montecarlo.py`: l'assenza di `numpy`
  produceva un `ModuleNotFoundError` nudo. Ora c'e' una guardia con il comando
  di installazione e codice di uscita 3.
- Percorsi di output non piu' cablati su `/mnt/user-data/outputs/`: la cartella
  dipende dall'ambiente (claude.ai, Cowork, Claude Code) e va chiesta una volta.

**Contenuto reintegrato dalle istruzioni di progetto v2**

- `metodo-fiduciario` §0 (nuovo): tre flussi di lavoro con profondita' diversa,
  flusso decisionale standard in otto passi, confine fra le skill.
- `metodo-fiduciario` §1: struttura prima del prodotto; tolleranza al rischio
  incrociata con capacita' e reazione reale.
- `metodo-fiduciario` §5: il canone e' autoritativo ma superabile da una fonte
  migliore; lente difensiva a tassonomia separata.
- `metodo-fiduciario` §6: seconda soglia di ribilanciamento (±10-20% relativo).
- `metodo-fiduciario` §7: range bottom-up osservato, non convenzionale; rimando
  alle tre correzioni della gamba obbligazionaria.
- `metodo-fiduciario` §11: sei voci di checklist recuperate.
- `consulenza-portafogli-etf/references/lente-anticrisi.md` (nuovo).
- `rendimenti-attesi-portafoglio/references/carry-di-copertura.md` (nuovo).

## 2026-08-02 (seconda tornata) — lo snapshot esce dalle istruzioni

**Il problema.** Lo snapshot del portafoglio viveva dentro le istruzioni di
progetto: tabella di posizioni, pesi, controvalori e piano di accumulo. Andava
riscritto a mano a ogni movimento, e nel frattempo invecchiava in silenzio —
un file di istruzioni non ha una data, quindi sembra sempre corrente. Ed era
duplicato in due progetti su quattro, che e' il modo in cui due copie divergono.

**La soluzione.** Lo snapshot diventa un record del registro, e le istruzioni
puntano alla vista generata.

- `kb.py`: nuovo `tipo: "snapshot"` con i campi `posizioni`, `totali`,
  `aggregati`, `piano`. Validazione: ISIN con cifra di controllo, pesi che
  devono chiudere a 1.0 o a 100 (tolleranza 0,5 pt), `classe` time-sensitive
  obbligatoria con `scade`.
- `kb.py`: la vista apre con la sezione **Snapshot del portafoglio** — tabella
  posizioni, totali, aggregati, piano — con la data del record e i giorni
  trascorsi. Oltre i 45 giorni avverte; oltre `scade` marca `SNAPSHOT SCADUTO`.
- **Uno snapshot scaduto NON sparisce dalla vista**, a differenza di ogni altro
  record. Sparendo, la vista direbbe "non ho numeri" invece di "questi numeri
  sono vecchi", e chi legge li ricostruirebbe a memoria: esattamente il
  comportamento che il registro esiste per impedire.
- `kb.py`: i vincoli sono **deduplicati per nome**. Vince la formulazione del
  record piu' recente e si conta quante volte e' stato confermato. Prima il
  sigillo compariva due volte con descrizioni diverse e chi leggeva doveva
  decidere quale valesse.
- `kb.py`: i `numeri` non sono piu' fusi in un dizionario unico e senza data.
  Restano attribuiti al record che li ha prodotti, con la sua data: due misure
  della stessa grandezza a due date diverse si sovrascrivevano in silenzio.
- `kb.py`: nuovo comando **`viste`**, che rigenera la vista globale e una per
  ogni soggetto in un colpo solo. La disciplina che dipende dal ricordarsi due
  comandi diversi non regge tre mesi.
- `metodo-fiduciario` §9 riscritto: la fonte dei numeri e' la vista, con quattro
  comportamenti obbligati (verifica dell'ambito, dichiarazione della data,
  gestione dello scaduto, stop se il file manca).
- `kb-registro`: SKILL.md e SCHEMA.md documentano il tipo snapshot, le
  validazioni e il comportamento alla scadenza.
- Istruzioni di progetto: §4 e §5 del mandato personale, §2 e §3 dei distillati,
  ancoraggio del mandato genitori — sostituiti dal puntatore alla vista.
