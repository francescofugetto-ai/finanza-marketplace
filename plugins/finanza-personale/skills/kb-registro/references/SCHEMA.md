# Schema del registro (`ledger.jsonl`)

Un record per riga, JSON valido, UTF-8. Append-only. Ordine di scrittura irrilevante: lo script ordina per data.

## Campi

| Campo | Tipo | Obbl. | Note |
|---|---|---|---|
| `id` | string | ✔ | `AAAA-MM-GG-slug`, univoco. Es. `2026-07-13-vmq-action-plan` |
| `data` | `AAAA-MM-GG` | ✔ | Data del documento, non di registrazione |
| `layer` | `dottrina` \| `mandato` | ✔ | Regola di visibilità (vedi SKILL.md) |
| `soggetto` | string | ✔ | `francesco` \| `genitori` \| `cliente:rossi` \| `-` (per `layer=dottrina`) |
| `tipo` | enum | ✔ | `action-plan` \| `revisione-pac` \| `distillato` \| `dossier` \| `canone` \| `nota` \| `snapshot` |
| `titolo` | string | ✔ | Una riga, leggibile |
| `file` | path \| null | ✔ | Relativo a `KB_ROOT`. `null` se il documento non è stato conservato |
| `verdetto` | enum \| null | ✔ | `AZIONE` \| `OSSERVATO` \| `CONTESTO` \| `RUMORE` **solo per i `tipo: distillato`**, cioe quando il documento giudica una fonte esterna. Per i documenti prodotti in proprio — `dossier`, `revisione-pac`, `action-plan`, `canone`, `nota` — vale sempre `null`: `kb audit` conta i verdetti per misurare se il filtro segnale/rumore si sta allentando, e mescolarci i documenti propri sporca il conteggio. **`OSSERVATO` richiede sempre almeno un `trigger`** con `cosa`, `soglia`, `fonte` e `riverifica`: osservare senza sapere cosa guardare non e un verdetto, e un modo elegante di non decidere |
| `decisione` | string | ✔ | **Una riga.** Cosa è stato deciso, in imperativo. Se nulla: `"nessuna azione"` |
| `classe` | `timeless` \| `time-sensitive` | ✔ | Determina se `scade` è obbligatorio |
| `scade` | `AAAA-MM-GG` \| null | ✔ | Obbligatorio se `classe=time-sensitive`. Oltre questa data il record non entra più in `STATO-ATTUALE.md` |
| `stato` | `vigente` \| `superato` \| `scaduto` \| `archiviato` | ✔ | Gestito dallo script per `superato`/`scaduto` |
| `supersedes` | string[] | | `id` dei record che questo documento sostituisce |
| `superato_da` | string \| null | | Valorizzato dallo script |
| `vincoli` | oggetto[] | | `{nome, descrizione, scade}` — sigilli, pause, divieti con data |
| `trigger` | oggetto[] | | `{cosa, soglia, fonte, riverifica}` — falsificabili, mai vaghi |
| `tag` | string[] | ✔ | Minuscolo, kebab-case. Es. `["fattoriale","pac","vmq"]` |
| `numeri` | oggetto | | Coppie chiave/valore utili al confronto nel tempo. Es. `{"peso_usa": 0.486, "peso_vmq": 0.162}` |
| `posizioni` | oggetto[] | | **Solo `tipo=snapshot`.** `{gamba, isin, ticker, quote, valore_eur, peso}`. Vedi §Snapshot |
| `totali` | oggetto | | `{valore_mercato_eur, carico_eur, pl_eur, pl_pct}` |
| `aggregati` | oggetto | | Sintesi per blocco. Es. `{"sleeve_vmq_pct": 16.2, "target_sleeve_vmq_pct": 33.0}` |
| `piano` | oggetto | | `{importo_mensile_eur, giorno, righe:[{gamba,isin,quote,importo_eur}], note}` |
| `condivisibile` | bool | ✔ | `true` solo se il contenuto può informare il mandato di un terzo. Per `layer=mandato` è quasi sempre `false` |

## Regole di validazione (applicate da `kb.py add`)

1. `id` univoco; `data` e `scade` in formato ISO.
2. `classe=time-sensitive` ⇒ `scade` non nullo.
3. `verdetto=AZIONE` ⇒ almeno un elemento in `vincoli` **o** in `trigger`.
4. `layer=dottrina` ⇒ `condivisibile=true`; `layer=mandato` con `condivisibile=true` richiede conferma esplicita.
5. `supersedes` deve puntare a `id` esistenti; lo script li marca `superato` e valorizza il loro `superato_da`.
6. `decisione` su una sola riga: se contiene un ritorno a capo, l'append fallisce. È un vincolo di progetto: se la decisione non sta in una riga, non è ancora una decisione.

## Esempio

