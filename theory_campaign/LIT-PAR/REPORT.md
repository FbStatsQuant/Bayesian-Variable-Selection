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
5. **COUNTEREXAMPLE (numerical, reproducible) to SaM-type feature splitting on a masked pair** (§3.1 G4, [n09]). In an LH-like
   design the exact posterior recovers S₀ in 20/20 datasets. Split-and-merge recovers it in 5/318 splits that separate the linked
   pair.
6. **What survives: our candidates, with no literature equivalent found.**
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
| **Zanella & Roberts 2019** TGS/wTGS, JRSSB; arXiv 1805.00541 [n04 5a] | All p tempered conditionals are computed in one vectorised pass; the chain is sequential | Exact (importance-weighted) | Thm 1: var(h, TGS) ≤ b²·var(h, GS) + b²·var_f(h). A *relative* bound against Gibbs only; no design condition, no absolute mixing bound | Applies to any X, but guarantees nothing absolute | Its parallel-within-step move is a candidate for Option B (§3.3) |
| **Jankowiak 2023** "BVS in a million dimensions", AISTATS (venue UNVERIFIED); arXiv 2208.01180 [n04 5b] | Subset wTGS on GPU; cost per iteration "sublinear in P"; chain sequential | Exact (weighted LLN) | Prop 1: a.s. consistency of weighted averages only; no rate | No guarantee under correlation (empirical correlated pairs only) | Practice precedent for GPU BVS |
| **Griffin, Łatuszyński, Steel 2021**, Biometrika; arXiv 1708.05678 [n04 5c] | Adaptive MCMC; sequential | Exact | Ergodicity and SLLN, no rate (also API-POS item 4) | — | Benchmark |

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

### 2.4 Data-splitting Bayes, variational / IBSS, scalable shrinkage samplers [n04]

| Work | Parallel; depth | Target | PROVED (conditions) | Holds for us? | Relation |
|---|---|---|---|---|---|
| **Scott et al. 2016** consensus Monte Carlo, IJMSEM 11:78–88 (abstract only; full text NOT read) | Shards of observations; one average | Approximate | None seen in the abstract | Splitting n = 200 into shards leaves n/K ≪ p; averaging γ-draws is not a model posterior | Not a model-space method |
| **Srivastava, Li, Dunson 2018** WASP, JMLR (arXiv 1508.05880); **Minsker et al. 2017** M-posterior, JMLR (arXiv 1403.2660) | Shards of observations; barycentre / geometric median | Approximate | Contraction for **continuous** parameters at fixed dimension, subset size → ∞, entropy/prior-mass conditions | No: fixed p, nothing for discrete model spaces | Not applicable |
| **Zhang, Lam, Lin 2018** "Robust and parallel Bayesian model selection", CSDA 127 (venue per RePEc); arXiv 1610.06194 | Shards of observations; geometric median of subset posterior model probabilities | A robust aggregate, not the posterior | Thms 1–3: Hellinger contraction; BMA selection for a **finite, fixed, non-nested** model set with N/R → ∞; exponential concentration in R | No: fixed D, non-nested (the BVS lattice is nested); simulation 5000 × 10, uncorrelated | The only data-splitting model-selection theory found; irrelevant at p ≫ n |
| **Li, Kang, Liu, Wu 2022**, Electron. Res. Arch. 30(5) | Data shards; local hierarchical Bayes; voting | Voting set | **No theorem** | AR(1) evidence (quoted): "With the increase of ρ, the number of selected noise variables increased, and the specificity ... decreased" | Empirical fragility |
| **Johndrow, Orenstein, Bhattacharya 2020**, JMLR 21(73); horseshoe | Sequential chain; threaded linear algebra | Continuous shrinkage posterior (exact chain) / approximate chain | Geometric ergodicity; TV(approx, exact) ≤ C√δ + O(δ); no rate in n, p | — | Not a model posterior |
| **Wang, Sarkar, Carbonetto, Stephens 2020** SuSiE/IBSS, JRSSB 82(5) | IBSS = sequential coordinate ascent over L effects; each single-effect fit is vectorised over p | Variational SuSiE posterior | Prop 2: convergence to a **stationary point** of the ELBO only. Quoted: "95% credible sets are not designed, or guaranteed, to have a frequentist coverage of 0.95". No 2023–2026 theory paper found | Designed for r > 0.99 LD; §4.1 has a masking-like example (the strongest marginal association is not causal), empirical only | Competes empirically under correlation; no guarantee |
| **Ray & Szabó 2022**, JASA; arXiv 1904.07150 | CAVI: sequential sweeps, order-sensitive | Mean-field VB | Thm 1: prediction/ℓ₁/ℓ₂ contraction if compatibility numbers φ(S₀) and sparse singular values φ̃(c\|S₀\|) are ≥ c₀; examples: "diagonal ..., orthogonal designs, i.i.d. ... random matrices and ... strong irrepresentability" | No: for a pair with ρ ≈ 0.99, φ̃(2) ≲ √(1−ρ) (our calc.) | Confirms the belief; approximation |
| **Yang, Pati, Bhattacharya 2020**, AoS 48(2) | No new algorithm | α-VB | Cor 4.2: rate √(s log(dn)/n) under a sparse-eigenvalue lower bound (supplement); no selection consistency | No (sparse eigenvalue → 0 with near-collinear pairs) | Same |

