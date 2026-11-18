# BRIEF — F9: fidelity read of the proposed thm9 / card row 2.1 text + line check of bridge B9.5 (Theory Department, 2026-11-16)
Sol (codex gpt-6.1-sol), effort high, ONE call, fresh, blind first read (you have not seen this text before). Two scopes in one review
(department deviation B5): (1) fidelity read, (2) line check of one new bridge.

Do not write any file outside the worktree and set no TMPDIR. Scratch only in /home/fb31/BVS-wt/THEORY-DEPT/.rc_tmp/, deleted at the end.
Write exactly one file: `/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Dept/research/DIST_thm9_fidelity/F9_sol.md`. Change no git state; edit nothing else.

## Inputs (read only; sha256 in inputs.sha next to this brief)
- Proposed reader text + bridges: `/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/DELTA_row21_thm9_DIST.md`
  (proposed READER_VERSIONS ROW thm9 = "Theorem 9", proposed CLAIMS_CARD rows 2.1/2.2, bridge table B9.0–B9.6).
- Masters (council R2 PASSED, MANIFEST c5cd9cdd…): `/home/fb31/Bayesian-Variable-Selection/Theory_work/Wave3/W3-DIST/STATEMENT.md`
  (§0 setting, §1 theorems DIST-1/2/3, Theorem A/B, Corollary C, **§1R the ticket's own reader versions**), `REPORT.md` (registry block: statuses
  and conditions), `CHECKPOINT_3.md`, `TARGET.md` §2 (Song–Liang comparison).
- Known context: the DIST-2 "best rate ≍ (1+s₀^r)…" gloss is LOOSE (no sparsity-dependence of a rate may be claimed in reader text).

## (1) Fidelity — for each display, assumption and sentence of the proposed Theorem 9, the card rows and the comparison paragraph:
- Is every numbered assumption implied by (or equal to) the masters' hypotheses, with nothing dropped that the masters need?
- Is every conclusion/display implied by a master, with the same rate, the same probability/expectation form and the same scope
  (joint law of (x, y), Hellinger, posterior contraction, which p)? Flag any STRONGER-than-proved wording.
- Are the stated conditions/statuses honest (conditional on SOP:TH09; W3-POST:Thm-1 where used; delivery premises where used)?
- Interpretive sentences ("hence…", "this means…", readings): list each and judge it (RIDER_RULES D71).
- No internal ids in reader text; asymptotics never framed as a limitation.
Output line: `FIDELITY: FAITHFUL | NOT-FAITHFUL`.

## (2) Bridge B9.5 (NEW): "exponent in (iii): cM log n = c nε_n²/log(p_raw ∨ n) at ε_n² := M log n log(p_raw ∨ n)/n". Verify the arithmetic and
that display (iii) of the proposed Theorem 9 is exactly the master's statement after this substitution (constants, the role of M, ranges).
Output line: `B9.5: VERIFIED | GAP | ERROR`.

Findings tagged C/S/F/E with file:line, ≤ 40 lines total.
