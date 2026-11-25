# EXPERIMENT_PLAN — SMC-BVS at p = 10⁶ (draft v0.2 after the Fable review, EXP-CP1, 2026-11-15; v0.3 update 2026-11-24; **v0.4 update 2026-11-25: the simulation suite is S1 and S2 only, S3 dropped**)

Status: **DRAFT FOR REVIEW.** Planning only: nothing is built, submitted or changed. Author: Experiment department
(Claude Opus 5.5, Claude Third, Owls). HQ approves every launch; one independent Sol review (feasibility and budget) comes
before any job. Open owner items are in `OWNER_DECISIONS.md` (OD-n); NOTS queries for HQ are in `REQUESTS.md`.

Sources read: BRIEF.md; HOLDS.md (empty at 17:07 CST); PROGRAM.md; theory_status_2026-11-13.tex; W3-DIST/STATEMENT.md
v1.0.2; W3-SCALE CHECKPOINT_2 and DESIGN_v1 rev 3 (`origin/theory/W3-SCALE`); W3-P6 DESIGN, CHECKPOINT_1, LOG
(`origin/theory/W3-P6`); SCALING_DESIGN_v0; lit_review_large_p_BVS.md; the core code (`Scripts/SMC_BVS/core/`, read at
daa08a3). One local Owls measurement (block sizes, §6.1).

Tags as in SCALING_DESIGN_v0: **[OP-bit]** same output bits as v3.1; **[OP-law]** same law, different bits or stream use;
**[Δ𝒞]** changes only how the frozen calibration is computed; **[Δlaw]** same target, different sampler law;
**UNVERIFIED** extrapolated or not run.

---

## v0.4 update (2026-11-25): S3 is DROPPED; the primary simulation suite is S1 and S2 only (owner decision via HQ). PLAN ONLY.

No run, NOTS job, Owls compute or ssh was used for this update; SMC-BVS is on its break (HQ H-54) and the owner restarts it later.

