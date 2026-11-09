# R03 — L4/L5 cross-family lemma check

Reviewed against STATEMENT.md v1.1 §§4–5. Read L4 and L5 line by line and checked the specified passages of T03R, [P3], [P1], 00_COMMON.md, the shipped score in 02_method.tex:84–135, and numerics SUMMARY.md (especially N3/N3b). All references below use the files and line numbers supplied in the task. No source file was changed; no git command was used.

Theorem F's comparison proof and Lemma T survive this check. There are necessary exposition/citation amendments, and L5 §2's paragraph following Lemma O2 contains an invalid inference and a false all-cutoffs claim. These do not invalidate Theorem F or either tail corollary.

## 1. Lemma S — VERIFIED-WITH-AMENDMENTS

L4:20–29, parts (a)–(c), are exact. The functional-calculus formula in [P3] lem:smoother(a) annihilates r even for singular candidate submodels. Symmetry then gives t_S(y_c) = t_S(ỹ), and orthogonality of r to μ^𝒞 gives Q^c_S(y_c) = Q̃_S(ỹ) + c_n with c_n = ‖r‖² + 2rᵀe. Nested projection differences annihilate r as claimed.

However, the posterior interpretation at L4:30–33 needs an explicit rate correction. Write

    b_y = b₀‖y_c‖²/N,     b̃ = b₀‖ỹ‖²/N.

Then the exact identities are

    b_y − b̃ = b₀c_n/N,
    2b_y + Q^c_S(y_c) = 2b̃ + Q̃_S(ỹ) + (1 + 2b₀/N)c_n.

Consequently, relative to the shipped posterior recomputed on ỹ, the common denominator shift is (1 + 2b₀/N)c_n, not just c_n. A shift of Q alone is correct only if the observed rate b_y is explicitly held fixed in the auxiliary comparison. Replace the reading paragraph with this distinction. The later proof does retain b_y and bound it using the full mean; it does not make the erroneous rate substitution.

Also qualify L4:125–126's interpretation that supersets are penalised “at least as strongly.” It is an asymptotic comparison of the established bounds, not a pointwise ordering of posteriors: c_n can be negative. For r ≠ 0, P(c_n < 0) = Φ(−‖r‖/(2σ)) > 0, and the common denominator shift then increases the Bayes factor of an extension with positive t gain relative to the posterior on ỹ.

The original n-dimensional score exponent ν = 0.01 + n/2 is kept throughout. There is no substitution of an ordinary raw-data likelihood for the shipped target.

## 2. Good event — VERIFIED

L4:35–45 correctly transports [P3] G1–G4 via T03R (C2). G1 and G2 require only Gaussian noise and ranks at most the model sizes. B1 supplies exact rank j for G3; B2 supplies rank |J(S)| for the G4 models. Their laws do not depend on the full mean. No conditioning on b or on the response scale is used.

G5 has exceptional probability at most 2/n, including the degenerate r = 0 case. A union bound, without any independence assumption, gives 7/n. Completing the square yields c_n ≥ −2σ² log n. The upper bound follows from 2σ√Δ_n ≤ σ² + Δ_n and has exactly the stated √2 coefficient. The full-mean energy assumption gives Δ_n ≤ Mn/N ≤ 2M. No missing hypothesis on the direction of r is needed beyond EP.

## 3. ongood^𝒞 and deterministic sequences — VERIFIED-WITH-AMENDMENTS

All four inequalities in L4:54–75 hold.

