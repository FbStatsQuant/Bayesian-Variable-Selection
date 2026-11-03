# LIT-PAR — REPORT: is there already a parallel, correlation-robust BVS with strong guarantees?

Run of 2026-11-03, branch `theory/LIT-PAR`. This is a literature task, and **no new theorem is claimed**. Status words follow
`theory_campaign/PROTOCOL.md`.
- A "PROVED" attributed to a paper means the paper states it as a theorem. Its proof was not re-checked here.
- All of our own items are **candidates**.

Source notes with verbatim quotes are in `notes/01`–`notes/08`; the report cites them as [n01]…[n08]. Every entry names the
file or URL actually read. **UNVERIFIED** marks anything seen only second-hand. Journal venues were mostly not checked on
journal pages; §4 says which.

Our registry IDs used below:
- T38(a), (b1-LH), (b2-LH), (c): `theory/T38-RECORD · T38_STATEMENT.md`;
- T32(i): cost, W5-LOCKBOOK / W7-SEC;
- T31(i): Ẑ-weighted island pooling;
- O-STAGES items 1–5: `theory/O-STAGES · REPORT.md`;
- API-POS: the rapid-mixing positioning;
- P6/P7: unbiased Ẑ under a frozen calibration.

---

## 1. Headline

1. **Verdict on the gap claim: TRUE WITH QUALIFICATIONS.**
   - Every parallel BVS method we found that has a theorem needs a design condition that strongly correlated or masked
     designs violate (§2), or else does not target the model-space posterior. The conditions are:
     - Song–Liang SaM: a nonzero *within-split* projection coefficient for each true variable;
     - DECO: well-conditioned Σ and s² log p/n small;
     - BB-SSL: low mutual coherence;
     - DFP: consistent plug-in estimates;
     - variational BVS: compatibility-type conditions.
   - We found **no** published method that combines all three of:
     - (i) the exact model posterior with an unbiased evidence estimate;
     - (ii) communication-free parallel width;
     - (iii) a proved bound on the sequential depth under a correlated design.
2. **The literal sentence "methods with guarantees are sequential" is FALSE in the work/depth sense. Do not print it.**
   - The strongest counterexample candidate is the informed chain of Zhou–Yang–Vats–Roberts–Rosenthal (ZYVR, JRSSB 2022). It has
     a *p-free* proved mixing bound, T_mix ≤ 800·max(nκ₁/c₁, 3s₀).
   - Each iteration scores O(p·s₀) neighbours, which the authors say "can be easily parallelized". So its depth is
     O(n log p) score rounds under ZYVR Condition 1.
   - API-POS found that Condition 1 holds on our own linked-hub (LH) family, with ZYVR's priors (PROOF SKETCH there).
   - Generic SMC theory also gives depth V·t that depends only on *local* mixing (Mathews–Schmidler 2024).
3. **Several of our ingredients are standard. Cite them as such, not as contributions.**
   - **Ẑ-weighted pooling of R independent SMC runs, consistent as R → ∞ at fixed N (our T31(i)):**
     - Whiteley–Lee–Heine (2016) §5.1 proves it;
     - Dai–Heng–Jacob–Whiteley (2022) eq. (4.8) states it;
     - Liang et al. (2024) prove "parallel strong scaling", MSE ≤ C/(NP), for non-communicating Ẑ-weighted islands, under
       global Doeblin mixing.
   - **Parallel tempered SMC for BVS on {0,1}^p:** Schäfer–Chopin (2013).
   - **Exact enumeration on correlation-clustered blocks, parallel over blocks:** Papaspiliopoulos–Rossell (2017). It is exact
     only for a block-diagonal Gram matrix, and otherwise a heuristic.
   - **The fine-grid stage law √c·T* → L (O-STAGES item 4):** this is the known thermodynamic-length / global-barrier result. Syed
     et al.'s Λ equals our L exactly for our bridge [n08].
