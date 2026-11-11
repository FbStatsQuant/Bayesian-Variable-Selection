# K2 v2 — independent line-by-line check (Sol, high)

Reviewed against STATEMENT v1.2. R03b was treated as a proposal, not evidence. No subagents or git operations. Only this review and `K2_scratch/check_v2.py` were written. Locations refer to the versions read; C includes the R_m=0 clarification at lines 32–33.

## Verdicts

| File | Verdict |
|---|---|
| lemmas/C_expectation.md | **VERIFIED** |
| lemmas/D_hellinger.md | **VERIFIED-WITH-AMENDMENTS** |
| lemmas/E_visibility.md | **VERIFIED-WITH-AMENDMENTS** |

**0 FATAL, 0 MAJOR, 1 MINOR, 1 NIT.** No counterexample to a theorem conclusion was found. Neither amendment changes assumptions, rates, c₁, C_H or C′_H.

## Numbered findings

### 1. [MINOR] D3's S₀ exception needs a simultaneous-event justification

**Location:** `lemmas/D_hellinger.md:59–66`, especially line 63, “for S₀: O_P(1), a fortiori.”

The paragraph announces deterministic simultaneous bounds on 𝒢^sup_n∩𝒢⁵_n, but the justification for the S₀ instance of line 62 is only O_P(1). Tightness implies a fixed-constant O(log n) bound with probability tending to one; it does not imply that bound on every realization in the specified event. Also, the explicit variance constant at line 66 needs uniform closeness of E[v|S,y] to σ*². The looser E[v|S,y]≤2σ*² used later would alone give a constant near 8σ*⁴/n, not 4σ*⁴/n.

**Fix preserving the event and constants:** put a₀=(I−M_{S₀})μ_c. Since a₀ belongs to col(X_{c,S₀}), (G2*) gives

    |eᵀa₀| ≤ ‖P_{S₀}e‖ ‖a₀‖ ≤ σ*√(C_A s₀ ρ̄ log n).

Thus, on the same event,

    |Q^c_{S₀}−‖e‖²|
      ≤ σ*²C_A s₀ log n + 2σ*√(C_A s₀ρ̄ log n) + ρ̄
      ≤ σ*²C_Q log n

eventually, since C_Q−C_A s₀>0. The onset may depend on M,φ₀, as allowed. This closes line 62 uniformly without another exceptional event. Then (G1) and line 65 give uniform deterministic closeness E[v|S,y]/σ*²→1 on the event. Take E[v|S,y]≤(5/4)σ*² and n/2−1.99≥0.4n after enlarging n₀. The variance is at most (125/32)σ*⁴/n<4σ*⁴/n, validating line 68's Chebyshev constant 16.

This is a local justification gap. The common-fluctuation argument and parametric variance rate are correct.

### 2. [NIT] Final masking remark still describes only Δ_S

**Location:** `lemmas/E_visibility.md:82–83`.

“Masking enters only through Δ_S” is left over from v1. In v2 the assumption and proof use L_S, which can strictly exceed Δ_S, even when a singular model spans μ_c.

**Fix:** “The sufficient interface uses ridge loss L_S. Projection masking is measured by Δ_S≤L_S; the W3-POST E4 numerics illustrated that projection component.”

## C: detailed audit

**C1, lines 18–29.** The energy step is valid: (F₀),(E) imply ‖θ*‖²/n≤M/((n−1)φ₀²)≤M/(2φ₀²) for n≥3. Evaluating the slab minimum at θ* gives Q^c_{S₀}≤‖e‖²+ρ with deterministic ρ≤ρ̄ and no cross term. The density-ratio integral matches [P1]. Both derivatives of F are correct. The triangle bound on |F″| is (8/9+128/27)N=(152/27)N<6N. The linear Taylor term has the right sign, so F≥−3N/n≥−3.

The data-dependent window is legitimate in a pointwise lower bound: no Gaussian law is conditioned on that window or the scale event. Both windows lie in a fixed compact interval where the fixed-rate IG density has a positive deterministic minimum. Their v-length is σ*²/√n. The penalty bound −ρ/(2σ*²u)≥−ρ̄/σ*² is conservative and correct. Thus c_den tracks correctly.

**C2, lines 32–42.** Line 37 is a deterministic multiple of N_m≥0 for fixed design/truth. Removing the event indicator before taking E N_m requires no independence. E N_m=ϖ(E_m)=R_mϖ(S₀) is exact: b₋ is data-free, the predictive density integrates to one, and W_K cancels. The zero-tail case is explicit. The scale probability matches [P1]. At x=N/8 the [P3] threshold is (5/4+1/√2)N<2N, giving exp(−N/8). R_{m♯}≤n^{−(s₀+2)/2} times √D_{S₀}√n gives exactly (1+1/n)^{s₀/2}n^{−1/2}.

