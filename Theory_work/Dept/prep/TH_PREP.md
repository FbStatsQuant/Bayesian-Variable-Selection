# TH-PREP: baseline theorem sheet, sensitivity map and S1/S2 checks for SMC-BVS v3.1.1

Theory Department, 2026-11-27. Ordered by the owner via HQ. This is preparation only: **no proofs were written**. It is the hard stop until Engineering's SMC-PERF engine decision.

Sources are the read-only main at `cda5670e`: the manuscript (`Docs/Writing/manuscript/`), the registry, and the Wave 1–3 folders. Two Sonnet extraction passes are kept in `TH_PREP_support/`:
- `W1_STATEMENTS.md`: statements, statuses and assumption verdicts, each with file:line.
- `W2_ROUTES.md`: where each model element enters each proof, with file:line.

Lines marked **[Opus]** are my own reading or inference. They are not proved, and none comes from a repository source.

## 0. Bottom line

1. **All three Song–Liang targets already have delivered counterparts for v3.1.1.** Each is proved and independently checked, or proved and checked with named inputs (§2).
   - True-model consistency: `thm:post-random`, `thm:post-fixed`.
   - Distribution consistency: `thm:dist`.
   - Misspecification: `thm:omitted` with C-MIS / W3-MISR.
   - The theory work after the engine decision is therefore *adapting* these to whatever changes, not starting over.
2. **The gap is the SMC particle limit.** For our sampler there is no proved result that the estimates converge as the number of particles N → ∞ (T16 is "conjectured, not proven"). What is proved:
   - exact unbiasedness of the evidence given the frozen calibration;
   - consistency at the fixed production budget as n → ∞.

   A particle-limit theorem looks cheap *because the calibration is frozen*; see T4.
3. **Most assumptions are (a): they have peer-reviewed precedents.** The exceptions:
   - The beta-min / fixed-signal conditions **do not literally cover S1**. S1's coefficients are set at the boundary, β ∝ √(log p/n), and the proof constant of the beta-min condition is far above the empirical S1 threshold. This is the main place where a (b) assumption, supported on S1/S2, should replace a proof constant (§2, §4).
   - Two others are (c): the dimension cap p ≤ n^A (narrower than Song–Liang) and the sampler idealisations.
4. **Sensitivity.**
   - **Cheap changes:** g = c·n, BB(1,p^u) with u ≥ 1, a different cap ≥ c·n, any fixed IG(a₀,b₀), more particles or islands, MPM vs HPM, or a fixed PIP threshold.
   - **Moderate changes:**
     - g = max(n,p²) (the Fernández–Ley–Steel benchmark choice) or another data-free slab;
     - a lighter size prior BB(1,p^u) with u < 1;
     - an in-run adaptive tempering schedule.
   - **Route-breaking changes:** BB(1,1); dropping centring/scaling; anything that makes the score non-closed-form.
5. **[Opus], for SMC-PERF.** For small models, BB(1,1) and BB(1,p) differ in per-variable prior penalty by only about log 2 (0.7 nats) out of the total 7.5–10 nats per variable. Switching to BB(1,1) would cost the size-tail proof step but would barely change under-selection. The levers that move under-selection are g and a p-dependent b with u < 1 (§3).

## 0a. Scope ruling (owner via HQ, 2026-11-27): what serves (1)–(3) and what is DEFERRED

Theory now does **only** the 1-to-1 Song–Liang equivalents in our setup:
- **(1)** true-model consistency;
- **(2)** true-distribution consistency;
- **(3)** consistency under misspecification.

Everything else is **DEFERRED** until (1)–(3) have finished proofs **and** Lean code. Assumptions are kept only if (1)–(3) need them. Proof writing stays on HOLD until the SMC-PERF engine decision. Tags used below: **[1]**, **[2]**, **[3]** = serves that theorem; **[DEFERRED]**.