4. **Self-critique: v3's per-particle depth is Θ(p) score evaluations per move round, not O(1).**
   - A round is p + B + 2 elementary steps run sequentially within each particle.
   - So "depth = stage count T" holds only if a round counts as one unit. Counted in score evaluations, the depth is
     T·L·(p + B + 2).
   - That is worse in p than a parallelised ZYVR chain. Either state the depth honestly, or change the move kernel
     (§3.3; method decision for HQ).
5. **What survives: our candidates, with no literature equivalent found.**
   - **(a) Coarse-grid stage-count laws** (O-STAGES items 1–3): T* = O(1) favourable; log₂A₀ + O(1) for a masked crossing,
     governed by the *start's* masking depth A₀ and not by the barrier Λ.
   - **(b) Guarantees in the masked-start regime** (T38 (b1-LH)/(b2-LH)). Generic SMC complexity bounds degrade
     exponentially there through μ⋆ = the minimal mode mass across stages.
   - **(c) The composition** "exact correlation-block start → exact-target SMC bridge → unbiased Ẑ". Its pieces exist separately
     (Papaspiliopoulos–Rossell; Schäfer–Chopin), but we found nothing that composes them with theorems.

---

## 2. Annotated table

Our design context:
- **LH:** the linked-hub family. On LH the truth is masked under the start π₀ but not under the posterior (API-POS).
- **Study designs:** n = 200, p ∈ {500, 1000}, scenarios S1–S6, strongly correlated. At n = 200 all errors are statistical
  (S-ELS).

"Holds for us?" judges whether the paper's *conditions* plausibly hold on these designs.

### 2.1 Feature-splitting / divide-and-conquer over predictors

| Work | Method; parallel; depth | Target | What is PROVED (conditions) | Holds for us? | Relation to ours |
|---|---|---|---|---|---|
| **Song & Liang 2015**, JRSSB 77(5):947–972 [n02]. Theorems read from author slides; paper paywalled | SaM: split predictors into K groups; Stage-I BVS per group (SAMC, sequential MCMC) in parallel; merge; Stage-II BVS. Depth = one subset MCMC + one merged MCMC | Posterior **restricted** to the merged set S̃; not the full posterior | Posterior consistency (Hellinger) under rate conditions and (A1). Sure screening for "identifiable" predictors (B1), which "controls the severeness of multicollinearity". Misspecified-subset Thm 5: on subset s, π(s̃ ⊂ ξ \| D_s) → 1, where s̃ = nonzero coordinates of the **projection** of the truth onto X_s. Asymptotic in n | **No** on masked designs. A true variable whose within-split projection coefficient cancels (partner in another split) is screened out at Stage I and is unrecoverable. Random splits separate LH pairs | Complementary. Confirms Felipe's belief. Our blocks keep correlated variables together; SaM's theory neither assumes nor analyses clustering |
| **Wang, Dunson, Leng 2016** DECO, NeurIPS; arXiv 1602.02575 [n02] | Global decorrelation X̃ = √p (XXᵀ + rI)^{-1/2} X (one synchronised O(n²p) step); then lasso per feature block in parallel | Lasso point estimate | Thm 2: if p > c₀n and 64C₀²A²s² log p/n ≤ 1, sup-norm and ℓ₂ rates plus sign consistency. Needs X ~ N(0, Σ); constants depend on λ_min, λ_max(Σ) (Lemma 7) | **No.** Random Gaussian design with well-conditioned Σ; s² log p/n not small at n = 200; no posterior | Complementary (point estimation) |
| **Gutierrez & Guhaniyogi 2022**, Technometrics (venue UNVERIFIED; read UCSC-SOE-21-04) [n06] | DFP: streaming shards; parameter blocks sampled in parallel from pseudo-conditionals that plug in point estimates of other blocks | Pseudo-posterior | "pseudo posterior densities over time being arbitrarily close to the full posterior as the data size grows", **assuming** the plug-in estimators are consistent ("validated empirically"). Supplement not read | **No.** Large-n streaming regime; plug-in consistency is what fails at fixed n with strong correlation | Unrelated regime |
| **Papaspiliopoulos & Rossell 2017**, Biometrika; arXiv 1606.03749 [n01] | Exact BMA and best subsets for block-diagonal XᵀX; blocks "processed in parallel"; for general X, spectral-clustering blocks plus an iterative heuristic | Exact posterior **iff** XᵀX is block-diagonal (Zellner prior) | Props 3.3–3.4: best model of each size and exact posterior quantities under block-diagonal XᵀX. General designs: "heuristic optimisation", no guarantee | Block-diagonality fails (cross-block correlation) | **Threat to novelty of the start** (correlation-clustered exact blocks). Complementary: v3 adds the bridge to the exact posterior |
| **Coats, Davies, Gupta 2026**, arXiv 2609.20000 (Sep 2026) [n02] | Row + column splitting, SaM-like screening per batch, consensus; parallel | Consensus selection | No theorem | n/a | Recent evidence for fragility: contiguous splits' F1 falls to 0.126 at Toeplitz ρ = 0.99. They recommend putting correlated columns in **separate** batches, the opposite of our blocks and harmful under masking |
| **Ma 2015** LIPS, JASA; arXiv 1403.2397 [n01] | SMC over a probabilistic forward-stepwise latent chain of length p; "islands" on L cores "in an (embarrassingly) parallel fashion". Depth O(p) steps | Exact (importance sampling, Horvitz–Thompson) | Thms 1–3: Markov/pFS representation exists; exact propagation is intractable. Consistency as N → ∞ only | No rate. Author reports PIPs "unreliable" "due to the high predictor correlation" | Prior instance of islands for exact BMA. Partial threat to "parallel + exact is new" |

