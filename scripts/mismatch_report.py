"""Render the open items in claims/mismatches.yaml as a short, polite report for Wispr.
Code only: every statement and quote is copied from the register and claims/sources.yaml, never reworded.
Usage: python scripts/mismatch_report.py [out.md]"""
import datetime, pathlib, re, sys, yaml
ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "outputs/review/mismatch-report.md"
reg = yaml.safe_load((ROOT / "claims/mismatches.yaml").read_text(encoding="utf-8"))
src = {s["id"]: s for s in yaml.safe_load((ROOT / "claims/sources.yaml").read_text(encoding="utf-8"))}
lib_hash = __import__("subprocess").run([sys.executable, str(ROOT / "scripts/stamp.py")], capture_output=True, text=True).stdout.strip()
KIND = {"contradiction": "Two pages say different things", "stale": "An older statement has not caught up",
        "scope-gap": "A broad statement leaves out an exception"}
def title(m): return re.sub(r"\s*\((replaces|context verified|successor)[^)]*\)", "", m.get("note", m["type"]).split(" | ")[0]).strip()
def wispr(m): return not any(m[k]["source_id"].startswith(("comp_", "ms_", "legal_")) for k in ("claim_a", "claim_b"))
def latest(sid):
    snaps = sorted((ROOT / "claims/snapshots" / sid).glob("*.md"))
    return snaps[-1].stem if snaps else ""
def side(c):
    s = src.get(c["source_id"], {})
    return f"- {c['claim']} Page wording: \"{c['source_quote']}\" ({s.get('url', c['source_id'])}, checked {latest(c['source_id'])})"
open_ = [m for m in reg if m["status"] == "open" and wispr(m)]
tri_p = ROOT / "claims/review/mismatch_triage.yaml"
was_open = {x["id"] for x in (yaml.safe_load(tri_p.read_text(encoding="utf-8")) if tri_p.exists() else []) if x["status"] == "open"}
fixed = [m for m in reg if m["status"] == "fixed" and m.get("closed_on") and wispr(m) and m["id"] in was_open]
order = {"high": 0, "medium": 1, "low": 2}
vorder = {"contradiction": 0, "stale": 1, "scope-gap": 2}
open_.sort(key=lambda m: (order.get(m["severity"], 3), vorder.get(m["verdict"], 3), m["id"]))
today = datetime.date.today().isoformat()
L = [f"# Things an approver would notice on Wispr Flow's public pages",
     f"Prepared {today} from Wispr's public pages. Snapshot reference {lib_hash}. Private; not shared with anyone else.",
     "",
     "I read Wispr's public pages the way an IT, security, legal or finance approver does before a company-wide purchase, "
     "and kept a register of places where two pages could leave that reader unsure. Each item quotes both pages word for word, "
     "so you can check it in a minute. Some may already be known or intended; I may be wrong about any of them.",
     "",
     "If you read only three: " + "; ".join(f"{n}. {title(m)}" for n, m in enumerate(open_[:3], 1)) + ".",
     "",
     f"**{len(open_)} open items**, most important first. **{len(fixed)} earlier items were fixed by page changes on or before {max([m['closed_on'] for m in fixed], default=today)}** (listed at the end).",
     ""]
for n, m in enumerate(open_, 1):
    L += [f"## {n}. {title(m)}",
          f"*{KIND.get(m['verdict'], m['verdict'])}. Severity for an approver: {m['severity']}. Ref {m['id']}.*", "",
          side(m["claim_a"]), side(m["claim_b"]), ""]
if fixed:
    L += ["## Already fixed", "These were in the register and the wording changed on Wispr's pages, so they are closed:", ""]
    seen = set()
    for m in sorted(fixed, key=lambda m: m["id"]):
        tt = title(m)
        if tt in seen: continue
        seen.add(tt); L.append(f"- {tt} (closed {m['closed_on']}, ref {m['id']})")
    L.append("")
L += ["## How this was made",
      "Wispr's public pages are snapshotted, facts are extracted with the exact quote, and pairs that might disagree are judged by a second model. "
      "Every item above was then reviewed by hand; items that turned out to be compatible were dropped as false positives. "
      "The method and register are available if useful."]
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
print(f"wrote {OUT}: {len(open_)} open, {len(fixed)} fixed")