| item in this file | serves | note |
|---|---|---|
| §1 model as coded (data, slab, σ², size prior, cap) | [1][2][3] | the sampler and report rows matter only to deferred results, except MPM/HPM, which (1) uses through `lem:summaries` |
| §2 T1 `thm:post-random`, assumptions GL, DIM, SP, GR/SGR, FSb, EFS | **[1] core** | SL Thm 3 + Thm S equivalent; `lem:summaries` (HPM/MPM/PIP from δ) is part of it |
| §2 T1 BM(a) / `asm:margin` (fixed-design variants) | **[1] variant, pending** | keep only if the owner wants S1's boundary signals inside (1); otherwise DEFERRED |
| §2 T1 sample EF, NC (fixed design `thm:post-fixed`) | [1] variant, pending; NC also **[2]** (as `nec`) | — |
| `thm:post-fixed` expectation bound (W3-POST2:C route) | **[3] input** | (3) reduces to it (R3 → R1 expectation route); an input lemma, not a separate result |
| `rem:sharp` (Result 6), `rem:thm2x`, `thm:post-margin` as separate results | **[DEFERRED]** | extensions |
| §2 T2 `thm:dist` and the `asm:dist` items (model, sparse, subg, nec, bs) | **[2] core** | SL Thm 1/2 equivalent |
| `prop:dist` (ii) (without NC), `thm:dist-param`, `cor:dist-output`, in-sample Hellinger (W3-POST2 D) | **[DEFERRED]** | extensions |
| §2 T3 `thm:omitted` / C-MIS MIS(i)–(iii), `asm:omitted` (a)(b)(c) | **[3] core** | SL **Cor 2** equivalent (selection of the projection support) |
| §2 T3 [Opus] candidate: `thm:dist` on the candidate re-run (KL-projection Hellinger) | **[3] core, candidate** | the 1-to-1 SL **Thm 4** equivalent; to be stated after the engine decision |
| §2 T4 (all SMC results: `prop:unbiased`, W3-SAMP, `thm:outputs`, T4a, T4b), assumptions EX-A, H-U, KERNEL, CAL/SI, START | **[DEFERRED]** | the particle-limit theorem is explicitly deferred |
| reported-model and screening results (`thm:reported`, `cor:famc`, `cor:list`, `thm:screen`), assumptions V, leakage set, local regressions, NL, C1/C2/C2p, SCR budget | **[DEFERRED]** | not Song–Liang equivalents; their assumptions are dropped from the (1)–(3) list |
| §3 sensitivity map, columns R1, R2, R3 | [1][2][3] | **columns R4 and R5: [DEFERRED]**. The kernel, tempering and N/islands rows affect only R4/R5, so they do not touch (1)–(3) |
| §3 rows: slab/g, ridge, size prior, cap, σ² prior, centring/scaling, MPM/HPM/threshold | [1][2][3] | still decision-relevant |
| §4 E1, E3 | [1] | — |
| §4 E2 | [1] (sample floors); [2] (nec) | — |
| §4 E4 | [2] | — |
| §4 E5, E6 | [1][2][3] | — |
| §4 E8 | [3] | — |
| §4 E7 | **[DEFERRED]** | the particle limit; HQ may tell Engineering to drop it |
| §5 items 1, 4, 5, 6 | [1][2][3] | item 1 = SONG_LIANG_MAP refresh |
| §5 items 2, 3 | **[DEFERRED]** | cards TH01/M1 |

**Net assumption list for (1)–(3):**
- **[1]:** GL, DIM, SP, GR (or SGR), FSb, EFS; plus BM/margin only if the S1-covering variant is chosen.
- **[2]:** the five `asm:dist` items.
- **[3]:** `asm:omitted` (a)(b)(c), plus the [1] inputs through the expectation route.

## 1. The model as coded (v3.1.1, tag `method-v3.1.1-listpip`)

| element | as coded | source |
|---|---|---|
| data | X and y centred and scaled to sample SD 1 (divisor n−1, so ‖x_j‖² = yᵀy = n−1); no intercept parameter | `v3_preprocess.R:35-68,116-127` |
| slab | β_S \| S, σ² ~ N(0, nσ²(X_SᵀX_S + I)⁻¹), i.e. a g-prior with g = n and a unit ridge; H = (n+1)G_S + I, A = G_S + I | `cpp/v3_score.h:175-223`; spec `sp3_distributions.tex:20-58` |
| σ² | IG(0.01, 0.01), independent of S | `v3_score.h:14,57` |
| model prior | BB(1,p): w(k) = ½/C(2p−1,k) per model of size k, renormalised over Ω = {\|S\| ≤ K}, **K = min(p, ⌊n/2⌋)**; prior mean size p/(p+1) ≈ 1 | `v3_score.h:15,40,61-70`; `v3_core.cpp:74`; kernel `v3_engine.h:116` |
| sampler | SMC with a pilot-calibrated tempering grid that is **frozen** before the final run; random-order block Gibbs, add, delete and swap rounds (blocks ≤ 16); 4 islands; LS0 local search | `v3_engine.h:275-375` |
| report | MPM (pooled PIP > ½) is reported; the HPM is stored | S1/S2 SPEC |

Per-variable price of adding one predictor to a model of size k:

  log[(2p−1−k)/(k+1)] (prior) + ½ log(n+1) (Occam factor)

On S1/S2 this is 7.5–10 nats, so the partial t² must exceed about 15–20 (§4, item E1).

## 2. Baseline statement sheet

