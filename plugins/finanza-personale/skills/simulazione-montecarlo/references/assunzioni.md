# Assunzioni di mercato (punti di partenza, da confermare)

Il motore non inventa: i parametri sono input. **Gerarchia delle fonti per `exp_return`:**

1. **Calcolato** dalla skill `rendimenti-attesi-portafoglio` (top-down: `DY + g` per le azioni, `YTW + roll-down` per i bond, netto TER e bollo, datato e con fonte). **È la via preferita**: il rendimento atteso è osservabile nei prezzi di oggi, non va assunto.
2. **Capital market assumptions** correnti di una casa dichiarata, verificate su valuta / orizzonte / convenzione geometrica.
3. **Tabella sotto** — *fallback dichiarato*, da usare solo quando 1 e 2 non sono eseguibili, e **dicendolo nel report**.

La `volatility` e la matrice di **correlazione** restano assunzioni di questa skill: il top-down stima il rendimento, non il rischio.

Qui ci sono **punti di partenza ragionevoli** per `exp_return`, `volatility`, `inflation`, da **confermare/aggiornare** con l'utente e con dati live. Sono ordini di grandezza prudenti, non profezie; quando possibile verificare le *capital market assumptions* aggiornate (Vanguard, BlackRock, JPM, Damodaran per l'equity risk premium) e dichiarare la fonte e la data nel report.

## Tabella di riferimento (nominale, EUR, lungo termine)

> ⚠️ **Fallback, non default.** Se hai eseguito `rendimenti-attesi-portafoglio`, usa quei numeri. Questa tabella è un ordine di grandezza prudente per quando il calcolo non è possibile: dichiaralo esplicitamente nel report ("assunzione di default, non stima calcolata").

| Asset / portafoglio | Rend. atteso annuo | Volatilità annua | Note |
|---|---|---|---|
| Azionario globale (ACWI) | 5,5–7,0% | 14–16% | prudente vista valutazioni USA alte; non usare il +10% storico USA |
| Azionario USA | 5,0–6,5% | 15–17% | valutazioni elevate → aspettative più basse |
| Azionario EM | 6,0–8,0% | 18–22% | premio per rischio non prezzabile; vedi canone EM |
| Obbligazionario IG EUR (Agg) | 2,5–3,5% | 4–6% | ~ YTM corrente è lo "spoiler" del rendimento |
| Inflation-linked EUR | 1,5–2,5% reale | 5–7% | ragiona in reale |
| Oro | 3,0–5,0% | 14–16% | alta vol, vedi canone (oro high-beta) |
| Monetario/cash EUR | ≈ €STR corrente | <1% | rischio di reinvestimento |
| **Inflazione EU (lungo)** | **2,0–2,5%** | — | "3% is the new 2%": valutare scenari 2,5–3% |

Costi tipici: **TER** ETF 0,05–0,30% (core) fino a 0,40–0,60% (fattoriali/satelliti). Bollo 0,20%/anno sul dossier (aggiungibile come costo).

## Come scegliere `exp_return`/`volatility` di portafoglio

Due strade. (1) **Multi-asset (consigliata)**: passi gli asset separati con i loro `exp_return`/`volatility`/`ter` + la matrice di correlazione, e il motore calcola da sé la vol di portafoglio (più bassa della media pesata grazie alle correlazioni < 1). (2) **Aggregata**: stimi a mano un `exp_return`/`volatility` di portafoglio come media pesata dei rendimenti e vol di portafoglio **minore** della media pesata delle vol. In dubbio, **prudenza**: meglio sottostimare il rendimento e sovrastimare la vol.

### Matrice di correlazione di riferimento (long-term, indicativa)

|  | Azioni | Bond IG | Oro |
|---|---|---|---|
| **Azioni** | 1,00 | 0,15 | 0,10 |
| **Bond IG** | 0,15 | 1,00 | −0,10 |
| **Oro** | 0,10 | −0,10 | 1,00 |

Caveat (canone The Bull): la correlazione azioni-bond **non è stabile** — negativa nel 1981-2021, tornata positiva dal 2020; negli shock d'offerta scende tutto insieme. Per lo scenario di stress, **alza i coefficienti** (es. tutti a 0,7-0,9) e rigira: è il modo per vedere "quanto fa male se la diversificazione salta proprio quando serve".

### Esempio di config multi-asset (70/15/15, ribilanciamento annuale)

```json
{
  "assets": [
    {"name":"Azionario globale","weight":0.70,"exp_return":0.065,"volatility":0.16,"ter":0.0020},
    {"name":"Obbligazionario IG","weight":0.15,"exp_return":0.030,"volatility":0.05,"ter":0.0015},
    {"name":"Oro","weight":0.15,"exp_return":0.040,"volatility":0.15,"ter":0.0025}
  ],
  "correlation": [[1.0,0.15,0.10],[0.15,1.0,-0.10],[0.10,-0.10,1.0]],
  "rebalance": "annual",
  "initial": 30000, "contribution": 1000, "years": 20,
  "inflation": 0.02, "n_paths": 30000, "goal": 600000, "real_goal": true
}
```

## Disciplina

- **Mostra sempre le assunzioni nel report** (blocco dedicato): è ciò che separa uno strumento serio da una scatola nera.
- **Scenari, non punto singolo**: gira almeno un caso *prudente* e uno *ottimista*. **Quando disponibile, non usare scarti arbitrari: usa la dispersione reale delle capital market assumptions** prodotta da `rendimenti-attesi-portafoglio` — top-down = caso base, **minimo** delle CMA ricomposte = prudente, **massimo** = ottimista. È un intervallo *osservato* fra le case, non un ±1,5 pt inventato, e mostra all'investitore quanto realmente diverge chi fa questo di mestiere (sullo stesso S&P 500 a 10 anni le stime vanno da 6,1% a 8,5%). In assenza, resta lo scarto convenzionale (rendimento −1,5 pt, inflazione +0,5 pt). Una probabilità che regge solo nello scenario ottimista è un campanello.
- **Non spacciare la mediana per certezza**, né l'assunzione per dato. Se l'utente non sa che rendimento mettere, proponi questa tabella come default *dichiarato*, non come verità.
- Aggiorna i numeri: derivano dal contesto e invecchiano (vedi la disciplina "time-sensitive" del canone The Bull nella skill di portafoglio).
