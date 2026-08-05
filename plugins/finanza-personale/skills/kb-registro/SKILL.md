---
name: kb-registro
description: "Memoria decisionale trasversale ai progetti di finanza personale. Legge e scrive il registro (ledger) dei report prodotti — action plan, revisioni PAC, distillati, dossier clienti, distillazioni del canone The Bull — tenendo traccia di decisioni vigenti, vincoli attivi con scadenza, trigger aperti e supersessioni. Usala SEMPRE all'apertura di una sessione che tocchi asset allocation, PAC/PIC, o che valuti una fonte, per recuperare cosa era già stato deciso e cosa è ancora vigente; e SEMPRE in chiusura, per registrare il documento appena prodotto. Attivala anche per verificare se una tesi è già stata distillata, per contare i verdetti AZIONE degli ultimi 12 mesi, o per rigenerare STATO-ATTUALE.md."
---

# Registro della knowledge base finanziaria

Questa skill risolve un problema che né i file di progetto né la ricerca semantica risolvono: **ricordare cosa è stato deciso, quando, e se vale ancora**.

Il vincolo di partenza — già scritto nelle istruzioni di progetto dell'utente — è che la ricerca semantica sui file di progetto *recupera per somiglianza e non legge le date*: un forecast depositato viene ripescato come attuale anni dopo. Quindi la KB **non è un archivio di documenti da cercare**: è un **registro di record datati con stato di validità**, e i documenti sono allegati inerti a valle. Si legge il registro, non l'archivio.

## Architettura

```
KB_ROOT/                      ← repo dati, separato dal plugin
├── ledger.jsonl              ← LA fonte di verità: 1 riga JSON per documento
├── STATO-ATTUALE.md          ← vista globale, rigenerata dallo script (mai a mano)
├── STATO-<soggetto>.md       ← una vista per mandato, filtrata e con la sua riga di ambito
└── reports/<soggetto>/<anno>/<file>.html   ← gli artefatti, immutabili
```

- **`ledger.jsonl` è l'unica cosa che si scrive.** Un record ≈ 15 righe: sintesi, non contenuto.
- **La vista del soggetto è l'unica cosa che si legge per prima.** È generata, contiene solo ciò che è **vigente oggi**, e si apre con la sezione **«Snapshot del portafoglio»**: posizioni con ISIN e peso, controvalori, piano di accumulo, tutti datati. È da lì che si prendono i numeri, mai dalle istruzioni di progetto e mai dalla cronologia.
- **Un comando solo per rigenerarle tutte:** `python3 scripts/kb.py viste` scrive la vista globale e una per ogni soggetto con mandato. La disciplina che dipende dal ricordarsi due comandi diversi non regge tre mesi.
- **Gli HTML non si leggono mai per intero all'apertura.** Si apre un report solo quando un record del registro lo indica come rilevante e serve il dettaglio.

### Dov'è `KB_ROOT`, e cosa fare quando non c'è

**`KB_ROOT` non si indovina mai.** È il difetto silenzioso di questa skill: un percorso
plausibile ma sbagliato produce un messaggio d'errore credibile — «non ho potuto scrivere» — che
nasconde il fatto che non si stava nemmeno guardando nel posto giusto. L'utente conclude che il
registro è irraggiungibile, quando magari era solo altrove.

**Ordine di ricerca, in questo ordine e senza saltare passaggi:**

1. La **variabile d'ambiente `KB_ROOT`**, se impostata.
2. Il **percorso passato esplicitamente** con `--kb <percorso>`.
3. Una cartella che contenga davvero un `ledger.jsonl`, **verificata** — non ipotizzata.

**Se nessuno dei tre dà un risultato, sei senza filesystem o senza registro.** È la condizione
normale in chat, sull'app e da telefono, e non è un guasto. In quel caso:

- **Non nominare nessun percorso.** Nessun `/tmp/…`, nessun `~/…`, nessuna cartella «di solito
  sta qui». Un percorso citato che l'utente non riconosce fa perdere tempo a entrambi e sposta
  la conversazione sul posto sbagliato.
- **Dillo con questa formula, o una equivalente**: *«In questa sessione non ho accesso in
  scrittura al registro. Ti passo il record già pronto: salvalo come `record.json` nella
  cartella del sistema, poi `kb.cmd add --file record.json` e doppio clic su
  `AGGIORNA-VISTE.cmd`.»*
- **Consegna il record**, completo e valido, dentro la risposta. Un record che resta nella testa
  di una sessione è un record perso: la sessione finisce, il registro no.
- **Non è un fallimento della consegna**: il documento è stato prodotto, la registrazione è
  rimandata di un passaggio manuale. Va detto una volta, in chiusura, senza scusarsi tre volte.

**In lettura vale la simmetrica**: se la vista non è fra i documenti di progetto, **chiedila e
fermati** — vedi §Quando si legge. L'assenza del file non è assenza di vincoli.

Schema completo dei campi: `references/SCHEMA.md`.

## Due livelli, mai da mescolare — `layer`

| `layer` | Cosa contiene | Chi può leggerlo |
|---|---|---|
| `dottrina` | Principi, distillazioni del canone The Bull, apprendimenti metodologici, letture strutturali durevoli | **Tutti** i progetti, incluso un mandato di terzi |
| `mandato` | Snapshot, posizioni, decisioni, sigilli, PAC di uno specifico soggetto | **Solo** il progetto di quel soggetto |