**Assumption classes.**
- **(a)** stated in a peer-reviewed ultrahigh-dimensional linear-regression selection paper.
- **(b)** new, but supported empirically on S1/S2.
- **(c)** a mild technical condition.

**Abbreviations.**
- SL = Song & Liang (2015, JRSS-B 77(5) 947–972); page numbers are as recorded in `SONG_LIANG_MAP.md` and `TRACK_B.md`.
- Precedents (all read and verified in `Docs/Writing/from_theory/PRECEDENTS_2026-11-17.md`):
  - CSV15 = Castillo, Schmidt-Hieber & van der Vaart (2015, AoS);
  - YWJ = Yang, Wainwright & Jordan (2016, AoS);
  - NH14 = Narisetty & He (2014, AoS);
  - SBJ = Shin, Bhattacharya & Johnson (2018, JASA);
  - SC11 = Shang & Clayton (2011, JSPI);
  - ZH08 = Zhang & Huang (2008, AoS);
  - BRT09 = Bickel, Ritov & Tsybakov (2009, AoS);
  - MY09 = Meinshausen & Yu (2009, AoS);
  - W09 = Wainwright (2009, IEEE-IT);
  - RWY = Raskutti, Wainwright & Yu (2011, IEEE-IT);
  - RZ = Rudelson & Zhou (2013, IEEE-IT).

### T1. True-model consistency (counterpart of SL Thm 3, sure screening, and Thm S, MAP consistency) — **[1]**

**Headline: `thm:post-random`** (`s4_results.tex:111-120`). Under GL, DIM, SP, SGR, FSb and EFS:
- 1 − π(S₀|y) = O_P(√(log n/n));
- P(HPM = MPM = S₀) → 1;
- max_j |PIP_j − 1{j∈S₀}| = O_P(√(log n/n)).

Status: proved and independently checked. The Gaussian-row case is registry row 1.2. The sub-Gaussian form was recorded on 2026-11-17.

The rate is sharp up to √log n (`rem:sharp`, row 1.3): no design gives a rate better than n^{−1/2}. SL give no rate for whole-model selection, and their Thm 3 covers sensitivity only. Our result gives specificity as well.

**Companions.**
- `thm:post-fixed` (supplement, row 1.1): fixed design with BC, EF, NC and BM; also gives the expectation bound E[1−π(S₀)] ≤ C√(log n/n).
- `thm:post-margin`: replaces beta-min and the floor off S₀ by an identifiability margin.
- `rem:thm2x`: expectation form with the floor on smaller sets.

| label | content | used by | class | source / precedent | S1/S2 |
|---|---|---|---|---|---|
| GL | Gaussian linear model, fixed σ², noise independent of X | all | (a) | SL model (1)–(2), pp. 947, 950: the same | true by construction |
| DIM | 2 ≤ p ≤ n^A, A ≥ 1 fixed | all | (a)/(c) | narrower than SL (Cor 1: P_n < exp(Cn^α), p. 954). SBJ, NH14 and SC11 allow larger p; "p ≤ n^A" is a convenience of our proofs. Referee risk: a known gap relative to SL, not a fight | A = log p/log n = 0.90–1.37 (S1), 1.50–1.77 (S2) |
| SP | s₀ ≥ 1 fixed | all | (a) | SL (4), p. 950: the same for Thms 2, 3 and S; NH14 Cond 4.3 | s₀ = 10 (S1); 5 or 10 (S2) |
| GR / SGR | i.i.d. N_p(m_n,Σ) rows (or sub-Gaussian along ≤ 5(A+1)(s₀+1)log n-sparse directions) | random-design form | (a) | ZH08, RWY, W09 (Gaussian); RZ, NH14 (sub-Gaussian). Comparable to SL Cond 1 (p. 953), neither implies the other | true by construction |
| EFS / EF | λ_min(Σ_S) ≥ φ² (population) on sets of size ≤ 5(A+1)(s₀+1)log n; or λ_min(R̂_S) ≥ φ₀² on sets of size ≤ 2(A+1)s₀+2 (sample) | T1 | (a) | ZH08, CSV15, YWJ (+ BRT09). Comparable to SL Cond 3 (p. 955) | **population form true analytically**: AR(1) gives λ_min ≥ (1−ρ)/(1+ρ), which is 0.25 (S1, ρ = 0.6) and 0.48 / 0.18 (S2, ρ = 0.35 / 0.7). Sample form: §4 E2 |
| NC | λ_min(G_S) ≥ g₀ on sets of O(log n) size (correlation floor g₀/(n−1), vanishing) | fixed design, T2 | (a) | SBJ, NH14, BRT09 (+ MY09). Adds a condition relative to SL Thms 1–2 | population: true. Sample: §4 E2 |
| FSb | b_lo ≤ \|β*_j\| ≤ b_hi fixed (raw scale) | headline | (a) | CSV15 Thm 5, YWJ, MY09 (beta-min type); SL state no lower bound on the coefficients | **S2: true** (β = 1, σ² = βᵀΣβ/ν fixed per setting). **S1: false as a sequence**, since β* = SNR·√(log p/n)·c sits exactly at the beta-min boundary |
| BM(a) | θ_min ≥ C_β σ √(log n/n) with C_β²φ₀² > c₀(s₀,A) | `thm:post-fixed` | (a) in form; **(b) for the constant** | CSV15, YWJ, MY09; SL proof step "at a fixed multiple of log n" (supp. pp. 6, 15) | S1: ratio θ_min/(σ√(log p/n)) = 2·SNR ∈ {1, 2, 4, 6}. The proof constant c₀ = max{4C*, 32[s₀(A+1)+2]} is far above the empirical transition (between ratio 2 and 4). **Proposed (b) replacement:** the margin form of `asm:margin`, with its constant fitted on S1/S2 (§4, E1) |
| asm:margin | every S that misses a true predictor and adds ≤ j₀ nulls has ‖(I−P_S)μ‖² ≥ c_id σ² log n | `thm:post-margin` | (b) candidate | none found as stated (precedent search: NOT FOUND); closest is NH14 Cond 4.4, residual-signal identifiability | this is the quantity that explains bt2 (§4, E1) |

