#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rendimenti_attesi.py — motore per la stima del rendimento atteso di portafoglio.

Uso:
    python3 rendimenti_attesi.py config.json results.json
    python3 rendimenti_attesi.py --selftest

Metodo: vedi references/metodologia-top-down.md e references/metodologia-bottom-up.md.
Non inventa dati: ogni input è esplicito nel config e viene ricopiato nell'output
insieme a fonte e data, così il report può mostrarlo.

--------------------------------------------------------------------------------
SCHEMA DEL CONFIG (JSON)
--------------------------------------------------------------------------------
{
  "meta": {
    "label": "Portafoglio Mario Rossi",
    "as_of": "2026-06-30",              # data dei dati di mercato
    "base_currency": "EUR",
    "horizon_years": 25,
    "convention": "per-share",          # per-share | aggregate  (mai mischiare)
    "notes": "..."
  },

  "inflation": {"value": 0.021, "source": "BCE SPF long-term, Q2 2026"},

  "costs": {"bollo": 0.0020},           # patrimoniale annua (bollo / IVAFE)

  "tax": {                              # applicata AL TERMINE sul guadagno
    "equity_rate": 0.26,
    "bond_rate": 0.125,
    "apply": true
  },

  "portfolio": {
    "name": "Proposto",
    "sleeves": [
      # --- EQUITY: dividend_yield + real_growth (+ valuation_change, default 0)
      {"name": "USA", "kind": "equity", "weight": 0.40,
       "isin": "IE00B5BMR087", "ter": 0.0007,
       "dividend_yield": 0.0112, "real_growth": 0.027,
       "valuation_change": 0.0, "volatility": 0.16,
       "source": "MSCI USA factsheet 30/06/2026; g = AQR CMA 2026"},

      # --- BOND: ytw (+ roll_down, credit_loss, hedging_carry; default 0)
      {"name": "BTP", "kind": "bond", "weight": 0.30,
       "isin": null, "ter": 0.0,
       "ytw": 0.0335, "roll_down": 0.0, "credit_loss": 0.0,
       "hedging_carry": 0.0, "duration": 7.0, "volatility": 0.05,
       "tax_rate": 0.125,
       "source": "YTM medio ponderato da analisi-titoli-di-stato-eu"},

      # --- NON COMPUTABILE: esce dal calcolo, riduce la copertura
      {"name": "Oro", "kind": "non_computable", "weight": 0.10}
    ]
  },

  "benchmarks": [ { ...stessa struttura di "portfolio"... } ],

  # opzionale: abilita la correzione geometrica (richiede volatility su ogni sleeve)
  "correlation": [[1.0, 0.15], [0.15, 1.0]],   # ordine = sleeve computabili

  # opzionale: bottom-up
  "bottom_up": {
    "source": "CMA lug-2026: BlackRock, JPM, Amundi, Capital Group, Schwab",
    "currency": "USD", "horizon": "10y", "basis": "n/d (verificare)",
    "map": {                       # nome sleeve -> lista di stime per casa
      "USA":  [0.085, 0.067, 0.065, 0.061, 0.061],
      "BTP":  [0.044, 0.047, 0.035, 0.043, 0.040]
    }
  },

  # opzionale: sensitivity automatica
  "sensitivity": {"growth_delta": 0.01, "inflation_delta": 0.005}
}
--------------------------------------------------------------------------------
"""

import json
import sys
from typing import Any, Dict, List, Optional

EPS = 1e-12


# ------------------------------------------------------------------ utilities

def _compound(nominal_real: float, inflation: float) -> float:
    """reale -> nominale, forma moltiplicativa (non additiva)."""
    return (1.0 + nominal_real) * (1.0 + inflation) - 1.0


def _deflate(nominal: float, inflation: float) -> float:
    """nominale -> reale, forma moltiplicativa."""
    return (1.0 + nominal) / (1.0 + inflation) - 1.0


def _terminal_net_of_tax(rate: float, years: float, tax: float) -> float:
    """
    Tassazione alla REALIZZAZIONE, non come drag annuo.
    Restituisce il rendimento annuo equivalente netto d'imposta.
    """
    gross_mult = (1.0 + rate) ** years
    net_mult = 1.0 + (gross_mult - 1.0) * (1.0 - tax)
    if net_mult <= 0:
        return -1.0
    return net_mult ** (1.0 / years) - 1.0


def _mean(xs: List[float]) -> Optional[float]:
    return sum(xs) / len(xs) if xs else None


# ------------------------------------------------------------ sleeve pricing

def price_sleeve(s: Dict[str, Any], inflation: float) -> Dict[str, Any]:
    """Calcola gli strati LORDI (reale e nominale) di una singola gamba."""
    kind = s.get("kind")
    out: Dict[str, Any] = {
        "name": s.get("name"),
        "kind": kind,
        "weight": s.get("weight", 0.0),
        "isin": s.get("isin"),
        "ter": s.get("ter", 0.0),
        "volatility": s.get("volatility"),
        "source": s.get("source"),
        "components": {},
    }

    if kind == "equity":
        dy = s["dividend_yield"]
        g = s["real_growth"]
        dv = s.get("valuation_change", 0.0)
        real_gross = dy + g + dv
        out["components"] = {"dividend_yield": dy, "real_growth": g,
                             "valuation_change": dv}
        out["real_gross"] = real_gross
        out["nominal_gross"] = _compound(real_gross, inflation)

    elif kind == "bond":
        ytw = s["ytw"]
        roll = s.get("roll_down", 0.0)
        credit = s.get("credit_loss", 0.0)
        hedge = s.get("hedging_carry", 0.0)
        nominal_gross = ytw + roll - credit + hedge
        out["components"] = {"ytw": ytw, "roll_down": roll,
                             "credit_loss": credit, "hedging_carry": hedge,
                             "duration": s.get("duration")}
        out["nominal_gross"] = nominal_gross
        out["real_gross"] = _deflate(nominal_gross, inflation)

    elif kind == "non_computable":
        out["real_gross"] = None
        out["nominal_gross"] = None
        out["note"] = ("Nessun flusso di cassa da scontare: rendimento atteso "
                       "non stimabile con metodo top-down (canone, principio 12).")
        return out

    else:
        raise ValueError(f"kind sconosciuto per la gamba '{s.get('name')}': {kind}")

    return out


# --------------------------------------------------------- portfolio pricing

def price_portfolio(port: Dict[str, Any], cfg: Dict[str, Any]) -> Dict[str, Any]:
    inflation = cfg["inflation"]["value"]
    bollo = cfg.get("costs", {}).get("bollo", 0.0)
    tax_cfg = cfg.get("tax", {}) or {}
    apply_tax = bool(tax_cfg.get("apply", False))
    years = float(cfg["meta"]["horizon_years"])

    sleeves_in = port["sleeves"]
    total_weight = sum(s.get("weight", 0.0) for s in sleeves_in)
    if abs(total_weight - 1.0) > 1e-6:
        raise ValueError(
            f"[{port.get('name')}] i pesi sommano a {total_weight:.6f}, non a 1.0"
        )

    priced = [price_sleeve(s, inflation) for s in sleeves_in]
    computable = [p for p in priced if p["kind"] in ("equity", "bond")]
    coverage = sum(p["weight"] for p in computable)

    if coverage <= EPS:
        raise ValueError(f"[{port.get('name')}] nessuna gamba computabile.")

    # pesi rinormalizzati sulla quota coperta
    for p in computable:
        p["weight_renorm"] = p["weight"] / coverage

    # --- strati aggregati -----------------------------------------------
    real_gross = sum(p["weight_renorm"] * p["real_gross"] for p in computable)
    nominal_gross = sum(p["weight_renorm"] * p["nominal_gross"] for p in computable)

    ter_w = sum(p["weight_renorm"] * p["ter"] for p in computable)
    nominal_net_costs = nominal_gross - ter_w - bollo
    real_net_costs = _deflate(nominal_net_costs, inflation)

    # --- fisco: aliquota effettiva ponderata, applicata al termine -------
    if apply_tax:
        eq_rate = tax_cfg.get("equity_rate", 0.26)
        bd_rate = tax_cfg.get("bond_rate", 0.125)
        tax_w = 0.0
        for p, s in zip(priced, sleeves_in):
            if p["kind"] not in ("equity", "bond"):
                continue
            override = s.get("tax_rate")
            rate = override if override is not None else (
                eq_rate if p["kind"] == "equity" else bd_rate)
            p["tax_rate"] = rate
            tax_w += p["weight_renorm"] * rate
        nominal_net_tax = _terminal_net_of_tax(nominal_net_costs, years, tax_w)
        real_net_tax = _deflate(nominal_net_tax, inflation)
    else:
        tax_w = None
        nominal_net_tax = None
        real_net_tax = None

    # --- correzione geometrica (opzionale) -------------------------------
    geo = None
    corr = cfg.get("correlation")
    vols = [p.get("volatility") for p in computable]
    if corr and all(v is not None for v in vols) and len(corr) == len(computable):
        w = [p["weight_renorm"] for p in computable]
        # geometrico -> aritmetico
        arith = [p["nominal_gross"] + (v ** 2) / 2.0 for p, v in zip(computable, vols)]
        mu_p_arith = sum(wi * ai for wi, ai in zip(w, arith))
        var_p = 0.0
        for i in range(len(w)):
            for j in range(len(w)):
                var_p += w[i] * w[j] * vols[i] * vols[j] * corr[i][j]
        g_p = mu_p_arith - var_p / 2.0
        geo = {
            "portfolio_volatility": var_p ** 0.5,
            "nominal_gross_geometric": g_p,
            "rebalancing_bonus": g_p - nominal_gross,
            "note": ("Correzione di second'ordine. L'headline resta la media "
                     "pesata semplice; per la distribuzione completa usare "
                     "la skill simulazione-montecarlo."),
        }

    # --- montanti ---------------------------------------------------------
    headline = nominal_net_tax if nominal_net_tax is not None else nominal_net_costs
    multiples = {
        "years": years,
        "gross_nominal": (1.0 + nominal_gross) ** years,
        "net_costs_nominal": (1.0 + nominal_net_costs) ** years,
        "net_all_nominal": (1.0 + headline) ** years,
        "net_all_real": (1.0 + _deflate(headline, inflation)) ** years,
    }

    return {
        "name": port.get("name"),
        "coverage": coverage,
        "weighted_ter": ter_w,
        "weighted_tax_rate": tax_w,
        "layers": {
            "real_gross": real_gross,
            "nominal_gross": nominal_gross,
            "nominal_net_costs": nominal_net_costs,
            "real_net_costs": real_net_costs,
            "nominal_net_tax": nominal_net_tax,
            "real_net_tax": real_net_tax,
        },
        "headline_nominal": headline,
        "geometric_refinement": geo,
        "multiples": multiples,
        "sleeves": priced,
    }


# ---------------------------------------------------------------- bottom-up

def price_bottom_up(port_res: Dict[str, Any], cfg: Dict[str, Any]) -> Optional[Dict]:
    bu = cfg.get("bottom_up")
    if not bu or not bu.get("map"):
        return None
    mapping = bu["map"]
    rows, w_used = [], 0.0
    acc_mean = acc_min = acc_max = 0.0
    for p in port_res["sleeves"]:
        if p["kind"] not in ("equity", "bond"):
            continue
        est = mapping.get(p["name"])
        if not est:
            continue
        w = p["weight_renorm"]
        w_used += w
        acc_mean += w * _mean(est)
        acc_min += w * min(est)
        acc_max += w * max(est)
        rows.append({"sleeve": p["name"], "weight_renorm": w, "estimates": est,
                     "mean": _mean(est), "min": min(est), "max": max(est),
                     "dispersion": max(est) - min(est)})
    if w_used <= EPS:
        return None
    scale = 1.0 / w_used  # rinormalizza sulle gambe effettivamente mappate
    return {
        "source": bu.get("source"), "currency": bu.get("currency"),
        "horizon": bu.get("horizon"), "basis": bu.get("basis"),
        "weight_mapped": w_used,
        "mean": acc_mean * scale, "min": acc_min * scale, "max": acc_max * scale,
        "rows": rows,
        "caveat": ("Verificare valuta, orizzonte e convenzione geometrica/"
                   "aritmetica prima di confrontare col top-down "
                   "(metodologia-bottom-up.md §3)."),
    }


# -------------------------------------------------------------- sensitivity

def sensitivity(cfg: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    sens = cfg.get("sensitivity")
    if not sens:
        return None
    out = {}
    for label, key, delta in (
        ("growth", "growth_delta", sens.get("growth_delta")),
        ("inflation", "inflation_delta", sens.get("inflation_delta")),
    ):
        if delta is None:
            continue
        scen = {}
        for sign, tag in ((+1, "up"), (-1, "down")):
            c = json.loads(json.dumps(cfg))  # deep copy
            if label == "growth":
                for s in c["portfolio"]["sleeves"]:
                    if s.get("kind") == "equity":
                        s["real_growth"] += sign * delta
                for b in c.get("benchmarks", []):
                    for s in b["sleeves"]:
                        if s.get("kind") == "equity":
                            s["real_growth"] += sign * delta
            else:
                c["inflation"]["value"] += sign * delta
            c["sensitivity"] = None
            scen[tag] = price_portfolio(c["portfolio"], c)["headline_nominal"]
        out[label] = {"delta": delta, **scen}
    return out


# --------------------------------------------------------------------- main

def run(cfg: Dict[str, Any]) -> Dict[str, Any]:
    port = price_portfolio(cfg["portfolio"], cfg)
    benchmarks = [price_portfolio(b, cfg) for b in cfg.get("benchmarks", [])]

    comparisons = []
    for b in benchmarks:
        d_annual = port["headline_nominal"] - b["headline_nominal"]
        d_mult = (port["multiples"]["net_all_nominal"]
                  / b["multiples"]["net_all_nominal"] - 1.0)
        comparisons.append({
            "benchmark": b["name"],
            "delta_annual": d_annual,
            "delta_terminal_wealth": d_mult,
            "note": ("Il delta annuo va sempre letto insieme al delta di "
                     "montante e al delta di rischio/concentrazione "
                     "(benchmark-e-confronto.md §3)."),
        })

    bu = price_bottom_up(port, cfg)
    divergence = None
    if bu:
        gap = port["layers"]["nominal_gross"] - bu["mean"]
        divergence = {
            "gap": gap,
            "classification": ("convergenza" if abs(gap) < 0.005
                               else "fisiologica" if abs(gap) <= 0.015
                               else "ANOMALIA — nominare e spiegare, non mediare"),
        }

    return {
        "meta": cfg["meta"],
        "assumptions": {
            "inflation": cfg["inflation"],
            "costs": cfg.get("costs", {}),
            "tax": cfg.get("tax", {}),
        },
        "portfolio": port,
        "benchmarks": benchmarks,
        "comparisons": comparisons,
        "bottom_up": bu,
        "divergence_top_vs_bottom": divergence,
        "sensitivity": sensitivity(cfg),
        "disclaimer": ("Stima dell'ordine di grandezza implicito nei prezzi "
                       "correnti, con variazione delle valutazioni posta a zero "
                       "per convenzione. NON è una previsione e non giustifica "
                       "market timing. Il capitale può ridursi."),
    }


# ------------------------------------------------------------------ selftest

def _selftest() -> int:
    """Riproduce l'esempio canonico di TB-339 e i controlli di coerenza."""
    ok = True

    def check(label, got, exp, tol=5e-4):
        nonlocal ok
        good = abs(got - exp) <= tol
        ok = ok and good
        print(f"  [{'OK ' if good else 'FAIL'}] {label}: {got:.6f} (atteso {exp:.6f})")

    # --- 1. esempio canonico 70% ACWI + 30% Euro Agg Treasury -------------
    cfg = {
        "meta": {"label": "TB-339 canonico", "as_of": "2026-06-30",
                 "base_currency": "EUR", "horizon_years": 10,
                 "convention": "per-share"},
        "inflation": {"value": 0.025, "source": "TB-339 (2,5%)"},
        "costs": {"bollo": 0.0},
        "tax": {"apply": False},
        "portfolio": {"name": "70/30", "sleeves": [
            {"name": "ACWI", "kind": "equity", "weight": 0.70, "ter": 0.0,
             "dividend_yield": 0.0157, "real_growth": 0.026},
            {"name": "EuroAggTreasury", "kind": "bond", "weight": 0.30, "ter": 0.0,
             "ytw": 0.030},
        ]},
    }
    r = run(cfg)
    print("1) Esempio canonico TB-339")
    check("ACWI reale lordo", r["portfolio"]["sleeves"][0]["real_gross"], 0.0417)
    check("ACWI nominale lordo", r["portfolio"]["sleeves"][0]["nominal_gross"],
          (1.0417 * 1.025) - 1)
    check("portafoglio nominale lordo", r["portfolio"]["layers"]["nominal_gross"],
          0.70 * ((1.0417 * 1.025) - 1) + 0.30 * 0.030)
    check("copertura", r["portfolio"]["coverage"], 1.0)

    # con l'approssimazione additiva dell'episodio (6,67% e 3,0%) -> 5,6%
    approx = 0.70 * 0.0667 + 0.30 * 0.030
    print(f"  [i  ] versione additiva dell'episodio: {approx:.4f} (atteso ~0.0560)")

    # --- 2. copertura < 100% e rinormalizzazione --------------------------
    cfg2 = json.loads(json.dumps(cfg))
    cfg2["portfolio"]["sleeves"] = [
        {"name": "ACWI", "kind": "equity", "weight": 0.63, "ter": 0.0,
         "dividend_yield": 0.0157, "real_growth": 0.026},
        {"name": "Bond", "kind": "bond", "weight": 0.27, "ter": 0.0, "ytw": 0.030},
        {"name": "Oro", "kind": "non_computable", "weight": 0.10},
    ]
    r2 = run(cfg2)
    print("2) Copertura parziale (10% oro)")
    check("copertura", r2["portfolio"]["coverage"], 0.90)
    check("stima invariata dopo rinormalizzazione",
          r2["portfolio"]["layers"]["nominal_gross"],
          r["portfolio"]["layers"]["nominal_gross"])

    # --- 3. fisco al termine batte il drag annuo --------------------------
    cfg3 = json.loads(json.dumps(cfg))
    cfg3["meta"]["horizon_years"] = 25
    cfg3["tax"] = {"equity_rate": 0.26, "bond_rate": 0.125, "apply": True}
    r3 = run(cfg3)
    lay = r3["portfolio"]["layers"]
    naive = lay["nominal_net_costs"] * (1 - r3["portfolio"]["weighted_tax_rate"])
    print("3) Fiscalità differita (25 anni)")
    print(f"  [i  ] netto costi {lay['nominal_net_costs']:.4f} -> "
          f"netto fisco al termine {lay['nominal_net_tax']:.4f} "
          f"(drag annuo ingenuo: {naive:.4f})")
    if lay["nominal_net_tax"] > naive:
        print("  [OK ] il differimento vale: netto-al-termine > drag annuo")
    else:
        ok = False
        print("  [FAIL] atteso netto-al-termine > drag annuo")

    # --- 4. benchmark, delta e montante -----------------------------------
    cfg4 = json.loads(json.dumps(cfg))
    cfg4["meta"]["horizon_years"] = 25
    cfg4["benchmarks"] = [{"name": "ACWI+Bond", "sleeves": [
        {"name": "ACWI", "kind": "equity", "weight": 0.70, "ter": 0.0020,
         "dividend_yield": 0.0157, "real_growth": 0.026},
        {"name": "EuroAggTreasury", "kind": "bond", "weight": 0.30, "ter": 0.0007,
         "ytw": 0.0311},
    ]}]
    r4 = run(cfg4)
    cmp0 = r4["comparisons"][0]
    print("4) Confronto benchmark")
    print(f"  [i  ] delta annuo {cmp0['delta_annual']*100:+.3f} pt · "
          f"delta montante {cmp0['delta_terminal_wealth']*100:+.2f}%")
    if (cmp0["delta_annual"] > 0) == (cmp0["delta_terminal_wealth"] > 0):
        print("  [OK ] segno del delta annuo e del delta montante coerenti")
    else:
        ok = False
        print("  [FAIL] segni incoerenti")

    # --- 5. il costo composto di 2 punti ----------------------------------
    print("5) Riferimento: 5% vs 3%")
    for T, exp in ((10, -0.1751), (25, -0.3817)):
        got = (1.03 ** T) / (1.05 ** T) - 1
        check(f"differenza di montante a {T} anni", got, exp, tol=2e-3)

    # --- 6. guardia sui pesi ----------------------------------------------
    cfg6 = json.loads(json.dumps(cfg))
    cfg6["portfolio"]["sleeves"][0]["weight"] = 0.60
    try:
        run(cfg6)
        ok = False
        print("6) [FAIL] pesi non a 1.0 non hanno sollevato eccezione")
    except ValueError:
        print("6) [OK ] pesi non a 1.0 correttamente rifiutati")

    print("\n=== SELFTEST:", "PASSATO" if ok else "FALLITO", "===")
    return 0 if ok else 1


def main(argv: List[str]) -> int:
    if len(argv) == 2 and argv[1] == "--selftest":
        return _selftest()
    if len(argv) != 3:
        print(__doc__)
        return 2
    with open(argv[1], "r", encoding="utf-8") as f:
        cfg = json.load(f)
    res = run(cfg)
    with open(argv[2], "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    p = res["portfolio"]
    print(f"OK — {p['name']}: nominale lordo {p['layers']['nominal_gross']*100:.2f}% · "
          f"headline netto {p['headline_nominal']*100:.2f}% · "
          f"copertura {p['coverage']*100:.0f}% → {argv[2]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