### 2.2 Samplers for BVS: sequential with guarantees, or parallel-friendly

| Work | Parallel; depth | Target | PROVED (conditions) | Holds for us? | Relation |
|---|---|---|---|---|---|
| **Zhou, Yang, Vats, Roberts, Rosenthal 2022**, JRSSB 84(5) [n06]; local PDF | One informed chain (LIT-MH). Neighbour scores per step are parallel (authors' remark). Depth O(n log p) | Exact posterior (MCMC) | Thm 1: T_mix ≤ 800·max(nκ₁/c₁, 3s₀) if n = O(p), s₀ log p = O(n), κ = O(s₀) and Condition 1 (no underfitted model without a p^{c₁}-better addition; overfitted additions penalised by p^{-c₀}) | Per API-POS: on LH (iid, with ZYVR's priors) Condition 1(b) holds (PROOF SKETCH). For **our** prior and cap it fails as stated | **Strongest counterexample candidate** (§3.2). Overlaps API-POS |
| **Yang, Wainwright, Jordan 2016**, AoS (UNVERIFIED here; read via API-POS) | Sequential RW-MH | Exact | Mixing O(p n s₀² log p) under restricted-eigenvalue-type conditions | as API-POS | Benchmark "sequential with guarantees" |
| **Schäfer & Chopin 2013**, Stat. Comput. [n06]; local PDF | Tempered SMC on {0,1}^p with a global independence kernel; "run many evaluations of π in parallel during the move step" | Exact (SMC) | No BVS theorem | n/a | **Threat to novelty** of "parallel SMC for BVS". Do not repeat its claim "No analogue speed-up ... in the context of Markov chains" (contradicted by informed proposals) |
| **Nie & Ročková 2023** BB-SSL, JASA; arXiv 2011.14279 [n05] | Independent MAP optimisations on reweighted data: "unapologetically parallelisable"; depth = one SSL optimisation | Bootstrap **pseudo-posterior** | Thms 4.2–4.3: near-minimax contraction if, among others, max_{i≠j}\|x_iᵀx_j\| ≲ λ₀²/n (low coherence) plus a restricted-norm condition | **No** (strong correlations) | Confirms Felipe's belief |
| *Rows 2.2b (SuSiE, variational BVS, scalable horseshoe, data-splitting Bayes): see §2.4, from notes/04* | | | | | |

