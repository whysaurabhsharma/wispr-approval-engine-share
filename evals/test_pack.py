"""Stage 2.4 evals on the approval pack (outputs are local drafts, so tests skip if a pack is missing)."""
import pathlib, re, sys, yaml, pytest
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verify"))
from check_ids import check, library_hash
PACK = ROOT / "outputs/review/approval-pack/approver-core.md"
PLANTED = ROOT / "outputs/review/approval-pack/planted-unanswerable.md"
STATUSES = {"ready", "partial", "ready-confirm", "escalate"}
LIB = {r["id"]: r for r in yaml.safe_load((ROOT / "claims/library.yaml").read_text(encoding="utf-8"))}
def rows(path):
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 6 and re.fullmatch(r"[a-z]+\d+", cells[0]):
            out[cells[0]] = {"answer": cells[3], "status": cells[4].strip("*` ").lower()}
    return out
def qids(path):
    return [c.strip() for line in path.read_text(encoding="utf-8").splitlines()
            for c in [line.strip().strip("|").split("|")[0]] if re.fullmatch(r"[a-z]+\d+", c.strip())]
def escalates(text): return "not found in sources" in text.lower()
def need(p):
    if not p.exists(): pytest.skip(f"{p.name} not generated yet")
def test_coverage_every_question_has_a_status():
    need(PACK); R = rows(PACK)
    missing = [q for q in qids(ROOT / "inputs/questions/approver-core.md") if q not in R]
    bad = {q: r["status"] for q, r in R.items() if r["status"] not in STATUSES}
    assert not missing and not bad, (missing, bad)
def test_ready_never_contains_an_escalation():
    need(PACK)
    assert not [q for q, r in rows(PACK).items() if r["status"] == "ready" and escalates(r["answer"])]
def test_escalate_rows_say_so():
    need(PACK)
    assert not [q for q, r in rows(PACK).items() if r["status"] == "escalate" and not escalates(r["answer"])]
def test_ids_and_hash_current():  # drift: any library change or conflicting citation fails here until the pack is rerun
    need(PACK)
    assert check(PACK) == []
def test_plan_scoped_claims_name_their_plan():
    need(PACK); problems = []
    for q, r in rows(PACK).items():
        for cid in re.findall(r"\[([a-z0-9]+(?:_[a-z0-9]+)+)\]", r["answer"]):
            scope = [p for p in LIB.get(cid, {}).get("plan_scope", []) if p not in ("unknown", "all")]
            names = {w for p in scope for w in re.split(r"[-\s]", p) if w not in ("tier", "plan")}
            if scope and not any(n in r["answer"].lower() for n in names):
                problems.append(f"{q}: [{cid}] is {scope} but the answer names no plan")
    assert not problems, problems
def test_planted_unanswerable_questions_escalate():
    need(PLANTED); R = rows(PLANTED)
    assert R and all(r["status"] == "escalate" for r in R.values()), {q: r["status"] for q, r in R.items()}
