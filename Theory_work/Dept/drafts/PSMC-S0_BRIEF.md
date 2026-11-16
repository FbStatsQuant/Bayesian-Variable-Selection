# PSMC-S0 — scoping leg for the parallel-method premise tickets T-PART and T-N (Theory Department, 2026-11-15)

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

## Deliverables (to CP1, target Thu 11-19 12:00 CT)
1. `AUDIT_PART.md`: for every registered claim that consumes the block partition (START, START2, RM2, (V), visibility,
   start tables / start mode, Lemma ASM, OVL, NEC, the block-relative functionals, anything in C-DLV, W3-SAMP or
   W3-POST2 that names blocks), one row: `claim id@version | where the partition enters (file:line) | property used
   (e.g. block size ≤ B; clusters = exact complete-linkage cut; within-block |r| ≥ τ; between-block |r| < τ;
   deterministic given X) | holds for OD-5(c)? yes / no / needs a bridge | effort`. Note that several START/START2
   hypotheses are partition-free and dominate their block-relative versions ((B1)); say which theorems therefore hold
   for **any** partition with blocks ≤ B.
   Then: a candidate T-PART statement ("the theorems hold for the method's partition under OD-5(c)", or the bridge
   needed), a recommendation on τ_n and the packing order if theory prefers something else, and the numerics (if any)
   that would show the law change on π₀ matters.
2. `AUDIT_N.md`: every result that uses N_e ≥ p, N₀ = max(2500, n, p) or "common N at N_e": TH01(e)(f)(i), TH06,
   TH08 (SoP anchors, `State_of_Project/`), settings rows, and a confirmation (file:line) that RM-0, LT♯, TR, D and
   the headline selection/PIP/DIST results are stated for arbitrary N (OD-1 says so; check it). Candidate T-N
   restatements for general (N, R′), each with effort.
3. `CHECKPOINT_1.md`: both verdicts in plain words for HQ and the Engineering Department (≤ 1 page). Proposed
   follow-on tickets (tier, hours, what they consume). Anything that blocks OD-1/OD-5, in the first paragraph.
4. One Sol fidelity read of the two audits (fresh; brief saved first): is each row's file:line and "holds?" verdict
   right, and is any consumer missing? Disposition file.
End your run at CP1. No proofs beyond sketches. Do not touch Docs/ (read only), W3-DIST, W3-READER, Lean.

Budget ~5–7 Opus hours; 1 helper allowed (Claude Third, Opus or Sonnet 5.5, e.g. for the N audit).
