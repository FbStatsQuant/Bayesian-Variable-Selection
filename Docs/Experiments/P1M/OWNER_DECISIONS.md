# OWNER_DECISIONS — p = 10⁶ experiment (draft v0.2, after the Fable review; EXP-CP1, 2026-11-15)

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

## OD-2 Large-p calibration rule (escalation and rebuild loop) — BLOCKING for the budget (rewritten v0.2 after REVIEW R1)
The coded rule (`v3_calib.R:60-61, 102, 115-118, 154`) escalates once to tier 1 (N, H and the T ceiling × 4) if **any** of
**seven** triggers fires: E1, E2 (sd(log Ẑ_r) > 1 over 4 diagnostic islands), E3, forced pilot steps, grid failure,
**`grid_unconverged`** (the rebuild loop reached its cap ℓ without a bitwise-identical grid) and **`local_limit`**.
v0.1 listed five and missed the last two.
Evidence:
- in B3 the loop ran to the cap in 3 of 3 runs at p ≥ 5k (13 / 14 / 15 = ℓ);
- the 5k profile fit escalated on E2 and the grid.

**Confirmed by REQUESTS R6 (B3 records):**
- `grid_unconverged` fired at 10k and 20k;
- 5k converged on its 13th = last allowed rebuild;
- E2 fired at 5k, 10k and 20k.

So under the coded rule escalation fires at every p ≥ 5k measured, and it survives disabling E2 alone.

| option | cost at 1M (planning, c = 2 µs) | class / theory |
|---|---|---|
| (a) coded rule | ×4 when it fires (likely): ≈ 15k core-h per fit; **no tier fits** | unchanged |
| (b) v0.1 proposal: only E2 stops escalating | still escalates through `grid_unconverged` | **withdrawn** |
| (c) **bounded large-p calibration** (**rec.**): no escalation except grid-construction failure (C-DLV fallback kept); at most I_max rebuilds, then freeze the last grid with flag `grid_unconverged`; all triggers still recorded | fit ≈ 19 island-equivalents instead of 26–33 (−30 to −42%); sequential depth 4 rounds instead of up to 21 | [Δ𝒞]. Results stated "for any frozen 𝒞" (LT♯, TR, RM-0, N1) untouched. Re-check C-DLV and any card item that reads E2, tiers or `grid_unconverged` (theory ticket **T-CAL**) |
| (d) pilot schedule only (I_max = 0) | ≈ 16 island-equivalents | [Δ𝒞]; a coded path already (`v3_calib.R:122-124`) |

**Recommendation: (c).** I_max is fixed *before* rung A by a three-arm comparison at 10⁴ on the same 5 datasets (≈ 300
core-h): (a)-without-escalation / I_max = 3 / (d). It is compared on σ̂(log Ẑ_r), the ESS floor, PIP agreement, HPM and
T. Spec default: I_max = 3.
Owner question (REVIEW Q1): may the large-p method use a declared bounded calibration, given that the theorems hold for any
frozen schedule?

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
- PIP_Z is exactly the estimator that degenerates when σ̂ is large (R1). R6: R_eff fell from ≈ 16 of 16 at 2k to 1.6–4.2 at p ≥ 5k.

Revisit only if a rung shows islands disagreeing on the PIPs or the HPM. HQ's "hybrid" (union HPM, evidence-weighted
PIPs with fallback) remains available as a secondary output.

## OD-5 Block partition above about 150k (G3) — BLOCKING for 1M; theory ticket T-PART (rewritten v0.2 after REVIEW R3)
Exact complete linkage holds dense 16p²-byte arrays: 4 TB even condensed at 1M. It fits a 251 GB node only to about 180k
(full) or 260k (condensed); the 515 GB nodes reach about 360k.
v0.1's rule (connected components of {|r| ≥ τ_n}, exact linkage inside each component) **fails on the primary design**.
Under AR(0.6), the lag-1 correlation 0.6 > r_n = 0.372 (n = 200), so the graph is one component of size p.