**Discrepancy to flag.** Notes 04 infers that ZYVR Condition 1(b) "likely fails" on masked LH because true variables are
marginally weak. That inference is **superseded by API-POS**. API-POS shows by exact enumeration (p = 16, 20) and a PROOF
SKETCH that on LH the masking is a property of the start π₀, not of π: every underfitted model has a strongly beneficial
addition. For the study scenarios S1–S6 (dilution-type masking), whether Condition 1 holds is **OPEN**.

**Literal-constant remark (notes 04).** The YWJ remark "s₀ log p ≤ n/32", quoted by ZYVR, admits no s₀ ≥ 1 at n = 200,
p = 1000. The theorems have unspecified universal constants, so they are asymptotic statements that are not checkable at the
study size. The same holds for our own asymptotic Thm 1 (T03♯, thresholds ≈ 2·10⁶).

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
- **G4. SaM-type splitting fails on a masked pair: COUNTEREXAMPLE (numerical) + PROOF SKETCH (analytic)** [n09],
  `scripts/sam_lh_demo.py`, seed 20261103.
  - Design: an LH-like design (our construction; p = 16, n = 200).
  - Result at β = 1: the exact full posterior recovers S₀ in 20/20 datasets. SaM recovers S₀ in **5/318** random splits that
    separate the linked pair (median Stage-I PIP of the masked variable 0.010), against 265/282 when the pair stays together.
    At β = 0.6 the separated count is 0/318.
  - The analytic sketch uses Song–Liang Thm 5: the masked variable has a zero within-split projection coefficient. The step
    "PIP → 0" is not verified against the paper.

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

## 4. Statements (PROTOCOL §2), evidence, failures

### 4.1 Refined statements proposed for the paper (positioning claims, not theorems)
- **S-GAP (CONJECTURE about the literature; evidence from §2).** Among published BVS methods, none simultaneously
  - (a) targets the exact model posterior with an unbiased evidence estimate,
  - (b) parallelises in communication-free width (islands), and
  - (c) has a proved sequential-depth (stage-count) bound on a correlated design whose start is masked.

  Every parallel BVS method with a theorem needs one of:
  - cross-split faithfulness (SaM);
  - weak correlation (DECO, BB-SSL, Ray–Szabó, Yang–Pati–Bhattacharya);
  - block-diagonal Gram (Papaspiliopoulos–Rossell);
  - large-n plug-in consistency (DFP);
  - fixed-dimension shards (WASP, M-posterior, Zhang–Lam–Lin).

  Exact parallel BVS samplers (Schäfer–Chopin, Ma, Jankowiak, Zanella–Roberts) have only qualitative or relative guarantees.
