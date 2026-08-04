# Metodologia BOTTOM-UP (capital market assumptions)

Il metodo delle grandi case: partire da aziende, settori e scenari macro per arrivare a stime di rendimento a 10 anni per asset class. **È previsione dalla prima all'ultima riga** — per questo ha rango subordinato al top-down (conflitto **C-K** del canone). Ma non si butta: è il **controllo incrociato** e la **misura dell'incertezza**.

---

## 1. A cosa serve davvero

| Serve per | NON serve per |
|---|---|
| Validare il top-down per confronto | Rispondere a "quanto renderà" |
| Misurare la **dispersione** = incertezza reale | Fissare le aspettative dell'investitore |
| Capire i **rischi** e gli scenari di rottura | Innescare una mossa tattica |
| Alimentare gli scenari prudente/ottimista della Monte Carlo | Sostituire la stima primaria |

`[TB-339]`: *"le storie di BlackRock e Amundi sono utilissime per capire i rischi, per non farsi trovare impreparati… Ma per rispondere alla domanda 'quanto renderà', il foglietto con due addizioni resta la palla di cristallo migliore che abbiamo."*

---

## 2. Le cinque case di riferimento

Set canonico usato in `[TB-339]`, da aggiornare a ogni pubblicazione:

| Casa | Pubblicazione | Cadenza tipica |
|---|---|---|
| **BlackRock** (Investment Institute) | Capital Market Assumptions | continua/trimestrale |
| **J.P. Morgan Asset Management** | Long-Term Capital Market Assumptions (LTCMA) | annuale (autunno) + midyear |
| **Amundi** (Amundi Investment Institute) | Capital Market Assumptions | annuale + outlook semestrale |
| **Capital Group** | Long-Term Outlook / CMA | annuale |
| **Charles Schwab** | 10-Year Market Outlook | annuale/semestrale |

Utili anche, quando servono numeri euro-nativi o accademici: **Vanguard** (VCMM, pubblica una versione area euro), **Research Affiliates** (Asset Allocation Interactive, gratuito e trasparente sul metodo), **AQR** (Capital Market Assumptions, dichiara la crescita reale per azione), **Damodaran** (ERP implicito mensile, gratuito).

> Research Affiliates e Damodaran sono **top-down travestiti da bottom-up**: partono anch'essi dai rendimenti impliciti. Se servono per il confronto, dichiararlo — non sono un test indipendente.

---

## 3. Le quattro trappole del confronto

Prima di mettere una CMA accanto a un numero top-down, verificare **tutte e quattro**. Se anche una sola non è verificabile, dichiararlo nel report.

### 3.1 Base valutaria
Le CMA sono tipicamente in **USD**. Il portafoglio è in **EUR**. Una CMA in USD per l'azionario globale non è confrontabile con un top-down in EUR senza conoscere l'assunzione di cambio della casa. J.P. Morgan e Vanguard pubblicano versioni in EUR: **preferirle**. Se si usa la versione USD, dirlo esplicitamente.

### 3.2 Orizzonte
BlackRock ~10 anni, JPM 10-15 anni, Schwab 10 anni, Capital Group 20 anni su alcune serie. Confrontare stime a 10 e a 20 anni come se fossero la stessa cosa è un errore silenzioso.

### 3.3 Geometrico vs aritmetico
Alcune case pubblicano rendimenti **aritmetici** (media annua semplice), altre **geometrici/compounded**. La differenza è `≈ σ²/2`: su un'azionaria con σ = 16% sono **1,3 punti**. JPM pubblica entrambi nelle tabelle LTCMA. Il top-down `DY+g` è **geometrico**. Confrontare geometrico con aritmetico crea un divario fantasma di oltre un punto.

### 3.4 Nominale vs reale
Verificare l'assunzione di inflazione della casa e, se necessario, riportare tutto in reale prima di confrontare.

---

## 4. Il bias commerciale — da nominare, senza malignità

`[TB-339]`: *"le società di asset management vendono prodotti di investimento. Senza voler essere maligni a tutti i costi, bisogna però tenere in considerazione che ciascuna società avrà qualche bias a seconda di dove sta puntando come strategia commerciale."*

Come si manifesta e come si gestisce:
- **Coerenza fra vista e prodotto**: una casa forte sui prodotti tematici AI tenderà a stime USA/tech più generose; una casa europea a stime europee più generose.
- **Regola operativa**: usare la **mediana** o la **media**, mai una singola casa. E riportare **sempre il range**, non solo il centro.
- **Segnale di allarme**: quando una casa è isolata di oltre 1,5 pt dalle altre sulla stessa asset class, la sua stima non aggiunge informazione — aggiunge posizione.

Esempio dal set lug-2026: S&P 500 a 10 anni, BlackRock **8,5%** contro Schwab e Capital Group **6,1%**. Un divario di **2,4 punti** sulla stessa asset class allo stesso momento. Su 25 anni sono ~78% di capitale terminale di differenza. *È questa la misura onesta dell'incertezza del bottom-up*, e va mostrata all'investitore.

---

## 5. Procedura di ricomposizione sui pesi del portafoglio

1. **Recupera le CMA correnti** (vedi `fonti-dati.md` §3). Registra per ciascuna: casa, data di pubblicazione, orizzonte, valuta, convenzione.
2. **Mappa** ogni gamba del portafoglio sulla riga CMA più vicina. Se la mappatura è approssimativa, dichiararla (es. "MSCI USA ≈ riga S&P 500").
3. **Calcola la media e il range** per riga, casa per casa.
4. **Ricomponi** sui pesi rinormalizzati del portafoglio, **esattamente come per il top-down**:
   `E[r]_BU = Σ w_i × media_CMA_i`
5. **Ricomponi anche gli estremi**: `E[r]_BU_min` (usando il minimo per riga) e `E[r]_BU_max`. Questi due alimentano gli scenari prudente/ottimista della Monte Carlo.
6. **Confronta** con il top-down e classifica:

| Divergenza | Lettura | Cosa fare |
|---|---|---|
| < 0,5 pt | Convergenza | Validazione incrociata. Usa il top-down, cita la convergenza. |
| 0,5 – 1,5 pt | Fisiologica | Usa il top-down, mostra il range come misura d'incertezza. |
| > 1,5 pt | **Anomalia** | **Nominala e spiegala**: le case stanno prezzando qualcosa che il top-down non vede (ΔV atteso, cambio, revisione degli utili), oppure c'è un errore di confronto (§3). **Non mediare in silenzio.** |

**Cross-check di riferimento (lug-2026)**: ricomponendo il bottom-up sui pesi ACWI (US 63,6% / dev ex-US ~25,3% / EM ~11,1%) si ottiene **6,92%** contro **6,67%** top-down. Divergenza 0,25 pt = convergenza. È il risultato che rende il top-down utilizzabile senza scuse.

---

## 6. Come si presenta all'investitore

Tre righe, non tre pagine:

1. *"La stima calcolata sui numeri di oggi dice **X%**."*
2. *"Le cinque grandi case dicono in media **Y%**, con un range da **A** a **B** — e il range è la misura onesta di quanto nessuno lo sa."*
3. *"Prendiamo **X** per pianificare, e teniamo **A** come scenario prudente."*

Aggiungere sempre il promemoria di `[TB-339]`: *"anche chi gestisce migliaia di miliardi non ha la palla di cristallo"* — e che le case partono dagli stessi temi arrivando a prescrizioni opposte (BlackRock sovrappesa USA, Amundi è quasi speculare). **Gli outlook servono a capire gli scenari, non a ricevere istruzioni.**
