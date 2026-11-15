# Independent blind proof check: B and C

Checked against W3-PSHARP STATEMENT v1.2. Line numbers below refer to the files as read, before any amendments. No proof source was modified.

## Verdicts and findings

| File | Verdict |
| --- | --- |
| `lemmas/B_sparsity.md` | **VERIFIED** |
| `lemmas/C_counterexample.md` | **VERIFIED-WITH-AMENDMENTS** |

Counts: **FATAL 0; MAJOR 0; MINOR 3; NIT 1.** All four findings concern commentary or numerical descriptions in C; none invalidates Proposition C items 1–3 or Corollary B.

### Findings, with exact corrections

1. **MINOR — `Theory_work/Wave3/W3-PSHARP/lemmas/C_counterexample.md:53`: false monotonicity of the exact quantity.** The value at n=200 is correct, but “decreasing” is false when interpreted over all integer n. For n=200 and 201, k=64, p=66, m=32, hence R is identical and n²R increases from 0.000356392383048979 to 0.000359965216689045. The scan finds an even larger value 0.000519284312442154 at n=225. Replace the parenthesis by: “Exact values: ... E2 — n²R = 3.6·10⁻⁴ at n=200; the selected larger-n values are smaller. The decreasing upper envelope in lines 46–47 proves the bound for every n≥200.” The proof never requires exact monotonicity.

2. **MINOR — `Theory_work/Wave3/W3-PSHARP/lemmas/C_counterexample.md:99`: overly strong condition for nonvacuity.** “Its bound is then vacuous unless log L ≫ n³b²/k” confuses a nontrivial bound with a bound tending to zero. Writing H_n=‖θ‖²/n, the coefficient-dependent term is asymptotic to H_n/(σ*² log L). Taking log L=C H_n with a sufficiently large fixed C gives a nontrivial bound without log L/H_n→∞. Replace the sentence after the semicolon by: “For fixed L the bound is eventually vacuous; to make its right side tend to zero with a growing threshold L=L_n one needs log L_n ≫ n³b²/k.” This preserves the intended point that this application supplies no fixed-constant tightness bound.

3. **MINOR — `Theory_work/Wave3/W3-PSHARP/lemmas/C_counterexample.md:106`: incorrect description of what has been shown.** Lines 104–105 choose b_n²=1200 V₀(log n)²/n, and lines 37–38 give
   
   `600 V₀(1−1/n)(log n)² ≤ min B_T ≤ 1200 V₀(1−1/n)(log n)²`.
   
   Thus failure at cost **of order (log n)² has been shown**. Replace lines 106–107 through “is open” by: “Shown: a sufficiently large constant multiple of (log n)² can break the conclusion. Not shown: whether an allowance B_n=o((log n)²) can break it, or the sharp constant at logarithmic-square order. Bounded cost is sufficient; the intermediate regime remains open.” Read STATEMENT:143's “gap” as this intermediate regime. The asserted failure for every B_n/(log n)²→∞ is valid and needs no weakening.

4. **NIT — `Theory_work/Wave3/W3-PSHARP/lemmas/C_counterexample.md:115`: numerical upper bound rounded downward.** The supplied output has maximum 3.149·10⁻¹³ in the n=50 control row, exceeding the asserted “≤3·10⁻¹³ in every seed.” Replace by “≤3.2·10⁻¹³ in every seed” (or give 3.149·10⁻¹³). This is a description of the supplied numerical output, not part of the proof.

## Scope and source discipline

Read the brief first; then B, C, the PSHARP statement, and the permitted dependency `S_one_step.md`. Read only the specified ranges of W3-POST STATEMENT (16–39), L1a_size_tail (9–19), W3-POST2 B_tail_approx (6–14), and W3-POST2 STATEMENT (44). Also read permitted numerics `core.py`, `c_counter.py`, and `b_check_out.txt`, `c_counter_out.txt`. No other review, log, plan, report, checkpoint, assumption map, or A proof was read. Existing numerical outputs were inspected as supplied, not represented as freshly reproduced full experiments.

New independent numerical checks and their output are `reviews/KBC_scratch/check.py` and `reviews/KBC_scratch/results.json`. They use `py -3.13 -I`, numpy and standard-library exact rational arithmetic. No imports of repository helpers, bytecode files, commits, or subagents were needed.