### 2.3 Parallel SMC / tempering theory (generic, not BVS) [n03, n05, n07, n08]

| Work | What is PROVED (conditions) | Relevance |
|---|---|---|
| **Whiteley, Lee, Heine 2016**, Bernoulli 22(1) (DOI from arXiv header) | §5.1: with q particles per run fixed and s → ∞ independent runs, the Ẑ-weighted pooled estimator → π_n(φ) a.s.; plain averaging is biased; relative variance of pooled Ẑ = (1/s)·that of a single run; it can grow exponentially in the horizon at fixed q | **T31(i) is this.** Cite it. The 1/R variance identity is the honest cost statement |
| **Dai, Heng, Jacob, Whiteley 2022**, JASA; arXiv 2007.11936 | §4.2 eq. (4.8): Σ_r Ẑ_r π_r(φ)/Σ_r Ẑ_r → π(φ) as R → ∞ for any fixed N, via Andrieu–Doucet–Holenstein (2010); runs "on parallel machines without communication" | Same; textbook-level statement |
| **Liang, Lohani, Lukens, Kirby, Searles, Law 2024**, arXiv 2402.06173v2 (peer review UNVERIFIED) | Thm 3.1: MSE ≤ C_φ/(NP) for P non-communicating Ẑ-weighted islands under bounded likelihood (C.1) and a uniform Doeblin minorisation of every kernel (C.2). Time cost independent of P: "parallel strong scaling" | **Threat to the phrasing** "fixed depth, width → ∞". Its C.2 with p-free ρ fails for BVS; our value is BVS-specific constants and depth |
| **Vergé, Dubarry, Del Moral, Moulines 2015**, Stat. Comput.; arXiv 1306.3911 | Independent islands with **plain** averaging: bias O(1/N₁), not reduced by more islands; variance ∝ 1/(N₁N₂); interaction helps when N₁ is small | Contrast: our pooling is Ẑ-weighted, not plain |
| **Lindsten et al. 2017**, JCGS; **Kuntz, Crucinio, Johansen** (AAP; arXiv 2110.15782) | D&C-SMC: Ẑ unbiased for every N; CLT; running time O(N·depth(tree)) with enough processors | Depth-as-tree-height accounting precedent. No R → ∞ pooling theorem |
| **Mathews & Schmidler 2024**, AAP 34(1); arXiv 2208.06672 | Thm 1: SMC error ≤ ε w.p. ≥ 3/4 if N ≳ poly(V, W, Z, 1/μ⋆)/ε² and t ≥ max local (restricted-kernel) mixing times. **Only local mixing needed**; μ⋆ = min mode mass over all stages | Template for "depth = V·t_local, width = N". Under a masked start μ⋆ is exponentially small, so the bound is useless there. That regime is ours (T38 (b1-LH)/(b2-LH)). T38(a) and T32(i) are BVS instances of the favourable side |
| **Marion, Mathews, Schmidler**, arXiv 1803.09365 | Finite-sample SMC bounds needing global stage mixing; within a log factor of MCMC | Generic |
| **Syed, Bouchard-Côté, Chern, Doucet**, arXiv 2408.12057v2 (2025) | Thm 3: lim_{T→∞} T·Var[Ẑ/Z] = E(φ)/N ≥ Λ²/N. Λ = ∫ sd_β(score) dβ for MCMC kernels; stable regimes need T ≳ Λ. Idealised performance model (temporal and particle independence, efficient local exploration) | **Λ = O-STAGES' L exactly** [n08]: O-STAGES item 4 is a known fact. Items 1–3 (coarse grid, T* = log₂A₀ + O(1) with L ≤ π) are **not** in it and contrast with it |
| **Syed et al. 2022** NRPT, JRSSB; arXiv 1905.02939 | Round-trip rate → 1/(2 + 2Λ); "adding more cores ... will never be harmful, but does have a diminishing return" | Width saturation at about Λ |
| **Lee, Yau, Giles, Doucet, Holmes 2010**, JCGS | Empirical GPU speedups of 35–500×; move steps "trivially parallelizable", resampling the sync point | Practice only |
| TCS parallel sampling (Feng–Sun–Yin 2017; Feng–Hayes–Yin 2021; Anari et al. 2021, 2023, 2024; H. Lee 2024; Fischer–Ghaffari; Miao–Yin 2026) [n03 Part C] | Polylog or √n depth for structured or high-temperature models (counting oracles, isoperimetry, Dobrushin/spectral conditions); Ω(log n)/Ω(diam) lower bounds only in the LOCAL model | No BVS posterior covered. Use their work/depth reporting style. Do **not** claim a depth lower bound |

