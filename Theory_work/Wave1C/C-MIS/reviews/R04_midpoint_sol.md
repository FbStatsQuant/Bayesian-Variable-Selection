Independent mid-point review of C-MIS

I read STATEMENT.md and all six requested proof files, then checked the relevant T03♯, [P3], [P1], M5(0), and GEN source arguments. I did not read this ticket's LOG.md or existing reviews. Song–Liang §2.3, printed pp. 956–957, was checked directly in the supplied attachment: :codex-file-citation{path="C:/Users/felip/.t3/userdata/attachments/647bfd65-83bc-403a-b3b0-0a8352044e7f-588fe83a-5cbe-4a20-8055-1cfbd7c9c936-pdf.pdf" purpose="source"}

The central strategy is viable. Theorem MIS is a correct transfer result under GR and H-MIS; Theorem F and Lemma T provide substantive additional work. I found two incorrect or insufficiently qualified statements in the Gaussian-design presentation, but no fatal defect in the central posterior arguments.

1. **MAJOR — The singleton precision formula uses a different omitted set in the statement and proof.**

   STATEMENT §1 defines 𝒪 as the omitted columns. STATEMENT §2(iii) then asserts that with “one active omitted variable k,” γ_j = −β_kΘ_jk/Θ_kk, where Θ is the inverse covariance on (x_𝒞, x_𝒪). This is false if 𝒪 also contains inactive omitted variables. L2 avoids the problem by first redefining 𝒪 := S₀ ∖ 𝒞 and using the covariance after marginalizing out the inactive omitted variables. That convention must also appear in the statement.

   Explicit counterexample: let 𝒞 = {1}, 𝒪 = {2,3}, β = (0,1,0), and take centered jointly Gaussian predictors with

   Θ = [[1,0,−1/2], [0,1,−1/2], [−1/2,−1/2,1]].

   This is positive definite, and

   Σ = [[3/2,1/2,1], [1/2,3/2,1], [1,1,2]].

   There is exactly one active omitted variable, k = 2. Nevertheless γ₁ = Σ₁₂/Σ₁₁ = 1/3, whereas −β₂Θ₁₂/Θ₂₂ = 0. The candidate is a proxy even though the corresponding edge in the full precision graph is absent.

   Required repair: either require 𝒪 = {k}, or explicitly use the precision matrix of the marginal vector (x_𝒞,x_k). Marginalizing inactive omitted variables can create edges. The general block identity γ = −Θ_𝒞𝒪Θ_𝒪𝒪⁻¹β_𝒪 remains correct with the original omitted set; Proposition P(d) is correct with L2's convention.

2. **MAJOR — Gaussian conditioning gives the decomposition at each n, but does not automatically give GR's fixed variance across n.**

   L2's setting explicitly permits Σ and m to depend on n. Proposition P(a), and the opening of STATEMENT §2(iii), nevertheless say that Gaussian rows imply GR. GR requires τ² to be fixed. Gaussian conditioning only supplies

   τ_n² = β_𝒪,nᵀΣ_{𝒪·𝒞,n}β_𝒪,n.

   For example, independent standard Gaussian candidates and an independent omitted active column with variance n² give τ_n² = n². This is not an instance of GR as stated. All the finite-n conditioning formulas remain valid.

   GD(b) correctly adds the fixed-σ_𝒞² requirement, and GD(a) has fixed parameters. Thus I do not regard this as a counterexample to their properly qualified conclusions. It is still a hypothesis mismatch in the unrestricted Proposition P(a)/MIS(iii) wording.

   Required repair: distinguish the finite-n Gaussian decomposition from its asymptotic use. State explicitly that MIS applies only when τ_n² is the fixed τ² required by GR, unless a separate theorem for varying variances is proved. Do not silently inherit fixed variance merely from Gaussianity.

3. **MINOR — MIS is meaningful, but its contribution and its screening clause need precise positioning.**

   Lemma R is exact: conditional on the candidate design, the response has the same law as a well-specified candidate regression with variance σ² + τ². The response standardization, candidate-dependent prior, cap, and algorithmic outputs therefore transfer because the method is rerun on the candidate data. No posterior equality with a conditioned full-model posterior is needed.

   Lemma DR's diagonal argument is correct. It upgrades tightness along every deterministic design sequence in the envelopes to uniform tightness, and then to joint-law O_P(r_n). It does not require a uniform expectation rate. The design-measurability and deterministic beta-min envelopes in L1.4 are the right safeguards. GD(a) and GD(b) adequately discharge the advertised design conditions in their respective regimes, subject to finding 2.

   This is a useful answer for omitted Gaussian covariates, although the reduction itself is elementary and provides no new robustness theorem for a conditionally misspecified candidate likelihood. The strongest new technical contribution is F/T. Present MIS as a transfer theorem and F/T as the extension requiring new proof.

   The comparison with Song–Liang is substantially accurate: their Corollary 2 is screening, whereas this ticket proves exact-model concentration under stronger assumptions. However, “without beta-min” here screens only J_n^𝒞(c), not every nonzero projected coefficient in an arbitrary triangular array. For fixed dimension, fixed covariance and fixed nonzero projected coefficients, GD(a) makes J_n^𝒞(c) = S₀^𝒞 eventually and recovers their full inclusion conclusion. Add that sentence to prevent a stronger reading of the general clause.

