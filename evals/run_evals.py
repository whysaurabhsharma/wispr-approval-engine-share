"""One command runs everything. Phase 0: skeleton checks. Later phases add test files under evals/."""
import pathlib, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
ok = True
def req(cond, msg):
    global ok
    print(("PASS " if cond else "FAIL ") + msg); ok = ok and cond
req((ROOT / "CLAUDE.md").exists(), "CLAUDE.md present")
req((ROOT / "claims/library.yaml").exists(), "claims library present")
req((ROOT / "inputs/accounts/SAMPLE_accounts.csv").exists(), "synthetic accounts present (run scripts/make_synthetic.py)")
drafts = list((ROOT / "outputs/review").glob("**/*.md"))
req(bool(drafts), "at least one draft in outputs/review (run /it-brief in Claude Code)")
for d in drafts:
    r = subprocess.run([sys.executable, str(ROOT / "verify/check_ids.py"), str(d)], capture_output=True, text=True)
    req(r.returncode == 0, f"id check: {d.name} {r.stdout.strip()}")
r = subprocess.run([sys.executable, "-m", "pytest", "-q", str(ROOT / "evals")], capture_output=True, text=True)
req(r.returncode == 0, "pytest: " + (r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "no output"))
sys.exit(0 if ok else 1)
