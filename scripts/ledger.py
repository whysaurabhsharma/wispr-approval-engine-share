"""Append-only ledgers.
Usage: ledger.py run <skill> <input> <result> <cost_usd>
       ledger.py state <file> <draft|reviewed|approved|sent|stale> <who>"""
import datetime, hashlib, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
RUNS, OUTS = ROOT / "ledger/runs.jsonl", ROOT / "ledger/outputs.jsonl"
def now(): return datetime.datetime.now().isoformat(timespec="seconds")
def run(skill, inp, result, cost):
    RUNS.open("a").write(json.dumps({"t": now(), "skill": skill, "input": inp, "result": result, "cost_usd": float(cost)}) + "\n")
def state(file, new_state, who):
    assert new_state in {"draft", "reviewed", "approved", "sent", "stale"}, "bad state"
    p = pathlib.Path(file); h = hashlib.sha256(p.read_bytes()).hexdigest()[:12]
    OUTS.open("a").write(json.dumps({"t": now(), "file": str(p), "state": new_state, "by": who, "hash": h}) + "\n")
def latest(file):
    rows = [json.loads(l) for l in OUTS.read_text().splitlines() if l.strip()] if OUTS.exists() else []
    rows = [r for r in rows if r["file"] == str(file)]
    return rows[-1] if rows else None
if __name__ == "__main__":
    cmd, *a = sys.argv[1:]
    {"run": run, "state": state}[cmd](*a); print("ok")
