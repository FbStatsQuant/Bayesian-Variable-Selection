# gpt-6.2-sol vs gpt-6.1-sol: quality log for Codex fidelity reads (owner request via HQ, 2026-11-17)

One line per gpt-6.2-sol fidelity read. Each read is judged against the 6.1 baseline below on four axes:
- real findings (confirmed on our check);
- false positives (findings we rejected);
- brief fidelity (stayed in scope, followed the brief's format and paths);
- speed.

Each axis gets BETTER, SAME or WORSE, with one reason.

## Baseline: gpt-6.1-sol reads in this department (all at high effort)
| Read | Findings (C/S/F/E) | Confirmed | Rejected | Brief fidelity | Note |
|---|---|---|---|---|---|
| D2 v1 | 2/1/4/1 = 8 | 8 | 0 | full | |
| D1 v1 | 1/4/1/1 = 7 | 7 | 0 | full | |
| A2 v1 | 0/2/1/1 = 4 | 4 | 0 | full | one finding was a slip inherited from TRACK_B |
| A2 v2 | 0/2/0/1 = 3 | 3 | 0 | full | |
| A3 (D2 v2) | 2/5/5/0 = 12 | 12 | 0 | full | the two C findings were dropped "> 0" conditions |
| A4 (scoped) | 0/0/0/1 = 1 | 1 | 0 | full (scoped excerpts) | |
| A5 (scoped) | 0/1/2/0 = 3 | 3 | 0 | full (scoped excerpts) | |
Baseline: 38 findings, all confirmed, 0 false positives, every read stayed within its brief.
Wall-clock time was not logged per read, so speed is judged against the typical 6.1 turnaround for a comparable scope.

## gpt-6.2-sol reads
| Date | Read | Findings (C/S/F/E) | Real findings | False positives | Brief fidelity | Speed | Reason |
|---|---|---|---|---|---|---|---|
| 2026-11-17 | A5 final (manuscript, diff vs A5b) | 2/9/6/2 = 19 | BETTER: 18 confirmed, including two C catches 6.1 never reached (Thm 2's raw-label conventions; an AR(1) visibility counterexample) | WORSE: 1 rejected (#01 flags the display label (SG) against the brief's key name; not a defect), vs 0 in 6.1's 38 | SAME: stayed in the diff scope, used the brief's format and paths | BETTER: ~6 min for a whole-manuscript diff | depth up, precision slightly down; 6 of the 18 fixes needed a second pass, because the findings cited several locations each |
| 2026-11-23 | A6 owner-review edition (scoped: statements, statuses, SL sentences, parameters vs code/F2) | 11/17/27/1 = 56 | BETTER: 56 confirmed, incl. C catches 6.1 never made at this depth (a dropped part of Result 6(a), the F2 calibration misdescribed, SL Thm 1 has no Gram floor); registry and code claims re-derived and right | SAME: 0 rejected (~10 are low-value summary-completeness S items, still valid against the brief's "no more, no less") | SAME: stayed in the four scopes, used the brief's format; edited only its report | BETTER: ~7 min for 56 findings | very thorough and exact; finding volume is high for a scoped read, so triage cost rose |

Tally after 2 reads (BETTER / SAME / WORSE): real findings 2/0/0; false positives 0/1/1; brief fidelity 0/2/0; speed 2/0/0.