| option | consequence |
|---|---|
| (a) exact linkage; stop the ladder at 10⁵ | no 1M |
| (b) new rule at 1M only | start law changes between rungs |
| (c) **complete linkage truncated at height 1 − τ_n, on the sparse graph {\|r\| ≥ τ_n}** (merge two clusters only while every cross pair is an edge; ties by R13). Then the coded top-down cut for clusters larger than B; next-fit packing with clusters ordered by **minimum index**. Used for the whole large-p mode, with an A3 paired comparison against exact linkage at 10⁴ (**rec.**) | O(edges) memory (≈ 2–3p edges on AR); equals the exact dendrogram below 1 − τ_n (complete linkage merges in increasing height; gate T11); [Δlaw] on π₀ only: through the merges above 1 − τ_n and the packing order |

**Recommendation: (c)**, τ_n = r_n = √(2 log p / n) (the method's neighbour-graph threshold) unless T-PART prefers
another. T-PART is asked about exactly this rule, including the packing order.

## OD-6 Design choices
**Recommendation:**
- **n.** n = 200 at 1M (A = 2.6). Reasons: B = 14 keeps the tables at about 2·10⁸ codes (about 2·10⁹ at n ≥ 256); per-step
  cost is lowest; X is 1.6 GB. n = 400 at 1M only in the Full tier. The n-trend comes from 10⁴ (n = 100–800) and 10⁵
  (n = 200, 400).
- **s₀ and β.** s₀ = 5. β* = a·(1, −0.8, 0.9, −0.7, 0.6) with a = 1 (strong) everywhere and a = 0.6 (weak, at the detection
  boundary) at 10⁴ for the PIP calibration and n-trend.
- **Designs.** AR(0.6) primary, IND, BLK(20, 0.5). Factor (cs) designs only at 10⁴ and only if the D1 ruling (P6 stage 1)
  says so. MIS and ADJ arms are optional at 10⁴.
- **Replicates.** 10 / 5 at 10⁴ (weak arm 20 at n = 100, 200), 5 at 10⁵, and at 10⁶ the cells of OD-14.
- **v0.2 (REVIEW Q7).** Distribution consistency is a decay-in-n statement. The plan shows the decay at 10⁴ (n = 100–800)
  and 10⁵ (n = 200, 400), and one point at 10⁶ (n = 200). Owner: is that acceptable? The alternative is n = 400 at 10⁶:
  tables ≈ 2·10⁹ codes (≈ 16 GB `logr`), ≈ 1.35× the cost per fit, and a table-memory check first.

## OD-7 Budget tier (HQ carries)
| tier | total billed core-h | what it shows |
|---|---|---|
| Minimal | ≈ 11k | existence proof: 2 AR-strong fits + 1 ADJ-OPP fit at 1M; a thin 10⁴/10⁵ ladder |
| **Standard (rec.)** | ≈ 26k (31k with 20% contingency) | C1–C8 with replicates; at 1M the five fits of OD-14 |
| Full | ≈ 42k | + n = 400 at 1M, BLK at 10⁵, all 10⁴ cells at 10 reps, MIS/FAC, 64-island census |

v0.2 basis:
- planning cost c = 2 µs per step with the bounded calibration of OD-2(c) (19 island-equivalents per fit): 27 / 272 / 2,720
  core-h per fit at 10⁴ / 10⁵ / 10⁶ (n = 200);
- the review's added cells (ablations, ADJ-OPP, null, second seed, three-arm calibration test, weak arm at 20 reps).

The direct-engine target (c ≈ 1.2 µs) would lower all tiers by about 40%. A label-major kernel (OD-16) might lower them by
much more, but that is a guess and no tier depends on it. **Recommendation:** approve Standard as a
ceiling, released stage by stage at the gates. Each gate re-sizes the rest from measured costs (as P6's ledger rule did).

## OD-8 Parallelism inside an island (G8)
| option | tag | gain | note |
|---|---|---|---|
| (a) speculative batched Gibbs scoring, serial commit (**rec.**) | [OP-bit] | 5–10× on 16 threads (UNVERIFIED) | output bits unchanged; Amdahl limit set by the serial commit. Needs OD-3 = B2-3 to drop the cache from the serial path |
| (b) counter-based per-particle streams | [OP-law] | near-linear | changes output bits; theorems hold for the law under the ideal-stream premise (O5); needs a new reference engine and distributional gates |
| (c) none: checkpointed serial islands | [OP-bit] | 1× | 1M fit ≈ 10–11 days of wall time; same core-h |

**Recommendation:** build (a); fall back to (b) only if (a) gives < 4× at 10⁵. Option (c) is always available, so this
decision changes wall time, not feasibility.
**v0.2: superseded by Note 1 and REVIEW R2b.** The recommendation is now (b) in its **position-addressed** form: every
uniform has a fixed address (island, phase, stage or round, particle, position, slot), drawn by a counter-based generator.
- Class: [OP-law], the same as (b).
- Any execution order (threads, particle groups, label-major) then gives the same bytes; gate T3.
- Theory ticket T-STREAM (O5, O18).

## OD-9 Number of islands R′
**Recommendation:**
- R′ = 16 at every rung, enough for σ̂ with 15 degrees of freedom and a union store.
- A 64-island census on 2 datasets each at 10⁴ and 10⁵, to chart σ̂ and R_eff against p (≈ 150 core-h at 10⁴ and
  ≈ 1,500 at 10⁵; included in Full only).
- ~~At 1M, R′ = 8 is the first budget lever~~ **withdrawn (v0.2, REVIEW R4):** at σ ≈ 1, R_eff/R′ ≈ 0.37, which leaves
  about 3 effective islands for PIP_Z and the evidence. R′ = 16 stays at every rung.

## OD-10 Competitors and framing
**Recommendation:**
- Competitors: lasso-CV, MCP/SCAD (biglasso), L0Learn, SuSiE, varbvs, BAS (10⁴), millipede/wTGS on CPU (10⁴–10⁵) and
  SIS → BVS as the split/screen category.
- v0.2 additions: SIS (d = 10⁴) → **our own method** (isolates what the joint run adds); an equal-budget model-space MCMC at
  10⁴ (10⁵ deferred until rung-A costs are measured).
- Framing of C1: "joint model-space SMC with PIPs at p = 10⁶ on individual-level data". The literature (lit_review
  rows 1–4) has a joint model-space sampler at 7.5·10⁵ (GPU, independent noise columns), mixture MCMC at 2·10⁶ (a′) and
  split-and-merge at 5·10⁵. So "not found in the literature", never "first".

## OD-11 Who builds the engine
**Recommendation:**
- The W3-SCALE leg-C team builds G1–G12 and G14 on its branch (it owns the engine and its gates).
- This department builds G13 (generator, DIST evaluator, competitor harness, analysis) and specifies the acceptance tests.
- HQ merges to `main` after Sol review.
- If W3-SCALE capacity is short, EXP takes G2/G4/G12 under the same gates.

---
### Note added 2026-11-15 (owner conversation): OD-8 under a wall-time limit
Felipe: about 1,000 concurrent CPUs on a quiet day; no multi-day runs. Under that limit only option (b) of OD-8
(per-particle counter-based streams, [OP-law]) uses 1,000 CPUs. Estimated wall time for one 1M fit is ≈ 5–6 h:
- calibration: 12 sequential rebuilds × ≈ 15–20 min, each rebuild 4 × 512 particles over ≈ 256 threads;
- final run: 16 islands × 2,500 particles over ≈ 1,000 threads, ≈ 1.2 h.

Option (a) (speculative, [OP-bit]) uses at most ≈ 16 threads per island, giving ≈ 1.5 days. Option (c) takes ≈ 10 days.
**Recommendation updated to (b)**, pending the owner's confirmation. Variables are never split across CPUs: every
particle sees all p (joint BVS). Splitting the variables would be split-and-merge, Song–Liang's category.

### Note 2 (2026-11-15): request shape on NOTS (owner conversation; correction)
A shared-memory process cannot span nodes, so one task is ≤ 1 node. Calibration therefore runs as 4 tasks × 96 CPUs,
not 4 × 384 (corrected from the earlier answer). Proposed request unit: **tasks of 96 CPUs (48 cores), --mem ≈ 20G (v0.2: 32G per REVIEW R6; file-backed pages are charged to the job),
--constraint=sapphirerapids, at most 16 at once = the 1,536-CPU cap** (memory ≈ 320 GB ≪ 2,304 GB).
- One fit alone: setup 1 × 96 → calibration 4 × 96 (≈ 4.5 h) → islands 16 × 96 (≈ 1.5 h) → merge 1 × 96. ≈ 6.5 h.
- Replicates pipelined (the next fit's calibration overlaps this fit's islands): the cap stays near full, so ≈ 2.5–3 h per fit
  amortised. 5 fits ≈ 15 h.
- Faster calibration (4 × 192 exclusive nodes, ≈ 2.5 h, or MPI across nodes) is optional.

---
## New items from the Fable review (v0.2; REVIEW_fable.md §6, REVIEW_disposition.md)

## OD-12 What the paper claims for the parallel (shipped) method (REVIEW Q2)
The 1M method differs from v3.1 **in law** in five places:
1. fixed N (OD-1);
2. R′ = 16 with process islands and a merge;
3. position-addressed streams (OD-8);
4. the truncated-linkage partition (OD-5);
5. the bounded calibration (OD-2).

It is not "output-identical". v3.1's bits are kept only in compat mode (one binary, two modes; ENGINEERING_SPEC §0).
**Recommendation:** the paper's parallel-method claim is "the same theorems, with each premise re-checked change by
change". The premise table is ENGINEERING_SPEC §4.2. Theory tickets for SMC-Theory: T-N, T-PART, T-STREAM, T-CAL,
T-MERGE (O1, O10, O19–O21).

## OD-13 Capacities that scale with p (REVIEW Q3, Q8)
- **Coded capacities.** Top store 40p + 1; leader stores 2 × 20p; calibration set V ≤ 40p + 1. At 1M: 4·10⁷ + 4·10⁷
  entries, about 2–5 GB per ledger in flat storage, plus minutes per grid build.
- **Which outputs depend on them.** DIST-C names the 40p + 1 top store. The final-run leader stores are returned
  (`v3_run.R:210`), but no consumer of them was found.
- **Recommendation:**
  - keep the top store at 40p + 1 (theory names it);
  - keep V as coded;
  - **drop the leader stores from final islands and from the output.** They feed V (calibration) only. This is a
    reporting change; please confirm nobody reads them.

## OD-14 Cells at 10⁶ (REVIEW Q4, R5)
As designed, 1M has only strong, isolated, evenly spaced truths. There the start mode plus LS0 probably already finds S₀,
and screening ties with the joint method.
**Recommendation (Standard): five fits at 1M, all n = 200:**
- AR-strong × 3 (the first is the pilot);
- **ADJ-OPP** × 1: adjacent AR truths of opposite sign, β = 1 and −0.8 at ρ = 0.6, so that the second's marginal effect
  is −0.2. Screening drops it;
- **AR-weak** × 1 (a = 0.6).

IND moves to 10⁴/10⁵ only.
Ablations run on every dataset: start mode / + LS0 / pilot + local / full.
C2 at 1M is stated as feasibility plus agreement with the trend of the lower rungs (3 of 3 gives a 95% lower bound of only 0.37).

## OD-15 New returned objects (REVIEW Q5, §3)
| object | cost | class | recommendation |
|---|---|---|---|
| PIP_𝒯 (store-renormalised, weight-free) and log Z_𝒯 (deterministic lower bound on log Z) | seconds | addition; existing outputs [OP-bit] | **return** |
| store-BMA law file `law.bin`: models above relative weight 10⁻¹², weights e^F, conjugate parameters | MB, seconds | addition; it is exactly Π̂^𝒯 of DIST-C(i) | **return**, as the method's "distribution output" |
| terminal particle supports | ≈ 100 KB per island | addition; diagnostic only (no theorem covers a particle law yet) | **archive, labelled diagnostic** |
| draws of (model, β, σ²) from the store law | ≈ 1 MB for 10⁴ draws | streams disjoint from the engine's | on request in `post`; not part of the fit |

New returned fields change the method's output list, so they need a registry entry (HQ).

## OD-16 One week for a kernel prototype before the engine kernel is fixed (REVIEW Q6, R2)
At 1M a Gram-free step reads 1.6 KB of X (≈ 168 TB per island), so memory bandwidth, not code quality, may bound the
direct design. A **label-major** kernel (one pass over X serves a group of particles; same class as OD-8 thanks to
position addressing) might cut a 1M fit from ≈ 1,600–2,700 to a few hundred core-h. That figure is the reviewer's guess.
**Recommendation:**
- 2 agent-days for an Owls prototype at 10⁵, in parallel with the engine skeleton (no delay to the build);
- the engine is built particle-major first, and the label-major kernel replaces it only if the prototype wins;
- the T3 gate guarantees identical output either way.
