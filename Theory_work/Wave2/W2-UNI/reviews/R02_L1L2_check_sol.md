# R02 — Cross-family lemma check: W2-UNI L1–L2

Reviewer: Codex GPT-6.1 Sol, high reasoning effort. Date: 2026-11-09.

Scope: `lemmas/L1_metric.md`, `lemmas/L2_k0.md`, against locked `STATEMENT.md` v1.1 §2, claim (ii), and R1–R2. Reviewed the cited LOC2 L1–L5/L7, APP L2_CT/L3_LOC, GROW L6 source chain, and FACA L7 delivery argument. This is an asymptotic proof review, conditional on the explicitly named score, posterior, operational, and implementation inputs. No git operations; no source edits.

| File | Verdict |
|---|---|
| `lemmas/L1_metric.md` | **VERIFIED-WITH-AMENDMENTS** — finding 1 |
| `lemmas/L2_k0.md` | **VERIFIED-WITH-AMENDMENTS** — finding 2 |

No FATAL or MAJOR finding. No counterexample to the substantive metric toolkit or UNI-0 reduction was found. The amendments below complete an empty-set convention and make an inherited random-scale argument precise; neither requires a stronger hypothesis or a change to the locked theorem.

## Numbered findings and exact fixes

### 1. MINOR — LOCL has two undefined empty-set maxima

**Location:** `L1_metric.md:125`, `:129–131` (M5(ii), (v), conventions).

LOCL permits every T, including T = ∅, and permits V = ∅. The displayed `max_{w∈V} ‖β_U(w)‖₁` is undefined when V = ∅; likewise `max_{j∈T}|x_j|` is undefined when T = ∅. The conventions presently specify zero coefficient vectors and Δ = 0, but do not define either maximum. This is a statement-definition defect, not a failed inequality. For example, T = ∅ is an allowed choice for every n, so this is not a finite-n objection.

**Exact fix:** append to the conventions at lines 130–131:

> A matrix with zero rows or zero columns has induced ℓ¹ operator norm zero. In (ii) and (v), a maximum over an empty index set is defined to be zero.

With this convention all five assertions hold, including U = ∅, V = ∅, and T = ∅.

### 2. MINOR — distinguish the auxiliary population calculation from the actual sample-standardised response

**Location:** `L2_k0.md:101–104`, §4(ii)–(iii); the corresponding A_cov summary in §3.

The notation `Cov(Y, W_v | W_{U₀})` and “population residual correlation of W_l and Y” is too literal: actual Y uses coefficients θ*_k/t_k, and t_k is a function of the entire raw sample. Thus actual Y is not the fixed jointly Gaussian population coordinate to which CD_M is applied. Conditioning on the realised scales does not restore that Gaussian population law.

The inherited proof is valid: GROW L6 §1, the paragraph beginning “For later partial correlations involving Y,” explicitly treats this as a **uniform algebraic comparison for bounded coefficient vectors**, which can subsequently be evaluated at the random scales. L2 cites that source and mentions bounded θ*/t, so this is an omitted clarification rather than an unclosed mathematical step. The distinction should be retained in a purported line-by-line delta.

**Exact fix:** insert before §4's population inputs, and use V_b in (ii)–(iii):

> For a deterministic coefficient vector b on S₀ with |b_k| ≤ 2θ_hi, define the auxiliary population coordinate V_b = ∑_{k∈S₀} b_k W_k + ε₀, where ε₀ is independent N(0, σ²). All population comparisons involving the response below mean comparisons with V_b, uniformly over these b. On the augmented entrywise event, t_k → 1 uniformly, so b_k = θ*_k/t_k lies in this bounded set. The empirical Schur-complement comparison is uniform over b and is then evaluated at these random coefficients; no conditional Gaussian law given the scales is asserted.

For TV in §3, retain the separate perturbation from θ* to θ*/t = θ* + O(ħ_n), or the direct standardised-Gram proof already cited. In §5 retain conditioning on W_D and ε, not on the raw scales of all columns: the true-column scales needed to fix r_Y are W_D-measurable because S₀ ⊆ D.

## L1: adversarial checks

