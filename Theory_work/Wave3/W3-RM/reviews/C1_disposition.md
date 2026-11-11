# Council round 1 — disposition

## Seat A (Codex gpt-6-astra, high): `reviews/C1_council_astra.md`
Gates: G1 PASS, G2 PASS, G3 PASS, G4 PASS, G5 PASS, **G6 FAIL**. Score **8.8**. "No theorem-level defect found."
| # | sev. | finding | disposition |
|---|---|---|---|
| 1 | MAJOR, REQUIRED | L2 runs were labelled as violating/satisfying (L-gain) although the experiment sets a POPULATION proxy strength, with sigma^2 normalisation and a cellwise A; the sample tau-normalised all-U condition was never measured | fixed: L2 relabelled everywhere as an exploratory experiment on nominal population leak strength (SHARPNESS section 6 table + a note on nominal classification for V1/L1/L2; section 3.1; `numerics/build_summary.py` text and regenerated `numerics/SUMMARY_SHARPNESS.md`; REPORT). No count changed |
| 2 | MINOR | input map omits non-posterior uses of T1-F (energy, p <= n^A, BM-inf) | arrows added in STATEMENT input map and ASSUMPTION_MAP |
| 3 | NIT | L2 seed-count note inconsistent | rule stated once (20; 10 for eta = 2, p = 200, n >= 1600; two cells not run) |

## Seat B (Claude Opus 5.5, high, claudeAgent): `reviews/C1_council_opus.md`
Gates: G1–G6 all PASS. Score **8.9**. No REQUIRED finding. Deductions: 0.5 for the remaining lattice condition (flagged
in the statement), 0.2 for the strength of Form R's leakage condition, 0.4 for documentation items.
| # | sev. | finding | disposition |
|---|---|---|---|
| 1 | MINOR | DLV's pathwise Claim / Corollary D' cited without its status | statuses quoted verbatim in STATEMENT section 5 and L0_core [C1-B1] |
| 2 | MINOR | SHARPNESS read as if the shipped LS0 succeeds on the FAC-PK class | reworded: PATH is the uncapped path; with the shipped cap LS0 does not reach S0 there [C1-B2] |
| 3 | MINOR | input map: (T1-F) components and (L-feas) -> \|Q\| <= K edges missing | added [C1-A2], [C1-B3] |
| 4 | NIT | under (N-chi) the old cap already suffices; define ell_n | remark added to (C1); ell_n defined in section 1 [C1-B4] |
| 5 | NIT | SAND-R' status line names only the same-provider check | R07 and R08 recorded [C1-B5] |
| 6 | NIT | "fails in general" rests on a heuristic; "just outside" loose; no p > n cell | reworded in STATEMENT section 6, ASSUMPTION_MAP, L1b_rss; SHARPNESS reading sentence [C1-B6] |
| 7 | NIT | sigma^2 fixed in Setting R; eta unused by Form R | added [C1-B7] |
| 8 | NIT | FAC-PK status and its proposed cap change not quoted | status quoted; the proposed cap (ell_n + 2\|S~0\|, HQ decides) recorded in SHARPNESS section 3.2 [C1-B8] |
Seat B also reports a file-rule breach on its side (it ran citecheck.py, which rewrote reviews/CITECHECK.txt with
identical counts); the lead re-ran the script after the fixes, so the file on disk is the lead's.

## Round 1 outcome
Scores 8.8 (seat A) and 8.9 (seat B); seat A's gate G6 FAILED on the sharpness record (L2 labelling) -> round 1 NOT
passed (pass rule: both >= 8.0 with all six gates in the same round). No theorem-level defect in either reply. All
findings of both seats fixed (STATEMENT v1.2.1: wording and record only). Round 2 launched with two fresh seats.
