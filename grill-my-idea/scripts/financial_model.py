#!/usr/bin/env python3
"""
financial_model.py — deterministic calculator for grill-my-idea.

Reads a model.json (see references/financial-model.md for how to fill it),
simulates pessimistic / realistic / optimistic scenarios month by month and
prints markdown tables you can paste into the dossier, plus a JSON with every
number (month-by-month series included).

Usage:
    python3 financial_model.py model.json
    python3 financial_model.py model.json --md 05-financial-model-tables.md --out model_output.json
    python3 financial_model.py model.json --lang pt      # pt-BR labels
    python3 financial_model.py --example > model.json    # starter file

Only the standard library is used on purpose: the script must run anywhere.

Model semantics (kept deliberately simple so every number is explainable):
    revenue_m            = active_users_m × arpu_monthly
    contribution / user  = arpu × (1 − tax_rate_on_revenue) − cogs_per_user_monthly
    new_users_m          = organic_new_users_monthly + marketing_budget_m / cac   (from launch_month on)
    churned_m            = active_users_(m−1) × monthly_churn
    costs_m              = fixed_costs_monthly + cogs × users + marketing_m + taxes_m
    cash                 = −one_time_costs + Σ (revenue − costs)
    break-even (simple)  = fixed / contribution
    break-even (sustain) = fixed / (contribution − cac × churn)   # also pays to replace churned users
"""

from __future__ import annotations

import argparse
import copy
import json
import math
import sys
from typing import Any

REQUIRED_BASE = [
    "arpu_monthly",
    "cogs_per_user_monthly",
    "fixed_costs_monthly",
    "cac",
    "marketing_budget_monthly",
    "organic_new_users_monthly",
    "monthly_churn",
]

# Default scenario overrides, used only when model.json does not define them.
# They are multipliers/offsets on the realistic case — documented in
# references/financial-model.md. Prefer explicit, justified overrides.
DEFAULT_PESSIMISTIC = {
    "monthly_churn": ("mul", 1.5),
    "cac": ("mul", 1.75),
    "arpu_monthly": ("mul", 0.8),
    "organic_new_users_monthly": ("mul", 0.5),
    "launch_month": ("add", 3),
    "fixed_costs_monthly": ("mul", 1.2),
}
DEFAULT_OPTIMISTIC = {
    "monthly_churn": ("mul", 0.7),
    "cac": ("mul", 0.7),
    "arpu_monthly": ("mul", 1.15),
    "organic_new_users_monthly": ("mul", 2.0),
}

LTV_LIFETIME_CAP_MONTHS = 60  # nobody should bank on a customer living > 5 years

