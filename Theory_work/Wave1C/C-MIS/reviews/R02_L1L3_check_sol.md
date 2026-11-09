# R02 — adversarial check of L1–L3

Scope: STATEMENT.md v1.1, §§1–3; L1_reduction.md, L2_gaussian.md, L3_hpm.md. Read-only review except this file; no git commands used. Verdicts concern the mathematical transfers relative to the cited inputs, retaining those inputs' recorded statuses. Section 4/Theorem F is not checked here.

## Lemma R — VERIFIED

L1:23–33 is an exact equality of experiments. Under GR, ε + ξ is centered Gaussian with covariance (σ² + τ²)I. The coefficient and intercept are β_𝒞 + γ and α + a. For random designs the conditional Gaussian law is constant in the design, which establishes independence of ε′ and the candidate design. Independent method uniforms then give equality of the entire candidate-only run, not merely equality of a likelihood kernel.

I checked the possible hidden dependence in T03♯. T03R:76–99 uses the Gaussian experiment's true density, bounded mean energy, truth Gram, and variance for its denominator and response-scale controls. T03R:138–205 uses Gaussian contrast noise, deterministic design/projections, and μ_c = X_cθ*. In particular, the pure-noise residual identities in [P3]:71,218,220,311 are valid for the reduced mean μ^𝒞; they do not require that this be the full-model structural mean. The source's response-dependent rate b = b₀s_y² is retained automatically ([P3]:61–78); the reduction does not silently substitute a raw-data likelihood or a different prior. Centering eliminates the intercept. No further property of the original generating mechanism enters.

The independence requirement is essential: marginal Gaussianity of ε and ξ without their stipulated conditional independence would not suffice. It is present here.

## Theorem MIS(i) — VERIFIED

L1:40–54 correctly substitutes the candidate problem into T03R:162–168. Positive sample SDs preserve support. T03♯ permits triangular arrays of coefficients/support labels with fixed support size; it does not require fixed raw coefficients. Its anchored eigenvalue conditions concern candidate subsets after substitution.

The posterior-to-PIP inequality, the strict majority implication for MPM and the global HPM, and the factor 2 expectation bound agree with [P3]:362–364. Bounded posterior error converging in probability implies convergence in mean; no expectation rate follows or is claimed. The no-beta-min inclusion is exactly T03R:168(iv),201, with fixed c > c₀(s,A); the empty large-signal set is harmless. Proxy/cancellation conclusions require the full concentration hypotheses, as stated. Empty projected support is correctly excluded by the adopted TH09 card.

The onset remark must retain the source's meaning: n ≳ 2·10⁶ is a disclosed illustrative obstruction/onset scale, not a universal sufficient threshold. SoP:787,810–811 explicitly excludes a universal n₀; T03R:170 makes it parameter-dependent.

## Lemma DR — VERIFIED

L1:64–72 has the correct quantifier order. If the limit of g(L) is η > 0, each integer L has arbitrarily large n with sup f_n^L > η/2. A strictly increasing n_L and approximate maximizing points therefore exist without attainment of the supremum. For fixed real L₀, every integer L ≥ L₀ gives f_{n_L}^{L₀} ≥ f_{n_L}^L > η/2, contradicting tightness along the completed sequence.

Eventual nonemptiness is precisely what permits completion outside the subsequence. No measurable choice of the maximizing points is needed: this is a deterministic contradiction, and the supremum is a number, not a random variable. Measurability is needed later for integration, not for this combinatorial implication. This genuinely extends GEN L5:57–64 from convergence to zero to tightness.

## Theorem MIS(ii) — VERIFIED-WITH-AMENDMENTS

The canonical Gaussian integral in L1:88–95 is the right conditional-probability version, defined at every admissible x rather than only almost surely. Measurable coefficients, positive sample SDs, finite posterior sums, and the measurable support map give a measurable integrand. Thus null conditional fibers cause no diagonalization problem. P(X ∈ 𝒜_n) → 1 ensures 𝒜_n is nonempty for all sufficiently large n.