* (a) is genuinely unchanged: [P3] lem:ongood(a) uses ‖μ_c‖² ≤ Mn and G1, not sparse representability of the full mean. It bounds the actual b_y.
* (b) correctly replaces the pure-noise residual by r + (I − P_S)e. Its squared norm is c_n + ‖e‖² − ‖P_Se‖². This gives exactly δ_n^𝒞 = δ_n + 2 log n/N; no factor of σ²_{𝒞,n}/σ² is missing.
* (c) uses B2 on S, nested orthogonal projections, and r ⟂ col(X_{c,S′}). The residual bound by ‖r + e‖² is valid because the cross term is the same before and after projecting e. The upper bound has coefficient 3 + √2 < 5 and additive constant (12b₀ + 8)(M + σ²). Dividing this constant by Nσ² is conservative, since σ²_{𝒞,n} ≥ σ². Its lower bound follows from G1, G5, and δ_n ≥ 3√(log n/N).
* (d) really uses only B ≥ Nσ²/2 and part (a). Thus the unchanged ρ_n = 8(M + σ²)/(Nφ₀²σ²) still works.

One bookkeeping amendment is required at L4:51–52: the actual sequences still depend on p_𝒞 through m♯_n. Replace “depend on the problem only through (...)” by “admit dominating sequences depending only on (...) and n.” This is the distinction made in [P3]:49. For a general cutoff bounded by C log n, the dominating sequences and n₀ also depend on C.

In particular, δ_n^𝒞 log n → 0, δ''^𝒞_n → 0, and ε_n^𝒞 → 0 are valid. One can simultaneously impose δ_n^𝒞 ≤ 1/2, δ''^𝒞_n ≤ 1, Nφ₀² ≥ 1, and all the original large-n requirements. No random threshold is introduced.

## 4. Supersets (C4)–(C5) — VERIFIED

The exact score ratio in L4:80 is [P3] eq:score with the observed common b_y. B1 supplies the determinant penalty and the exact χ²_j law. B3's upper bound requires the normalised eigenvalue bound only on S₀, supplied by R^𝒞, rather than on its extension. Both μ^𝒞 and r disappear from the projection difference; the denominator uses the corrected ongood^𝒞(b).

For clarity, the complete propagated definitions are

    a_n = (0.02n + 1)/(n² − 1),
    υ_n^𝒞 = (1 + a_n)/(1 − δ_n^𝒞),
    ε_n^𝒞 = (υ_n^𝒞 − 1)C_A log n/2,
    (q_n^𝒞)² = [e C_A log n/(4(n + 1))](1 + 1/g₀)exp(2ε_n^𝒞).

Use ε_n^𝒞 in every weight defining Υ_n and Υ_n^{>j₀}. Then q_n^𝒞 ≤ min(1/2, c_q r_n), c_q = √(e C_A(1 + 1/g₀)), once exp(2ε_n^𝒞) ≤ 4. The proof in T03R (C5), and [P3] prop:sup's truncated χ² moment calculation, are otherwise verbatim. Correlation between the χ²_J variables causes no problem: expectations are summed, not factorised.

The weighted tail bound in L4:86 follows because (j₀ + 1)/2 ≥ s(A + 1/2) + 1. Thus both Υ_n = O_P(r_n) and the stated O_P((log n)^{(j₀+1)/2}/n) remainder are correct. No enlarged beta-min constant is needed here.

## 5. Underfitting (C6)–(C10) — VERIFIED-WITH-AMENDMENTS

(C6)(a) is valid for every S, without an eigenvalue condition. It uses prior ratios, D_{S′}/D_S ≤ (n + 1)^{|J|}, smoother monotonicity, and positivity of 2b_y + Q^c_S. It does not require a pure-noise residual or the candidate density to be the true density.

In (C6)(b), B2 supplies the lower half of cor:diff. The first exponential inequality follows exactly as in [P3] lem:SvsSp, including its sign split when V_S − η_n‖y_c‖² < 0. The denominator can then be enlarged to E_n^𝒞 + V_S without reversing an inequality incorrectly. The ridge error is bounded using E_n^𝒞 ≥ Nσ²(1 − δ_n^𝒞) and ongood^𝒞(d).

For the second inequality,

    ν[n/(n + 1)]V/(2E_n^𝒞)
      ≥ [n²/(n² − 1)]V/[4σ²_{𝒞,n}(1 + δ''^𝒞_n)]
      ≥ V/(8σ²_{𝒞,n}),

