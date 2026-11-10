# R04: independent line-by-line proof check of L5 and L6

Scope: every line of L5_exact.md and L6_sharp.md, checked against STATEMENT.md §§0–2, L1_score.md, L2_noise.md, and the stated screening results in L3_screening.md. No proof of SCR-A/A° is independently certified here. No subagents or git commands were used. Only this report and R04_scratch/ were written.

## Verdicts

| Item | Verdict |
|---|---|
| L5.1 Step 1 | CORRECT |
| L5.1 Step 2 | CORRECT |
| L5.1 Step 3 | CORRECT |
| L5.2 | CORRECT |
| SCR-C | CORRECT-WITH-MINOR-FIX |
| Remark on ω(S) | WRONG |
| SCR-R | CORRECT-WITH-MINOR-FIX |
| SCR-N | CORRECT-WITH-MINOR-FIX |
| Consequence 1 | CORRECT |
| Consequence 2 | CORRECT-WITH-MINOR-FIX |

The delivered statements of SCR-C, SCR-R and SCR-N survive this check. The substantive false claim is the separate, explicitly unclaimed-in-the-statement ω remark. Consequence 2 has an incorrect displayed asymptotic rate and an unsupported final inference about the square. Other repairs are local proof wording/case fixes.

## Numbered findings

1. **MAJOR — The ω-only replacement in the remark is false.**

   Location: `lemmas/L5_exact.md`, remark: “SCR-C holds under sup_S ω(S) ≤ (2 log p + log n)/(2 log p) − ε.”

   Step 2 indeed permits replacing 1/φ by ω(S). Step 1 still needs a determinant lower bound: ω controls the angles between normalized dual directions, not their unnormalized residual lengths a(j|S\j), and therefore does not supply the log n term in Λ_k. It is not legitimate to discard that use of the floor.

   Here is a fixed-s₀ counterexample to the resulting exclusion of LO supersets. Set σ=1, p=4, q=3, S₀={1}, θ*=(1,0,0,0). In the centred subspace choose orthonormal e₁,e₂,e₃,e₄ and set

       x₁=√(n−1)e₁,
       x₂=√(n−1)e₂,
       x₃=√(n−1)(cos(3/n)e₂+sin(3/n)e₃),
       x₄=√(n−1)e₄.

   All standardization requirements hold; q≤K−1 eventually. Every model missing truth 1 uses columns orthogonal to x₁. Consequently γ(1|T)=(n−1)²/(n−1+λ₀)~n for every such T, Γ_n(3)~n, τ_n²=2, and (A∞) holds with ratio tending to infinity. Also s₀=1, ‖θ*‖₂=1, and q log p=o(n).

   Every excess set in a superset of size ≤3 has at most two elements, hence ω(S)≤2 (a correlation matrix of dimension ≤2 has largest eigenvalue ≤2). The proposed upper bound (2 log 4+log n)/(2 log 4)−ε tends to infinity, so it holds, for example with fixed ε=1, for all sufficiently large n. In contrast φ_n(3)=1−cos(3/n)~9/(2n²), so the actual SCR-C floor correctly rejects this example.

   Consider S={1,2,3}. Write Z_i=e_i'ε. Take Z₃ in a small interval about 3, Z₁,Z₂,Z₄ in small intervals about zero, and the noise energy in the orthogonal complement divided by n tending to 1. The first conditions have fixed positive probability; the last has probability tending to 1 independently. For j=2 or 3,

       a(j|S\j)~11/n,   a₁(j|S\j)→2,   D(j|S\j)→11/2,
       g_{y_c}(j|S\j)→(9/11)Z₃²,
       q_S(y_c)/n→1.

   Thus the exact score formula gives, at Z₂=0 and uniformly in small neighborhoods,

       F(S\j)−F(S) → log(5/3)+(1/2)log(11/2)−9Z₃²/22.

   At Z₃=3 this limit is approximately −2.3186. Deleting truth 1 loses order n. Adding column 4 loses (1/2)log n+O(1), and swapping either excess column for column 4 also loses (1/2)log n+O(1); swapping out truth 1 loses order n. These exhaust the neighborhood. Hence S is a strict LO superset with probability bounded away from zero. Strictness persists on open Gaussian coordinate intervals, so this is a probability counterexample, not a measure-zero noise realization.

   This disproves the LO-superset exclusion needed for the asserted replacement theorem. A certificate that only certifies LO cannot exclude this model; a statement about a particular algorithm's avoidance of this basin would need a separate algorithmic argument, absent here. The original SCR-C proof and theorem are unaffected.

   Independent direct-score numerical verification is in `reviews/R04_scratch/remark_counterexample.py`. It forms H=(n+1)G+I and evaluates F directly, without using scr_lib.py. At n=10000, Z₃=3 and the other displayed coordinates zero, the two excess deletion differences are about −2.31649, the addition difference is −4.60517, the two excess swap differences are about −7.43248, and removing/replacing truth gives differences below −3459. All seven neighbors are worse. The remaining response energy is explicitly set to n−1, consistent with the asymptotic typical residual energy used above.

   **Fix:** delete the asserted ω-only sufficiency. Retain the valid Step-2 refinement, and state its nonasymptotic consequence with the actual deletion penalties B_j or a separate uniform lower bound on the a(j|S\j). Keeping the original SCR-C floor and merely replacing its Step-2 factor by ω(S) is valid. Any genuinely weaker asymptotic theorem needs both a determinant condition and a carefully scaled positive margin; it does not follow from the displayed ω inequality alone.