- **Binding decision.** The last entry of `MAIN:Theory_work/Wave3/HQ_DECISIONS.md` (line 910, "2026-11-25. OWNER: the simulation suite is S1 and S2 only; S3 is DROPPED") supersedes the S3 part of the 11-24 evening entry (line 908). **Why (the entry's reason):** an independent Haiku re-check (3 agents, full text) confirmed S1 = Griffin et al. 2021 Sec 4.1 + Table 1 exactly and S2 = Hastie et al. 2020 Sec 3.1 exactly, but S3 matches no paper: it was a composite (ρ = 0.5 from Shin 2018, ρ = 0.8 from Dezeure 2015, s₀ = 10 a Theory choice, n and p an HQ default copied from S1).
- **What changed in this file.**
  - **S3 removed** from §1 (v0.3 note), §2.0 (the S3 table; one line remains at §2.0.4), §2.0.5, §2.0.7, §3.6, §4A, §6A (all of it re-computed), §7 R13 and §10 (the two S3-only references).
  - **Cells:** 138 (S1 16 + S2 120 + block E 2), down from 170 [D, script output]. **Our SMC fits: 8,260** (6,900 F2 + 1,360 T), down from 10,180.
  - **Central total 5,294 core-h NOTS-billed if everything ran on NOTS (range 2,312–15,759), down from 11,813 (4.4k–37.7k).** The recommended NOTS/Owls split is 2,330 NOTS billed + 2,884 Owls core-h (§6A.7).
  - **Block E does not depend on S3** (it is two S1 cells), so it stays unchanged.
  - **Open choices that only concerned S3 are removed:** the S3 signal and SNR levels, and the Theory question on S3 (compound symmetry, D1, ties in the partition). The HQ_DECISIONS entry does not keep either.
  - **§6A.9 (new, replaces the pilot paragraph of §6A.6):** the calibration pilot re-based on S1/S2.
  - **Script:** `results/s1s3_compute_estimate.py` now drops S3 by default (`INCLUDE_S3`; `--with-s3` reproduces the v0.3 numbers, 11,813 central, as a check). Every number in §6A is that script's output.
- **Where v0.4 and v0.3 conflict, v0.4 governs.** Writing removes S3 from `sim_designs_cite.tex` (HQ_DECISIONS line 910).

## v0.3 update (2026-11-24): the primary simulation suite is S1–S3 (owner decision via HQ). PLAN ONLY. **[S3 part superseded by v0.4 above.]**

No run, NOTS job, Owls compute or ssh was used for this update; SMC-BVS is on its break (HQ H-54) and the owner restarts it later.

- **Binding decision.** The 11-24 evening entry of `MAIN:Theory_work/Wave3/HQ_DECISIONS.md` (line 908, "2026-11-24 evening. OWNER: the
  simulation suite is S1–S3 from BENCH_DESIGN §6.1") made S1–S3 the simulation suite; line 910 (11-25) dropped S3. The spec is `MAIN:Theory_work/Dept/assess/BENCH_DESIGN/REPORT.md`
  §6.1 (9e783a89); the per-paper setups are in `MAIN:…/BENCH_DESIGN/PAPERS.md`. Engineering updates this plan only.
- **What changed in this file** (everything else is the v0.2 text, unchanged):
  - **§2.0 (new):** the primary suite S1–S3: cells, data-generating process, replicates, the two engines.
  - **§2.1–§2.3 and §6.2–§6.4:** the own-β cells (s₀ = 5, β* = a·(1, −0.8, 0.9, −0.7, 0.6)) are labelled **SECONDARY** and kept (§2.0.6 says why).
  - **§3.6 (new):** the standard metrics and the real-data rule. **§4A (new):** competitors for S1–S3. **§6A (new):** fit counts and the compute estimate. **§10 (new):** References.
- **Where v0.3 and the older text conflict for the simulation suite, v0.3 governs;** the older text still governs the secondary cells.
- **Paths.** File references are relative to this folder (`Docs/Experiments/P1M/`, worktree branch exp/P1M) unless prefixed `MAIN:` (the main clone `/home/fb31/Bayesian-Variable-Selection/`).
- **Labels on every number in the v0.3 text:** **[M]** measured (a file is cited); **[D]** derived by arithmetic from measured numbers; **[X]** extrapolated outside the measured range (unverified);
  **[P] PROPOSED (needs owner/HQ)** a value the sources do not fix.

---

## v0.2 errata (Fable review, `REVIEW_disposition.md`). These override the text below wherever they conflict.
- **Calibration (OD-2 rewritten).** Seven triggers escalate, including `grid_unconverged`, which fired in effect in 3 of 3
  B3 runs at p ≥ 5k (rebuilds = ℓ). The plan now assumes a bounded calibration [Δ𝒞] (I_max = 3, fixed by a three-arm test
  at 10⁴). Cost per fit: 19 island-equivalents, not 26.3.
- **Partition (OD-5, G3 rewritten).** Complete linkage truncated at 1 − τ_n on the sparse graph. The v0.1 component rule
  fails on AR(0.6).
- **Hot path.** The direct Gram-free step may be bandwidth-bound at 1M (1.6 KB of X per step). Gate T5 measures it before
  G-B. A label-major prototype (OD-16) runs in parallel. Streams are position-addressed (OD-8).
- **Rung C cells (OD-14):** AR-strong × 3, ADJ-OPP × 1, AR-weak × 1 (n = 200); IND only at 10⁴/10⁵. Added everywhere:
  ablations (start mode / + LS0 / pilot + local / full), a null control at 10⁴/10⁵, a second seed on the same data,
  SIS → our method, an equal-budget MCMC at 10⁴, and the exact reference at p ≤ 25 (T8).
- **C2 at 1M** is stated as feasibility plus agreement with the trend of the lower rungs (3/3 gives a 95% lower bound of 0.37).
- **Budget (OD-7 v0.2):** Minimal ≈ 11k, Standard ≈ 26k (31k with contingency), Full ≈ 42k. Planning cost per fit:
  27 / 272 / 2,720 core-h at 10⁴ / 10⁵ / 10⁶. The Minimal tier is the stated expectation for December.
- **New metrics:** log Z_𝒯 (deterministic lower bound), PIP_𝒯, ablation outcomes, seed agreement, occupancy check (needs
  terminal supports, OD-15).
- **Engineering:** ENGINEERING_SPEC.md v1 replaces §5's gap list as the build document. Task memory 32 GB.

## 0. Summary

1. **Feasibility at 10⁶ depends on two law-level choices and one engineering wall. Bit-identical parallelism alone will not get there.**
   - The v3.1 rule N_e = max(2500, n, p) gives 1.6 years per island at 1M. Fixed N per island (OD-1) is required.
   - Exact complete linkage (block partition) needs a p × p distance matrix: 4 TB condensed at 1M. Above about
     150–250k the partition rule must change (OD-5, [Δlaw], start law π₀).
   - In B3 the calibration's E2 trigger (sd(log Ẑ_r) > 1) fired at p ≥ 5k. If it fires at 1M it multiplies the cost by
     about 4 (OD-2).
2. **The headline selection theorems survive these choices.**
   - RM-0 holds pathwise for every seed, N_e, R′ and calibration outcome. LT♯/TR hold for any N_e and frozen schedule.
   - The partition change needs a premise re-check of START/START2/RM2 (theory ticket T-PART, §5).
3. **Planned cost of one fit (pessimistic, today's measured per-step cost).** About 38 core-h at 10⁴, 380 at 10⁵ and
   3,800 at 10⁶ (n = 200, N = 2,500, R′ = 16, no escalation). The v4 engine target is about 0.6× of this.
4. **Budget options.**
   - Minimal (existence proof): about 10k core-h.
   - Standard (recommended): about 31.6k core-h, or 38k with contingency.
   - Full: about 52k core-h.
   - All three are an order of magnitude above any earlier ticket (W3-P6: 1.9k).
5. **Wall time.** Engineering 3–4 weeks, then the ladder 10⁴ → 10⁵ → 10⁶ with gates. First 1M fit about
   2026-12-21; 1M results in the first half of January 2027. Holidays put this at risk.

## 1. Claims the experiment supports

Every claim is illustrated, not proved, by the experiment. Designs appear only as examples (presentation rule).

| id | claim (what the numbers show) | theorem / paper section | primary metric |
|---|---|---|---|
| C1 | **Feasibility.** Joint (non-split, no screening) SMC-BVS completes at p = 10⁶ on individual-level data. | paper §Experiments (scale); theory #16 (parallel SMC, W3-SCALE) | completion; wall, core-h, peak RSS (§3.5) |
| C2 | **Reported model = S₀** with probability rising to 1 in n (estimated at 10⁴/10⁵; at 10⁶ feasibility plus agreement with that trend). | RM-0/RM-F/RM-R (#7), RM2-F/R (#8), Delivery C-DLV (#10), GEN/GROW (#6) | P̂(HPM = S₀), outcome class (posterior / search) |
| C3 | **Start mass.** π₀(S₀) → 1 at the rate n^{−c}, computed exactly from the start tables. | W3-START, START2 (#5) | log(1 − π₀(S₀)) against log n |
| C4 | **PIP consistency.** pip_primary → 1_{S₀} in sup-norm; MPM = HPM = S₀. | SAMP LT♯, TR, D (#9); C-PACK SL1/SL2 | sup_{j∉S₀} PIP, min_{j∈S₀} PIP, P̂(MPM = S₀) |
| C5 | **Distribution consistency (top priority).** The returned output's predictive law contracts to f* in Hellinger at the rate s₀ log p / n (store-BMA) and at the parametric rate under selection (HPM/MPM plug-in). | W3-DIST: DIST-1, DIST-2, DIST-3, DIST-C(i)–(iv) (candidates, status CANDIDATE); POST2 Hellinger (#2) | d_H² of the plug-in and predictive outputs; n·d_H² against n (§3.3) |
| C6 | **Certified screening** where the reported-model conditions are not met: certified models of size ≤ q_n contain S₀. | W3-SCR (#11) | P̂(S₀ ⊆ Ŝ given certified) |
| C7 | **Evidence and merge diagnostics.** These are measured, not claimed: unbiased pooling holds, and the dispersion is documented as a function of p. | N1, O1, O19; O2 is open | σ̂(log Ẑ_r), R_eff/R′, \|PIP_Z − PIP_eq\| |
| C8 | **Comparison.** Selection, prediction and cost against methods that actually run at each p. | paper §Experiments | §4 |
| C9 (contingent) | **Strong factors at p ≫ n** (D1), at 10⁴ only, if P6 or the D1 ruling says it is fair game. | D1 (#12) | as in C2 and C6 |

**v0.3/v0.4 note.** The selection, PIP, distribution and comparison claims (C2, C4, C5, C8) are now evidenced first on the primary suite S1 and S2 (§2.0), in the field's
metrics (§3.6) and against the field's competitors (§4A). The scale claim C1 and the large-p start-mass and evidence claims (C3, C7) stay on the secondary own-β cells (§2.1–2.3),
which supply the 10⁴, 10⁵ and 10⁶ rungs that S1 and S2 do not reach (they stop at p = 5,000). **[P] PROPOSED (needs owner/HQ):** this split of the claims between the two families.
C9 (strong factors, D1) stays contingent as in v0.2: with S3 dropped, no primary cell is a compound-symmetry design.

Claims are always worded with the theorem's labels. C5's coded-output statements are conditional on the delivery premises
P-STORE / P-HIT, so the run records the diagnostics for those premises (§3.3). C5 is stated only as an
illustration of a candidate theorem until W3-DIST records a status.

## 2. Designs

### 2.0 PRIMARY: the simulation suite S1 and S2 (owner decisions 2026-11-24 and 2026-11-25; spec `MAIN:…/BENCH_DESIGN/REPORT.md` §6.1 rows S1–S2; S3 dropped)

#### 2.0.1 Common data model
Random design as in §2.1: each replicate draws a fresh (X, ε) with rows x_i ~ N_p(0, Σ), y = Xβ* + ε, ε ~ N(0, σ²I), α* = 0. Data are regenerated from the seed
(counter-based generator, hash-checked, as in §2.1). At p ≤ 5,000 and n ≤ 1,000 a matrix is ≤ 40 MB **[D]** (n·p·8 bytes), so nothing needs to be shipped.
**[P] Seeds (needs owner/HQ):** data seed = 5·10⁸ + 10⁶·(suite code) + 10³·(cell index) + replicate; engine seed s1 = data seed, as in `results/overlap1e4/OVERLAP_1e4_PREREG.md` §1.
Every cell reports its SNR three ways (REPORT §6.1 S8; §3.6).

#### 2.0.2 S1: YWJ/Griffin (the Bayesian-sampler standard; REPORT §0.2, §6.1 S1)
| item | spec |
|---|---|
| Σ | AR(1), Σ_jk = 0.6^{\|j−k\|}. This is the Griffin version ("YWJ/Griffin, ρ = 0.6"); YWJ's own e^{−\|j−k\|} (ρ ≈ 0.37) is **not** used (REPORT §6.1 S1) |
| (n, p) | n ∈ {500, 1000} × p ∈ {500, 5,000} (four pairs) |
| s₀, S₀ | 10; the first 10 coordinates |
| β* | SNR·√(log p / n)·(2, −3, 2, 2, −3, 3, −2, 3, −2, 3), zeros elsewhere; σ = 1 |
| SNR | {0.5, 1, 2, 3} |
| cells | 2 × 2 × 4 = **16** |
| signal size [D, REPORT §2 table, ν scales as SNR²] | at n = 500, p = 5,000: ν = 0.11 / 0.44 / 1.75 / 3.94 for SNR 0.5 / 1 / 2 / 3 (PVE 0.30 / 0.64 / 0.80 for SNR 1 / 2 / 3); β_min/(σ√(log p/n)) = 2·SNR |

#### 2.0.3 S2: Hastie–Tibshirani–Tibshirani grid (the best-subset standard; REPORT §6.1 S2, `MAIN:…/PAPERS.md` "Hastie2020")
| item | spec |
|---|---|
| Σ | AR(1), Σ_jk = ρ^{\|j−k\|}, ρ ∈ {0, 0.35, 0.7} |
| (n, p, s) | (50, 1000, 5) and (100, 1000, 10) (HTT "high-5" and "high-10") |
| β* | beta-type 1: s ones at roughly equally spaced indices; beta-type 2: the first s coordinates equal 1 (PAPERS.md). **[P]** beta-type 3 (optional in REPORT) is left out |
| SNR | ν = Var(xᵀβ)/σ² on the 10-point grid {0.05, 0.09, 0.14, 0.25, 0.42, 0.71, 1.22, 2.07, 3.52, 6.00} (PVE 0.05–0.86); σ² = β*ᵀΣβ*/ν |
| cells | 3 × 2 × 2 × 10 = **120** |

#### 2.0.4 S3 (equicorrelated): DROPPED by the owner, 2026-11-25
Dropped by the owner (HQ_DECISIONS line 910): S3 matched no paper. It was a composite of ρ = 0.5 (Shin 2018), ρ = 0.8 (Dezeure 2015), s₀ = 10 (a Theory choice) and an (n, p) copied from S1. No S3 cell, fit or cost remains in this plan. The 32 S3 cells and their compute are visible only through `results/s1s3_compute_estimate.py --with-s3` (the v0.3 check).

#### 2.0.5 Replicates (REPORT §6.1 S7, §2 "Replicates")
- REPORT S7: ≥ 50 data sets per cell for selection rates (100 if cheap), with Monte Carlo standard errors. For efficiency: 1 data set × ≥ 50 independent runs. The field's usual counts are 50–200 (selection) and 10 (best-subset papers; Hastie et al. use 10, PAPERS.md).
- **[P] PROPOSED (needs owner/HQ), F2 engine (§2.0.7):** **R_F = 50** data sets per cell in both suites (the S7 floor; 100 for S1 if cheap, since F2 is cheap, §6A.3).
- **[P] PROPOSED (needs owner/HQ), theorem-covered method T (§2.0.7):** a paired **bridge subset of R_T = 10** of the same data sets per cell (the HTT count), because T is about 7–20× dearer than F2 per fit (§6A.3, [D]). T on every data set (R_T = 50) is costed in §6A.6; with S3 gone it is 20.4k central, about 91% of the remaining envelope, so it still does not fit with a reserve.
- **[P] Efficiency block E:** the S1 cell n = 500, p = 5,000 at SNR ∈ {1, 2}, **1 data set × 50 independent engine seeds** (F2), against the baselines of §4A; the gold standard for PIP-MSE is one long MC3 run per cell. Needs owner/HQ.

#### 2.0.6 Why the old own-β cells are secondary
The owner chose literature-standard designs over our own (HQ_DECISIONS line 908; the suite is S1 and S2 since line 910). BENCH_DESIGN found our suite nonstandard in three ways: our own β with s₀ = 5, no SNR grid, and
not the community's metrics (REPORT §0.5). Our cells are well defined and already used by the theory (A7 Thms 1–4 quote β_min), so they are **kept, as the secondary family**
(REPORT §6.3), reported in the S8 units so readers can place them (§3.6). They also carry the scale rungs (10⁴, 10⁵, 10⁶) that S1 and S2 do not reach.
Status of that family: 10⁴ overlap and science legs, the 10⁵ rung and 7 fits at 10⁶ are done (`LEDGER.md` totals, closed ≈ 6,042 core-h [M]); no further secondary compute is planned in v0.3 **[P]**.

#### 2.0.7 Which engine each suite needs (the theory is about the method as coded)
| arm | what it is | evidence on file |
|---|---|---|
| **T, the theorem-covered method** | the frozen v3.1 core (tag method-v3.1.1, R), and the new C++ engine in law mode with the "bit form" scorer, which equals `v3::Scorer` in bits (`ENGINEERING_SPEC.md` lines 78–81: 0 mismatches of 4,096 at 10⁵ and 10⁶; the stage-level bit-identity gates are in `LEDGER.md`). Law: N = max(2500, n, p), R′ = 4, the coded calibration with escalation (tier 1 = 4× N, H, T) (`results/overlap1e4/OVERLAP_1e4_PREREG.md` §2). The 10⁴ cost anchor of §6A.2 is the C++ law mode; the p = 500/1,000 anchor is the R core | the theorems (RM-0, LT♯, TR, …) are statements about this object |
| **F2, the production engine** | engine tag p1m-freeze-F2: fixed N = 2,500, R′ = 16, bounded calibration (I_max 0), class A. [Δlaw] relative to T | RM-0 holds pathwise for every seed, N_e, R′ and calibration outcome (this plan §0.2). For p ≤ 2,500 and n ≤ 2,500 its N equals v3.1's (`DECISIONS.md` D-1, Theory PSMC-S0). At p = 10⁴, n = 200: 40/40 fits delivered, HPM equal 10/10 data sets, max \|ΔPIP\| 3.8·10⁻⁴, d_H(V,T)/d_H(T,f*) 0.0034–0.0136 (`results/overlap1e4/OVERLAP_1e4_VERDICT.md`, summary 2) [M] |

Which suite needs which:
- **A claim that cites a theorem ("the method the theory covers does X on the standard benchmark") needs T results on the same data sets.** F2 alone supports a claim about the engine, with the 10⁴ overlap as the only agreement evidence; that was at n = 200 and p = 10⁴, **not** at S1 or S2 settings.
- **S1:** F2 on all 16 cells (workhorse for 50 replicates). T bridge on all 16 cells. The p = 500 cells are the closest to T in law (N = 2,500 for both; only R′ and the calibration differ). The p = 5,000 cells differ in N (T: 5,000; F2: 2,500), so they are exactly where the bridge is needed.
- **S2:** F2 on all 120 cells; T bridge on all 120 cells. p = 1,000 gives N = 2,500 for both (as above). At n = 50 and n = 100 T is expected to escalate (§6A.2).
- **[P]** The bridge criteria are those of `results/overlap1e4/OVERLAP_1e4_PREREG.md` §4, re-registered for S1 and S2 before any run.
- An F2 build for Owls (§6A.7) would carry a different floating-point ISA family from the NOTS build, so its bits would not pool with NOTS bits (R10, P6 N2).

### 2.1 SECONDARY. Common data model (random design, matches W3-DIST (RD))
Rows iid. y = Xβ* + ε, ε ~ N(0, σ*²I), σ* = 1, α* = 0. s₀ = 5. Each replicate draws a fresh (X, ε): random design.
Data are **regenerated from the seed by every worker** (counter-based generator, one stream per column chunk) and
checked by hash, so nothing p-wide is stored or shipped. At n = 200, X is 1.6 GB in doubles; at n = 400, 3.2 GB.

### 2.2 SECONDARY. Design families (examples only)
*(SECONDARY since v0.3: the owner chose the literature-standard designs of §2.0 as the primary suite. These cells are kept; why, in §2.0.6.)*
| code | law of x (unit variances) | role | random access for test points |
|---|---|---|---|
| IND | iid N(0, 1) | no correlation: the cleanest feasibility case | yes |
| AR | Toeplitz 0.6^{\|j−l\|} (AR(1) recursion along the columns) | metric-local (UNI-0 example), the **primary** design | yes (Markov bridge on any sorted subset) |
| BLK | blocks of 20 consecutive columns, within-block correlation 0.5 (x_j = √.5 f_b + √.5 e_j) | grouped proxies, (V)/(L) with a non-trivial Q | yes |
| FAC (C9) | one factor, cs ρ = 0.3 | D1 only, at 10⁴, contingent | yes |

Truth: S₀ spread evenly (k-th truth at ⌊(k − ½)p/5⌋, shifted so that no two truths share a BLK block).
β*_{S₀} = a·(1.0, −0.8, 0.9, −0.7, 0.6).
- **Strong** (a = 1, β_min = 0.6): at n = 200, β_min√n = 8.5 against √(2 log p) = 5.3 at 1M.
- **Weak** (a = 0.6, β_min = 0.36): at n = 200, β_min√n = 5.1. This sits at the detection boundary at n = 100–200, so P(HPM = S₀) rises
  visibly with n and the PIPs take intermediate values (needed for PIP calibration).

Optional arms, each at 10⁴ only:
- **MIS** (W3-MISR): one sixth true variable, independent of X, with β = 0.8, omitted from X. Target = the projected
  model = S₀.
- **ADJ**: AR with two adjacent truths, a (V)/(L) stress case.

### 2.3 SECONDARY. Ladder and gates (n, signal, replicates)
*(SECONDARY since v0.3. The rungs 10⁴, 10⁵ and 10⁶ run on these own-β cells; S1–S3 stop at p = 5,000. Status of the ladder is in `LEDGER.md`.)*
p = n^A with A = log p / log n. At 1M: A = 2.6 (n = 200), 2.3 (n = 400).

| rung | p | designs × signal | n | reps | R′ | notes |
|---|---|---|---|---|---|---|
| S0 | ≤ 2·10⁴ | PROD-H 24 units + supplementary; 5k/10k/20k setups | as recorded | — | 4 | engine gates only (§5.2) |
| A1 law bridge | 10⁴ | AR strong | 200 | 10 + 10 | 4 vs 16 | v3.1 law (N = p = 10⁴, R′ = 4) against fixed N = 2,500 (R′ = 16) on the **same datasets** |
| A2 main | 10⁴ | AR strong + weak; IND, BLK strong | 100, 200, 400, 800 (AR); 100, 200, 400 (IND, BLK) | 10 (AR strong), 5 (others) | 16 | n-trend for C2–C5 |
| A3 partition | 10⁴ | AR, BLK strong | 200 | 10 | 16 | exact complete linkage against the 1M partition rule, same data: π₀(S₀) and outcomes (OD-5) |
| A4 extras | 10⁴ | MIS, ADJ, FAC (if D1 says so) | 200, 400 | 5 | 16 | optional |
| B | 10⁵ | AR strong (n-trend), IND strong | 200, 400 (AR); 200 (IND) | 5 | 16 | first rung needing G1–G7 |
| C | 10⁶ | AR strong (primary); ADJ-OPP; AR weak (v0.2) | 200; 400 (AR, Full tier only) | 3 / 1 / 1 | 16 | rep 1 is the pilot |

Gates (each needs HQ approval with measured numbers; a failed gate returns to HQ and the owner):
- **G-A (enter rung A).** All of:
  - S0 bit-identity passes;
  - the fixed-N mode with N = max(2500, n, p), R′ = 4 reproduces revision D bit for bit at p ≤ 20k;
  - the DIST evaluator matches a brute-force Monte Carlo to 3 significant digits on 20 fixtures;
  - two pilot fits at 10⁴ complete within 1.5× the cost model.
- **G-B (enter 10⁵).** All of:
  - rung-A completion ≥ 95% (no unexplained non-delivery);
  - measured core-h per fit ≤ 1.5× model;
  - memory ≤ the model;
  - E2 escalation frequency recorded (input to OD-2);
  - one 10⁵ pilot completes at ≤ 1.5× model, peak RSS < 50% of a node.
- **G-C (enter 10⁶).** All of:
  - rung B completion ≥ 90%;
  - the 1M cost extrapolated from the 10⁵ fits (per-step µs, T, I) fits the approved budget;
  - island checkpoint/restart tested by a forced kill at 10⁵;
  - G3 partition implemented and T-PART answered.
  - The 1M pilot fit is then submitted alone.
  - **Kill rule:** if the pilot's calibration exceeds 2× its modelled core-h, or any island exceeds 2× at 50% progress,
    stop and return.
- **G-C2 (1M main).** The pilot completes. Its per-fit cost re-sizes the remaining 1M replicates within the budget.

## 3. Metrics (per fit, all saved in a flat per-fit record plus p-wide binaries)

### 3.1 Selection (C2, C3, C6)
- Reported HPM = S₀; MPM = S₀; Hamming distance, TP/FP of HPM and MPM.
- Outcome class as in P6: posterior, F(HPM) > F(S₀); or search, F(S₀) > F(HPM), with F(S₀) scored directly and checked
  against the ledger.
- Provenance (phase, mechanism, φ) at which S₀ became the running HPM; `local_certified`; certified-screening
  coverage; LS0 moves and first scoring scan; start-mode size.
- **Exact log π₀(S₀) and π₀ of the lattice {S₀ ⊆ T ⊆ Q}** from the start tables (C3). This is free, and it gives a direct
  check of START/START2 rates.

### 3.2 PIP (C4)
- sup_{j∉S₀} PIP and min_{j∈S₀} PIP for pip_primary (equal-weight) and PIP_Z; per-island spread (sd over islands, max).
- Brier score; pooled reliability curve (weak-signal arm), with PIPs binned 0.05–0.95.
- Count of j ∉ S₀ with PIP > 0.1 and > 0.5.

### 3.3 Distribution / predictive (C5; the W3-DIST metrics)
Let d_H²(f, g) = 1 − ∫√(fg) (the affinity form of STATEMENT §0; [SL]'s d² = 2d_H²). All three coded-output objects of
DIST-C are computed from the returned output plus the data, as STATEMENT §2 prescribes:
- **Π̂^H** = Π(· | S = HPM, D_n); **Π̂^M** = Π(· | S = MPM, D_n);
- **Π̂^𝒯** = the store BMA over the merged `top_store` with weights e^{F(S)}. It is truncated at relative weight 10⁻¹²
  and the dropped mass is reported. At 1M the store holds 4·10⁷ models, but the weight sits on a handful.

Then:
- **Oracle reference** Π(· | S₀, D_n): the DIST-3 benchmark. Each output is reported as a ratio to the oracle.

For each object:
1. **Plug-in Hellinger, closed form.** Plug in the posterior mean (θ̄, v̄) and raw coefficients b. For Gaussian ν_x with
   known Σ, Δ(x) ~ N(m, s²) with s² = (b − β*)ᵀΣ(b − β*). Then
   d_H² = 1 − √(2√(vσ*²)/(v + σ*²)) · (1 + 2a s²)^{−1/2} exp(−a m²/(1 + 2a s²)), with a = 1/(4(v + σ*²)).
   This is exact: no test set and no Monte Carlo error.
2. **Posterior law of d_H** under the object: 10⁴ conjugate draws of (θ, v), with d_H computed in closed form per draw.
   - Report its quantiles.
   - Report the tail curve ε ↦ Π̂(d_H > ε) on ε² ∈ {c·log n / n : c = ½, 1, 2, 4, 8}. This is the DIST-1 / DIST-C statement
     without having to choose C.
3. **Predictive-density Hellinger** d_H²(f̄, f*), where f̄ is the object's posterior predictive density (Student-t in y
   given x, mixed over models for Π̂^𝒯). Computed with 4,000 x draws × 64-node Gauss–Hermite in y. Same draws used for the
   **KL / log-score** E_{f*} log(f*/f̄).
4. **Prediction error** E_x(μ̂(x) − μ*(x))² (closed form), plus test-set MSE and mean log predictive density on
   10⁴ fresh rows. The test rows need only the support columns, so they are cheap at 1M.
5. **Store-mass diagnostic for P-STORE / P-HIT:** π̂(𝒯) = Σ_{S∈𝒯} e^{F(S)} / Ẑ (a ratio of estimates; also a lower bound
   on Z, cross-checking log Ẑ), and whether S₀ ∈ 𝒯.

Decay in n:
- At fixed p (10⁴: n = 100–800; 10⁵: 200, 400; 10⁶: 200, plus 400 in the Full tier), report median and quartiles over
  replicates of n·d_H² and of n·d_H² / (s₀ log p).
- Report the fitted slope of log d_H² on log n, with a bootstrap CI over replicates.
- Expected shape: store-BMA ≲ s₀ log p / n (DIST-1); plug-in → s₀/n under selection (DIST-3).
- Rung A also gives a p-at-fixed-n comparison (10⁴ / 10⁵ / 10⁶ at n = 200) of n·d_H² / log p.

The same predictive metrics are computed for every competitor that returns a predictive (§4), so C5 also has a
comparison.

### 3.4 Evidence and merge diagnostics (C7)
- log Ẑ, log Ẑ_r; σ̂ and robust σ̂ (1.4826·MAD); max − median; R_eff/R′ and max W_r; max_j |PIP_Z − PIP_eq|.
- `log_Z_lower95`; log Ẑ against log Σ_𝒯 e^F.
- T, I, tier and escalation, the trigger that fired, per-stage ESS, distinct counts.

### 3.5 Cost
- Wall time per phase (setup, calibration, census, islands, merge, tail, LS0); thread-h and billed core-h (sacct CPUTimeRAW).
- Peak RSS per process, private and shared (mmap); bytes written and read.
- Per-step µs by phase; `score_counts$logical` (and `fresh` as OD-3 rules); node type (sapphirerapids only).

### 3.6 Standard metrics for S1 and S2, and the real-data rule (v0.3, S3 removed in v0.4; REPORT §4, §6.1 S6–S8)
Computed for both our arms (T and F2) and for every competitor, by one evaluator. The §3.1–§3.5 metrics stay as extras (REPORT §6.1 S6 keeps sup-PIP error, Brier/reliability, Hellinger and the evidence metrics).
- **Selection (truth known):** TPR and FDR of the reported model (HPM) and of the MPM; exact recovery P(Ŝ = S₀); FP and FN counts; model size. Each with a Monte Carlo standard error over the data sets of a cell.
- **Posterior accuracy:** PIP-MSE against a long-run gold standard (REPORT §4: Liang 2022/2023, Staerk 2024). **[P]** The gold standard is a long MC3 run, produced for the efficiency block E only (§2.0.5), not for every data set.
- **Efficiency:** time-standardised relative ESS r_{A,B} = (ESS_A/t_A)/(ESS_B/t_B) of the PIP estimates, from the PIP variance over 50 independent runs, relative to the add–delete–swap baseline (REPORT §4; block E).
- **Estimation and prediction:** ℓ₂ error of β̂ (under HPM, MPM and the store BMA); out-of-sample prediction error (closed form, §3.3 item 4); for S2 the relative risk and relative test error of Hastie et al. (PAPERS.md "Hastie2020").
- **Cost:** runtime and billed core-h per fit (§3.5).
- **SNR three ways, every cell (REPORT §6.1 S8):** ν = Var(xᵀβ)/σ², PVE = ν/(1+ν), and β_min/(σ√(log p/n)). This applies to the secondary own-β cells too, so that all four signal conventions of REPORT §2 can place them.
- **Real data (not truth-known) is for posterior accuracy and prediction only** (HQ_DECISIONS line 908). On real data we report PIP-MSE against a gold standard, PIP calibration against the gold standard,
  out-of-sample prediction error and log predictive density, and runtime. We make **no** TPR, FDR or exact-recovery claim on real data, because S₀ is unknown there.
  **[P] needs owner/HQ:** which real data sets (REPORT §6.1 S5: PCR mouse n = 60, p = 22,575; Schäfer–Chopin's Boston/concrete/protein; Tecator; and the riboflavin fits already running on Owls, n = 71, p = 4,088, `HANDOFF_V2.md` §1).
  The semi-real design S4 (real X + synthetic β) is **not** part of the owner's suite (S1 and S2) and is left out until the owner or HQ rules.

## 4. Competitors that can actually run at each p
*(This table is for the secondary 10⁴–10⁶ rungs. The competitors for S1 and S2 are in §4A.)*

Every competitor runs on the **same regenerated datasets**, with default or CV tuning fixed before the runs. Selection
and predictive metrics are computed by the same evaluator.

| method (package) | type | 10⁴ | 10⁵ | 10⁶ (n = 200) | predictive object |
|---|---|---|---|---|---|
| Lasso, 10-fold CV, λ_min and λ_1se (glmnet / biglasso) | penalised | yes | yes | yes (X 1.6 GB; biglasso memory-maps) | N(xᵀb̂, σ̂²_CV) |
| MCP / SCAD (ncvreg / biglasso) | penalised | yes | yes | yes | same |
| L0Learn (L0L2, CV) | best-subset approx. | yes | yes | likely (UNVERIFIED memory/time) | same |
| SuSiE (susieR, L = 10) | variational Bayes, joint | yes | yes | yes (O(Lnp) per iteration, about 2·10⁹ flops) | mixture of single-effect posteriors |
| varbvs | variational spike-and-slab, joint | yes | yes | yes | variational posterior |
| BAS (MCMC) or mombf/modelSelection | model-space MCMC | yes | marginal (time) | no | BMA |
| millipede / wTGS (CPU) | model-space MCMC (Jankowiak 2023, 7.5·10⁵ on GPU) | yes | yes (slow on CPU) | only with a GPU (none budgeted) | BMA |
| SIS (d = n / log n) → exact BVS on survivors | screen-then-select, category (b) | yes | yes | yes | BMA on the screened set |
| SMC-BVS v3.1 serial (law reference) | ours, old law | yes (A1) | no (N = p) | no | DIST-C objects |

Cost: under 10 core-h per dataset for all the penalised and variational methods at 1M. BAS and millipede are restricted
to 10⁴–10⁵. Budgeted at about 1–2% of the total.

## 4A. Competitors for S1 and S2 (v0.3; S3 column removed in v0.4; REPORT §6.1 S9)
All run on the same data sets as our arms, with tuning frozen before the first run and the same evaluator (risk R14). Runtime comparisons are only valid between jobs on the same hardware class.
| group | methods (code) | S1 | S2 | note |
|---|---|---|---|---|
| frequentist and variational | glmnet (lasso, 10-fold CV, λ_min and λ_1se), ncvreg (MCP/SCAD), L0Learn (L0L2, CV), SuSiE (susieR, L = 10), varbvs | all | all | REPORT S9: "already standard" |
| best-subset set (S2 only) | forward stepwise, relaxed lasso, and best subset through L0Learn (Hastie et al. also use Gurobi MIO; no licence is assumed) | – | all | PAPERS.md "Hastie2020"; their R code is public (github.com/ryantibs/best-subset) |
| Bayesian MCMC baselines | add–delete–swap MC3 (baseline), ASI (Griffin 2021), PARNI (Liang 2022), wTGS (Zanella–Roberts 2019); public code | all | **[P] not run** | REPORT S9; the Griffin/Liang/Zanella code is public (REPORT S1 "Why"). **[P]** S2 is the frequentist frame; MCMC there only if owner/HQ ask |
| SMC precedent | Schäfer–Chopin 2013 SMC | **[P]** if the scripts can be obtained | – | REPORT S9 |
Block E also runs the four MCMC baselines (50 runs each) for r_{A,B}. Cost: §6A.5.

## 5. Engineering prerequisites: gap list from W3-SCALE revision D to a 1M-ready engine ("v4")

Baseline: revision D (6866f57) is bit-identical to v3.1 on PROD-H. It is still Θ(p²) in memory, serial, and has a 4-island
in-process layout. Sizes are agent-days (A-d) of an Opus lead plus a review, and NOTS core-h of gates.
"Owner" means who builds: **SCALE** = W3-SCALE leg C team (engine owner); **EXP** = this department; **TH** = a theory ticket;
**HQ** = decision.

| id | item | tag | why at 1M | size | owner |
|---|---|---|---|---|---|
| G1 | **Gram-free canonical scorer.** G_{S,j} from X columns by lane-parallel *sequential* dot products (same summation order as `data_init`, v3_score.h:45–53); per-particle factor cache. | [OP-bit] (v0 local check: identical bits) | the Gram is 8 TB at 1M | 4 A-d, gate 20 core-h | SCALE |
| G2 | **Streamed correlation tiles** for the neighbour graph (r_n threshold, partial selection, O(pB) memory, threaded) and for duplicate components (now R `crossprod`, O(np²) in R). | [OP-bit] | 2·10¹⁴ flops at n = 200, about 1–2 node-hours; no p² array | 3 A-d | SCALE |
| G3 | **Block partition above about 150k.** Exact complete linkage needs the full distance matrix (v3_blocks.h:54: dense r and dist, 16p² bytes; 4 TB condensed at 1M). **v0.2 rule:** complete linkage truncated at height 1 − τ_n on the sparse graph {\|r\| ≥ τ_n}; the coded top-down cut; next-fit packing by minimum index (the v0.1 component rule fails on AR(0.6)). | **[Δlaw]** (π₀ changes); O8 | hard memory wall | 5 A-d + TH | SCALE + **TH T-PART** |
| G4 | **Tables** by depth-first search with a bordered Cholesky; threaded over blocks; compact storage (drop `logm_tab` / `route_tab` after HPM ingestion); one read-only mmapped file shared by all islands on a node. | [OP-bit] (v0: 5–8×, identical) | ≈ 2·10⁸ table codes at 1M, n = 200 (§6.1); ≈ 7 GB | 3 A-d | SCALE |
| G5 | **No O(p) work per elementary step.** In-place flip and undo (no `tmpQ = P` bitset copy, v3_engine.h:120,131,152,172); `nth_nonmember` by a word-prefix index; O(p) Fisher–Yates kept (it is law). | [OP-bit] | a 125 KB copy per step would cost about 10× the score | 2 A-d (part done in B1; verify) | SCALE |
| G6 | **Score-cache capacity decoupled from p.** 500p entries is 5·10⁸ at 1M (30–50 GB per island); fixed capacity instead. | [OP-bit] except `fresh` | memory | 1 A-d | SCALE, after **OD-3** |
| G7 | **Compact stores and external merge.** Top store 40p + 1 = 4·10⁷ models per island as flat arrays; streaming top-c merge of R′ stores from disk; leader stores the same. | [OP-bit] | about 2–3 GB per island; 6·10⁸ entries at R′ = 16 | 3 A-d | SCALE |
| G8 | **In-island threads.** (a) Speculative batched scoring of upcoming Gibbs labels at fixed S, with cache, ledger and uniforms committed in serial order. (b) Fallback: counter-based per-particle streams (O5). | (a) [OP-bit], expected 5–10× on 16 threads, UNVERIFIED; (b) [OP-law] | wall time only: a serial 1M island takes about 70 h, a calibration rebuild about 15 h | (a) 5 A-d, (b) 3 A-d | SCALE |
| G9 | **Process-parallel islands J0–J4** (DESIGN_v1 §4.1 contract): manifest, workers as a Slurm array, merge and tail, statuses; **checkpoint/restart at stage boundaries** (stream positions, particles, ledger). | [OP-bit] for the contract at R′ = 4 | 24 h task limit; R′ = 16 | 6 A-d, gate 40 core-h (CP2 estimate) | SCALE |
| G10 | **Fixed-N mode** (N_isl, H, R′ decoupled from p) + the escalation policy (OD-2) + census rule (O3) + flags for R′ ≠ 4 (O20). | [Δlaw] / [Δ𝒞] | N = p is infeasible | 3 A-d + TH (O4 restatements) | SCALE + HQ |
| G11 | **Large-p I/O.** C++ preprocessing (standardisation now runs R `apply` over p columns); keep n·p < 2³¹ for R/Rcpp int indexing (n ≤ 2,000 at 1M); binary X input; binary outputs for p-wide arrays and stores (no R lists of 4·10⁷ models); a memory preflight rewritten for the new layout (the present model refuses at about 19k at 8 GiB). | [OP-bit] for outputs | R overhead, preflight refusal | 4 A-d | SCALE |
| G12 | **Threaded local search / LS0 scans.** One scan is p + k(p − k) ≈ 6·10⁶ models at k = 5 and 10⁸ at k = 100; deterministic reduction order; the B4 preflight charge re-modelled at 1M. | [OP-bit] | serial tail of the merge | 2 A-d | SCALE |
| G13 | **Data generator** (counter-based, all designs, hash) + **DIST evaluator** (§3.3) + **competitor harness** (§4) + per-fit record schema + analysis scripts (rule-15 review). | n/a | — | 6 A-d | **EXP** |
| G14 | **Gates.** S0 bit-identity (PROD-H 24 + supplementary + 5k/10k/20k setups) for every [OP-bit] item; distributional equivalence tests for G3/G8(b)/G10. | — | — | 2 A-d, about 150 core-h | SCALE + EXP |
| T-PART | Theory check: do START/START2/RM2/(V) use any property of the coded partition beyond "blocks of size ≤ B, built from \|r\|"? If yes, what is the minimal property the new rule must keep? | — | G3 changes π₀ | ≤ 1 Opus leg | **TH** |
| T-N | O4: restate TH01(e)(f)(i), TH06, TH08 for general (N, R′); confirm that RM-0, LT♯, TR, D need nothing. | — | fixed N | ≤ 1 Opus leg (HQ_NOW: "short Opus note") | **TH** |

Total: about 46 A-d of engine work, about 6 A-d in EXP, 2 theory legs. With three parallel builders (two SCALE, one EXP)
this is 3–4 calendar weeks including reviews. G1, G2, G4, G5 and G12 are the efficiency core the owner asked for. G8(a) is the one large
UNVERIFIED speed-up: without it a 1M fit still runs, through checkpointed serial islands, but takes about 10 days of
wall time (§7).

## 6. Cost model and budget (SECONDARY own-β cells; v0.3/v0.4: the compute of the primary suite S1 and S2 is §6A)
*(§6.2–§6.4 are the v0.2 planning numbers for the secondary ladder. The actual spend to date is in `LEDGER.md`: closed ≈ 6,042 core-h of the ≈ 28.3k envelope [M].)*

### 6.1 Inputs (measured unless marked)
- Island (DESIGN_v1): t = N(p + 16)(T + 21.6)·c µs. Formula c = 1 µs. Measured effective c ≈ 2 at 10k (0.70 h for a 0.36 h formula) and
  ≈ 1.1 at 20k (revision D, n = 200).
- Calibration, tier 0 with H = 512 under fixed N: about (0.82·I + 0.5) island-equivalents at N = 2,500.
  Measured 5.9–6.7 h at 10k–20k (I = 14–15).
- A fit with R′ = 16 and I = 12 is therefore about 26.3 island-equivalents.
- **Block sizes (Owls, 2026-11-15, core at daa08a3, iid/AR designs).**
  - n = 200 (B = 14): mean block size about 9; about 210 table codes per column.
  - n = 1,000 (B = 16): about 2,200 codes per column (AR 0.5 at p = 5k: 1,080).
  - So at 1M: about 2·10⁸ codes at n = 200 against about 2·10⁹ at n ≥ 256. This is one reason n = 200 is the 1M default (OD-6).
- Assumed (UNVERIFIED): T ≈ 30 and I ≈ 12 at every p (the cap ℓ = 20 at 1M; I = 20 adds 25%); c(n) ∝ 1 + n/400 for the
  Gram-free scorer, i.e. 1.5× at n = 400 and 2.25× at n = 800 relative to n = 200; no escalation.
- Billing: 2 CPUs billed per single-thread task (as in P6). Threaded tasks: billing = allocated CPUs × wall, so
  thread-efficiency losses count (REQUESTS R2).

### 6.2 Per-fit planning cost (billed core-h; c = 2 µs, pessimistic; v4 target c ≈ 1.2 gives ×0.6)
| p | n = 100 | 200 | 400 | 800 | with E2 escalation (tier 1) |
|---|---|---|---|---|---|
| 10⁴ | 32 | 38 | 51 | 75 | ≈ ×4 |
| 10⁵ | — | 377 | 509 | — | ≈ ×4 |
| 10⁶ | — | 3,770 | 5,090 | — | ≈ ×4 (infeasible within any tier below) |

A v3.1-law fit at 10⁴ (N = 10⁴, R′ = 4, H = 2,048): ≈ 82 core-h.

### 6.3 Budget per stage (billed core-h, pessimistic c; the target c removes about 40%)
| stage | Minimal | Standard (rec.) | Full |
|---|---|---|---|
| S0 engine gates + benchmarks | 300 | 300 | 300 |
| A1 law bridge | 600 (5 + 5) | 1,200 (10 + 10) | 1,200 |
| A2 main | 600 (AR strong, n = 100–400, 5 reps) | 4,150 | 6,340 (all cells 10 reps) |
| A3 partition, A4 extras | 100 | 400 (A3) | 1,700 (A3 + MIS + ADJ + FAC) |
| Competitors (all rungs) | 100 | 300 | 500 |
| B (10⁵) | 1,100 (AR n = 200, 3 reps) | 6,300 | 8,200 (+ BLK n = 200) |
| C (10⁶) | 7,500 (AR n = 200, 2 reps) | 18,900 (AR 3 + IND 2, n = 200) | 34,100 (+ AR n = 400 × 3) |
| **total** | **≈ 10.4k** | **≈ 31.6k (38k with 20% contingency)** | **≈ 52.3k** |

Levers, largest first:
- R′ = 8 at 1M: −30% of rung C.
- The v4 target per-step cost: −40% overall.
- Dropping IND at 1M: −7.5k.
- Fewer A2 cells.

The plan is infeasible if E2 escalation fires at 1M under the coded rule (OD-2).

### 6.4 Wall time (per fit; replicates in parallel; 150-task limit not binding)
| p | serial islands, checkpointed | with G8(a) at 8× on 16 threads |
|---|---|---|
| 10⁴ | ≈ 8 h (calibration 6–7 h + islands 0.7 h) | ≈ 1 h |
| 10⁵ | ≈ 1.3 days (calibration ≈ 1 day: 12 rebuilds × 1.5 h; islands 7 h) | ≈ 4 h |
| 10⁶ | calibration ≈ 7 days (12 rebuilds × 15 h, diagnostics in parallel) + islands 72 h (3 chained jobs) ≈ 10–11 days | ≈ 1.5 days |

## 6A. Compute estimate for the primary suite S1–S3 (v0.3, 2026-11-24)

Plan only; nothing was run. Units: **NOTS billed core-h** = allocated CPUs × elapsed (`LEDGER.md` rules). A single-thread NOTS task is billed 2 CPUs (§6.1; `results/RERUN_2400_VERDICT.md`: 86.3 elapsed = 172.6 billed [M]).
Labels as in the v0.3 update ([M] measured, [D] derived, [X] extrapolated, [P] PROPOSED). All sums were computed by one script, `results/s1s3_compute_estimate.py` (uncommitted; it prints every table below; the formulas are in §6A.2).

### 6A.1 Fit counts (cells × replicates × methods)
Central design: R_F = 50 data sets per cell for F2; a paired bridge of R_T = 10 of them per cell for T; block E (§2.0.5). All counts **[D]** from §2.0.
| suite | cells | data sets (50/cell) | F2 fits | T bridge fits (10/cell) | frequentist/VB fits (5 methods) | MCMC-baseline runs (4 methods) |
|---|---|---|---|---|---|---|
| S1 | 16 | 800 | 800 | 160 | 4,000 | 3,200 |
| S2 | 120 | 6,000 | 6,000 | 1,200 | 30,000 | 0 [P] |
| S3 | 32 [P] | 1,600 | 1,600 | 320 | 8,000 | 6,400 |
| E (2 cells × 50 seeds, 1 data set each) | 2 [P] | 2 | 100 | 0 | – | 400 |
| **total** | **170** | **8,400** | **8,500** | **1,680** | **42,000** | **10,000** |

**Our SMC fits: 8,500 + 1,680 = 10,180.** The other replicate choices (same cost model, §6A.6): R_F = 20 gives 5,140 SMC fits; R_F = 100 gives 18,580; T on every data set (R_T = 50) gives 16,900.

### 6A.2 Measured inputs, and the scaling assumption
| input | value | source |
|---|---|---|
| T at p = 10⁴, n = 200, 20 fits (law mode, N = 10⁴, R′ = 4, coded calibration) | **44.0** billed core-h per fit on average (879.08/20); tier 0 (17 fits) mean 33.2, range 2.3–51.5; tier 1 (3 fits, N_final = 40,000) mean 104.9, max 143.96 [M] | `results/overlap1e4/OVERLAP_1e4_VERDICT.md` §4 |
| T escalation incidence at 10⁴, n = 200 | 3 of 20 (15 %) [M] | same, §4 |
| T (R core v3.1) at p = 500 and p = 1,000, n = 200 (121 PROD-H data sets, c = 1) | mean wall 833 s and 1,877 s on one core, i.e. 0.46 and 1.04 billed core-h per fit [D from M] | `rerun2400/verdict/per_fit.csv` (new = v3.1, runtime_new), `results/RERUN_2400_VERDICT.md` |
| T escalation at small n | P6: escalated in 103/105 (n = 50, p/n = 5–10) and 16/16; a cs design at n = 100, p = 1,000 took 16 h, always escalated [M, quoted, not re-read] | `RIBOFLAVIN_ETA` (results/RIBOFLAVIN_ETA.md §3) and risk R13 below |
| F2 at p = 10⁴, N = 2,500, R′ = 16, I_max 0, n = 100–800, 170 fits | mean **1.38** core-h per fit; per-class means 1.07–2.32 [M] | `results/precision1e4/leg_readback/science/science_per_fit.csv` |
| F2 at 10⁵ and 10⁶, N = 2,500 | 29.6 and 26.1 (10⁵, n = 200); 346–482, mean 405 over 5 fits (10⁶, n = 200) [M] | `results/rung1e5/RUNG_READBACK.md` §7; `results/gc1m/GC_1M_BLOCK_SUMMARY.md` |
| F2 at N = 10⁴ against N = 2,500 | ×3.3 at 10⁴ (18.07 against 5.3–5.6, R′ = 64); ×2.7 at 10⁵ [M] | `results/vn_minileg/MINILEG_READBACK.md` §3, `vn_minileg/twin_costs.csv`; RUNG_READBACK §7 |
| Owls against NOTS, same fit | Owls = 1.93× slower per core [M] | `results/RIBOFLAVIN_ETA.md` §2 |
| riboflavin, R core v3 on Owls, p = 4,088, n = 71, one core | ≥ 88 h per fit (the 11-18 units ran ≈ 88 h and died in the 11-22 reboot; no fit exists; relaunched 11-22, ETA ≈ 11-27); 8.1 µs per move against 1.0–1.6 on NOTS synthetic data [M] | `HANDOFF_V2.md` §1; `MAIN:Docs/Experiments/realdata_riboflavin/README.md` status line; `results/RIBOFLAVIN_ETA.md` §2, §5 |

**Scaling assumption, stated once.**
1. **T (per fit, NOTS billed):** cost = A · (N_law · p / 10⁸) · f_n · f_esc, with **A = 44.0** [M, row 1] and **N_law = max(2500, n, p)** (the v3.1 law, PREREG §2). So cost ∝ p for p ≤ 2,500 and ∝ p² above. This is one time-unit per particle-move (∝ N·p per round).
   **Check [D]:** the model gives 0.55 at p = 500 and 1.10 at p = 1,000 against the measured 0.46 and 1.04, within 20 %; between p = 1,000 and 10⁴ it matches the slope ≈ 1.6 that RIBOFLAVIN_ETA §5 quotes from the plan. The model is **anchored at 10⁴ and validated only down to p = 500–1,000; p = 5,000 is interpolated [X]** (no T fit at p = 5,000 is on file).
2. **n-factor f_n [X]:** 1.0 for n ≤ 200. For n = 500 and 1,000 the central value is 1.25 (low 0.8, high (1 + n/400)/1.5 = 1.5 and 2.33). Basis: the F2 arm is flat in n at p = 10⁴ (class means 1.1–1.7 for n = 100–800, science_per_fit.csv [M]); the v0.2 law 1 + n/400 was refuted for F2 (LOG 2026-11-19 14:54, S7: "n = 400 is CHEAPER than n = 200"). **T at n > 200 has no measurement.**
3. **Escalation factor f_esc:** relative to the 10⁴ mixture mean A: tier 0 = 0.75 and tier 1 = 2.38 [D from row 1]. S1: central 1.0 (the measured mix, 15 % escalated), low 0.75 (none), high 1.40 (40 % escalated). **[P]** S2 n = 50: 100 % escalated (central 2.38; low 1.57 = 50 %; high 3.27 = the measured tier-1 maximum). S2 n = 100: central 1.57 (50 %), low 1.0, high 3.27. S3: central 2.38, low 1.57, high 3.27.
4. **A-multiplier** (model error): low 0.7, central 1.0, high 1.6 [P].
5. **F2 (per fit):** c_F2(p) = max(0.10, 1.4 · p/10⁴) core-h at N = 2,500, R′ = 16, I_max 0, for any n in 100–1,000 and any S1–S3 cell. Anchor: 1.38 at p = 10⁴ [M]. Measured growth 10⁴ → 10⁵ → 10⁶ is ×20 and ×14, i.e. an exponent ≈ 1.2–1.3 [D]; **below 10⁴ the exponent is set to 1 and the 0.10 floor is a guess [X]**. Low ×0.5, high ×3 [P] (harder S2/S3 grids, longer stage counts; cost follows the stage count T, RUNG_READBACK §7).
6. **N for F2 [P]:** 2,500 (equal to T's N for p ≤ 2,500). N = 10⁴ would multiply the F2 cost by 2.7–3.3 [M] (F2 total 1.9k → 5.0–6.2k) **[D]**.
7. **Owls conversion [D]:** a single-thread job costs Owls core-h = (NOTS billed / 2) × 1.93 ≈ 0.97 × NOTS billed. For F2's threaded islands, Owls core-h = 1.5 × NOTS billed (range 1.0–1.93; at 10⁶ engine time was 0.71 of billed island core-h, GC summary) **[P]**.

### 6A.3 Per-fit planning cost, central (NOTS billed core-h) **[D]**
| cell class | T (law N) | F2 | T / F2 |
|---|---|---|---|
| S1, p = 500 (N = 2,500; n = 500 or 1,000) | 0.69 | 0.10 | 7 |
| S1, p = 5,000 (N = 5,000) | 13.8 | 0.70 | 20 |
| S2, n = 50, p = 1,000 (N = 2,500; escalated) | 2.62 | 0.14 | 19 |
| S2, n = 100, p = 1,000 (half escalated) | 1.73 | 0.14 | 12 |
| S3, p = 500 (escalated) | 1.64 | 0.10 | 16 |
| S3, p = 5,000 (N = 5,000; escalated) | **32.8** | 0.70 | 47 |

### 6A.4 Totals by suite and engine (NOTS billed core-h) **[D]**; central design of §6A.1
| suite | F2 | T bridge | competitors (§6A.5) | **total central** | low | high |
|---|---|---|---|---|---|---|
| S1 | 320 | 1,155 | 186 | **1,661** | 624 | 5,671 |
| S2 | 840 | 2,610 | 60 | **3,510** | 1,631 | 9,666 |
| S3 | 640 | 5,507 | 372 | **6,519** | 2,094 | 21,940 |
| E | 70 | – | 53 | **123** | 56 | 422 |
| **total** | **1,870** | **9,272** | **671** | **11,813 (≈ 11.8k)** | **4.4k** | **37.7k** |

- **By engine (central):** T 9.3k (78 %), F2 1.9k (16 %), competitors 0.7k (6 %). T needs the **theorem-covered R/law-mode method** for any theorem-cited claim; F2 (the engine) carries the replicate count (§2.0.7).
- **Low and high are scenario bounds with every assumption of §6A.2 set at its extreme at once, not confidence intervals.** The central estimate is the number to plan with; **the high scenario does not fit the envelope** (§6A.8).
- **S3 is the cost driver:** 59 % of the T bridge, from p = 5,000 (N = 5,000, escalation) alone: 160 T fits × 32.8 = 5.2k [D].

### 6A.5 Competitor cost, separately (rough, no measurement on file) **[P]**
Assumed per data set: frequentist and VB set (5 methods) 0.1 core-h at n = 1,000, p = 5,000, scaling ∝ n·p with a floor of 0.01; the four MCMC baselines 0.33 core-h at p = 5,000 (≈ 5 min each at a fixed iteration count), ∝ p with a floor of 0.05.
The MCMC baselines run on S1, S3 and block E only. Central **0.67k** (S1 0.19k, S2 0.06k, S3 0.37k, E 0.05k), range 0.27k–2.7k (×0.4 to ×4). This is about 6 % of the central total, above the 1–2 % that §4 assumed for the secondary rungs.
**Calibrate on 10 data sets before relying on it.** The competitors are R/Python single-thread jobs and are cheap enough for Owls (§6A.7).

### 6A.6 Replicate alternatives and levers (central cost model, NOTS billed core-h) **[D]**
| R_F | R_T | SMC fits | F2 | T | competitors | total |
|---|---|---|---|---|---|---|
| 20 | 10 | 5,140 | 0.8k | 9.3k | 0.3k | 10.4k |
| **50** | **10** | **10,180** | 1.9k | 9.3k | 0.7k | **11.8k** |
| 100 | 10 | 18,580 | 3.7k | 9.3k | 1.3k | 14.2k |
| 50 | 20 | 11,860 | 1.9k | 18.5k | 0.7k | 21.1k |
| 50 | 50 (T on every data set) | 16,900 | 1.9k | 46.4k | 0.7k | 48.9k (does not fit) |

Levers, largest first: T bridge at S3 p = 5,000 from 10 to 5 per cell (−2.6k); S3 SNR levels from two to one (halves S3, −3.3k); S2 T bridge from 10 to 5 per cell (−1.3k); F2 at N = 2,500 (not 10⁴) is already assumed.
**A calibration pilot before any batch [P]:** 5 T fits at S3 p = 5,000 (≈ 164), 5 at S2 n = 50 (≈ 13) and a few dozen F2 fits ≈ **190 core-h [D]**, to replace the [X] and [P] assumptions above (T at p = 5,000, f_n, escalation at n = 50 and under compound symmetry, the F2 floor). Under the ledger rules this is within the exploratory ≈ 200 core-h standing authority, but nothing starts during the break.

### 6A.7 By machine: NOTS against Owls
Owls: ≤ 16 cores, nice 19; the host is shared (load 20–29 from other users; 5 cores held by the riboflavin units until ≈ 11-27 [M, RIBOFLAVIN_ETA §4, HANDOFF_V2 §1]). **[P]** Usable capacity ≈ 16 cores × 24 h × 0.6 ≈ 230 core-h per day [D].
| work | NOTS billed, central (low–high) | Owls core-h, central (low–high) | where |
|---|---|---|---|
| T bridge, p ≤ 1,000 (S1 p = 500, all of S2, S3 p = 500) | 2.9k (1.3k–8.0k) | 2.8k (1.2k–7.7k); ≈ 12 days at 230/day | **Owls fits**: single-thread, the R core measured at p = 500/1,000 (rr2400); 1.93× slower per core, billed 2 CPUs on NOTS |
| T bridge, p = 5,000 (S1, S3) | 6.3k (1.9k–21.4k) | 6.2k on the synthetic anchor; **≈ 62k on the riboflavin anchor** (88 h × (5,000/4,088)² ≈ 132 core-h per fit, 8.1 µs per move [D]) | **NOTS.** The two anchors differ ≈ 10×; the riboflavin one is real data, n = 71; no p = 5,000 T fit exists. At 230/day even 6.2k is 27 days, and 62k is impossible |
| F2, all cells and block E | 1.9k (0.9k–5.6k) | 2.8k (1.4k–8.4k) if an Owls build existed [P] | **NOTS.** The V build is compiled for the sapphirerapids ISA (`results/overlap1e4/OVERLAP_1e4_PREREG.md` §2); Owls is Skylake. An Owls build is unverified, and its bits would not pool with NOTS bits (R10) |
| competitors | – | 0.7k (0.3k–2.7k) | **Owls**; their timings need the same hardware class as the F2 timings for r_{A,B}, so rerun the timed block E on one machine |

**Recommended split [P]:** NOTS = F2 + T at p = 5,000 = **8.2k billed (range 2.8k–27.0k)**, i.e. 37 % of the remaining envelope (central) [D]. Owls = T at p ≤ 1,000 + competitors = **3.5k Owls core-h** (≈ 15 days), which is not billed to the envelope.
If everything ran on NOTS: **11.8k** (4.4k–37.7k).

### 6A.8 Against the NOTS envelope
Envelope ≈ 28.3k, closed ≈ 6,042 (`LEDGER.md`, totals 2026-11-21), so **≈ 22,258 remain [D]**. Nothing else is planned on NOTS: the 1M block stopped after W2 (HQ H-53; `HANDOFF_V2.md` §1).
| scenario | NOTS billed | share of the remaining 22.3k | share of the 28.3k envelope (cumulative with 6.0k closed) |
|---|---|---|---|
| central, all on NOTS | 11.8k | 53 % | 63 % |
| **central, recommended split** | **8.2k** | **37 %** | **50 %** |
| low, all on NOTS | 4.4k | 20 % | 37 % |
| high, all on NOTS | 37.7k | **169 %: does not fit** | – |
The central design fits with room (a 25 % reserve on the central total is 14.8k, still inside). The high scenario does not; levers in §6A.6 and the calibration pilot come first, and any batch above ≈ 200 core-h needs an HQ go (`LEDGER.md` rules).

**Open choices for the owner/HQ (all PROPOSED above):** (1) replicates: R_F = 50 (100?) and the T bridge R_T = 10; (2) S3 signal and SNR levels {1, 2}; (3) F2 at N = 2,500 (not 10⁴); (4) T bridge on all cells against a subset;
(5) S2: beta-types 1–2 only, MCMC baselines on S2 or not; (6) the NOTS/Owls split and whether an Owls F2 build is wanted; (7) block E cells and the gold-standard run; (8) which real data sets are in scope; (9) the Theory question on S3 (compound symmetry, D1; ties in the partition).

## 7. Risk register

| # | risk | likelihood / impact | mitigation | trigger to HQ |
|---|---|---|---|---|
| R1 | **log Ẑ dispersion** grows with p (σ̂ 0.76–1.15 at 5k–20k, N = 2,500; right tail not cured by 4N). Weight degeneracy (R_eff/R′ → small) at 1M. | high / medium: affects evidence and PIP_Z, not HPM or PIP_eq (islands agree so far) | report, never switch on it; keep PIP_eq primary (OD-4); the union HPM/store needs no weights; 64-island census at 10⁴/10⁵ to chart σ̂(p) | R_eff/R′ < 0.1 or islands disagree on the HPM |
| R2 | **Escalation at large p** (any of 7 triggers, incl. `grid_unconverged`) quadruples the cost | high / high | bounded calibration OD-2(c); three-arm test at 10⁴ fixes I_max | any escalation in production mode |
| R3 | **Memory**: the Θ(p²) objects (Gram, r, dist), cache 500p, store 40p + 1, tables | certain without G1–G7 / blocking | G1–G7, G11; mmap-shared tables and X; memory model checked at 10⁵ (G-B) | RSS > 1.2× model |
| R4 | **Partition change** (G3) alters π₀ and possibly the START premises | medium / high (theory) | T-PART before rung C; A3 paired comparison at 10⁴ | T-PART says a premise fails |
| R5 | **Per-step cost at 1M** is UNVERIFIED and may be **bandwidth-bound** (1.6 KB of X per Gram-free step ≈ 168 TB per island) | medium / high | gate T5 (bandwidth curve + step cost on Owls/one node at 10⁵–10⁶) before G-B; label-major prototype (OD-16) | > 1.5× model |
| R6 | **T and I grow with p** (ℓ = 20 at 1M) | medium / medium (+25–60%) | measured at 10⁵; budget lever R′ = 8 | I hits ℓ or T > 45 |
| R7 | **24 h limit / preemption**: a serial 1M island takes about 70 h | certain without checkpoints | G9 checkpoint at stage boundaries; forced-kill test at 10⁵; commons only (no scavenge for long work) | restart not bit-identical |
| R8 | **Preflight refusals**: the memory preflight refuses from about 19k; the LS0 charge refusal returns between 20k and 30k | certain without G11/G12 | rewrite the preflight models; admission only (O14) | — |
| R9 | **Data generation and storage**: X is 1.6–3.2 GB per dataset; RB arrays and PIPs p-wide; stores 4·10⁷ | low / medium | regenerate X per worker from the seed plus a hash; binary outputs; /scratch quota (REQUESTS R4) | scratch > 70% |
| R10 | **Scheduler**: 150 concurrent tasks; cascadelake 1.7–2× slower (P6) | medium / medium | `--constraint=sapphirerapids` always; node type recorded; hardware reruns never pooled (P6 N2) | queue wait > 24 h |
| R11 | **Wall time and holidays**: engineering slip pushes 1M into January | medium / medium | Minimal tier as the fall-back target; the 1M pilot first | slip > 1 week at G-B |
| R12 | **B2-3 unresolved**: the `fresh` counters block G6/G8(a) under O17, and B2-1 trace replay is physically impossible at 1M (≈ 2·10¹² lookups, about 30 TB per fit) | certain if not decided | OD-3 | — |
| R13 | **D1 / factor designs**: cs designs at p ≫ n are expensive (P6: 16 h at n = 100, p = 1,000, always escalated) | high cost if included | FAC only at 10⁴ and only if D1 says so. **v0.3:** S3 (§2.0.4) is a compound-symmetry design at p = 500 and 5,000, so this risk is now live; pilot first (§6A.6), Theory asked about D1 and ties in the partition | — |
| R14 | **Competitor fairness**: tuning and the predictive object are chosen after the fact | medium / reputational | freeze settings and the evaluator before rung A; Sol review of the harness | — |
| R15 | **DIST statement changes** (W3-DIST in progress) | high / low | metrics cover all three objects plus the oracle; the evaluator is versioned | STATEMENT version change |

## 8. Timeline (SECONDARY ladder; v0.2 calendar, superseded by `LEDGER.md` and `LOG.md`; no S1–S3 dates are set because SMC-BVS is on its break, HQ H-54)

| dates | work | output |
|---|---|---|
| 11-16 → 11-20 | Sol review of this plan; owner decisions; T-PART and T-N legs (theory week); Owls micro-benchmarks (G1/G5 at p = 10⁵–10⁶ in RAM; no NOTS) | plan v1.0, budget approved |
| 11-23 → 12-04 | G1, G2, G4, G5, G6, G7, G11, G12 (SCALE); G13 (EXP); S0 gates on NOTS (≈ 150 core-h); Sol code review | v4 engine (OP-bit part) |
| 12-07 → 12-11 | G3, G9, G10, G8; A1 + A2 pilots → **G-A** | rung A running |
| 12-14 → 12-18 | rung A main; 10⁵ pilot → **G-B** | rung A results, σ̂(p), E2 rate |
| 12-21 → 12-31 | rung B main; 1M pilot fit → **G-C** | first joint BVS fit at 10⁶ |
| 01-04 → 01-15 | rung C main → **G-C2**; analysis, figures, paper section | 1M results |

## 9. What this plan does not do
- It does not prove anything about the parallel method beyond what T-N and T-PART deliver.
- It does not change the target posterior. Screening appears only as a competitor.
- It does not use scavenge for long jobs, and it does not run on cascadelake.
- It does not run anything on NOTS without an HQ go.
- **v0.3:** it does not start S1–S3 (the owner restarts SMC-BVS later); it does not use real data for selection claims (§3.6); it does not claim the F2 engine is the theorem-covered method outside the 10⁴, n = 200 overlap evidence (§2.0.7).

## 10. References (the five works named in the HQ decision of 2026-11-24, `MAIN:Theory_work/Wave3/HQ_DECISIONS.md` line 908; titles and journals from REPORT §8)
| key | reference | DOI | used for |
|---|---|---|---|
| YWJ 2016 | Yang, Wainwright, Jordan. On the computational complexity of high-dimensional Bayesian variable selection. Annals of Statistics 44(6):2497–2532 | 10.1214/15-AOS1417 | S1: the β* vector and the SNR scaling |
| Griffin et al. 2021 | Griffin, Łatuszyński, Steel. In search of lost (mixing) time: adaptive MCMC schemes for Bayesian variable selection with very large p. Biometrika 108(1):53–69 | 10.1093/biomet/asaa055 | S1: AR 0.6, n ∈ {500, 1000}, p ∈ {500, 5000}; the ASI competitor |
| Hastie et al. 2020 | Hastie, Tibshirani, Tibshirani. Best subset, forward stepwise or lasso? Analysis and recommendations based on extensive comparisons. Statistical Science 35(4):579–592 | 10.1214/19-STS733 | S2: the AR(ρ) grid, beta-types, the ν grid |
| George–McCulloch 1993 | George, McCulloch. Variable selection via Gibbs sampling. J. Amer. Statist. Assoc. 88(423):881–889 | 10.1080/01621459.1993.10476353 | S3: equicorrelation ρ ≈ 0.5 |
| Dezeure et al. 2015 | Dezeure, Bühlmann, Meier, Meinshausen. High-dimensional inference: confidence intervals, p-values and R-software hdi. Statistical Science 30(4):533–558 | 10.1214/15-STS527 | S3: equicorrelation ρ = 0.8 |

The design synthesis behind S1–S3 is REPORT.md (BENCH_DESIGN, 89 papers), with the per-paper setups in PAPERS.md; both are in `MAIN:Theory_work/Dept/assess/BENCH_DESIGN/`.