4. **MINOR — Theorem F's changed steps check out; retain their domains and correct the degenerate-residual aside.**

   I checked L4 against T03R (C1)–(C10) and the underlying [P3] lemmas. The essential changes are all present:

   - EP gives P_Sr = M_Sr = 0, unchanged score increments, and the common shift c_n = ‖r‖² + 2rᵀe.
   - The response-dependent rate is retained: b_y − b̃ = b₀c_n/N, so the complete denominator shift is (1 + 2b₀/N)c_n.
   - G5 gives c_n ≥ −2σ² log n. Consequently δ_n becomes δ_n^𝒞, including in υ_n, ε_n, q_n and the superset assembly.
   - The upper bound E_n^𝒞 uses ‖r + e‖² and σ²_{𝒞,n}, while exact chi-square laws and denominator lower bounds still use σ².
   - The signal calculation uses μ^𝒞; the residual cancels from (P_{S′} − P_S)y_c.
   - The sharp underfitting comparison is restricted to |S| ≤ m_n and |J′(S)| ≤ j₀. The large-|J′| part uses the crude comparison, which needs no additional eigenvalue hypothesis.
   - Step 0 is replaced by TAIL^𝒞.

   These changes suffice. The general deterministic cutoff m_n = O(log n) is legitimate; its constant must enter the dominating sequences and onsets, as L4.9 states. The bounds give O_P(r_n), and boundedness gives convergence of the expectation, without an expectation rate.

   One small false aside remains: L4.7's formula P(c_n < 0) = Φ(−‖r‖/(2σ)) holds for r ≠ 0. If r = 0, then c_n = 0 identically and that probability is zero, not 1/2. Qualify the aside.

5. **MINOR — Corollaries F(a), F(b) and Lemma T are sound, with important qualifications worth keeping visible.**

   F(a)'s finite-family argument correctly gives m♯_n = K eventually when p_𝒞 is bounded. It removes TAIL, not SE_w: full candidate rank and the asserted unnormalized eigenvalue floor still have to hold.

   Lemma T's denominator lower bound is uniform over all comparison supersets because P_{S′} ⪯ P_V and r ⟂ V. The resulting coefficient t_n is eventually below t̄ < 3/8 under the strict TL margin. The determinant ratio is at least one even for rank-deficient auxiliary supersets. Their projected noise has χ²_{r_J} law with r_J ≤ j, which is enough for the exponential moment.

   The geometric sum is correctly controlled by

   ρ = (1/2)(1 − 2t̄)^(−1/2) < 1.

   The factor 2^s(2p_𝒞)^s(n+1)^(s/2) accounts for underfitting comparisons and their multiplicity; the prescribed m_n^T cancels its polynomial growth and leaves O((log n)^s/n). No independence among different projected chi-square variables is needed. Auxiliary S′ outside the cap are legitimate score-comparison devices, as [P3] explicitly permits.

   F(b) follows: when m_n < K, it is at least m_n^T; when m_n = K, the tail is zero. Its SE_w assumption must be evaluated at the enlarged cutoff m_n, not merely the old m♯_n.

   No extra tail proof is needed before final council for these stated regimes. TL is sufficient, not necessary. Keep the window below its threshold explicitly unresolved.

6. **MINOR — Both HPM transfers are correct, conditional on exactly the named operational and GEN premises.**

   Corollary H is a pathwise posterior-to-decision argument followed by Markov's inequality. Replacing S₀ by a candidate-design-measurable T causes no problem: π_𝒞(T) > 1/2 makes T the unique global score maximizer, and the coupling transfers scored-set inclusion on the output event. This works under F as well as MIS.

   Corollary D transfers the whole run under GR, including the actual candidate-only partition. Replacing σ² by σ_𝒞² everywhere in GEN is essential; adding τ² again to GEN's Δ_T would be wrong. L3 uses μ^𝒞 and makes the correct substitution. Its BM-∞ requirement is stronger than MIS's optional BM(c), and is properly disclosed. The random-design version requires GEN's complete envelopes, not just MIS's envelopes.

   D′'s W-family construction also survives the variance change: BM and VIS retain diverging margins, and its leakage bounds vanish for fixed σ_𝒞². The result is about the intersection with output availability. Neither H nor D establishes P(U_n) → 0, and neither establishes a reported-HPM theorem under EP alone. Preserve these distinctions in the eventual report.

