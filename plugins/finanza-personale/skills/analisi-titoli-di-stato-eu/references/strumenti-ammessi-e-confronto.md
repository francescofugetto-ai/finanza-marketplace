# Strumenti ammessi (governativi euro) e confronto bond singolo vs ETF

Tassonomia dei titoli di Stato area euro utilizzabili nel mandato, con funzione, fiscalità e trappole; e il framework per confrontare **onestamente** un bond singolo con un ETF governativo. Nessun dato (ISIN, prezzo, YTM) va riportato a memoria: qui ci sono **categorie e criteri**, non titoli specifici.

## Indice
1. Perimetro e white-list
2. Titoli italiani
3. Governativi esteri white-list
4. Sovranazionali
5. Framework di confronto: bond singolo vs ETF governativo
6. Criteri di selezione del singolo titolo

---

## 1. Perimetro e white-list

**Ammessi:** titoli di Stato dell'area euro emessi da Paesi **white-list** (12,5%) — Italia, Germania, Francia, Spagna e altri Paesi white-list — più sovranazionali/equiparati white-list. **Esclusi** (per mandato): corporate singoli, subordinate, perpetue, high yield singolo, derivati, leva, strutturati. Gli **ETF obbligazionari** entrano solo come **benchmark di confronto**.

La white-list (D.Lgs. 239/1996; DM 4/9/1996 e aggiornamenti) determina il **12,5%**. I major EU sovereign sono white-list; verifica se hai dubbi su un emittente meno comune.

## 2. Titoli italiani

