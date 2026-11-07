---
account: {account_id}
type: business-case
generated: {timestamp}
claims_used: []
claims_retrieved: []
library_hash: {library_hash}
reviewed_by:
status: draft
sample_data: {true|false}
variant: {count|public-signal}
---
# Business case: Wispr Flow at {company}

## Summary
{Two or three sentences: what the numbers show at the placeholder inputs, and the break-even. No claim that Flow will save any specific amount.}

## Price
{Each listed price with its claim id and plan. If the pages list more than one price for a plan, show all and say which to confirm with Wispr.}

## Per-user economics
{Paste the table and break-even lines printed by scripts/build_case.py. Count variant: also the table for the account's user count.}

## Inputs and placeholders
- Hours saved per user per month: placeholder. Wispr publishes no per-user hours figure. Replace with the company's own measurement.
- Loaded cost per hour: placeholder. Replace with the company's figure.
- Users: {count variant: from the account row, SAMPLE | public-signal: no user count; figures are per user}

## How Flow compares with built-in dictation
| | Wispr Flow | Apple Dictation (Mac) | Microsoft fluid dictation (Windows) |
|---|---|---|---|
| {row} | {cell with claim id or "not stated"} | ... | ... |

## When built-in dictation is enough
{Mandatory. When the built-in tools cover the need, from competitor claims, said plainly.}

## Open questions for Wispr
- {mismatch id}: {what to confirm}

## Sources
{source ids and URLs for every claim used}
