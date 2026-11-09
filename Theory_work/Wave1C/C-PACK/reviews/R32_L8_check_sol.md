# R32 — Adversarial mathematical review of L8 / (C1′)

**Verdict: VERIFIED-WITH-AMENDMENTS.**

Reviewed the current L8 in full against STATEMENT.md v2.3, L1, L2, the main proof map, and R10/R11/R12. Also checked L6(a),(c), the actual block rule, and the local T22iii proof's explicit NL_η-to-NL_avg calculation. Paths below are repository-relative; line numbers refer to the files as read for this review. No source files were changed. The script, its output, and this review are the only files written, all under `Theory_work/Wave1C/C-PACK/`.

The exact and thresholded projection certificates are mathematically correct. In particular, the current root-margin inequality gives VIS with **the same M_n**, uniformly over every required subset, and the small-part energy gives exactly the stated uniform NL_η bound. I found no missing factor of φ₀, n−1, σ², or block size. The qualification is that obtaining averaged leakage requires choosing admissible ε₀ and κ; the certificate does not preserve arbitrary previously fixed values of those constants. L2 already acknowledges that choice. One stale downstream W parenthetical and one notation collision remain.

## Numbered findings

1. **MINOR — Spell out the ε₀/κ choice in “hence (H2c)”; the implication is false if ε₀ is held at an arbitrary prescribed value.**

   **Locations:** `Theory_work/Wave1/W1-GEN/lemmas/L8_certificate.md:36`, `:40`; `Theory_work/Wave1/W1-GEN/STATEMENT.md:72`, `:75`. The relevant text is:

   > Then S* := ∪_b supp(γ^L_b) satisfies (H2b) and NL_η(S*), hence (H2c).

   STATEMENT introduces the exponent with:

   > h_n := √(2(A + ε₀) log n), E_{T,l} := min{δ²_{T,l}/(2Δ_T), δ²_{T,l}/(2v_T) + |δ_{T,l}|σh_n/v_T}, with E_{T,l} := 0

   **What is missing:** NL_η bounds its second branch by

   \[
   E_{T,l}\le c_\eta(\varepsilon_0)\log n,
   \qquad c_\eta(\varepsilon_0)=\eta/2+\sqrt{2\eta(A+\varepsilon_0)}.
   \]

   Thus the same leakage family, the maximum over T, and the average with denominator p−s* satisfy the required bound with C_L=η and any

   \[
   0<\kappa\le\tfrac12-c_\eta(\varepsilon_0),
   \]

   **provided the right side is positive**. The displayed threshold on η guarantees that sufficiently small positive ε₀ exist; it does not guarantee this for every fixed ε₀>0 or every positive κ. For η>0 an explicit admissible choice is

   \[
   0<\varepsilon_0<\frac{(1-\eta)^2}{8\eta}-A,
   \qquad
   \kappa=\tfrac12\{\tfrac12-\eta/2-\sqrt{2\eta(A+\varepsilon_0)}\}.
   \]

   For η=0, all E are zero and any ε₀>0 and 0<κ≤1/2 work. No factor 2^B is needed for this deterministic implication: every term is bounded before taking its maximum or average.

   **Counterexample to preserving arbitrary ε₀:** Let p=4, A=1, σ²=M=1, η=0.1, φ₀²=0.49, M_n=log n, and normalized Gram

   \[
   R=\operatorname{diag}\!\left(
     \begin{pmatrix}1&1/2\\1/2&1\end{pmatrix},
     \begin{pmatrix}1&1/2\\1/2&1\end{pmatrix}\right).
   \]

   The actual rule has B=2 and recovers blocks {1,2}, {3,4}. Take μ=a_n x₁+b_n x₃, where

   \[
   a_n=\frac{\sqrt{0.1\log n}+\sqrt{3}\log n}{\sqrt{0.49(n-1)}},
   \qquad b_n=\sqrt{0.1\log n/(n-1)}.
   \]

   Split the first block's coefficients as γ^L=(a_n,0), γ^S=0, and the second block's as γ^L=0, γ^S=(b_n,0). All of L8.2's hypotheses hold eventually, at equality in the large-coefficient threshold and second block's small-energy bound. Energy is O(log² n)≤n; within-block floor is 1/2>0.49; S*={1} is bounded and feasible. Also 0.1<(√3−√2)².

   At the leakage triple (second block, T=∅, l=3), δ²=0.1 log n, Δ_T=a_n²+b_n²→0, and the first branch of E is much larger than log n. If ε₀=1 is kept fixed,

   \[
   \frac{E_{\varnothing,3}}{\log n}\longrightarrow
   0.05+\sqrt{0.4}=0.682455532\ldots>1/2.
   \]

   Consequently the averaged exponential is at least exp(E_{∅,3})/3 and violates NL_avg(κ) for every fixed κ>0 eventually. This is a genuine counterexample to the **arbitrary-fixed-ε₀ reading**, not to the existential choice intended by L8/L2, and not a counterexample to GEN under H0: this construction need not satisfy H0's BM-∞ for the weak truth. The script reproduces the failure and verifies that exactly the same design satisfies averaged leakage with ε₀=0.001.

   **Concrete repair:** append to L8.2 and STATEMENT's NL_η parenthetical:

   > Here (H2c) is supplied with C_L=η and with ε₀>0 chosen sufficiently small that η/2+√(2η(A+ε₀))<1/2; any fixed 0<κ≤1/2−η/2−√(2η(A+ε₀)) is then valid. For η=0, any ε₀>0 and 0<κ≤1/2 are valid. If ε₀ and κ have already been prescribed, require this compatibility inequality.

   **Why MINOR rather than a gap in the intended theorem:** `lemmas/L2_centre.md:62` already says exactly:

   > NL_η → (NL_C, NL_avg(κ)) (NL_η implies both for admissible κ and sufficiently small ε₀, [P:404-425]); EXP′ assumed → proved (L1, needs (H2a) and bounded energy);

   The local cited proof also makes this choice explicit at `Docs/Theory/proofs/T22iii_T16_start_aggregation/PROOF_v2.tex:406-424`. The amendment makes the constant contract visible at the certificate itself.

