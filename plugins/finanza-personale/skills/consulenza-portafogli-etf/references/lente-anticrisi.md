# Lente anticrisi — resilienza e decorrelazione, tassonomia separata

Questo file esiste per una ragione precisa: circolano **due elenchi diversi chiamati entrambi "5 pilastri"**, e fonderli produce un portafoglio con doppioni e un'architettura patrimoniale sbagliata. Qui si tengono separati, si dice quando la lente difensiva è pertinente, e si dà la regola anti-doppioni che l'una impone all'altra.

---

## 1 · I due elenchi non sono la stessa cosa

| | **5 pilastri di accumulo** (`architettura-5-pilastri.md`) | **5 mattoncini di resilienza** (lente anticrisi) |
|---|---|---|
| Che cosa sono | **architettura patrimoniale**: dove sta ogni euro e con che missione | **menu di strumenti** per attenuare i drawdown |
| Unità | bucket / pilastro (cash, emergenza, azionario, obbligazionario, diversificatori) | singolo ETF o classe di strumenti |
| Domanda a cui rispondono | *quanto e perché* | *con che cosa, se voglio smorzare* |
| Quando comanda | sempre | solo quando la resilienza è un obiettivo dichiarato |

**Regola.** L'architettura decide **prima**; la lente anticrisi al più popola il pilastro 5 e la parte difensiva del pilastro 4. Mai il contrario. Un menu di strumenti non è un'architettura, e trattarlo come tale porta a costruire il portafoglio a partire dai prodotti invece che dalle funzioni.

---

## 2 · I cinque mattoncini di resilienza, e che cosa fa ciascuno

1. **Obbligazionario a breve termine.** Smorza la volatilità e restituisce liquidità spendibile quando l'azionario è in perdita. Non protegge dall'inflazione. Il suo valore è la **disponibilità**, non il rendimento: è il mattoncino che evita di vendere azioni al momento peggiore.
2. **World Minimum Volatility.** Riduce la deviazione standard selezionando titoli a bassa volatilità storica. Costa: sottoperforma nei recuperi rapidi e incorpora un forte tilt implicito verso **low-vol e quality**.
3. **Settori difensivi** (Healthcare, Consumer Staples, Utilities). Cash-flow più stabili lungo il ciclo. Incorporano **lo stesso tilt low-vol/quality** del punto 2 — vedi §3.
4. **Managed futures / trend following.** È l'unico mattoncino con una decorrelazione *strutturale* e non solo statistica: guadagna dalla persistenza dei trend, quindi tende a funzionare nei drawdown **lenti** e a non funzionare nei crolli improvvisi. L'offerta UCITS per un investitore europeo è **ristretta**: verifica caso per caso disponibilità, TER, capacità e negoziabilità sul broker — questa è la gamba dove il divario fra la teoria e ciò che si può davvero comprare è più ampio.
5. **Oro.** Copre debasement monetario e paura, non l'inflazione in senso stretto. Nel regime recente si comporta più da **high-beta sul rischio-fiducia** che da rifugio: vedi `canone-the-bull/P5a-oro.md`. Non ha flusso di cassa, quindi **esce dal calcolo del rendimento atteso**.

---

## 3 · Regola anti-doppioni — la sola cosa di questo file che vale sempre

**Minimum Volatility e settori difensivi caricano lo stesso fattore.** Tenerli insieme non diversifica: raddoppia l'esposizione a low-vol/quality, somma due TER e produce un portafoglio che *sembra* più articolato di quanto sia. Se entrano entrambi, si sceglie quale porta il tilt e l'altro esce, oppure si dimezzano entrambi — non li si somma a pieno peso.

Vale anche il caso simmetrico e più comune: **un tilt Quality esplicito nella sleeve fattoriale rende ridondante il Min Vol**. Prima di aggiungere un mattoncino difensivo, verifica in look-through quale fattore è già presente e con che peso.

Il controllo di doppioni va fatto **in look-through**, non sui nomi degli strumenti: due ETF con etichette diverse possono contenere le stesse trenta società.

---

## 4 · Quando questa lente è pertinente, e quando no

**Non è pertinente** su un mandato di accumulo puro con orizzonte lungo e nessuna passività datata. Su un portafoglio 100% azionario a 25 anni gli unici due elementi operativi sono:

- la **terza gamba anti-inflazione** (oro / materie prime), se manca — dottrina in `canone-the-bull/inflazione.md`;
- la **diagnosi dei doppioni** del §3.

Tutto il resto sarebbe rischio ridotto pagato in rendimento atteso, su un orizzonte in cui il drawdown non è il vincolo binding.

**Diventa pertinente** quando: (a) ci si avvicina a un evento di finanziamento — acquisto casa, passaggio in decumulo; (b) esiste un **cap di perdita** dichiarato, e allora il dimensionamento della parte difensiva è un calcolo, non una preferenza; (c) il profilo comportamentale reale, non quello dichiarato, dice che l'investitore ha già venduto in un drawdown passato.

---

## 5 · Come si dichiara nel report

Se usi questa lente, dillo: *«mattoncini di resilienza, tassonomia distinta dall'architettura a 5 pilastri»*. Se non la usi su un mandato dove qualcuno se l'aspetta, dichiara **perché**: su un accumulo lungo la risposta è che la volatilità non è il rischio rilevante, l'abbandono del piano lo è — e a quello si risponde con la disciplina e con il bucket C, non comprando Min Vol.