- **BTP (nominali):** cedola fissa semestrale, scadenze da brevi a lunghissime. Il mattone base della ladder. 12,5%. Rischio-emittente Italia (spread) da modellare.
- **BOT:** zero-coupon, scadenze ≤12 mesi. Rendimento tutto da scarto, 12,5%. Duration ≈ vita residua. Utili per il gradino brevissimo/parcheggio.
- **CCTeu (tasso variabile):** cedola Euribor 6m + spread. **Duration ≈ 0**, prezzo molto stabile → parcheggio a bassa volatilità **al 12,5%** (alternativa white-list all'ETF monetario, tassato 26%). **Non** ha YTM fisso ex-ante: valuta a prezzo/margine, non con l'IRR fisso.
- **BTP€i (indicizzati all'inflazione europea):** capitale e cedole rivalutati con **HICP eurozona ex-tabacco**. Tenuti a scadenza **bloccano i flussi reali**. Prezzo scontato al **tasso reale** (se i tassi reali salgono, scendono nonostante l'inflazione). 12,5%. Per la protezione del potere d'acquisto **in euro**.
- **BTP Italia (indicizzati all'inflazione italiana):** indicizzati al **FOI** nazionale, cedole semestrali su capitale rivalutato, **premio fedeltà** per chi detiene alla scadenza (retail). 12,5%. Copre l'inflazione *italiana* (rilevante per spese domestiche).
- **BTP Valore:** retail-only, **cedole step-up** crescenti + premio fedeltà finale; sottoscrivibile alla pari in emissione, poi negoziabile. 12,5%. Semplice, pensato per il piccolo risparmiatore che tiene a scadenza.

**Dosaggio inflation-linked:** usa il **break-even inflation** (vedi `curva-e-contesto.md`) per decidere IL vs nominale. Soglia di rilevanza dalla dottrina canone: sotto ~5-10% della gamba l'IL è simbolico e non sposta nulla; riferimento **1/3-1/2 della gamba obbligazionaria** in IL se la protezione reale è priorità. Preferisci l'IL **singolo tenuto a scadenza** (blocca i flussi reali) all'IL-ETF (che non scade) per un mandato di preservazione.

## 3. Governativi esteri white-list

- **Bund / Bobl / Schatz (Germania):** massima qualità di credito dell'area, benchmark "core". Cedole spesso basse/nulle → molti sono comprati **sotto la pari** (utile a scadenza al 12,5%). Diversificano il **rischio-emittente** rispetto ai BTP. Sono in euro → **nessun rischio cambio**.
- **OAT (Francia), Bonos (Spagna):** governativi core/semi-core in euro, white-list (12,5%), utili per diversificare l'emittente restando in euro.
- **Regola cambio:** finché si resta su emittenti **in euro**, non c'è rischio valuta. Un governativo in **valuta estera** (es. Treasury USA, Gilt) introduce rischio cambio che **domina** la funzione difensiva → per un euro-investitore va **coperto (hedge EUR)**, e in un mandato di preservazione in genere non aggiunge valore rispetto ai governativi euro. Ricorda che un titolo **estero** può avere trattamento fiscale/operativo diverso: verifica.

## 4. Sovranazionali

Emittenti come **BEI/EIB, ESM, UE (NGEU)**: alta qualità, in euro, in genere white-list/equiparati (verifica). Possono offrire diversificazione d'emittente e talvolta spread interessanti. Trattali come i governativi core, verificando white-list e liquidità.

## 5. Framework di confronto: bond singolo vs ETF governativo

Quando l'utente chiede "meglio il BTP o l'ETF governativo?", il confronto è legittimo **solo a parità di netto** e di funzione. Passi:

1. **Porta entrambi al netto reale.** Singolo: YTM netto 12,5% (cedole + scarto/plus) − bollo, deflazionato. ETF: rendimento a scadenza dell'indice **meno TER**, tassazione 26% con riduzione a 48,08% sulla quota white-list (≈12,5% effettivo *su quella quota*), − bollo, deflazionato. Non confrontare un lordo con un netto.
2. **Confronta la funzione, non solo il numero.**
   - **Certezza a scadenza:** singolo sì (flusso e capitale a data nota); ETF no (non scade, duration perpetua).
   - **Duration:** singolo decrescente e controllabile; ETF costante (roll).
   - **Diversificazione emittente:** ETF alta per costruzione; singolo da costruire con più titoli.
   - **Costi:** singolo nessun TER; ETF TER ricorrente.
   - **Operatività:** ETF più semplice (un ordine, PAC); singolo richiede gestione della ladder.
   - **Fiscalità:** singolo 12,5% pieno/certo; ETF ≈12,5% effettivo solo sulla quota white-list, dipendente dal pass-through.
3. **Verdetto secondo il mandato.** Per **accumulo/orizzonte lungo** l'ETF è spesso più pratico (tesi The Bull). Per **preservazione/decumulo con flussi datati e cap di perdita**, il **singolo white-list a scadenza** vince su certezza, controllo di duration e fiscalità certa — a costo di più gestione. Esplicita il trade-off; non nascondere i pregi dell'ETF (diversificazione, semplicità).

Onestà intellettuale: **non** affermare un divario fiscale di 13,5 punti "su tutto" (sarebbe falso: l'ETF governativo euro puro è ≈12,5% effettivo sulla quota white-list). Il vantaggio del singolo è **certezza + nessun TER + maturità definita + semplicità del 12,5%**, non un divario di aliquota generalizzato.

## 6. Criteri di selezione del singolo titolo

A parità di scadenza-obiettivo e di merito d'emittente, preferisci il titolo con:
- **miglior YTM netto reale** (dopo 12,5%/bollo/scarto, deflazionato);
- **carry + roll-down** favorevole per unità di duration (senza allungare oltre il bisogno);
- **liquidità** adeguata sul MOT/EuroTLX (spread bid-ask contenuto, taglio/lotto compatibile);
- **fiscalità pulita:** white-list (12,5%); se comprato sotto la pari, utile a scadenza a bassa tassazione;
- **coerenza con la diversificazione d'emittente** della ladder (non concentrare troppo su un solo nome/Paese);
- **negoziabilità sul broker** dell'investitore (Fineco): verifica accesso al mercato e costi.

Tutti i dati specifici (ISIN, prezzo, YTM, TER dell'ETF di confronto) si **verificano live** (vedi `protocollo-verifica-isin.md`), mai a memoria.