2. **MINOR — L8's repaired W split is correct, but the linked L6 example still asserts the old, non-disjoint split.**

   **Locations:** `Theory_work/Wave1/W1-GEN/lemmas/L8_certificate.md:60-65`; `Theory_work/Wave1/W1-GEN/lemmas/L6_instances.md:107`. L8 correctly says:

   > * **W.** In a signal group C ∋ j₁, P_Cμ = θx_{j₁} + θP_Cx_{j₂}; take γ^L := γ_{j₁}e_{j₁} (the actual coefficient on the

   But L6 retains:

   >     (T22iii PROOF_v2.tex:404-425). (Also L8.2 with γ^L = θe_{j}.)

   **What is wrong:** For the nine-column equicorrelation block, Σ_CC=(3/4)I+(1/4)11ᵀ and Σ_CC⁻¹1=1/3. Thus the actual active coefficient is θ(1+ε_n/3), and each other coefficient is θε_n/3. Taking γ^L=θe_j leaves a nonzero γ^S_j=θε_n/3 on the same coordinate, contradicting L8.2's disjoint-support hypothesis. This is R10 item 3's issue, fixed in L8 but still present in L6's parenthetical. It does not invalidate L6's separate direct VIS/leakage proof.

   **Concrete repair:** replace only that L6 parenthetical with:

   > (Also L8.2 with γ^L=γ_j e_j=θ(1+ε_n/3)e_j and γ^S equal to the actual coefficients on C∖{j}, as in L8.3.)

   The current L8 small-energy argument is valid. In fact for the exact W block its corrected small part has energy

   \[
   \|X_C\gamma^S\|^2
   =(n-1)\theta^2\frac{22}{9}\varepsilon_n^2,
   \]

   since the eight off-active coordinates have Gram quadratic form (3/4)·8+(1/4)·8²=22. The numerical algebra check gives 2.4444444444×10⁻⁶ per n−1 for θ=1, ε=0.001, in agreement. The 4/3 and 3ε_n bounds actually written in L8 are looser but correct. For W's θ=n⁻¹/⁴ and ε_n=1/(np), this energy tends to zero, while the large-coefficient condition holds with a sufficiently small constant times √n/log n as M_n. Thus both L8.2(i) and (ii), not just (i), are available.

3. **NIT — M denotes both the fixed energy constant and a missing-coordinate set; the thresholded proof also leaves that set implicit.**

   **Locations:** `Theory_work/Wave1/W1-GEN/lemmas/L8_certificate.md:7-8`, `:20`, `:23`, `:29-31`, `:44-45`. Line 20 states:

   > (c) for U ⊆ C_b with U*_b ⊄ U and M := U*_b ∖ U: g_{b,U} ≥ (n − 1)φ₀²‖γ_{b,M}‖² ≥ (n − 1)φ₀² min_{j∈U*_b} γ²_{b,j}.

   Line 23 uses the energy constant again:

   >   (n − 1)φ₀² min_{b} min_{j∈supp γ_b} γ²_{b,j} ≥ M_n (σ² + 2M) log n,  M_n → ∞   (empty minima = +∞).      (BBM)

   **What is wrong:** In the proof paragraph ending at line 31, the reader must silently switch M from a set back to the scalar energy bound. In L8.2 the subscript M in X_Mγ^L_M is used without a local definition. The intended meanings are clear, so there is no mathematical counterexample.

   **Concrete repair:** name the missing set D_{b,U}:=U*_b∖U in both proofs; replace all set-indexed X_M, γ_{b,M}, γ^L_M, G_{U∪M} accordingly. Reserve M throughout for the scalar in ‖μ‖²≤Mn.

## Line-by-line mathematical audit

**L8:1-13 — setting and coefficients.** H2a on the full block implies full column rank and hence unique γ_b. The matrix G here must be the unnormalized Gram XᵀX, consistently with L1:54. The design is the centered, standardized X from STATEMENT, and μ=CX^rβ; no replacement of raw β by standardized θ* is hidden in the coefficient formula. The explicit energy, feasibility, bounded-cardinality and relevance-set qualifications added after R10 are present. The certificate supplies H2b/H2c, not H0/H1 or bounded reference size by itself. No full-design rank assumption is used.

**L8:17-26 — exact minimizers.** For U⊆C_b, P_U P_C=P_U, and P_Cμ decomposes orthogonally into P_Uμ and (I−P_U)P_Cμ. Thus maximizing its projected norm is equivalent to containing P_Cμ in span X_U. Block injectivity makes this equivalent to supp γ_b⊆U. The unique inclusion-minimal minimizer is correct; supersets tie. No uniqueness of a global Λ-minimizer or start mode is asserted or required here.

**L8:19,27-28 — exact leakage.** Every admissible l is in its block outside U*_b, every admissible T contains U*_b, and u_{T,l} lies in span X_C while orthogonal to span X_T. Hence uᵀμ=uᵀP_Cμ=0 for every required T and l, including masked true l. The residual orthogonal to the entire block cannot contribute. This is precisely the family in STATEMENT:69 and L2:29-32. With p>s*, all averaged terms are exp(0)=1, giving NL_avg(κ) for 0<κ≤1/2; with p=s* the average is omitted.

**L8:20,29-31 — exact gain and Gram floor.** Write D=U*_b∖U. Because U∪U*_b contains the entire support, P_{U∪U*_b}μ=P_Cμ. Therefore the gain vector is (I−P_U)X_Dγ_D. For its Schur complement S=X_Dᵀ(I−P_U)X_D and any z,

\[
z^TSz=\min_a\|X_Dz-X_Ua\|^2
\ge (n-1)\phi_0^2\min_a(\|z\|^2+\|a\|^2)
=(n-1)\phi_0^2\|z\|^2.
\]

The argument includes U=∅ by the direct Gram interpretation. Thus the stated coefficient-norm bound and the minimum-coordinate bound follow. There is exactly one normalized eigenvalue factor φ₀² in squared gain; no extra square or reciprocal is needed.

The variance bound is exactly

\[
v_U\le\sigma^2+\|\mu\|^2/(n-1)
\le\sigma^2+Mn/(n-1)\le\sigma^2+2M\quad(n\ge2).
\]

Consequently BBM implies g≥M_n v_U log n with **no reduction of the supplied M_n**. The factor 2 is a safe ceiling, not a sharp asymptotic constant. R10's energy and finite-n denominator objections are fixed.

**L8:35-43 — thresholded decomposition.** Disjoint supports identify a concrete reference U*_b=supp γ^L_b and do not require μ to lie in span X_{S*}. The identity P_Cμ=X_{U*}γ^L+s_b is exact. Every projection onto a block subspace, and every difference of two such projections, annihilates μ−P_Cμ. Full block rank also prevents a nonzero small coefficient vector from representing the zero block vector. Empty large supports give vacuous VIS inequalities; they still require the small-energy bound and leakage checks. The empty-minimum convention is present.

**L8:43-45 — thresholded VIS and absorption.** For every U missing a reference coordinate, Q=P_{U∪U*}−P_U is an orthogonal projection: the spaces are nested, irrespective of correlations. It is a contraction, so ‖Qs_b‖≤‖s_b‖. On the large part, QX_{U*}γ^L=(I−P_U)X_Dγ^L_D. The Schur argument just given applies to this vector alone; it does not require the full mean's support to be U*. Reverse triangle inequality gives

\[
\sqrt{g_{b,U}}\ge\sqrt{(n-1)\phi_0^2}\|\gamma^L_D\|
-\|s_b\|
\ge\sqrt{M_n(\sigma^2+2M)\log n}
\ge\sqrt{M_n v_U\log n}.
\]

The root-margin hypothesis makes the lower bound nonnegative before squaring. This handles cancellation by the small part even when U contains some small coordinates. It is uniform over all U, including U containing block nulls, proxies, or other small coefficients. The current additive slack is sufficient, with the same η, M, φ₀ and M_n; no unstated block-size factor appears.

“Collectively negligible” must mean the energy bound actually written in (i), not just separate bounds on individual coefficients. For example, sixteen orthogonal small coordinates each with energy ησ²log n would have total energy sixteen times the allowance. L8 does not make that weaker, invalid substitution.

**L8:45-46 — thresholded leakage.** For every required T⊇U*_b and l∈C_b∖U*_b, uᵀX_{U*}=0 and ‖u‖=1, so δ=uᵀs_b and δ²≤‖s_b‖²≤ησ²log n. This proves exactly NL_η, not just leakage at T=U*_b. “Outside” here means outside the block's reference support **within the same block**. Neither H2c nor L8 claims this bound for an l outside C_b, or for arbitrary cross-block conditioning sets. The resulting C_L is η. The averaged-leakage constants are as in finding 1.

**L8:50-57 — interpretation and checkability.** The coefficients concern the full mean projected onto the block, so cross-block signal and proxies are included. A coefficient can be omitted only if the chosen small part satisfies its collective energy bound; merely falling short of the large threshold does not certify negligibility. The words are correct under that reading. The population regression formula is the population analogue, not a sample-to-population implication. Random-design use still needs the sample inequalities on design events with common constants/envelopes under C4. No new theorem about sample fluctuations follows from solving the population regressions alone.

**L8:58-59 — LH.** L6(a):32-37 supplies exact block projections: b-group covariances cancel identically, a-group projection is β_i(1−ψ_i²)x_{a_i}, and visible/null projections have the stated form. With the cited fixed parameters and recovered groups, nonzero coefficients have a uniform fixed positive lower bound, giving BBM with a sufficiently small constant times n/log n. Leakage is zero. This uses L6's partition input; it does not establish that input independently.

**L8:60-65 — W.** The active coefficient uses the actual γ_j, so the split is disjoint. The identity for s_b is exact. The projection energy inequality follows from Σ_C≽(3/4)I, and |c|≤‖Σ_C⁻¹‖·‖Σ_{C,j₂}‖≤(4/3)·3ε_n. Thus the triangle inequality used here is valid even though the two pieces in P_Cx_{j₂}−cx_j are generally not orthogonal. Null-group projections involve both truths, changing only a fixed multiplicative constant. The energy order, limit, and existence of an admissible divergent VIS envelope are correct. Finding 2 concerns L6's stale parenthetical only.

**L8:66-77 — finite core and masking example.** Orthogonality of outside columns to the core makes each block Gram block-diagonal across its core/outside portions, so its regression has zero outside coefficients and ζ_n=0. H1a follows from the core floor and orthogonality, since each outside column has standardized variance 1 and φ₀²≤1. Bounded energy follows from fixed θ and fixed core Gram; fixed nonzero truth coefficients give BM-∞. The explicitly imposed outside anchored-eigenvalue conditions supply the remaining H0 conditions. Since the core is fixed, only finitely many core subsets can occur in any actual partition: their finitely many nonzero regression coefficients have a common positive minimum. Thus no stabilization of the block pattern is needed for the claimed uniform BBM; the extra genericity language is unnecessary but harmless. S*_can⊆𝒦 has bounded size and is eventually feasible.

For the concrete r example, Cov(x₂,μ)=r−r=0, Cov(x₁,μ)=1−r², and x₃/outside columns are orthogonal. Split blocks give the stated coefficients; a joint block gives (1,−r). From {1}, adding x₂ removes deterministic residual energy r²(1−r²)(n−1)>0; swapping to {2} loses the nonzero projection on x₁. Null additions have only stochastic gains. Thus the one-move descent description is correct in the theorem's eventual high-probability sense, not a deterministic finite-noise assertion. With p small enough that the actual block rule forces separation, only that case occurs; for larger p a joint block may occur. The conditional descriptions themselves are both correct.

## Falsification experiment and limits

Saved runnable standard-library script:
`Theory_work/Wave1C/C-PACK/numerics/item3_L8_falsify.py`.
Saved console output:
`Theory_work/Wave1C/C-PACK/numerics/item3_L8_falsify_out.txt`.

Command: `python -B Theory_work/Wave1C/C-PACK/numerics/item3_L8_falsify.py`.

The run used **12 distinct random seeds**, 108 designs, and three n values (4096, 16384, 65536); it completed locally in about four seconds without dependencies or network access. There were 3,024 checks of the exact VIS inequalities and 6,480 leakage triples. It enumerated every subset of every block and every required leakage l and T, computed E using both branches and the exact Δ_T and v_T, and took the maximum and average from STATEMENT/L2. Exact-certificate cases also checked the full characterization of block minimizers. It checked the geometric lower bound, coefficient recovery, energy premise and full-Gram floor. There were **zero falsifications of the correctly quantified certificate**.

Random SPD correlation matrices have four size-four blocks and a small correlated cross-block component with random signs. Within-block correlations are uniformly larger in absolute value than cross-block correlations, so complete linkage, size cutting and next-fit recover these actual blocks with p=16 and B=4. Every Gram matrix has a centered standardized realization in dimension n; this is exact design-level computation, not an informal population replacement. A single common μ in the full design span is constructed to have the prescribed regressions on all blocks. Its global energy is checked after construction; block coefficients are not assigned inconsistently to unrelated means.

The cases include η=0 and η=0.1, small-part energies at their allowed boundary, root-margin multipliers exactly 1 and 1+10⁻¹⁰, positive and negative coefficients, an empty reference block, and a block with two large coefficients. The minimum root-margin ratio and maximum small-part energy ratio were both 1 to printed precision; regression recovery error was at most 1.67×10⁻¹⁶. The minimum VIS ratio over the entire random run was 4.076612140, and the maximum NL_η ratio was 0.915302268. These ratios show that touching a sufficient certificate boundary need not make its conservative VIS lower bound sharp. They do not establish optimality or necessity of its constants.

The additional deterministic four-column construction in finding 1 verifies the ε₀ limitation. At n=10⁶, using ε₀=1 gives an averaged-exponential lower bound divided by √n of 4.095872237, already excluding every positive κ at that n; the analytic exponent limit proves eventual failure. With ε₀=0.001, c_η=0.497437146424 and κ=0.001281426788, the same certificate passes the correct averaged bound. Separate Gram algebra checks reproduce finite-core masking and the corrected W coefficients.

No noise was simulated: the certificate's conclusion is deterministic at the design/mean level, so simulation of noise is unnecessary to falsify it. The experiment does not test posterior concentration, recover a random partition from sampled data, or prove GEN's separate H0/H1 and implementation assumptions. Those limits do not weaken its exhaustive checking of the VIS/NL quantities for the constructed designs.

**VERIFIED-WITH-AMENDMENTS — FATAL: 0; MAJOR: 0; MINOR: 2; NIT: 1.**
