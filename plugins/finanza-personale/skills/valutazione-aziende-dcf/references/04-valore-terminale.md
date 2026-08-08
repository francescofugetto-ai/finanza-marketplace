# 04 · Il valore terminale — il pezzo che pesa più di tutti gli altri

Nel caso di riferimento, il valore terminale attualizzato vale **10.402,8** su un
enterprise value di **12.510,6**: l'**83,2%** del totale. I cinque anni di ipotesi
costruite con cura — crescita anno per anno, percorso dei margini, reinvestimento
— valgono il 17% restante.

Chi non lo sa passa il tempo sulla parte che conta meno.

---

## 1 · Che cosa rappresenta

L'orizzonte esplicito del modello è fisso a **cinque anni**. Non è un parametro
regolabile: è una scelta di dottrina, perché oltre il quinto anno le ipotesi
puntuali valgono meno del valore terminale che le assorbe.

Il **valore terminale** — spesso abbreviato TV, *terminal value* — è il valore, al
termine del quinto anno, di **tutti i flussi successivi presi insieme**. Non è
«quanto vale l'azienda se la vendo nel 2030»: è la somma attualizzata al 2030 di
ciò che produrrà dal 2031 in poi, per sempre.

Nel motore compaiono due grandezze distinte, ed è bene non confonderle:

| Campo | Che cos'è |
|---|---|
| `terminal_value` | il valore al termine del quinto anno, **non** attualizzato |
| `pv_terminal` | lo stesso valore riportato a oggi, dividendo per `(1 + wacc)^5` |

Nel caso di riferimento: `terminal_value = 16.753,8` e `pv_terminal = 10.402,8`. È
`pv_terminal` quello che si somma ai flussi espliciti.

---

## 2 · La formula di Gordon, nella versione semplice

Il modello di Gordon dice che una serie infinita di flussi che cresce a tasso
costante `g`, scontata a tasso `wacc`, vale:

```
valore = flusso del primo anno successivo ÷ (wacc − g)
```

Applicata al nostro caso, il flusso del sesto anno è il NOPAT del quinto fatto
crescere di `g`:

```
TV_semplice = ebit[5] × (1 + g) × (1 − tax_rate) ÷ (wacc − g)
```

Con i numeri di riferimento — `ebit[5] = 1.835,0`, `g = 3%`, `tax_rate = 27%`,
`wacc = 10%`:

```
1.835,0 × 1,03 × 0,73 ÷ 0,07 = 19.710,6
```

Questa formula ha un difetto, e non è piccolo: **assume che la crescita sia
gratis.** Fa crescere il flusso del 3% l'anno per sempre senza che l'azienda
debba investire un euro per ottenerlo. È lo stesso errore che il campo
`sales_to_capital` evita nei cinque anni espliciti — solo che qui riguarda l'83%
del valore.

---

## 3 · La versione corretta, con il ROIC

La correzione parte da un'identità che vale in stato stazionario:

```
crescita = ritorno sul capitale × quota di utile reinvestita
g = ROIC × tasso di reinvestimento
```

Il senso è diretto. Se ogni euro reinvestito rende il 20%, e si reinveste il 15%
dell'utile, l'utile cresce del `20% × 15% = 3%`. Girando l'identità:

```
tasso di reinvestimento = g ÷ ROIC
quota libera            = 1 − g ÷ ROIC
```

Il flusso davvero disponibile è quindi il NOPAT **al netto** di quel
reinvestimento, e la formula diventa quella che il motore usa:

```
TV = ebit[5] × (1 + g) × (1 − tax_rate) × (1 − g / roic_terminal) ÷ (wacc − g)
```

Con i numeri di riferimento: `g/ROIC = 3/20 = 15%` reinvestito, **85% libero**.

```
1.835,0 × 1,03 × 0,73 × 0,85 ÷ 0,07 = 16.753,8
```

### Quanto costa dimenticarsene

| | TV | `pv_terminal` | Enterprise value | Fair value |
|---|---|---|---|---|
| Gordon semplice, senza il fattore | 19.710,6 | 12.238,7 | 14.346,6 | **17,06** |
| Gordon con ROIC, versione corretta | 16.753,8 | 10.402,8 | 12.510,6 | **14,14** |

