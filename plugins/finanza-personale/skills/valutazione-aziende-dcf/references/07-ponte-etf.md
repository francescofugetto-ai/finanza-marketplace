# 07 · Il ponte verso il portafoglio — regole restrittive e riga di confine

Questo è il file che dice **no**.

L'idea da cui è nato tutto il lavoro era: valuto le aziende più pesanti dei miei
ETF, scopro che sono care, e sposto peso. È un'idea naturale, ed è la ragione per
cui questa skill esiste. Non è però ciò che questa skill fa, e la distanza fra le
due cose va scritta qui, per esteso, perché è l'unico punto in cui il metodo può
rompersi in silenzio.

> **Il lavoro di valutazione può cambiare quanto ti aspetti e quanto rischio sai
> di correre. Non può cambiare i pesi.**

---

## 1 · Perché il ponte è stretto

Tre ragioni, indipendenti. Ciascuna basterebbe da sola.

**Contraddice la dottrina già scritta.** In `metodo-fiduciario/SKILL.md`
l'anti-timing è fra le regole non negoziabili. Spostare peso da uno strumento a un
altro perché un DCF dice che certe aziende sono care **è market timing basato
sulle valutazioni**. Non è una versione più colta del timing: è il timing, con un
modello davanti.

**L'incertezza di misura non regge una decisione sui pesi.** L'episodio 337 ha
valutato la stessa azienda con ipotesi tutte difendibili ottenendo **3,93 · 14,14
· 36,27**: un fattore nove. Una decisione di portafoglio presa su una misura con
quell'ampiezza non è una decisione, è un sorteggio con un rituale.

**L'errore non si annulla sommando aziende.** È l'obiezione tecnicamente più
importante, e la meno intuitiva. Sommando dieci valutazioni indipendenti gli
errori si compenserebbero in parte; ma queste **non sono indipendenti**: il costo
del capitale è costruito sullo stesso tasso privo di rischio e sullo stesso premio
per il rischio azionario per tutte. Se il WACC è sbagliato di un punto, è
sbagliato di un punto in tutte e dieci, nella stessa direzione. **La media di
dieci errori correlati è l'errore, non un decimo dell'errore.**

C'è poi un argomento di livello: la domanda «questo indice è caro?» ha strumenti
propri e migliori — CAPE, premio per il rischio implicito, earnings yield contro
tasso privo di rischio — e una parte è già in `rendimenti-attesi-portafoglio`,
metodo top-down `DY + g`. Rispondere a quella domanda sommando DCF di singole
aziende è usare uno strumento fine per un lavoro grosso.

---

## 2 · Le quattro regole restrittive

### Regola 1 — Mai sommare i fair value

**Non esiste il fair value di un ETF.** Non come approssimazione, non come ordine
di grandezza, non «solo per farsi un'idea».

Un ETF su un indice largo ha centinaia di posizioni, di cui se ne valutano otto o
dodici. Le altre non sono «il resto»: sono la maggioranza del peso, e fra loro ci
sono banche, assicurazioni, holding e cicliche — cioè esattamente le categorie che
`references/00-dottrina-valutazione.md` §5 esclude dal DCF. Un aggregato costruito
su ciò che si è potuto valutare e silenzioso su ciò che non si è potuto valutare
è peggio di nessun aggregato: ha un numero al posto di un buco.

Sono vietate, in ogni forma: la somma dei fair value pesata per i pesi dell'ETF;
l'upside medio ponderato; la percentuale di sopravvalutazione dell'indice; la
crescita implicita «media» del paniere. L'elenco sta anche in
`references/06-verdetto-e-linguaggio.md` §3-G.

### Regola 2 — L'unica aggregazione ammessa è la tabella di prezzatura implicita

Si mostra **cosa il prezzo sconta**, azienda per azienda, senza mai fondere le
righe in un numero.

| # | Azienda | Peso nell'ETF | Prezzo (data) | Crescita implicita | Categoria | Ultima valutazione |
|---|---|---|---|---|---|---|
| 1 | … | 6,2% | … | 58% l'anno | eroiche | 12 mag 2026 |
| 2 | … | 4,8% | … | 11% l'anno | modeste | 3 giu 2026 |
| … | | | | | | |
| | **Copertura** | **31,4% del peso** | | | | |

Quattro vincoli sulla tabella.

- **Nessuna riga di totale**, né somma né media. La riga finale riporta una cosa
  sola: **quale quota del peso dell'ETF è coperta da valutazioni correnti**. È
  un'informazione sulla copertura, non sul valore.
- **La colonna della categoria è qualitativa** e usa le tre parole del `06`:
  *modeste · esigenti · eroiche*.
- **Ogni riga porta la data della propria valutazione.** Righe di età diversa non
  si mescolano in silenzio.
- **La data delle holdings è dichiarata in testa alla tabella.** I pesi di un ETF
  sono aggiornati al giorno, non al momento — vedi
  `references/08-manutenzione-e-batch.md`.