### 2.4 Data-splitting Bayes, variational / IBSS, scalable shrinkage samplers
(filled from `notes/04_datasplit_scalable_bvs.md`; see below)

---

## 3. Gaps, threats, phrasing

### 3.1 Gaps: what nobody has proved that we prove or could prove
- **G1.** A guarantee for an exact-target parallel sampler for BVS whose start is *masked* (truth's basin has exponentially small
  start mass), on an explicit correlated family.
  - Generic theory (Mathews–Schmidler) needs μ⋆ ≥ 1/poly. Syed et al. assume efficient local exploration. pSMC (Liang et
    al.) assumes uniform Doeblin mixing.
  - Ours: T38 (b1-LH) with LS0, and (b2-LH) under STAB-LH (XF-VERIFIED by A-REV7 on an explicit subfamily). Candidates only.
- **G2.** Stage-count laws at a *coarse, production* ESS threshold: T* = O(1) favourable, log₂A₀ + O(1) masked, O(log log n)
  on LH masking (O-STAGES items 2–3).
  - The literature has only dense-schedule asymptotics in Λ.
  - The contrast "Λ = L ≤ π while T* → ∞" is a clean new observation (O-STAGES item 4 with [n08]).
- **G3.** A theorem tying the depth of a parallel BVS sampler to a design-dependent quantity (A₀, a property of the start built
  from correlation blocks). Nobody analyses correlation-clustered splitting. SaM and Coats et al. split arbitrarily or
  anti-cluster; Papaspiliopoulos–Rossell cluster but give no guarantee off block-diagonality.
- **G4 (could prove, cheap).** A "no-split" impossibility contrast: on LH, any split that separates a linked pair makes SaM
  Stage I discard a true variable with probability → 1. This would be a short COUNTEREXAMPLE to SaM-type guarantees on our
  family. Its premise would be Song–Liang Thm 5 read in the paper itself. **OPEN; not attempted here.**

### 3.2 Threats: results that make ours standard, weaker or redundant
- **TH1 (high). ZYVR + parallel neighbour scoring.**
  - What it is: a single chain with a p-free proved iteration bound and per-iteration width O(ps₀).
  - Why it matters: on LH it applies with ZYVR's priors (API-POS). It undercuts "guarantees ⇒ sequential" and any claim that
    our depth is better in p.
  - Counter-arguments:
    - (i) Condition 1 excludes posterior multimodality, such as competing models at n = 200 (S-ELS posterior misses).
    - (ii) It gives no unbiased Ẑ and no communication-free width beyond one step.
    - (iii) It does not apply as stated to the paper's prior and cap (API-POS item 3).
  - Paper action: we must compare with it explicitly.
- **TH2 (high). T31(i) is standard** (Whiteley–Lee–Heine 2016 §5.1; Dai et al. 2022 eq. 4.8; Andrieu–Doucet–Holenstein 2010).
  - Only the method-specific hypothesis is ours: unbiasedness of v3's Ẑ under the frozen calibration (P6/P7).
