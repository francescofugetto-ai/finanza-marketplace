# Fase 6 — Materiali operativi e dossier

Si produce **solo dopo** che asset allocation e strumenti sono stati discussi e confermati con l'investitore. Tre deliverable, in quest'ordine: timeline operativa → simulazione Monte Carlo → dossier. Il Monte Carlo alimenta la "proiezione di rendimento" del dossier, quindi va prodotto prima.

Regola trasversale: questi materiali sono **educativi**, non promesse. Ogni proiezione mostra una **distribuzione di esiti** (incluso il downside), con **assunzioni esplicite**. Nessun numero "garantito".

---

## 1. Timeline operativa

Sequenza concreta e datata delle azioni, con **layout grafico accattivante** (timeline orizzontale o a tappe). Renderizzala come visual inline e/o inseriscila nel dossier.

Contenuti tipici (adatta al caso):
- **T0 — Setup:** scelta/apertura broker; verifica regime fiscale; costituzione di cash (Pilastro 1) e fondo emergenza (Pilastro 2).
- **T0–T+n mesi — Ingresso PIC:** lump-sum o tranche (se spalmatura comportamentale concordata), con importi e date.
- **Mensile — PAC:** importo e ripartizione per strumento; data di addebito.
- **Annuale / a soglie — Ribilanciamento:** quando e come (regola scritta).
- **Milestone — Glide-path:** date in cui si scorporano/de-rischiano obiettivi datati (es. de-risking ultimi ~5 anni di un goal).
- **Revisione periodica:** check annuale del piano (non per fare timing, ma per verificare coerenza con profilo, costi, condizioni broker).

Tieni il visual pulito: poche tappe, etichette brevi, un colore per tipo di azione.

---

## 2. Simulazione Monte Carlo (PIC + PAC)

Stima la **distribuzione** del montante futuro modellando insieme l'ingresso una tantum (PIC) e i versamenti periodici (PAC) sull'orizzonte dell'investitore. Esegui in Python (l'ambiente ha code execution).

