#!/usr/bin/env python3
"""
Monte Carlo per portafogli (PIC + PAC) — single-asset o MULTI-ASSET correlato.

DUE MODALITA':
 1) Aggregata: fornisci exp_return + volatility di PORTAFOGLIO.
 2) Multi-asset: fornisci "assets" (lista) + "correlation" (matrice NxN).
    Gli asset sono simulati separatamente con shock CORRELATI (Cholesky),
    ribilanciati periodicamente o lasciati driftare. La volatilita' di
    portafoglio emerge dalle correlazioni (< media pesata = diversificazione).

Output (identico nelle due modalita', con extra per il multi-asset):
  - lordo / netto-costi / netto-netto (reale)
  - bande percentili annuali (fan-chart), distribuzione terminale
  - P(obiettivo), money multiple, shortfall, prob. perdita reale
  - [multi-asset] portfolio_implied (rend/vol di portafoglio) + echo assets

USO:
  python3 montecarlo.py config.json risultati.json
  echo '{...}' | python3 montecarlo.py - -

Niente e' inventato: tutte le assunzioni sono nel config.
Strumento di pianificazione probabilistica, non una previsione.
"""
import sys, json

try:
    import numpy as np
except ImportError:  # pragma: no cover
    # Il motore e' vettorizzato: 20.000 percorsi su 300 periodi sono 6 milioni di
    # estrazioni, e la fattorizzazione di Cholesky serve per gli shock correlati.
    # Una riscrittura in Python puro girerebbe due ordini di grandezza piu' lenta
    # e con una matematica diversa da quella dei vettori registrati: meglio un
    # errore che dice cosa fare, subito, che un risultato ottenuto in un altro modo.
    sys.stderr.write(
        "\n[montecarlo] Manca numpy: questo motore non puo' girare senza.\n"
        "Installalo nell'ambiente in cui esegui lo script:\n"
        "    pip install numpy            (oppure)\n"
        "    pip install --break-system-packages numpy\n"
        "Verifica con:  python3 -c \"import numpy; print(numpy.__version__)\"\n\n"
    )
    raise SystemExit(3)

DEFAULTS = {
    "initial": 0.0, "contribution": 0.0, "contribution_growth": 0.0,
    "years": 20, "periods_per_year": 12,
    "exp_return": 0.06, "volatility": 0.15, "ter": 0.0022, "entry_cost": 0.0,
    "inflation": 0.02, "n_paths": 20000,
    "dist": "lognormal", "t_df": 5,
    "goal": None, "goal_year": None, "real_goal": True,
    "contribute_timing": "begin", "seed": 42,
    # multi-asset (opzionali):
    "assets": None,            # lista di {name, weight, exp_return, volatility, ter}
    "correlation": None,       # matrice NxN (lista di liste); None => identita'
    "rebalance": "annual",     # "annual" | "none" | intero = ogni N periodi
}
PCTS = [5, 10, 25, 50, 75, 90, 95]


def per_period_logparams(mu_annual, sigma_annual, ppy):
    s = np.asarray(sigma_annual) / np.sqrt(ppy)
    m = np.log1p(np.asarray(mu_annual)) / ppy - 0.5 * s * s
    return m, s


def safe_cholesky(corr):
    """Cholesky robusta: se la matrice non e' PSD, clip degli autovalori."""
    corr = np.asarray(corr, dtype=float)
    try:
        return np.linalg.cholesky(corr), None
    except np.linalg.LinAlgError:
        w, V = np.linalg.eigh(corr)
        w = np.clip(w, 1e-8, None)
        fixed = V @ np.diag(w) @ V.T
        d = np.sqrt(np.diag(fixed))
        fixed = fixed / np.outer(d, d)
        return np.linalg.cholesky(fixed), "matrice di correlazione non PSD: corretta col clipping degli autovalori"


def _percentile_bands(snaps, years_axis, deflate):
    out = {}
    for y in years_axis:
        arr = snaps[y] / deflate(y)
        out[y] = {f"p{p}": float(np.percentile(arr, p)) for p in PCTS}
    return out


def _stats(arr):
    return {"mean": float(arr.mean()), **{f"p{p}": float(np.percentile(arr, p)) for p in PCTS}}