**Main proof, lines 45–55.** The classes cover Ω∖{S₀}. Superset expectations use truncated-moment bounds, not merely O_P bounds. With A_n=(2p)^s₀(n+1)^{s₀/2}, the underfit expectation is bounded by

    2^s₀κ̄_n(1+e^ρ_n EΥ) + 2^s₀e^(2ρ_n)A_nEΥ^{>j₀}.

Case (i): [T03R] C5(b),C8 give EΥ≤Cr_n and A_nEΥ^{>j₀}≤C(log n)^{(j₀+1)/2}/n. Cases (ii)–(iii): C5′(b) and the two distinct OS bounds give EΥ′≤C_OSr_n and A_nEΥ′^{>j₀}≤C_OSr_n. C10 supplies κ̄_n=e^ρ_n n^{−2} in (i)–(ii); E1 supplies n^{−2} in (iii). C's extra e^ρ_n on the high shell is harmless. Complements cost ≤5/n. Finally (log n)^{(j₀+1)/2}/n=o(r_n).

These are single-n inequalities with uniform deterministic onsets, using m♯≤C_m log n. They do not require OS/floors at other n. The BM-∞ envelope and random-design conditioning qualifications suffice. Decision/PIP corollaries and LB's domain restrictions check out. For ξ_q, “all O(r_n)” means fixed q∈(0,1), as its denominator requires.

## D: detailed audit

**D0, lines 8–17.** The transformed joint posterior, IG shape ν=.01+n/2, Gaussian covariance, centred original response scale and isometry identity match [P1]. The normal affinity and all scalar inequalities hold for every v,w>0. D0 requires no variance floor.

**D1, lines 20–29.** All four assertions hold for empty and singular models. Covariance tracing gives v tr(M_S). The spectral facts M_S²⪯M_S⪯P_S and (I−M_S)²⪯I−M_S prove the two norm bounds. Squared triangle inequality gives (b); expansion of y_cᵀ(I−M_S)y_c gives (d). IG moments are correct. No eigenvalue floor enters (b) or (d).

**D(a), lines 33–47.** L_{S₀}≤ρ̄, fixed rank s₀ and the fixed-vector Gaussian cross term give Q^c_{S₀}−‖e‖²=O_P(1). Bounded energy and [P1] give b=O_P(1). IG moments give root-n variance contraction at every diverging multiplier. Conditional mean-loss second moments are tight, so Markov gives every diverging squared-mean threshold. The coefficient bound uses only the floor Nφ₀² on S₀, after paying δ_n for S≠S₀. The event inclusions and final Hellinger thresholds have the correct powers of M_n.

**D(b), lines 50–74.** The retained set is deterministic given design/truth, has bounded size, and L_S≤c₂σ*²log n eventually. The complement decomposition is valid. E1 applies individually to bounded-excess members of 𝒰_far at c₂=c₁+1; no global ID assumption on near models is needed. Large-excess models use C6(a), extended scores for unions outside Ω, and the second OS inequality. Hence π(Ω∖𝒮_n)=O_P(r_n), without beta-min or (F_λ).

The cutoff-range claims in D and E are valid, though abbreviated. For fixed B≥s₀+1 and p≥B, q_B≥1/[2 binom(2B−1,B)] and w(s₀)≤1/2. If K≥B this bounds R_{B−1} away from zero while the cutoff target tends to zero, so m♯≥B eventually. If K<B and n≥2B, p=K<B; finitely many possible p imply m♯=K eventually. This justifies (G2*) and (G3′) on the bounded retained/comparison family, uniformly also for fixed small p.

The near-model cross event gives simultaneous O(log n) control of Q^c_S−‖e‖²; finding 1 handles S₀ on the same event. The exact identity in line 64 is correct: 2(ν−1)=n−1.98 and N=n−1 leave +0.98σ*². The leading fluctuation is the single common ‖e‖²−Nσ*². Its absolute value is O_P(√n), giving the supremum of conditional-mean errors O_P(n^{−1/2}); no union bound over models is needed, and log n/n=o(n^{−1/2}).

C_H=8σ*²[C_A(s₀+j₀)+c₂]+1 depends only on s₀,A,σ*². M,φ₀,C_OS affect onsets, not C_H. The fitted-mean triangle bound, Markov constant 8σ*²(s₀+j₀)/(C_H log n), and Chebyshev bound check out after finding 1. Taking M_n=√log n gives exactly C′_H=1+C_H/(4σ*²).