and the other branch is at least n/5 for n ≥ 4. These constants are correct.

The changed signal quantity must indeed be Δ_S = ‖(I − P_S)μ^𝒞‖². [P3] lem:signal then applies verbatim with μ^𝒞. In signalgain, P_{S′}μ^𝒞 = μ^𝒞 and (P_{S′} − P_S)r = 0 give the required decomposition. G4 implies N_S ≤ σ²C_* log n ≤ σ²_{𝒞,n}C_* log n. Hence L ≥ 4C_* gives V_S ≥ Δ_S/4 and the constant 32 remains correct.

The beta-min step also checks: for c > L_*, n ≥ c/(c − L_*) gives (1 − 1/n)c ≥ L_*. Together with n/5 ≥ [s(A + 1) + 2]log n this yields κ_n(𝒰) ≤ exp(ρ_n)n^{−2}. Thus

    c₀ = L_* = max{4C_*, 32[s(A + 1) + 2]}

is unchanged. BM-∞ suffices because σ²_{𝒞,n} ≤ σ² + 2M. The inclusion-only argument uses only the coefficient of the omitted strong coordinate and needs no beta-min condition on other coordinates.

Exact amendment: add “|S| ≤ m♯_n” explicitly to the signalgain statement at L4:103, or state that its domain is the models in (C6)(b). G4 and ongood^𝒞(c) were imposed only in that domain. All actual applications already have this restriction.

(C8) is the T03R version, not the older [P3] displayed version with two factors of exp(ρ_n) in its large-J term. The improved crude (C6)(a) gives the single factor in T03R. Counting at most 2^s − 1 underfitting preimages and the q_n^𝒞 expectation bound gives exactly the claimed remainder, which is o_P(r_n).

## 6. Assembly / Theorem F — VERIFIED

Conditional on TAIL^𝒞, L4:116–122 correctly partitions the complement of S₀ into the size tail, small supersets, and small underfitting models. Replacing T03R (C9)'s O_P(n^{−1/2}) by O_P(r_n) suffices; the proof never needs the stronger tail rate. Removing the good-event restriction is legitimate because its exceptional probability tends to zero. It need not be o(r_n) for this O_P conclusion, although the available 7/n bound is stronger anyway.

[P3] (ii) and (iii) are deterministic posterior arguments followed by boundedness of posterior mass to obtain convergence of its expectation. They do not invoke the true density. Paragraph (iv) uses the inclusion version of (C10), the fixed bound |J_n| ≤ s, and the assumed tail. No additional pure-noise or σ² upper-bound use is hidden in assembly.

The following dependencies were specifically checked: [P3] lem:red(a), smoother, cor:diff, det, prior, chi, and Gprob use identities/design/noise facts retained here; red(b)'s full-mean sparse-span assertion is replaced in L4.0–L4.1; ongood(b),(c), onesup's projection cancellation, signal, and signalgain's P_{S′}μ = μ step are explicitly repaired; [P1]'s true-density denominator argument is removed from Theorem F rather than silently reused. Thus I found no omitted misspecification-dependent step in the comparison proof.

This verdict incorporates the local wording/domain amendments listed above; none requires strengthening Theorem F's hypotheses or changing its rates.

## 7. Corollary F(a) — VERIFIED

For bounded p_𝒞 and n ≥ 2P̄, K = p_𝒞. For each nonempty index range s ≤ m < K, R_m is strictly positive and depends on a finite triple (p_𝒞, s, m). Its positive finite-family minimum exceeds n^{−(s+2)/2} eventually, while R_K = 0. Therefore m♯_n = K eventually and TAIL^𝒞 is identically zero.

If the finite family is empty, as in p_𝒞 = s = 1 throughout, simply observe m♯_n = K = s directly rather than taking a minimum of an empty family. This harmless boundary case does not change the corollary. SE_w(K; g₀) then requires a full-column-rank candidate design, as the text discloses. The corollary retains the other hypotheses of F.

## 8. Cutoff remark — VERIFIED-WITH-AMENDMENTS

