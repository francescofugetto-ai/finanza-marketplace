# Protocollo di verifica ISIN — tolleranza zero

Un ISIN sbagliato = un titolo sbagliato = una raccomandazione sbagliata. In passato un errore di scadenza è stato intercettato dall'utente: la soglia di tolleranza qui è **zero**. Questa procedura viene **prima** di qualsiasi calcolo o raccomandazione (FASE 1).

## Principio

Non riportare **mai** un ISIN a memoria. Gli ISIN non si "ricordano": si **verificano** su fonti autoritative, incrociandone almeno due, prima di usarli. Se non si raggiunge la certezza, si **dichiara** e non si procede con quel titolo.

## Due percorsi, secondo l'ambiente

Il protocollo è lo stesso; cambia chi lo esegue.

**Percorso A — connettore `finanza` disponibile** (il tool `stato_connettore` risponde). È la via preferita.

1. `decodifica_sigla_broker` sulla sigla del broker: restituisce la lettura e **tutti** i candidati compatibili, mai un ISIN dedotto. Se i candidati sono più d'uno, fatti confermare quale.
2. `verifica_isin` su ogni ISIN: incrocia il registro ESMA FIRDS e l'elenco Banca d'Italia, e restituisce ogni campo con fonte, data e stato.
3. Leggi lo **stato**: `verificato` (due fonti concordi) → procedi; `singola_fonte` → usabile ma **non** verificato, dichiaralo; `discordante` → **fermati**, non scegliere quale fonte credere.
4. Restano comunque a carico tuo, perché il connettore non li fornisce: **prezzo secco** (dal book, al momento dell'ordine), **data ultimo stacco**, **lotto minimo e negoziabilità sul broker**.

**Percorso B — connettore assente** (sessione da web o telefono). Vale la procedura manuale descritta qui sotto. Ogni dato così ottenuto si marca **`[verifica libera]`**, l'esito è una **nota di lavoro** e non un report, non se ne ricava alcuna raccomandazione operativa, e si chiude con l'elenco degli ISIN da ricontrollare al primo accesso al connettore.

## Fonti autoritative (incrociarne ≥2) — percorso B

- **Borsa Italiana** (borsaitaliana.it) — scheda del titolo su MOT/EuroTLX: ISIN, cedola, scadenza, prezzo, lotto minimo.
- **btpfacile.it** — schede BTP con cedola, scadenza, ISIN, prezzo, rendimento indicativo.
- **oltrerisparmio.com** — schede e liste titoli di Stato.
- **MOT / EuroTLX** (Borsa Italiana) — mercato di negoziazione, dati ufficiali.
- Per emittenti esteri: sito del **Tesoro** emittente / **Bloomberg/justETF** per l'anagrafica, e la scheda del broker.
- **KID/prospetto** e la **scheda del broker (Fineco)** per lotto minimo, negoziabilità, mercato.

Se una fonte non è raggiungibile o i dati non collimano tra le due fonti, **fermati**: non "scegliere" quale credere. Segnala la discrepanza all'utente.

## Decodifica delle sigle abbreviate del broker

Fineco (e altri) mostrano nomi sintetici, non l'ISIN. Vanno **decodificati e poi verificati**, mai assunti.

**Schema tipico:** `EMITTENTE-GGMMMAA CEDOLA`
- `GG` = giorno, `MMM` = mese (IT: GE FB MZ AP MG GN LU AG SE OT NO DC), `AA` = anno di **scadenza**.
- `CEDOLA` = tasso cedolare annuo nominale in %.

**Esempi (da decodificare e POI verificare l'ISIN — non assumere):**

| Sigla broker | Lettura | Da verificare |
|---|---|---|
| `BTP-15MZ28 0,25` | BTP, scad. **15 marzo 2028**, cedola **0,25%** | ISIN, stacco cedola, lotto |
| `BTP-1AP30 1,35` | BTP, scad. **1 aprile 2030**, cedola **1,35%** | ISIN, stacco cedola, lotto |
| `SPAIN-31MZ29 2,35` | Bonos Spagna, scad. **~31 marzo 2029**, cedola **2,35%** | ISIN, giorno esatto, white-list |
| `GERMANY-15FB31 0` | Bund, scad. **15 febbraio 2031**, cedola **0%** | ISIN, tipo (Bund/Bobl), white-list |

Attenzione: il **giorno** può differire (28/29/30/31 a fine mese); la sigla è indicativa, la scheda ufficiale è autoritativa.

## Dati minimi da estrarre e confermare per ogni titolo

Prima di passare alla FASE 2 (metriche), avere **verificati**:
1. **ISIN** (incrociato ≥2 fonti).
2. **Emittente** e **white-list** sì/no (per l'aliquota 12,5% vs 26%).
3. **Scadenza** (data esatta).
4. **Cedola** annua e **frequenza** (BTP/Bund/OAT/Bonos: semestrale; BOT: zero-coupon; CCTeu: variabile).
5. **Data ultimo stacco** cedola (serve per il rateo).
6. **Prezzo** secco corrente (e **prezzo di carico** se è un titolo già in portafoglio, per la fiscalità).
7. **Lotto minimo** e **mercato** (MOT/EuroTLX) e **negoziabilità sul broker**.
8. Per gli **indicizzati** (BTP€i/BTP Italia): indice di riferimento (HICP ex-tabacco / FOI), coefficiente d'indicizzazione corrente.

## Trappole comuni

- **Titoli omonimi con scadenze vicine:** stesso emittente, cedole simili, scadenze a mesi di distanza → ISIN diversi. Verifica **sempre** scadenza *e* cedola *insieme*, non una sola.
- **Nominale vs indicizzato:** un BTP nominale e un BTP€i possono avere descrizioni simili ma fiscalità/comportamento diversi. Controlla il tipo.
- **Bund vs Bobl vs Schatz:** scadenze/segmenti diversi del governativo tedesco; verifica il tipo, non solo "Germany".
- **Giorno di scadenza** copiato male dalla sigla (fine mese).
- **Prezzo tel-quel vs secco:** assicurati di sapere quale prezzo stai leggendo (il book può mostrare l'uno o l'altro); per lo YTM serve il **secco + rateo**.
- **CCTeu trattato come tasso fisso:** è variabile, non ha uno YTM fisso ex-ante.

## Cosa scrivere nell'output

Nella tabella titoli riporta **ISIN + fonte/e di verifica**, la data della verifica e il **percorso** usato (connettore / verifica libera). Se un dato non è stato verificabile, marcalo esplicitamente come **"da verificare"** e non costruirci sopra una raccomandazione operativa.