7. **MINOR — Add an explicit analytic target-separation example and qualify the sample-projection support.**

   The population projection support is the right random-design target. The fixed-design target is the support of the sparse representation of P_𝒞μ_c, with the stated identifiability assumptions; KL minimization alone does not identify a named support in a redundant design. The statement handles that distinction appropriately.

   The following fully Gaussian fixed-dimension example makes the practical consequence unusually clear. Let x₁,x₂,x₃,z be independent standard normals, candidates 𝒞 = {1,2,3}, omitted x_k = −x₁ + x₂ + z, and

   y = x₁ + x_k + ε = x₂ + z + ε.

   Then the full-model truth is {1,k}, the retained truth is {1}, but β^𝒞 = (0,1,0) and the candidate target is {2}. GD(a) gives π_𝒞({2}|y) → 1: candidate 2 is selected as a proxy and candidate 1 is cancelled. Furthermore, conditional on a full-rank candidate sample, the least-squares projection of the realized full mean x₂ + z has nonzero coefficients on all three candidates almost surely. Thus its sample-projection support is {1,2,3}, and its posterior mass also tends to zero.

   This supplies an analytic example for both misleading alternatives, without relying on numerics. Add it or an equivalent proposition before council.

   L1's Corollary N should also restrict its reference to “the support of the sample projection” to a setting where the coefficient vector is uniquely defined, such as full candidate column rank. With p_𝒞 > N, the projected vector is unique but its coefficient support need not be. A named coefficient-selection convention would be needed for a general version.

8. **MINOR — The boundary beyond GR needs a failure example; Gaussian marginals alone are insufficient.**

   Here is a direct counterexample to weakening GR to centered Gaussian marginals with equal variances. For even n ≥ 4, take deterministic centered orthogonal raw candidate columns x₁,x₂ with ‖x_j‖² = n and balanced entries x₂i = ±1. Let Z ~ N(0,1) be independent of ε ~ N_n(0,I), define the omitted raw column x_k = Zx₂, and take

   y = x₁ + x_k + ε.

   The omitted contribution has conditional mean zero and identical Gaussian marginal variances 1, but covariance x₂x₂ᵀ rather than I. The conditional expected candidate mean is x₁, so a mean-only projection prescription would target {1}. Conditional on each fixed Z = z ≠ 0, however, the raw candidate regression has coefficients (1,z). Standardizing the columns only rescales these by √(n/N). Its exact posterior concentrates on {1,2} by T03♯. Integrating the conditional convergence gives π_𝒞({1}|y) → 0 in probability.

   Thus a common random omitted slope defeats the proposed transfer despite Gaussian marginals, zero conditional mean and homoscedastic marginal variances. The covariance/independence content of GR matters. This example is not an iid-row counterexample to Song–Liang, and should not be presented as one.

   Likewise, simply dropping EP for a proposed fixed sparse target leaves noncentral signal in extension directions: taking μ_c = bx₁ + cx₂ + r with orthogonal candidates, c ≠ 0 and r ⟂ span X_𝒞 makes {1} the wrong target; F(a) instead selects {1,2}. Neither example proves GR or EP is necessary for every possible consistency theorem. They demonstrate why the present transfer/proof cannot be generalized merely by deleting those hypotheses.

9. **MINOR — Address the null projection and clean up the frontier before council.**

   The explicit exclusion s₀^𝒞 = 0 prevents an overclaim, but removes a central misspecification case: every signal is omitted and independent of the candidates, or all retained projected signals cancel. A referee will notice. A bounded-candidate null-support lemma would be useful; the underlying [P3] proof already treats empty-support conventions, but the adopted T03♯ card does not authorize silently importing that extension. Either prove it separately or emphasize the omission in the final result's synopsis.

   Lemma O2 is a valid obstruction to the particular full-experiment denominator strategy. Its mixture bound is uniform over S and the positive rate, and its exponential loss is not a posterior inconsistency result. The statement's phrase that candidate densities “cannot fit the residual's variance” is misleading: the candidate model can inflate its scalar variance to σ² + Δ_n; it cannot represent the orthogonal mean r. Describe the resulting likelihood/KL loss that way.

   L5 §3(b)'s “not proved” large-residual route has been substantially superseded by Lemma T, which proves a stronger direct-tail route without eigenvalue assumptions beyond the truth set. Mark it as superseded or remove it. Also register Lemma T and F(b) in 00_MAIN's proof map; they are absent from its current rows.

Before final council, fix findings 1–2, make the small statement/frontier corrections, and add the explicit analytic boundary examples. Keep a concise hypothesis-to-step table covering true σ² versus effective σ², candidate-only rerunning, auxiliary models beyond the cap, the enlarged F(b) cutoff, and GEN's operational premises. A separate null-support lemma is desirable but not a condition for accepting the expressly nonempty-support theorem. I see no reason to replace the F/T strategy or spend another cycle on exploratory numerics.

VERDICT: CONTINUE — The core reduction, fixed-design proof, tail lemma and HPM transfers withstand this review. Correct the two Gaussian-design statement mismatches and strengthen the scope/boundary presentation before final council; no fatal obstruction or strategic redirection is indicated.

