# Things an approver would notice on Wispr Flow's public pages
Prepared 2026-11-07 from Wispr's public pages. Snapshot reference bd692c9cd4d8. Private; not shared with anyone else.

I read Wispr's public pages the way an IT, security, legal or finance approver does before a company-wide purchase, and kept a register of places where two pages could leave that reader unsure. Each item quotes both pages word for word, so you can check it in a minute. Some may already be known or intended; I may be wrong about any of them.

If you read only three: 1. Growth model training: admins control it vs locked off org-wide; 2. HIPAA plan availability: pricing page section headed On every plan says HIPAA-ready with a signed BAA; business page and HIPAA docs say Growth and Enterprise only, and docs say Free and Pro are not HIPAA-ready; 3. Which plan can sign the org BAA: BAA-revoke page says an active Enterprise subscription; HIPAA docs say Growth and Enterprise.

**16 open items**, most important first. **4 earlier items were fixed by page changes on or before 2026-11-06** (listed at the end).

## 1. Growth model training: admins control it vs locked off org-wide
*Two pages say different things. Severity for an approver: high. Ref M010.*

- The growth plan lets admins control model training for the whole team. Page wording: "Admin control over model training for your whole team" (https://wisprflow.ai/business, checked 2026-11-07)
- On Growth and Enterprise, the model-improvement setting is locked off organization-wide. Page wording: "is locked off organization-wide" (https://docs.wisprflow.ai/articles/4218718535-hipaa-compliance-healthcare-use, checked 2026-11-07)

## 2. HIPAA plan availability: pricing page section headed On every plan says HIPAA-ready with a signed BAA; business page and HIPAA docs say Growth and Enterprise only, and docs say Free and Pro are not HIPAA-ready
*Two pages say different things. Severity for an approver: high. Ref M067.*

- HIPAA compliance is available on the Growth and Enterprise plans with a signed Business Associate Agreement. Page wording: "Available on Growth and Enterprise with a signed Business Associate Agreement." (https://wisprflow.ai/business, checked 2026-11-07)
- Dictation and Notetaker are HIPAA-ready with a signed BAA on every plan. Page wording: "HIPAA-ready dictation and Notetaker with a signed BAA." (https://wisprflow.ai/pricing, checked 2026-11-07)

## 3. Which plan can sign the org BAA: BAA-revoke page says an active Enterprise subscription; HIPAA docs say Growth and Enterprise
*Two pages say different things. Severity for an approver: high. Ref M068.*

- Signing an org BAA requires an active enterprise subscription. Page wording: "Signing requires an active enterprise subscription" (https://docs.wisprflow.ai/articles/9642648659-how-to-revoke-a-hipaa-baa-agreement, checked 2026-11-07)
- HIPAA BAA signing is available on the Growth and Enterprise plans. Page wording: "HIPAA BAA signing is available on Growth and Enterprise" (https://docs.wisprflow.ai/articles/4218718535-hipaa-compliance-healthcare-use, checked 2026-11-07)

## 4. Personal BAA: BAA-revoke page says it can be signed on iOS; HIPAA docs say personal BAAs cannot be signed from the app
*Two pages say different things. Severity for an approver: high. Ref M072.*

- A personal BAA can be signed on iOS. Page wording: "A personal BAA can be signed on iOS" (https://docs.wisprflow.ai/articles/9642648659-how-to-revoke-a-hipaa-baa-agreement, checked 2026-11-07)
- Personal BAAs cannot be signed from the app. Page wording: "personal BAAs cannot be signed from the app" (https://docs.wisprflow.ai/articles/4218718535-hipaa-compliance-healthcare-use, checked 2026-11-07)

## 5. ISO 27001: compliance note says pending issue; docs say certificate held
*An older statement has not caught up. Severity for an approver: high. Ref M004.*

- Wispr holds an ISO/IEC 27001:2022 certificate. Page wording: "ISO/IEC 27001:2022 certificate" (https://docs.wisprflow.ai/articles/2941320990-vendor-security-assessments-and-questionnaires, checked 2026-11-07)
- The ISO 27001 certificate is pending issue. Page wording: "the certificate is pending issue" (https://wisprflow.ai/post/a-note-on-our-compliance-program, checked 2026-11-07)

## 6. Pricing says Flow is SOC 2 and ISO certified; Notetaker was outside audit scope
*A broad statement leaves out an exception. Severity for an approver: high. Ref M001.*

- Meeting Notetaker was not assessed in the SOC 2 Type I, SOC 2 Type II, or ISO 27001 certification audits. Page wording: "Meeting Notetaker launched after those audit periods and was not assessed" (https://docs.wisprflow.ai/articles/3467817258-security-and-compliance-faq, checked 2026-11-07)
- Flow is SOC 2 Type II and ISO 27001 certified. Page wording: "SOC 2 Type II and ISO 27001 certified." (https://wisprflow.ai/pricing, checked 2026-11-07)

## 7. Enterprise model improvement off, but usage metadata (app, URL) still uploaded
*A broad statement leaves out an exception. Severity for an approver: high. Ref M032.*

- For Enterprise, model improvement is off and administrators cannot re-enable it. Page wording: "it is off for Enterprise and administrators cannot re-enable it" (https://docs.wisprflow.ai/articles/3467817258-security-and-compliance-faq, checked 2026-11-07)
- With model improvement off, Flow still uploads dictation details such as word count, duration, app, URL and timestamp. Page wording: "Flow still uploads dictation details such as word count, duration" (https://docs.wisprflow.ai/articles/9609615338-private-cloud-sync-and-data-sharing-preferences-in-wispr-flow, checked 2026-11-07)

## 8. Cloud storage off covers dictation only; Notetaker content has no opt-out
*A broad statement leaves out an exception. Severity for an approver: high. Ref M033.*

- Dictation transcripts and audio are stored on Wispr servers only if dictation cloud storage is on. Page wording: "stored on Wispr servers only if Dictation cloud storage is on" (https://wisprflow.ai/post/a-note-on-our-compliance-program, checked 2026-11-07)
- Notetaker transcripts and summaries have no setting to opt out of cloud storage. Page wording: "with no setting to opt out" (https://docs.wisprflow.ai/articles/9609615338-private-cloud-sync-and-data-sharing-preferences-in-wispr-flow, checked 2026-11-07)

## 9. Ask Wispr: does sign-out reset cloud storage to on for a BAA account?
*A broad statement leaves out an exception. Severity for an approver: high. Ref M053.*

- Signing a personal BAA turns Dictation cloud storage off for the account. Page wording: "and Dictation cloud storage off for your account" (https://docs.wisprflow.ai/articles/9642648659-how-to-revoke-a-hipaa-baa-agreement, checked 2026-11-07)
- Signing out resets the cloud-storage preference to on. Page wording: "Signing out resets the cloud-storage preference to on" (https://docs.wisprflow.ai/articles/9609615338-private-cloud-sync-and-data-sharing-preferences-in-wispr-flow, checked 2026-11-07)

## 10. Android: HIPAA on Growth and Enterprise with a BAA, but Android has no BAA signing flow
*A broad statement leaves out an exception. Severity for an approver: high. Ref M057.*

- Android has no BAA signing or revocation flow. Page wording: "Android has no BAA signing or revocation flow" (https://docs.wisprflow.ai/articles/4218718535-hipaa-compliance-healthcare-use, checked 2026-11-07)
- HIPAA compliance is available on the Growth and Enterprise plans with a signed Business Associate Agreement. Page wording: "Available on Growth and Enterprise with a signed Business Associate Agreement." (https://wisprflow.ai/business, checked 2026-11-07)

## 11. Signed BAA copy: Enterprise HIPAA rows offer no download of the signed BAA; ask how an organization gets its signed copy
*A broad statement leaves out an exception. Severity for an approver: high. Ref M076.*

- Neither enterprise HIPAA row offers a download of the signed BAA. Page wording: "Neither enterprise row offers Download signed BAA" (https://docs.wisprflow.ai/articles/9642648659-how-to-revoke-a-hipaa-baa-agreement, checked 2026-11-07)
- HIPAA BAA signing is available on the Growth and Enterprise plans. Page wording: "HIPAA BAA signing is available on Growth and Enterprise" (https://docs.wisprflow.ai/articles/4218718535-hipaa-compliance-healthcare-use, checked 2026-11-07)

## 12. Vulnerability reporting: network docs say email security@wispr.ai; vendor-assessment docs say the programme does not accept emailed reports
*Two pages say different things. Severity for an approver: medium. Ref M074.*

- Wispr asks that vulnerabilities be reported to security@wispr.ai. Page wording: "Report vulnerabilities to security@wispr.ai" (https://docs.wisprflow.ai/articles/2021284475-configure-your-network-for-wispr-flow, checked 2026-11-07)
- The Vulnerability Disclosure and Bug Bounty Program does not accept vulnerability reports emailed to a security@ inbox. Page wording: "does not accept submissions emailed to a security@ inbox" (https://docs.wisprflow.ai/articles/2941320990-vendor-security-assessments-and-questionnaires, checked 2026-11-07)

## 13. SIEM: compliance note says API and SIEM connectors are in progress; audit-log docs describe SIEM streaming on Enterprise
*An older statement has not caught up. Severity for an approver: medium. Ref M073.*

- API and SIEM connectors for audit logs are in progress, not yet available. Page wording: "API and SIEM connectors are in progress" (https://wisprflow.ai/post/a-note-on-our-compliance-program, checked 2026-11-07)
- Streaming audit events to a SIEM requires an Enterprise plan and streaming access. Page wording: "Requires an Enterprise plan and streaming access" (https://docs.wisprflow.ai/articles/1282257172-audit-logs-for-enterprise-admins-track-team-membership-and-join-request-activity, checked 2026-11-07)

## 14. Enterprise 'disable org-wide' covers Mac and Windows only, not iOS
*A broad statement leaves out an exception. Severity for an approver: medium. Ref M015.*

- On Enterprise, the Disable for all users option turns Context Awareness off for everyone on Mac and Windows and locks the setting. Page wording: "which turns it off for everyone on Mac and Windows and locks the setting" (https://docs.wisprflow.ai/articles/4678293671-feature-context-awareness, checked 2026-11-07)
- Admins can disable context awareness org-wide on Enterprise. Page wording: "Admins can disable it org-wide on Enterprise" (https://wisprflow.ai/post/a-note-on-our-compliance-program, checked 2026-11-07)

## 15. 'Admins control context awareness' but on Growth they cannot enforce it off
*A broad statement leaves out an exception. Severity for an approver: medium. Ref M038.*

- Admins control whether context awareness is available. Page wording: "whether context awareness is available" (https://wisprflow.ai/business, checked 2026-11-07)
- On Growth, each person controls their own Context Awareness setting and administrators cannot enforce it off. Page wording: "each person controls their own setting and administrators cannot enforce it off" (https://docs.wisprflow.ai/articles/4678293671-feature-context-awareness, checked 2026-11-07)

## 16. Pro price: plan table shows $15 per user per month, while the ROI calculator labels $12 the Pro monthly cost; ask which applies to monthly billing
*A broad statement leaves out an exception. Severity for an approver: medium. Ref M071.*

- The pricing page lists Pro at $15 per user per month in one view of the plan table. Page wording: "Pro For individuals and teams $15 /user/mo" (https://wisprflow.ai/pricing, checked 2026-11-07)
- The pricing page ROI calculator uses $12 as the Flow Pro monthly cost. Page wording: "Flow Pro monthly cost: $12" (https://wisprflow.ai/pricing, checked 2026-11-07)

## Already fixed
These were in the register and the wording changed on Wispr's pages, so they are closed:

- Notetaker under a BAA: works alongside (docs) vs disabled (pricing) (closed 2026-11-06, ref M002)
- SOC 2: blog posts still say report expected in September; docs say it exists (closed 2026-11-06, ref M003)
- 'HIPAA compliance on any plan' omits that the BAA covers dictation only (closed 2026-11-06, ref M012)
- Android: 'HIPAA on any plan' omits that Android has no BAA signing flow (closed 2026-11-06, ref M054)

## How this was made
Wispr's public pages are snapshotted, facts are extracted with the exact quote, and pairs that might disagree are judged by a second model. Every item above was then reviewed by hand; items that turned out to be compatible were dropped as false positives. The method and register are available if useful.
