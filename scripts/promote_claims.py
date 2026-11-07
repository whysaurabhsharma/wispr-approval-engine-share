"""Promote reviewed candidates into claims/library.yaml (the CONTROLLED library).
Takes keep=y rows from claims/review/review.csv, copies each row's content from its candidate file,
links CONFLICT groups (status -> conflicting), normalises plan names, re-runs the quote check, then writes.
Usage: python scripts/promote_claims.py"""
import csv, pathlib, re, sys, yaml
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verify"))
from check_quotes import check_rows
review = list(csv.DictReader(open(ROOT / "claims/review/review.csv", encoding="utf-8-sig")))
blank = [r["id"] for r in review if r["keep"] not in ("y", "n")]
if blank: sys.exit(f"keep must be y or n on every row; blank: {blank[:10]}")
cands = {}
for f in (ROOT / "claims/candidates").glob("*.yaml"):
    for c in yaml.safe_load(f.read_text(encoding="utf-8")) or []:
        cands[(c["source_id"], c["id"])] = c
def plans(p):
    out = []
    for x in p or ["unknown"]:
        for y in re.split(r"[/,]", str(x)):
            y = re.sub(r"\s*plan$", "", y.strip().lower())
            if y and y not in out: out.append(y)
    return out or ["unknown"]
lib, groups, missing = [], {}, []
for r in review:
    if r["keep"] != "y": continue
    c = cands.get((r["source_id"], r["id"]))
    if c is None: missing.append(r["id"]); continue
    row = {k: c[k] for k in ("id", "version", "topic", "claim", "source_id", "source_quote", "checked", "status")}
    row["checked"] = str(row["checked"])
    row["plan_scope"] = plans(c.get("plan_scope"))
    row["conflicts_with"] = []
    m = re.match(r"CONFLICT ([A-Z]):", r["note"] or "")
    if m: groups.setdefault(m.group(1), []).append(row)
    if (r["note"] or "").startswith("Important:"): row["approver_note"] = r["note"][len("Important: "):]
    lib.append(row)
if missing: sys.exit(f"review rows with no candidate (re-run make_review_sheet?): {missing}")
ids = [x["id"] for x in lib]
dups = sorted({i for i in ids if ids.count(i) > 1})
if dups: sys.exit(f"duplicate ids among kept rows: {dups}")
for letter, members in groups.items():
    for row in members:
        row["conflicts_with"] = [o["id"] for o in members if o is not row]
        row["status"] = "conflicting"
problems = check_rows(lib)
if problems: sys.exit("quote check failed, nothing written:\n - " + "\n - ".join(problems))
out = ROOT / "claims/library.yaml"
header = "# CONTROLLED. Written by scripts/promote_claims.py from claims/review/review.csv. Do not edit by prompt.\n"
out.write_text(header + yaml.safe_dump(lib, sort_keys=False, allow_unicode=True, width=1000), encoding="utf-8", newline="\n")
print(f"wrote {out}: {len(lib)} claims, {sum(r['status']=='conflicting' for r in lib)} conflicting in {len(groups)} groups ({', '.join(sorted(groups))}), "
      f"{sum(r['status']=='in-progress' for r in lib)} in-progress, {sum(r['status']=='unknown' for r in lib)} unknown")
