# Wispr Flow approval engine: one-page summary

**What it is.** A small engine that answers the people who approve a company-wide Flow purchase (IT, security, legal, finance) using only Wispr's own public pages, with a source and exact quote behind every sentence. It is built for the moment after employees already use Flow and someone has to say yes.

**What it found (pages checked 5 to 7 November 2026).**
- 22 public pages read; 361 live facts, each with a quote checked word for word against the page.
- 16 open places where two Wispr pages could leave an approver unsure, including direct contradictions on which plan can sign a BAA, whether Growth admins control model training, HIPAA "Growth and Enterprise" versus "every plan", and whether a personal BAA can be signed in the app.
- Wispr's page changes were detected within a day, twice: 9 statements retired on 6 November and 15 on 7 November, and 4 earlier issues (SOC 2 "expected", Notetaker under a BAA, two HIPAA "any plan" items) credited as fixed.

**What it produces.**
- Approval pack: 38 questions seeded from the CSA CAIQ v4.1 domains plus the governance questions no standard form asks. Current answers: 7 ready, 18 partial, 10 confirm-with-Wispr, 3 escalations.
- Consent memo: a starting point for counsel on recording consent, written as questions, never as legal advice.
- IT briefs for companies with public signs of Flow use: never state or guess a user count; open with exactly what the public source shows.
- Business case: per-user maths with a break-even (about 12 to 33 minutes saved per user per month, depending on plan and price) and a fair note on when built-in dictation is enough.

**Why it can be trusted.**
- Code checks every quote against the page and every citation against the library.
- One model drafts; a different model judges each sentence; anything unsupported blocks the output.
- Measured: 29 of 30 extracted facts correct against a hand-labelled set; 4 of 4 planted conflict tests; 3 of 3 planted unanswerable questions correctly escalated.
- Every output is reviewed by a person before it is marked reviewed; nothing is ever sent by the engine.

**What I am asking.** One answer: when a company with Flow users stalls, who says no and why? If the answer is an approver, I would like to run a 30-day pilot on 20 accounts with a named owner on your side.