## Dependency check: Lemma V and Lemma S

These are dependencies, not additional requested per-file verdicts.

- **V, lines 8–15: VERIFIED.** Expanding gives Hessian H_S/n since G_S+(G_S+I)/n=((n+1)G_S+I)/n. H_S is positive definite even for dependent columns; the unique minimizer is nH_S⁻¹z_S, with objective Q_S. Both original terms are nonnegative. Scaling by s_y² and substituting the coefficient divided by s_y proves the raw-response form. For S=∅ the coefficient space has dimension zero and Q=yᵀy. No rank restriction is required.
- **S(1), lines 18–35: VERIFIED.** The appended diagonal entries are n² in H and n in G+I, giving the stated two positive Schur complements. The difference matrix has eigenvalue
  
  `[(n+1)λ+n²+n+1]/[((n+1)λ+1)(λ+1)] > 0`
  
  for every λ≥0. Thus the determinant ratio is ≤n, with equality exactly when g=0. This includes singular G, where both regularized matrices remain invertible. For S=∅ equality holds and the ratio is n. Iteration works even outside Ω as a matrix identity; B and C use it only for admissible models.
- **S(2), lines 37–43: VERIFIED.** The block inverse gives exactly n(x_jᵀρ̃_S)²/s for the Q decrease. Positivity and s≤n² give its lower bound; V supplies Q≥0. No extra independence, rank, or projection identity is used.
- **S(3–4), lines 45–57: VERIFIED.** Prior ratio, determinant factor and fit ratio have the stated directions. Since b₀>0, γ∈[0,1), and −log(1−γ)≥γ. Distinct singleton supersets contribute distinct positive odds terms; an empty null set gives a zero right side. These parts are not needed for the main B/C arguments but introduce no incompatible hypothesis.

## B: line-by-line derivation

The domain throughout is n≥3, p≥2, s_y>0 and 0≤s₀≤K−1; no truth or data law is assumed. The phrase “every data set” inherits s_y>0 from §0. In particular s₀<p, and all denominators below are positive.

