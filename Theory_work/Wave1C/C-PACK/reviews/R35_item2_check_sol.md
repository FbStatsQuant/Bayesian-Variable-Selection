# R35 — independent mathematical review of Item 2

**Verdict: VERIFIED-WITH-AMENDMENTS.** The replacement probability inputs suffice, including for GEN's full allowed slowly growing p range. The literal event-identity assertion needs PXN's exact-branch convention, which I2 currently omits. There is also a false statement of logarithmic comparability and a small citation cleanup. These are repaired below without adding a probabilistic assumption. I found no counterexample to the repaired asymptotic assertion or to the operator-norm argument.

Reviewed object: `Theory_work/Wave1C/C-PACK/lemmas/I2_LHiid_unconditional.md` (84 lines). This is an independent check of the transfer and rate substitution, not a fresh certification of all GEN lemmas or of GEN(d)'s Lemma SEL. No source, registry, skill, or git state was changed. Only the requested R35 review and numerical files were written under C-PACK.

Path abbreviations used below:

- I2 = `Theory_work/Wave1C/C-PACK/lemmas/I2_LHiid_unconditional.md`.
- GEN = `Theory_work/Wave1/W1-GEN/`; PXN = `Theory_work/Wave1/W1-PXN/`.
- PX = `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/API-PXNGAP/PROOF.md`.
- W7 = `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/W7-PART/PROOF.md`.
- CORE = `Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/core/`.

## Numbered findings

### 1. MAJOR — the claimed identity omits the exact-branch definition repair

**Locations:** I2:14-16,43,51-58; GEN/STATEMENT.md:37-38; PXN/FINAL_PROOF.md:12-15; PXN/STATEMENT.md:103-106; PXN/lemmas/R_branch_repair.md:28-40; CORE/v3_fit.R:125-146.

**What is wrong.** I2:58 asserts, exactly:

> ℛ_n is PXN's 𝒜_n (same family, same partition algorithm, same B_n, same SIZE; §3).

But GEN/STATEMENT.md:37 calls its blocks "the method's actual partition", whereas PXN/FINAL_PROOF.md:12 explicitly adopts the "Exact-branch convention". In PXN/lemmas/R_branch_repair.md:33 the objects are:

