# Architettura a 5 pilastri (= 3 bucket) — regole di costruzione

Struttura di accumulo per investitori area euro in stile "lazy efficiente". Ogni pilastro ha una funzione; il peso dipende dal profilo (Fase 1) e non dalle previsioni di mercato. Si parte sempre dalla domanda: *quale rischio sto cercando di ridurre con questo mattoncino?*

## Identità bucket ↔ pilastri

I "bucket" (per missione e orizzonte) e i "pilastri" (per funzione tecnica) sono **la stessa struttura** vista a due livelli di zoom, non due tassonomie concorrenti. Mappatura fissa, da non tradire:

- **B1 ≡ P1** — Cash spese correnti.
- **B2 ≡ P2** — Fondo emergenza + progetti a brevissimo termine + polvere da sparo.
- **B3 ≡ P3 + P4 + P5** — Il portafoglio investito: azionario, obbligazionario, diversificatori/satelliti.

Conseguenza operativa: una **passività con scadenza ravvicinata** (es. acconto casa fra 1–3 anni) **non** è B2/P2 (non è un'emergenza né un orizzonte "brevissimo") e **non** può stare nell'azionario di P3. Vive in **P4 in missione goal**, ring-fenced (vedi sotto). Resta dentro B3 per classificazione — è il pilastro obbligazionario — ma è operativamente separata dal motore azionario.

## Pilastro 1 — Cash (liquidità operativa)
- **Funzione:** coprire le spese correnti e gli imprevisti minori senza toccare gli investimenti.
- **Dimensionamento:** ~2–3× le spese mensili.
- **Dove:** conto corrente (accesso immediato). Non è un investimento, è un cuscinetto operativo.

## Pilastro 2 — Fondo emergenza
- **Funzione:** assorbire shock di reddito (perdita lavoro, spese impreviste grandi) senza vendere l'azionario nel momento sbagliato.
- **Dimensionamento:** ~6× le spese mensili come base. Alza la riserva se il reddito è instabile (tipo "azioni", P.IVA), se c'è un solo reddito nel nucleo, o se ci sono persone a carico; puoi ridurla se il reddito è molto stabile (tipo "bund") e c'è patrimonio liquido di riserva.
- **Dove:** conto deposito svincolabile, oppure ETF monetario / governativo area euro a brevissima scadenza. Priorità ad accessibilità e bassa volatilità, non al rendimento.
- **Polvere da sparo (opzionale, dentro B2):** liquidità tenuta per comprare in caduta. Va ammessa **solo con una regola di deployment scritta** e quantificata (es. "schiero 50% a –15% di drawdown sull'azionario, il resto a –25%"). Senza trigger non è strategia: è *cash drag* (rendimento atteso perso a tenerla ferma) travestito da prudenza, ed è market timing implicito — che la filosofia "just keep buying" rifiuta, perché il lump-sum batte la diluizione nella maggioranza dei casi storici. Se non si scrive la regola, la polvere confluisce nel motore (P3).

## Pilastro 3 — Azionario (motore di crescita)
- **Funzione:** il vero motore del rendimento di lungo periodo.
- **Versione semplice:** **1 ETF azionario globale** market-cap (indice FTSE All-World o MSCI ACWI/World secondo copertura desiderata). È la scelta di default per la maggior parte degli investitori.
- **Versione "pro" (scomposizione in ~3 ETF):** giustificata **solo** se produce un beneficio concreto:
  1. abbattere il TER medio ponderato,
  2. dare tilt geografici *voluti* (es. sovrappeso emergenti),
  3. sfruttare le commissioni zero del broker (es. PAC gratuiti).
  Il costo è maggiore complessità: distribuzione del PAC su più strumenti (il PAC dev'essere cospicuo perché abbia senso) e ribilanciamento più articolato. Proponila solo a chi ha la disciplina per gestirla.
- **Gating della complessità (importante):** per **neofiti, bassa esperienza o disponibilità psicologica incerta**, default alla **versione a 1 ETF**, anche se la capacità di rischio sarebbe alta. La scomposizione in 3 ETF e il tilt fattoriale si riservano a investitori esperti e disciplinati. La priorità per chi parte è la *gestibilità in panico*, non l'ottimizzazione del TER.
- **Default:** ETF ad **accumulazione** in fase di accumulo.

## Pilastro 4 — Obbligazionario (due missioni distinte)

Il Pilastro 4 fa **due mestieri diversi**, da non confondere perché hanno regole opposte:

- **Missione STABILITÀ (portafoglio):** ammorbidire il drawdown del motore azionario e fornire carburante da cui attingere per ribilanciare. È **condizionale**.
- **Missione GOAL (passività datata):** mettere al sicuro il capitale di un obiettivo con scadenza nota (acconto casa, auto, tasse di un anno). È **obbligatoria e ring-fenced**: separata dall'equity per mandato, non per percentuale.

### Missione STABILITÀ (condizionale)
- **Quando NON serve:** orizzonte lungo (>20–25 anni), profilo aggressivo, meno di ~40–45 anni → gamba assente o minima. Aggiungerla presto frena il motore senza beneficio proporzionato.
- **Quando serve:** avvicinandosi all'exit, con profilo più prudente.
- **Eccezione comportamentale:** per un neofita con disponibilità psicologica incerta, una piccola quota difensiva (es. ~10%) è giustificata anche quando la regola per età direbbe di ometterla: ammorbidisce il primo drawdown e fa da carburante al ribilanciamento. È un costo di rendimento atteso accettato per ridurre il rischio di abbandono del piano.
- **Strumento:** **ETF aggregate / Euro Aggregate**, **duration corta**, **cambio coperto in EUR** (hedge EUR) se l'obbligazionario è in valuta estera — altrimenti il movimento valutario domina e annulla la funzione difensiva. Più duration/credito/valuta = più correlazione con l'azionario, proprio quando vorresti scollegare.
- **Avvertenza:** la correlazione negativa azioni–bond non è più affidabile come un tempo (2022 docet). Non dare per scontato che il bond faccia sempre da scudo.

### Missione GOAL — albero per tempo-alla-scadenza
La regola dipende **da quanto manca** all'obiettivo. È l'errore più costoso da sbagliare: un obiettivo vicino lasciato in azionario può perdere un terzo del valore mesi prima della data.

- **Goal lontano (> ~7–10 anni, es. studi di un figlio):** resta nel **motore azionario (P3)**; si scorpora e si de-rischia progressivamente **negli ultimi ~5 anni** verso strumenti a scadenza vicina alla data. Non si de-rischia in anticipo né lo si lascia interamente azionario fino all'ultimo.
- **Goal ravvicinato (entro ~3–5 anni, es. acconto casa):** **ring-fenced da subito**, **mai equity, mai HY, mai EM, mai duration oltre l'orizzonte**. Strumenti ammessi: BTP/BOT/Bund con **scadenza ≤ orizzonte**, conto deposito vincolato a scadenza allineata, ETF monetario EUR (€STR), obbligazionario IG EUR a duration <2y EUR-hedged. La fiscalità premia i titoli di Stato white-list (12,5%) rispetto al 26%.
- **Glide path obbligatorio:** man mano che la data si avvicina, la quota a rischio-prezzo scende verso il monetario/cash. Riferimento: a **T-12 mesi, 100% cash/monetario**; revisione almeno trimestrale. La duration residua non deve mai superare i mesi che mancano alla scadenza.
- **Strumento per goal singolo a scadenza nota:** un **bond singolo** (govt o IG di qualità) che matura vicino alla data elimina il rischio-prezzo a scadenza (lo tieni fino a maturity e incassi il nominale), meglio di un ETF obbligazionario che non ha scadenza.

**Decisione mutuo vs. liquidazione del goal (a ridosso della data):** confronta il costo del mutuo *netto* (post deducibilità interessi prima casa) con il rendimento atteso del capitale lasciato investito. È una decisione **numerica**, non di pancia: se il capitale-goal rende meno del costo netto del mutuo, conviene usarlo; altrimenti conviene il mutuo e lasciare investito.

## Pilastro 5 — Diversificatori / satelliti (decorrelazione e premi)

Pilastro **satellite**, non core. Tre famiglie, tutte a **peso misurato**: oltre una certa quota smettono di diversificare e diventano scommesse. Per stomaci sufficientemente forti da tollerare lunghi periodi di "torto apparente".

**5a — Oro / commodities (decorrelazione monetaria/geopolitica)**
- **Funzione:** terza fonte di comportamento, decorrelata da azioni e bond; reagisce a sfiducia sulle valute fiat, tassi reali in calo, tensioni geopolitiche.
- **Quando ha più senso:** per chi vuole ridurre le fluttuazioni avvicinandosi all'exit (es. 50–55 anni con uscita a 60–65). Meno prioritario in piena fase di accumulo aggressiva.
- **Dimensionamento:** quota piccola. Una quota grande trasforma l'oro da diversificatore a scommessa macro su tassi reali, dollaro e geopolitica.
- **Limiti da dichiarare:** l'oro non genera cedole né dividendi; è esposto al dollaro per chi investe in euro; può sottoperformare per anni. Le commodities aiutano soprattutto negli shock energetico-geopolitici ma possono restare deboli a lungo.

**5b — Fattoriale / smart beta (premi attesi da fattori)**
- **Funzione:** inseguire premi attesi di lungo periodo da fattori come **Value**, **Momentum**, **Quality**, **Size**.
- **Soglia di rilevanza:** il tilt conta solo se abbastanza grande, indicativamente **≥ ~33% dell'azionario totale**. Sotto quella soglia è **rumore**: aggiunge complessità e TER senza spostare il risultato (es. un 5%+5% Value+Momentum è omeopatico e, se gli ETF sono "World", ri-compra le large cap USA già nel core — vedi regola anti-doppioni).
- **Costo comportamentale:** i fattori possono sottoperformare il mercato per **anni** (anche oltre 10). Solo per chi capisce e tollera il "torto apparente". Mai inserirlo "di pancia".

**5c — Real estate (REIT)**
- **Funzione:** esposizione all'immobiliare quotato (canoni + rivalutazione), parzialmente decorrelata dall'equity puro, sensibile ai tassi.
- **Limiti da dichiarare:** i REIT quotati sono **più correlati all'azionario** di quanto suggerisca l'etichetta "immobiliare", e sensibili al rialzo tassi (duration implicita). Soprattutto: se l'investitore possiede **immobili fisici** (prima casa, immobili a reddito), l'esposizione real estate è **già massiccia e concentrata** — aggiungere REIT spesso raddoppia un rischio già presente invece di diversificare. Verificare il patrimonio reale prima di proporlo.

## Regola anti-doppioni (sempre)
Leggi il portafoglio in modo **aggregato**, non ETF per ETF. Strumenti diversi possono nascondere la stessa esposizione:
- **Minimum Volatility + settori difensivi** (Healthcare, Consumer Staples, Utilities) rafforzano lo stesso fattore (low-vol/quality): sommali, non trattarli come diversificazione.
- Controlla il **peso reale degli USA** e dei top-10 titoli quando coesistono più ETF azionari. **Calcolalo in look-through**, non a occhio: gli ETF fattoriali "World" (Value, Momentum, Quality, Min Vol) sono ~70% USA, quindi sommano peso USA a quello dei core/USA dedicati. Esempio: 50% MSCI USA + 6% World Value + 6% World Momentum ⇒ USA reale ≈ 50% + 0,70×12% ≈ **58%**, non 50%.
- Verifica l'**esposizione valutaria** complessiva.
La domanda utile non è "quanto pesa questo ETF?" ma "quanto pesa davvero *quel fattore/rischio* nel portafoglio complessivo?".

## Mappatura indicativa per età / profilo
Indicazioni di partenza, da adattare al profilo reale (mai meccaniche). **Riguardano la missione-STABILITÀ di P4 e i satelliti P5**: la **missione-GOAL di P4 è indipendente dall'età** — se esiste una passività datata ravvicinata va comunque ring-fenced, anche per un 30enne aggressivo.
- **<40–45 anni, orizzonte >20 anni, profilo aggressivo:** baricentro su Pilastro 3 (azionario), bond-stabilità minimo/assente, oro eventuale e piccolo, tilt fattoriale solo se convinti e sopra soglia.
- **Fase intermedia:** introduzione graduale del Pilastro 4 e/o 5 man mano che l'orizzonte si accorcia o il profilo si fa più prudente.
- **Vicino all'exit (es. 50–55+ con uscita a 60–65):** crescono stabilità (Pilastro 4) e decorrelazione (Pilastro 5); qui ha senso approfondire la logica anticrisi del documento "ETF Italia — I 5 pilastri di un portafoglio più solido" (obbligazionario breve, Min Vol, settori difensivi, managed futures, oro), tenendo presente che è una tassonomia *difensiva* distinta da questa struttura di accumulo.

## PIC / PAC e ribilanciamento
- **Vincolo di cassa (controllare sempre per primo):** cash (Pilastro 1) e fondo emergenza (Pilastro 2) si finanziano **prima** del PIC, dalla stessa liquidità disponibile. Il PIC reale è ciò che **resta** dopo aver coperto i cuscinetti: non si può finanziare il PIC e tenere il fondo emergenza con gli stessi soldi. Verifica questo prima di proporre qualsiasi importo.
- Definisci sempre la **modalità di ingresso**: PIC (una tantum), PAC (versamenti periodici), o combinazione. Su orizzonti lunghi il PAC dà disciplina e riduce l'errore comportamentale; non trasformarlo in market timing ("aspetto il punto migliore").
- **PIC: lump-sum vs spalmatura.** L'ingresso in un'unica soluzione (lump-sum) batte statisticamente la diluizione nella maggioranza dei casi storici. Per un neofita nervoso è però legittimo **spalmare il PIC in poche tranche su pochi mesi** come *accomodamento comportamentale* — non come market timing. Dichiaralo per quello che è: serve a non abbandonare il piano, non a indovinare il minimo.
- Scrivi una **regola di ribilanciamento** esplicita:
  - **a soglie** (es. si interviene quando una componente si allontana dal target oltre ±10 punti percentuali), oppure
  - **a calendario** (al massimo annuale, q1a).
  - In ribassi importanti la regola può prevedere di riportare l'azionario al target (o ampliarlo) attingendo dalla gamba difensiva, **senza** chiedersi se è "il momento giusto".
- La regola va scritta prima della crisi: serve a trasformare una decisione emotiva in una procedura.