- **TH3 (medium). "Parallel strong scaling" for Ẑ-weighted islands is published** (Liang et al. 2024).
  - Keep our claim BVS-specific and quantitative.
- **TH4 (medium). O-STAGES item 4 is the thermodynamic-length result** (Syed et al.; Gelman–Meng 1998).
- **TH5 (medium). Novelty of the components.**
  - Parallel tempered SMC for BVS: Schäfer–Chopin 2013.
  - Correlation-block exact enumeration in parallel: Papaspiliopoulos–Rossell 2017.
  - Islands for exact BMA: Ma 2015.
  - Our novelty is the composition plus theorems, not any component.
- **TH6 (medium). Mathews–Schmidler 2024 makes "SMC needs only local mixing + bounded stage ratios" standard.**
  - T38(a) (favourable) and T32(i) should be framed as BVS verifications of that template.
  - Cite it; check whether T38(a)'s proof could simply invoke their Thm 1.
- **TH7 (self). v3's Θ(p) per-round depth (§1 item 4).**

### 3.3 How to phrase the parallel-scaling claim so a referee accepts it
1. **Define the cost model explicitly.** Unit = one score evaluation s(k).
   - **Work** W = R·N·T·L_r·(p + B + 2)·s(K), plus tables Σ_b 2^{|C_b|}. Here L_r = move rounds per stage.
   - **Depth** D = (table depth 2^B·s(B)) + T·L_r·(p + B + 2)·s(K) + T·O(log(RN)) for resampling.
   - **Width** = R·N particles (and p/B blocks for the tables).
   - State that D is **independent of R** and that R needs no communication. (Whiteley–Lee–Heine; Dai et al.)
2. **The carrying theorem.**
   - "Depth = O(T·L_r·p)" combined with O-STAGES' T bounds gives D = O(p) on favourable BO, O(p log n) on proxy masking, and
     O(p log log n) on LH masking (O-STAGES items 3 and 5). The constant L_r must be fixed by the method.
   - T31(i) / Whiteley–Lee–Heine handles the error at fixed N as R → ∞: relative variance of pooled Ẑ = single-island
     relative variance / R.
   - What is **missing** is a bound on the single-island relative variance in the masked regime. Without it, "R → ∞ fixes
     everything" may need exponential R (Whiteley et al.'s own warning).
3. **Do not claim depth O(T) unless the kernel changes.**
   - Option A (no method change): phrase the claim as "depth = T stages of p-step rounds; T = O(1)–O(log n) by O-STAGES".
   - Option B (method change): make rounds parallel within a particle, e.g. informed or tempered-Gibbs moves that score all
     p neighbours at once. Then D = O(T·L_r·log p), and "depth = stage count up to log p" becomes true.
   - Either way, compare with parallelised LIT-MH, whose depth is O(n log p).
4. **What to measure.**
   - Strong scaling: wall time and error vs number of workers at fixed total work.
   - Weak scaling: R grows with workers, error ∝ 1/R.
   - Report T vs n and p for S1–S6. Report the critical path in score evaluations, not only wall time.
   - Report single-island relative variance of Ẑ (the 1/R constant).
   - Report the comparator ZYVR LIT-MH with parallel neighbour scoring: iterations × log p.
5. **Wording to avoid:**
   - "methods with guarantees are sequential";
   - "no analogue speed-up for MCMC";
   - "first parallel exact BVS";
   - "depth = T" without the per-round factor.
6. **Wording that survives:**
   - "We know of no BVS method that targets the exact posterior, scales out in communication-free width with consistent
     Ẑ-weighted pooling, and has a stage-count (depth) bound proved on a correlated design with a masked start.
     Feature-splitting methods with guarantees require cross-split faithfulness or weak correlation."
   - Plus the citations of §2.

---

## 4. Sources actually read
(see §4 at the end, compiled after notes/04)
