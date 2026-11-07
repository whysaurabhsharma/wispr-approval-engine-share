# Problem evidence: does approval stall Wispr Flow deals?

Checked: 2026-11-06. Every item links to a public source. Items marked *competitor* or *unverified* are labelled as such; read them as signals, not proof.

## The claim

When employees at a company already use Wispr Flow, the step that slows or stops a company-wide purchase is approval by IT, security, legal or finance, not demand.

## Evidence for

| # | Evidence | Source | Type |
|---|---|---|---|
| 1 | Wispr's Founding AE owns the whole cycle including procurement, security and legal, and must have run InfoSec reviews before. The company is hiring for the approval step. | [Built In job post](https://builtin.com/job/founding-account-executive-ae/7791402), [Jobright listing](https://jobright.ai/jobs/info/6925288df0beb0723261b47f) | Primary (job post) |
| 2 | Wispr is hiring a customer-facing security assurance and GRC lead to own assurance reviews and enterprise customer requirements, plus an engineering lead to move from SMB to enterprise. | [Hotfix company page](https://hotfix.jobs/companies/wispr-flow) | Primary (job post, aggregator) |
| 3 | The Senior Technical Account Manager role asks for a record of taking pilots through procurement. | [Built In job post](https://builtin.com/job/senior-technical-account-manager/7928951) | Primary (job post) |
| 4 | After its compliance vendor (Delve) was accused of templated audits in March 2026, Wispr publicly moved to a new auditor (A-LIGN) and platform (Drata). Assurance had to be rebuilt in public. | [A note on our compliance program](https://wisprflow.ai/post/a-note-on-our-compliance-program), [Our path to a new audit](https://wisprflow.ai/post/new-independent-audit) | Primary (Wispr) |
| 5 | Our mismatch register found 14 open inconsistencies across Wispr's own pages that an approver would notice: SOC 2 report still "expected in September" on blog posts while docs say it exists; Notetaker "works alongside" a BAA in docs but is "disabled" under one on pricing; Growth vs Enterprise BAA availability. | `claims/mismatches.yaml` (M001-M054), built from Wispr pages snapshotted 2026-11-05 | Our analysis of primary sources |
| 6 | Wispr's docs state limits that trigger security review questions: no EU data residency, no end-to-end encryption, no customer-managed keys, and no setting to opt Notetaker transcripts out of cloud storage. | [Security and compliance FAQ](https://docs.wisprflow.ai/articles/3467817258-security-and-compliance-faq), [Data sharing preferences](https://docs.wisprflow.ai/articles/9609615338-private-cloud-sync-and-data-sharing-preferences-in-wispr-flow) | Primary (Wispr) |
| 7 | A rival publishes a long page on whether Wispr Flow is safe and walks through what a security reviewer would find. Rivals compete on trust, which only matters if approvers decide. | [Voibe: Is Wispr Flow Safe?](https://www.getvoibe.com/resources/is-wispr-flow-safe.md) | *Competitor* |
| 8 | A second rival's comparison table describes Wispr as having consumer-grade security without enterprise certifications, which Wispr's own docs contradict. Approvers may meet this framing first. | [Willow blog](https://willowvoice.com/blog/executives-write-client-emails-faster-willow) | *Competitor* |
| 9 | A Reddit post (August 2026) describes a quarterly audit after which a security team removed Wispr Flow from six machines. | [r/growthhackers](https://www.reddit.com/r/growthhackers/comments/1vghyeo/security_team_pulled_wispr_flow_from_6_machines/) | *Unverified*, single anonymous account |
| 10 | Netskope reports that nine in ten organisations block at least one generative AI app, and the average blocks ten. | Cited by [Voibe](https://www.getvoibe.com/resources/is-wispr-flow-safe.md) from Netskope Cloud and Threat Report 2026 | Secondary; confirm against the Netskope report before quoting |
| 11 | A Sapio survey for BlackFog (2,000 staff at firms over 500 people, Nov 2025) found 49% use AI tools their employer has not approved, and 51% have connected AI tools to work systems without IT approval. Shadow use is common; formal approval is the bottleneck. | [BlackFog research note](https://www.blackfog.com/?p=67688), [CIO coverage](https://www.cio.com/article/4124760/roughly-half-of-employees-are-using-unsanctioned-ai-tools-and-enterprise-leaders-are-major-culprits.html) | Vendor-sponsored survey |
| 12 | Class actions against AI note-takers (Granola, Otter) centre on recording consent; a court let the core wiretap claims against Otter proceed. Legal teams now review any capture tool. | [Barnes & Thornburg](https://btlaw.com/en/insights/alerts/2026/what-the-granola-class-action-means-for-companies-building-and-deploying-conversation-capture-tools), [UC Today](https://uctoday.com/productivity-automation/otter-ai-fails-to-dismiss-core-privacy-claims-in-u-s-court/) | Legal context |

## Evidence against

| # | Evidence | Source | What it suggests |
|---|---|---|---|
| A | Users rate the app highly: 4.8 on the iOS App Store from over 8,500 reviews (Trustpilot is lower at 2.7). | Cited by [Voibe](https://www.getvoibe.com/resources/is-wispr-flow-safe.md) | Demand is strong; the stall, if any, is after adoption, but this is not proof that approval is where it stalls. |
| B | Wispr already ships most of what approvers ask for: SAML SSO, SCIM, audit logs, IP allowlist, enforced zero retention, self-serve DPA, BAA, vendor assessments for Enterprise. | Wispr docs and pricing (library ids `saml_sso_growth_enterprise`, `scim_provisioning_supported`, `docs_network_ip_allowlist_enterprise_only`, `dpa_available_every_plan`) | Approvers may find their answers without help. |
| C | A-LIGN issued a clean SOC 2 Type I in April 2026, and current docs describe a SOC 2 Type II report and ISO 27001 certificate. | [Security and compliance FAQ](https://docs.wisprflow.ai/articles/3467817258-security-and-compliance-faq), [Vendor assessments](https://docs.wisprflow.ai/articles/2941320990-vendor-security-assessments-and-questionnaires) | The biggest blocker of 2026 may already be fixed. |
| D | Hiring AEs and TAMs can mean enterprise deals are closing well, not stalling. | Items 1 to 3 | The same job posts support both readings. |
| E | Items 7 to 10 come from competitors, an anonymous post, or a secondary citation; item 11 is sponsored by a vendor that sells shadow-AI controls. | As listed | Discount these when weighing the case. |
| F | No public source gives Wispr's win rate, sales cycle length, or where deals are lost. | n/a | The core claim is still a hypothesis. |

## Reading it honestly

The public record shows that Wispr is building for the approval step (items 1 to 4), that its own pages give approvers reasons to pause (items 5 and 6), and that the market around it treats trust as the battleground (items 7 to 12). It does not show that approval is where Wispr's deals actually stall. Only Wispr's sales data can show that.

## The one question that settles it

"When a company with Flow users stalls, who says no and why?"

If the answer names IT, security, legal or finance, the engine is aimed correctly. If it names budget, a competitor, or lack of champion, re-aim Phase 3 before building more.