| Place in B | Check |
| --- | --- |
| 7–10 | **VERIFIED:** the displayed conclusions follow from the derivations below, including s₀=0. |
| 13–14 | **VERIFIED:** j≤K−s₀ implies S_J∈Ω. Cancel the common posterior normalizer; all factors are finite and strictly positive. |
| 15–17 | **VERIFIED:** iterate S(1–2) along j additions. Every intermediate model has size ≤K−1. Q cannot increase, so the fit factor is ≥1; D can increase by at most n each time, so its inverse square-root factor is ≥n^(−j/2). |
| 17–19 | **VERIFIED:** there are C(p−s₀,j) distinct supersets at level j, disjoint across levels and excluding S₀. Since π(S₀)>0, δ/(1−δ) is exactly the sum of all other model odds. Restricting that sum gives the lower bound. |
| 20–21 | **VERIFIED:** the binomial ratio is (s₀+j)!/s₀! divided by the falling product of 2p−1−s₀. Multiplication by the count cancels j! and yields C(s₀+j,j) times the displayed falling-product ratio. This is an exact finite-sum expression, with no missing truncation or multiplicity factor. |
| 22–23 | **VERIFIED:** j=1 is available since s₀≤K−1. It is exactly c(p,s₀)/√n. Taking the reciprocal of 1+odds gives the stated caps, including √n/(√n+c). |
| 25 | **VERIFIED:** the comparison with 1/3 is equivalent to p+1≥2s₀, implied by s₀≤p/2. |
| 26 | **VERIFIED:** numerator minus denominator in c≥1 is (s₀−1)(p−s₀−1). Both factors are nonnegative for 1≤s₀≤p−1. For s₀=0 the separate value p/(2p−1)>1/2 is correct. |
| 27 | **VERIFIED:** division by p gives the stated limit 1/2. |
| 29–31 | **VERIFIED:** the additional restriction s₀≤p/2 permits a_n=(s₀+1)/(3√n), with pointwise π≤1/(1+a_n) and δ≥a_n/(1+a_n). |
| 32–34, B1 | **VERIFIED:** if a deterministic upper bound bounded away from 1 occurred along a further subsequence, convergence of π to 1 in probability would be impossible. Hence a_n→0 is necessary. The λ bound and the a_n→∞ conclusion follow pointwise. “Surely” needs no separate probabilistic estimate: the deterministic bound holds for every realization. |
| 35–36 | **VERIFIED:** critical scale implies s₀→∞ and s₀=o(n); s₀/p→0 implies p−s₀→∞. More explicitly K−s₀=min(p−s₀,⌊n/2⌋−s₀), and both arguments tend to infinity. Thus every fixed j eventually appears. |
| 37–38 | **VERIFIED:** for fixed j, C(s₀+j,j)n^(−j/2)=Π_(l=1)^j((s₀+l)/√n)/j!→λ^j/j!. Each falling-product ratio tends to 1/2. The term limit is (λ/2)^j/j!. |
| 39 | **VERIFIED:** for each fixed J, eventual inclusion and nonnegativity imply liminf of the full sum is at least the limit of its first J terms. Supremum over J yields e^(λ/2)−1. No exchange of an infinite sum and a limit, and no dominating function, is asserted or required. |
| 40 | **VERIFIED:** x↦1/(1+x) is continuous and decreasing on [0,∞); the liminf lower bound therefore gives limsup π≤e^(−λ/2), pointwise for every sequence of data and designs. |
| 41–43, B2 | **VERIFIED:** for a deterministic positive rate ρ_n→0, O_P gives one fixed finite C and eventual probability at least 1/2 of δ≤Cρ_n. On that nonempty event the deterministic a_n/(1+a_n)≤Cρ_n; hence it holds numerically. Eventually Cρ_n≤1/2 and a_n≤Cρ_n/(1−Cρ_n)≤2Cρ_n. Therefore s₀+1=O(√nρ_n). For r_n the resulting s₀=O(√log n) is correct. A zero rate is excluded by the usual definition of O_P(ρ_n); direct zero-error concentration would contradict the strictly positive lower bound. |
| 43–47, witness part/B3 | **VERIFIED as a consequence of the explicitly invoked Corollary A2:** see coverage discussion below. It is not asserted to follow from the design-free j=1 bound alone. |
| 50–52 | **VERIFIED as an algebraic comparison:** keeping all superset determinant ratios and then bounding each by n^j gives exactly the stated relation. The specified domain for c≥1 is correct. No independent verification of the excluded parent proof is claimed. |
| 53–54 | **VERIFIED:** for orthogonal X every one-column determinant ratio is n; y orthogonal to col X gives every z_S=0, hence Q_S=yᵀy. Thus the superset odds equal the finite sum. Other models can contribute additional odds when S₀≠∅; the text correctly says “superset odds.” |
| 55–59 | **VERIFIED against the permitted supplied output:** the tabulated critical-scale values, 55,740 cases and minimum ratio 1.033240 agree with the descriptions. These observations do not replace the proof. |

### B coverage and probability

STATEMENT:92–102 (Corollary B, constants, B1 and critical scale) and the design-free part of 103–104 are fully proved. There is no new probabilistic model in B: randomness may come from data or designs, and the deterministic inequalities apply simultaneously. S₀ and its size are the specified problem sequence, as in the statement; the O_P necessity is about that deterministic sequence of sizes.

The witness clause of B2 and B3 explicitly depend on A2 (STATEMENT:75–77). Its proof file is outside this brief, so this check verifies the implication from the recorded A2 statement, not A2 itself. Set h_n=(s₀+1)√(log p/(πn)); A2 gives odds≥(1−o_P(1))h_n. If δ→0, odds→0, forcing h_n→0 and s₀=o(√(n/log p)). If δ=O_P(r_n), odds=O_P(r_n) because δ→0; the high-probability lower bound forces h_n=O(r_n). For log p≍log n this yields s₀=O(1). In the consistency regime δ=odds/(1+odds) has the corresponding rate obstruction. If h_n does not vanish, consistency is already ruled out, rather than an unbounded lower bound on δ being claimed. For a general witness block the same argument uses Λ_n. Hence the recorded growing-s₀ target cannot retain r_n on those witnesses. The caveat for log p=o(log n) is compatible with this reasoning. The final obstruction at s₀≍√n follows directly from B1; no HPM consistency theorem is proved or needed by the statement's “can be aimed at” wording.

