# Fonti, dati e igiene del dato

## Dove prendere i dati (verifica sempre live)

- **Strumento (ETF/ETC)**: KIID/KID e **factsheet dell'emittente** (iShares, Xtrackers, Amundi, SPDR, Invesco, Vanguard…) → TER, replica, domicilio, AUM, acc/dist, indice. Fonte primaria. Col connettore `finanza`, parti da `etf_anagrafica` (ISIN e denominazione da fonte ufficiale) e `documenti_prodotto` (link al factsheet giusto): TER e replica si leggono comunque sulla pagina dell'emittente, il connettore non li fornisce.
- **Confronto neutro**: **justETF** (TER, dimensione, rendimenti, composizione, lista ETF su un indice), Morningstar (rating, rischio), sito dell'**indice** (MSCI/FTSE/Bloomberg) per metodologia e composizione.
- **Mercato/macro**: prezzi e valutazioni live (P/E forward, tassi, spread, FX) via web; banche centrali e istituzioni per le proiezioni.
- **Articoli**: la fonte allegata; web_fetch per i link. Parafrasa, rispetta il copyright.

## Gerarchia di affidabilità

emittente/KIID/factsheet e banche centrali/istituzioni (BCE, Fed, FMI) > dati neutri (justETF, indici, Morningstar) > **sell-side** (analisti banche, incentivati al trading) > **marketing buy-side** (asset manager long-only, incentivo a "stay invested"). Quando due fonti confliggono, **esplicita il conflitto** e prendi posizione motivata.

## Igiene del dato (regola d'oro)

- **Non inventare.** Se un numero non è reperibile con certezza, scrivi **"n/d"** e dillo nel footer. Mai una stima spacciata per dato.
- **Data il report** e segnala che i dati di mercato vanno verificati al momento (cambiano di continuo). Dichiara anche **come** hai verificato: connettore `finanza` (fonti ufficiali incrociate) o verifica libera via web — nel secondo caso marca i dati `[verifica libera]`.
- Distingui sempre **dato storico** vs **stima/consensus** vs **opinione**.
- I numeri nel template e nel sample sono **placeholder illustrativi**, non dati correnti: sostituiscili.
- Coerenza unità (valuta, base index, %, bps) e arrotondamenti sensati; numeri in tabella con `.num` (incolonnati).

## Glossario metriche (per il confronto)

- **TER** *(Total Expense Ratio)*: costo annuo dichiarato del fondo, in % del capitale.
- **AUM** *(Asset Under Management)*: patrimonio del fondo; sotto ~100-500M € attenzione a liquidità/chiusura.
- **Sharpe** = (rendimento − risk-free) / volatilità: extra-rendimento per unità di rischio totale; >1 buono.
- **Volatilità** annualizzata: deviazione standard dei rendimenti.
- **Max drawdown**: perdita massima picco-minimo nel periodo.
- **Tracking error**: scostamento del rendimento dell'ETF dall'indice.
- **Replica**: fisica (compra i titoli) vs sintetica/swap (rischio controparte UCITS ≤10%).
- **Domicilio** IE/LU: rilevante per fiscalità (ritenute) e armonizzazione UCITS.
- **Overlap**: quota di titoli/esposizione già presente nel portafoglio (un satellite che ricompra il core non diversifica).
- **Esposizione geografica/settoriale**: da look-through, non dal nome (un fattoriale "World" può essere ~70% USA).