## E: detailed audit

**E1(a), lines 16–27.** The residual is correctly (I−M_S)μ_c. Its cross-term variance is σ*²‖(I−M_S)μ_c‖²≤σ*²L_S. The family count 2^s₀(j₀+1)p^j₀ is valid with rank loss and the cap. The two-sided Gaussian bound and x_n leave (2/e)^s₀/n≤1/n. Also x_n≤C_xlog n for n≥3. Zero-variance cases are harmless.

**E1(b), lines 28–47.** The score identity, prior ratio and determinant upper ratio remain valid when S′ leaves Ω or S is singular. The prefactor bound holds for n≥5. The bound on Q^c_{S₀} is [P1] lem:den's first paragraph and needs only (F₀); it gives R_n≤8(M+σ*²). The B′ bound uses the bound on E_n from [P3], not its floor-dependent assertion about arbitrary underfits.

The exact decomposition of Q^c_S is correct. Subtracting the true-model residual bound gives

    D ≥ L_S + 2eᵀ(I−M_S)μ_c
        − eᵀ(P_{S′}−P_{S₀})e − R_n.

The nesting col(X_S)⊆col(X_{S′}) justifies the noise-projection comparison even at rank loss. (G3′), including χ²_∅=0, and the cross event give precisely line 40. No (F_λ) is used.

The split D≥B′ versus D<B′ is valid; log(1+u)≥(log 2)min(u,1). The factor log 2/2 is conservative and correctly tracked. The function φ(λ)=λ−2√(2C_xλ)−C_Aj₀ is increasing above 2C_x; c₁≥8C_x. Direct substitution yields φ(c₁)=(2/log 2)[s₀(A+1)+2]. Thus strict c>c₁ absorbs both the bounded R_n/log n loss and δ″_n uniformly. The n^{−2} comparison follows with the stated constant.

**E2, lines 50–62.** Each completion S′ arises from at most 2^s₀−1 underfits. Bounded excess uses E1 and large excess C6(a), with the latter requiring no floor. Nonnegative sums over algebraic completions outside Ω are legitimate. C5′ and both OS bounds give the displayed rate. The exceptional probability is ≤5/n. The same assembly restricted to j∉S proves the coordinate-specific assertion under ID^M_j alone. The deterministic SL consequences and random-design transfer are applicable. E3's implication F_λ∧BM(c)⇒ID(c(1−1/n)) is correct, with a fixed intermediate margin c′∈(c₁,c) for uniform asymptotics. At s₀=A=1, c₁≈160.8 and c₀=128 are correct.

## Citation/source audit

All labels below were checked in the actual specified sources, rather than accepted from R03b or prior review statuses. Paths for [P1], [P3], [T03R], [W3P], [L1a′], [LB] are exactly those in the review brief.

