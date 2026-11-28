# FR1 — Sol fidelity read of PSMC-S0 Part 1 (brief, saved before launch)

Reviewer: Sol (gpt-6.1-sol), reasoning effort high, fresh agent, no earlier context. Read-only: write nothing in the
repository; return your report as your final message.

Repository worktree: `/home/fb31/BVS-wt/PSMC-S0` (all paths below are relative to it unless absolute).

## Files under review
- `Theory_work/Wave3/PSMC-S0/AUDIT_N.md`
- `Theory_work/Wave3/PSMC-S0/AUDIT_CAL.md`

## Context (facts, not conclusions)
The large-p engine changes the method in two places audited here:
- OD-1: fixed N = 2,500 particles per island for every p (v3.1: N₀ = max(2500, n, p)), 16 islands;
- OD-2(c): bounded calibration — no escalation to tier 1 except after a grid-construction failure; at most I_max
  rebuilds, then freeze the last grid with flag `grid_unconverged`; tier-1 fallback grid (C-DLV) kept.
- D-7 / OD-13: drop the final-run leader stores (`leaders_gamma0/1`, `Scripts/SMC_BVS/core/v3_run.R:210`) from final
  islands and from the output; keep leader stores in calibration.
Sources for these changes (read only): `/home/fb31/Bayesian-Variable-Selection/Docs/Experiments/P1M/ENGINEERING_SPEC.md`
§4.2–4.3, `OWNER_DECISIONS.md` OD-1, OD-2, OD-13. Registry: `Theory_work/INFRA/registry/claims.tsv` (rows with
state ACTIVE are the registered claims). Code: `Scripts/SMC_BVS/core/` (`v3_preprocess.R`, `v3_calib.R`, `v3_fit.R`,
`v3_run.R`, `cpp/v3_core.cpp`, `cpp/v3_ledger.h`). Theory sources: `Theory_work/State_of_Project/sections/*.tex`,
`Theory_work/State_of_Project/registry/*.tsv`, `Theory_work/Wave1*/`, `Theory_work/Wave2/`, `Theory_work/Wave3/`
(do not read `Theory_work/Wave3/W3-DIST/` beyond a grep).

## Questions (try to break the audits)
1. For every row of both audits: is each `file:line` citation right (does the cited line say what the row says)? Is
   the "holds?" verdict right? Give the row number and what is wrong.
2. Missing consumers: is there any registered (ACTIVE) claim, card item (SoP §4 cards, `theory_main.tsv`,
   `theory_supp.tsv`) or output flag that uses N_e ≥ p, N₀ = max(2500, n, p), N₀ ≥ n, H₀, "common N", the escalation
   rule, E1/E2/E3 as calibration triggers, the tier, `grid_unconverged`, rebuild convergence, or the final-run leader
   stores, and is not in the tables? Search the registry and the statement/lemma files yourself.
3. The confirmations (AUDIT_N §2, AUDIT_CAL §2): does each quoted result really hold for arbitrary N_e and any frozen
   calibration as stated, or does some proof step (not only the statement) use the production budgets or the
   coded escalation rule? Check at least W1-N1, W3-SAMP (D, LT♯, C, TR), W3-RM RM-0 and C-DLV L4.
4. AUDIT_N row 6 (W3-SAMP D production corollary) and row 7 (W2-APP ENUM (ii)): is the claimed weakening right,
   and is the arithmetic right (12,560p threshold; p ≤ 17)?
5. AUDIT_CAL §1 rows 1–3: does C-DLV Theorem D / Proposition F really go through under OD-2(c) with the fallback kept?
   Is there a calibration exit path under the bounded rule that the audit misses?
6. AUDIT_CAL §3 (leader stores): is the verdict "safe to drop the final-run leader stores, provided the calibration
   leader stores still feed V and the inherited set" right on the code? Does anything read the final ledger's lead0 /
   lead1 other than the output export?

## Output format
- A table `| audit | row/section | finding | tag | fix |` with tag C (citation/fact wrong), S (verdict overstated or
  understated), M (missing consumer), E (editorial).
- A list of missing consumers (if any) with file:line.
- One line: `FIDELITY-VERDICT: PASS | PASS-WITH-FIXES | FAIL`.
