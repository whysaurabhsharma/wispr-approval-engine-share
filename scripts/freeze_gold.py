"""Freeze the human-labelled gold rows from claims/review/review.csv into evals/claims/gold.yaml.
Usage: python scripts/freeze_gold.py"""
import csv, datetime, pathlib, yaml
ROOT = pathlib.Path(__file__).resolve().parents[1]
rows = [r for r in csv.DictReader(open(ROOT / "claims/review/review.csv", encoding="utf-8-sig")) if r["gold"] == "yes"]
missing = [r["id"] for r in rows if r["correct"] not in ("y", "n")]
if missing: raise SystemExit(f"label these first: {missing}")
out = {"frozen": datetime.date.today().isoformat(), "extractor": "claim-extractor (haiku), rules 1-6",
       "score": f"{sum(r['correct'] == 'y' for r in rows)}/{len(rows)}", "threshold": "28/30",
       "rows": [{k: r[k] for k in ("id", "source_id", "status", "plan_scope", "claim", "source_quote", "correct", "note")} for r in rows]}
path = ROOT / "evals/claims/gold.yaml"
path.write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
print("froze", len(rows), "rows, score", out["score"], "->", path)
