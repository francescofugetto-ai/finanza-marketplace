# 00 — Conflitti risolti, confine con la skill ETF, dottrina del cash-flow matching

Entry point dottrinale. Chi usa questa skill legge **prima** questo file: chiarisce perché per questo investitore i bond singoli sono lo strumento corretto (contro la tesi di default di The Bull), dove finisce questa skill e comincia quella ETF, e su quale impianto teorico si costruisce.

## Indice
1. Il conflitto centrale con The Bull (accumulo vs decumulo)
2. Perché l'aritmetica si ribalta in decumulo
3. Registro conflitti risolti (tabella)
4. Confine e handshake con `consulenza-portafogli-etf`
5. Dottrina: cash-flow / liability matching

---

## 1. Il conflitto centrale con The Bull

Il Canone The Bull (`P4-obbligazionario.md` della skill ETF) sostiene, in ottica **accumulo**, che *"investire in ETF obbligazionari è quasi sempre più pratico ed efficiente dei singoli bond"* e che *"i bond singoli scadono quindi sono sicuri"* è **vero ma irrilevante**. Le quattro motivazioni: diversificazione, YTM reinvestito, duration costante gestibile, aritmetica (il "fotogramma vs film").

**Quella tesi è corretta per il suo destinatario** — un accumulatore giovane con orizzonte lungo, il cui obiettivo è massimizzare la ricchezza terminale composta. Per **quel** profilo l'ETF governativo ad accumulazione reinveste le cedole *tax-deferred*, mantiene duration costante da ribilanciare, e la scadenza del singolo titolo è irrilevante perché non c'è una passività da coprire a data fissa.

**Non è il nostro investitore.** Qui il mandato è **preservazione/decumulo**: investitore in età di pensionamento, orizzonte legato all'aspettativa di vita, **tetto di perdita esplicito** (il valore sta nel mandato, non qui), bisogno di flussi noti a date note e di certezza del capitale. Per questo profilo la conclusione di The Bull **non si applica**, e la stessa skill ETF lo riconosce già nella **"Missione GOAL"** di `architettura-5-pilastri.md`, dove scrive testualmente che *"un bond singolo che matura vicino alla data elimina il rischio-prezzo a scadenza … meglio di un ETF obbligazionario che non ha scadenza"* e che *"la fiscalità premia i titoli di Stato white-list (12,5%) rispetto al 26%"*.

**Sintesi:** un portafoglio di preservazione/decumulo **è** una Missione GOAL su scala di portafoglio. Non stiamo contraddicendo The Bull; stiamo applicando la sua stessa eccezione, portandola dal ruolo di nicchia a ruolo strutturale, perché il profilo lo impone.

## 2. Perché l'aritmetica si ribalta in decumulo

The Bull smonta il "tengo a scadenza e riavrò il capitale" con cinque punti. Vediamo perché ognuno **cade o si inverte** per un investitore in preservazione. Da tenere a mente ogni volta che si è tentati di applicare la tesi accumulo.

- **"Il valore reale è eroso dall'inflazione."** Vero, ma vale **identicamente** per l'ETF: nessuno dei due protegge il potere d'acquisto per costruzione. L'erosione reale si affronta a parte — con **BTP€i/BTP Italia** (inflation-linked *singoli*, che a scadenza bloccano i flussi reali, cosa che un IL-ETF non fa) e con la piccola quota azionaria del portafoglio — non pretendendo che l'ETF nominale risolva un problema che non risolve.

- **"Un ETF è fatto di bond, quindi equivalente."** Sul **prezzo** sì; sull'**obiettivo** no. L'investitore in decumulo non vuole un'esposizione duration perpetua e liquida da tradare: vuole che *quel* flusso arrivi a *quella* data. Il singolo lo garantisce (salvo default); l'ETF, che non scade e rolla, no. L'equivalenza di prezzo è irrilevante quando la funzione richiesta è la certezza a scadenza.

- **"Pull to par vale anche dentro l'ETF."** Sì, ma dentro l'ETF il pull-to-par è **continuamente rimescolato dal roll** e catturato in un guadagno tassato al 26% con *pass-through* parziale della quota white-list (base ridotta a 48,08%, dipendente dal reporting del fondo). Sul **singolo white-list** l'utile a scadenza — scarto + plusvalenza — è tassato al **12,5% pieno e certo**, senza TER, senza dipendere dal meccanismo del fondo. Sui titoli comprati **molto sotto la pari** (nel portafoglio: Bund a ~88, BTP a ~93-95) questo è un vantaggio **grande e quantificabile**, non teorico.

- **"Una ladder non scade mai, resti sempre esposto ai tassi."** In accumulo è un difetto (non blocchi nulla). In decumulo è **il punto**: costruisci la ladder in modo che a ogni data serva un flusso, e l'esposizione residua ai tassi la governi tu con il glide-path, non il gestore. La ladder è lo strumento, non l'effetto collaterale.

- **"Lo YTM si realizza solo reinvestendo le cedole, tassate al 12,5%."** Per i bond del mandato — **vita residua breve (2-5 anni) e cedole basse** — l'impatto del reinvestimento sullo YTM è **trascurabile** (lo dicono anche le istruzioni di progetto). E l'investitore in decumulo **vuole** incassare le cedole (sono reddito), non comporle: il "drag da mancato reinvestimento" che penalizza l'accumulatore qui non è un difetto, è la funzione.

**Un punto di The Bull resta valido e va onorato:** la **diversificazione**. Un singolo emittente ha rischio-emittente concentrato (spread BTP 2011: +570 bps). Per questo la skill non fa "tutto BTP": diversifica per emittente white-list (Italia + Germania + altri core UE), controlla la concentrazione sul rischio-Italia, e non spinge mai su un singolo nome oltre quanto il cap di perdita tolleri in uno shock di spread. La diversificazione qui si ottiene **tra** titoli di Stato, non rinunciando ai titoli di Stato.