**No B statement item is left without either a proof here or the explicitly declared A2 dependency.** Independent verification of A2 remains outside scope, not a silent assumption in this verdict.

## C: line-by-line derivation

Fix σ*²>0 and b̄>0; V₀=σ*²+b̄² is fixed. The signal b=b_n is deterministic. All statements involving its lower bound are conditional on 0<b≤b̄ and nb²≥1200V₀(log n)². This is not feasible at n=200, but the design/cutoff bounds are unconditional for n≥200 and feasible signal sequences exist eventually because (log n)²/n→0. There is no claim that such a b exists at every small n.

### §0 and item 1

- **8–10: VERIFIED.** k is an integer, T′ has k indices, and the construction takes k+1 mutually orthogonal centered vectors; x₂ is their specified linear combination. Raw X^r=X already has column sample variances one, so the truth's standardization leaves β*=θ*. Each active coefficient is nonzero.
- **12–15 (F1): VERIFIED.** k≤12L+1 gives p≤12L+3. The function 12log n+3−n/2 has derivative 12/n−1/2<0 for n≥200 and is negative at 200 (66.5798084−100). Thus p≤⌊n/2⌋, K=p, and all subsets including T′ are admissible. Also k+1=p−1≤n−1, so an orthogonal family of this size exists in 1^⊥. No full-column-rank assumption on X is required.
- **16–18 (F2–F4): VERIFIED.** ‖u‖²=k(n−1); the cross term x₁ᵀu vanishes. Multiplication by c² normalizes x₂ exactly. Its inner products are c(n−1) with x₁ and −cη(n−1) with each active column. Its membership in the original orthogonal span preserves rank k+1. The bounds c≤1 and k≤n² follow immediately (the latter also from F1).
- **21–25: VERIFIED.** ‖μ‖²=b²(n−1), and x₁−x₂/c=ηu gives the exact representation on T. The coefficient norm is b²/(η²k)(2+η²k)≥b²n⁴/k. Dividing by n and substituting the signal lower bound gives n²·1200V₀L²/(12L+1)→∞. Since η>0, k>0 and u≠0 is orthogonal to x₁, x₁ and x₂ are independent; no different exact representation on T can repair the coefficient norm. These are exactly the hypotheses in the permitted L1a′ statement, except its fixed coefficient bound.
- **27–32, Lemma P projection: VERIFIED.** The missing active columns are an orthogonal family. Their projection kills x₁ and all included active columns. It takes x₂ to −cη times their sum; thus residual projection has coefficient b/√k+cηϑ₂, with the plus sign as written. If 2∉S, setting ϑ₂=0 is valid. If 1∈S its projection is zero. Both columns can be present or absent; S can be empty. Projecting can only reduce squared norm.
- **33–34, Lemma P minimization: VERIFIED.** Complete the square in A(β+γx)²+x²/n. The positive quadratic coefficient is Aγ²+1/n, the minimizer is −Aγβ/(Aγ²+1/n), and the minimum is Aβ²/(1+nAγ²). Applying the minimum to the actual coefficient (or relaxing the constraint x=0 if column 2 is absent) proves the first inequality. Since d≤k and c≤1, n(n−1)dc²η²≤k/n²≤1, proving the second. This proof also covers rank-deficient S.
- **36–38, reference lower/upper cost: VERIFIED.** Drop ‖X_Tϑ‖²/n and all coefficient penalties except ϑ₂²/n, then apply P at d=k. Its denominator is ≤1+k/n²≤2. Choosing ϑ=0 gives the stated upper bound. The cost is coercive, so its minimum exists. Since (n−1)/n is bounded away from zero, these bounds give exact order nb², diverging at least logarithmically squared.
- **39: VERIFIED.** On T′ the exact coefficients have squared norm b² and fitted squared norm b²(n−1). Their cost is precisely b²≤b̄². This is a different reference with k columns and does not repair the claims for T.

### §2, item 2: every constant and cutoff

