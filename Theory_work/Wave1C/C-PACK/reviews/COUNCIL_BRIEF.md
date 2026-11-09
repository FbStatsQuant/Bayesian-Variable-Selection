# C-PACK council brief (both seats receive this file only, plus the repo)

You are one of two independent council reviewers (Codex gpt-6.1-sol xhigh; Claude Opus 5.5 high) for ticket C-PACK of
Theory Wave 1C (SMC-BVS paper). Score independently; do not coordinate. Try to break the results.
Repo: C:\Users\felip\Bayesian-Variable-Selection. Read-only except `Theory_work/Wave1C/C-PACK/reviews/` (write your reply
there only). No git state changes.

## Object scored (items 1–4)
`Theory_work/Wave1C/C-PACK/`: STATEMENT.md (locked v2 — the targets), METHOD_REQUIREMENTS.md, SONG_LIANG_MAP.md,
lemmas/I1_e4_replacement.md (item 1), lemmas/I2_LHiid_unconditional.md (item 2), patches/P_SEL_L6d.md and
patches/P_L8_certificate.md (item 3, patches to `Theory_work/Wave1/W1-GEN/lemmas/L6_instances.md` §(d) and
`L8_certificate.md`), lemmas/I4_SL_corollaries.md (item 4), patches/P_e4_consumers.md, patches/P_GEN_LHiid.md.
Context (not scored, per HQ's brief: "item 5 needs only its fidelity check"): item5_PXN_consolidated/ and its fidelity
review reviews/R36_item5_fidelity_sol.md.
You may read reviews/ (all earlier reviewer replies and dispositions), numerics/ and LOG.md, and must open the cited
sources (Theory_work/Wave1/*, Theory_work/State_of_Project/*, Theory_work/Old_Projects/New_BVS_Headquarters/*, frozen code
Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/core/, Song–Liang PDF
C:\Users\felip\.t3\userdata\attachments\647bfd65-83bc-403a-b3b0-0a8352044e7f-588fe83a-5cbe-4a20-8055-1cfbd7c9c936-pdf.pdf).
Rules of the wave: Theory_work/Wave1C/PROTOCOL.md and Theory_work/Wave1/PROTOCOL.md.

## Gates (each PASS/FAIL with reasons)
G1 correctness of every step; G2 hypotheses used = hypotheses stated; G3 no hidden assumptions; G4 cited lemmas have
adequate status, statuses quoted verbatim, nothing upgraded; G5 constants/rates tracked; G6 fidelity to the method as
coded (frozen v2.2.1 start_mode etc.) and as it will ship (LS0/e4 integration explicitly a premise).

## Output
Write `reviews/C1_council_<seat>.md` (seat = sol or opus): per-item assessment (items 1–4), gate verdicts G1–G6, a list of
blocking issues (if any) with exact fix text, non-blocking issues, and an uncapped 0–10 score. Pass = both seats ≥ 8.0 with
all gates PASS. End your reply with "SCORE: x.x; GATES: G1 … G6".
