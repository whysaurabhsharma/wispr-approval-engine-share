"""Build claims/review/review.csv from all candidate files, for one human pass in Excel.
Columns you fill: keep (y/n) on every row; correct (y/n) on the 30 rows marked gold=yes.
Usage: python scripts/make_review_sheet.py"""
import csv, collections, pathlib, random, re, sys, yaml
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verify"))
from check_quotes import norm, snapshot_text
OUT = ROOT / "claims/review/review.csv"
if OUT.exists():
    sys.exit(f"{OUT} already exists. Rename or delete it first so your edits are never overwritten.")
rows = []
for f in sorted((ROOT / "claims/candidates").glob("*.yaml")):
    for r in yaml.safe_load(f.read_text(encoding="utf-8")) or []:
        rows.append(r)
counts = collections.Counter(r["id"] for r in rows)
gold = set() if (ROOT / "evals/claims/gold.yaml").exists() else {id(r) for r in random.Random(42).sample(rows, min(30, len(rows)))}  # gold is frozen once
def context(r, words=12):
    text, q = snapshot_text(r["source_id"]) or "", norm(str(r.get("source_quote") or ""))
    i = text.find(q) if q else -1
    if i < 0: return ""
    before = text[:i].split()[-words:]; after = text[i + len(q):].split()[:words]
    s = " ".join(before) + " [[" + q + "]] " + " ".join(after)
    return re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "[email]", s)  # keep the sheet commit-safe
OUT.parent.mkdir(parents=True, exist_ok=True)
cols = ["keep", "gold", "correct", "note", "id", "dup_id", "source_id", "topic", "status", "plan_scope", "claim", "source_quote", "context"]
with OUT.open("w", newline="", encoding="utf-8-sig") as fh:
    w = csv.DictWriter(fh, fieldnames=cols); w.writeheader()
    for r in rows:
        w.writerow({"keep": "", "gold": "yes" if id(r) in gold else "", "correct": "", "note": "",
                    "id": r["id"], "dup_id": "DUP" if counts[r["id"]] > 1 else "", "source_id": r["source_id"],
                    "topic": r["topic"], "status": r["status"], "plan_scope": ",".join(map(str, r.get("plan_scope") or [])),
                    "claim": r["claim"], "source_quote": r["source_quote"], "context": context(r)})
print(f"wrote {OUT}: {len(rows)} rows, {len(gold)} gold, {sum(1 for c in counts.values() if c > 1)} duplicate ids")