## 3. Registro conflitti risolti

| # | Tesi The Bull (accumulo) | Decisione di questa skill (decumulo) | Perché |
|---|---|---|---|
| C-1 | ETF obbligazionario > bond singoli quasi sempre | **Bond singolo white-list a scadenza** è lo strumento core della gamba difensiva | Serve certezza di flusso/capitale a date note + cap di perdita; è la "Missione GOAL" su scala di portafoglio |
| C-2 | La scadenza del singolo è "vera ma irrilevante" | La scadenza è **il criterio di selezione** | In cash-flow matching la data è il vincolo primario, non un dettaglio |
| C-3 | Il 12,5% sulle cedole è un drag vs l'ETF acc. tax-deferred | Il **12,5% pieno e certo** su cedole *e* scarto/plus è un **vantaggio** vs il 26% con pass-through parziale dell'ETF | L'investitore incassa le cedole (non le compone); l'utile a scadenza sui titoli sotto la pari è grande e a bassa tassazione |
| C-4 | Duration costante dell'ETF è un pregio (ribilanci) | Duration **decrescente e controllata** del singolo è un pregio | In decumulo si vuole ridurre il rischio-prezzo avvicinandosi alle date, non mantenerlo costante |
| C-5 | Reinvestire le cedole è essenziale | Non è essenziale per questo profilo | Cedole basse + vita breve → impatto trascurabile; e le cedole servono da reddito |

Se in futuro emerge un nuovo conflitto, aggiungilo qui con lo stesso schema (tesi / decisione / perché), così la logica resta tracciabile.

## 4. Confine e handshake con `consulenza-portafogli-etf`

Due skill, responsabilità singola ciascuna. Non duplicare, non invadere.

**Possiede questa skill (`analisi-titoli-di-stato-eu`):**
- analisi, selezione, confronto e monitoraggio dei **titoli di Stato singoli** area euro;
- YTM netto/reale, duration/convexity, carry, roll-down, scarto, rateo;
- lettura della **curva** e dello **spread BTP-Bund**, lettura dei report sui governativi;
- costruzione e roll della **bond ladder** / cash-flow matching;
- confronto **bond singolo vs ETF governativo** (a parità di netto) — come *analisi*, non come raccomandazione dell'ETF.

**Possiede la skill ETF (`consulenza-portafogli-etf`):**
- gamba **azionaria** (selezione ETF, overlap, look-through) e **monetaria** (XEON come cash/P2);
- **asset allocation complessiva** e sua revisione;
- profilazione (questa skill **consuma** il profilo, non lo rifà);
- disciplina comportamentale e regole di ribilanciamento d'insieme.

**Oggetti di confine (handshake esplicito):**
- **Monetario (XEON):** è territorio della skill ETF (cash/P2). Questa skill lo tratta solo come *leg di parcheggio/reinvestimento* della ladder. Se rileva che una **grande quota monetaria a 26%** potrebbe diventare più efficiente con **CCTeu/BOT/BTP brevi white-list a 12,5%**, lo **segnala** come tema di allocazione da decidere al livello di progetto — non lo decide da sola.
- **Inflation-linked singoli (BTP€i/BTP Italia):** sono titoli di Stato singoli → **analisi e selezione** stanno qui. **Quanto** IL tenere nel portafoglio è una decisione di allocazione condivisa: usa la dottrina IL del canone (`P4-obbligazionario.md`, soglia utile ≥5-10%, 1/3-1/2 della gamba) ma applicala a titoli *singoli tenuti a scadenza*.
- **Quota totale obbligazionaria e sua funzione (stabilità vs goal):** decisione d'insieme → skill ETF/progetto. **Come** implementarla in titoli specifici → qui.

Regola pratica: se la domanda è *"quanto/quale asset class"*, è allocazione (ETF/progetto). Se è *"quale titolo, a quale prezzo netto, con quale scadenza e rischio"*, è questa skill.

## 5. Dottrina: cash-flow / liability matching

L'impianto teorico non è "lazy portfolio", è **matching di passività** (Bernstein: *liability-matching portfolio*; Haghani; la letteratura su bond ladder e decumulo). Principi operativi:

1. **Prima le passività, poi gli asset.** Mappa i bisogni futuri (spese ricorrenti reali, riserve, eventuali esborsi datati). Poi costruisci flussi di titoli che li coprano per data e importo. Il portafoglio "insegue" le passività, non un benchmark.
2. **La scadenza è il vincolo primario.** Si sceglie prima *dove* sulla curva serve il flusso, poi il titolo migliore su quella scadenza (miglior YTM netto a parità di merito/rischio, preferendo white-list per il 12,5%).
3. **Duration = orizzonte, non scommessa.** La duration della gamba non è una vista sui tassi: è il riflesso di *quando* servono i soldi. Allungarla per "prendere più YTM" è market timing travestito.
4. **Diversificazione tra emittenti white-list**, con controllo esplicito della concentrazione sul rischio-Italia (spread). Il singolo emittente non deve poter sfondare il cap di perdita in uno shock di spread.
5. **Held-to-maturity di default; vendita solo per motivo.** Si vende un titolo prima della scadenza solo per: (a) ribilanciamento verso un flusso mancante, (b) deterioramento del merito di credito, (c) relative value netto e materiale (uno switch che migliora il netto a parità di scadenza/rischio, dopo i costi). Mai per reagire al prezzo.
6. **Reale prima di nominale.** L'obiettivo è preservare il potere d'acquisto: i BTP€i/BTP Italia e la quota azionaria coprono l'inflazione; i nominali danno certezza e reddito. Il rendimento si giudica **netto e reale**.
