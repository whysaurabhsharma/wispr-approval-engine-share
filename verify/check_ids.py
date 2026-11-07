"""Stage A verification: every [claim_id] in an output exists, is confirmed, and the header hash matches."""
import hashlib, pathlib, re, sys, yaml
ROOT = pathlib.Path(__file__).resolve().parents[1]
LIB = ROOT / "claims/library.yaml"
def library_hash() -> str:
    return hashlib.sha256(LIB.read_bytes()).hexdigest()[:12]
def check(path: pathlib.Path) -> list:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    if not m:
        return ["no header"]
    header, body = yaml.safe_load(m.group(1)) or {}, m.group(2)
    claims = {c["id"]: c for c in yaml.safe_load(LIB.read_text(encoding="utf-8"))}
    problems = []
    if header.get("library_hash") != library_hash():
        problems.append(f"library_hash {header.get('library_hash')} != current {library_hash()} (stale)")
    cited = set(re.findall(r"\[([a-z0-9]+(?:_[a-z0-9]+)+)\]", body))  # ids always contain an underscore; [unknown] is a placeholder
    for cid in cited:
        if cid not in claims:
            problems.append(f"unknown claim id [{cid}]")
        elif claims[cid]["status"] != "confirmed":
            problems.append(f"[{cid}] status is {claims[cid]['status']}")
    for cid in header.get("claims_used", []) or []:
        if cid not in cited:
            problems.append(f"header lists [{cid}] but body never cites it")
    return problems
if __name__ == "__main__":
    p = pathlib.Path(sys.argv[1]); probs = check(p)
    print("PASS" if not probs else "FAIL")
    for x in probs: print(" -", x)
    sys.exit(1 if probs else 0)
