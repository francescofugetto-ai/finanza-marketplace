# fra-finanza — marketplace privato

Un solo plugin, `finanza-personale`, che installa in un colpo tutte le skill di
finanza personale e la memoria decisionale condivisa fra i progetti.

## Contenuto

| Skill | Ruolo |
|---|---|
| `consulenza-portafogli-etf` | profilazione, asset allocation, canone The Bull, PIC/PAC |
| `analisi-titoli-di-stato-eu` | bond governativi singoli, YTM netto, ladder |
| `analisi-documenti-investimento` | distillazione fonti + gate segnale/rumore + design system |
| `rendimenti-attesi-portafoglio` | E[r] a 10 anni top-down e bottom-up |
| `simulazione-montecarlo` | distribuzione del capitale futuro, P(obiettivo) |
| `metodo-fiduciario` | dottrina e flusso di lavoro comuni a tutti i mandati — **entry point** |
| `kb-registro` | memoria decisionale trasversale ai progetti |

Le skill di dominio si citano fra loro **per percorso relativo**
(es. `consulenza-portafogli-etf/references/canone-the-bull/rendimenti-attesi.md`).
Per questo stanno tutte in **un unico plugin**: se fossero plugin separati finirebbero
in cartelle di cache diverse e quei rimandi si romperebbero.

## Struttura

```
fra-finanza/
├── .claude-plugin/marketplace.json
└── plugins/finanza-personale/
    ├── .claude-plugin/plugin.json
    └── skills/<sette skill>/
```

## Installazione

Da Claude Code o Cowork, una volta sola:

```
/plugin marketplace add <owner>/<repo>      # oppure ./percorso/locale per provarlo
/plugin install finanza-personale@fra-finanza
/reload-plugins
```

Su claude.ai (web e app desktop) il marketplace si aggiunge dal menu **Customize**.
Le skill del plugin funzionano in chat, desktop e Cowork; hook e sub-agent solo in Cowork.

## Aggiornamento

1. Modifica le skill **nel repo**, non nella cache di installazione.
2. `git push`.
3. Lato utente: prima `/plugin marketplace update fra-finanza`, poi
   `/plugin update finanza-personale`. In quest'ordine: aggiornare il plugin senza
   aver prima aggiornato il catalogo non serve a niente.
4. Verifica in una **chat nuova**: una conversazione gia' aperta continua a usare la
   versione che aveva all'avvio.

> **Questo plugin non ha, e non deve avere, un campo `version`.** E' una scelta
> deliberata, confermata dalla documentazione ufficiale (*Plugins reference —
> Version management*): omettendo `version` sia da `plugin.json` sia dalla voce di
> marketplace, la versione diventa il commit git, quindi **ogni push pubblicato conta
> come versione nuova** e l'aggiornamento arriva sempre. E' l'impostazione che la
> documentazione raccomanda per i plugin interni in sviluppo attivo.
>
> Se invece si imposta `version`, bisogna ricordarsi di alzarlo a ogni modifica: se lo
> si dimentica, Claude confronta il numero, lo trova identico e **non scarica nulla,
> senza alcun messaggio d'errore**. E' un guasto silenzioso, ed e' esattamente cio' che
> questa scelta evita. Non impostare `version` in due posti (`plugin.json` e voce di
> marketplace): vincerebbe `plugin.json`, in silenzio.

## Validazione prima di pubblicare

```
claude plugin validate .                        # marketplace.json + manifest
claude plugin validate ./plugins/finanza-personale   # frontmatter delle skill
```

## Note

- Nome marketplace: kebab-case obbligatorio. Evita i nomi riservati Anthropic
  (`anthropic-*`, `claude-*`, `first-party-plugins`, ...).
- Il repo puo' essere privato: l'installazione usa le credenziali git gia' configurate.
  Per gli aggiornamenti automatici in background su repo privati serve un remote SSH
  con chiave in `ssh-agent`, oppure `CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE=1`.
- Il connettore MCP locale `finanza` puo' essere dichiarato in `plugin.json` sotto
  `mcpServers`, usando `${CLAUDE_PLUGIN_ROOT}` per i percorsi. Funziona dove girano
  processi locali (Claude Code, Cowork/desktop), non da web o telefono.
