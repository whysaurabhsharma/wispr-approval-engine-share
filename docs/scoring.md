# Account scoring (provisional)

The ranking in `scoring/score_accounts.py` orders accounts so the first briefs go where an approver conversation is most likely to help. It is a reasoned guess, not a validated model.

**Why provisional.** Validating a ranking needs outcomes: which accounts with Flow users went on to buy a company plan. Only Wispr has that data. Until Phase 4 brings it, the weights in `scoring/weights.yaml` are not tuned to anything, and no rank should be presented to Wispr as predictive.

**Inputs and weights.**
- Count variant (synthetic or, later, Wispr's own data): penetration (users / employees), absolute users, no team plan, no SSO, regulated industry, any public signal.
- Public-signal variant (real companies, public evidence only): strength of public evidence (strong 2.0, medium 1.0, weak 0.5) and regulated industry. No user counts are ever stated or estimated.

**Rules.**
- Every rank carries its top three reasons, so a reader can disagree with a specific input.
- Employee counts stay blank unless taken from a dated public source.
- `it_contact` holds a role only, never a name, until Wispr supplies contacts.
- A weight changes only with a dated line in `docs/decisions.md` saying why.

**How it gets validated (Phase 4).** If Wispr shares which accounts converted, rank those accounts blind, compare with the outcomes, adjust weights, and record the before and after in `docs/decisions.md`.