- **S-COUNTER (from the literature).** Under ZYVR Condition 1, a single informed chain has a p-free iteration bound with
  O(ps₀) parallel work per iteration. "Guarantees ⇒ sequential" is false as a general statement.
- **S-DEPTH (to be carried by our theorems; status inherited).**
  - v3 has depth D = T·L_r·(p + B + 2)·s(K) + O(2^B s(B)) + T·O(log RN) and width R·N.
  - T obeys the O-STAGES bounds (PROVED / PROOF SKETCH there).
  - Pooled error at fixed N decays as 1/R by T31(i) (standard; Whiteley–Lee–Heine).
  - A single-island relative-variance bound in the masked regime is **OPEN**.

### 4.2 Evidence
- One script: `scripts/sam_lh_demo.py`, outputs in `results/` [n09]; the G4 COUNTEREXAMPLE.
- Quoted statements from primary sources (notes 01–08), plus these published empirical findings:
- Coats et al. 2026: F1 falls to 0.126 at ρ = 0.99 with contiguous splits;
- Li et al. 2022: specificity falls with AR(1) ρ;
- Ma 2015: PIPs are "unreliable" under high correlation;
- Schäfer–Chopin 2013: parallel SMC at p ≈ 1000 on 64 CPUs.

### 4.3 What fails and why (routes tried)
- **Falsification route 1: find a feature-split method with a correlation-free guarantee.** DECO comes closest ("(almost) no
  assumptions"), but its constants depend on λ_min(Σ), it needs s² log p/n small and Gaussian random design, and it targets a
  lasso estimate. It fails as a counterexample to the exact-posterior claim.
- **Falsification route 2: data-splitting Bayes for model spaces.** Only Zhang–Lam–Lin, with a fixed non-nested finite model
  set. It fails.
- **Falsification route 3: an exact parallel sampler with guarantees.** Two candidates came close:
  - ZYVR parallelised: succeeds as a counterexample to "guarantees ⇒ sequential", but not to the three-part S-GAP (no
    unbiased Ẑ, no islands, unimodality condition);
  - pSMC (Liang et al. 2024): generic, and its uniform Doeblin condition fails for BVS.
- **Not attempted:**
  - reading the Song–Liang paper itself (paywalled; author slides used);
  - the DFP supplement;
  - the consensus Monte Carlo full text;
  - Lindsten/Kuntz journal versions;
  - most TCS proceedings pages.

## 5. Needs escalation
1. **Song–Liang Thm 5 and our reading of it** (screening keeps only variables with a nonzero projection coefficient within their
   split). This needs a check against the JRSSB text. The proposed G4 counterexample on LH depends on it.
2. **Whether T38(a) and T32(i) reduce to Mathews–Schmidler Thm 1.** If they do, they become corollaries, and the paper should
   say so.
3. **HQ method decision on depth** (§3.3 Options A/B). This is a method change if Option B is chosen.
4. **Venues and pages** marked UNVERIFIED in notes 03 and 04 need a bibliography pass.

## 6. Outside scope
- **ZYVR Condition 1 on S1–S6.** If it holds for the paper's own prior, a parallelised LIT-MH is a strong baseline for the study.
  Recommend an O-task to check Condition 1 by enumeration at small p, mirroring API-POS.
- **Single-island relative variance of Ẑ in the masked regime.** Whiteley–Lee–Heine and Syed et al. both say this controls the R
  needed. We have only one-sided M1–M3 results. This is the theorem a referee will ask for once the 1/R framing is used.
- **SuSiE as an empirical comparator under masking-like designs.** Its §4.1 example is of exactly our type.

## 7. Confidence card

| Target | Refined statement | True? | Provable at reasonable cost? | Crux | Method change? |
|---|---|---|---|---|---|
| Gap claim (paper thesis) | S-GAP, three-part form (§4.1), with "guarantees ⇒ sequential" dropped | medium-high (a literature claim can always be overturned by a missed paper; 2023–2026 coverage was by search, not exhaustive) | n/a (literature) | ZYVR + parallel scoring; Schäfer–Chopin; pSMC | no |
| Parallel scaling (S-DEPTH) | depth = T·L_r·(p+B+2) score evals, width R·N, error ∝ 1/R at fixed N | high (accounting) | high for the accounting; **low–medium** for a masked-regime single-island variance bound | single-island Var(Ẑ/Z) under a masked start | Option B (parallel-within-particle moves) is needed for "depth ≈ T up to log p" |
| T31(i) | Ẑ-weighted pooling consistent as R → ∞ at fixed N | high | already proved in the literature | unbiasedness under the frozen calibration (P6/P7) | no; cite Whiteley–Lee–Heine and Dai et al. |
| O-STAGES item 4 | √c·T* → L = Λ (Syed et al.) | high | known | — | no; cite |
| O-STAGES items 2–3 | coarse-grid T* = log₂A₀ + O(1); not in the literature | (as O-STAGES) | (as O-STAGES) | layer law (PROOF SKETCH there) | no |
| T38 masked-regime novelty | no published guarantee for SMC with a masked start on a correlated BVS family | medium-high | (as T38-RECORD) | μ⋆ exponentially small defeats generic bounds | no |

## 8. Sources actually read
Full lists with URLs and quotes are in `notes/03` (§"Sources actually read") and `notes/04` (§"Sources actually read").
Read directly by the main run:

- **Local PDFs:**
  - Papers/Core_bibliography/12 (Papaspiliopoulos–Rossell 2017);
  - 13 (Ma 2015);
  - 10 (Zhou et al. 2022);
  - 07 (Schäfer–Chopin 2013);
  - 24 (Le, Fay, Chopin, Vihola 2026; header and parallel remarks only);
  - 02 (Syed et al. arXiv 2408.12057v2).
- **arXiv PDFs:**
  - 1602.02575 (DECO);
  - 2011.14279 (BB-SSL);
  - 2609.20000 (Coats, Davies, Gupta 2026);
  - 2208.06672 (Mathews–Schmidler);
  - 1803.09365 (Marion–Mathews–Schmidler);
  - 2007.11936v3 (Dai–Heng–Jacob–Whiteley);
  - 2402.06173v2 (Liang et al. pSMC).
- **Other:**
  - https://www.stat.purdue.edu/~fmliang/STAT598Purdue/partI4.pdf (Liang's slides with the SaM theorems);
  - https://tr.soe.ucsc.edu/sites/default/files/technical-reports/UCSC-SOE-21-04.pdf (DFP).
- **Read by sub-sweeps** (verbatim quotes in their notes):
  - **notes 03:** Vergé et al. 1306.3911; Lindsten et al. 1406.4993; Kuntz et al. 2110.15782; Whiteley–Lee–Heine 1309.2918;
    Lee et al. 0905.2441; Syed et al. 1905.02939, 2408.12057; and the TCS papers listed there.
  - **notes 04:** Zhang–Lam–Lin 1610.06194; Li et al. 2022 (aimspress PDF); WASP 1508.05880; M-posterior 1403.2660;
    Johndrow et al.; SuSiE (JRSSB copy); Ray–Szabó 1904.07150; Yang–Pati–Bhattacharya 1710.03266; Zanella–Roberts 1805.00541;
    Jankowiak 2208.01180; Griffin et al. 1708.05678; Yang–Wainwright–Jordan 1505.07925.
- **Our branches read:** W8-SYNTH BRIEF, T38-RECORD T38_STATEMENT (head), API-POS REPORT §1, O-STAGES REPORT §1–2, W7-SEC
  REPORT (grep), F-REFINE ARCHITECTURE (grep), METHODOLOGY_v3 §§1, 6.3–6.6, 8–9.
- **Not read** (cited second-hand only, UNVERIFIED): the Song–Liang JRSSB full text; consensus Monte Carlo full text; the DFP
  supplement; Andrieu–Doucet–Holenstein 2010 (cited via Dai et al.); Gelman–Meng 1998 (cited via Syed et al.).
