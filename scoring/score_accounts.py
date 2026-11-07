"""Rank accounts from a CSV. Every rank carries its top-3 reasons. Weights live in weights.yaml (PROVISIONAL, see docs/scoring.md).
Usage: python scoring/score_accounts.py <accounts.csv> [enrichment.csv]
enrichment.csv (optional) adds columns by account_id, e.g. industry, employees, it_contact."""
import csv, math, pathlib, sys, yaml
ROOT = pathlib.Path(__file__).resolve().parents[1]
W = yaml.safe_load((ROOT / "scoring/weights.yaml").read_text(encoding="utf-8"))
REG = {"healthcare", "legal", "fintech"}
def score(r):
    parts = {}
    users = float(r["flow_users"]) if r.get("flow_users") else 0.0
    emp = float(r["employees"]) if r.get("employees") else 0.0
    if users and emp: parts["penetration"] = W["penetration"] * min(users / emp, 0.5) * 2
    if users: parts["absolute_users"] = W["absolute_users"] * math.log10(users)
    if r.get("has_team_plan") == "false": parts["no_team_plan"] = W["no_team_plan"]
    if r.get("sso_enabled") == "false": parts["no_sso"] = W["no_sso"]
    if r.get("industry") in REG: parts["regulated_industry"] = W["regulated_industry"]
    if r.get("strength") in W.get("signal_strength", {}): parts[f"public_signal_{r['strength']}"] = W["signal_strength"][r["strength"]]
    elif r.get("signals"): parts["signal"] = W["signal"]
    reasons = sorted(parts, key=parts.get, reverse=True)[:3]
    return round(sum(parts.values()), 2), reasons
def read(p): return list(csv.DictReader(open(p, encoding="utf-8-sig")))
if __name__ == "__main__":
    src = pathlib.Path(sys.argv[1]); rows = read(src)
    if len(sys.argv) > 2:
        extra = {e["account_id"]: e for e in read(sys.argv[2])}
        for r in rows: r.update({k: v for k, v in extra.get(r["account_id"], {}).items() if v != "" and k != "account_id"})
    for r in rows:
        s, why = score(r); r["score"], r["reasons"] = s, ";".join(why) or "no scoring inputs"
    rows.sort(key=lambda r: -r["score"])
    n = len(rows)
    for i, r in enumerate(rows): r["tier"] = "A" if i < n * 0.3 else "B" if i < n * 0.6 else "C"
    out = src.with_name(src.stem + "_ranked.csv")
    cols = list(dict.fromkeys(k for r in rows for k in r))
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
    print("wrote", out); [print(f"  {r['tier']} {r['score']:>5} {r['account_id']} {r.get('company', r.get('domain', ''))}: {r['reasons']}") for r in rows]
