"""Deterministic synthetic accounts for evals and demos. Everything here is invented (SAMPLE)."""
import csv, pathlib, random
random.seed(7)
ROOT = pathlib.Path(__file__).resolve().parents[1]
inds = ["saas", "logistics", "healthcare", "legal", "fintech", "support-outsourcing"]
rows = []
for i in range(20):
    emp = random.choice([200, 450, 900, 1800, 3200, 5000])
    users = random.choice([0, 12, 35, 60, 142, 310])
    rows.append({"account_id": f"sample-{i+1:02d}", "domain": f"sample{i+1:02d}.example",
                 "flow_users": users or "",
                 "users_by_team": f"Sales:{users//2};Support:{users//3}" if users else "",
                 "has_team_plan": random.choice(["true", "false"]), "sso_enabled": random.choice(["true", "false"]),
                 "employees": emp, "industry": random.choice(inds), "it_contact": "[find IT lead]",
                 "champion": "[unknown]",
                 "signals": random.choice(["", "hiring security lead", "employee posted about Flow"])})
out = ROOT / "inputs/accounts/SAMPLE_accounts.csv"
with out.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print("wrote", out)