**Più 21% di valore per una moltiplicazione mancante.** È l'errore più costoso che
si possa fare in un DCF, e non lascia traccia: il modello gira, i numeri tornano,
il risultato è semplicemente più alto.

### Il fattore cambia con `g` — l'errore da conoscere

`(1 − g/ROIC)` **non è una costante del modello**. Dipende da `g`, e quindi cambia
in ogni cella della matrice di sensibilità:

| `g_terminal` | reinvestito | fattore, con ROIC 20% |
|---|---|---|
| 2,0% | 10% | 0,90 |
| 2,5% | 12,5% | 0,875 |
| 3,0% | 15% | 0,85 |
| 4,0% | 20% | 0,80 |
| 5,0% | 25% | **0,75** |

Chi lo calcola una volta al caso centrale e lo riusa lungo tutta la riga ottiene
un errore che **cresce allontanandosi dal centro**: la matrice torna al 3% e
sbaglia progressivamente sulle colonne esterne. È esattamente il sintomo che la
prova di riferimento del motore controlla, cella per cella.

C'è anche una conseguenza di sostanza, non solo di calcolo: **una crescita
perpetua più alta non è gratis**. Passando dal 2% al 5% il flusso libero scende
dal 90% al 75% del NOPAT. Il valore sale lo stesso — perché il denominatore
`(wacc − g)` si stringe — ma meno di quanto suggerirebbe la formula semplice. La
correzione, insomma, rende la sensibilità a `g` meno esplosiva.

---

## 4 · Il vincolo `wacc > g_terminal`

Il denominatore è `(wacc − g)`. Se `g` si avvicina al `wacc`, il denominatore
tende a zero e il valore tende all'infinito. Se `g` lo supera, il valore diventa
negativo — matematicamente, non economicamente.

Il motore **solleva un errore** se `wacc ≤ g_terminal`. Non restituisce un numero
grande, non restituisce zero: si ferma. È il caso limite più importante di tutto
il modello, perché è quello in cui l'aritmetica produce ancora un risultato mentre
il significato è già sparito.

Quanto è ripida quella parete, con i numeri di riferimento e il `wacc` fermo al
10%:

| `g_terminal` | denominatore | Fair value per azione |
|---|---|---|
| 3% | 0,07 | 14,14 |
| 5% | 0,05 | 18,43 |
| 9% | 0,01 | **76,78** |
| 10% | 0,00 | **errore** |

Da 3% a 9% il valore si moltiplica per cinque e mezzo. Un modello con `g` al 9% e
`wacc` al 10% non è aggressivo: è rotto, e sembra funzionare benissimo.

Nella matrice di sensibilità le celle con `wacc ≤ g` valgono `None`. Il buco resta
visibile invece di essere riempito con un numero enorme.

---

## 5 · Perché `g` deve stare sotto il tasso privo di rischio

La crescita perpetua è l'ipotesi più modesta in apparenza e la più impegnativa
nella sostanza: **per sempre** significa per sempre.

Il ragionamento, dovuto a Damodaran, è di ordine di grandezza. Il tasso privo di
rischio a lungo termine incorpora l'inflazione attesa e la crescita reale attesa
dell'economia: è quindi una buona approssimazione della **crescita nominale
dell'economia nel suo complesso**. Un'azienda che cresce per sempre più
dell'economia in cui vive, prima o poi, *diventa* l'economia — il che è un modo
educato per dire che l'ipotesi è impossibile, non solo ottimista.

Da qui la linea guida: **`g_terminal` non supera il tasso privo di rischio** usato
per costruire il `wacc`.

Nel motore il controllo è un **allarme, non un errore**: quando `g_terminal >
risk_free` viene emesso `G_SOPRA_RISK_FREE` e il calcolo prosegue. La scelta è
deliberata — esistono casi discutibili, per esempio un'azienda esposta a
un'economia che cresce più di quella in cui è quotata — ma vanno **argomentati nel
report**, non nascosti in un campo.

Con una conseguenza da tenere presente: `risk_free` è opzionale, e se non lo si
valorizza **l'allarme non può scattare**. Il silenzio, in quel caso, non è
un'assoluzione.

---

## 6 · Quando il valore terminale pesa troppo