```json
{"id":"2026-03-10-tilt-fattoriale-decisione","data":"2026-03-10","layer":"mandato","soggetto":"titolare","tipo":"action-plan","titolo":"Decisione sul tilt fattoriale: portarlo sopra soglia o eliminarlo","file":"reports/titolare/2026/action_plan_tilt_10032026.html","verdetto":null,"decisione":"Tilt fattoriale portato a target 33% dell'azionario; convergenza solo via flussi, mai via vendite","classe":"timeless","scade":null,"stato":"vigente","supersedes":[],"superato_da":null,"vincoli":[{"nome":"sigillo-comportamentale","descrizione":"Nessuna rivalutazione della scelta fattoriale; alla review si traccia solo la convergenza verso il target, mai la performance relativa","scade":"2027-03-10"},{"nome":"pausa-flussi-core","descrizione":"Gamba core esclusa dal piano di accumulo finche il suo peso non rientra sotto la soglia stabilita","scade":null}],"trigger":[{"cosa":"Fatto strutturale sugli strumenti: metodologia dell'indice, TER, passaggio a replica sintetica, fusione o liquidazione, regime fiscale del domicilio","soglia":"qualunque variazione documentata dall'emittente","fonte":"KID/prospetto dell'emittente","riverifica":"2027-03-10"}],"tag":["fattoriale","piano-accumulo","sigillo"],"numeri":{"peso_core":0.486,"peso_fattoriale":0.162,"target_fattoriale":0.33},"condivisibile":false}
```
> Nota: l'esempio ha `verdetto: null` pur essendo un `AZIONE` nel merito. Il campo
> `verdetto` giudica **fonti esterne** e resta nullo sui documenti prodotti in proprio;
> cio che rende vincolante un action plan sono i `vincoli` e i `trigger`, non il verdetto.

---

## Snapshot del portafoglio — `tipo: snapshot`

Lo snapshot è **un record come gli altri**, non un blocco di testo dentro le istruzioni di progetto. La differenza non è di forma: un blocco nelle istruzioni va riscritto a mano a ogni movimento e nel frattempo **invecchia in silenzio**, perché un file di istruzioni non ha una data e sembra sempre corrente. Un record ha la sua data, si chiude con `supersedes` invece di essere sovrascritto, e la vista lo rende dichiarando quanti giorni ha.

### Campi

```json
{
  "id": "AAAA-MM-GG-snapshot-<soggetto>",
  "tipo": "snapshot",
  "classe": "time-sensitive",
  "scade": "AAAA-MM-GG",
  "posizioni": [
    {"gamba": "MSCI World ex USA", "isin": "IE0006WW1TQ4", "ticker": "EXUS",
     "quote": 576, "valore_eur": 22861.44, "peso": 0.235557}
  ],
  "totali":   {"valore_mercato_eur": 97052.27, "carico_eur": 92895.82,
               "pl_eur": 4156.45, "pl_pct": 4.47},
  "aggregati":{"sleeve_vmq_pct": 16.2, "target_sleeve_vmq_pct": 33.0},
  "piano":    {"importo_mensile_eur": 1721.46, "giorno": "15 del mese",
               "righe": [{"gamba": "...", "isin": "...", "quote": 12, "importo_eur": 476}],
               "note": "una riga su cosa è escluso dal piano e perché"}
}
```

### Validazioni specifiche

1. **`posizioni` obbligatorio** se `tipo=snapshot`, e viceversa: un record con posizioni deve dichiararsi snapshot.
2. **Ogni ISIN passa il controllo di formato e cifra di controllo.** Un ISIN trascritto male viene fermato qui, prima di entrare in una vista e da lì in una raccomandazione.
3. **I pesi devono chiudere** a `1.0` (frazioni) o a `100` (percentuali), tolleranza 0,5 punti. Un portafoglio che somma a 0,93 non è un portafoglio: è una tabella con una riga dimenticata.
4. **`classe` deve essere `time-sensitive` con `scade`**: la data oltre cui va richiesto un aggiornamento.

### Comportamento alla scadenza — diverso dagli altri record

Un record scaduto esce dalla vista. **Uno snapshot no.** Resta, con un avviso `SNAPSHOT SCADUTO` in evidenza e l'invito a chiedere i numeri correnti prima di quantificare.

La ragione: sparendo, la vista non direbbe *«questi numeri sono vecchi»* ma *«non ho numeri»*, e chi legge ricostruirebbe i pesi a memoria — cioè esattamente il comportamento che il registro esiste per impedire. Un dato vecchio e dichiarato tale è utilizzabile con cautela; un buco invita a riempirlo.

### Aggiornamento

Non si modifica il record esistente. Se ne scrive uno nuovo con `supersedes: ["<id del precedente>"]`, poi si rigenerano le viste. Lo snapshot vecchio resta nel registro come storia, con `stato: superato`.

```
python3 scripts/kb.py add --file snapshot-nuovo.json
python3 scripts/kb.py viste
```
