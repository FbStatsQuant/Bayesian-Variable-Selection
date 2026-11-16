# PSMC-S0 — scoping leg for the parallel-method premise tickets T-N, T-CAL (preliminary) and T-PART (Theory Department, 2026-11-15, rev. 1 after Engineering's dates)

Lead: Claude Opus 5.5, effort high, Claude Third, on Owls. Scoping to CP1 only (Tier B rules; mostly a premise
audit). Worktree `/home/fb31/BVS-wt/PSMC-S0`, branch `theory/PSMC-S0`, folder `Theory_work/Wave3/PSMC-S0/`.
Read first: `RIDER_RULES.md` (this folder; §1 parents read-only, §4 agents, §6 stops apply), `PROTOCOL_v4.md`,
`PROGRAM.md`, `POLICIES.md` (repo root).

## Why now
The SMC - Engineering Department's p = 1M engine changes the method in law in five places (`Docs/Experiments/P1M/
ENGINEERING_SPEC.md` §4.2; `OWNER_DECISIONS.md` OD-12). Two of these need an answer before the owner decides them
(target 11-20) and before setup code is written (WP2 from 11-23):
- **OD-5 / T-PART:** complete linkage truncated at height 1 − τ_n on the sparse graph {|r| ≥ τ_n}, τ_n = r_n =
  √(2 log p / n); then the coded top-down cut for clusters larger than B; next-fit packing with clusters ordered by
  minimum index. Class Δ on π₀ only. Gate T11 checks it equals the exact dendrogram below 1 − τ_n.
- **OD-1 / T-N:** fixed N = 2,500 per island for every p (was N_e = max(2500, n, p)). Class Δ.
Read only (other department's folder): OD-1, OD-5, OD-12, SPEC §0, §3, §4. Engineering facts come from there or from
the code (`Scripts/SMC_BVS/core/`, pinned file:line); questions to the Engineering Department go through the manager.

## Order and dates (Engineering, `Docs/Experiments/P1M/REQUESTS.md` THEORY-1..3; soft / hard)
- **Part 1 → CHECKPOINT_1 by Thu 11-19 12:00 CT** (owner batch OD-1/OD-2, soft 11-20): `AUDIT_N.md` (T-N, below) and
  `AUDIT_CAL.md` (T-CAL preliminary): every delivered / registered result, card item or flag reading E2, the tier,
  escalation, `grid_unconverged` or grid convergence; and a confirmation (file:line) that results stated "for any frozen
  calibration 𝒞" (LT♯, TR, RM-0, N1, …) need nothing under OD-2(c) bounded calibration (I_max rebuilds, no escalation
  except grid-construction failure, C-DLV fallback kept). Re-check C-DLV's use of escalation.
- **Part 2 → CHECKPOINT_2 by Tue 11-24 18:00 CT** (soft 11-25): `AUDIT_PART.md` (T-PART, below), covering **every**
  consumer in THEORY-1's table (tables and π₀; the composite γ₀ and discrepancy d(S) that define the SMC bridge path;
  initial and independence draws; the γ₀ leader store → V → grid; start mode → LS0 centre and cap; table models in the
  stores; (V) via B − 1), plus the sub-choice ≥ vs > for the edge set (the neighbour graph uses >).
The manager answers CHECKPOINT_1 and tells you whether to continue to Part 2 in the same run.

## Deliverables
1. `AUDIT_PART.md` (Part 2): for every registered claim that consumes the block partition (the THEORY-1 consumer
   table; START, START2, RM2, (V), Lemma ASM, OVL, NEC, block-relative functionals, N1/LT♯/C/TR through γ₀ and d(S),
   SAMP D, RM-0/E4/GEN/GROW/MR1/MR2 through the start mode, SL2/DIST-C through table models), one row: `claim id@version | where the partition enters (file:line) | property used
   (e.g. block size ≤ B; clusters = exact complete-linkage cut; within-block |r| ≥ τ; between-block |r| < τ;
   deterministic given X) | holds for OD-5(c)? yes / no / needs a bridge | effort`. Note that several START/START2
   hypotheses are partition-free and dominate their block-relative versions ((B1)); say which theorems therefore hold
   for **any** partition with blocks ≤ B.
   Then: a candidate T-PART statement ("the theorems hold for the method's partition under OD-5(c)", or the bridge
   needed), a recommendation on τ_n and the packing order if theory prefers something else, and the numerics (if any)
   that would show the law change on π₀ matters.
2. `AUDIT_N.md` (Part 1): every result that uses N_e ≥ p, N₀ = max(2500, n, p) or "common N at N_e": TH01(e)(f)(i), TH06,
   TH08 (SoP anchors, `State_of_Project/`), settings rows, and a confirmation (file:line) that RM-0, LT♯, TR, D and
   the headline selection/PIP/DIST results are stated for arbitrary N (OD-1 says so; check it). Candidate T-N
   restatements for general (N, R′), each with effort.
2b. `AUDIT_CAL.md` (Part 1), as in "Order and dates".
3. `CHECKPOINT_1.md` (Part 1) and `CHECKPOINT_2.md` (Part 2): verdicts in plain words for HQ and the Engineering Department (≤ 1 page). Proposed
   follow-on tickets (tier, hours, what they consume). Anything that blocks OD-1/OD-5, in the first paragraph.
4. One Sol fidelity read per part (fresh; brief saved first): is each row's file:line and "holds?" verdict
   right, and is any consumer missing? Disposition file.
End your run at CP1. No proofs beyond sketches. Do not touch Docs/ (read only), W3-DIST, W3-READER, Lean.

Budget ~4 Opus hours per part; 1 helper allowed (Claude Third, Opus or Sonnet 5.5, e.g. for the N audit).