| Cited source location | Checked content and use |
|---|---|
| [P1] PROOF_v3.tex:68–88, lem:slab | Variational Q identity, Gaussian covariance and integral; supports C1, D0/D1 and L_S=min B_S. |
| [P1]:90–111, lem:spec(a)–(e) | Quadratic form, smoother bounds, true-model residual bound, nesting monotonicity, determinant product and upper bound. |
| [P1]:113–138, lem:prior | Capped normalization and prior ratios. |
| [P1]:155–211, prop:closed and thm:T01i | IG shape/rate, Gaussian conditional, and exact transformation of the joint posterior. |
| [P1]:234–250, thm:T01iii | Unconditional Gaussian law, scale concentration, and (8+24M/σ*²)/(n−1). |
| [P1]:255–264, thm:Ta | Mixed-endpoint κ² transfer, with numerator at b₋ and denominator at b₊. |
| [P1]:317–321, lem:num | Proper fixed-rate predictive density and exact E N_m identity. |
| [P1]:324–359, lem:den | True-model residual upper bound and exact density-ratio integral. C1 re-proves its window step; it does not cite an unproved stronger denominator from this source. |
| [P3] PROOF_v2.tex:64–82, lem:red/eq:score | Contrast coordinates and exact algebraic score ratio. |
| [P3]:94–128, lem:smoother/lem:det | Spectral bounds, nesting and unconditional determinant-ratio upper bound. |
| [P3]:130–151, lem:prior/lem:signal | Prior completion prefactor and projection signal lower bound under the anchored floor. |
| [P3]:154–166, lem:chi | Laurent–Massart-style tails, rank domination and truncated exponential moment. In particular C2 cites P3(a), not the weaker differently numbered P1 chi-square tail. |
| [P3]:169–218, sec:good/lem:Gprob/ongood(a),(b) | Events, per-size bound actually proved at line 190, projection ranks at line 194, and floor-free parts of good-event control. |
| [P3]:197–222, ongood(c),(d) and deterministic sequences | E_n's upper bound depends only on energy and (G1); it remains usable in E1 without asserting the arbitrary-model part of (c). |
| [P3]:233–279, lem:onesup/prop:sup | Superset comparison, truncated expectations and geometric sum constants; modified by T03R and A as recorded. |
| [P3]:303–330, lem:signalgain/lem:assemble | Signal exponent, completion counting, and amplified high-shell expectation calculation. |
| [P3]:332 onward, sec:main(i)–(iv) | Three-class decomposition, deterministic PIP/selection implications, Markov HPM error, coordinate-specific assembly. |
| [T03R] PROOF.md:79–97 | Refined cutoff tail, exact prior-tail normalization and fixed-rate numerator. |
| [T03R]:138–145, Lemma B | B1 supplies the unnormalised floor/determinant in case (i); B2 supplies bounded-excess anchored floors; B3 needs only the smaller-model floor for the upper smoother difference. |
| [T03R]:172–201, C1–C10 | Checked the replacements invoked by C and E: C5 expectations, floor-free C6(a), C8 counting/high-shell expectation, C9 tail, C10 strict BM margin and envelope onset. |
| A_occam.md:45–78, G3′/C4′/C5′/C8′ | Rank-dominated events, exact determinant factors, rank-sensitive truncated moments, and OS-based assembly. The d_J=0 case is explicitly valid. C8′ must be read as the same counting argument with the appropriate available comparison bound; E2 writes that floor-free replacement out. |
| [L1a′] L1a_size_tail.md, Changed step and Remark 1 | Exact-reference Q bound and coefficient bound; no unsupported design-free denominator step was inherited. |
| [W3P] STATEMENT.md, §§0–2 | Cutoff definition, R1, BM constants, random-design quantifiers and conclusions 1–6 agree with their uses here. |
| [LB] LB_rate_lower_bound.md, proposition and proof | Domain s₀<p, s₀+1≤K and deterministic lower bound (1+√(n+1))^{−1}. |
| [SL] I4_SL_corollaries.md, SL0/SL1 | Deterministic PIP, threshold, HPM, model-size and bounded-functional consequences; independently re-derived. |
| [POST] L1_POST.md, step (5) | Every-sequence/common-constant diagonal transfer, conditional on design/truth measurable events. |

**D4 external comparison:** inspected the original attached Song–Liang PDF, printed pp. 952–954 (PDF pages 6–8), with `pdftotext`. The publisher web fetch failed, so the attached original was used. Theorem 1 has the joint/design-integrated Hellinger definition and exponential inner/outer thresholds; Theorem 2 states the corresponding result under Condition 1 and strict sparsity; Corollary 1 gives the quoted logarithmic-size rate. Their normalization is d²=2H². D4 accurately distinguishes that object and probability mode from the current theorem. This verifies the main-text claims, not their online supplement's proofs. Original: [Song and Liang (2015)](https://doi.org/10.1111/rssb.12095). Attachment read: `C:/Users/felip/.t3/userdata/attachments/647bfd65-83bc-403a-b3b0-0a8352044e7f-588fe83a-5cbe-4a20-8055-1cfbd7c9c936-pdf.pdf`.

## Independent numerical attempts

Ran `py -3.13 -I Theory_work/Wave3/W3-POST2/reviews/K2_scratch/check_v2.py` successfully. This is a separate matrix check, without importing the existing enumerator or creating bytecode elsewhere.

- C1: n=16,17,32,100,1000,10000; 41 E′ values over [0,2N] and 301 window points each. Minimum sampled F was −0.2466791004; maximum sampled |F″|/N was 1.5. Both claimed conservative inequalities passed. Fixed-rate IG window quadrature at n≤100, σ*²=1,M=2,φ₀=1/2 gave minimum window integral / claimed bound 840.8998163.
- D1/E1: 7,680 model checks over n=16,32,100, p=6, all subsets, regular, exactly duplicated, nearly duplicated and dependent columns. Used SVD smoothers to avoid spurious inversion failure at exact rank loss. Maximum Q decomposition error was 3.4106051e−13; minimum D1(b) slack 0.3861352; minimum E1 pre-event gain-bound slack 0.00178410. No violation of ‖(I−M_S)μ_c‖²≤L_S or the exact gain comparison occurred.

These finite checks target the revised algebra, not asymptotic certification. The paper's existing Monte Carlo summaries are not used as proof or as evidence for a uniform constant. No theorem-level obstruction was found.