Che cosa si può dire di quella tabella, in tutto: *«su un terzo del peso
dell'ETF, sette posizioni su dieci scontano aspettative esigenti o eroiche.»*
Un'osservazione, con la sua copertura dichiarata. Non un numero da confrontare con
un altro ETF, e non un input di nessuna formula.

### Regola 3 — L'output entra in `rendimenti-attesi-portafoglio` come strato di contesto

L'unico canale legittimo verso il portafoglio, e ha una direzione sola.

Il metodo top-down di quella skill stima il rendimento atteso di un blocco
azionario da dividend yield più crescita. **Questo lavoro non lo sostituisce e non
lo corregge aritmeticamente.** Non esiste un coefficiente che traduce «sette
posizioni su dieci scontano aspettative eroiche» in punti di rendimento atteso in
meno: se esistesse, sarebbe l'aggregazione vietata dalla regola 1 con un altro
nome.

Che cosa può fare, allora. Una revisione del rendimento atteso di un blocco è
legittima se soddisfa **tutte e quattro** queste condizioni:

1. è **motivata a parole** e la motivazione cita la tabella di prezzatura
   implicita con la sua copertura;
2. porta una **data** e resta tracciata nel registro;
3. si muove **dentro l'intervallo** che il metodo top-down produce già, non fuori:
   sposta il punto scelto dentro il range, non crea un range nuovo;
4. è **rivista alla revisione successiva** come tutte le altre ipotesi, non
   diventa permanente.

Vale la soglia di materialità già in vigore in `metodo-fiduciario/SKILL.md`: il
rendimento atteso non si ritocca per movimenti sotto i 0,3 punti. Sotto quella
soglia, l'osservazione resta scritta e il numero non si muove.

Vedi `consulenza-portafogli-etf/references/canone-the-bull/rendimenti-attesi.md`
per la dottrina di quel numero, e
`rendimenti-attesi-portafoglio/references/metodologia-top-down.md` per il metodo
che questo strato **non** sostituisce.

### Regola 4 — Nessun trigger automatico di ribilanciamento

Un *trigger* è una condizione scritta che, quando si verifica, fa scattare
un'azione. In questa skill i trigger esistono — sono nel record del registro — ma
possono far scattare **una cosa sola**: una nuova valutazione.

| Trigger ammesso | Che cosa fa scattare |
|---|---|
| nuova relazione annuale pubblicata | rivalutazione piena |
| acquisizione o cessione rilevante | rivalutazione piena |
| guidance rivista in modo materiale | rivalutazione piena |
| tasso privo di rischio mosso oltre la soglia dichiarata | rivalutazione piena |
| oltre 90 giorni dall'ultimo aggiornamento | riesame leggero |
| oltre 12 mesi, o `ipotesi_valide_fino_a` superata | rivalutazione piena |

| Trigger vietato |
|---|
| «se il prezzo supera il fair value del 30%, riduci» |
| «se tre posizioni su dieci passano a eroiche, sposta peso» |
| «se la copertura scende sotto il 25%, sospendi il PAC su quell'ETF» |
| qualunque condizione la cui conseguenza sia un peso, un ingresso o un'uscita |

La differenza non è di forma: un trigger che produce una valutazione produce
**conoscenza**, e chi la riceve decide. Un trigger che produce un peso ha già
deciso, e lo ha fatto in un momento in cui nessuno stava guardando.

---

## 3 · Che cosa il ponte può portare

Tre cose, tutte con soglia e data, tutte tracciate nel registro.

**Le aspettative.** La revisione del rendimento atteso di un blocco, alle quattro
condizioni della regola 3.

**I vincoli di consapevolezza.** Un vincolo di consapevolezza non cambia
l'allocazione: cambia che cosa si sa di stare rischiando, e va scritto prima che
serva. *«Il 31% del peso di questo ETF sconta aspettative esigenti o eroiche: un
drawdown del 40% su quel blocco è dentro il previsto, non è un imprevisto.»* È
scritto, ha una data, e sopravvive al momento in cui accade — che è l'unico
momento in cui serve.

**Un tetto di concentrazione deciso *ex ante*.** Legittimo, con un vincolo forte:
si fissa **prima**, in astratto, come regola di costruzione del portafoglio. Un
tetto fissato guardando l'ultimo report è un ribilanciamento con un altro nome.

---

## 4 · La zona grigia dei flussi del PAC

Dichiarata come tale, non risolta di nascosto.

Dirigere i **nuovi versamenti** del piano di accumulo verso l'ETF le cui
posizioni scontano aspettative più modeste è una forma morbida della stessa
scommessa. Più difendibile del vendere — non si realizzano imposte, non si esce
da niente, si sposta solo il marginale — ma **resta timing sulle valutazioni**.

La posizione della skill è: se la si vuole ammettere, va scritta **prima**, come
regola, con quattro elementi obbligatori.

1. **Una soglia numerica**, decisa in astratto e non sull'ultimo report.
2. **Una data di entrata in vigore**, e una di riesame.
3. **Un tetto alla deviazione** — quanta parte del flusso mensile può essere
   dirottata, mai la totalità.
