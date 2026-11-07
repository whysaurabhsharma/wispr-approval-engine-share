"""Find claim pairs worth checking for contradictions. Code only, no AI.
A pair is listed when two claims share a topic or a subject term and enough key words, or are already linked by conflicts_with.
Writes claims/diff_pairs.yaml for the /mismatch-report skill to judge.
Usage: python scripts/diff_claims.py [library.yaml] [out.yaml]"""
import itertools, pathlib, re, sys, yaml
ROOT = pathlib.Path(__file__).resolve().parents[1]
lib_path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "claims/library.yaml"
out_path = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "claims/diff_pairs.yaml"
lib = yaml.safe_load(lib_path.read_text(encoding="utf-8"))
lib = [r for r in lib if r.get("status") != "retired"]  # retired claims are history, not live statements
STOP = set("""a an the and or of to for in on with by at from is are be can its it this that as not no any all
user users users' admin admins page says states wispr flow willow apple microsoft per when if only also their
your into after before under each every such than more other""".split())
# subject terms: two claims about the same subject are compared even across topics
SUBJECTS = {"soc2": r"soc ?2", "iso27001": r"iso ?(/iec )?27001", "baa": r"\bbaa\b|business associate", "hipaa": r"hipaa",
            "notetaker": r"notetaker", "android": r"android", "sso": r"\bsso\b|single sign-on|saml", "scim": r"\bscim\b",
            "training": r"model training|improve the model|model improvement|train", "retention": r"retain|retention|deleted within|kept for",
            "residency": r"united states|\bus\b|residency|eea|region", "dpa": r"\bdpa\b|data processing", "subprocessor": r"subprocessor|sub-processor",
            "encryption": r"encrypt|tls|aes", "context": r"context awareness", "cloud_storage": r"cloud storage", "privacy_mode": r"privacy mode",
            "pricing": r"\$\d|price|pricing|per seat|billing"}
def words(t): return {w for w in re.findall(r"[a-z0-9]+", t.lower()) if w not in STOP and len(w) > 2}
def subjects(t): return {k for k, rx in SUBJECTS.items() if re.search(rx, t.lower())}
info = {r["id"]: (r, words(r["claim"]), subjects(r["claim"])) for r in lib}
pairs = {}
for a, b in itertools.combinations(info, 2):
    (ra, wa, sa), (rb, wb, sb) = info[a], info[b]
    if ra["source_id"].startswith(("comp_", "ms_", "legal_")) != rb["source_id"].startswith(("comp_", "ms_", "legal_")):
        continue  # never compare Wispr claims with competitor or legal claims
    if ra["source_id"].startswith(("comp_", "ms_")) and ra["source_id"].split("_")[:2] != rb["source_id"].split("_")[:2]:
        continue  # each competitor is compared only with itself
    linked = b in (ra.get("conflicts_with") or []) or a in (rb.get("conflicts_with") or [])
    shared_subj = sa & sb
    overlap = len(wa & wb) / max(1, min(len(wa), len(wb)))
    if linked or (shared_subj and overlap >= 0.35) or (ra["topic"] == rb["topic"] and overlap >= 0.5):
        key = tuple(sorted((a, b)))
        pairs[key] = {"a": key[0], "b": key[1], "linked": linked, "subjects": sorted(shared_subj), "overlap": round(overlap, 2),
                      "same_source": ra["source_id"] == rb["source_id"]}
watch_p = ROOT / "claims/watch_pairs.yaml"  # human-chosen pairs that are always judged, whatever their wording
for w in (yaml.safe_load(watch_p.read_text(encoding="utf-8")) or []) if watch_p.exists() else []:
    if w["a"] in info and w["b"] in info:
        key = tuple(sorted((w["a"], w["b"])))
        pairs[key] = {"a": key[0], "b": key[1], "linked": True, "subjects": ["watch"], "overlap": 0, "same_source": False}
    else: print("watch pair skipped, id not in library:", w)
ordered = sorted(pairs.values(), key=lambda p: (not p["linked"], -len(p["subjects"]), -p["overlap"]))
out_path.write_text(yaml.safe_dump(ordered, sort_keys=False), encoding="utf-8", newline="\n")
print(f"{len(lib)} claims -> {len(ordered)} pairs to judge ({sum(p['linked'] for p in ordered)} already linked) -> {out_path}")