**CT_M and the zero shell.** The shell estimate counts all indices in `[m,m+1)` by C₀(m+2)^{d₀}. Starting at m = 0 handles both coincident indices and arbitrarily small positive distances. There is no implicit lower separation. The nonmonotone perturbation envelope is bounded shell-wise, not incorrectly fed into the monotone G-shell formula. For φ(i) = δ(i,j), the triangle inequality gives |φ(i)−φ(k)| ≤ δ(i,k), and δ(i,k) = 0 forces the perturbation entry E_ik to vanish. The symmetric entrywise majorant controls both row and column sums even though E need not be symmetric.

The series defining S converges locally uniformly for t < a′, is continuous at zero, and diverges as t ↑ a′. Consequently the stated positive t* exists and S(t*) ≤ α/2. The Neumann-series bound applies to the nonsymmetric conjugated matrix. Finite-dimensional conjugation requires no uniform bound on D itself. Interlacing, inherited entries, and restricted growth give exactly the same constants for every principal submatrix. No upper eigenvalue bound or unit diagonal is used here.

**CD_M, both branches.** In the covariance branch CT_M first supplies precision decay. In the precision branch it is already assumed. Applying restricted CT_M to Θ_HH, H = [p]∖U, with lower eigenvalue 1/C proves conditional decay with K₂ = 2C. For a smaller V ⊆ H, the proof correctly uses a principal submatrix of `(Θ_HH)⁻¹`, rather than falsely identifying its covariance with `(Θ_VV)⁻¹`. Both conditional spectral bounds [c,C] follow. The conversion between branches uses the advertised constants and includes diagonal bounds where claimed.

**RB_M and TAIL_M.** For G = `(Ψ_{A∪{l}})⁻¹`, block inversion yields β_v = −G_vl/G_ll. The denominator satisfies G_ll = 1/ψ_{l|A} ≥ 1/C. Hence B = 2C/c is valid without unit diagonal; B = 2/c is valid for the correlation case. Summing from shell zero gives a bound uniform in A and l. TAIL_M uses a conditional covariance matrix with lower eigenvalue c and sums squared conditional covariances over δ(l,v)>r. Its floor(r) tail may overcount, but never undercounts. The explicit G-tail estimate is valid for real d₀ ≥ 0, including the separately stated d₀ = 0 convention.

**LOCL(i)–(v).** The sign in (i) is correct. Each column w of Ψ_UU⁻¹Ψ_UV is precisely β_U(w), with w∉U. Thus (ii) is the induced ℓ¹ norm identity, not a row-sum bound, and RB_M makes its constant independent of |U| and |V|. Zero padding gives Δ_U = −Ψ_UU⁻¹Ψ_UV β_{T,V} and Δ_V = β_{T,V}, proving (iii). The residual for T is orthogonal to every coordinate in T; therefore the variance identity in (iv) is exact. Its use of the upper spectral bound C is explicit and legitimate. Hölder proves (v). After finding 1, all empty cases are defined. Uniformity in T, l, p, n and geometry follows because every constant uses only the fixed class parameters.

**SC_M.** Diagonal entries lie in [c,C], so congruence gives spectrum [c/C,C/c]; covariance entries scale by at most 1/c and precision entries by at most C. The stated common decay envelope is valid. Rescaling changes fixed class constants, as disclosed.

## L2: source-chain and engine audit

**Inventory completeness.** G1–G17 account for the geometric dependencies in the source chain: packing and shell counts; the distance-to-basepoint Lipschitz function; conditional covariance decay; relevance and removal-neighbourhood cardinalities; and NA reference counts. APP L3.6's line windows and GROW L6.6's nearest-neighbour Markov regression are explicitly replaced by NA-R. Neither is silently reused. APP L3.2–L3.5 and GROW L6.2–L6.5 have no additional ordering, nearest-neighbour, Euclidean-volume, or separation requirement after these replacements.

**Q and feasibility.** The union-of-balls bound gives |Q⁰| ≤ s₀C₀(1+d_n)^{d₀}. In the enlarged branch, failure of the integer test gives p ≤ 2|Q⁰|+32s₀. Thus |Q| = O((log n)^{d₀}) in both branches. In the retained branch the population test controls p and polylogarithmic size controls floor(n/2), giving the required bound on their minimum. In the enlarged branch p = polylog(n), hence K_n = p eventually. Also q ≤ K_n eventually. For d₀ = 0, taking a radius covering the finite pseudometric space gives p ≤ C₀; all arguments remain valid.