The assertion that every deterministic selection is a T03♯ array is valid provided “finite-n inequalities” is read literally as follows. Require s(x)=s, p≤n^A, energy≤Mn, the truth Gram floor, and the two anchored eigenvalue inequalities at that n, with the same constants. For BM-∞ require the displayed deterministic lower envelope M_n→∞; a bare assertion that individual designs satisfy “BM-∞” has no finite-n meaning. For BM(c) require the fixed-c inequality at that n. Since p≥s, K=min(p,⌊n/2⌋)≥s once n≥2s, regardless of the selected designs. Proof thresholds are not extra design hypotheses: T03R:170–201 derives them from the fixed constants, and from the shared BM envelope in the BM-∞ case. No design-dependent onset can evade this argument.

Exact amendments:

1. At L1:81–83 spell out the preceding finite-n interpretation, or explicitly point to STATEMENT:66–67. Delete the ambiguous wording that an individual x “satisfies (H-MIS)” as an asymptotic condition. State that all requirements are imposed for n beyond a deterministic starting index; no common small-n validity is needed.
2. At L1:98 replace “by bounded convergence” with the elementary bound E Y_n ≤ ε + P(Y_n>ε), since only convergence in probability has been proved. This repairs the name of the argument, not the conclusion.
3. To obtain the **without-beta-min** clause of (i) under random design, explicitly add a second version of (ii): retain the finite-n base conditions and fixed s, omit both beta-min alternatives, and apply DR to Y′_n using T03R(iv). The last sentence of L1:99 supplies the proof, but the hypotheses of L1:81–83 currently still impose beta-min. Under the written beta-min hypotheses the inclusion conclusion is already valid; the amendment states the broader advertised scope without ambiguity.

On 𝒜_nᶜ one may define posterior mass of an infeasible support to be zero, as in [P3]:362–364. The finitely many indices before feasibility can be discarded. The pathwise error-event inclusion at L1:97 is correct; design-measurable, varying support labels do not change it.

## Proposition P — VERIFIED

Every displayed algebraic identity checks. Gaussian conditioning yields γ=Σ_𝒞𝒞⁻¹Σ_𝒞𝒪β_𝒪, a=m_𝒪ᵀβ_𝒪−m_𝒞ᵀγ and the stated nonnegative Schur-complement variance. Independent rows remain conditionally independent, and the residual law is free of the candidate matrix. The covariance equation for β^𝒞 includes the original candidate contribution and has the correct sign. It is the slope with an intercept; the intercept adjustment matters for nonzero means.

The two block equations from ΣΘ=I give exactly −Θ_𝒞𝒪Θ_𝒪𝒪⁻¹ and Θ_𝒪𝒪⁻¹. Multiple omitted variables give only the claimed support inclusion, since their weighted contributions may cancel. With one active omitted variable, β_k/Θ_kk is nonzero, so supp γ equals the stated neighbor set. The formula for S₀^𝒞, including the cancellation equality, is correct. Partial correlation has sign −Θ_jk/√(Θ_jjΘ_kk).

Crucially Θ is the precision of the **reduced vector of candidates and active omitted columns**, as L2:5–7,19 specifies. It need not be the corresponding principal block of the precision of a larger vector containing inactive omitted variables. The proof makes no such invalid identification.