### Input (da dichiarare sempre, esplicitamente)
- **Orizzonte** (anni) dal profilo.
- **PIC** iniziale e **PAC** periodico (importo, frequenza, eventuale crescita del versamento nel tempo).
- **Rendimento atteso e volatilità** del portafoglio, derivati dai pesi dei pilastri e da assunzioni di lungo periodo per asset class. **Dichiara le assunzioni** e, quando possibile, ancorale alle *capital market assumptions* raccolte in Fase 2 (es. BlackRock, Morningstar) invece di numeri inventati. In assenza di stime aggiornate, usa ipotesi prudenti e segnale come tali.
- **Costi** (TER medio ponderato) sottratti dal rendimento lordo.
- Lavora preferibilmente in termini **reali** (al netto dell'inflazione) oppure dichiara se nominali.

### Metodo
- Simula **molti percorsi** (es. 10.000). A ogni anno estrai un rendimento dalla distribuzione assunta (es. lognormale sui rendimenti, ossia normale sui log-rendimenti) e **aggiungi i versamenti PAC** lungo il percorso: così emerge il **sequence-of-returns risk** (l'ordine dei rendimenti conta quando si versa nel tempo).
- Sottrai i costi; se in reale, deflaziona.

### Output
- **Distribuzione** del montante finale e **percentili chiave**: 5°, 25°, **50° (mediana)**, 75°, 95°.
- **Capitale versato totale** vs montante, per percentile (mostra anche il caso sfavorevole in cui si resta vicini o sotto al versato).
- **Probabilità** di raggiungere eventuali obiettivi a importo/data noti.
- **Drawdown**: peggiori cali lungo i percorsi (max drawdown atteso/percentili), per dare il senso della sofferenza possibile.
- **Fan chart** (percorsi/percentili nel tempo) da inserire nel dossier.

### Caveat (sempre, vicino ai numeri)
- Non è una previsione: i risultati dipendono **interamente** dalle assunzioni; cambiando rendimento/volatilità cambiano gli esiti.
- Mostra **sempre** gli scenari sfavorevoli, non solo la mediana.
- I rendimenti passati non predicono quelli futuri; **il capitale può ridursi**.
- Il modello è una semplificazione (non cattura fat tails, regimi, cambi di correlazione): è uno strumento per *ragionare sugli ordini di grandezza*, non per fissare aspettative.

---

## 3. Dossier professionale

Documento di sintesi consegnabile all'investitore. **Tecnico ma accessibile, non lungo** (indicativamente 4–8 pagine).

### Specifiche di design
- **Formato di default: HTML**, nello stile del template di progetto (§8.2 delle istruzioni di progetto) — non ricrearlo da zero, replicane il sistema di design: `.kicker` (eyebrow maiuscolo) → `.article-headline`/`.article-sub` → `.box-purple`/`.box-warn`/`.box-accent`/`.box-danger`/`.box-success` (callout bordo sinistro colorato) → `.stat-row`/`.stat` (metriche chiave) → `table.cmp` (tabelle con `td.best`/`warn`/`danger`) → `.action-list` (checklist numerata) → `.conclusion-box.verdict` → `.footer-note`.
- **Sfondo chiaro** (bianco/grigio molto tenue #FAF9F7); ampi spazi bianchi.
- **Font chiaro**, sans-serif leggibile (Inter); gerarchia tipografica sobria.
- **Colori "meaningful":** assegna un colore coerente a ciascun asset/pilastro (riusando la palette blue/amber/red/green/purple del template) e **riusalo identico in tutti i grafici e tabelle**, così il lettore associa subito colore → componente. Evita palette arbitrarie o eccessive.
- Ricco di **grafici a torta/ciambella, barre e tabelle**; ogni grafico ha titolo e legenda chiari.

### Contenuti obbligatori
1. **Copertina** sobria + una riga sull'obiettivo.
2. **Profilo sintetico** (dalla Scheda Profilo): età, orizzonte, profilo di rischio, broker.
3. **Asset allocation** — grafico a torta dei pilastri/pesi + tabella.
4. **Tipologia di asset** — ripartizione per classe (azionario/obbligazionario/oro/liquidità) a torta o barre.
5. **Esposizione geografica** — torta/barre per area (USA, Europa, Pacifico, Emergenti…), aggregando i pesi reali sottostanti gli ETF.
6. **Strumenti** — tabella dei mattoncini con i campi **verificati** (ISIN, TER, replica, Acc/Dist, AUM, spread, costo zero sul broker) o marcati "da verificare".
7. **Timeline operativa** (dal punto 1).
8. **Proiezione di rendimento** — fan chart e percentili dal Monte Carlo, con le assunzioni dichiarate accanto.
9. **Max drawdown** — atteso/storico e cali peggiori dei percorsi simulati, come misura di rischio reale.
10. **Regole d'oro** (sotto).
11. **Disclaimer** completo.

### Regole d'oro (incl. quelle richieste; adatta/integra)
- **Non vendere mai in preda al panico né senza prima consultare il consulente di fiducia.**
- **Non cambiare strategia o asset allocation senza consultare il consulente di fiducia.**
- Mantieni il **PAC automatico**, soprattutto quando i mercati scendono.
- **Ribilancia per regola**, non per emozione né per previsione.
- **Ignora il rumore** di breve termine e le notizie allarmistiche.
- **Non inseguire la performance** (l'ultimo ETF/tema che ha corso).
- **Tieni i costi bassi** e verificali nel tempo.
- **Ricorda l'orizzonte:** il portafoglio è costruito per anni, non per mesi.
- **Hai già deciso** cosa fare a -10% / -20% / -30%: esegui il piano.

---

## Note tecniche di produzione
- Formato di default: **HTML**, nello stile del template di progetto (vedi Specifiche di design sopra). Salva nella cartella di output dell'ambiente (`metodo-fiduciario` §10) e condividi il file.
- `PDF` o `.docx` restano disponibili solo su **richiesta esplicita** (es. il dossier va stampato o firmato). In quel caso, prima di generare i file leggi la SKILL.md di produzione pertinente (`pdf` o `docx`, ed eventualmente `frontend-design`/`canvas-design` per il layout).
- Mantieni i colori coerenti tra timeline, grafici del dossier e fan chart del Monte Carlo.
- Consegna i file con `present_files` e una sintesi breve.
