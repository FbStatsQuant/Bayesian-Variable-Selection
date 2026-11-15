# OWNER_DECISIONS — p = 10⁶ experiment (draft v0.1, EXP-CP1, 2026-11-15)

Each item: options, consequences, recommendation. "HQ" = decisions with a budget, compute or code-on-main impact,
which HQ carries. Numbers are from `EXPERIMENT_PLAN.md` §6 (billed core-h, pessimistic per-step cost c = 2 µs unless stated).
Ranking: **OD-1, OD-2, OD-3, OD-5 block the 1M rung**; the others shape it.

---

## OD-1 Particle count per island at large p (W3-SCALE reserved item (i); obligation O4) — BLOCKING
| option | 1M island (formula; T = 30) | theory | consequence |
|---|---|---|---|
| (a) keep N_e = max(2500, n, p) | 1.6 years; particle memory 233 GiB | as delivered | **1M impossible**; 10⁵ at about 6 days per island |
| (b) fixed N = 2,500 for every p (**rec.**) | 36 h serial (c = 1); about 70 h at c = 2 | RM-0 is pathwise for every N_e; LT♯ and TR hold for any N_e and frozen schedule; D holds per draw. TH01(e)(f)(i), TH06 and TH08 need restating for general (N, R′) (ticket T-N, short) | equals v3.1 exactly for p ≤ 2,500 (N₀ = 2,500 there). Evidence precision degrades: σ̂(log Ẑ_r) ≈ 0.8–1.2 at 5k–20k, and B3 showed that 4N does not cure the tail |
| (c) mixed: N = p up to p*, fixed above | — | as (b) above p* | keeps the old law to p* (e.g. 20k); adds a discontinuity in the ladder |

**Recommendation: (b), N = 2,500.** It is the only option under which 1M exists. It matches v3.1 where v3.1 was studied
(p ≤ 2.5k), and every headline selection and PIP theorem is stated for arbitrary N_e. Rung A1 measures the law change
directly at 10⁴ (old law against fixed N on the same 10 datasets).

## OD-2 Calibration escalation at large p (E2 trigger) — BLOCKING for the budget
In the code (`v3_calib.R:102,154`) any trigger escalates once to tier 1, with N, H and the T ceiling multiplied by 4. The
triggers are E1, E2 (sd(log Ẑ_r) > 1 over the 4 diagnostic islands), E3, forced pilot steps and grid failure. In
B3, σ̂ ≈ 1 at p ≥ 5k, and the 5k profile escalated on E2.
| option | cost at 1M | theory |
|---|---|---|
| (a) keep as coded | about ×4 when it fires: ≈ 15k core-h per 1M fit, rung C alone ≈ 75k; **no tier fits** | unchanged |
| (b) in fixed-N mode, E2 does not escalate (still recorded); grid failure, E1 and E3 still escalate (**rec., pending A2 data**) | as planned | [Δ𝒞]. Delivery (C-DLV) uses the tier-1 fallback on *grid-construction failure*, which (b) keeps. Results "for any frozen 𝒞" are unaffected. Check that no delivered theorem uses E2 |
| (c) E2 → raise R′ by a census rule (O3) instead of N | +R′ islands | V-measurable census, O3; rule not designed yet |

**Recommendation: (b)**, decided at gate G-B with A2's measured E2 frequency at 10⁴. If HQ prefers (a), the 1M rung
must assume escalation: rung C alone rises to about 75k.

## OD-3 Cost column (B2-3) and `fresh` counters — BLOCKING for G6 and G8(a)
O17 requires identical published quantities. `fresh` depends on the whole ordered cache history.
| option | at 1M | consequence |
|---|---|---|
| B2-1 trace replay | ≈ 2·10¹² lookups ≈ 30 TB per fit | **physically impossible** at 1M; feasible only as the R′ = 4 equivalence build at p ≤ 2k |
| B2-2 cost column filled by serial runs only | large-p fits publish no cost column | blocks C1's cost evidence exactly where it matters |
| B2-3 redefine (**rec.**) | publish `logical` score counts (machine-free, identical under any parallel layout) as the cost measure, plus `fresh` under a declared, fixed cache capacity as a secondary, labelled quantity | registry/lifecycle note for the cost column; old tables keep their values. It frees G6 (fixed cache size) and G8(a) (speculative scoring) to be [OP-bit] for everything else |

**Recommendation: B2-3, with `logical` as the published cost measure.** Combine it with B2-1 only for the p ≤ 2k
equivalence build if HQ wants that proof.

## OD-4 Primary PIP (W3-SCALE reserved item (ii))
**Recommendation: keep equal-weight `pip_primary` as primary; report PIP_Z, R_eff/R′ and max W_r alongside.** Reasons:
- in all 6 B3 runs and all 25 saved fits the islands agree (max |PIP_Z − PIP_eq| ≤ 0.0023);
- LT♯ and TR are proved for the coded equal-weight RB PIP;
- PIP_Z is exactly the estimator that degenerates when σ̂ is large (R1).

Revisit only if a rung shows islands disagreeing on the PIPs or the HPM. HQ's "hybrid" (union HPM, evidence-weighted
PIPs with fallback) remains available as a secondary output.

