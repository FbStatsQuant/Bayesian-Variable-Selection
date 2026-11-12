# INFRA R07 — one anchored "accepted with remarks" body-cell form (HQ, 2026-11-12)

Implementer: Claude Opus 5.5, effort high, provider claude-personal. Worktree `C:/Users/felip/BVS-wt/INFRA-R07` (branch
`infra/R07-accept-form`, from main 5144365). **Change no git state** (HQ commits).

## Why
R06's strict per-claim decision reader (LIFECYCLE §"Seat tables by addendum") rejects W3-START's Opus R2 body cells:
- F1: `accepted with non-blocking remarks (Issue 5: the η = 0 sentence is read under the premise of F1(ii))`
- BR: `accepted with non-blocking remarks (Issue 3)`
- OVL: `accepted with non-blocking remarks (Issue 2: wording of the P-OVL row in STATEMENT.md §4, not of OVL itself)`
- EX: `accepted (F-1, F-2, F-3, G-1, G-2 verified; UNI-0 and AR(1) correctly not claimed)`
(file `C:/Users/felip/BVS-wt/W3-START/Theory_work/Wave3/W3-START/reviews/R2_council_opus.md` l.58–70), so they
"contradict" the same-seat addendum ACCEPT and W3-START is refused. Decision (HQ + consultant): extend the grammar by
ONE anchored form; no keyword heuristics.

## Do
1. A body decision cell reads as ACCEPT iff, after the existing trimming, it matches exactly:
   `accepted` [ ` with non-blocking remarks` ] [ ` (` <text without unbalanced parentheses> `)` ] and nothing else
   (case as in the existing whitelist for `accepted`; one optional parenthetical, at the end, balanced; nothing after it).
   Everything else that is unreadable still contradicts an addendum decision, exactly as now.
2. Regression tests: the four real cells above → ACCEPT; negatives → not accepted / contradiction: `accepted except part
   (ii)`, `accepted conditional on X`, `accepted, with blocking remarks`, `not accepted (…)`, `accepted (…) but …`,
   `accepted (…) (…)`, `accepted (unbalanced`, trailing text after the parenthetical, the form inside a split/continued row.
3. Re-run the decision reading on all four ticket branches (theory/W3-START, W3-PSHARP, W3-MISR, W3-RM2 — read them from
   `git show <branch>:<path>`): W3-START's 21 claims now accepted by both seats; PSHARP, MISR, RM2 verdicts unchanged.
   Then staged acceptance of W3-START in a disposable clone of main + the branch: 0 acceptance ERROR.
4. Full suite + `check.py --quiet` 0 ERROR. Update LIFECYCLE §"Seat tables by addendum" with the one form.
5. One narrow Sol check (codex `gpt-6.1-sol` high, mode wait), phrased as a correctness test of the cell grammar (no
   attack wording); output `Theory_work/INFRA/R07FIX/R07_sol.md`. Fix findings once.
6. `Theory_work/INFRA/R07FIX/REPORT.md`; end with ≤ 8 lines. No other agents.
