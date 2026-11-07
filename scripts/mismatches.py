"""Mismatch register helper. Code only, no AI.
  python scripts/mismatches.py batch [pairs.yaml] [library.yaml] [out_dir]   -> batch files of 30 pairs for mismatch-judge
  python scripts/mismatches.py build                                         -> claims/mismatches.yaml from verdict files (keeps your statuses)
  python scripts/mismatches.py score <verdicts.yaml> <expected.yaml>         -> planted-pair eval"""
import datetime, pathlib, sys, yaml
ROOT = pathlib.Path(__file__).resolve().parents[1]
FLAG = {"contradiction", "stale", "scope-gap"}
STATUSES = {"open", "accepted", "fixed", "false-positive"}
def load(p): return yaml.safe_load(pathlib.Path(p).read_text(encoding="utf-8"))
def dump(p, data, header=""):
    p = pathlib.Path(p); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(header + yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=1000), encoding="utf-8", newline="\n")
def slim(r): return {k: r.get(k) for k in ("id", "claim", "source_id", "source_quote", "checked", "status", "plan_scope")}
def batch(pairs_p=ROOT / "claims/diff_pairs.yaml", lib_p=ROOT / "claims/library.yaml", out=ROOT / "claims/review/mismatch_batches"):
    lib = {r["id"]: r for r in load(lib_p)}
    pairs = load(pairs_p); out = pathlib.Path(out)
    for old in out.glob("batch_*.yaml"): old.unlink()
    items = [{"pair": f"{p['a']}|{p['b']}", "a": slim(lib[p["a"]]), "b": slim(lib[p["b"]])} for p in pairs]
    n = 0
    for i in range(0, len(items), 30):
        n += 1; dump(out / f"batch_{n:02d}.yaml", items[i:i + 30])
    print(f"{len(items)} pairs -> {n} batch files in {out}")
def build():
    bdir, vdir = ROOT / "claims/review/mismatch_batches", ROOT / "claims/review/mismatch_verdicts"
    reg_p = ROOT / "claims/mismatches.yaml"
    old = {m["pair"]: m for m in (load(reg_p) or [])} if reg_p.exists() else {}
    verdicts, problems = {}, []
    for b in sorted(bdir.glob("batch_*.yaml")):
        v = vdir / b.name
        if not v.exists(): problems.append(f"no verdict file for {b.name}"); continue
        want = [x["pair"] for x in load(b)]; got = {x["pair"]: x for x in (load(v) or [])}
        missing = [p for p in want if p not in got]
        if missing: problems.append(f"{v.name}: {len(missing)} pairs without a verdict")
        verdicts.update({p: got[p] for p in want if p in got})
    if problems: sys.exit("not building, fix first:\n - " + "\n - ".join(problems))
    pairs = {f"{x['a']['id']}|{x['b']['id']}": x for b in sorted(bdir.glob("batch_*.yaml")) for x in load(b)}
    next_n = max([int(m["id"][1:]) for m in old.values()] + [0]) + 1
    reg, today = [], datetime.date.today().isoformat()
    for key, v in verdicts.items():
        if v.get("verdict") not in FLAG: continue
        prev = old.get(key, {})
        mid = prev.get("id") or f"M{next_n:03d}"
        if "id" not in prev: next_n += 1
        status = prev.get("status", "open"); status = status if status in STATUSES else "open"
        reg.append({"id": mid, "pair": key, "type": v.get("type", "unlabelled"), "verdict": v["verdict"],
                    "severity": v.get("severity", "medium"), "status": status, "note": prev.get("note", ""), "reason": v.get("reason", ""),
                    "first_seen": prev.get("first_seen", today), "claim_a": pairs[key]["a"], "claim_b": pairs[key]["b"]})
    RETIRED = {r["id"] for r in load(ROOT / "claims/library.yaml") if r.get("status") == "retired"}
    flagged = {r["pair"] for r in reg}
    gone = [m["id"] for k, m in old.items() if k not in flagged]
    for k, m in old.items():  # keep history: items no longer flagged stay in the register, closed
        if k in flagged: continue
        retired = [c for c in m["pair"].split("|") if c in RETIRED]
        if retired and m.get("status") in ("open", "accepted"):
            m["status"], m["closed_on"] = "fixed", m.get("closed_on", today)
            m["note"] = (m.get("note", "") + f" | fixed on {today}: Wispr removed the wording ({', '.join(retired)})").strip(" |")
        elif not retired and "not re-flagged" not in m.get("note", ""):
            m["note"] = (m.get("note", "") + f" | not re-flagged on {today} (judge variance); status kept").strip(" |")
        reg.append(m)
    reg.sort(key=lambda m: ({"high": 0, "medium": 1, "low": 2}.get(m["severity"], 3), m["type"], m["id"]))
    dump(reg_p, reg, "# CONTROLLED. Written by scripts/mismatches.py build. Edit only the status field: open | accepted | fixed | false-positive\n")
    from collections import Counter
    print(f"{len(verdicts)} pairs judged -> {len(reg)} mismatches "
          f"({dict(Counter(m['verdict'] for m in reg))}; {dict(Counter(m['severity'] for m in reg))}) -> {reg_p}")
    print("types:", ", ".join(f"{t} {c}" for t, c in Counter(m["type"] for m in reg).most_common()))
    if gone: print("no longer flagged, kept as fixed (check each):", gone)
def triage():
    reg_p, tri_p = ROOT / "claims/mismatches.yaml", ROOT / "claims/review/mismatch_triage.yaml"
    reg, tri = load(reg_p), {x["id"]: x for x in load(tri_p)}
    bad = [x["id"] for x in tri.values() if x["status"] not in STATUSES]
    if bad: sys.exit(f"invalid status on {bad}")
    for m in reg:
        if m.get("closed_on"): continue  # closed by a source change; reopen only by editing the register
        if m["id"] in tri: m["status"], m["note"] = tri[m["id"]]["status"], tri[m["id"]].get("note", "")
    dump(reg_p, reg, "# CONTROLLED. Written by scripts/mismatches.py build. Edit only the status field: open | accepted | fixed | false-positive\n")
    from collections import Counter
    untriaged = [m["id"] for m in reg if m["id"] not in tri]
    print("triage applied:", dict(Counter(m["status"] for m in reg)), "| not in triage file:", untriaged or "none")
def score(verdicts_p, expected_p):
    got = {v["pair"]: v["verdict"] for v in load(verdicts_p)}
    exp = load(expected_p); ok = True
    for e in exp:
        flagged = got.get(e["pair"]) in FLAG
        good = flagged == e["flag"]; ok &= good
        print(("PASS" if good else "FAIL"), e["pair"], "expected", "flag" if e["flag"] else "no flag", "got", got.get(e["pair"]))
    print("PLANTED EVAL", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    {"batch": batch, "build": build, "triage": triage, "score": score}[cmd](*args)
