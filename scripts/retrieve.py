"""Retrieve candidate claims for each question. Code only, no AI.
Keyword search over claim text (with a small synonym list) plus a bonus for matching topics.
Competitor claims are never retrieved; legal-context claims only for legal or consent questions.
Usage: python scripts/retrieve.py [questions.md] [out.yaml]"""
import math, pathlib, re, sys, yaml
ROOT = pathlib.Path(__file__).resolve().parents[1]
Q_PATH = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "inputs/questions/approver-core.md"
OUT = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "outputs/review/approval-pack/retrieval.yaml"
TOP_K, MIN_SCORE = 12, 1.0
STOP = set("""a an the and or of to for in on with by at from is are be can do does we our us you your it its this that
which what who how when where there their them any all each every on off out into about as not no yes use used using""".split())
SYN = {"sso": ["saml", "single", "sign"], "saml": ["sso"], "scim": ["provisioning", "provision"], "provision": ["scim"],
       "personal": ["individual"], "mdm": ["deployment", "managed"], "residency": ["united", "states", "region", "eea"],
       "region": ["residency", "united", "states"], "subprocessors": ["subprocessor", "providers"], "train": ["training", "improvement", "improve"],
       "training": ["train", "improvement", "improve"], "retention": ["retain", "retained", "kept", "deleted", "zero"],
       "kept": ["retain", "retained", "retention"], "encrypted": ["encryption", "encrypts", "tls", "aes"], "encryption": ["encrypted", "tls", "aes"],
       "keys": ["key", "byok"], "logged": ["audit", "logs", "log"], "logs": ["audit", "log", "siem"], "siem": ["audit", "logs"],
       "vulnerabilities": ["vulnerability", "penetration", "bug"], "incidents": ["incident", "breach"], "outage": ["availability", "sla", "uptime"],
       "sla": ["slas", "support", "uptime"], "dpa": ["processing", "addendum", "scc", "sccs"], "baa": ["business", "associate", "hipaa"],
       "notetaker": ["meeting", "meetings"], "consent": ["notice", "notification", "confirmation"], "bot": ["bot", "join", "device"],
       "cost": ["price", "pricing", "$"], "invoice": ["invoicing", "po", "billing"], "seat": ["seats", "minimum"], "plan": ["plans"],
       "delete": ["deletion", "deleting", "deleted"], "export": ["download", "archive"], "audit": ["soc", "iso", "audited", "assessed"],
       "soc": ["soc2", "audit"], "iso": ["27001", "certificate"], "network": ["domains", "destinations", "allowlist", "tls"],
       "ip": ["allowlist", "cidr"], "sent": ["send", "upload", "uploaded", "metadata"], "collected": ["upload", "send", "metadata", "collect"],
       "sharing": ["improvement", "share"], "allow": ["wildcard", "allowlist", "bypas"], "context": ["awareness"], "platforms": ["mac", "windows", "ios", "android"], "device": ["local", "history"]}
def stem(w): return w[:-1] if len(w) > 4 and w.endswith("s") and not w.endswith("ss") else w
def words(t):
    return [stem(w) for w in re.findall(r"[a-z0-9$]+", t.lower()) if w not in STOP and len(w) > 1]
def expand(ws):
    out = set(ws)
    for w in ws: out.update(stem(s) for s in SYN.get(w, []))
    return out
def questions(path):
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 6 and re.fullmatch(r"[a-z]+\d+", cells[0]):
            rows.append({"id": cells[0], "reviewer": cells[1], "question": cells[2],
                         "topics": [t.strip() for t in cells[3].split(",")], "caiq": cells[4], "drata_covers": cells[5]})
    return rows
lib = yaml.safe_load((ROOT / "claims/library.yaml").read_text(encoding="utf-8"))
lib = [r for r in lib if r.get("status") != "retired"]
docs = {r["id"]: set(words(r["claim"] + " " + r["id"].replace("_", " "))) for r in lib}
N = len(lib); df = {}
for ws in docs.values():
    for w in ws: df[w] = df.get(w, 0) + 1
idf = {w: math.log((N + 1) / (c + 0.5)) for w, c in df.items()}
out = []
for q in questions(Q_PATH):
    qw = expand(words(q["question"]))
    allow_legal = bool({"legal", "consent"} & set(q["topics"]))
    scored = []
    for r in lib:
        sid = r["source_id"]
        if sid.startswith(("comp_", "ms_")) or (sid.startswith("legal_") and not allow_legal): continue
        hit = qw & docs[r["id"]]
        if not hit: continue
        s = sum(idf.get(w, 0) for w in hit) + (0.5 if r["topic"] in q["topics"] else 0)
        if s >= MIN_SCORE: scored.append((round(s, 2), r))
    scored.sort(key=lambda x: -x[0])
    top = scored[:TOP_K]
    out.append({**q, "claims_retrieved": [{"id": r["id"], "score": s, "status": r["status"], "plan_scope": r["plan_scope"]} for s, r in top]})
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True, width=1000), encoding="utf-8", newline="\n")
empty = [q["id"] for q in out if not q["claims_retrieved"]]
print(f"{len(out)} questions -> {OUT}; avg {sum(len(q['claims_retrieved']) for q in out) / max(1, len(out)):.1f} claims each; no claims: {empty or 'none'}")
