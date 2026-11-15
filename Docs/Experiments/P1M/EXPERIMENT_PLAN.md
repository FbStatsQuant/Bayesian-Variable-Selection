# EXPERIMENT_PLAN — SMC-BVS at p = 10⁶ (draft v0.1, EXP-CP1, 2026-11-15)

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
| C2 | **Reported model = S₀** with probability rising to 1 in n, at every p of the ladder. | RM-0/RM-F/RM-R (#7), RM2-F/R (#8), Delivery C-DLV (#10), GEN/GROW (#6) | P̂(HPM = S₀), outcome class (posterior / search) |
| C3 | **Start mass.** π₀(S₀) → 1 at the rate n^{−c}, computed exactly from the start tables. | W3-START, START2 (#5) | log(1 − π₀(S₀)) against log n |
| C4 | **PIP consistency.** pip_primary → 1_{S₀} in sup-norm; MPM = HPM = S₀. | SAMP LT♯, TR, D (#9); C-PACK SL1/SL2 | sup_{j∉S₀} PIP, min_{j∈S₀} PIP, P̂(MPM = S₀) |
| C5 | **Distribution consistency (top priority).** The returned output's predictive law contracts to f* in Hellinger at the rate s₀ log p / n (store-BMA) and at the parametric rate under selection (HPM/MPM plug-in). | W3-DIST: DIST-1, DIST-2, DIST-3, DIST-C(i)–(iv) (candidates, status CANDIDATE); POST2 Hellinger (#2) | d_H² of the plug-in and predictive outputs; n·d_H² against n (§3.3) |
| C6 | **Certified screening** where the reported-model conditions are not met: certified models of size ≤ q_n contain S₀. | W3-SCR (#11) | P̂(S₀ ⊆ Ŝ given certified) |
| C7 | **Evidence and merge diagnostics.** These are measured, not claimed: unbiased pooling holds, and the dispersion is documented as a function of p. | N1, O1, O19; O2 is open | σ̂(log Ẑ_r), R_eff/R′, \|PIP_Z − PIP_eq\| |
| C8 | **Comparison.** Selection, prediction and cost against methods that actually run at each p. | paper §Experiments | §4 |
| C9 (contingent) | **Strong factors at p ≫ n** (D1), at 10⁴ only, if P6 or the D1 ruling says it is fair game. | D1 (#12) | as in C2 and C6 |

Claims are always worded with the theorem's labels. C5's coded-output statements are conditional on the delivery premises
P-STORE / P-HIT, so the run records the diagnostics for those premises (§3.3). C5 is stated only as an
illustration of a candidate theorem until W3-DIST records a status.

## 2. Designs

### 2.1 Common data model (random design, matches W3-DIST (RD))
Rows iid. y = Xβ* + ε, ε ~ N(0, σ*²I), σ* = 1, α* = 0. s₀ = 5. Each replicate draws a fresh (X, ε): random design.
Data are **regenerated from the seed by every worker** (counter-based generator, one stream per column chunk) and
checked by hash, so nothing p-wide is stored or shipped. At n = 200, X is 1.6 GB in doubles; at n = 400, 3.2 GB.

### 2.2 Design families (examples only)
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

### 2.3 Ladder and gates (n, signal, replicates)
p = n^A with A = log p / log n. At 1M: A = 2.6 (n = 200), 2.3 (n = 400).

| rung | p | designs × signal | n | reps | R′ | notes |
|---|---|---|---|---|---|---|
| S0 | ≤ 2·10⁴ | PROD-H 24 units + supplementary; 5k/10k/20k setups | as recorded | — | 4 | engine gates only (§5.2) |
| A1 law bridge | 10⁴ | AR strong | 200 | 10 + 10 | 4 vs 16 | v3.1 law (N = p = 10⁴, R′ = 4) against fixed N = 2,500 (R′ = 16) on the **same datasets** |
| A2 main | 10⁴ | AR strong + weak; IND, BLK strong | 100, 200, 400, 800 (AR); 100, 200, 400 (IND, BLK) | 10 (AR strong), 5 (others) | 16 | n-trend for C2–C5 |
| A3 partition | 10⁴ | AR, BLK strong | 200 | 10 | 16 | exact complete linkage against the 1M partition rule, same data: π₀(S₀) and outcomes (OD-5) |
| A4 extras | 10⁴ | MIS, ADJ, FAC (if D1 says so) | 200, 400 | 5 | 16 | optional |
| B | 10⁵ | AR strong (n-trend), IND strong | 200, 400 (AR); 200 (IND) | 5 | 16 | first rung needing G1–G7 |
| C | 10⁶ | AR strong (primary); IND strong | 200 (AR, IND); 400 (AR, Full tier only) | 3 (AR), 2 (IND) | 16 (8 if budget) | rep 1 is the pilot |

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

## 4. Competitors that can actually run at each p

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

## 5. Engineering prerequisites: gap list from W3-SCALE revision D to a 1M-ready engine ("v4")

Baseline: revision D (6866f57) is bit-identical to v3.1 on PROD-H. It is still Θ(p²) in memory, serial, and has a 4-island
in-process layout. Sizes are agent-days (A-d) of an Opus lead plus a review, and NOTS core-h of gates.
"Owner" means who builds: **SCALE** = W3-SCALE leg C team (engine owner); **EXP** = this department; **TH** = a theory ticket;
**HQ** = decision.

| id | item | tag | why at 1M | size | owner |
|---|---|---|---|---|---|
| G1 | **Gram-free canonical scorer.** G_{S,j} from X columns by lane-parallel *sequential* dot products (same summation order as `data_init`, v3_score.h:45–53); per-particle factor cache. | [OP-bit] (v0 local check: identical bits) | the Gram is 8 TB at 1M | 4 A-d, gate 20 core-h | SCALE |
| G2 | **Streamed correlation tiles** for the neighbour graph (r_n threshold, partial selection, O(pB) memory, threaded) and for duplicate components (now R `crossprod`, O(np²) in R). | [OP-bit] | 2·10¹⁴ flops at n = 200, about 1–2 node-hours; no p² array | 3 A-d | SCALE |
| G3 | **Block partition above about 150k.** Exact complete linkage needs the full distance matrix (v3_blocks.h:54: dense r and dist, 16p² bytes; 4 TB condensed at 1M). Proposed rule: exact complete linkage inside the connected components of {\|r\| ≥ τ_n}; components larger than B cut by the same top-down rule; components packed by next-fit in index order. | **[Δlaw]** (π₀ changes); O8 | hard memory wall | 5 A-d + TH | SCALE + **TH T-PART** |
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

## 6. Cost model and budget

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

## 7. Risk register

| # | risk | likelihood / impact | mitigation | trigger to HQ |
|---|---|---|---|---|
| R1 | **log Ẑ dispersion** grows with p (σ̂ 0.76–1.15 at 5k–20k, N = 2,500; right tail not cured by 4N). Weight degeneracy (R_eff/R′ → small) at 1M. | high / medium: affects evidence and PIP_Z, not HPM or PIP_eq (islands agree so far) | report, never switch on it; keep PIP_eq primary (OD-4); the union HPM/store needs no weights; 64-island census at 10⁴/10⁵ to chart σ̂(p) | R_eff/R′ < 0.1 or islands disagree on the HPM |
| R2 | **E2 escalation at large p** quadruples the cost | high / high | OD-2 decided before rung B, with A2 data on how often it fires | E2 rate > 20% in A2 |
| R3 | **Memory**: the Θ(p²) objects (Gram, r, dist), cache 500p, store 40p + 1, tables | certain without G1–G7 / blocking | G1–G7, G11; mmap-shared tables and X; memory model checked at 10⁵ (G-B) | RSS > 1.2× model |
| R4 | **Partition change** (G3) alters π₀ and possibly the START premises | medium / high (theory) | T-PART before rung C; A3 paired comparison at 10⁴ | T-PART says a premise fails |
| R5 | **Per-step cost at 1M** is UNVERIFIED (cache misses on p-long arrays, nth_nonmember, permutations) | medium / high | 10⁵ pilot measures it; micro-benchmarks on Owls at 10⁵–10⁶ before G-B | > 1.5× model |
| R6 | **T and I grow with p** (ℓ = 20 at 1M) | medium / medium (+25–60%) | measured at 10⁵; budget lever R′ = 8 | I hits ℓ or T > 45 |
| R7 | **24 h limit / preemption**: a serial 1M island takes about 70 h | certain without checkpoints | G9 checkpoint at stage boundaries; forced-kill test at 10⁵; commons only (no scavenge for long work) | restart not bit-identical |
| R8 | **Preflight refusals**: the memory preflight refuses from about 19k; the LS0 charge refusal returns between 20k and 30k | certain without G11/G12 | rewrite the preflight models; admission only (O14) | — |
| R9 | **Data generation and storage**: X is 1.6–3.2 GB per dataset; RB arrays and PIPs p-wide; stores 4·10⁷ | low / medium | regenerate X per worker from the seed plus a hash; binary outputs; /scratch quota (REQUESTS R4) | scratch > 70% |
| R10 | **Scheduler**: 150 concurrent tasks; cascadelake 1.7–2× slower (P6) | medium / medium | `--constraint=sapphirerapids` always; node type recorded; hardware reruns never pooled (P6 N2) | queue wait > 24 h |
| R11 | **Wall time and holidays**: engineering slip pushes 1M into January | medium / medium | Minimal tier as the fall-back target; the 1M pilot first | slip > 1 week at G-B |
| R12 | **B2-3 unresolved**: the `fresh` counters block G6/G8(a) under O17, and B2-1 trace replay is physically impossible at 1M (≈ 2·10¹² lookups, about 30 TB per fit) | certain if not decided | OD-3 | — |
| R13 | **D1 / factor designs**: cs designs at p ≫ n are expensive (P6: 16 h at n = 100, p = 1,000, always escalated) | high cost if included | FAC only at 10⁴ and only if D1 says so | — |
| R14 | **Competitor fairness**: tuning and the predictive object are chosen after the fact | medium / reputational | freeze settings and the evaluator before rung A; Sol review of the harness | — |
| R15 | **DIST statement changes** (W3-DIST in progress) | high / low | metrics cover all three objects plus the oracle; the evaluator is versioned | STATEMENT version change |

## 8. Timeline (calendar; assumes OD decisions by 11-20 and two engine builders)

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