**Regularity and selection removal.** Entrywise concentration uses Gaussian rows, unit variances, and p ≤ n^A. For any fixed exponent κ′, `(log n)^{κ′}√(log n/n) → 0`; hence every required polylogarithmic Gram floor follows without a union over subsets. The L0′ enlargement covers the lattice family and its score contrasts. Removal neighbourhoods have O((log n)^{d₀}) members, but only subsets of size ≤15 are used, so the reference count is O((log n)^{15d₀}). The bounded-dimensional partial-correlation recursion remains uniform. Finding 2 supplies the precise interpretation of its response population inputs.

**Spherical tail and size ladder.** The conditional truth covariance has floor c; α = O(e^{−t₂d_n}), b_j is bounded by √15/c, and τ²∈[c,1]. The resulting mean shift is O(1). Conditioning on W_D and ε fixes the response residual; the innovation remains isotropic Gaussian. The source's CN_D integration avoids conditioning the sphere law on A_cov. The new reference count contributes only exp(O(log log n)); the e^{O(√log n)} shift cost is n^{o(1)}. The expectation bound remains k n^{−1/2+o(1)}, uniformly in k. The dyadic ladder has O(log n) levels, including near-cap sizes. Replacing k₀ by a fixed power of log n preserves both the ladder failure bound and the positive junk-deletion margin. Truth additions are feasible by the verified dichotomy.

**NA-R inputs.** N0 and N1 are verified. For R1, all coefficients are deterministic population regressions and the singleton frame count satisfies log N_n ≤ log p + O((log log n)^{d₀}) = log p + o(log n). For R2 the coordinate atoms have variance exactly one, the decomposition has the correct sign, and the actual maximum coefficient norm is bounded by 2L₀. Therefore its square times log(|𝒜_n|+1) is O(log log n). For R3, TAIL_M gives η_n = κ(log log n)/c → 0. NA-R requires only this convergence, not η_n log n → 0. No growing-radius coefficient localisation beyond RB_M is needed for k = 0.

**Assembly and delivery.** TL uses fixed beta-min, a signal of order n, and polylogarithmic errors from L0′. The global spectral floor supplies the posterior LSF hypothesis. Bounded posterior error converts convergence in probability to convergence of its expectation. PLR and the shipped cap then give the stated output-intersected conclusions. Delivery correctly proves the LS0-scoring event directly and uses it with posterior dominance; it does not reverse the bound involving D_n. The operational and delivery premises, including the recorded e4/N3 qualifications, remain named inputs.

**Upper spectrum and diagonal audit.** The upper bound C is needed for conditional decay and its derived constants; the separate C in general LOCL(iv) is also explicit. Unit diagonal is genuinely used for concentration normalisation, residual upper bounds, the spherical regression estimate, and variance-one atoms. UNI-0 assumes it. No use of an unproved unit diagonal for general Ψ remains in L1.

## Independent numerical probe and limitations

Ran an in-memory `py -3.13 -B` check on ten indices with duplicated sites and δ(i,j)=|z_i−z_j|^{0.7}, so there are zero-distance pairs and a valid growth exponent d₀=1/0.7. Used a non-unit-diagonal covariance `D(exp(−δ)+0.4I)D` and its inverse as the two branch examples. Exhausted every (l,T) and four radii: **20,480 triples per branch**. Maximum normal-equation identity residuals were 3.94e−16 and 3.90e−16; variance-identity residuals 1.05e−15 and 1.37e−15; column-norm identity residuals 1.11e−16 and 2.22e−16. Minimum principal-inverse diagonal entries were 0.2205 and 0.2430, independently illustrating why ≥1 is unavailable without unit diagonal.

Also inspected the supplied n2 probe and output. Its very loose tail constants make numerical passage of ε/κ bounds weak evidence, as M8 already acknowledges. Numerical checks do not prove uniformity or asymptotics. The verification above rests on the analytic inequalities and source-chain audit. No new full-algorithm sandwich simulation was run.
