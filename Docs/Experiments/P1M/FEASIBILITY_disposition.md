# FEASIBILITY_disposition — Fable 5.2 feasibility study (`FEASIBILITY_fable.md`), 2026-11-15

Disposition by the Engineering manager. Brief: `briefs/BRIEF_fable_feasibility.md`, with the owner's addenda (final
mandate c7f62b2; the 1M variant may modify the algorithm, 6b1cfd5).

## Verdict adopted
**Deliverable (1): a PLAN.** No NOTS infrastructure obstruction holds for every SMC BVS scheme, so no impossibility
argument (deliverable 2) is offered. The plan is **V-1M**:
- the same target on all p, the same π₀ family, the same bridge and labelled round;
- 16 islands + a merge;
- the changes listed in `ENGINEERING_SPEC.md` §0-v2.

## Own checks before adopting (Engineering manager, 11-15, read-only `ssh nots`)
- **Distinct supports per stage (the study's measurement 2, partly).** `distinct_moved` in the final islands of the
  W3-SCALE profiles: 1,349–1,647 of N = 2,500 at p = 2k (≈ 57%); 9,453–12,559 of N = 20,000 at 5k (≈ 52%). This
  confirms the study's "≈ 1,500 distinct supports per round": a diverse population. Sharing step 3 across particles can
  save at most about 2× (so M ≈ 1.5 is optimistic; planning keeps M = 3).
  Accepted Gibbs moves per round (`gibbs_change`) are not in these records; the stage tables of the P6 fits are the next
  place to look.
- **The right-tail island at 5k** (profile, N = 20,000): the island with the highest log Ẑ_r (−114.03, against
  −115.3 to −115.7) also had the highest minimum ESS share (0.853, against 0.70–0.73). This is consistent with the
  study's lineage-loss hypothesis (§2.1), but it is one fit.

## Item by item

| # | item | verdict | action |
|---|---|---|---|
| F1 | Label-major batched kernel removes the bandwidth blocker. Measured on Owls: 42–128 ns (class A) and 163–288 ns (bit form) per (support, label), against 2,100–2,700 ns for the direct step. X traffic 6 TB instead of 528 TB per precise island | **ADOPT** | build order reversed: **label-major first**, particle-major only as its one-thread reference (T3). Supersedes D-9 |
| F2 | Class-A arithmetic at 1M (scores agree with the coded scorer to ≈ 10⁻⁹ relative); bit form for the theory's method (study Q1) | **ADOPT** (technical) | the variant may modify the algorithm; the bit-form kernel serves the theory mode on the overlap rung. New D-15 |
| F3 | Cost model c = M·c_s + c_f; planning M = 3, c_s = 90 ns, c_f = 30 ns | **ADOPT** | spec §7 v2; G0 measures M, store-offer cost and SPR scaling |
| F4 | Low-precision X, Gram-block caches, sufficient statistics, bounded skipping: not recommended | **ADOPT** (reasons accepted) | — |
| F5 | Evidence degeneracy is not a feasibility blocker (no selection, PIP or distribution output uses the weights) | **ADOPT** | — |
| F6 | Store/occupancy evidence log Ẑ_occ = log Z_A − log π̂(A) (A = top-M of the merged store), reported with log Z_𝒯 (deterministic lower bound) and the unbiased SMC log Ẑ (study Q2) | **ADOPT** as the precise evidence at 1M, labelled "no theorem yet" (consistent in N, not unbiased). Validated at p ≤ 25 against enumeration and at 10⁴ against the theory method | new D-13. The paper wording goes on the owner sheet (it touches a claim) |
| F7 | PIP_𝒯 on the merged store, with the bound 1 − π̂(𝒯) | **ADOPT** (already D-8) | — |
| F8 | Grid refinement ×m (m = 4) | **ADOPT-CONDITIONAL**: m ∈ {1, 4} fixed by the 10⁴ precision study | new D-12 |
| F9 | Systematic resampling; more N-swap labels (study Q4) | **ADOPT-CONDITIONAL**: switched on only if the 10⁴ precision study shows a gain | new D-14 |
| F10 | N = 2,500 default; N = 10⁴ arm in the precision study and one 1M doubling fit | **ADOPT** | D-1 updated |
| F11 | Bounded calibration: pilot + at most 3 rebuilds; I_max ∈ {0, 3} by the study; thread the V re-scoring | **ADOPT** | D-2 updated |
| F12 | Islands targeting disjoint parts; interacting islands; in-island adaptive schedules: not recommended | **ADOPT** (reasons accepted) | — |
| F13 | Island homogeneity test of top-M occupancies per fit (flag only) | **ADOPT** | spec §5 invariant I7 |
| F14 | Gates G0 → G-A → G-B → G-C → G-C2, with G0 thresholds (≤ 700 ns per step: precise; 700–1,500: baseline; > 1,500: stop and report) | **ADOPT** | plan and spec v2 |
| F15 | Overlap design: exact at p ≤ 25; **5k anchor with the existing unmodified code**; 10 datasets at 10⁴ with T run in the new engine's theory mode (same law) and V, 2 seeds each; optional 10⁵ T overlap (≈ 6,100 core-h); 1M self-check (V vs V with N = 10⁴). Tolerances as in its §3.2 | **ADOPT**. The 10⁵ T overlap goes to the **owner sheet** (budget). "Bits at ≤ 5k, law at 10⁴" as the meaning of "validated" (study Q5) also goes to the owner sheet (paper claim) | spec §4 v2 |
| F16 | T as coded cannot run at 10⁴ inside 24 h (escalation is certain at p ≥ 5k, R6) | **ADOPT** as a fact. T at 10⁴ runs in the new engine's theory mode, threaded and checkpointed; compat-mode bits are anchored at ≤ 5k | — |
| F17 | Budget ≈ 16.4k + 25% = 20.5k core-h (26.6k with the 10⁵ T overlap); a precise 1M fit ≈ 963 core-h, ≈ 2.2 h at the cap | **ADOPT** as the planning budget; replaces OWNER_DECISIONS OD-7 v0.2 tiers | owner sheet |
| F18 | Diffuse posterior at 1M, n = 200 (π(S₀ \| data) ≈ 0.3–0.45 on one synthetic draw); null PIPs up to 0.1–0.2 expected | **ADOPT** as a wording risk. **ADD:** the 10⁵ rung reports π̂(S₀) by n (200, 400), so the 1M wording is set from data | plan §1 C2/C4 wording |
| F19 | Not measured: store offers, M on real fits, SPR per-core speed, 48-thread scaling | **ADOPT** as gate G0 | §9 / batch request to HQ (≤ 5 core-h kernel benchmark + ≈ 60 core-h stage-level study) |

## What changes elsewhere
- `ENGINEERING_SPEC.md` → **v2**: a new §0-v2 (the V-1M change list, the overlap design, gates, kernels, budget) on top
  of v1. §7 is superseded where §0-v2 gives numbers.
- `DECISIONS.md`: D-1, D-2 and D-9 updated; D-12 to D-15 added.
- `OWNER_DECISIONS.md` → owner sheet `OWNER_SHEET.md`: OD-7 (budget: 20.5k vs 26.6k with the 10⁵ T overlap), OD-10
  (competitors and framing), the paper wording for the evidence at 1M and for "validated" (F6, F15).