4. **Un criterio di uscita**: a quale condizione la regola smette di valere.

Senza tutti e quattro, la risposta della skill è **no**, e il no va scritto nel
report invece di essere lasciato all'assenza di una riga.

**Che cosa non è mai ammesso**, nemmeno con la regola scritta: decidere caso per
caso guardando l'ultimo report; dirottare il 100% del flusso; sospendere un PAC;
applicare la regola a ritroso su versamenti già fatti.

---

## 5 · Come si presenta il verdetto d'insieme

Quando la sessione produce un quadro su più aziende — tipicamente al termine del
comando di manutenzione — la sintesi ha una forma fissa, e ricalca il verdetto
del `06` a livello di paniere.

```
1. la copertura ............. quale quota del peso è coperta, e a quale data
2. la distribuzione ......... quante posizioni in modeste / esigenti / eroiche
3. che cosa la falsificherebbe  quali due o tre eventi cambierebbero il quadro
4. che cosa NON segue ....... esplicito, una riga
```

Il quarto punto va scritto ogni volta, e in chiaro:

> Da questo quadro non segue nessuna indicazione su pesi, ingressi o uscite. Non
> esiste un fair value di questo ETF, e nessuno è stato calcolato.

Sembra ridondante alla prima lettura. Non lo è alla decima, quando il documento è
diventato familiare e la conclusione ovvia comincia a scriversi da sola nella
testa di chi legge.

---

## 6 · La riga di confine

È la formulazione che va nel §0.3 di `metodo-fiduciario/SKILL.md`, e vale come
regola operativa in ogni sessione.

> **`valutazione-aziende-dcf` — confine.**
> Si occupa di singole aziende quotate. Non decide mai pesi di portafoglio, non
> genera trigger di ribilanciamento, non entra nelle sessioni di allocazione, PAC
> o profilazione.
> Il suo output alimenta due cose e due sole: le **aspettative**
> (`rendimenti-attesi-portafoglio`, come strato di contesto, mai come sostituto
> del top-down `DY + g`) e i **vincoli di consapevolezza** a registro.
>
> **Il lavoro di valutazione può cambiare quanto ti aspetti e quanto rischio sai
> di correre. Non può cambiare i pesi.**
>
> L'anti-timing resta intatto. Dirigere i nuovi flussi del PAC sulla base di una
> valutazione è una forma morbida di timing: se ammessa, va scritta *ex ante* come
> regola con soglia numerica e data, mai decisa caso per caso.

Nota che l'anti-timing **ne esce rafforzato, non emendato**. Prima era una regola
implicita che non aveva mai incontrato una tentazione concreta. Ora la tentazione
ha un nome, un modello e una tabella — ed è per questo che serviva scriverle
accanto un divieto altrettanto concreto.

---

## 7 · Il confine con le altre skill

| Domanda | Skill |
|---|---|
| «quanto vale questa azienda, e con quali ipotesi» | **questa** |
| «questo strumento serve al mio scopo, e come si confronta con i concorrenti» | `analisi-documenti-investimento`, modalità B |
| «quanto metto, e su quale asset class» | `consulenza-portafogli-etf` |
| «quanto rende l'insieme a dieci anni» | `rendimenti-attesi-portafoglio` |
| «quale titolo di Stato, a quale netto» | `analisi-titoli-di-stato-eu` |

Il confine più sottile è il primo con il secondo, perché entrambi guardano uno
strumento e producono un verdetto. La distinzione è nell'oggetto: la modalità B
valuta **un prodotto rispetto a uno scopo** — costo, replica, liquidità,
alternative; questa skill valuta **un'azienda rispetto a un prezzo**. Vedi
`analisi-documenti-investimento/references/modalita-B-strumento.md`.

Una sessione che nasce come «vale la pena questo ETF?» non è questa skill,
nemmeno se poi si parla delle aziende che contiene.

---

## 8 · Riepilogo

```
MAI  sommare fair value, in nessuna forma
MAI  un trigger la cui conseguenza sia un peso, un ingresso o un'uscita
MAI  decidere i flussi del PAC guardando l'ultimo report
SI'  tabella di prezzatura implicita, riga per riga, con la copertura dichiarata
SI'  revisione delle aspettative, dentro il range top-down, con motivazione e data
SI'  vincoli di consapevolezza, scritti prima che servano
```

Cinque cose da ricordare.

1. **Non esiste il fair value di un ETF.** L'unica aggregazione è una tabella che
   non si somma.
2. **L'errore non si annulla sommando aziende**: le ipotesi sono correlate fra
   loro.
3. **L'unico canale verso il portafoglio** è lo strato di contesto sulle
   aspettative, con quattro condizioni.
4. **I trigger di questa skill fanno scattare valutazioni, mai pesi.**
5. **La zona grigia del PAC resta grigia**, e il no si scrive invece di essere
   sottinteso.

Il file successivo, `references/08-manutenzione-e-batch.md`, è la parte operativa:
come si tiene aggiornato un nucleo di otto-dodici aziende senza rifarle tutte, e
che cosa fa esattamente il comando di manutenzione.