Regola dura: **un progetto cliente legge `layer=dottrina` + `soggetto=<quel cliente>`, e nient'altro.** Non deve mai vedere le posizioni di Francesco, dei genitori o di un altro cliente. Non è una preferenza di ordine: è separazione di dati di terzi, e il collasso dei due livelli è anche il modo tipico in cui il portafoglio del consulente si replica addosso al cliente.

## Quando si legge (apertura di sessione)

Obbligatorio prima di qualunque lavoro che tocchi allocazione, PAC/PIC, ribilanciamento, o che valuti una fonte:

1. Leggi `STATO-<soggetto>.md` e **verifica la riga di ambito in testa**: deve nominare il soggetto del progetto in cui stai lavorando. Se ne nomina un altro, è il file sbagliato — fermati, non filtrare a mano.
1-bis. Dalla sezione **«Snapshot del portafoglio»** prendi pesi, ISIN e controvalori, e **dichiara la sua data** in apertura del documento. Se è marcato `SNAPSHOT SCADUTO`, dillo e chiedi i numeri correnti prima di quantificare un impatto in euro.
2. Interroga il registro per il tema in questione:
   `python3 scripts/kb.py query --soggetto francesco --tag fattoriale --vigenti`
3. **Prima di scrivere una riga**, dichiara in apertura del documento: quali **vincoli attivi** valgono (con la loro data di scadenza), quali **trigger aperti** esistono, e qual è l'**ultimo record vigente** sullo stesso tema.
4. Se il tema è già stato trattato, apri con *cosa è cambiato rispetto all'ultima volta*. Se una tesi ricompare per la terza volta in pochi mesi, dillo: non è più forte, è più prezzata.

Se non trovi la KB (sessione web o mobile, senza filesystem): la vista dev'essere **caricata fra i documenti di progetto**. Se non c'è, chiedila e **fermati**: non ricostruire pesi e vincoli a memoria. L'assenza del file non è assenza di vincoli, ed è la differenza fra una modalità degradata dichiarata e un errore silenzioso.

## Quando si scrive (chiusura di sessione)

Dopo `present_files`, **prima di chiudere il turno**, appendi il record del documento appena prodotto:

```
python3 scripts/kb.py add --file record.json
```

Regole di scrittura, non negoziabili:

- **Se non puoi scrivere, non fingere di sapere dove.** Niente percorsi ipotizzati: si applica la procedura del §«Dov'è `KB_ROOT`, e cosa fare quando non c'è» — si dichiara la modalità degradata e **si consegna il record nella risposta**.

- **Si registra il record, non il contenuto.** Un forecast deperibile entra come *titolo + verdetto + scadenza*, mai come tesi archiviata. Ciò che è `time-sensitive` **deve** avere `scade`.
- **Un verdetto AZIONE genera sempre almeno un `vincolo` o un `trigger`** con data. Se non riesci a scriverlo con soglia e data, non era un'azione: era un'opinione.
- **Chi supera, dichiara.** Se il nuovo documento sostituisce una decisione precedente, valorizza `supersedes: [id]`; lo script marca il vecchio record `superato`.
- **Se i numeri di portafoglio sono cambiati, si registra uno snapshot nuovo** (`tipo: snapshot`, `supersedes` sul precedente) — non si corregge il vecchio, e non si scrive il nuovo dentro le istruzioni di progetto. Schema e validazioni in `references/SCHEMA.md` §Snapshot.
- **Si chiude con `kb.py viste`**, sempre. Un record scritto e una vista non rigenerata sono una decisione che nessun progetto vedrà.
- **Non riscrivere mai un record esistente** salvo cambio di `stato`/`superato_da`. Il registro è append-only: la storia delle decisioni è il suo valore.
- Dopo l'append, rigenera la vista: `python3 scripts/kb.py stato`.

## Igiene periodica (una volta al mese, prima della revisione PAC)

```
python3 scripts/kb.py scaduti   # record time-sensitive ancora 'vigente' oltre la data di scadenza
python3 scripts/kb.py audit     # conteggio verdetti per classe negli ultimi 12 mesi
```

`audit` implementa la guardia già scritta nelle istruzioni: **se in 12 mesi i verdetti AZIONE sono più di 1-2, l'ipotesi da privilegiare è che il filtro si sia allentato, non che il mondo sia cambiato.** Segnalalo esplicitamente all'utente quando succede — è il tipo di conclusione scomoda che va messa in apertura, non in fondo.

## Cosa questa skill non fa

- Non decide. Fornisce il contesto; la decisione resta al workflow della skill di dominio (`consulenza-portafogli-etf`, `analisi-documenti-investimento`, ...).
- Non archivia fonti esterne. Report sell-side, outlook e articoli restano deperibili: entra il loro **record**, non il loro testo.
- Non sostituisce il canone. Un dato *timeless* che muove la dottrina va nel canone della skill `consulenza-portafogli-etf` via `MANUTENZIONE.md`; nel registro resta solo la traccia che la distillazione è avvenuta (`tipo: canone`).