LABELS = {
    "en": {
        "title": "Financial model",
        "scenario": "Scenario",
        "pessimistic": "Pessimistic",
        "realistic": "Realistic",
        "optimistic": "Optimistic",
        "summary": "Scenario summary",
        "unit": "Unit economics",
        "breakeven": "Break-even",
        "projection": "Projection",
        "sensitivity": "Sensitivity (realistic scenario, ±20% on each lever)",
        "assumptions": "Assumptions",
        "warnings": "Warnings",
        "market": "Market sizing (from inputs)",
        "users_m12": "Users @ m12",
        "users_m24": "Users @ m24",
        "users_m36": "Users @ m36",
        "mrr_m12": "MRR @ m12",
        "mrr_m36": "MRR @ m36",
        "arr_end": "ARR @ end",
        "be_month": "First profitable month",
        "cash_be_month": "Cash-positive month",
        "peak_cash": "Peak cash need",
        "cum_cash_end": "Cumulative cash @ end",
        "contribution": "Contribution / user / month",
        "gross_margin": "Gross margin",
        "ltv": "LTV (contribution)",
        "ltv_cac": "LTV / CAC",
        "payback": "CAC payback (months)",
        "lifetime": "Avg. lifetime (months)",
        "be_simple": "Break-even users (simple: fixed costs only)",
        "be_planned": "Break-even users (at planned marketing spend)",
        "be_sustain": "Break-even users (sustainable: incl. churn replacement)",
        "n_max": "Steady-state user ceiling with this budget",
        "be_pct_sam": "Sustainable break-even as % of SAM",
        "be_pct_som": "Sustainable break-even as % of SOM (yr 3)",
        "never": "never",
        "month": "Month",
        "users": "Users",
        "new": "New",
        "churned": "Churned",
        "revenue": "Revenue",
        "costs": "Costs",
        "profit": "Profit",
        "cash": "Cum. cash",
        "lever": "Lever",
        "value": "Value",
        "note": "Justification",
        "base_value": "Realistic",
        "tam": "TAM",
        "sam": "SAM",
        "som": "SOM (year 3)",
        "customers": "customers",
        "annual_revenue": "annual revenue",
        "be_users_sustain": "Sust. break-even users",
        "no_warnings": "No warnings — but re-read the assumptions; a clean model is usually an optimistic one.",
        "defaults_used": "Scenario '{name}' was not defined in model.json; default multipliers were applied. Define it explicitly with justified numbers.",
    },
    "pt": {
        "title": "Modelo financeiro",
        "scenario": "Cenário",
        "pessimistic": "Pessimista",
        "realistic": "Realista",
        "optimistic": "Otimista",
        "summary": "Resumo dos cenários",
        "unit": "Unit economics",
        "breakeven": "Ponto de equilíbrio (break-even)",
        "projection": "Projeção",
        "sensitivity": "Sensibilidade (cenário realista, ±20% em cada alavanca)",
        "assumptions": "Premissas",
        "warnings": "Alertas",
        "market": "Tamanho de mercado (a partir dos inputs)",
        "users_m12": "Usuários no mês 12",
        "users_m24": "Usuários no mês 24",
        "users_m36": "Usuários no mês 36",
        "mrr_m12": "MRR no mês 12",
        "mrr_m36": "MRR no mês 36",
        "arr_end": "ARR no fim",
        "be_month": "Primeiro mês com lucro",
        "cash_be_month": "Mês em que o caixa acumulado fica positivo",
        "peak_cash": "Necessidade máxima de caixa",
        "cum_cash_end": "Caixa acumulado no fim",
        "contribution": "Contribuição / usuário / mês",
        "gross_margin": "Margem bruta",
        "ltv": "LTV (contribuição)",
        "ltv_cac": "LTV / CAC",
        "payback": "Payback do CAC (meses)",
        "lifetime": "Vida média do cliente (meses)",
        "be_simple": "Usuários para empatar (simples: só custos fixos)",
        "be_planned": "Usuários para empatar (com o marketing planejado)",
        "be_sustain": "Usuários para empatar (sustentável: inclui reposição do churn)",
        "n_max": "Teto de usuários com esse orçamento (estado estacionário)",
        "be_pct_sam": "Break-even sustentável como % do SAM",
        "be_pct_som": "Break-even sustentável como % do SOM (ano 3)",
        "never": "nunca",
        "month": "Mês",
        "users": "Usuários",
        "new": "Novos",
        "churned": "Perdidos",
        "revenue": "Receita",
        "costs": "Custos",
        "profit": "Resultado",
        "cash": "Caixa acum.",
        "lever": "Alavanca",
        "value": "Valor",
        "note": "Justificativa",
        "base_value": "Realista",
        "tam": "TAM",
        "sam": "SAM",
        "som": "SOM (ano 3)",
        "customers": "clientes",
        "annual_revenue": "receita anual",
        "be_users_sustain": "Usuários p/ empatar (sust.)",
        "no_warnings": "Sem alertas — mas releia as premissas; um modelo limpo costuma ser um modelo otimista.",
        "defaults_used": "O cenário '{name}' não foi definido no model.json; multiplicadores padrão foram aplicados. Defina-o explicitamente com números justificados.",
    },
}


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def fail(msg: str) -> None:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(2)


def fmt_money(x: float, currency: str, lang: str) -> str:
    if x is None or (isinstance(x, float) and (math.isnan(x) or math.isinf(x))):
        return "—"
    s = f"{abs(x):,.0f}"
    if lang == "pt":
        s = s.replace(",", ".")
    sign = "-" if x < 0 else ""
    sym = {"BRL": "R$", "USD": "US$", "EUR": "€", "GBP": "£"}.get(currency, currency + " ")
    return f"{sign}{sym} {s}"


def fmt_num(x: float, lang: str, digits: int = 0) -> str:
    if x is None or (isinstance(x, float) and (math.isnan(x) or math.isinf(x))):
        return "—"
    s = f"{x:,.{digits}f}"
    if lang == "pt":
        s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return s


def fmt_pct(x: float, lang: str, digits: int = 1) -> str:
    if x is None or (isinstance(x, float) and (math.isnan(x) or math.isinf(x))):
        return "—"
    s = f"{x * 100:.{digits}f}%"
    return s.replace(".", ",") if lang == "pt" else s