2. **MINOR — SCR-C temporarily drops σ from an assumption in a model allowing σ_n to vary.**

   Location: `lemmas/L5_exact.md`, SCR-C, left side (i): “with ‖θ*‖₂ = O(√n) this gives”.

   The hypothesis is ‖θ*‖₂=O(σ√n), and STATEMENT explicitly permits σ to depend on n. The displayed unscaled O(√n) need not hold when σ grows. The immediately following normalized conclusion is nevertheless correct:

       ‖θ*‖₂/(σ√(n²−1))=O(n^(−1/2)).

   **Fix:** replace the phrase by “with ‖θ*‖₂/σ=O(√n)”. No theorem change.

3. **MINOR — SCR-R must explicitly allow the screening event of SCR-A°.**

   Location: `lemmas/L5_exact.md`, SCR-R: “On 𝓔_R ∩ (the event of SCR-A)”.

   STATEMENT allows either (A∞) or (A°∞). Under the second alternative MC need not follow, and the applicable event is the SCR-A° event, not necessarily E1∩E2⁺ with MC. The subsequent refit algebra uses only containment and works on either event.

   **Fix:** write “the screening event supplied by SCR-A or SCR-A°, respectively”. Failure probability for E_R remains exactly 2q_n n^(−2); add the appropriate o(1) screening failure probability when stating the joint event.

4. **MINOR — The lower-bound proof for B_n omits a sign case.**

   Location: `lemmas/L6_sharp.md`, bounds on B_n: “1 − e^(−u) ≥ u(1 − u/2) ... and ... ≥ 1 − n^(−2) give the lower bound.”

   Write c_n=(n+1)(n−0.98)/(n(n+0.02))=1−0.98/(n²+0.02n). The derivation yields B_n≥c_n(1−u/2)L_n. Replacing c_n by its lower bound is valid only if u≤2; when u>2 that multiplication reverses the ordering. The nonasymptotic proposition does not assume log p=o(n), so u>2 is allowed.

   The claimed bound itself is true: if u≥2, its proposed left side is nonpositive while B_n>0. If u<2, the printed multiplication is valid.

   **Fix:** add this two-case argument. This does not affect (★), the probability bound, or either explicit sequence.

5. **MINOR — Consequence 2 loses a factor (log n)² in the final B1 rate.**

   Location: `lemmas/L6_sharp.md`, final sentence: “Lemma B1's lower bound Δ²/(n‖θ*‖₁²) ~ 1/n is of the exact order of Γ_n(0)”.

   Here b²=(log n)², Δ=2(n−1)b²/n, and ‖θ*‖₁²=4b². Exactly,

       Δ²/(n‖θ*‖₁²)=(n−1)²b²/n³ ~ (log n)²/n,
       Γ_n(0)=(n−1)²(n+1)b²/n⁴ ~ (log n)²/n.

   Their ratio Γ/[Δ²/(n‖θ*‖₁²)]=(n+1)/n→1. Thus the “exact order” observation is correct after repairing the written rate. For actual B1, c_θ²=2b²/(n+1), c_θ/√Δ~n^(−1/2), and Δ≥c_θ² eventually, so its precise lower bound Δ(√Δ−c_θ)²/(n‖θ*‖₁²) is also asymptotic to (log n)²/n.

   **Fix:** replace “~1/n” by “~(log n)²/n”.

