# Canone The Bull — P4 Obbligazionario

Fonti: `[TB-141]` duration · `[TB-187]` singoli vs ETF · `[TB-190]` i 3 dubbi · `[TB-bond-4miti]` i 4 miti / fotogramma-vs-film · `[TB-339]` lo yield iniziale come stima del rendimento (rimando: `rendimenti-attesi.md`).

## Meccanica di base `[TB-141]`

- Un'obbligazione è un titolo di debito: capitale a scadenza (alla pari, 100) + cedole periodiche. **Tassi su → prezzi giù; tassi giù → prezzi su.**
- I mercati sono **forward-looking**: i prezzi si muovono sulle *aspettative* dei tassi, non sull'intervento effettivo della banca centrale. Dato inflazione > attese → bond giù subito; dato occupazione debole → bond su (anticipa tagli).
- **Duration** = tempo medio di rientro dell'investimento via flussi di cassa. **Duration modificata** = duration / (1+YTM); approssima la variazione % del prezzo per ±100 bps di tassi: **Δprezzo ≈ −Δtassi × duration**.
- Breve termine guidato dalle banche centrali; **lungo termine guidato dai bond vigilantes** (Yardeni): es. dopo il taglio Fed, il decennale USA può vedere i *rendimenti salire* se il mercato teme inflazione futura.
- **ETF obbligazionario**: fondo che replica un indice di bond. **Non scade** (salvo i pochi ETF a scadenza tipo iBonds): "rolla" i titoli per mantenere la **duration costante**. Prezzo della quota = cedole reinvestite (se accumulazione) + variazioni tassi. Un ETF duration 7 → ~±7% per ±100 bps.

## Singoli bond vs ETF obbligazionari — le 4 motivazioni `[TB-187]`

Tesi canonica: **investire in ETF obbligazionari è quasi sempre più pratico ed efficiente dei singoli bond**, e il "i bond singoli scadono quindi sono sicuri" è vero al 100% ma **irrilevante** al 100%.

1. **Diversificazione.** Impossibile diversificare bene con singoli bond senza grandi capitali. Solo titoli di Stato, taglio minimo ~1.000 €: una *bond ladder* su 3 emittenti per 10 anni richiede 25-30k € e resta lontana da una vera diversificazione. PAC mensile impraticabile con tagli da 1.000 €. **Corporate** singoli fuori discussione (tagli 100-250k, OTC, spread alti). Il singolo BTP ha **rischio di credito + rischio emittente**: nel 2011 lo spread schizzò +570 bps; uno spread da 120→520 bps con duration 5 = ~−20% sul prezzo. Default IG ~2% in 10 anni → con una ladder di 25 bond, ~50% di probabilità che uno faccia default. Il **corporate IG** in portafoglio (via ETF) è un layer intermedio sensato tra Stato e azioni; YTM Bloomberg Euro Corporate ~3,2% vs Treasury eurozona ~2,7% (spread stretto = alta propensione al rischio del mercato; storicamente IG USA ~+150 bps sui Treasury su 20 anni).

