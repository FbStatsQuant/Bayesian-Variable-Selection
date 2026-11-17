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

Tally (BETTER / SAME / WORSE, per axis): none yet.
