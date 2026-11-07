"""Code check for claim rows: schema valid, quote short, quote really appears in the sanitised snapshot.
Usage: python verify/check_quotes.py <claims.yaml> [more.yaml ...]"""
import pathlib, re, sys, yaml
ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCES = {s["id"]: s for s in yaml.safe_load((ROOT / "claims/sources.yaml").read_text(encoding="utf-8"))}
STATUSES = {"confirmed", "conflicting", "unknown", "in-progress", "retired"}
TOPICS = {"privacy", "governance", "consent", "compliance", "security", "pricing", "product", "legal", "competitor"}
ID_RE = re.compile(r"^[a-z0-9]+(_[a-z0-9]+)+$")  # must contain an underscore, so [unknown] is never a claim id
DANGLING = {"is", "are", "was", "be", "the", "a", "an", "and", "or", "to", "of", "with", "for", "by", "that", "not"}
REQUIRED = ["id", "version", "topic", "claim", "source_id", "source_quote", "checked", "status", "plan_scope"]
def norm(s: str) -> str:
    s = s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    return re.sub(r"\s+", " ", s).strip().lower()
def snapshot_text(source_id: str):
    snaps = sorted((ROOT / "claims/snapshots" / source_id).glob("*.md"))
    return norm(snaps[-1].read_text(encoding="utf-8")) if snaps else None
def check_rows(rows) -> list:
    problems, seen = [], set()
    for i, r in enumerate(rows or []):
        tag = r.get("id", f"row {i}")
        for f in REQUIRED:
            if f not in r: problems.append(f"{tag}: missing field {f}")
        if not ID_RE.match(str(r.get("id", ""))): problems.append(f"{tag}: id must be lower_snake_case with at least one underscore")
        if r.get("id") in seen: problems.append(f"{tag}: duplicate id")
        seen.add(r.get("id"))
        if r.get("status") not in STATUSES: problems.append(f"{tag}: status {r.get('status')} not in {sorted(STATUSES)}")
        if r.get("topic") not in TOPICS: problems.append(f"{tag}: topic {r.get('topic')} not in {sorted(TOPICS)}")
        sid, quote = r.get("source_id"), str(r.get("source_quote") or "")
        if sid not in SOURCES: problems.append(f"{tag}: source_id {sid} not in sources.yaml"); continue
        if r.get("status") == "unknown" and not quote: continue  # unknowns may have no quote
        if r.get("status") == "retired": continue  # retired rows keep their old quote as history
        if not quote: problems.append(f"{tag}: empty source_quote"); continue
        if len(quote.split()) >= 15: problems.append(f"{tag}: quote is {len(quote.split())} words (limit 14)")
        if quote.split() and quote.split()[-1].strip(".,;:").lower() in DANGLING:
            problems.append(f"{tag}: quote ends mid-sentence on '{quote.split()[-1]}' and may not prove the claim")
        text = snapshot_text(sid)
        if text is None: problems.append(f"{tag}: no snapshot for {sid}")
        elif norm(quote) not in text: problems.append(f"{tag}: quote not found verbatim in {sid} snapshot")
    return problems
if __name__ == "__main__":
    allp = []
    for a in sys.argv[1:]:
        allp += [f"{a}: {p}" for p in check_rows(yaml.safe_load(pathlib.Path(a).read_text(encoding="utf-8")))]
    print("PASS" if not allp else f"FAIL ({len(allp)})")
    for p in allp: print(" -", p)
    sys.exit(1 if allp else 0)