6. **MINOR — The explicit sequence does not establish the appended claim that the square cannot be dropped.**

   Location: `lemmas/L6_sharp.md`, final clause: “the square in B1 and the ‖θ*‖₁ control cannot be dropped.”

   The sequence establishes that a Δ≥C log(p∨n) condition alone fails, and after finding 5 it demonstrates the order-sharpness of B1 on this sequence. But Δ→∞ here. Replacing Δ² by Δ in its leading expression produces a weaker lower bound, of order 1/n, which this example does not contradict. Therefore the asserted necessity of the square does not follow from this counterexample.

   **Fix:** restrict the conclusion to the demonstrated margin-only failure and order-sharpness, or add a separate scaling argument if “dropping the square” means replacing the homogeneous numerator by Δ uniformly. For fixed X and a nonzero θ with Δ≥c_θ², replacing θ by tθ scales Γ, Δ and c_θ² by t², and ‖θ‖₁² by t². The proposed Δ/(n‖θ‖₁²) would remain constant as t↓0 while Γ→0. This supplies the missing argument for that interpretation. The stated Consequence 2 in STATEMENT, which claims only margin-only failure, is correct.

7. **NOTE — The pair formula for ω requires augmented, not ordinary, partial correlation.**

   Location: `lemmas/L5_exact.md`, remark: “For a pair of excess columns with partial correlation ρ given S₀, ω = 1 + |ρ|.”

   Precisely, ρ=M₁₂/√(M₁₁M₂₂), with M the Gram matrix of (I−P̃_{S₀})x̃_i. Inverting a 2×2 matrix gives the correlation matrix of its inverse with off-diagonal −ρ, hence eigenvalues 1±|ρ|. With ordinary residuals (I−P_{S₀})x_i, the finite-n identity generally fails because M includes ridge augmentation.

   **Fix:** identify ρ explicitly as the augmented partial correlation. The formula is otherwise correct and does not rescue the false sufficiency claim in finding 1.

## Line-by-line verification record (including passed steps)

### L5.1: assumptions, representation and Step 1

- The setting supplies n≥3, σ>0, deterministic X, k≤q≤K−1≤p; m≥1 makes all uses of U(k,x), division by m, and binomial coefficients legitimate. For a given S, φ≤1 also follows from the diagonal of G_S/(n−1) being 1. No restriction on σ being constant is used.
- X̃θ* lies in span X̃_S and also in span X̃_{S\j} for j∈E. The decomposition ỹ_c=X̃θ*−b̃+ε̃ is exactly L1.7, so both identities (1) follow by orthogonality. Centre projection on the noise is correctly preserved in ε̃.
- L1.6 is applied at sizes k−1→k; its prior term is log((2p−k)/k), with the correct shift. Multiplication by τ̂² gives exactly (n+1)(0.02τ̂²+q_S)/(nν). There is no substitution of Q_{S\j} for Q_S.
- For A=G_S+λ₀I, a=1/(A^(−1))_{jj}. Since (A^(−1))_{jj}≤1/λ_min(A), reciprocal order gives a≥λ_min(A)≥φ(n−1)+λ₀. The text uses a weaker valid bound. L1.3 then gives 2B_j≥2log((2p−k)/k)+log(φ(n²−1)/n)=Λ_k.
- L1.1 gives q_S(v)=‖v‖²/(n+1)+n v'R_Sv/(n+1). L1.7 gives v'R_Sv=‖(I−P̃_S)ṽ‖², because I−P̃_S is an orthogonal projector. Thus the lower bound used is valid; it is not the incorrect identity v'R_Sv=‖R_Sv‖² in the original space.
- Pythagoras, reverse triangle inequality, E2chi and E3a give the stated noise-energy minus projection bound. The normalized bias term is √λ₀‖θ*‖₂/[σ√(n−1)]=‖θ*‖₂/[σ√(n²−1)]. When the difference of square roots is negative, nonnegativity of a norm justifies its positive part before squaring. This is exactly the definition of 1−η, and 0≤1−η≤1.
- For B_j≥0 one may drop 0.02τ̂² and insert the q lower bound; for B_j<0 one instead uses g≥0. Thus the positive-part argument does not multiply a lower bound by a negative penalty. In fact B_j≥0 throughout the coded setting: (2p−k)/k≥1 and D≥1. The additional sign discussion is harmless.
- The factor is (n−1)/(2ν)=(n−1)/(n+0.02)=1−1.02/(n+0.02)≥1−1.02/n. It is positive for n≥3. The factor 1/2 from B_j≥Λ_k/2 is correctly absorbed. Equation (2) has no missing n/(n+1) or σ² factor.

