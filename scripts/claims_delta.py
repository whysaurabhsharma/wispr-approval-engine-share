"""Update the CONTROLLED library from refreshed candidates, without re-reviewing everything.
  python scripts/claims_delta.py build <source_id> [...]  -> claims/review/delta.csv (retire rows whose quote vanished, add genuinely new rows)
  python scripts/claims_delta.py apply                     -> applies keep=y rows to claims/library.yaml, re-runs the quote check
Retired rows stay in the library with status retired and retired_on, so history is kept."""
import csv, datetime, pathlib, sys, yaml
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verify"))
from check_quotes import norm, snapshot_text, check_rows
LIB, DELTA = ROOT / "claims/library.yaml", ROOT / "claims/review/delta.csv"
HEADER = "# CONTROLLED. Written by scripts/promote_claims.py and scripts/claims_delta.py. Do not edit by prompt.\n"
COLS = ["keep", "action", "id", "source_id", "topic", "status", "plan_scope", "claim", "source_quote", "note"]
def load_lib(): return yaml.safe_load(LIB.read_text(encoding="utf-8"))
def save_lib(rows): LIB.write_text(HEADER + yaml.safe_dump(rows, sort_keys=False, allow_unicode=True, width=1000), encoding="utf-8", newline="\n")
def build(*sources):
    if DELTA.exists(): sys.exit(f"{DELTA} exists; apply or delete it first so your edits are never overwritten")
    lib = load_lib(); ids = {r["id"] for r in lib}; out = []
    for sid in sources:
        text = snapshot_text(sid) or ""
        live = [r for r in lib if r["source_id"] == sid and r["status"] != "retired"]
        for r in live:
            if norm(str(r["source_quote"])) not in text:
                out.append({"keep": "y", "action": "retire", **{k: r.get(k) for k in COLS[2:9]}, "note": "quote no longer on the page"})
        have = {norm(str(r["source_quote"])) for r in live if norm(str(r["source_quote"])) in text}
        for c in yaml.safe_load((ROOT / f"claims/candidates/{sid}.yaml").read_text(encoding="utf-8")) or []:
            if norm(str(c["source_quote"])) in have: continue
            cid = c["id"] if c["id"] not in ids else f"{c['id']}_v2"
            out.append({"keep": "", "action": "add", "id": cid, **{k: c.get(k) for k in COLS[3:9]}, "note": ""})
    for r in out: r["plan_scope"] = ",".join(map(str, r["plan_scope"] or []))
    DELTA.parent.mkdir(parents=True, exist_ok=True)
    with DELTA.open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS); w.writeheader(); w.writerows(out)
    print(f"wrote {DELTA}: {sum(r['action']=='retire' for r in out)} retire, {sum(r['action']=='add' for r in out)} add")
def apply():
    rows = list(csv.DictReader(open(DELTA, encoding="utf-8-sig")))
    blank = [r["id"] for r in rows if r["keep"] not in ("y", "n")]
    if blank: sys.exit(f"keep must be y or n on every row; blank: {blank[:10]}")
    lib, today = load_lib(), datetime.date.today().isoformat()
    by_id = {r["id"]: r for r in lib}
    retired = added = 0
    for d in rows:
        if d["keep"] != "y": continue
        if d["action"] == "retire" and d["id"] in by_id:
            by_id[d["id"]]["status"], by_id[d["id"]]["retired_on"] = "retired", today; retired += 1
        elif d["action"] == "add":
            if d["id"] in by_id: sys.exit(f"id {d['id']} already in library")
            row = {"id": d["id"], "version": 1, "topic": d["topic"], "claim": d["claim"], "source_id": d["source_id"],
                   "source_quote": d["source_quote"], "checked": today, "status": d["status"],
                   "plan_scope": [p for p in d["plan_scope"].split(",") if p] or ["unknown"], "conflicts_with": []}
            lib.append(row); by_id[row["id"]] = row; added += 1
    problems = check_rows(lib)
    if problems: sys.exit("quote check failed, library NOT written:\n - " + "\n - ".join(problems))
    save_lib(lib); stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    done = DELTA.with_name(f"delta_applied_{stamp}.csv"); DELTA.rename(done)
    print(f"library: {retired} retired, {added} added -> {len([r for r in lib if r['status'] != 'retired'])} live claims; delta saved as {done.name}")
if __name__ == "__main__":
    {"build": build, "apply": apply}[sys.argv[1]](*sys.argv[2:])