def budget_series(value: Any, horizon: int) -> list[float]:
    if isinstance(value, (int, float)):
        return [float(value)] * horizon
    if isinstance(value, list) and value:
        series = [float(v) for v in value]
        if len(series) < horizon:
            series += [series[-1]] * (horizon - len(series))
        return series[:horizon]
    fail("marketing_budget_monthly must be a number or a non-empty list")
    return []


def apply_overrides(base: dict, overrides: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in overrides.items():
        if isinstance(v, (list, tuple)) and len(v) == 2 and v[0] in ("mul", "add"):
            op, amount = v
            if k not in out:
                continue
            cur = out[k]
            if isinstance(cur, list):
                out[k] = [c * amount if op == "mul" else c + amount for c in cur]
            else:
                out[k] = cur * amount if op == "mul" else cur + amount
        else:
            out[k] = v
    return out


# --------------------------------------------------------------------------- #
# core math
# --------------------------------------------------------------------------- #
def unit_economics(p: dict, horizon: int = 36) -> dict:
    arpu = float(p["arpu_monthly"])
    cogs = float(p["cogs_per_user_monthly"])
    tax = float(p.get("tax_rate_on_revenue", 0.0))
    churn = float(p["monthly_churn"])
    cac = float(p["cac"])
    fixed = float(p["fixed_costs_monthly"])
    organic = float(p["organic_new_users_monthly"])
    launch = max(1, int(p.get("launch_month", 1)))
    cap = float(p.get("ltv_cap_months", LTV_LIFETIME_CAP_MONTHS))
    budget = budget_series(p["marketing_budget_monthly"], horizon)
    live_budget = budget[launch - 1:] or [0.0]
    avg_marketing = sum(live_budget) / len(live_budget)

    contribution = arpu * (1 - tax) - cogs
    gross_margin = contribution / arpu if arpu > 0 else float("nan")
    lifetime = min(1 / churn, cap) if churn > 0 else cap
    ltv = contribution * lifetime
    ltv_cac = ltv / cac if cac > 0 else float("inf")
    payback = cac / contribution if contribution > 0 else float("inf")

    be_simple = fixed / contribution if contribution > 0 else float("inf")          # N_static
    be_planned = (fixed + avg_marketing) / contribution if contribution > 0 else float("inf")  # N_plan
    replace_cost = cac * churn
    sustain_margin = contribution - replace_cost
    be_sustain = fixed / sustain_margin if sustain_margin > 0 else float("inf")      # N_sust
    new_per_month = organic + (avg_marketing / cac if cac > 0 else 0.0)
    n_max = new_per_month / churn if churn > 0 else float("inf")                     # N_max

    return {
        "contribution_per_user": contribution,
        "gross_margin": gross_margin,
        "avg_lifetime_months": lifetime,
        "ltv": ltv,
        "ltv_cac": ltv_cac,
        "cac_payback_months": payback,
        "breakeven_users_simple": be_simple,
        "breakeven_users_planned": be_planned,
        "breakeven_users_sustainable": be_sustain,
        "steady_state_ceiling": n_max,
        "new_users_per_month": new_per_month,
        "avg_marketing_budget": avg_marketing,
        "replacement_cost_per_user_month": replace_cost,
    }


def simulate(p: dict, horizon: int, one_time: float) -> dict:
    arpu = float(p["arpu_monthly"])
    cogs = float(p["cogs_per_user_monthly"])
    tax = float(p.get("tax_rate_on_revenue", 0.0))
    churn = float(p["monthly_churn"])
    cac = float(p["cac"])
    fixed = float(p["fixed_costs_monthly"])
    organic = float(p["organic_new_users_monthly"])
    launch = int(p.get("launch_month", 1))
    budget = budget_series(p["marketing_budget_monthly"], horizon)

    users = 0.0
    cash = -float(one_time)
    rows = []
    first_profit_month = None
    cash_positive_month = None
    peak_need = cash
    for m in range(1, horizon + 1):
        live = m >= launch
        marketing = budget[m - 1] if live else 0.0
        paid_new = (marketing / cac) if (live and cac > 0) else 0.0
        new = (organic + paid_new) if live else 0.0
        churned = users * churn
        users = max(0.0, users + new - churned)
        revenue = users * arpu
        taxes = revenue * tax
        cost_cogs = users * cogs
        costs = fixed + cost_cogs + marketing + taxes
        profit = revenue - costs
        cash += profit
        peak_need = min(peak_need, cash)
        if first_profit_month is None and profit >= 0 and live:
            first_profit_month = m
        if cash_positive_month is None and cash >= 0 and m > 1:
            cash_positive_month = m
        rows.append(
            {
                "month": m,
                "users": users,
                "new_users": new,
                "churned": churned,
                "revenue": revenue,
                "marketing": marketing,
                "cogs": cost_cogs,
                "taxes": taxes,
                "fixed": fixed,
                "costs": costs,
                "profit": profit,
                "cumulative_cash": cash,
            }
        )

    def at(month: int, key: str) -> float:
        return rows[month - 1][key] if month <= horizon else float("nan")

    return {
        "rows": rows,
        "first_profitable_month": first_profit_month,
        "cash_positive_month": cash_positive_month,
        "peak_cash_need": -peak_need,
        "cumulative_cash_end": cash,
        "users_m12": at(12, "users"),
        "users_m24": at(24, "users"),
        "users_m36": at(36, "users"),
        "mrr_m12": at(12, "revenue"),
        "mrr_m36": at(36, "revenue"),
        "arr_end": rows[-1]["revenue"] * 12,
        "users_end": rows[-1]["users"],
    }


def market_block(p: dict) -> dict | None:
    if "sam_users" not in p and "tam_users" not in p:
        return None
    arpu = float(p["arpu_monthly"])
    tam = float(p.get("tam_users", 0) or 0)
    sam = float(p.get("sam_users", 0) or 0)
    share = float(p.get("som_share_year3", 0) or 0)
    som = sam * share
    return {
        "tam_users": tam,
        "sam_users": sam,
        "som_users_year3": som,
        "som_share_year3": share,
        "tam_annual_revenue": tam * arpu * 12,
        "sam_annual_revenue": sam * arpu * 12,
        "som_annual_revenue": som * arpu * 12,
    }


def sensitivity(base: dict, horizon: int, one_time: float) -> list[dict]:
    levers = [
        "arpu_monthly",
        "monthly_churn",
        "cac",
        "fixed_costs_monthly",
        "cogs_per_user_monthly",
        "organic_new_users_monthly",
    ]
    out = []
    ref_ue = unit_economics(base, horizon)
    ref_sim = simulate(base, horizon, one_time)
    for lever in levers:
        row = {"lever": lever}
        for label, mult in (("minus20", 0.8), ("plus20", 1.2)):
            p = copy.deepcopy(base)
            p[lever] = float(p[lever]) * mult
            ue = unit_economics(p, horizon)
            sim = simulate(p, horizon, one_time)
            row[label] = {
                "breakeven_users_sustainable": ue["breakeven_users_sustainable"],
                "cumulative_cash_end": sim["cumulative_cash_end"],
                "peak_cash_need": sim["peak_cash_need"],
            }
        row["reference"] = {
            "breakeven_users_sustainable": ref_ue["breakeven_users_sustainable"],
            "cumulative_cash_end": ref_sim["cumulative_cash_end"],
            "peak_cash_need": ref_sim["peak_cash_need"],
        }
        out.append(row)
    return out


WARN = {
    "en": {
        "contrib": "[{s}] contribution per user ≤ 0: every customer loses money before fixed costs.",
        "never_sustain": "[{s}] sustainable break-even is never reached: CAC × churn ({v}) ≥ contribution per user.",
        "engine": "[{s}] the acquisition engine as budgeted plateaus at ~{v} users, below the {n} needed to break even at planned spend: raise the budget, cut CAC or churn — and say which is believable.",
        "ltv_cac": "[{s}] LTV/CAC = {v} (< 3). Acquisition is too expensive or retention too weak.",
        "payback": "[{s}] CAC payback = {v} months (> 12). Growth will eat cash.",
        "margin": "[{s}] gross margin {v} (< 50%): looks like a services business, not software.",
        "churn": "[{s}] monthly churn {v} — at this level the whole base is replaced every ~{m} months.",
        "never_profit": "[{s}] never profitable within the {h}-month horizon.",
        "be_gt_som": "[{s}] sustainable break-even ({v}) exceeds SOM year 3 ({som}): the model does not close inside the obtainable market.",
        "users_gt_sam": "[{s}] projected users at the end ({v}) exceed SAM ({sam}): growth inputs are inconsistent with market inputs.",
    },
    "pt": {
        "contrib": "[{s}] contribuição por usuário ≤ 0: cada cliente dá prejuízo antes mesmo dos custos fixos.",
        "never_sustain": "[{s}] o break-even sustentável nunca é atingido: CAC × churn ({v}) ≥ contribuição por usuário.",
        "engine": "[{s}] o motor de aquisição orçado estaciona em ~{v} usuários, abaixo dos {n} necessários para empatar com o marketing planejado: aumente o orçamento, reduza CAC ou churn — e diga qual é crível.",
        "ltv_cac": "[{s}] LTV/CAC = {v} (< 3). Aquisição cara demais ou retenção fraca demais.",
        "payback": "[{s}] payback do CAC = {v} meses (> 12). Crescer vai consumir caixa.",
        "margin": "[{s}] margem bruta {v} (< 50%): parece negócio de serviços, não software.",
        "churn": "[{s}] churn mensal {v} — nesse nível a base inteira é trocada a cada ~{m} meses.",
        "never_profit": "[{s}] nunca dá lucro dentro do horizonte de {h} meses.",
        "be_gt_som": "[{s}] break-even sustentável ({v}) é maior que o SOM do ano 3 ({som}): o modelo não fecha dentro do mercado obtível.",
        "users_gt_sam": "[{s}] usuários projetados no fim ({v}) ultrapassam o SAM ({sam}): as premissas de crescimento contradizem as de mercado.",
    },
}


def warnings_for(name: str, p: dict, ue: dict, sim: dict, market: dict | None, lang: str) -> list[str]:
    L = LABELS[lang]
    W = WARN[lang]
    w = []
    s = L[name]
    if ue["contribution_per_user"] <= 0:
        w.append(W["contrib"].format(s=s))
    if math.isinf(ue["breakeven_users_sustainable"]):
        w.append(W["never_sustain"].format(s=s, v=fmt_num(ue["replacement_cost_per_user_month"], lang, 2)))
    if not math.isinf(ue["breakeven_users_planned"]) and ue["steady_state_ceiling"] < ue["breakeven_users_planned"]:
        w.append(W["engine"].format(s=s, v=fmt_num(ue["steady_state_ceiling"], lang), n=fmt_num(ue["breakeven_users_planned"], lang)))
    if ue["ltv_cac"] < 3:
        w.append(W["ltv_cac"].format(s=s, v=fmt_num(ue["ltv_cac"], lang, 1)))
    if ue["cac_payback_months"] > 12:
        w.append(W["payback"].format(s=s, v=fmt_num(ue["cac_payback_months"], lang, 1)))
    if 0 < ue["gross_margin"] < 0.5:
        w.append(W["margin"].format(s=s, v=fmt_pct(ue["gross_margin"], lang)))
    churn = float(p["monthly_churn"])
    if churn >= 0.10:
        w.append(W["churn"].format(s=s, v=fmt_pct(churn, lang), m=fmt_num(1 / churn, lang, 0)))
    if sim["first_profitable_month"] is None:
        w.append(W["never_profit"].format(s=s, h=len(sim["rows"])))
    if market and market["som_users_year3"] > 0 and not math.isinf(ue["breakeven_users_sustainable"]):
        if ue["breakeven_users_sustainable"] > market["som_users_year3"]:
            w.append(W["be_gt_som"].format(s=s, v=fmt_num(ue["breakeven_users_sustainable"], lang), som=fmt_num(market["som_users_year3"], lang)))
    if market and market["sam_users"] > 0 and sim["users_end"] > market["sam_users"]:
        w.append(W["users_gt_sam"].format(s=s, v=fmt_num(sim["users_end"], lang), sam=fmt_num(market["sam_users"], lang)))
    return w


# --------------------------------------------------------------------------- #
# rendering
# --------------------------------------------------------------------------- #
def render_md(result: dict, lang: str) -> str:
    L = LABELS[lang]
    cur = result["currency"]
    names = ["pessimistic", "realistic", "optimistic"]
    S = result["scenarios"]
    lines: list[str] = []
    lines.append(f"## {L['title']} — {result['idea']}")
    lines.append("")

    # market
    mk = result.get("market")
    if mk:
        lines.append(f"### {L['market']}")
        lines.append("")
        lines.append(f"| | {L['customers']} | {L['annual_revenue']} |")
        lines.append("|---|---:|---:|")
        lines.append(f"| {L['tam']} | {fmt_num(mk['tam_users'], lang)} | {fmt_money(mk['tam_annual_revenue'], cur, lang)} |")
        lines.append(f"| {L['sam']} | {fmt_num(mk['sam_users'], lang)} | {fmt_money(mk['sam_annual_revenue'], cur, lang)} |")
        lines.append(
            f"| {L['som']} ({fmt_pct(mk['som_share_year3'], lang)} SAM) | {fmt_num(mk['som_users_year3'], lang)} | {fmt_money(mk['som_annual_revenue'], cur, lang)} |"
        )
        lines.append("")

    # summary
    lines.append(f"### {L['summary']}")
    lines.append("")
    lines.append(f"| | {L['pessimistic']} | {L['realistic']} | {L['optimistic']} |")
    lines.append("|---|---:|---:|---:|")

    def row(label: str, fn) -> None:
        lines.append(f"| {label} | " + " | ".join(fn(S[n]) for n in names) + " |")

    row(L["users_m12"], lambda s: fmt_num(s["sim"]["users_m12"], lang))
    row(L["users_m24"], lambda s: fmt_num(s["sim"]["users_m24"], lang))
    row(L["users_m36"], lambda s: fmt_num(s["sim"]["users_m36"], lang))
    row(L["mrr_m12"], lambda s: fmt_money(s["sim"]["mrr_m12"], cur, lang))
    row(L["mrr_m36"], lambda s: fmt_money(s["sim"]["mrr_m36"], cur, lang))
    row(L["arr_end"], lambda s: fmt_money(s["sim"]["arr_end"], cur, lang))
    row(L["be_month"], lambda s: str(s["sim"]["first_profitable_month"] or L["never"]))
    row(L["cash_be_month"], lambda s: str(s["sim"]["cash_positive_month"] or L["never"]))
    row(L["peak_cash"], lambda s: fmt_money(s["sim"]["peak_cash_need"], cur, lang))
    row(L["cum_cash_end"], lambda s: fmt_money(s["sim"]["cumulative_cash_end"], cur, lang))
    lines.append("")

    # unit economics
    lines.append(f"### {L['unit']}")
    lines.append("")
    lines.append(f"| | {L['pessimistic']} | {L['realistic']} | {L['optimistic']} |")
    lines.append("|---|---:|---:|---:|")
    row(L["contribution"], lambda s: fmt_money(s["ue"]["contribution_per_user"], cur, lang))
    row(L["gross_margin"], lambda s: fmt_pct(s["ue"]["gross_margin"], lang))
    row(L["lifetime"], lambda s: fmt_num(s["ue"]["avg_lifetime_months"], lang, 1))
    row(L["ltv"], lambda s: fmt_money(s["ue"]["ltv"], cur, lang))
    row(L["ltv_cac"], lambda s: fmt_num(s["ue"]["ltv_cac"], lang, 1))
    row(L["payback"], lambda s: fmt_num(s["ue"]["cac_payback_months"], lang, 1))
    lines.append("")

    # break-even
    lines.append(f"### {L['breakeven']}")
    lines.append("")
    lines.append(f"| | {L['pessimistic']} | {L['realistic']} | {L['optimistic']} |")
    lines.append("|---|---:|---:|---:|")
    def n_or_never(v: float) -> str:
        return L["never"] if math.isinf(v) else fmt_num(v, lang)

    row(L["be_simple"], lambda s: n_or_never(s["ue"]["breakeven_users_simple"]))
    row(L["be_planned"], lambda s: n_or_never(s["ue"]["breakeven_users_planned"]))
    row(L["be_sustain"], lambda s: n_or_never(s["ue"]["breakeven_users_sustainable"]))
    row(L["n_max"], lambda s: "∞" if math.isinf(s["ue"]["steady_state_ceiling"]) else fmt_num(s["ue"]["steady_state_ceiling"], lang))
    if mk and mk["sam_users"] > 0:
        row(L["be_pct_sam"], lambda s: fmt_pct(s["ue"]["breakeven_users_sustainable"] / mk["sam_users"], lang, 2) if not math.isinf(s["ue"]["breakeven_users_sustainable"]) else "—")
    if mk and mk["som_users_year3"] > 0:
        row(L["be_pct_som"], lambda s: fmt_pct(s["ue"]["breakeven_users_sustainable"] / mk["som_users_year3"], lang, 0) if not math.isinf(s["ue"]["breakeven_users_sustainable"]) else "—")
    lines.append("")

    # projection per scenario (every 6 months)
    checkpoints = [m for m in (3, 6, 12, 18, 24, 30, 36, 48, 60) if m <= result["horizon_months"]]
    for n in names:
        s = S[n]
        lines.append(f"### {L['projection']} — {L[n]}")
        lines.append("")
        lines.append(f"| {L['month']} | {L['users']} | {L['new']} | {L['churned']} | {L['revenue']} | {L['costs']} | {L['profit']} | {L['cash']} |")
        lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|")
        for m in checkpoints:
            r = s["sim"]["rows"][m - 1]
            lines.append(
                f"| {m} | {fmt_num(r['users'], lang)} | {fmt_num(r['new_users'], lang)} | {fmt_num(r['churned'], lang)} | "
                f"{fmt_money(r['revenue'], cur, lang)} | {fmt_money(r['costs'], cur, lang)} | {fmt_money(r['profit'], cur, lang)} | {fmt_money(r['cumulative_cash'], cur, lang)} |"
            )
        lines.append("")

    # sensitivity
    lines.append(f"### {L['sensitivity']}")
    lines.append("")
    lines.append(f"| {L['lever']} | {L['be_users_sustain']} −20% | {L['be_users_sustain']} +20% | {L['cum_cash_end']} −20% | {L['cum_cash_end']} +20% |")
    lines.append("|---|---:|---:|---:|---:|")
    for r in result["sensitivity"]:
        def be(v: float) -> str:
            return L["never"] if math.isinf(v) else fmt_num(v, lang)
        lines.append(
            f"| {r['lever']} | {be(r['minus20']['breakeven_users_sustainable'])} | {be(r['plus20']['breakeven_users_sustainable'])} | "
            f"{fmt_money(r['minus20']['cumulative_cash_end'], cur, lang)} | {fmt_money(r['plus20']['cumulative_cash_end'], cur, lang)} |"
        )
    lines.append("")

    # assumptions
    lines.append(f"### {L['assumptions']}")
    lines.append("")
    lines.append(f"| {L['lever']} | {L['pessimistic']} | {L['realistic']} | {L['optimistic']} | {L['note']} |")
    lines.append("|---|---:|---:|---:|---|")
    keys = list(result["scenarios"]["realistic"]["params"].keys())
    notes = result.get("notes", {})
    for k in keys:
        vals = []
        for n in names:
            v = result["scenarios"][n]["params"].get(k)
            if isinstance(v, list):
                vals.append(f"[{fmt_num(v[0], lang)}…{fmt_num(v[-1], lang)}]")
            elif isinstance(v, float) and k in ("monthly_churn", "tax_rate_on_revenue", "som_share_year3"):
                vals.append(fmt_pct(v, lang))
            elif isinstance(v, (int, float)):
                vals.append(fmt_num(v, lang, 2 if abs(v) < 10 and v != int(v) else 0))
            else:
                vals.append(str(v))
        lines.append(f"| {k} | " + " | ".join(vals) + f" | {notes.get(k, '')} |")
    lines.append(f"| one_time_costs | | {fmt_money(result['one_time_costs'], cur, lang)} | | {notes.get('one_time_costs', '')} |")
    lines.append("")

    # warnings
    lines.append(f"### {L['warnings']}")
    lines.append("")
    if result["warnings"]:
        for w in result["warnings"]:
            lines.append(f"- {w}")
    else:
        lines.append(f"- {L['no_warnings']}")
    lines.append("")
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
EXAMPLE = {
    "idea": "exemplo-saas-para-dentistas",
    "currency": "BRL",
    "horizon_months": 36,
    "one_time_costs": 40000,
    "base": {
        "arpu_monthly": 99,
        "cogs_per_user_monthly": 8,
        "fixed_costs_monthly": 18000,
        "cac": 250,
        "marketing_budget_monthly": 6000,
        "organic_new_users_monthly": 15,
        "monthly_churn": 0.05,
        "launch_month": 3,
        "tax_rate_on_revenue": 0.06,
        "tam_users": 500000,
        "sam_users": 80000,
        "som_share_year3": 0.03,
    },
    "scenarios": {
        "pessimistic": {
            "monthly_churn": 0.08,
            "cac": 400,
            "arpu_monthly": 79,
            "organic_new_users_monthly": 5,
            "launch_month": 6,
            "fixed_costs_monthly": 22000,
        },
        "optimistic": {"monthly_churn": 0.035, "cac": 180, "arpu_monthly": 119, "organic_new_users_monthly": 40},
    },
    "notes": {
        "arpu_monthly": "anchored on competitor plans at R$ 89 and R$ 129",
        "monthly_churn": "SMB SaaS benchmark 3–7%/month",
        "cac": "Google Ads BR CPC R$ 3–6 × landing 3% × trial→paid 20%",
        "fixed_costs_monthly": "2 founders PJ R$ 7k each + tools/cloud R$ 2k + contador R$ 600 + misc",
    },
}


def build(model: dict, lang: str) -> dict:
    base = model.get("base")
    if not isinstance(base, dict):
        fail("model.json needs a 'base' object (the realistic scenario)")
    missing = [k for k in REQUIRED_BASE if k not in base]
    if missing:
        fail(f"base is missing required keys: {', '.join(missing)}")
    for k in ("monthly_churn", "tax_rate_on_revenue", "som_share_year3"):
        if k in base and not (0 <= float(base[k]) <= 1):
            fail(f"base.{k} must be a fraction between 0 and 1 (got {base[k]})")

    horizon = int(model.get("horizon_months", 36))
    one_time = float(model.get("one_time_costs", 0))
    currency = model.get("currency", "BRL")
    scen_in = model.get("scenarios", {}) or {}
    notes = model.get("notes", {}) or {}
    warnings: list[str] = []

    params = {"realistic": copy.deepcopy(base)}
    if isinstance(scen_in.get("pessimistic"), dict) and scen_in["pessimistic"]:
        params["pessimistic"] = apply_overrides(base, scen_in["pessimistic"])
    else:
        params["pessimistic"] = apply_overrides(base, DEFAULT_PESSIMISTIC)
        warnings.append(LABELS[lang]["defaults_used"].format(name="pessimistic"))
    if isinstance(scen_in.get("optimistic"), dict) and scen_in["optimistic"]:
        params["optimistic"] = apply_overrides(base, scen_in["optimistic"])
    else:
        params["optimistic"] = apply_overrides(base, DEFAULT_OPTIMISTIC)
        warnings.append(LABELS[lang]["defaults_used"].format(name="optimistic"))

    scenarios = {}
    for name, p in params.items():
        ue = unit_economics(p, horizon)
        sim = simulate(p, horizon, one_time)
        mk = market_block(p)
        scenarios[name] = {"params": p, "ue": ue, "sim": sim, "market": mk}
        warnings.extend(warnings_for(name, p, ue, sim, mk, lang))

    return {
        "idea": model.get("idea", "idea"),
        "currency": currency,
        "horizon_months": horizon,
        "one_time_costs": one_time,
        "market": scenarios["realistic"]["market"],
        "scenarios": scenarios,
        "sensitivity": sensitivity(base, horizon, one_time),
        "notes": notes,
        "warnings": warnings,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="grill-my-idea financial model")
    ap.add_argument("model", nargs="?", help="path to model.json")
    ap.add_argument("--out", help="write full JSON result here")
    ap.add_argument("--md", help="write markdown tables here (also printed to stdout)")
    ap.add_argument("--lang", choices=["en", "pt"], default="en", help="label language for the markdown")
    ap.add_argument("--example", action="store_true", help="print an example model.json and exit")
    args = ap.parse_args()

    if args.example:
        print(json.dumps(EXAMPLE, indent=2, ensure_ascii=False))
        return
    if not args.model:
        ap.error("model path required (or --example)")

    try:
        with open(args.model, encoding="utf-8") as f:
            model = json.load(f)
    except FileNotFoundError:
        fail(f"file not found: {args.model}")
    except json.JSONDecodeError as e:
        fail(f"invalid JSON in {args.model}: {e}")

    result = build(model, args.lang)
    md = render_md(result, args.lang)
    print(md)
    if args.md:
        with open(args.md, "w", encoding="utf-8") as f:
            f.write(md)
    if args.out:
        def clean(o: Any) -> Any:
            if isinstance(o, float):
                if math.isinf(o):
                    return None
                if math.isnan(o):
                    return None
                return round(o, 4)
            if isinstance(o, dict):
                return {k: clean(v) for k, v in o.items()}
            if isinstance(o, list):
                return [clean(v) for v in o]
            return o
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(clean(result), f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
