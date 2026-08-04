# Changelog — finanza-personale

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