> objects computed from the data on **every** branch (hypothetical when

The next line continues "the actual run takes the exact branch)." This convention is substantive for the claimed domain. The production exact branch returns at CORE/v3_fit.R:136; setup and assignment of blocks occur only at :138-146. Thus actual-built blocks do not exist there. GEN's L5_assembly.md:35-37,46-47 correctly handles discovery on exact runs but does not explicitly supply a hypothetical partition for its separate recovery event.

**Counterexample to literal actual-object identity.** For n sufficiently large, set

    g=9, c=1, v=0, rho=.7, psi=.5,
    p_n=9 max{9, ceil(log_2 log_2 n)}.

Then p_n is a multiple of g, p_n→∞, 18≤p_n≤n (eventually), and 9≤B_n≤16<18, so SIZE holds. Once K=p_n,

    sum_{k≤K} choose(p_n,k) = 2^{p_n} ≤ 2^9 (log_2 n)^9,
    (5H_0+4N_0)p_n ≥ 4np_n.

Consequently exact dispatch occurs eventually; it does not build an actual partition. Treating absent blocks as an empty collection would even make actual recovery false with probability one. This is a definitional counterexample, not a counterexample to recovery for make_blocks. The assumption p≥18 does not fix it. The sequence can start at a later finite index to meet all standing inequalities.

**Fix text (insert before Lemma I2, and carry into the proposed GEN wording):**

> Throughout this lemma, blocks mean the deterministic `make_blocks(X,B_n)` partition, defined for every design, hypothetically when the production run dispatches to exact enumeration, as in W1-PXN `lemmas/R_branch_repair.md` §3 and `FINAL_PROOF.md` §0. The events ℛ_n and PXN's 𝒜_n concern this same data function; equality of partitions ignores their enumeration labels. Block tables and start objects used for the theoretical argument have the same hypothetical interpretation. On the exact branch, once s₀≤K, enumeration already scores S₀, so that branch contributes zero to D_n; no actual block construction or LS0 execution is needed for that conclusion.

With this convention the claimed event identity and both recovery bounds are valid on the entire allowed p range. Do not add p≥n^a. The amendment is necessary to justify the literal identity as written; it requires no new probability proof and no change to the consistency conclusion.

### 2. MINOR — one-sided logarithmic domination is called equality of orders

**Location:** I2:76-78, especially :77.

**What is wrong.** The parenthesis says, exactly:

> (since log p ≤ A log n, these are the same orders up to A)

The inequality does not imply two-sided comparability. For the sequence in finding 1, log p_n is of order log log log n and log p_n/log n→0. The new concentration radius can therefore be much larger than the old one. I2:71-73 already correctly recognizes this for (b), but the quoted parenthesis contradicts it for (d).

**Effect.** No failure of the substitution results: every relevant bound in (d) still vanishes, as checked below. In particular the leakage perturbation becomes O(log n/n), which is still small enough after multiplication by n in the exponent calculation.

**Fix text (replace the parenthesis and following rate explanation):**

> Since log p≤A log n, the new bound is a possibly weaker upper rate; the two logarithms need not be comparable. With e_n:=δ_n=O(√(log n/n)), the partial-correlation perturbation is O(e_n²)=O(log n/n). Combining it with the unchanged fixed-family bound |ρ_{T₀,l}|=O(√(log n/n)) gives an exponent error O((log n)^{3/2}/√n+(log n)²/n)=o(1). All other cited uses require only e_n=o(1) or L′_n e_n=o(1).

An optional alternative avoids any weaker-rate substitution: CR's general δ inequality, at δ=32√(3 log p/(n−1)), gives failure at most 3/p→0. Since log p≤A log n, this δ is eventually ≤2 and is O(√(log p/n)). Thus the original GEN concentration rate can itself be proved from CR; summability is unnecessary for GEN's use. This is an additional direct derivation, not an upgrade to the archive's cited [CONC] status.

### 3. NIT — several source anchors are shifted

**Locations:** I2:16,26,42,61.

**What is wrong / fixes:**

| I2 location | Cited anchor | Current correct anchor |
|---|---|---|
| :16, block definition | GEN/STATEMENT.md:36-37 | :37-38 |
| :26, definition of PXN's 𝒜_n | PXN/FINAL_PROOF.md:16-17 | :14-15 (definition at :15) |
| :42, p range in PX | PX:44 | PX:41 |
| :61, F4 and its displayed lower bound | PX:57 | PX:56 |

The cited statements exist and have the claimed content. No mathematical counterexample results. Replace those anchors; the status quotations checked below do not need alteration.

## Event and model audit

With finding 1's explicit convention, GEN's ℛ_n is exactly PXN's 𝒜_n, as events on the same Gaussian design law. GEN's overall good-design event, also named 𝒜_n at L6_instances.md:67, is a different event: it is an intersection of five events. These two uses of the letter 𝒜 must not be conflated.

| Component | Source check and conclusion |
|---|---|
| Design family | GEN/lemmas/L6_instances.md:44-47 imports PX:36-60. PXN/STATEMENT.md:13-20 imports the same family: fixed g,c,v,rho,psi_i and signal coefficients; p=G_ng; rank-one hub links, with cross correlations 0, psi_i, rho psi_i, rho² psi_i. No substitution of constant cross-group correlation is permissible. |
| Parameter range | PX:38-41 and PXN/STATEMENT.md:13-15 require fixed A≥1, 18≤p_n≤n^A, p_n→∞. GEN's abbreviated heading inherits these from the explicitly cited family. There is no lower polynomial growth bound. Fixed c and v also mean enough groups to contain the signal units, eventually. |
| Raw versus standardized truth | GEN/lemmas/L6_instances.md:46-47 explicitly uses fixed raw theta, mu=CX^r theta and theta*=D_x theta. These agree with PX:48-50,62-64 and PXN/STATEMENT.md:18,24. Replacing theta* by fixed coefficients on standardized columns would invalidate population masking; the reviewed I2 does not make that replacement. |
| Correlation | Centering and dividing columns by their positive sample SD gives Pearson correlation X'X/(n−1). CORE/v3_blocks.h:8-16 explicitly normalizes the Gram diagonal too. Exact-real columns have norm² n−1, so this is the same r-hat used by CR. Constant-column exceptions have Gaussian probability zero. Standardizing the response does not enter partition recovery. |
| Algorithm | SoP/sections/02_method.tex:187-192,205-206; CORE/v3_blocks.h:39-44,121-143; W7:15-24 agree: complete linkage on 1−abs(r-hat), sorted-union lex merge ties, smaller-minimum-index child first, top-down **size** cut, and whole-cluster next-fit in that traversal order. No height threshold or neighbour-graph threshold is used. |
| B and SIZE | B_n=min(floor√n,floor√p,16), g≤B_n<2g eventually, identically PX:52-53 and PXN/STATEMENT.md:20. Since n,p→∞, the eventual g range is 9..16. At a particular finite n the actual B formula must still be used. |
| Onset | Repaired (R-b) applies at any n≥5 satisfying SIZE. I2(i)'s n≥max(5,n₁) is sufficient for its exponential bound. The extra inequality in (R-c) is needed for the p^{-C} assertion, which I2 does not require. I2(ii) retains both δ_n≤2 and L′_nδ_n≤λ₀/2. |

Strict global separation implies every group is a dendrogram node before any cross merge. SIZE retains exactly those nodes and makes packing two groups impossible. This direct argument is PXN/lemmas/R_branch_repair.md:20-26; it bypasses W7's defective A0(c). It needs neither A2 nor a choice of the original arbitrary-t false inequality.

## Audit of all relevant GEN dependencies

I searched GEN's Markdown statement and proof files, then checked the occurrences in context. The substantive Theorem B/R use is L6_instances.md:68-69, followed by pointwise replacement of group objects by block objects on ℛ_n at :80-82. The other occurrences are declarations of the same dependency: STATEMENT.md:129-131,172-173; lemmas/00_MAIN.md:38-39; L6_instances.md:5,83; and REPORT.md:22,65,98. They introduce no further mathematical use.

GEN does **not** require a recovery rate, summability, a bound uniform over growing A, or the original false chain S(t)≤K_n for every t. GEN's tails and exponential moments at L6:53-66,74-79 are for fixed group families under their unconditional laws. Recovery is intersected afterward. The good-event probability follows from a finite union bound; nothing multiplies an uncontrolled moment by the recovery-failure probability. The only imported recovery fact needed is P(ℛ_n^c)→0 for each fixed family and fixed A.

C4 (GEN/STATEMENT.md:115-120 and L5_assembly.md:57-82) does need every deterministic design sequence in the chosen event to meet common constants and deterministic envelopes. Replacing the Gram event by CR's explicit event preserves those requirements. The bounds are pointwise on that event; no extra probabilistic uniformity theorem is needed.

## I2(ii), the cutoff, and concentration substitution

Let E_n={max_{j<k}|r-hat_jk−Σ_jk|≤δ_n}. CR_corr_tails.md:32-39 gives P(E_n^c)≤3n^{-2} when p≤n^A and δ_n≤2. All design families at issue have positive-definite population correlation matrices. Diagonal errors are zero. For every T simultaneously, with no additional union bound,

    ||R-hat_T−Σ_T||_op ≤ ||R-hat_T−Σ_T||_{∞→∞}
                         ≤ (|T|−1)δ_n ≤ |T|δ_n.

The first inequality is valid here because the error matrix is symmetric; its spectral norm is its spectral radius, bounded by the maximum absolute row sum. Population interlacing gives λ_min(Σ_T)≥λ_min(Σ)≥λ₀, where I2 defines the fixed lower constant λ₀=(1−psi_bar)(1−rho). Weyl then gives λ_min(R-hat_T)≥λ₀−L′_nδ_n≥λ₀/2. The original PX notation λ₀:=λ_min(Σ) differs from I2's explicit lower-bound constant, but the argument needs only the inequality and is valid. In the common-rho LH-iid setting GEN's rho_+ can be taken to be rho.

The O(log n) cutoff is not an additional concentration assumption. Independently, with the actual BB(1,p) per-model weight w(k)=1/[2 choose(2p−1,k)], put q_k=choose(p,k)w(k). The product for choose(p,k)/choose(2p−1,k) has first factor at most 1 and all subsequent factors at most 1/2, so q_k≤2^{-k}. Consequently

    R_m ≤ 2^{1−m}(2p)^{s₀},
    m♯_n ≤ min{K, max{s₀, ceil(1+s₀+(As₀+(s₀+2)/2)log₂ n)}}

eventually, when s₀≤K. If the displayed logarithmic cutoff exceeds K, the tail at m=K is empty. This is the same calculation as PXN/lemmas/P8_T03sharp.md:27-35 and matches GEN/STATEMENT.md:52-53. Hence

    L′_n=m♯_n+s₀+j₀+|𝒱|+1=O(log n),
    L′_nδ_n=O((log n)^{3/2}/√n)→0.

All of s₀,j₀,|𝒱| are fixed for each fixed A and family. Restricting |T| to at most p only reduces the family. GEN's within-block orders are covered too, since |𝒱|=g(2c+v)≥2g and blocks have size at most 16 under SIZE. Anchored sets S₀∪J required by both SE hypotheses are included. Multiplication by n−1 converts the normalized floor into the required unnormalized SE_w floor with fixed g₀=λ₀/2. There is no claim of a full empirical eigenvalue floor when p≥n.

The remaining two parts of GEN's 𝒞_n have probability tending to one: mu=CX^r theta and the active sample SDs involve a fixed finite collection of raw columns. Their energy and SD limits give M=2theta'Σtheta+1 and b₀=(1/2)min theta_j² as in GEN/lemmas/L6_instances.md:70-73. An iid-row coupling supplies an SLLN; convergence in probability alone suffices. I2 correctly assigns the explicit 1−3n^{-2} bound only to the eigenvalue event, not to the whole 𝒞_n.

### Every concentration use in GEN(d)

Write e_n=δ_n. The following checks concern replacing [CONC], not the independent correctness of all SEL assertions.

| GEN/lemmas/L6_instances.md lines | Required bound | With CR's e_n |
|---|---|---|
| :123-125 | Uniform entrywise event and stable bounded-order partial correlations | e_n→0; for matrices of fixed size at most 40 the operator error is O(e_n), preserving a positive eigenvalue floor eventually; inverse/Schur-complement perturbations are O(e_n). |
| :127-131 | Within/between strict separation and no splitting a whole group | 0.4−e_n>e_n eventually; the deterministic clustering/cut/packing argument is unchanged. S1 does not need separation. |
| :132 and :168-170 | H0, H2a, including the m♯_n order | The O(log n) operator calculation above gives the required 0.05 floor from λ_min(Σ_s)≥0.1. |
| :133-138 | Uniform VIS and bounded energy | Bounded-order Schur complements have O(e_n) error. Fixed support and fixed standardized theta* make sample energy (n−1)theta*'R-hat_{S₀}theta*, with O(e_n) normalized error. Both retain the fixed enlarged bounds and n/log n VIS envelope. |
| :153-159 | SEL's null-regressor perturbation | If a truth is missing, residual signal variance stays bounded below. Then ||a||,||b||=O(e_n); R^{-1} is bounded. The exact recursive formula yields |rho_{T,l}−rho_{T₀,l}|=O(e_n²)(1+|rho_{T₀,l}|). If all truths are included, leakage is exactly zero. |
| :160-165 | Uniform exponent and NL_C | The fixed-family Beta bound is still O(√(log n/n)); it was not obtained from [CONC]. Squaring after the O(e_n²) perturbation gives exponent error O((log n)^{3/2}/√n+(log n)²/n)=o(1), and squared leakage remains O(log n). |
| :166-169 | Markov/average transfer and event probability | The multiplicative factor e^{omega_n}=1+o(1) survives; the underlying fixed-family expectation O(n^{1/4}) is unaffected. All CR event complements still tend to zero. |
| :180-185 | S5's excluded-scenario argument | The limiting positive marginal covariance has only O(e_n) error, so its fixed positive lower bound survives. |
| :186-191 | S2's excluded-scenario argument | For fixed 0<alpha<1, e_n/n^{-alpha/2}=O(√log n/n^{(1−alpha)/2})→0. Thus the selected population covariances still dominate sample error even if p grows very slowly. |

In the study generator mu uses fixed coefficients on sample-standardized truth columns. Bounds involving mu above follow from the same entrywise design event and its fixed finite support; CR need not be applied to mu as though it were an additional iid Gaussian column. Subject to finding 2's wording correction, no use of [CONC] in (b) or (d) requires the sharper log p radius.

## Status bookkeeping

The substantive status bookkeeping is correct and does not upgrade an archive or HQ registry status. The following are exact excerpts of the consulted sources:

| Source | Exact status text / excerpt |
|---|---|
| PXN/REPORT.md:4 | `**PROVED-CHECKED**` |
| PXN/REPORT.md:42, item 4 status cell | `XF VERIFIED incl. Hotelling density, W7 Lemma 2 and the Corollary B constant, after splitting the false "every t" display (E-15); W7 A0(c) bypassed by a direct margin argument (E-17); independent cruder route (R′) XF VERIFIED` |
| PXN/lemmas/CR_corr_tails.md:3 | `PROVED (by this seat); XF VERIFIED (R19, Codex gpt-6.1-sol)` |
| PXN/lemmas/R_branch_repair.md:3 | `XF VERIFIED WITH MINOR FIXES (R21), fixes applied` |
| PXN/reviews/R14_I4_TheoremR_codex.md:1 | `VERDICT: ERROR` |
| PXN/reviews/R19_I9_repairs_codex.md:1 | `VERDICT: VERIFIED WITH MINOR FIXES` |
| PXN/reviews/R21_repair_recheck_codex.md:1 | `VERDICT: VERIFIED WITH MINOR FIXES` |
| GEN/reviews/R07_L6_check_sol.md:1, clause (b) | `(b) VERIFIED-WITH-AMENDMENTS (conditional on the named partition input)` |

I2's quoted REPORT item-4 cell and CR status match. R14's overall ERROR concerns the unamended source; its verified intended recovery conclusion and the separate R21 repair check support citing the repaired theorem. R19 and R21 have dispositions at their ends recording the minor fixes. PXN/REPORT.md:81 records the council scores 8.6/8.3 as I2 says. These are source records, not new scores assigned by this review.

PXN/REPORT.md:66-68 explicitly keeps the old W7 registry status, including `Corollary B XF GAP (A-REV9, L2 constants)`, while stating that the constant has now been independently checked and the registry row is HQ's to update. I2 does not claim to have edited or upgraded that row. Its removal of GEN's two named candidate/citation conditions is a proposed dependency substitution using repaired PXN results, not adoption of the original W7 display. GEN's own hypotheses, operational premises, LS0 integration obligations, and other dependency statuses remain in force. The label “unconditional” must be read in this limited dependency sense.

## Falsification simulation

Files produced:

- `Theory_work/Wave1C/C-PACK/numerics/R35_falsify.py`
- `Theory_work/Wave1C/C-PACK/numerics/R35_falsify_out.txt`

Executed successfully with the existing environment, without installing anything:

    & 'C:/Users/felip/anaconda3/python.exe' -B Theory_work/Wave1C/C-PACK/numerics/R35_falsify.py

The PATH Python lacks NumPy; the completed run used Python 3.12.4, NumPy 1.26.4, SciPy 1.13.1. Runtime was 148.93 seconds. Six RNG seeds, 0..5, were each advanced through 24 configurations: n∈{200,800,3200}, g∈{9,10,11,12}, c∈{1,2}, 24 groups, v=0, rho=.7, psi=.5, p=24g∈{216,240,264,288}. A=2 covers p>n at n=200. All 144 configurations satisfy SIZE. This is a finite grid of the family, not a diverging p_n experiment.

The script constructs the actual rank-one hub-linked population covariance, centers and sample-standardizes Gaussian columns, and implements complete linkage with the specified sorted-union lex tie rule, min-index children, top-down size cut, and whole-cluster next-fit packing. It checks population recovery at B=14,16 for g=10 and deliberate nonrecovery at B=20=2g, plus an exact-tie identity-matrix fixture. It does not use a correlation threshold as the cut.

For every draw it computes m♯_n from the actual capped prior tail, then L=min(p,m♯_n+s₀+j₀+g s₀+1). Eigenvalue probes include every group, the signal-unit union, the first L columns, and 12 random subsets at each of three sizes (16, ceil(log n), L). A full empirical minimum eigenvalue is also calculated: a full-Gram floor certifies all subsets by interlacing, whereas passing a finite probe list alone does not.

| n | Draws | blocks=groups | Strict global margin | Draws with a probed eigenvalue below .075 | Full-Gram certificates for every subset | Literal I2(ii) onset met |
|---|---:|---:|---:|---:|---:|---:|
| 200 | 48 | 48 | 40 | 48 | 0 | 0 |
| 800 | 48 | 48 | 48 | 0 | 7 | 0 |
| 3200 | 48 | 48 | 48 | 0 | 48 | 0 |

The threshold is λ₀/2=.075. The smallest tested sparse eigenvalue at n=200 was approximately .01245145. These 48 finite-n failures would refute an onset-free eigenvalue claim, but I2 makes no such claim. Its δ_n values here are approximately 12.78993, 7.16952, 3.93713; even δ_n≤2 fails at all three n values, before considering Lδ_n≤.075. Hence none of these eigenvalue failures is a counterexample to I2(ii). At n=200 the full Gram is singular because p>n−1, which also does not refute a small-subset assertion. At n=800 the missing full certificates do not imply failure for subsets of size at most L.

Recovery occurred even on eight draws without the global margin, showing that the margin is sufficient rather than necessary. Every checked deterministic implication passed. These six-seed observations neither prove an asymptotic probability theorem nor validate its tiny tail bound empirically. The analytic rate/onset calculation remains necessary.

**Final disposition:** Accept the dependency discharge after explicitly importing the exact-branch convention and correcting the rate-comparability sentence; repair the four source anchors. The probabilistic transfer, sparse spectral estimate, m♯_n order, and sufficiency of the replacement rate all check. No new candidate premise is needed.

VERDICT: VERIFIED-WITH-AMENDMENTS — FATAL: 0; MAJOR: 1; MINOR: 1; NIT: 1.
