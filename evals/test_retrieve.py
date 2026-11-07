import pathlib, subprocess, sys, tempfile, yaml
ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = pathlib.Path(tempfile.mkdtemp()) / "retrieval.yaml"
subprocess.run([sys.executable, str(ROOT / "scripts/retrieve.py"), str(ROOT / "inputs/questions/approver-core.md"), str(OUT)], check=True)
R = {q["id"]: [c["id"] for c in q["claims_retrieved"]] for q in yaml.safe_load(OUT.read_text(encoding="utf-8"))}
LIB = {r["id"]: r for r in yaml.safe_load((ROOT / "claims/library.yaml").read_text(encoding="utf-8"))}
def test_every_question_has_a_row():
    assert len(R) >= 30
def test_sso_found():  # the miss from the Phase 1 brief
    assert {"saml_sso_growth_enterprise", "sso_saml_enforcement"} <= set(R["q01"])
def test_scim_found():
    assert "scim_provisioning_supported" in R["q02"]
def test_soc2_report_found():
    assert "soc2_type_ii_report" in R["q12"]
def test_residency_found():
    assert "no_data_residency_outside_us" in R["q16"]
def test_notetaker_under_baa_found():  # M002 was fixed on 2026-11-06: the "disabled under a BAA" side was retired
    assert "notetaker_works_alongside_baa" in R["q29"]
def test_retired_claims_never_retrieved():
    assert not [c for ids in R.values() for c in ids if LIB[c].get("status") == "retired"]
def test_no_competitor_claims():
    assert not [c for ids in R.values() for c in ids if LIB[c]["source_id"].startswith(("comp_", "ms_"))]
def test_metadata_still_sent_found():  # q21 escalated in the first pack run
    assert {"model_improvement_off_metadata_still_uploaded", "ca_off_still_sends_app_and_domain"} <= set(R["q21"])
def test_network_destinations_found():  # q06 gave no destination list in the first pack run
    assert "docs_network_wildcard_list_required" in R["q06"]
