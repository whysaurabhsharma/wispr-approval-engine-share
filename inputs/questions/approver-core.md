# Approver core questions

38 questions an IT, security, legal or finance approver asks before a company-wide Wispr Flow purchase.

Seeded from the domains of the CSA Cloud Controls Matrix and CAIQ v4.1 (released 27 January 2026; 17 domains), https://cloudsecurityalliance.org/artifacts/cloud-controls-matrix-v4-1. Domain codes in the `caiq` column. Questions marked `caiq: none` are the governance-of-existing-users questions no standard form asks.

`topics` uses the claim library's topic names. `drata_covers`: yes = a standard security questionnaire or trust center normally answers it; partly = it answers the general control but not the plan or default; no = outside standard questionnaires. The pack answers all of them and states which Drata covers.

| id | reviewer | question | topics | caiq | drata_covers |
|---|---|---|---|---|---|
| q01 | it | Can we require SAML single sign-on for everyone on our domain, and on which plan? | governance, security | IAM | partly |
| q02 | it | Can we provision and remove users automatically with SCIM? | governance, security | IAM | partly |
| q03 | it | How do we find employees who already use Flow on personal or free accounts? | governance | none | no |
| q04 | it | Can we move those users into a company-managed account and stop new personal sign-ups on our domain? | governance | none | no |
| q05 | it | Can we deploy and configure Flow through MDM? | governance, product | UEM | partly |
| q06 | it | Which network destinations must we allow, and does Flow work behind TLS inspection? | security, product | IVS | partly |
| q07 | it | Can we restrict access to Flow by IP range? | security, governance | IAM | partly |
| q08 | it | What is stored on the device, and can admins set how long local history is kept? | privacy, governance | UEM | no |
| q09 | it | Can an admin turn Notetaker off for the whole organisation? | governance | none | no |
| q10 | it | Can an admin turn context awareness off for everyone, and on which platforms? | governance, privacy | none | no |
| q11 | it | Which platforms are supported, and do admin controls apply on all of them (Mac, Windows, iOS, Android)? | product, governance | none | no |
| q12 | security | What is the current SOC 2 Type II and ISO 27001 status, and how do we get the reports? | compliance | A&A | yes |
| q13 | security | Which products are in the audit scope: dictation, Notetaker, or both? | compliance | A&A | partly |
| q14 | security | How is customer data encrypted in transit and at rest? | security | CEK | yes |
| q15 | security | Is there end-to-end encryption, or support for customer-managed keys? | security | CEK | yes |
| q16 | security | Where is customer data processed and stored, and is regional data residency available? | privacy | DSP | yes |
| q17 | security | Who are the subprocessors, including AI model providers, and how are we told about changes? | privacy, legal | STA | yes |
| q18 | security | Do third-party AI providers keep or train on our data? | privacy | STA | partly |
| q19 | security | Is our content used to train Wispr's models by default, and can we enforce training off for everyone? | privacy, governance | DSP | partly |
| q20 | security | Can we enforce zero data retention for all users? | privacy, governance | DSP | partly |
| q21 | security | What data is still sent or collected when data sharing and cloud storage are off? | privacy | DSP | no |
| q22 | security | Are admin and membership changes logged, and can we export logs or stream them to a SIEM? | security, governance | LOG | yes |
| q23 | security | Which Wispr staff can access customer data, and is that access logged? | security | IAM | yes |
| q24 | security | How are vulnerabilities reported, and how often is the product penetration tested? | security | TVM | yes |
| q25 | security | How are security incidents handled, and how are customers notified? | security | SEF | yes |
| q26 | security | Is there an uptime or support SLA, and what happens to dictation during an outage? | product | BCR | yes |
| q27 | legal | Do you provide a DPA, with EU Standard Contractual Clauses and a UK Addendum? | legal | STA | yes |
| q28 | legal | Do you sign a BAA, on which plans, and which products does it cover? | legal, compliance | none | yes |
| q29 | legal | Can Notetaker be used on an account under a BAA? | legal, compliance | none | no |
| q30 | legal | What consent controls does Notetaker offer for meeting participants? | consent | none | no |
| q31 | legal | Does Notetaker join meetings as a bot or record from the device, and do participants see a notice? | consent, product | none | no |
| q32 | legal | How long are Notetaker audio, transcripts and summaries kept, and can we opt out of cloud storage? | privacy, consent | DSP | no |
| q33 | legal | How do we export or delete a user's data, and what is kept after deletion? | privacy, legal | DSP | yes |
| q34 | legal | Who controls the data of an employee on a company account? | legal, governance | DSP | no |
| q35 | finance | What does each plan cost per user, monthly and annually? | pricing | none | no |
| q36 | finance | Which plan do we need for SSO, SCIM, audit logs and enforced retention? | pricing, governance | none | no |
| q37 | finance | Can we pay by invoice or purchase order, and are custom contract terms available? | pricing | none | no |
| q38 | finance | Is there a minimum seat count or a long-term commitment? | pricing | none | no |