- **42–44: VERIFIED.** q_j=½Π_(i=0)^(j−1)(p−i)/(2p−1−i). The first factor is ≤2/3 for p≥2; subsequent factors are ≤1/2 since i≥1. Thus q_j≤(2/3)2^(−j), and the tail is ≤(2/3)2^(−m). Here m=m_n≥2, so no q₀ issue occurs. Exactly 1/w(2)=2C(2p−1,2)=(2p−1)(2p−2)≤4p²; therefore R≤(8/3)p²2^(−m).
- **45: VERIFIED.** m=⌊k/2⌋≥(k−1)/2≥6L−1/2 gives 2^(−m)≤√2 n^(−6log2), with 6log2=4.158883083... . The ceiling/floor effects have been bounded in the safe direction.
- **46–47: VERIFIED.** Since n≥1, n^(−2.158883...)≤n^(−2.158), and 8√2/3=3.771236...≤3.78. At n=200 the final upper envelope is 0.1813653<0.19<1. Its logarithmic derivative has sign 24/(12L+3)−2.158<0 at and beyond 200. This proves the bound for all real n≥200, hence every integer n, without exact-tail monotonicity.
- **48: VERIFIED.** The defining threshold for t=2, ω=L/2 is n^(−3/2)e^(−L/2)=n⁻². Since m_n≥2 and R at that m satisfies this threshold, the minimum admissible cutoff is ≤m_n. The empty-tail endpoint m=K ensures existence.
- **49–50: VERIFIED.** For a 2×2 Gram matrix, det(I+aG)=1+a tr G+a²det G. Here tr G_T=2(n−1) and det G_T=(n−1)²η²k/(1+η²k)≤k/n². The numerator is ≤2n²−1+(1+1/n)²k≤2n²+2k because (1+1/n)²≤(4/3)²<2 for n≥3. This supplies the omitted elementary justification for its last inequality.
- **51: VERIFIED.** The denominator is ≥2n−1. The claimed ratio is ≤2n when 2k≤2n²−2n; F1 gives this with considerable slack for n≥200.
- **52: VERIFIED.** R≤n⁻² and D_T≤2n give A≤√2/n≤2/n≤n^(−1/2) (last step needs n≥4, satisfied here).
- **53:** value at 200 verified; monotonicity requires finding 1's correction.

### §3, item 3: uniform posterior loss

