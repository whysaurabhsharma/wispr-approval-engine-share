import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from build_case import build
def test_outcome_doc_sample():
    r = build(142, 4, 60, 18)
    assert r["monthly_value"] == 34080 and r["monthly_cost"] == 2556 and r["ratio"] == 13.3
