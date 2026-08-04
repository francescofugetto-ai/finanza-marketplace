# Canone The Bull — Protocollo di manutenzione e aggiornamento

> Scopo: mantenere il canone **vivo**. Le viste di The Bull evolvono nel tempo (es. l'oro da rifugio a high-beta; la posizione di Coletti sui bond; il target del fattoriale che sale verso 1/3). Questo protocollo dice **come integrare nuovo materiale senza rompere la coerenza e senza perdere la tracciabilità**.

> **Canone condiviso — si distilla una volta, serve tutti.** Questo canone è un'unica fonte usata da più progetti Claude (consulenza a terzi e portafoglio personale del titolare). Ogni episodio si distilla **una sola volta, qui nella skill**, e da quel momento serve automaticamente tutti i progetti: **non** duplicare il canone dentro i singoli progetti né distillare lo stesso episodio due volte.

## Principio guida: timeless vs time-sensitive

Ogni tesi del canone è di due tipi. Distinguerli è la cosa più importante della manutenzione.

- **TIMELESS** — meccanismi e principi che non scadono col contesto. Es.: Δprezzo ≈ −Δtassi × duration; il fotogramma-vs-film; le tre motivazioni della diversificazione; reverse budgeting; l'aritmetica del pull-to-par; i 5 criteri di Swedroe; volatility drag. → Si aggiornano **solo** se The Bull cambia il *ragionamento*, non i numeri.
- **TIME-SENSITIVE** — viste legate al regime/momento. Es.: "oro high-beta", price target $10k, livello dei tassi, composizioni geografiche degli indici fattoriali, valutazioni settoriali, "3% is the new 2%", i pesi specifici dei tre portafogli modello, i tickers/TER. → **Scadono**. Vanno rinfrescati e, se superati, marcati come superati con data.

Ogni file riporta in fondo un blocco `time-sensitive` con gli elementi deperibili.

## Quando esce nuovo materiale da The Bull (episodio, newsletter, libro)

Procedura in 6 passi:

1. **Estrai i datapoint che muovono una decisione** (non riassumere l'episodio): tesi nuove, revisioni di tesi vecchie, nuovi strumenti/tickers, nuovi numeri rilevanti. Scarta sponsor, aneddoti, divagazioni.
2. **Assegna un tag** `[TB-NNN]` con il numero d'episodio (o titolo se il numero manca) e **aggiungi la riga all'indice** in `00-principi-e-mappa.md`.
3. **Individua il file pilastro** di destinazione (P3/P4/P5a/P5b/asset-allocation) e **aggiungi la tesi** nel paragrafo pertinente, taggata.
4. **Se la tesi CONTRADDICE una tesi esistente**: non sovrascrivere in silenzio. Marca la vecchia come superata e spiega:
   ```
   ~~[vecchia tesi]~~ → **SUPERATA [TB-NNN, data]**: [nuova tesi e motivo del cambiamento].
   ```
   Mantiene l'**audit trail**: serve a capire *perché* la vista è cambiata (es. l'oro: "diversificatore" → "high-beta dal regime post-Jackson-Hole ago-2025"). Una vista che evolve è informazione, non rumore.
5. **Se è una tesi time-sensitive nuova** che invecchierà (un target, un livello di tassi, una composizione indice): aggiungila al blocco `time-sensitive` del file con la **data**, così alla revisione successiva si sa cosa ricontrollare.
6. **Aggiorna l'header di versione** in fondo a `00-principi-e-mappa.md` (data + lista episodi incorporati + lacune note) e al file toccato.

## Gestione dei conflitti

- I conflitti **interni al canone** (tesi che sembrano confliggere ma convivono) vanno nel **registro conflitti** di `00-principi-e-mappa.md` (sezione "Registro dei conflitti risolti"), con la risoluzione e i tag.
- I conflitti tra **canone The Bull e altre fonti** (paper accademici, BlackRock, Morningstar, ecc.): prevale il **ragionamento più solido e aggiornato**, non l'autorità del podcast per partito preso. La skill resta un consulente indipendente: The Bull è la *base dottrinale di riferimento*, non un vangelo. Se una fonte più recente o più rigorosa smentisce una tesi The Bull, segnalalo esplicitamente all'utente (che è un fan: va trattato il disaccordo con rispetto e dati, non con deferenza né con derisione).

## Esempio svolto: integrazione dell'azionario (lacuna chiusa)

`P3-azionario.md` era inizialmente **incompleto** (file `Azioni.docx` ricevuto a 0 byte). Al ricaricamento è stato integrato **applicando questo stesso protocollo** — vale come esempio di riferimento:
1. Estratta la dottrina azionaria piena dai 4 episodi (`[TB-222]` valore/sconto flussi, `[TB-241]` prezzi-vs-tassi/Gordon, `[TB-288]` aziende-smart-money/buyback, `[TB-313]` mercati emergenti).
2. **Riscritto** `P3-azionario.md` rimuovendo l'avviso ⚠️ e sostituendo i contenuti "ricostruiti" con quelli reali taggati per episodio.
3. **Aggiornati** indice episodi, mappa pilastri e footer di versione in `00-principi-e-mappa.md`; aggiunto il **principio trasversale 12** (investimento vs speculativo) emerso da `[TB-241]`; tolti i marker "incompleto" dalla `SKILL.md`.
4. Auto-verifica (rimandi, copertura concetti, tag) prima della consegna.

Stesso flusso da seguire per qualunque nuovo episodio o lacuna futura.

## Igiene generale

- **Mai inventare un dato** per riempire un buco: se manca, marcalo come mancante (come per l'azionario). Coerente con i guardrail della `SKILL.md`.
- **Verifica live** i dati deperibili (tickers, TER, rendimenti, tassi) al momento dell'uso: il canone dà il *razionale e la struttura*, non i numeri correnti.
- Mantieni i file **densi e senza fronzoli**: sono reference operativi, non trascrizioni. Niente sponsor, niente aneddoti.

<!-- VERSIONE FILE -->
**Stato:** protocollo attivo. Ultima modifica: aggiunta nota "Canone condiviso" (distillazione unica multi-progetto).
