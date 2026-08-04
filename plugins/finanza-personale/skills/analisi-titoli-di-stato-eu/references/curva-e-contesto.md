# Curva dei rendimenti, contesto macro e lettura dei report

Come inquadrare il regime dei tassi, leggere la curva e lo spread BTP-Bund, e usare un report sui governativi — **per scegliere il punto della curva su cui comprare e per spiegare il regime, non per fare market timing** (FASE 3).

## Indice
1. Precisazione terminologica (backwardation ≠ inversione)
2. Forma della curva e cosa dice
3. Steepening / flattening / twist
4. Roll-down sulla curva (ripresa)
5. Term premium e "bond vigilantes"
6. Spread BTP-Bund (rischio-Italia)
7. Break-even inflation
8. Come leggere un monitor sui governativi e le pagine fixed income di JP Morgan
9. La linea macro/timing

---

## 1. Precisazione terminologica (importante per il rigore)

*Backwardation* e *contango* descrivono, a rigore, la struttura a termine dei **futures** (prezzo spot vs prezzo a termine di una commodity o di un futures su tasso): **contango** = a termine più caro dello spot; **backwardation** = a termine più a buon mercato. **Non** sono i termini corretti per la **curva dei rendimenti** dei titoli di Stato.

Per la curva dei rendimenti il vocabolario preciso è:
- **Curva normale / inclinata positivamente:** rendimenti crescenti con la scadenza.
- **Curva piatta:** rendimenti simili su tutte le scadenze.
- **Curva invertita / inclinata negativamente:** rendimenti a breve **maggiori** di quelli a lunga (spesso segnale di attese di taglio/recessione).
- **Curva a gobba (humped):** massimo su scadenze intermedie.

Quando l'utente dice "backwardation" riferendosi ai bond, intende quasi sempre **curva invertita** e/o l'assenza di **roll-down** positivo. Usa i termini corretti (inversione, roll-down, carry) e, se utile, esplicita la mappatura una volta.

## 2. Forma della curva e cosa dice

La curva lega rendimento e scadenza degli **stessi** emittenti (es. curva BTP, curva Bund). Riflette: attese sui tassi ufficiali (breve), attese d'inflazione e crescita (medio-lungo), e **term premium** (compenso per l'incertezza a lunga). Serve a:
- capire **dove** il mercato paga di più per unità di duration;
- valutare il **roll-down** atteso di un acquisto;
- contestualizzare le aspettative (non a decidere il timing).

## 3. Steepening / flattening / twist

- **Steepening** (curva che si irripidisce): il tratto lungo sale più del breve (bear steepening) o il breve scende più del lungo (bull steepening).
- **Flattening** (curva che si appiattisce): breve sale (bear flattening, tipico dei rialzi BCE) o lungo scende (bull flattening).
- **Twist:** rotazione della curva. Rilevante per una ladder perché cambia il valore relativo dei diversi tratti.

Per un mandato di cash-flow matching questi movimenti **non** sono segnali di trading: informano *dove* conviene piazzare i nuovi acquisti a parità di orizzonte del flusso, e come si comporterà il mark-to-market della ladder (che si ignora se si tiene a scadenza, salvo il cap di perdita).

## 4. Roll-down sulla curva (ripresa da metriche)

Su **curva positiva**, un titolo invecchiando "scivola" verso scadenze a rendimento più basso → **guadagno di prezzo** (roll-down positivo), che si somma al **carry** (cedola/rateo). Su **curva piatta** roll-down ~0; su **curva invertita** roll-down **negativo**. Il criterio per scegliere il punto d'acquisto è il **carry+roll netto per unità di duration/rischio**, mai l'allungamento della scadenza oltre il bisogno del flusso.

## 5. Term premium e "bond vigilantes"

- Il **breve** è ancorato alle attese sui tassi ufficiali (BCE/Fed).
- Il **lungo** è guidato anche dai **"bond vigilantes"** (Yardeni): il mercato può alzare i rendimenti a lunga se teme inflazione, deficit o offerta netta elevata, **anche dopo** un taglio della banca centrale. I prezzi sono **forward-looking**: si muovono sulle *aspettative*, non sull'intervento effettivo.
- **Fiscal dominance / debasement:** in regime di alti debiti/deficit, la parte lunga incorpora un term premium più alto. Rilevante per decidere quanto allungare la ladder (in genere: non oltre l'orizzonte del flusso).

## 6. Spread BTP-Bund (rischio-Italia)

È la differenza di rendimento tra BTP e Bund di pari scadenza (di norma il decennale): misura il **rischio-emittente Italia** percepito dal mercato. Storia utile da ricordare (non come previsione): 2011 spread oltre +570 bps; tensioni ricorrenti 2018. **Uno spread che si allarga fa scendere i BTP anche se i tassi "core" (Bund) sono fermi.**

Implicazioni operative:
- Il rischio-Italia va **modellato a parte** negli scenari: un titolo tutto-BTP può violare il cap di perdita in uno shock di spread anche senza rialzo dei tassi core. In un portafoglio di preservazione la presenza di **Bund** e **Bonos** accanto ai BTP è diversificazione di rischio-emittente, non decorazione.
- Non "scommettere" sullo spread (long/short Italia): la funzione è certezza del flusso, non il carry sul rischio-paese.

## 7. Break-even inflation

Livello d'inflazione che rende equivalente un nominale e un inflation-linked di pari scadenza: `break-even ≈ rendimento nominale − rendimento reale`. Se l'inflazione **realizzata** supera il break-even, conveniva l'IL; sotto, il nominale. Un IL è "meglio" **solo** se l'inflazione *ex post* supera quella *già prezzata*, non se l'inflazione è "alta" in assoluto. È il criterio per dosare BTP€i/BTP Italia vs nominali (vedi `strumenti-ammessi-e-confronto.md`).

## 8. Come leggere un monitor sui governativi e JP Morgan Guide to the Markets

Quando l'utente fornisce un report (es. un *monitor gov bond* mensile, o le pagine fixed income della *Guide to the Markets*), **leggilo con `project_knowledge_search`/estrazione** ed estraine, senza inventare:
- **Livello e forma delle curve** (Bund/BTP/Treasury): dove sono i rendimenti per scadenza, inclinazione, movimenti recenti.
- **Duration e rendimento a scadenza degli indici** governativi (per il confronto con i singoli).
- **Spread** sovrani (BTP-Bund, OAT-Bund, ecc.) e loro percentili storici.
- **Aspettative d'inflazione** (break-even) e tassi reali.
- Eventuali **viste** dell'emittente del report (che vanno riportate **come viste di terzi**, contestualizzate, non come verità o come segnali di timing).

Regola di rigore: cita solo dati **effettivamente presenti** nel report; se un dato non c'è, dillo. Non riempire i vuoti a memoria. Rispetta i limiti di citazione (parafrasa, non copiare).

## 9. La linea macro / timing (da non superare)

La macro serve a **contestualizzare, scegliere il punto di curva e calibrare le aspettative**. **Non** serve a:
- cronometrare l'ingresso ("aspetto che i tassi salgano ancora");
- allungare/accorciare la duration inseguendo le previsioni sui tassi;
- scommettere sullo spread o sulla direzione della curva.

Se il quadro macro spinge verso una decisione tattica, **segnala la tentazione e riconducila alla regola**: in cash-flow matching si compra la scadenza che serve, al miglior netto disponibile, quando la liquidità è pronta. Il "momento giusto" è quando serve il flusso, non quando il modello dice che i tassi gireranno.