## OD-5 Block partition above about 150k (G3) — BLOCKING for 1M; needs theory ticket T-PART
Exact complete linkage holds dense 16p²-byte arrays: 4 TB even condensed at 1M. It fits one 251 GB node only up to about
180k (full) or 260k (condensed).
| option | consequence |
|---|---|
| (a) exact linkage, 10⁴–10⁵ only; stop the ladder at 10⁵ | no 1M |
| (b) new rule at 1M only | the ladder changes start law between rungs; 1M not comparable to 10⁴/10⁵ |
| (c) **new rule (threshold components {\|r\| ≥ τ_n} + exact complete linkage inside components) for the whole "v4 large-p mode"**, plus a paired comparison against exact linkage at 10⁴ (A3) (**rec.**) | one method across the ladder; [Δlaw] on π₀ only (target, kernel and outputs unchanged); START/START2/RM2 premises re-checked by T-PART before rung C |

**Recommendation: (c).** τ_n is to be fixed with the theory side. One natural choice is the neighbour-graph threshold
r_n = √(2 log p / n) already in the method.

## OD-6 Design choices
**Recommendation:**
- **n.** n = 200 at 1M (A = 2.6). Reasons: B = 14 keeps the tables at about 2·10⁸ codes (about 2·10⁹ at n ≥ 256); per-step
  cost is lowest; X is 1.6 GB. n = 400 at 1M only in the Full tier. The n-trend comes from 10⁴ (n = 100–800) and 10⁵
  (n = 200, 400).
- **s₀ and β.** s₀ = 5. β* = a·(1, −0.8, 0.9, −0.7, 0.6) with a = 1 (strong) everywhere and a = 0.6 (weak, at the detection
  boundary) at 10⁴ for the PIP calibration and n-trend.
- **Designs.** AR(0.6) primary, IND, BLK(20, 0.5). Factor (cs) designs only at 10⁴ and only if the D1 ruling (P6 stage 1)
  says so. MIS and ADJ arms are optional at 10⁴.
- **Replicates.** 10 / 5 at 10⁴, 5 at 10⁵, 3 + 2 at 10⁶.

## OD-7 Budget tier (HQ carries)
| tier | total billed core-h | what it shows |
|---|---|---|
| Minimal | ≈ 10.4k | existence proof: 2 AR fits at 1M, a thin 10⁴/10⁵ ladder |
| **Standard (rec.)** | ≈ 31.6k (38k with contingency) | C1–C8 with replicates, at 1M: AR × 3 + IND × 2 |
| Full | ≈ 52k | + n = 400 at 1M, BLK at 10⁵, all 10⁴ cells at 10 reps, MIS/ADJ/FAC |

The v4 per-step target (c ≈ 1.2 µs) would lower all three by about 40%. **Recommendation:** approve Standard as a
ceiling, released stage by stage at the gates. Each gate re-sizes the rest from measured costs (as P6's ledger rule did).

## OD-8 Parallelism inside an island (G8)
| option | tag | gain | note |
|---|---|---|---|
| (a) speculative batched Gibbs scoring, serial commit (**rec.**) | [OP-bit] | 5–10× on 16 threads (UNVERIFIED) | output bits unchanged; Amdahl limit set by the serial commit. Needs OD-3 = B2-3 to drop the cache from the serial path |
| (b) counter-based per-particle streams | [OP-law] | near-linear | changes output bits; theorems hold for the law under the ideal-stream premise (O5); needs a new reference engine and distributional gates |
| (c) none: checkpointed serial islands | [OP-bit] | 1× | 1M fit ≈ 10–11 days of wall time; same core-h |

**Recommendation:** build (a); fall back to (b) only if (a) gives < 4× at 10⁵. Option (c) is always available, so this
decision changes wall time, not feasibility.

## OD-9 Number of islands R′
**Recommendation:**
- R′ = 16 at every rung, enough for σ̂ with 15 degrees of freedom and a union store.
- A 64-island census on 2 datasets each at 10⁴ and 10⁵, to chart σ̂ and R_eff against p (≈ 150 core-h at 10⁴ and
  ≈ 1,500 at 10⁵; included in Full only).
- At 1M, R′ = 8 is the first budget lever (−30% of rung C).

## OD-10 Competitors and framing
**Recommendation:**
- Competitors: lasso-CV, MCP/SCAD (biglasso), L0Learn, SuSiE, varbvs, BAS (10⁴), millipede/wTGS on CPU (10⁴–10⁵) and
  SIS → BVS as the split/screen category.
- Framing of C1: "joint model-space SMC with PIPs at p = 10⁶ on individual-level data". The literature (lit_review
  rows 1–4) has a joint model-space sampler at 7.5·10⁵ (GPU, independent noise columns), mixture MCMC at 2·10⁶ (a′) and
  split-and-merge at 5·10⁵. So "not found in the literature", never "first".

## OD-11 Who builds the engine
**Recommendation:**
- The W3-SCALE leg-C team builds G1–G12 and G14 on its branch (it owns the engine and its gates).
- This department builds G13 (generator, DIST evaluator, competitor harness, analysis) and specifies the acceptance tests.
- HQ merges to `main` after Sol review.
- If W3-SCALE capacity is short, EXP takes G2/G4/G12 under the same gates.