- **56, 58–59: VERIFIED.** If |S|≤m≤k/2 then d=k−|S∩T′|≥k/2. The coefficient penalty ‖ϑ‖²/n dominates ϑ₂²/n. P therefore gives L_S≥(n−1)b²/4, including S=∅ and all four reference-column membership patterns.
- **61: VERIFIED.** Lemma V's raw-response version applies to Cy^r=μ+Cε, and its penalty is (G_S+I)/n, not an unregularized least-squares penalty.
- **62–64: VERIFIED.** The residual v=μ−X_Sϑ lies in the fixed centered space 𝒳. Thus vᵀCε=vᵀε=vᵀP_𝒳ε. Cauchy–Schwarz followed by 2ab≤a²/2+2b² gives the displayed lower bound. The penalty dominates half of ‖ϑ‖²/n; dropping its remaining nonnegative part is permitted.
- **65: VERIFIED.** Minimization yields half of L_S plus the common noise terms. Substitution of L_S≥(n−1)b²/4 gives the additive loss (n−1)b²/8. This is one simultaneous deterministic inequality for all S; there is no union bound over models.
- **67–68: VERIFIED.** Evaluate V at the exact T′ coefficients. The residual is Cε and its ridge penalty is b²; this is an upper bound on the minimized Q, with the correct raw-response scale.
- **70–71: VERIFIED.** For the fixed design, C and P_𝒳 are orthogonal projections of ranks n−1 and k+1. Isotropic Gaussian noise therefore gives the two asserted chi-square marginal laws. They are dependent (𝒳⊂1^⊥), but independence is not used. Chebyshev gives P(χ²_r>2r)≤2/r; the union bound gives 2/(n−1)+2/(k+1)→0. This bound is uniform over all choices of the orthogonal family, over b, and over the stated fixed constants. Standardization is defined almost surely since σ*²>0 gives P(s_y=0)=0.
- **72: VERIFIED.** a=2b₀s_y²=.02‖μ+Cε‖²/(n−1). The squared-sum bound produces .04(b²+2σ*²) on F_n. The use of the random s_y is thus controlled explicitly, without treating standardized y as Gaussian.
- **73–75: VERIFIED.** k+1≤12L+2 gives the coefficient (48L+8)/(1200L²). It decreases for L>0 and at log200 is 0.0077870498<0.0078. Also (n−1)/(8n)≥199/1600=.124375≥.1243 and 1/n≤.005. Hence Δ/(nb²)≥.1243−.0078−.005=.1115≥.111≥.1. The rounded log200 lower bound 5.298 used in the text is safe; 5.298²=28.068804, and evaluating the text's rounded expression still gives <.0078.
- **76–78: VERIFIED.** Steps 2–3 imply a+s_y²Q_S≥a+s_y²Q_T′+Δ. The denominator a+s_y²Q_T′ is positive and ≤a+‖Cε‖²+b². On F_n this is ≤2σ*²n+1.04b̄²≤2nV₀. Thus the ratio is at least 1+b²/(20V₀), with no reversal from substituting an upper bound on the denominator.
- **79–80: VERIFIED.** x=b²/(20V₀)∈(0,1/20]. Integrating or differentiating gives log(1+x)≥x−x²/2≥.975x on that interval. Since ν≥n/2, the reciprocal fit ratio to power ν is ≤exp[−.975nb²/(40V₀)]≤exp[−nb²/(42V₀)], because .975/40=.024375>1/42=.0238095238.
- **82–85: VERIFIED.** S≠T′ and both are admissible. The ratio formula is exact. Its prior factor is ≤C(2p−1,k)≤2^(2p−1), since its denominator is ≥1. T′ is orthogonal, so D_T′=n^k exactly. Each Gram eigenvalue λ≥0 contributes ((n+1)λ+1)/(λ+1)≥1 to D_S; empty products give D_∅=1. There are at most 2^p small models.
- **86: VERIFIED.** π(T′)≤1 implies π(S)≤π(S)/π(T′). Summing the uniform ratio bound gives 2^(3p−1)n^(k/2) times the fit exponential. There is no missing posterior normalizer.
- **87–88: VERIFIED.** p≤12L+3 and k≤12L+1 give entropy ≤(36L+8)log2+(6L+1/2)L. Since log2<.6932, this is ≤6L²+25.5L+5.6. The polynomial 6L²−25.5L−5.6 is positive at 4.46 and increasing thereafter; L≥log200 suffices. Finally 12L²≤nb²/(100V₀).
- **89: VERIFIED.** 1/42−1/100=29/2100=.0138095238 is larger than 1/73=.0136986301. Thus c₁=1/(73V₀) is valid and depends only on (σ*²,b̄).
- **90–91: VERIFIED.** F_n has probability tending to one, and nb²→∞, proving exactly the exponential high-probability conclusion. Since m^T_n≤m_n, the tail above the former is at least the tail above the latter. The resulting convergence to one is in probability.

### §4, what fails, and §5 numerical descriptions