Il motore emette `TV_DOMINANTE` quando `pv_terminal` supera l'**85%**
dell'enterprise value. Nel caso di riferimento siamo all'83,2%: sotto la soglia,
per poco.

Come si muove quella quota, sempre sullo stesso modello:

| Combinazione | Quota del TV sull'EV | Allarme |
|---|---|---|
| `wacc` 12%, `g` 2% | 78,0% | no |
| `wacc` 10%, `g` 3% (base) | 83,2% | no |
| `wacc` 8%, `g` 5% | **91,4%** | sì |

Un `wacc` basso e una `g` alta spingono valore nella coda per pura aritmetica.

**Che cosa significa un TV dominante.** Non che il modello sia sbagliato: che sta
dicendo qualcosa di diverso da quello che sembra. Con il 91% del valore nel
terminale, il modello **non sta valutando i cinque anni espliciti** — sta
esprimendo un'opinione su ciò che accade dal sesto anno in poi, e i cinque anni
sono poco più di un raccordo.

È legittimo, per un'azienda giovane in forte crescita è persino inevitabile.
Quello che non è legittimo è **presentarlo come se il valore venisse dalle ipotesi
operative**. Quando l'allarme scatta, il report deve dire in chiaro quale quota
del valore sta nella coda.

---

## 7 · Il caso `roic_terminal` ≤ `g_terminal` — il motore si ferma

**Il motore lo blocca con un errore esplicito.** Non è una nota di cautela: è una
delle condizioni di validità della formula, come `wacc > g_terminal`.

Se `roic_terminal` è uguale a `g_terminal`, il fattore `(1 − g/ROIC)` vale **zero**:
il tasso di reinvestimento è il 100%, tutto il NOPAT torna dentro l'azienda per
finanziare la crescita, e il flusso libero è nullo. Il valore terminale è zero. Ha
un significato preciso — **una crescita che rende esattamente quanto costa non crea
valore** — ma non è un fair value: è un modello che ha smesso di dire qualcosa.

Se `roic_terminal` è **minore** di `g_terminal`, il fattore diventa negativo e il
valore terminale con lui. Aritmeticamente coerente — per crescere così in fretta
con un ritorno così basso bisognerebbe immettere capitale all'infinito — ma il
risultato non è una valutazione: è la descrizione di una combinazione che non
esiste come stato stazionario.

In entrambi i casi il motore **solleva `DcfError` e non restituisce niente**. È la
stessa famiglia di `wacc ≤ g_terminal`, e riceve lo stesso trattamento per la
stessa ragione: un valore terminale nullo o negativo esce dal modello come un
numero plausibile, con la virgola al posto giusto, e nessuno si accorge che sotto
non c'è nessuna azienda. Le celle della matrice di sensibilità che finiscono in
questa condizione restano **vuote**, come quelle in cui il WACC non supera `g`.

Cosa farne, quando capita: non si aggira alzando il ROIC finché il motore riparte.
Le due ipotesi vanno riportate a coerenza guardando quale delle due è debole — di
norma è la crescita perpetua, non la barriera competitiva.

---

## 8 · Riepilogo

```
g_terminal ...... float, %.  Sotto risk_free. Sempre sotto wacc, o e' errore.
roic_terminal ... float, %.  Solo qui. Barriera competitiva nominabile.
                             Sempre sopra g_terminal, o e' errore.
```

Quattro cose da ricordare:

1. Il valore terminale pesa l'**80-85%**: è lì che va speso il controllo.
2. Il fattore `(1 − g/ROIC)` **cambia con `g`**. Dimenticarlo vale +21% di valore;
   calcolarlo una volta sola sbaglia le colonne esterne della sensibilità.
3. `wacc > g_terminal` **e** `roic_terminal > g_terminal` non sono
   raccomandazioni: sono le due condizioni perché la formula significhi qualcosa.
   Su entrambe il motore si ferma, e fa bene.
4. Se il TV supera l'85% dell'enterprise value, il modello sta parlando del sesto
   anno in poi. Va detto, non nascosto.

Il file successivo, `05-reverse-dcf.md`, prende tutto questo e lo rovescia: invece
di chiedere quanto vale l'azienda date certe ipotesi, chiede **quali ipotesi il
prezzo di mercato stia già scontando**. È spesso la domanda più utile delle due.