### L5.1: Step 2 and Step 3

- Augmented columns are linearly independent even when original columns coincide. Their residuals w_i modulo span X̃_{S₀} form a basis of W of dimension m. M is the stated positive definite Schur complement.
- d_j=Σ_i(M^(−1))_{ji}w_i has inner products δ_ij with w_i. It belongs to W, is orthogonal to the other excess residuals and to the truth span, and is parallel to the leave-one-out residual direction. In fact the proportionality sign can be chosen positive, but allowing signs changes no eigenvalue or squared gain.
- The dual Gram matrix is M^(−1), its diagonal is N, and the normalized Gram matrix is N^(−1/2)M^(−1)N^(−1/2), up to sign conjugation. The matrix norm bound gives λ_max≤max_j[1/(M^(−1))_{jj}]/λ_min(M); the reciprocal diagonal is in the numerator, as required.
- To check λ_min(M)≥λ_min(A), partition A=G_S+λ₀I into truth/excess blocks. For any excess coefficient z, z'Mz=min_b (b,z)'A(b,z)≥λ_min(A)‖z‖². No reversal occurs in this Schur-complement step.
- The numerator ≤n−1+λ₀. Hence its ratio to φ(n−1)+λ₀ is at most 1/φ for 0<φ≤1. This proves the printed factor, including φ=1 and m=1.
- Every normalized direction lies in W, so Ũ'v=Ũ'P_Wv. Inserting v=ε̃−b̃ is justified by (1). Triangle inequality and contraction of P_W bound the bias by ‖θ*‖₂/√(n+1). This is the only bias size used in (3).
- E3b applies to precisely this W(E). S₀ is fixed and S=S₀∪E, so W is determined by E and X, with no noise dependence and no missing union over truth subsets. There are exactly C(p−s₀,m) choices at size m. For an orthonormal basis B of W, the noise quadratic form is ε'CB₁B₁'Cε, a positive contraction of rank ≤m. T3 therefore gives domination by σ²χ²_m despite the zero lower noise block. T2 with t=log C(p−s₀,m)+x'm gives U'. The union bound at size m is e^(−x'm), whose sum is e^(−x')/(1−e^(−x')).
- Summing (2), comparing (3), multiplying by φ and dividing by mσ² yields EC. In particular √(U'/m)=1+√(2log C(p−s₀,m)/m+2x'); the x'm in U' is essential and is handled correctly.

### Corollary L5.2

- SCR-A gives containment on E1∩E2⁺ under MC. Any remaining strict superset has the required eigenvalue bound from the definition of φ_n(q). EC then contradicts its stipulated violation. No existence of an LO model equal to S₀ is asserted or needed.
- The event failure sum is exactly 3e^(−x_A)+(1+2q)e^(−x)+e^(−x')/(1−e^(−x')). The SCR-A° alternative adds E4 and replaces 3 by 4, correctly.
- If q<s₀, the superset floor is +∞ and the range 1≤m≤q−s₀ is empty. Interpret the EC requirement as an empty universal quantifier, without evaluating log φ at infinity. Screening rules out all LO models in that size range. If q=s₀, there is also no strict-superset case. These are valid vacuous cases, not missing counterexamples.

### SCR-C

- The cited L3 proofs choose x_A=√log n and yield MC or MC° under the corresponding asymptotic hypotheses. No increase to 2log n is imposed on those screening margins. The separate noise event uses x=2log n; E3b uses x'=ε log n/8. Their distinct roles are correct.
- The total failure bound tends to zero since q≤n/2, ε>0 is fixed, and all three x choices diverge. In the nontrivial superset case φ≤1 and φ≥ϑ_n+ε imply ε<1. The φ=+∞ vacuous subsequence is handled separately as stated.
- (a+b)²≤2a²+2b² gives U≤2k+4log C(p,k)+4x≤2k+4klog(ep/k)+8log n. With p≥2, q log p=o(n) implies q=o(n), hence qlog(ep)=o(n). This proves the uniform o(n). Together with the normalized coefficient hypothesis (finding 2), it proves sup η→0 uniformly, without assuming σ fixed.
- Bounded s₀ makes c₂ uniformly bounded, even if s₀ varies with n. k=s₀+m≤(s₀+1)m and 2p−k≥p give Λ≥2log(p/m)+log n−c₂. The bound log(1−1/n²)≥−1 is valid for n≥2. The positive part is eventually active uniformly because log n−c₂→∞.
- The RHS uses log C(p−s₀,m)/m≤log(ep/m)=ℓ+1. Its normalized bias is bounded by a fixed c₃ for all m≥1; no m-dependent hidden constant is required. Expanding its square yields the printed RHS bound.
- φ(2ℓ+log n)−2ℓ is decreasing in ℓ for φ≤1. Since 0≤ℓ≤log p, its minimum is φ(2log p+log n)−2log p≥ε(2log p+log n). This is the correct inequality direction and precisely explains the stated threshold.
- Set L=2log p+log n. All losses are bounded by o(1)L+O(1)+2ε₁L+O(√L). Since ε₁=ε/8, the remaining coefficient is at least ε/2 eventually. The square-root replacement by √(2L+2) is valid since ε₁≤1. Uniformity holds for m=1, m=2 and growing m. In particular correlated pairs do not refute SCR-C when its floor holds; the example in finding 1 violates that floor.
- Bounded s₀ and ‖θ*‖₂=O(σ√n) are sufficient conditions, not claimed necessary ones. They give bounded c₂,c₃ and vanishing η. Weaker growth conditions could suffice, but are not needed for the delivered claim. For p≤n^A, ϑ_n≤2A/(2A+1) is immediate. The certified-set conclusion follows from the stated certificate implication that every certified model is LO.

### SCR-R

- With containment, y_c=X_Cθ*_C+Cε and centred columns give X_C'Cε=X_C'ε. Extending the refit by zeros outside C yields X(θhat_C−θ*)=P_Cε. The notation C for a model and for the centring matrix is overloaded, but dimensions disambiguate it.
- E3a explicitly contains the ordinary-projector bound as well as the augmented one, so its use here is justified. At x=2log n it supplies U(k,2log n)=(√k+√(2log C(p,k)+4log n))², bounded by the exact constant in STATEMENT. Uniformity over the data-selected certified model is supplied by that event.
- Positive φ implies invertibility. Diagonalizing G_C gives X_CG_C^(−2)X_C'≤P_C/λ_min(G_C), proving the stated coefficient bound with denominator φ(n−1). Its error probability is ≤2q_n n^(−2)→0 plus screening failure. No q log p=o(n) assumption is needed for these possibly nonvanishing refit bounds. Only the event wording needs finding 3's repair.

### SCR-N

- At ∅, a=n−1+λ₀=n²/(n+1), a₁=n and D=n exactly. L1.4 yields the printed score difference, with 0.02+Q_∅=n−0.98 and the quadratic reduction (x_j'y)²/n. Its logarithm has a positive denominator by L1.1.
- Solving the inequality is monotone and gives exactly (★), including the leading (n+1)/n in B_n. The noiseless γ and variance of ζ_j are (n+1)(x_j'μ)²/n² and σ²(n²−1)/n², respectively. The strict variance upper bound by σ² is legitimate; no independence between columns is assumed.
- T1 plus a union bound costs ≤e^(−x) over the s₀ true columns and ≤(p−s₀)e^(−x)/p≤e^(−x) over the other columns. If p=s₀ the second event is vacuous. Adding E2⁻ failure costs ≤2e^(−x), giving 4e^(−x) exactly. E2⁻ in L2 genuinely supplies the noncentral scale lower bound; a central chi-square lower bound alone would not suffice here.
- For t=1−4a_x∈[0,1], E2⁻ gives τhat²≥τ_n²t≥τ_n²t², hence τhat≥τ_nt. This justifies the deliberately conservative squared-scale conversion. At t=0 the signal/noise upper-bound hypotheses cannot hold for σ>0 and x>0, so that endpoint is harmless.
- K≥1, and ∅ has additions only. Thus the p inequalities prove LO with no omitted swaps or deletions. The bound works for p=1, n=3, correlated or duplicate columns. The probability lower bound may of course be negative for small x; that is a valid uninformative bound.
- The B_n upper bound is valid, in fact its prefactor c_n<1 gives B_n≤L_n. Its lower bound is valid after the sign case in finding 4. For log p=o(n), u_n=o(1), and these bounds give B_n/L_n→1.

### Consequence 1

- For every fixed A>0 the construction exists in the centred space for n≥4; arbitrarily many columns may repeat, so p>n creates no feasibility problem. Only x₁ must be orthogonal to them.
- Let H_n=2log p+log n and d_n=(n−1)²(n+1)/n²~n. The exact solution is θ₁²=(1−δ)²σ²H_n/[d_n−(1−δ)²H_n]>0 eventually. Thus θ₁≍√(log n/n), τ_n²=σ²+θ₁²→σ², and Γ_n(0)=(1−δ)²τ_n²H_n exactly.
- With p=ceil(n^A)∨2, H_n~(2A+1)log n, B_n/H_n→1, a_{x_n}→0. The ratio of the null-column noise threshold to τ_n√H_n tends to √(2A/(2A+1))<1; hence (ii) holds with a fixed positive asymptotic gap, even for arbitrarily large fixed A. This uses fixed A, not an unjustified uniformity over A_n→∞.
- The true-column noise threshold is O((log n)^(1/4))=o(√H_n). Its signal ratio is 1−δ, while the available RHS ratio tends to 1. Hence (i) holds. Also 4a_{x_n}≤1 eventually and 4e^(−x_n)→0.
- At q=0 the A∞ denominator has no witness-count term, so the ratio is exactly 1−δ. For any proposed constant c<1 choose δ with c<1−δ<1. This proves the claimed sharpness for all LO models, with precisely the qualification about algorithm output stated in the file. No numerical assertion about N1 is needed for this proof.

### Consequence 2

- The two-column centred design with r=1−1/n exists for n≥3. Its Gram eigenvalues are positive. Δ=2(n−1)b²/n~2(log n)² and τ_n²=σ²+2(log n)²/n→σ². At q=0, Γ is exactly either of the two equal γ values, asymptotic to (log n)²/n→0.
- With x_n=√log n, the signal square root is O(log n/√n), and the noise threshold is O((log n)^(1/4)). Both are o(√log n). B_n~log n because p=2 is fixed; its RHS is asymptotic to σ√log n. Thus (i) holds eventually, (ii) is empty, and the proposition yields P(∅ LO)→1.
- Δ/log(p∨n)~2log n→∞, so it refutes every fixed-C margin-only screening condition exactly as stated. ‖θ*‖₁=2log n. The final rate and extra square claim require findings 5–6's repairs; the explicit sequence and its stated screening counterexample do not.

## Scope of verification and disposition

No blocker was found in L5.1, L5.2 or the delivered SCR-C/SCR-R/SCR-N statements. No fixed-s₀ counterexample to SCR-C under its actual floor was found; its uniform EC contradiction is valid. The false ω-only remark should be removed or replaced before use. All other findings can be repaired locally without changing the target statements. Numerical work was restricted to the independently implemented scratch score check; analytic calculations above are the proof evidence, and do not rely on scr_lib.py or simulation frequency.