- **94–96: VERIFIED.** The quoted L1a′ definition, constants, and tail inequality match exactly the permitted lines 10–19. Fixed σ*²,M,M′ give asymptotic tightness uniformly in m. For this reference t=2, the cutoff identity gives π(tail)=O_P(n^(−1/2)); the factor (1+1/n)^(t/2) stays bounded.
- **97–98: VERIFIED.** m_n<k<K, so R at m_n is strictly positive. On F_n the tail is ≥1−e^(−c₁nb²); R≤n⁻² gives the lower bound for Θ. Its deterministic factor n²/((n+1)√n) grows like √n. Hence Θ→∞ in probability and tail at m^T_n→1. This disproves a uniform version with the coefficient bound omitted, not the actual lemma with a fixed valid M′.
- **99–100:** the actual norm satisfies ‖θ‖²/n=b²n³(2+η²k)/k, hence its stated order is correct, and the lemma can be applied separately at each n with this growing M′. The final nonvacuity description needs finding 2's correction.
- **101: VERIFIED.** The permitted 1a″ statement assumes deterministic ϑ with cost ≤B and defines exactly A and Θ″. Its bound has C″(B)=1/√2+1/2+B/(2σ*²)+√(2B/π)/σ*, giving tightness for fixed M,B (and σ*²). No dependence on reference size was silently inserted.
- **102–103: VERIFIED.** A>0 at m_n and A≤2/n imply Θ″≥(1−e^(−c₁nb²))n/2 on F_n, so Θ″→∞ in probability. Exact approximation on T is possible, but cost remains large for every coefficient vector; approximation error alone cannot replace the cost hypothesis.
- **104–105: VERIFIED.** For any deterministic allowance B_n with B_n/L²→∞, fix σ*²,b̄ and set b_n²=1200V₀L²/n. Eventually b_n≤b̄ and nb_n²≤B_n. The deterministic choice ϑ=0 already gives cost b_n²(n−1)≤B_n. All signal hypotheses hold and the failed posterior conclusion still follows. Exact-fit coefficients are not required to be the same coefficients witnessing the cost allowance; the relaxed lemma only asks for existence of a deterministic cost witness. This argument establishes precisely the asserted failure for these growing allowances.
- **106–107:** the “not shown” sentence is false at logarithmic-square order; finding 3 gives the correction. The strictly intermediate cost regime is not resolved by this proof. Sufficiency of fixed cost is part of the quoted 1a″ statement. The cited N6b experiment is outside the allowed source set and was not independently checked; its existence is unnecessary to any of the counterexample implications.
- **108:** the mechanism is rigorously expressed by P and Steps 1–2: small models have large penalized signal loss. Since T itself is an exact unpenalized representation, “needs ≍log n columns” should be understood here as needing such a size to attain small ridge cost, not as an unpenalized representability assertion.
- **111–114: VERIFIED against supplied script/output.** V1's two errors, E2's cutoffs, and the rounded counter-arm medians at b=3 are accurately described. The enumerated k=16–22 experiments explicitly use scaled-down k and do not meet the theorem's signal threshold; they illustrate the mechanism, rather than empirically verify the asymptotic high-signal theorem. No full E1 rerun was necessary for the independent algebraic checks.
- **115:** the control-arm upper bound needs finding 4's rounding correction.

### C coverage

STATEMENT:118–122's design, standardization and truth are realized. Item 1 (125–131) is proved by §1 and P, including the “every coefficient vector” cost lower bound and the alternative bounded-cost reference. Item 2 (132–133) is proved for every n≥200 by §2. Item 3 (134–135) is proved by §3 with the explicit c₁. The consequences in 137–142 are proved by §4: divergence is in probability, the failure concerns the reference T, and every allowance B_n/(log n)²→∞ is covered. The intermediate-cost question in 143 is open in the restricted sense clarified above. **No item of Proposition C is unproved, and no stronger signal, rank, independence, or design hypothesis has been silently used.** The four amendments concern the accompanying descriptions.

## Independent numerical checks and analytic extension beyond the scan

All assertions in the scratch script passed, exit code 0. The checks are separate implementations, not reruns of the supplied helper functions.

| Check | Result |
| --- | --- |
| Exact rational B coefficient identity, p=2,...,60, every s=0,...,p−1 and j=1,...,p−s | 37,819 identities; constant inequalities also pass at endpoints |
| Dense random posterior enumeration, (n,p)=(3,2),(4,3),(6,4),(10,5),(16,6), four designs each, including duplicated columns | Minimum actual odds / B lower bound = 1.14838413447 |
| Dense one-step determinant/fit and variational identities | 1,244 one-step pairs; maximum absolute discrepancy 9.77·10⁻¹⁴ |
| Lemma P independent augmented least-squares minimization, all subsets with d≥1, n=20,k=4 and n=200,k=6, η=n⁻² and η=.05 | 624 cases; minimum actual cost / bound = 0.9999999999999991, consistent with rounding |
| Every integer n=200,...,2,000,000, actual k=⌈12log n⌉ | All design-dimension, R≤n⁻², D_T≤2n, A≤2/n, Δ≥nb²/10, and entropy bounds pass |
| Maximum n²R over scan | 0.0005192843124421544 at n=225 |
| Maximum nA over scan | 0.0005200257910970326 at n=225 |
| Maximum D_T/n over scan | 1.003291716123444 at n=200 |
| Minimum normalized Δ lower bound using the actual ceiling k | 0.111656797578724 at n=200 |
| Exponent comparison | (1/42−1/100)−1/73 = 0.000110893672538 > 0 |

The scan is finite and is not used to infer all-n validity. The analytic monotone envelopes in §2 and the explicit constant inequalities checked above extend the proof to every n≥200, independently of all ceiling transitions. For critical scale, the finite-partial-sum argument above supplies the limit justification; the supplied T1 table is corroboration only.
