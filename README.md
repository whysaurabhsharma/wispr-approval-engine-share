# Wispr Flow approval engine (shared copy)

Thanks for taking a look. This repo reads Wispr Flow's public pages the way an IT, security, legal or finance approver does before a company-wide purchase, and answers them with a source and exact quote behind every sentence. It is private, shared only with you, and nothing in it has been published.

## Start here (5 minutes)

1. **`outputs/mismatch-report.md`**: places where two of your public pages could leave an approver unsure, each quoted word for word with links, plus the items that your recent page changes already fixed. Start with the "If you read only three" line.
2. **`docs/engine-summary.md`**: one page on what the engine does, how it is checked, and what I am asking.
3. **`docs/problem-evidence.md`**: public evidence for and against the idea that approval is where company-wide purchases stall.

## What is in the repo

| Folder | What it holds |
|---|---|
| `claims/sources.yaml` | The 22 public pages read, each with a trust level |
| `claims/snapshots/` | Dated text copies of those pages (your pages, plus a few competitor and legal-context pages) |
| `claims/library.yaml` | Every fact extracted, each with the exact quote, page, date checked and status. Facts Wispr has since removed are kept as `retired` |
| `claims/mismatches.yaml` | The full register behind the report, including items judged false positives and why |
| `inputs/questions/` | The approver question sets (seeded from the CSA CAIQ v4.1 domains) |
| `scripts/`, `verify/`, `ingest/` | The code: fetching, cleaning, retrieval, quote checks, citation checks, reports |
| `.claude/` | The Claude Code skills and agents that draft and judge outputs |
| `evals/` | Tests, including a hand-labelled gold set and planted conflict and "cannot answer" cases |
| `ledger/` | A record of every run and every human review |
| `CLAUDE.md` | The rules every output follows |

## Why it can be trusted

- Code checks that every quote appears word for word on the page it cites, and that every citation points to a confirmed fact.
- One model drafts; a different model judges each sentence; an unsupported sentence blocks the output.
- Measured: 29 of 30 extracted facts correct against a hand-labelled set; 4 of 4 planted conflict tests; 3 of 3 planted unanswerable questions correctly escalated.
- Every output is reviewed by a person. Nothing is ever sent by the engine.

## Run the checks yourself

```
python -m venv .venv
.venv\Scripts\activate          # macOS or Linux: source .venv/bin/activate
pip install -r requirements.txt
python verify/check_quotes.py claims/library.yaml
python -m pytest -q evals
```

`check_quotes.py` confirms every quote in the library against the snapshots. Some tests check generated drafts that are not included here; those tests skip.

## Limits

- Pages were read between 5 and 7 November 2026. Your pages changed twice in that window; anything since then is not reflected.
- The engine only knows what your public pages say. Where they are silent, it says so and lists the question instead of guessing.
- Nothing here is legal advice.

Questions or corrections are very welcome; a correction becomes a test so the same mistake cannot recur.
