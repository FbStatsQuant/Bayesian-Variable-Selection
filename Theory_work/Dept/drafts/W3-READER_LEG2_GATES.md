# W3-READER leg 2 — strength gates for the five-pillar candidate rows (Theory Department, draft 2026-11-15)

Starts after W3-READER CP1 is answered. Same lead and worktree. Outside the department's lead cap.

## Why
HQ cleared all 44 tool-set headline flags (consultant H5, 11-15). Acceptance no longer waits on the strength gates,
so the gates must still run: they are the control against sub-par theorems. A row is cited as a pillar (card, chapter,
paper) only when it is `headline=yes` with its gates run. Deadline: **Thu 11-19 18:00 CT** for the five-pillar rows,
so the recorder can enter the gates before the Friday freeze.

## Scope
Every theorem row of CLAIMS_CARD pillars 1–3, master claim(s) per row:
- 1.1 W3-POST:Thm-1 / SOP:TH09
- 1.2 W2-APP:POST
- 1.3 W3-PSHARP:A, B
- 3.1 W3-RM2:RM2-R (+ RM-0, F-UNI)
- 3.2 RM2-F
- 3.3 W3-START2:START-R, W3-START:FLOOR
- 3.4 W3-MISR:Cor-G(b)
- 3.5 W1-N1:Thm-N1
- 3.6 W3-SAMP:C, TR, LT♯, D
- 3.7 W3-SCR:A1

W3-DIST runs its own gates in its chain (TARGET.md). The rider tickets' new rows get theirs at their CP1 (TARGET.md).

## Per row (LIFECYCLE §4.2)
- **lit:** a table of hypotheses and conclusion vs Song–Liang (2015) and the closest BVS consistency result (stronger /
  weaker / incomparable; flag literature dominance). Reuse each ticket's TARGET / ASSUMPTION_MAP / SHARPNESS parity rows.
- **necessity:** per hypothesis, NECESSARY (counterexample) / NECESSARY-FOR-ROUTE / ARTEFACT (keeps `improvable`),
  from the ticket's ASSUMPTION_MAP, SHARPNESS and `sharpness.tsv`. Cite the files; no new proofs.
- **better:** rows covered by the blind API sharpness audits (`API_AUDIT/sharp1`, `sharp1b`, `sharp2`) cite the verdict
  file and the triage disposition (A/B/C/D → adopted / ticket / declined / remark). **Uncovered rows go to an API Fable
  sharpness batch** (HQ, 11-15: independent stronger reviewer, no Codex, HQ's credits, ~$15–25). Prepare the request list
  in the format of `Theory_work/Wave3/API_AUDIT/audit_batch.py` modes `sharp`/`sharp2`: a `SHARP3_TICKETS` spec or an
  explicit list of row ids, each with statement file:line. Save it as `SHARP3_REQUEST.md` and send it to the manager by
  **Wed 11-18 12:00 CT**. HQ builds and submits the batch and returns the results; you triage them (as `sharp2/TRIAGE.md`)
  and record the dispositions. No Opus better-reviews.
- Output: `GATES.md` (one section per row: lit / necessity / better, each PASS or the open item) and a
  `gates_staged.tsv` for the recorder (id | lit | necessity | better | better-proposals | file refs).
- Rows where a gate cannot pass go to the manager at once: that is a sub-par signal touching a headline candidate.

## Budget
~6–8 Opus hours; up to 2 helpers (Claude Third, Opus/Sonnet 5.5, effort high); fresh Opus reviewers as above.
