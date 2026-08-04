# Costruzione della ladder e cash-flow matching per il decumulo

Come si disegna, si mantiene e si monitora la gamba di titoli di Stato singoli quando la funzione è **preservazione/decumulo** (FASE 4). L'impianto è il *liability-matching portfolio*, non il lazy portfolio.

## Indice
1. Dalle passività alla ladder
2. Bond ladder: costruzione
3. Roll e rischio di reinvestimento
4. Glide-path e riduzione del rischio-prezzo
5. Scenario avverso e cap di perdita
6. Regola di monitoraggio (cosa osservare, cosa ignorare)
7. Tenere a scadenza vs vendere

---

## 1. Dalle passività alla ladder

Ordine di ragionamento (mai invertirlo):
1. **Mappa le passività/bisogni futuri:** spese ricorrenti reali coperte dalle pensioni vs eventuale integrazione dal portafoglio; riserve di sicurezza; eventuali esborsi datati (spese mediche prevedibili, aiuti ai figli, imposte). Distingui i bisogni **certi e datati** (da coprire con flussi certi) da quelli **incerti** (da coprire con riserva liquida).
2. **Traduci i bisogni in flussi target:** importi a date. Questi definiscono **dove** sulla curva servono le scadenze.
3. **Copri i flussi con titoli:** per ogni scadenza, il miglior titolo di Stato white-list disponibile (miglior YTM **netto** a parità di merito/rischio), diversificando per emittente.
4. **Quel che avanza** rispetto ai bisogni datati alimenta la parte di stabilità/riserva (titoli brevi, CCTeu, monetario) e la piccola quota a rischio (azionario, territorio skill ETF).

Il portafoglio insegue le **passività**, non un benchmark: il successo è "ogni flusso arriva quando serve", non "ho battuto l'indice".

## 2. Bond ladder: costruzione

Una **ladder** (scala) distribuisce il capitale su titoli con **scadenze scaglionate** (es. una tranche ogni 1-2 anni). Vantaggi per il decumulo:
- a ogni gradino **scade** un titolo → liquidità disponibile alla data, senza vendere sul mercato (niente rischio-prezzo a scadenza);
- riduce il **rischio di reinvestimento** (non reinvesti tutto a un unico tasso in un unico momento);
- **duration media** governabile scegliendo l'ampiezza della scala;
- diversificazione per **emittente** su ciascun gradino (Italia + core UE), controllando la concentrazione sul rischio-Italia.

Parametri da fissare esplicitamente: numero di gradini, distanza tra scadenze, quota per gradino, mix emittenti per gradino, quota nominale vs inflation-linked (vedi break-even). Documenta ogni scelta con la sua funzione.

## 3. Roll e rischio di reinvestimento

Quando un gradino **scade**, il capitale va **reinvestito** sul gradino più lungo (o dove serve il prossimo flusso). Qui compare il **rischio di reinvestimento**: il nuovo titolo renderà quanto il mercato offre allora, non quanto rendeva il vecchio. In curva scendente reinvesti a meno; in curva salente a più.

- In cash-flow matching il roll segue i **bisogni**, non le previsioni: si reinveste sulla scadenza che copre il prossimo flusso, al miglior netto disponibile.
- La **laddering stessa** è la mitigazione del rischio di reinvestimento (scaglioni → non tutto allo stesso tasso/momento).
- I **CCTeu** (variabili) e il **monetario** assorbono il rischio di reinvestimento di brevissimo, ma non bloccano un rendimento: sono parcheggio, non gamba strutturale.

## 4. Glide-path e riduzione del rischio-prezzo

Per un flusso datato, man mano che la data si avvicina la quota a **rischio-prezzo** scende verso strumenti a scadenza vicina/monetario. Riferimenti (dalla dottrina Missione GOAL della skill ETF, qui applicati ai singoli):
- la **duration residua** di un titolo destinato a un flusso **non deve superare** i mesi/anni che mancano alla data;
- a ridosso della data (indicativamente T-12 mesi) la quota destinata a quel flusso è in **monetario/scadenza brevissima**;
- per l'intera gamba in decumulo, la duration media si **accorcia** nel tempo, coerente con l'orizzonte che si riduce.

## 5. Scenario avverso e cap di perdita

Anche se si tiene a scadenza, un mandato di preservazione ha di norma un **cap di perdita** — il valore è nel mandato e si legge nella vista del registro — che è un vincolo di **mark-to-market** (es. se servisse liquidare, o per tollerabilità psicologica). Costruisci sempre lo scenario avverso combinando:
- **tassi core +100 / +200 bps** (usa `price_shock` con duration e convexity di ciascun titolo, poi aggrega per peso);
- **spread BTP-Bund +150 bps** applicato ai soli titoli italiani (shock idiosincratico Italia);
- effetto sulla quota azionaria (territorio skill ETF, ma il totale va sommato per il cap).

Se il drawdown aggregato in mark-to-market sfonda il cap, **dillo chiaramente** e indica la leva (accorciare duration, ridurre concentrazione Italia, aumentare la quota brevissima/CCTeu). Ricorda che per la parte tenuta a scadenza il drawdown è **potenziale/contabile**, non realizzato: distingui i due piani nell'output.

## 6. Regola di monitoraggio (cosa osservare, cosa ignorare)

Scrivi la regola **prima**, così l'emotività ha meno spazio.

**Da IGNORARE** (rumore per un titolo tenuto a scadenza):
- il **Var %** giornaliero/mensile del book (mark-to-market);
- piccole oscillazioni di prezzo dovute ai tassi entro l'orizzonte.

**Da OSSERVARE** (segnali che richiedono decisione):
- **merito di credito** dell'emittente (rating, spread strutturalmente in ampliamento non ciclico) → rivaluta la concentrazione;
- **avvicinarsi delle scadenze** → prepara il roll e il glide-path;
- **relative value netto** materiale: se uno switch a parità di scadenza/rischio migliora il netto **dopo i costi**, valutalo;
- **variazione dei bisogni** dell'investitore (nuova passività datata, cambio orizzonte) → ridisegna i flussi target;
- **cambi fiscali** (aliquote, white-list) → aggiorna i netti.

Frequenza: revisione **almeno annuale**, più un check a ogni scadenza in arrivo e a ogni nuovo bisogno.

## 7. Tenere a scadenza vs vendere

**Default: tenere a scadenza.** Si vende un titolo prima **solo** per uno di questi motivi, esplicitato:
1. **Ribilanciamento** verso un flusso mancante (serve liquidità a una data non coperta).
2. **Deterioramento del merito di credito** dell'emittente.
3. **Relative value** netto e materiale (uno switch che migliora il netto a parità di scadenza/rischio, **dopo** costi e fiscalità — inclusa l'eventuale minus/plus generata).

**Mai** vendere per reagire al prezzo, per "prendere profitto" sul mark-to-market, o inseguendo una previsione sui tassi. Se emerge la tentazione, riconducila alla regola: la ladder serve i bisogni, non il book.
