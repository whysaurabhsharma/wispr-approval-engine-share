import sys, pathlib, tempfile, yaml
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verify"))
from check_ids import check, library_hash, LIB
ROWS = yaml.safe_load(LIB.read_text(encoding="utf-8"))
CONFIRMED = next(r["id"] for r in ROWS if r["status"] == "confirmed")
CONFLICTING = next((r["id"] for r in ROWS if r["status"] == "conflicting"), None)
def _write(body, hash_=None):
    h = hash_ or library_hash()
    p = pathlib.Path(tempfile.mkdtemp()) / "x.md"
    p.write_text(f"---\naccount: t\ntype: it-brief\nclaims_used: []\nlibrary_hash: {h}\nstatus: draft\n---\n{body}", encoding="utf-8")
    return p
def test_confirmed_claim_passes():
    assert check(_write(f"A fact [{CONFIRMED}].")) == []
def test_unknown_id_fails():
    assert any("unknown claim id" in x for x in check(_write("Made up [not_a_claim].")))
def test_conflicting_claim_fails():
    assert CONFLICTING, "library should hold at least one conflicting claim"
    assert any("status is conflicting" in x for x in check(_write(f"Contested [{CONFLICTING}].")))
def test_stale_hash_fails():
    assert any("stale" in x for x in check(_write(f"ok [{CONFIRMED}].", hash_="deadbeef0000")))
def test_placeholder_is_not_an_id():
    assert check(_write(f"Champion: [unknown]. Fact [{CONFIRMED}].")) == []