def simulate(cfg):
    rng = np.random.default_rng(cfg["seed"])
    ppy = int(cfg["periods_per_year"])
    T = int(round(cfg["years"] * ppy))
    n = int(cfg["n_paths"])
    years_axis = list(range(0, int(cfg["years"]) + 1))
    infl = cfg["inflation"]
    deflate = lambda y: (1.0 + infl) ** y
    warnings = []

    multi = cfg.get("assets")
    if multi:
        assets = cfg["assets"]
        N = len(assets)
        w = np.array([a["weight"] for a in assets], dtype=float)
        if abs(w.sum() - 1.0) > 1e-6:
            warnings.append(f"pesi non sommano a 1 ({w.sum():.3f}): normalizzati")
            w = w / w.sum()
        mu = np.array([a["exp_return"] for a in assets], dtype=float)
        sig = np.array([a.get("volatility", cfg["volatility"]) for a in assets], dtype=float)
        ter = np.array([a.get("ter", 0.0) for a in assets], dtype=float)
        corr = np.array(cfg["correlation"], dtype=float) if cfg.get("correlation") is not None else np.eye(N)
        L, warn = safe_cholesky(corr)
        if warn:
            warnings.append(warn)

        mg, sg = per_period_logparams(mu, sig, ppy)
        mn, sn = per_period_logparams(mu - ter, sig, ppy)

        init = float(cfg["initial"])
        Ag = np.outer(np.full(n, init), w)   # ricchezza per-asset, lordo (n,N)
        An = np.outer(np.full(n, init), w)   # netto
        base_contrib = float(cfg["contribution"]) * (1.0 - cfg["entry_cost"])
        cg = cfg["contribution_growth"]; timing = cfg["contribute_timing"]
        rb = cfg["rebalance"]
        rb_every = ppy if rb == "annual" else (int(rb) if isinstance(rb, (int, float)) and rb not in (0, "none") else None)

        snap_g = {0: Ag.sum(1)}; snap_n = {0: An.sum(1)}; contributed = init
        for t in range(1, T + 1):
            Zc = rng.standard_normal((n, N)) @ L.T
            gg = np.exp(mg[None, :] + sg[None, :] * Zc)
            gn = np.exp(mn[None, :] + sn[None, :] * Zc)
            contrib = base_contrib * ((1.0 + cg) ** ((t - 1) // ppy))
            cvec = contrib * w
            if timing == "begin":
                Ag = (Ag + cvec) * gg; An = (An + cvec) * gn
            else:
                Ag = Ag * gg + cvec; An = An * gn + cvec
            contributed += contrib
            if rb_every and t % rb_every == 0:
                tg = Ag.sum(1, keepdims=True); Ag = tg * w
                tn = An.sum(1, keepdims=True); An = tn * w
            if t % ppy == 0:
                snap_g[t // ppy] = Ag.sum(1); snap_n[t // ppy] = An.sum(1)

        # rendimento/vol IMPLICITI di portafoglio (analitici)
        cov = np.outer(sig, sig) * corr
        port_vol = float(np.sqrt(w @ cov @ w))
        port_mu_gross = float(w @ mu)
        port_mu_net = float(w @ (mu - ter))
        weighted_avg_vol = float(w @ sig)
        portfolio_implied = {
            "exp_return_gross": port_mu_gross, "exp_return_net": port_mu_net,
            "volatility": port_vol, "weighted_avg_volatility": weighted_avg_vol,
            "diversification_vol_saving": weighted_avg_vol - port_vol,
            "weighted_ter": float(w @ ter),
        }
        assumptions_echo = {**{k: cfg[k] for k in cfg},
                            "exp_return": port_mu_gross, "volatility": port_vol, "ter": float(w @ ter)}
    else:
        # ---- modalita' aggregata (single-asset) ----
        mu_gross = cfg["exp_return"]; mu_net = cfg["exp_return"] - cfg["ter"]; sigma = cfg["volatility"]
        mg, sg = per_period_logparams(mu_gross, sigma, ppy)
        mn, sn = per_period_logparams(mu_net, sigma, ppy)
        if cfg["dist"] == "t":
            df = float(cfg["t_df"]); z = rng.standard_t(df, size=(T, n)) * np.sqrt((df - 2) / df)
        else:
            z = rng.standard_normal(size=(T, n))
        gg = np.exp(mg + sg * z); gn = np.exp(mn + sn * z)
        init = float(cfg["initial"]); Wg = np.full(n, init); Wn = np.full(n, init)
        base_contrib = float(cfg["contribution"]) * (1.0 - cfg["entry_cost"])
        cg = cfg["contribution_growth"]; timing = cfg["contribute_timing"]
        snap_g = {0: Wg.copy()}; snap_n = {0: Wn.copy()}; contributed = init
        for t in range(1, T + 1):
            contrib = base_contrib * ((1.0 + cg) ** ((t - 1) // ppy))
            if timing == "begin":
                Wg = (Wg + contrib) * gg[t - 1]; Wn = (Wn + contrib) * gn[t - 1]
            else:
                Wg = Wg * gg[t - 1] + contrib; Wn = Wn * gn[t - 1] + contrib
            contributed += contrib
            if t % ppy == 0:
                snap_g[t // ppy] = Wg.copy(); snap_n[t // ppy] = Wn.copy()
        portfolio_implied = None
        assumptions_echo = {k: cfg[k] for k in cfg}

    # ---- output comune ----
    bands = {
        "gross": _percentile_bands(snap_g, years_axis, lambda y: 1.0),
        "net":   _percentile_bands(snap_n, years_axis, lambda y: 1.0),
        "real":  _percentile_bands(snap_n, years_axis, deflate),
    }
    gy = int(cfg["goal_year"]) if cfg["goal_year"] else int(cfg["years"])
    gy = max(0, min(gy, int(cfg["years"])))
    termG = snap_g[gy]; termN = snap_n[gy]; termR = termN / deflate(gy)

    terminal = {"at_year": gy, "gross": _stats(termG), "net": _stats(termN),
                "real": _stats(termR), "total_contributed": float(contributed)}
    mm = termN / max(contributed, 1e-9)
    terminal["money_multiple_net"] = {f"p{p}": float(np.percentile(mm, p)) for p in PCTS}
    init0 = float(cfg["initial"])
    if float(cfg["contribution"]) == 0.0 and init0 > 0 and gy > 0:
        cagr = (termN / init0) ** (1.0 / gy) - 1.0
        terminal["cagr_net_pct"] = {f"p{p}": float(np.percentile(cagr, p)) for p in PCTS}
    else:
        terminal["cagr_net_pct"] = None

    goal_block = None
    if cfg["goal"] is not None:
        goal = float(cfg["goal"]); compare = termR if cfg["real_goal"] else termN
        sf = goal - compare; sfp = sf[sf > 0]
        goal_block = {"goal": goal, "basis": "real" if cfg["real_goal"] else "net_nominal",
                      "p_goal": float((compare >= goal).mean()),
                      "median_value": float(np.percentile(compare, 50)),
                      "median_shortfall_if_miss": float(np.median(sfp)) if sfp.size else 0.0,
                      "prob_miss": float((compare < goal).mean())}

    res = {
        "assumptions": assumptions_echo,
        "years_axis": years_axis, "bands": bands, "terminal": terminal,
        "goal": goal_block,
        "prob_loss_real_vs_contributed": float((termR < contributed).mean()),
        "percentiles_reported": PCTS,
        "warnings": warnings,
    }
    if portfolio_implied is not None:
        res["portfolio_implied"] = portfolio_implied
        res["assets"] = cfg["assets"]
        res["correlation"] = cfg.get("correlation")
    return res


def main():
    if len(sys.argv) >= 2 and sys.argv[1] != "-":
        cfg_in = json.load(open(sys.argv[1], encoding="utf-8"))
    else:
        cfg_in = json.load(sys.stdin)
    # Guardia sui nomi dei parametri. Una chiave sconosciuta non viene usata dal
    # motore, ma finisce comunque nel blocco "assumptions" dell'output: nel report
    # sembrerebbe un'assunzione applicata, mentre la simulazione ha girato con il
    # valore di default. Un numero sbagliato che si presenta come giusto e' peggio
    # di un errore. Qui non si blocca l'esecuzione — si dice a voce alta cosa e'
    # successo, su stderr, cosi' il risultato resta riproducibile.
    ignote = [k for k in cfg_in if k not in DEFAULTS]
    if ignote:
        noti = ", ".join(sorted(DEFAULTS))
        sys.stderr.write(
            "\n[montecarlo] ATTENZIONE — parametri non riconosciuti, quindi NON usati:\n"
            + "".join(f"    {k} = {cfg_in[k]!r}\n" for k in ignote)
            + "  La simulazione ha usato il valore di default per le grandezze corrispondenti.\n"
            "  Controlla i nomi: i piu' comuni sono 'exp_return' (non 'mu') e\n"
            "  'volatility' (non 'sigma'), 'n_paths' (non 'paths'), 'goal' (non 'target').\n"
            f"  Parametri riconosciuti: {noti}\n\n")

    cfg = {**DEFAULTS, **cfg_in}
    out = json.dumps(simulate(cfg), ensure_ascii=False, indent=2)
    if len(sys.argv) >= 3 and sys.argv[2] != "-":
        open(sys.argv[2], "w", encoding="utf-8").write(out); print(f"OK -> {sys.argv[2]}")
    else:
        print(out)


if __name__ == "__main__":
    main()