The mathematical assertion in L4:140–143 is correct: any deterministic s ≤ m_n ≤ min(K, C log n) works if the corresponding SE_w(m_n; g₀) and TAIL^𝒞(m_n) hold. C1 only needs the logarithmic envelope and s ≤ m_n ≤ K. C2–C8 and C10 use no defining inequality for R_{m♯}; they work at the new cutoff, including when m_n < j₀. SE_λ(j₀) still supplies all the bounded-extension eigenvalue bounds needed in their actual ranges.

Two precise qualifications: (1) n₀ and the deterministic dominating sequences may now depend on C; replace any C-independent threshold claim accordingly. (2) This is not an arbitrary-cutoff version of the original T03R (C9). That step uses the defining prior-tail inequality for m♯. Its valid replacement here is the separately assumed TAIL^𝒞(m_n), exactly as the remark states.

## 9. Lemma T — VERIFIED

All substantive steps in L4:145–178 check without SE_w or SE_λ on extensions.

**Event and denominators.** G1 costs at most 2/n, G5 at most 2/n, and the χ²_{d_n} upper-tail event at most 1/n. Thus P(E_T^c) ≤ 5/n. For every extension S′ of S₀, P_{S′} ⪯ P_V gives the same simultaneous lower bound

    2b_y + Q^c_{S′} ≥ NΔ_n + 2rᵀe + ‖e‖² − ‖P_Ve‖².

G1 contributes 3σ²√(N log n), and the projection bound contributes at most 2σ²√(N log n) + 2σ² log n beyond σ²d_n. G5 contributes at most (σ² + 2M)√(2N log n). Their sum is exactly the displayed error. TL gives W_n ≥ 4σ²/[3(1 − κ)] ≥ 4σ²/3; hence the proposed ζ_n is correct, deterministic, and tends to zero. This uniform denominator estimate uses the full span, not a union bound over exponentially many models.

**Determinants and numerator.** D_{S′}/D_{S₀} ≥ 1 is valid even when S′ is singular: the proof of [P3] lem:det gives a product of j factors f(λ) ≥ 1. B3's proof uses only the lower bound on G_{S₀}, supplied by R^𝒞. It does not use full column rank or an eigenvalue bound on S′. Nested projections give r_J ≤ j and χ̃²_J ~ χ²_{r_J}; if r_J = 0, take χ²_0 identically zero.

**Exponent and TL.** The identity νn/((n + 1)N) = υ⁰_n/2 is correct. Thus the coefficient is t_n = υ⁰_nϑ_n/[2(1 − ζ_n)]. The fixed κ margin makes it eventually at most t̄ = (3/8)(1 − κ/2). The proposed ridge remainder is an upper bound and is O(1/n). In particular, no σ² upper bound on the misspecified residual is being used here.

The threshold 3/4 in TL has the right origin: after discarding determinant penalties, the prior contributes 2^{−j} and the MGF contributes (1 − 2t̄)^{−j/2}. Their product contracts precisely when t̄ < 3/8. Therefore

    ρ = (1/2)(1 − 2t̄)^{−1/2} = (1/2)(1/4 + 3κ/8)^{−1/2} < 1.

TL is a sufficient condition for this argument, not asserted to be necessary. Its exact rearrangement is Δ_n/σ² ≥ d_n/N + 4/[3(1 − κ)] − 1. The “about one third” reading requires small κ, as stated.

**MGF, prior, counting, cutoff.** The MGF formula is valid at t̄ < 1/2, and its value for rank r_J is bounded above by the value at j. [P3] lem:prior(b) applies for all s + j ≤ p_𝒞, including auxiliary extensions outside Ω_𝒞; it yields 2(j + 1)^sρ^j after summing over J. No independence across J is needed. Every S mapping to S′ = S ∪ S₀ is obtained by choosing S ∩ S₀, so at most 2^s preimages occur. The crude (C6)(a) applies to all of them without a size/eigenvalue restriction, even if S′ is outside the cap.