The Song–Liang identification is supported by the locally available primary-paper extraction, Theory_work/Wave1C/C-PACK/R38_song_liang_extract.txt:594–619, especially eq. (19). Their Corollary 2 is support inclusion, not exact-model concentration. Thus L2:52–53 should be understood as implying that conclusion with stronger exact-model control, not as identifying the two theorems. [Song–Liang paper](https://doi.org/10.1111/rssb.12095).

## Lemma GD(a) — VERIFIED

L2:47–61 has genuine slack in every population-limit inequality. With fixed p, sample covariance/SD convergence gives the asserted high-probability event and positive SDs. The full sample correlation floor supplies every anchored normalized floor by interlacing, including unions larger than the cap. Multiplying by N=n−1 supplies SE_w with g₀=1 once Nφ₀²≥1. For n≥2p, K=p. The standardized coefficient bound is θ_j²=σ̂_j²(β_j^𝒞)²≥κ, so the deterministic envelope diverges at n/log n. Fixed m,Σ,β ensure τ² and hence σ_𝒞² are fixed here. No additional Gaussian-design assumption is missing.

## Lemma GD(b) — VERIFIED-WITH-AMENDMENTS

The probability and normalization calculations work under the fixed-σ_𝒞² scope of Theorem MIS. Deterministic contrast rotation removes the row means: Cov(W_a,W_b)=1{a=b}Σ_𝒞𝒞, and joint Gaussianity gives independent rows, even when candidate columns are correlated. This does not require independence of columns of W.

The SD union bound is 2p exp(−(A+2)log n)≤2n⁻². For each size k the sparse singular-value union bound is ≤n⁻² using the one-sided inequality, hence ≤k_n n⁻² over all sizes. Here k_n=O(log n), while √k_n+t_{k_n}=O(log n)=o(√N); consequently the stated √(N/2) lower bound holds eventually. Independence between different subsets T is unnecessary.

The normalization is safe: W_TᵀW_T≽c₀NI/2 and max σ̂_j²≤2C₀ imply G_T≽c₀NI/(4C₀), hence R̂_T≽c₀I/(4C₀). This is stronger than φ₀²=c₀/(8C₀). The order k_n covers both anchored union families. Energy uses a single χ²_N variable with variance parameter ≤M₀; taking its tail parameter log n gives the claimed 1−1/n probability for all sufficiently large n. Combining these events gives failure at most 2n⁻²+k_n n⁻²+n⁻¹ eventually.

Exact amendments:

1. At L2:63 explicitly retain Σ_𝒞𝒞≻0 and σ_𝒞²=σ²+τ² **fixed in n** from MIS. L2:7 allows triangular Σ,m, and the listed population design assumptions alone do not control τ_n². Without this inheritance the assertion is false: take p=⌊n^(1/3)⌋ independent unit-variance candidates, β^𝒞=e₁, and an independent omitted Gaussian column of variance n² with coefficient 1; let σ²=1. All listed population restricted-eigenvalue, variance, energy and projected-beta-min conditions hold with c₀=C₀=M₀=1, but σ_𝒞,n²=1+n² and the sample BM ratio tends to zero rather than infinity. This counterexample is outside GR's fixed-τ² scope, so it does not refute the locked theorem under that scope.
2. Define 𝒜_n by the actual finite-n energy, anchored eigenvalue and coefficient inequalities, not by the asymptotic phrase “(H-MIS) holds” at L2:66. Specify the envelope M_n=M′_nφ₀²/(2σ_𝒞²) and the deterministic starting index for s≤K and Nφ₀²≥1. This makes the use of MIS(ii) precise.
3. For the displayed one-sided DS bound, cite the proof of Vershynin Cor. 5.35 together with Thm 5.32 and Prop. 5.34. The corollary's printed two-sided event has failure **2**exp(−t²/2); its proof applied to −s_min gives the required one-sided exp(−t²/2). Alternatively use the printed corollary and replace k_n n⁻² by 2k_n n⁻² everywhere; the conclusion is unchanged. [Primary text, §5.3.1](https://arxiv.org/pdf/1011.3027).
4. At L2:81 sum only over 1≤k≤min(p,k_n), and at L2:89 replace “K≥min(p,⌊n/2⌋)” by equality. These are bookkeeping corrections.

## Corollary H — VERIFIED

L3:13–28 correctly generalizes T38:41–45. RO/GUARD-W transfers outputs pathwise to the potential run. For any feasible T, π(T)>1/2 makes T the strict global score maximizer. If it was scored, the running-best rule returns it. Thus the error is contained in {1−π(T)≥1/2} union the potential-run never-scored event. Markov gives exactly 2E[1−π(T)]+D_n(T), under any input law. Design measurability of T is more than sufficient; no truth-specific Gaussian premise is used. SoP:477–480 confirms that the deterministic δ₁ is pointwise, whereas its probability bound uses expectation. L3 follows that corrected reading.

For the asymptotic sentence, use the same bounded-variable convergence-in-mean argument given above. Its reference to Theorem F remains conditional on F being established elsewhere; this review does not validate F.

## Corollary D — VERIFIED

L3:32–47 is a valid transfer of GEN C3/C3-fav/C4. All run quantities are functions of candidate data and independent uniforms. GEN G explicitly allows any fixed positive noise variance (GEN STATEMENT:29–31), so substitution of σ_𝒞² is legitimate without a scale-invariance theorem. The response is standardized in precisely the same way in both experiments.

The substitution is correctly made in v_T, E_{T,l}, VIS, NL and BM; μ and Δ_T use the projected signal, with no second addition of τ². GEN H0 requires BM-∞; the text correctly refuses a BM(c)-only extension. GEN C4 and L5:68–77 supply canonical conditional versions and common constants/envelopes for measurable random-design coefficients and certificates. Merely having the deterministic conditions hold with probability tending to one, without those envelopes, would not suffice; Corollary D explicitly invokes C4.

The liminf equality follows from P(𝒪,Ŝ⁺=S₀^𝒞)=1−P(U_n)−o(1), not from a delivery claim. All named implementation premises remain hypotheses. In particular this transfer does not prove e4 or production LS0 integration.

## Optional Corollary D′ — VERIFIED-WITH-AMENDMENTS

The construction is a valid fixed-candidate GR experiment. The omitted raw column is random; multiplying it by its structural coefficient θ_n gives θ_n x_{j₂}+τz exactly. Thus j₂ is a structural null but belongs to the projected support, and effective variance 1+τ² is fixed.

GEN L6(c):90–98 gives the actual partition, full Gram floor, bounded energy and both anchored eigenvalue conditions, independently of σ². Its BM ratio becomes √n/(2σ_𝒞²log n)→∞. For visibility the residual norm floor is 3N/4 and the cross contribution is at most Nε_n; v_U≤σ_𝒞²+3n^(−1/2). A simple valid deterministic choice is M_n=√n/(4σ_𝒞²log n) for all sufficiently large n. This leaves a factor-three margin relative to the asymptotic gain, so the unspecified multiplicative (1+o(1))⁻¹ in L3:63 is unnecessary.

Exact amendment: replace L3:64–65's justification “E_{T,l}→0 since δ→0 and v_T≥σ_𝒞²” by a rate calculation. That implication alone is false because h_n grows like √log n. From GEN L6(c):104–105, uniformly over every leakage triple,

    δ² ≤ (16/3)n^(−1/2)(n−1)ε_n² = O(n^(−7/6))

for the larger ε_n=n^(−1/2)/p, since p is asymptotic to n^(1/3); the other variant is smaller. Consequently

    0 ≤ E_{T,l} ≤ δ²/(2σ_𝒞²) + |δ|h_n/σ_𝒞 → 0 uniformly.

This proves NL_avg, for example with κ=1/4 and any fixed ε₀>0, and also NL_C and NL_η for every fixed positive admissible η. Alternatively cite GEN's NL_η⇒NL_avg implication directly, after verifying its threshold and choosing ε₀,κ accordingly. These repairs establish H0,H2 with S*=S₀^𝒞 for every fixed σ_𝒞²>0; H1 is unnecessary. D′'s output-intersection claim follows, with no discovery/delivery probability asserted.

## Numerical context and limits

I inspected SUMMARY.md and the candidate posterior implementation/generators in mis_core.py and run_experiments.py. Their score, sample normalization, cap and per-model weight match the stated target. The proxy and cancellation experiments concern population projection support, as the proof requires. These runs do not establish the asymptotic rates, the growing-p design lemma, or the GEN/LS0 conclusion; N5 is correctly outside GR. No experiments were rerun and no numerical outputs were modified.

**OVERALL VERDICT: VERIFIED-WITH-AMENDMENTS.** The Gaussian experiment reduction, diagonal argument, projection identities and GEN/HPM transfers survive the adversarial checks under the locked fixed-variance scope. Apply the exact envelope, citation and leakage-rate amendments above before calling L1–L3 fully checked. The optional growing-p claim is false if read without the inherited fixed effective-variance hypothesis; an explicit counterexample is supplied above.
