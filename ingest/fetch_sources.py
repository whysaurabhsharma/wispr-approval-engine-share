"""Fetch allowlisted sources only (GET), save raw HTML + fetch log. Read-only by design."""
import datetime, json, pathlib, yaml, requests
ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCES = yaml.safe_load((ROOT / "claims/sources.yaml").read_text())
LOG = ROOT / "claims/snapshots/fetch_log.jsonl"
today = datetime.date.today().isoformat()
for s in SOURCES:
    out = ROOT / "claims/snapshots" / s["id"]; out.mkdir(parents=True, exist_ok=True)
    rec = {"id": s["id"], "url": s["url"], "date": today}
    try:
        r = requests.get(s["url"], timeout=30, headers={"User-Agent": "approval-engine/0.1 (read-only)"})
        rec["status"] = r.status_code
        if r.ok:
            (out / f"{today}.html").write_text(r.text, encoding="utf-8")
        else:
            rec["stale"] = True
    except Exception as e:  # keep last good snapshot, mark stale
        rec.update(status="error", error=str(e), stale=True)
    LOG.open("a").write(json.dumps(rec) + "\n")
    print(rec)