The geometric-polynomial tail is bounded by C_{ρ,s}(m^T_n + 2)^sρ^{m^T_n−s}. The chosen ceiling gives ρ^{m^T_n−s} ≤ n^{−s(A+1/2)−1}, exactly cancelling p_𝒞^s(n + 1)^{s/2} up to a constant and leaving O((log n)^s/n). Markov's inequality plus P(E_T^c) → 0 gives the stated O_P rate, and (log n)^s/n = o(r_n) for fixed s. If m^T_n ≥ K the tail is simply zero.

Large-n thresholds here must include κ and the deterministic onset of TL, in addition to the previously fixed constants. No assumption d_n/N → 0 is required by this lemma.

## 10. Corollary F(b) — VERIFIED

m_n = min(K, max(m♯_n, m^T_n)) is deterministic, at least s, and O(log n), since both uncapped cutoffs are O(log n). If m_n < K it is at least m^T_n, so its tail is bounded by Lemma T's tail; if m_n = K the tail is zero. Apply the cutoff version of F with the stipulated SE_w(m_n; g₀), SE_λ(j₀), and projected beta-min. This proves the conclusion without TAIL^𝒞 as an independent assumption.

The statement correctly increases the range of SE_w to m_n; using only SE_w(m♯_n; g₀) would not justify this corollary. Lemma T itself requires no such extension eigenvalue hypothesis.

## 11. Lemma O1 — VERIFIED-WITH-AMENDMENTS

The lemma at L5:8–9 is exact: rank N means V = ℝ^N and V^⊥ = {0}. The distinctions between unrestricted span, capped representability, and exact sparse representability are valid. p_𝒞 ≥ n does not by itself imply rank N. The STATEMENT §5 version is correct.

Amend L5:14–15 to say that GR restores a well-specified conditional Gaussian regression, and that it is sparse only under the separately assumed population-projection sparsity condition. GR/Gaussianity alone does not restore sparsity. For example, with independent standard Gaussian candidate coordinates and an omitted variable equal to their sum plus independent Gaussian noise, its population projection has every candidate coefficient nonzero. STATEMENT already explicitly assumes this sparsity elsewhere; the frontier prose should not suggest it follows from GR.

## 12. Lemma O2 — VERIFIED-WITH-AMENDMENTS; its following consequence is partly GAP and partly FALSE

**The lemma's displayed uniform inequality is valid.** A proper probability mixture of Gaussian densities is bounded by their supremum. For fixed S, optimisation in β gives the OLS residual, and optimisation in v gives (2πv̂_S)^{−N/2}exp(−N/2). Eventually d_n < N, so this residual is positive almost surely, simultaneously over the finite candidate family.

The simultaneous residual lower bound through V is exact. Its error divided by σ² + Δ_n is o_P(1): the dimension term vanishes, the χ² fluctuation is O_P(N^{−1/2}), and √Δ_n/[√N(σ² + Δ_n)] → 0 even if Δ_n is not bounded above. No independence between the cross term and the residual square is required. Thus

    log[m^c_{b′}(S)/f₀] ≤ −(N/2)log(1 + Δ_n/σ²) + o_P(N)

uniformly in S and b′. The positive lower bound on Δ_n converts this into the claimed relative-error form. Uniformity in b′ is pointwise from the common supremum, not an unjustified union bound over rates.

**Required citation correction, L5:33.** The contrast mixture in [P1]:52–56 and 340–342 uses IG(0.51, b′), equivalently IG(a₀ + 1/2, b′), not IG(a₀, b′). This shape change is also explicit in the shipped reduction at 02_method.tex:127–130. The slab is the proper ridge slab N(0, nv(G_S + I)^{−1}). Correcting the mixture identification leaves the supremum proof intact. Using IG(0.01, b′) would define a different evidence with a different exponent.