2. **Yield-to-maturity reinvestito.** Lo YTM si realizza **solo se reinvesti tutte le cedole** allo stesso tasso. Quasi nessun risparmiatore reinveste le cedole (le spende, o restano a far muffa) → lascia rendimento per strada, e le cedole sono **tassate al 12,5%** (drag fiscale sull'interesse composto). L'**ETF ad accumulazione** reinveste le cedole **automaticamente e tax-free**. Come i dividendi (Meb Faber): senza reinvestirli, il 10% medio dell'S&P 500 "lo vedi col binocolo".

3. **Duration costante e gestione di portafoglio.** L'ETF mantiene la duration costante → sai che in recessione un taglio di 1-2 punti fa salire l'ETF dell'8-16% mentre l'azionario crolla, e puoi **ribilanciare**. Con singoli bond la duration cala nel tempo e devi rinnovare manualmente la ladder. In più, un ETF molto liquido e diversificato regge meglio durante gli shock (flight-to-quality), mentre i BTP in pancia possono *sprofondare* se il mercato prezza recessione (Treasury/Bund volano, BTP giù per rischio emittente).

4. **Aritmetica (la più importante — qui inciampa il 99,99%).** "Tengo il bond a scadenza e riavrò il capitale" è un'**illusione ottica**:
   - *Il valore reale è eroso*: il prezzo scende quando i tassi salgono, e i tassi salgono per l'inflazione → a scadenza riavi il nominale ma vale meno in termini reali. **Anche con i singoli a scadenza si perdono soldi (reali).**
   - *Un ETF È fatto di bond* (Asness: come può un fondo di bond essere peggio dei bond che contiene?). Se i tassi salgono e l'ETF duration 7 fa −14%, il titolo di Stato equivalente è sceso *anch'esso* del ~14%: puoi vendere l'ETF e comprarne i titoli sottostanti allo stesso prezzo. Equivalenza esatta.
   - **Pull to par**: il prezzo di un bond sotto la pari risale a 100 verso la scadenza *se i tassi non si muovono più* — ma vale anche per i bond **dentro** l'ETF (tirati alla pari prima del roll), e i nuovi bond rollati pagano **cedole più alte** ai nuovi tassi.
   - **Una ladder non scade mai**: a ogni scadenza reinvesti → resti **sempre esposto ai tassi**, esattamente come un ETF, ma con più seccature.
   - Eccezione: in **pensione** una ladder di bond (anche inflation-linked) può servire a generare reddito reale costante — ma presuppone un patrimonio già costruito. In **accumulo** (90% degli ascoltatori) i singoli bond lasciano il tempo che trovano.

## Perché bond se da 10 anni rendono male `[TB-190]`

- I backtest su JustETF arrivano al massimo al ~2010 e mostrano azionario che spacca e obbligazionario IG (specie lungo) mediocre. **Driver comune: tassi a zero** (politica monetaria eccezionale post-GFC) → bond a rendimento ~0, equity growth dopato.
- **2022 = peggior anno di sempre per i bond**: Treasury decennali −18% (mai a doppia cifra negativa dal 1928). Concentrazione unica di fattori: tassi di partenza a zero + pandemia/liquidità + guerra/energia. **Ignorare le performance passate limitate agli ultimi 15 anni.**
- **Oggi normalizzato**: tassi e tassi reali positivi; il rendimento viene **dalle cedole**, non solo dall'attesa di tagli → a parità di scadenza, **duration minore**. Un Bloomberg Euro Aggregate Treasury rende ~2,8% lordo: yield positivo, total return dipende dai prezzi. Per rivivere il 2022 servono i tre ingredienti (tassi a zero di partenza + pandemia + shock energetico da invasione) — oggi non in agenda.

## Inflation-linked (IL / TIPS / BTP Italia) `[TB-bond-4miti, TB-268]`

- Proteggono il **potere d'acquisto**: capitale e cedole rivalutati con l'inflazione. Esempio: titolo 100 cedola 1%, inflazione 3% → capitale 103, cedola 1,03.
- **Break-even inflation** = livello d'inflazione che rende equivalente un nominale e un IL di pari scadenza. Es. Treasury 4,2% e TIPS 1,8% → break-even 2,4%. Inflazione *realizzata* > 2,4% → conveniva il TIPS; < 2,4% → conveniva il nominale. **Un IL è "meglio" solo se l'inflazione *ex post* supera quella *prezzata*, non se l'inflazione è "alta" in assoluto.**
- **NON sono inflation-proof nel breve**: il prezzo è scontato al **tasso reale**; se i tassi reali salgono, l'IL scende — gli IL europei persero >15% da mar a ott 2022 *nonostante* l'inflazione galoppasse. Due forze: inflazione realizzata (spinge su il nominale rivalutato) vs tasso reale (spinge giù il prezzo di mercato). Sul **lungo** preservano il potere d'acquisto meglio dei nominali, specie in fiammate o inflazione strutturalmente alta.
- **Europa vs USA**: il mercato TIPS USA è enorme, liquido, su tutta la curva; in Europa le emissioni sono concentrate in **Francia, Italia, Spagna** (la Germania ha smesso di emettere nuovi IL nel 2023) → meno diversificazione, qualità di credito non AAA, tassi reali più bassi (Europa più "rassegnata" a crescita bassa; risparmio alto, demografia stagnante, mercato meno profondo). Non esiste un "risk-free indicizzato" europeo equivalente al TIPS.
- **Implementazione**: se l'obiettivo è potere d'acquisto **in euro** → IL europei, no-brainer. Globali a cambio coperto solo con una vista attiva (rischio: se non copri, rischio valuta; se copri, costi). Backtest 5 anni: Euro Aggregate Treasury −13%; IL europei +4,5%; globali cambio aperto −6,5%; globali cambio coperto −12,6%. Regola pratica: **da 1/3 a 1/2 della gamba obbligazionaria** può andare in IL; oppure **2/3 nominali + 1/3 IL** `[TB-318]`. **Size minima** `[TB-331]`: i TIPS hanno inflation beta ~0,85; una quota simbolica (es. il 2% di Vanguard) non sposta nulla → **≥5-10% o niente** (conflitto C-I); per l'inflazione *inattesa* l'hedge più reattivo sono le commodities (vedi `inflazione.md`).
- **Allocation modello di Victor Haghani** (citato): metà TIPS decennali, 1/4 T-bills (≈monetario), 1/4 Bloomberg Aggregate; solo azioni+bond, ma approva una piccola quota d'oro.

## I 4 miti dei bond — "fotogramma vs film" `[TB-bond-4miti]`

1. **"I singoli bond sono più sicuri perché scadono"** → falso/irrilevante (vedi §motivazione 4). Conta l'esposizione continua ai tassi, non il dato statico tra acquisto e scadenza.
2. **"I bond sono inutili, da 10 anni rendono male"** → recency bias/estrapolazione. 2022 unico; oggi yield positivi; lo YTM iniziale è uno **spoiler potente** del rendimento futuro — **quantificato in `[TB-339]`: R² ≈ 89% sui rendimenti a 5 anni successivi** (Bloomberg U.S. Aggregate, J.P. Morgan *Guide to the Markets*), ~90% sul decennio. "Il rendimento di partenza di un paniere di bond è quasi una profezia che si autoavvera, per pura matematica finanziaria."
3. **"Gli inflation-linked sono a prova d'inflazione"** → falso nel breve (esposti ai tassi reali). Coprono solo l'inflazione *non già prezzata*. L'alleato strutturale contro l'inflazione di lungo è il **portafoglio nel suo insieme**, con l'equity come migliore copertura storica; gli IL sono un completamento, non una sostituzione.
4. **"Il cash sostituisce i bond"** → no (vedi §cash sotto).

## Cash (ETF monetario, es. XEON) ≠ bond `[TB-190, TB-bond-4miti]`

Due cose diverse, **non alternative**:
- **Monetario** replica lo short-term rate (€STR/tasso sui depositi): ottimo **parcheggio** per liquidità <1 anno, fondo emergenza, capitale per un investimento imminente o un **goal datato ravvicinato** (ring-fence). Rende quanto i bond *solo* perché la curva è ancora piatta (è stata invertita 2 anni, si raddrizza). **Rischio di reinvestimento**: tassi giù → rendimento giù; non blocchi niente, sei in balìa della banca centrale.
- **Bond** = asset **strutturale**: rendimento reale di lungo **positivo** (term premium), si apprezza in recessione, dà **duration** (beneficio aggiuntivo se i tassi scendono). Il cash è un pessimo investimento di lungo termine; in recessione il suo rendimento va verso zero.
- Errore tipico: trasformare la situazione contingente 2022-2024 (monetario al 4%, curva invertita) in verità permanente. Chi a inizio 2023 riversò miliardi nei monetari "no-brainer al 5%" si è perso il +50% dell'S&P 500.
- **Quando il cash ha senso**: liquidità di breve (emergenza, spesa entro l'anno, capitale stabile pre-investimento). Come **gamba strutturale sostitutiva dei bond**, inefficiente.

## Ruolo dei bond in portafoglio — sintesi operativa

- Bond **non vuol dire** BTP, **non vuol dire** "reddito", **non vuol dire** "asset che non perde mai" `[TB-318]`.
- Funzione: contenere la volatilità quando l'azionario scende (*spesso, non sempre*); riserva di stabilità nominale; proteggere in scenari **recessivi/deflattivi** (tagli tassi). Soffrono negli shock d'offerta/inflattivi e nelle guerre (rendimento reale negativo).
- Default: **nominali di alta qualità, ampia diversificazione, Global Aggregate hedged in EUR o governativi euro**; in ottica "bentornati anni '70", 1/3 inflation-linked. **Coprire il cambio** sui bond in valuta estera (il movimento valutario domina e annulla la funzione difensiva).
- **Coletti (precisazione approvata)** `[TB-190]`: aveva ragione a tuonare contro chi vendeva *fondi* obbligazionari (cari) a risparmiatori avversi al rischio nel 2021 a tassi zero. Ma il problema è **investire in bond a tassi rasoterra**, non gli ETF in sé. Con tassi a zero non comprare ETF obbligazionari lunghi; oggi (yield ~3%) il discorso è diverso. Il vero disaccordo è sulla visione dell'investimento azionario, non sullo strumento.
- **Stima del rendimento atteso** `[TB-339]`: `E[r] nominale ≈ YTW iniziale + roll-down`, valido su orizzonte ≈ **duration di Macaulay** (non la scadenza media: sono numeri diversi — es. Euro Aggregate Treasury al 30/06/2026, scadenza media 8,6 anni ma duration 7,0). Nei panieri con callable usare lo **yield to worst**, non lo YTM. Correzioni obbligatorie non presenti nella fonte: **(a)** sui panieri **EUR-hedged** sottrarre il costo di copertura ≈ differenziale dei tassi a breve (un Global Aggregate USD hedgiato in EUR rende lo YTM *meno* il differenziale, non lo YTM); **(b)** su credito/HY sottrarre la **perdita attesa da default** (IG ~0,05-0,15 pt/anno, HY ~2-3 pt); **(c)** al netto, sottrarre TER e **bollo 0,20%/anno**, che su uno yield del 3% si mangia oltre il 6% del rendimento. Procedura: `rendimenti-attesi.md` §3 e skill `rendimenti-attesi-portafoglio`. Per i **singoli titoli di Stato** la stima è ancora più diretta (YTM netto a scadenza) → skill `analisi-titoli-di-stato-eu`.

<!-- VERSIONE FILE -->
**Episodi:** TB-141, TB-187, TB-190, TB-bond-4miti (+ rif. TB-339). **Stato:** completo. **Time-sensitive:** ogni YTM/YTW, duration e livello di spread citato — rieseguire da factsheet dell'emittente.