### T2. Distribution consistency (counterpart of SL Thm 1 and Thm 2, Hellinger contraction) — **[2]**

**`thm:dist`** (`s4_results.tex:191-198`, row 2.1). Under the setting of `asm:dist`, for every level M ≥ M₀ with √n/log n ≥ M:

P*[Π(d_H(f,f*) > √(M log n/n) | D_n) > n^{−c_H M}] ≤ n^{−c_H M}

This is SL display (15) in exponential form, inside the window M ≤ √n/log n. No beta-min condition and no fixed eigenvalue floor are needed. Status: **proved and independently checked**.

Companions: `prop:dist` (level-M form; without NC the radius gains a factor √log(p∨n)) and `thm:dist-param` (the parametric rate M_n/√n under beta-min). Note that `SONG_LIANG_MAP.md` row 1 ("no Hellinger analog") is stale: it predates W3-DIST.

| label | content | class | source | S1/S2 |
|---|---|---|---|---|
| model | i.i.d. pairs, Gaussian linear y \| x | (a) | SL p. 950 | true |
| sparse | ≤ s nonzero, 2 ≤ p ≤ n^A | (a)/(c) | as for SP and DIM | true |
| subg | sub-Gaussian along q_n-sparse directions, q_n = O(M log n) | (a) | RZ, NH14; SL Cond 1 or 2 (pp. 953–954) | true (Gaussian, L = 1) |
| nec | λ_min(Corr(x_T)) ≥ c_ψ/n, \|T\| ≤ q_n | (a) | SBJ, NH14, BRT09 | population: true |
| bs | \|β*_j\|sd(x_j) ≤ b̄σ* | (a) | YWJ, SC11 | true per setting |

### T3. Misspecification (counterpart of SL Thm 4 and Cor 2) — **[3]**

The delivered counterparts are `thm:omitted` (supplement, row 1.4) and C-MIS Theorem MIS (i)–(iii) / Cor N, with W3-MISR MIS(i), (i′), (ii). The setting: the method is re-run on the candidate columns only, and the omitted part is Gaussian given the candidates. Then:
- E[1 − π(S₀^C | y)] = O(√(log n/n)), where S₀^C = supp(β_C + γ) is the support of the best approximating model;
- the HPM equals S₀^C with probability → 1;
- proxies (null in the full model) are selected and cancelled true predictors are dropped;
- for jointly Gaussian X, a candidate is a proxy iff its partial correlation with an omitted active variable is nonzero (Prop P).

Status:
- `thm:omitted`: "proved and independently checked" (main edition).
- W3-MISR: "PROVED-CHECKED, conditional on W2-APP:POST".

These are stronger than SL in one way: they give the exact best model at a rate, not just inclusion of supp β₀. They are narrower in another: Gaussian residual with scalar variance, in probability rather than almost surely.

**Gap.** There is no literal SL Thm 4: a fixed subset model, with KL-projection *density* consistency.

**[Opus] Candidate, not proved.** Under jointly Gaussian X, the candidate-only data form a *correctly specified* Gaussian linear model with (β^C, σ_C²) (Prop P / Example `ex:omitted`). Then `thm:dist`, applied to the candidate re-run, should give Hellinger contraction to the KL projection f₀ at √(M log n/n), provided s_C is fixed and `asm:dist` holds on the candidates. That would be an SL Thm 4 counterpart at a rate, almost for free. It is to be checked after the engine decision.