**GAP in L5:41.** O2 supplies an upper bound on m^c_{b₊}(S₀)/f₀. The mixed-rate posterior inequality needs a lower bound on that quantity. Substituting O2 into its reciprocal cannot yield the displayed upper bound on posterior tail mass. Nor does O2 prove a matching exponential-order lower bound or an O_P(1) multiplicative remainder. Delete “the T02(i♯) bound becomes” and its displayed posterior inequality unless an appropriate lower-bound argument is separately supplied.

**FALSE in L5:42–44.** The assertion that this bound is vacuous “for every m ≤ K” when Δ_n ≥ σ² is false. At m = K the tail and R_K are identically zero. Even excluding this trivial endpoint does not fix the assertion: the finite-population correction to the geometric prior tail cannot be discarded at cutoffs comparable with p.

A nontrivial counterexample to that all-cutoffs assertion is n = 2p, K = p, s = 1, σ² = 1, with all p candidate columns equal to √N u₁, where u₁,u₂ are orthonormal contrast vectors. Take μ^𝒞 = a√N u₁ for fixed a ≠ 0 and r = √N u₂. EP and G hold, d_n = 1 = o(N), Δ_n = 1, and R^𝒞 holds for a fixed sufficiently large M. At m = p − 1,

    R_m = (2p − 1)/binom(2p − 1, p),
    log R_m = −2p log 2 + O(log p) = −n log 2 + O(log n).

For S₀ = {1}, Q^c_{S₀}/N → 2, D_{S₀} = n, and ‖e‖²/N → 1. The fixed-rate integral in [P1], restricted to a shrinking interval about v = 2, gives the matching lower exponential rate; together with O2,

    log[m^c_{b₊}(S₀)/f₀] = −(N/2)log 2 + o_P(N).

The normalised Markov numerator is O_P(1), and the fixed-rate envelope has constant cost. Hence the actual numerator-mean / S₀-denominator strategy gives an upper bound of order

    exp{−(n/2)log 2 + o_P(n)},

which tends to zero at this m < K. This is a counterexample to the frontier remark, not to Theorem F; the duplicate design need not satisfy F's extension eigenvalue hypotheses.

**Exact replacement for L5:41–47.** State only: “O2 rules out the polynomial lower bound with a tight exponent used by den′ in the full experiment. For Δ_n bounded away from zero, a method using only the numerator's mean and a single S₀ denominator incurs an exponential denominator loss. At a nonempty logarithmic cutoff m = O(log n), E1(c) gives log R_m = −o(n), so the prior factor cannot compensate for that loss. This obstructs that particular route to TAIL^𝒞 at logarithmic cutoffs. It does not establish an upper bound on posterior tail mass, nor a sharp necessary cutoff for arbitrary m.”

Finally, change L5:45's “discharged here only for bounded p_𝒞” to include Lemma T / Corollary F(b) under TL. As written it contradicts the addition in L4 and STATEMENT v1.1.

## Additional context checks

N3's failed weak-signal recovery at Δ = 4 uses a beta-min ratio of only 1.2 relative to σ²_{𝒞,n}, so it is not a counterexample to F. N3b rescales that signal by the omitted-energy factor and is consistent with F(a). Its ratio 6 is still below the conservative proved c₀, so it is empirical support for the scale, not a test verifying the theorem's stated sufficient constant or Lemma T for growing p.

L5 §§3–5 contain proposed extensions rather than inputs to F. Their conjectural reduced-experiment and approximate-sparsity assertions are not proved by O1/O2 and should retain their conjecture labels. The sufficient-statistic observation in §3(a) is correct, including the dependence of b_y on the total squared norm. The external SL comparison is not needed for, or certified by, this check of the local lemmas.

**Overall verdict: VERIFIED-WITH-AMENDMENTS for Theorem F, Corollaries F(a)/F(b), Lemma T, and Lemmas S/O1/O2. No substantive gap found in the core consistency proof. L5 §2's asserted posterior upper-bound consequence is a GAP, and its all-cutoffs-vacuity claim is FALSE; replace that paragraph as specified before accepting L4/L5 as a fully verified package.**