| label | content | class | source | S1/S2 |
|---|---|---|---|---|
| asm:omitted (a), GR^c | candidate rows Gaussian; y \| x_C linear-Gaussian with σ_C² = σ² + τ² | (c) for jointly Gaussian designs (it is then a consequence: Prop P); otherwise new | no precedent for exact selection under misspecification (`ASSUMPTION_MAP`: CSV15, NH14 and YWJ are well-specified only); SL Thm 4 has Condition 4 instead | S1/S2 are well-specified. Checking T3 needs a hidden-column experiment (§4, E8) |
| asm:omitted (b) | floor λ_min(R_T) ≥ c_C on 3(A+1)(s_C+1)log n sets | (a) | as EF / NC | population: true |
| asm:omitted (c) | signal relative to residual variance: β^CᵀΣβ^C ≤ M_C σ_C², and n·min Σ_jj(β^C_j)²/(σ_C² log n) → ∞ | (a) | beta-min form, as BM(b) | computable from the population (§4, E8) |

### T4. SMC theorems (particle limit; no SL analog in this form) — **[DEFERRED]** (scope ruling 2026-11-27; kept for record)

SL's sampler results are almost-sure limits as the number of iterations → ∞ (supp. pp. 9–16).

**Delivered:**
- `prop:unbiased` (Result 5, row 3.5): given the frozen calibration, each island's Ẑ_r is exactly unbiased for Z, on every design. With W1-N1 it also gives E[Ẑ_r·PIP̂_rj | C] = Z·PIP_j.
- W3-SAMP, Thms D, LT♯, C, TR: consistency at a fixed budget as n → ∞, conditional on T1 (δ → 0) and on the start mass π₀(S₀).
- `thm:outputs` (row 3.6): rate ρ_n for Ẑ/Z and the reported PIPs. Its NL assumption holds on independent designs only.

**Missing:** consistency as N → ∞ (T16 is conjectured; card M1(f) only cites it).

**[Opus] Candidate T4a, a particle law of large numbers and CLT given the frozen calibration.** Fix the data and the calibration C (grid, T, L, kernels). As N → ∞:
- Ẑ_r/Z → 1 and PIP̂_rj → PIP_j almost surely;
- √N(PIP̂_r − PIP, Ẑ_r/Z − 1) ⇒ a centred Gaussian.

Its route is a standard Feynman–Kac application (Del Moral 2004; Chopin 2004 Thm 1), on a *finite* state space with bounded test functions and a fixed sequence of π-invariant kernels.

**Candidate T4b:** the island count R → ∞ at fixed N (T16(ii)): the Ẑ-weighted pooled PIP → PIP_j.

| label | content | class | source |
|---|---|---|---|
| EX-A, H-U | exact arithmetic; i.i.d. uniforms | (c) | standard idealisations, disclosed (`appendices.tex:131-186`) |
| finite Ω, m(S) > 0, ϖ(S) > 0 | — | (c) | automatic for the coded prior (cap K, ridge) |
| KERNEL | each coded move is π_φ-invariant (code audit N9) | (c) | code-checked (`W1-N1/STATEMENT.md` §2) |
| CAL / SI | calibration frozen on separate streams before the final run | (c) | true by construction in v3.1.1; **this is what makes T4a classical**. An in-run adaptive schedule would need Beskos, Jasra, Kantas & Thiery (2016, AAP) |
| START | exact draws from π₀ and exact Z₀ | (c) | code-checked |

Two caveats. These classes come from the SMC literature, not from regression-selection papers; the owner's (a) test does not fit them literally. And no S1/S2 evidence is needed for them beyond the Monte Carlo-error checks in §4, E7.

## 3. Sensitivity map

**Scope (2026-11-27):** only columns R1–R3 serve (1)–(3). Columns R4 and R5, and the rows on kernels, tempering and N/islands, are **[DEFERRED]**.

Ratings:
- **cheap:** constants only, or a one-line re-check;
- **moderate:** a named proof step is re-done along a known route;
- **route-breaking:** the current route fails, and a new argument or new assumption is needed.

Theorem keys:
- R1 = T1 (posterior concentration);
- R2 = T2 (dist);
- R3 = T3 (omitted);
- R4 = the SMC results (unbiasedness, fixed-budget consistency, T4a);
- R5 = the reported-model theorem (`thm:reported`).

Where each element enters, element by element: `TH_PREP_support/W2_ROUTES.md` §6.

| element → change | R1 | R2 | R3 | R4 | R5 | overall | what changes |
|---|---|---|---|---|---|---|---|
| **slab g = n → g = c·n** | cheap | cheap | cheap | cheap | cheap | **cheap** | Occam factor (cn+1)^{−1/2}: constants |
| **g → max(n,p²) or p^{2α}** (FLS benchmark; YWJ) | moderate | moderate | moderate | cheap | moderate | **moderate** | The Occam factor becomes (g+1)^{−1/2} ≈ p^{−1}. The rate statement, `rem:sharp` (lower bound 1/(1+√(g+1))), the (ND) constants and R5's visibility bracket (½ log(n+1) → log p) must be redone. Beta-min constants change only by a factor of A (p ≤ n^A). The YWJ route is closer for this choice. **It worsens under-selection** (larger per-variable penalty) |
| **slab → data-free V = τ²I** (ASI's V = 9I) | moderate | moderate (SL's Jiang route then applies) | route-breaking (the exact scale reduction R′ uses n(G+I)⁻¹ and b₀s_y²) | cheap | moderate | **moderate / route-breaking for T3** | the bound D_S ≤ (n+1)^{\|S\|} is lost, adding log factors |
| ridge +I → +cI, or no ridge with \|S\| < rank | cheap | cheap | cheap | cheap | cheap | **cheap** | Without the ridge, singular models must be excluded (YWJ's rank condition); still cheap |
| **size prior BB(1,p) → BB(1,c·p) or BB(a,b) with b ≍ p, a fixed** | cheap | cheap | cheap | cheap | cheap | **cheap** | per-variable ratio (k+a)/(b+…): constants |
| **→ BB(1,p^u), u > 1** (CvdV complexity prior) | cheap | cheap (also opens SL's sieve route) | cheap | cheap | cheap | **cheap** | A → uA in the constants. Increases the penalty, so under-selection gets worse |
| **→ BB(1,p^u), u < 1** (lighter) | moderate | moderate | moderate | cheap | moderate | **moderate** | [Opus] the multiplicity is no longer cancelled, leaving p^{(1−u)j} for the Occam factor n^{−λj/2} to beat. This needs roughly (1−u)A < ½ (S2: u > 0.72; S1 p = 5000, n = 500: u > 0.64). It becomes a new DIM-type condition, (c) or (b) |
| **→ BB(1,1)** | route-breaking | route-breaking | route-breaking | cheap | moderate | **route-breaking** | The multiplicity cancellation survives, but the geometric size tail 2^{−m} (T02(i), Lemma S) is lost. Only an Occam-plus-(ND) bound on sets up to K ≈ n/2 is left, which is not a refereeable assumption for p ≫ n. [Opus] the gain is only about log 2 per variable for small models, so it is not worth the cost |
| **cap K = ⌊n/2⌋ → c·n, n−2, or any K ≥ m_n + s₀** | cheap | cheap | cheap | cheap (b_X constant; re-check kernel guard) | cheap if K ≥ 2\|Q\|+32s₀+1 (L-feas) | **cheap** | Nowhere is the cap used as a residual-df bound (searched) |
| **cap → fixed K** (e.g. 50) | cheap if K ≥ m_n | cheap if K ≥ m_n | cheap | cheap | moderate (L-feas fails as n grows) | **moderate** | asymptotic statements need K → ∞ at least like log n |
| **cap removed (K = p > n)** | moderate | moderate | moderate | moderate | moderate | **moderate** | models with \|S\| ≥ n enter; the ridge keeps m(S) defined. Re-check the sparse-eigenvalue ranges and the kernel |
| **σ² prior → other fixed IG(a₀,b₀)** | cheap | cheap | cheap | cheap | cheap | **cheap** | constants c_IG, κ |
| **→ Jeffreys 1/σ²** (b₀ → 0) | cheap–moderate | cheap–moderate | cheap (scale invariant) | cheap | cheap | **cheap–moderate** | the envelope b₋ = b₀σ²/2 > 0 must be re-done at b₀ = 0 |
| **→ rate not data-scaled, or plug-in σ̂²** | cheap | cheap | **route-breaking** for R′ | cheap | moderate | **moderate** | T3's exact reduction needs the rate b₀s_y² |
| centring/scaling: divisor n vs n−1 | cheap | cheap | cheap | cheap | cheap | **cheap** | — |
| **→ no scaling, or unit-norm columns** | moderate | moderate | route-breaking | cheap | moderate | **route-breaking for T3** | couples with g (the slab is no longer normalised) |
| **kernel: add or replace moves** (informed, ASI-type, PARNI-type) | none | none | none | cheap if every move is π_φ-invariant (N9 audit); moderate for M2's Doeblin and stage-count constants | cheap unless LS0 changes | **cheap** | — |
| **tempering: pilot-frozen → in-run adaptive (same particles)** | none | none | none | **route-breaking for exact unbiasedness**; moderate for T4a (Beskos et al. 2016 gives consistency, not unbiasedness) | cheap | **moderate** | `prop:unbiased` becomes asymptotic only |
| N, islands, pooling weights, escalation tiers | none | none | none | cheap (T4a/T4b constants; TH01(i) R′_n) | cheap | **cheap** | — |
| **selection rule MPM ↔ HPM** | cheap (`lem:summaries`, deterministic) | none | cheap | cheap (W3-SAMP covers both) | cheap (R5 is stated for the HPM via LS0) | **cheap** | — |
| **→ PIP threshold q ∈ (0,1) fixed** | cheap (δ < min(q,1−q)) | none | cheap | cheap | cheap | **cheap** | SL ξ_q analog (SL1(b)) |
| **→ size-calibrated or F1-oriented rule** | moderate | none | moderate | moderate | moderate | **moderate** | cheap if the rule is a fixed function of the PIPs that returns S₀ when every PIP is within δ of its indicator |

**[Opus] What moves under-selection, from the formula in §1.**
- The per-variable cost is log[(2p−1−k)/(k+1)] + ½ log(n+1).
- Lowering it means a smaller g, or a lighter size prior, i.e. b ≍ p^u with u < 1. Both are **moderate**: rates and constants are redone, with a new DIM-type condition for u < 1.
- BB(1,1) changes the cost by only log 2 at small k, so it is **route-breaking for little gain**.
- A different reporting rule (threshold or HPM) is **cheap**.
- Any change keeps T1–T3 as long as the per-variable cost stays above about (1+ε) log p, enough to absorb the multiplicity.

## 4. Assumptions that can be checked on S1/S2, and what Engineering would log

**Already logged per fit** (`harness/diagnostics.R`; SPEC §10):
- beta_min_ratio (raw scale, √(log p/n));
- lambda_min_S0 (X_S₀ᵀX_S₀/n);
- max_abs_corr_null_true;
- snr_realised;
- π_S₀ (list view), gap_logpost, min_true_pip, max_null_pip, mass_size_gt_2s0;
- σ̂ (under the MPM);
- log Z per island, ESS per stage, top-50 models with F.

**No logging needed** (true by construction or computable from the settings):
- GL, GR/SGR, SP;
- DIM: A = log p/log n;
- the population EFS / NC / nec floor (AR(1): (1−ρ)/(1+ρ));
- s₀ log p/n. This is 0.06–0.17 on S1 but **0.69 on S2**, so S2 is far from the asymptotic regime, and its low-ν failures do not contradict T1.

**New items.** Everything except E7(b) and E8 can be computed **post hoc**: regenerate X and y from the stored seeds (`gen_data`), then re-score with the engine's own scorer `v3_score`. No new fits are needed. Priority as marked.

| # | assumption checked | quantity to log | why |
|---|---|---|---|
| E1 (P1) | beta-min / margin (BM, asm:margin), i.e. **the (b) candidate** | (a) For each j ∈ S₀, the partial t²_j from the OLS fit on S₀: θ̂_j² x_jᵀ(I−P_{S₀∖j})x_j/σ², and its population analogue nβ_j²(Σ_jj − Σ_{j,R}Σ_R⁻¹Σ_{R,j})/σ². Log the minimum and its argmin. (b) The per-variable price log[(2p−1−s₀)/s₀] + ½ log(n+1). (c) ‖(I−P_S)μ‖²/(σ² log n) for S = MPM, HPM and the best rival | Tests whether "min t² > 2 × price" predicts exact recovery. [Opus] a back-of-envelope estimate already matches S1: SNR 1 gives t² ≈ 12–16 against a threshold of 15–20 (fail); SNR 2 gives t² ≈ 47–64 (pass). It also explains bt2 through the margin (c) |
| E2 (P1) | sample floors EF / NC on small sets | λ_min(R̂_T) for T = S₀ ∪ (union of the top-50 models), and a greedy sparse-eigenvalue lower proxy at \|T\| = 2s₀ and at ⌈2(A+1)s₀+2⌉ (capped at n−1) | the fixed-design form of T1 and `thm:screen` |
| E3 (P1) | the T1 conclusion and rate: 1−π(S₀) vs √(log n/n) | **π(S₀) as the particle estimate** (pooled, Ẑ-weighted, and per island), not only the list view; the ratio (1−π̂(S₀))/√(log n/n) | (b) support for the rate constant; it separates the posterior from the list |
| E4 (P2) | T2: Hellinger contraction | Per fit, the posterior mean of β (sparse: entries with PIP > 10⁻³) and E[σ² \| y]. Per top-50 model, β̂_S and E[σ² \| S]. Theory computes d_H to the truth in closed form with the population Σ | an empirical counterpart of Result 2, including fits where selection fails (no beta-min needed) |
| E5 (P2) | the cap and the size tail | maximum \|S\| over the final particles and over all visited models; mass at \|S\| ≥ K−2 | checks that the cap never binds (needed if the cap changes) |
| E6 (P2) | σ² prior / envelope | σ̂² under the posterior (not only under the MPM), compared with the true σ² | the IG(0.01,0.01) constants |
| E7 **[DEFERRED]** | T4 particle limit | (a) Per-island PIP vectors, or their between-island SD on S₀ ∪ {PIP > 0.01}. (b) **Only if SMC-PERF runs N-ladders anyway:** PIP and log Ẑ at N, 2N and 4N on a few cells, to check Monte Carlo variance ∝ 1/N | (b) support for T4a/T4b; costs no extra runs if piggy-backed on SMC-PERF |
| E8 (P3, optional, needs refits) | T3 misspecification | hide k ∈ {1,2} true columns, refit on the candidates, and compare the MPM/HPM with the population S₀^C = supp(β_C + Σ_CC⁻¹Σ_CMβ_M) (on AR(1), the two neighbours of a hidden column) | the only way to get (b) evidence for T3. Owner-level compute decision |

Definitions follow the existing SPEC §10 conventions: X scaled with `scale()`, the true σ, and seeds only (never store X or y).

### 4a. Evidence received: Engineering TH-CHECKS P1 (E1–E3), 2026-11-27

Source: `_local/engineering/reports/S1S2/theory_checks/P1.md` (13,600 fits, post hoc; validation PASS to 1e-12). Read through the scope ruling (§0a).

- **E1 → [1], `asm:margin` (the (b) candidate).** "min t² > 2 × price" is a near-perfect **necessary** condition: 9 of 11,466 fits below it recover S₀ (sensitivity 0.993, AUC 0.989). It is **not sufficient**: P(exact | yes) = 0.95 on S1 and 0.45 on S2. The §4 back-of-envelope matches the **population** min t² (S1 SNR 1: 11.7/16.0 against 15.4/20.0; SNR 2: 46.8/64.1). It explains bt2 at ρ > 0: population min t² at ν = 6 drops to 24.5–26.8 (ρ = 0.35) and 4.9–6.7 (ρ = 0.7) against 2 × price ≈ 15–16, and margin_MPM > 0 in 96–100% of bt2 fits. Consequence for (1): state the margin condition with constant c ≥ 2 on the **population** t²; it is (b)-supported as a necessary threshold. The sufficiency gap on S2 is consistent with s₀ log p/n = 0.69 (non-asymptotic), not a counterexample.
- **E2 → [1], design form.** S1: sample sparse floors stay ≥ 0.06 at ⌈2(A+1)s₀+2⌉ and ≥ 0.12 at 2s₀, so the fixed-design EF holds there. S2: the greedy proxy (an upper bound) at ⌈2(A+1)s₀+2⌉ is about 1e-4 (n = 100) and 1e-5 (n = 50), so the **sample EF form is vacuous on S2**. Consequence: state (1) in the **random-design, population-EFS form** (headline `thm:post-random`), which holds analytically on both suites. Keep `thm:post-fixed` as secondary, with S1-only empirical support.
- **E3 → [1], rate (list view only).** S1, SNR ≥ 2: (1−π̂(S₀))/√(log n/n) ≈ 4.2–5.1, roughly flat from n = 500 to 1000. This is consistent with the T1 rate, with a constant of about 4.5 (two n values only). S2 is uninformative. The particle-level π̂ and E7 are not available. Both are **[DEFERRED]** (SMC limit); no refits needed for (1)–(3).
- **Still open for (1)–(3):** P2 (E4 Hellinger → [2]; E5 cap and E6 σ² → [1]–[3]).

## 5. Inconsistencies found (for the post-decision theory pass)

These are listed in `W1_STATEMENTS.md` §6; the ones that matter:
1. `SONG_LIANG_MAP.md` is stale: its rows 1 and 10–11 predate W3-DIST and the C-MIS delivery.
2. Card TH01 still shows N1 as "PROOF SKETCH" while the registry has it PROVED-CHECKED.
3. Card M1(f) *cites* a particle limit that T16 calls conjectured.
4. The freeze statuses and the main statuses differ for Results 1, 5 and 3.6 and for the expectation bound.
5. The ledger lists Prop-LB as a dependency of the expectation bound, but the proof uses it only for sharpness.
6. "g = n" vs ‖x_j‖² = n−1: a constants-only difference, documented nowhere.

None of these blocks TH-PREP. They should be fixed when the statements are re-issued after the engine decision.
