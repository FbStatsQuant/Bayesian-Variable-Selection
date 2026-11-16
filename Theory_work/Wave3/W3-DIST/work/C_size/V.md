# V — Lemma V (variational split and moment bound for supersets) — W3-DIST stream C

Status: **DRAFT (by this seat, unchecked)**. Author: stream C (Claude Opus 5.5, Claude Third, high), 2026-11-15.
Target: STATEMENT.md v1.3.1 §3 "Lemma V" and API_CARDS.md "Card V". Source verified line by line: helper H1,
`work/prior_probe/REPORT.md` §3 lines 82–88 and Appendix A2 lines 189–204 (unchecked). Numerical check:
`c_checks.py` → `c_checks_out.txt` (lines "V:" and "V-MC:").

**No STATEMENT-CHANGE REQUEST.** The lemma holds as stated (Card V wording). Two precisions, both consistent with the
statement: (1) ‖D′‖ ≤ cn/(cn + 1) (explicit); (2) STATEMENT §3's form of (c), "eᵀD′e ≤ σ*²χ²_{d_J} + ‖P_{S₀}e‖²", is read as
"eᵀD′e ≤ ‖(P_S − P_{S₀})e‖² + ‖P_{S₀}e‖², where ‖(P_S − P_{S₀})e‖²/σ*² ~ χ²_{d_J} exactly, d_J := rank X_{c,S} − rank X_{c,S₀} ≤ |J|"
(a pathwise inequality with an exactly χ²-distributed first term).

**Verdict on H1 A2.** Correct in substance. Line-by-line notes: (i) A2(a) is right as written ((1 + 1/η)ρ′ from the upper
Young bound for Q_{S₀}, ρ′/η from the lower one for Q_S); both Young inequalities are derived below; (ii) A2(b)'s Weyl step
compares det(I − D′) with det(I − D′^{1/2}Σ₀D′^{1/2}); the needed facts (the eigenvalues of D′^{1/2}Σ₀D′^{1/2} are < 1, and
they dominate those of D′ index by index) are proved below — H1 does not prove the first; (iii) the identity
det Σ^{(c)}_T = D^{(c)}_T and D^{(1)}_T = D_T are proved below (H1 asserts them); (iv) H1's ρ′ is the right quantity, with
the exact representation μ_c = X_{c,S₀}θ* made explicit (it fails for references that are not exact; see Remark V.3).

## Setting (Card V; API_CARDS "Common definitions")
Fixed design. n ≥ 3, N = n − 1, X_c := UᵀX ∈ ℝ^{N×p}; for T ⊆ [p], X_{c,T} its columns in T, G_T = X_{c,T}ᵀX_{c,T} (= X_TᵀX_T),
A_T := G_T + I_{|T|} (positive definite for every design), H_T = (n+1)G_T + I, D_T = det H_T / det A_T, M_T = nX_{c,T}H_T⁻¹X_{c,T}ᵀ,
P_T the orthogonal projection onto col X_{c,T}. Empty set: G_∅, A_∅ void, D_∅ = 1, M_∅ = P_∅ = 0.
**No condition on the design**: G_T may be singular, columns may be duplicated, |T| may be as large as p.
Truth: μ_c = X_{c,S₀}θ* with θ* ∈ ℝ^{S₀} (exact representation; for s₀ = 0, μ_c = 0), y_c = μ_c + e, e ~ N_N(0, σ*²I).
Q^c_T := y_cᵀ(I − M_T)y_c. For a > 0 put
  M^{(a)}_T := X_{c,T}(G_T + aA_T/n)⁻¹X_{c,T}ᵀ,  Q^{(a)}_T(Y) := Yᵀ(I − M^{(a)}_T)Y  (Y ∈ ℝ^N),
  Σ^{(a)}_T := I_N + (n/a)X_{c,T}A_T⁻¹X_{c,T}ᵀ,  D^{(a)}_T := det Σ^{(a)}_T,
with M^{(a)}_∅ = 0, Σ^{(a)}_∅ = I, D^{(a)}_∅ = 1. (G_T + aA_T/n = (1 + a/n)G_T + (a/n)I is positive definite.)
**ρ′ := θ*ᵀA_{S₀}θ*/n = (‖μ_c‖² + ‖θ*‖²)/n = (‖μ‖² + ‖θ*‖²)/n** (ρ′ := 0 if s₀ = 0); under (E; M), (C; M′): ρ′ ≤ M + M′.
(θ*ᵀG_{S₀}θ* = ‖X_{c,S₀}θ*‖² = ‖μ_c‖², and ‖μ_c‖ = ‖Uᵀμ‖ = ‖μ‖ because μ ∈ range C = range U.)

## Statement (Lemma V)
Let S = S₀ ∪ J with J ∩ S₀ = ∅ (J = ∅ allowed), η > 0, c := 1 + η, and D′ := M^{(1/c)}_S − M^{(c)}_{S₀}. Then:
- **(a)** D′ ⪰ 0, ‖D′‖ ≤ cn/(cn + 1) < 1, and, for every e ∈ ℝ^N (pathwise),
  Q^c_{S₀} − Q^c_S ≤ eᵀD′e + (1 + 2/η)ρ′.
- **(b)** For e ~ N_N(0, σ*²I): E[(D_{S₀}/D_S)^{1/2} exp(eᵀD′e/(2σ*²))] ≤ (1 + η)^{s₀ + |J|/2}.
  (Sharper: ≤ (1 + η)^{(r₀ + r_S)/2}, r_T := rank G_T.)
- **(c)** D′ ⪯ (P_S − P_{S₀}) + R₀ with R₀ := P_{S₀} − M^{(c)}_{S₀}, 0 ⪯ R₀ ⪯ P_{S₀}. Hence, pathwise,
  eᵀD′e ≤ ‖(P_S − P_{S₀})e‖² + ‖P_{S₀}e‖² = ‖P_Se‖², where ‖(P_S − P_{S₀})e‖²/σ*² ~ χ²_{d_J}, ‖P_{S₀}e‖²/σ*² ~ χ²_{r₀}, independent,
  d_J := rank X_{c,S} − rank X_{c,S₀} ≤ |J|, r₀ := rank X_{c,S₀} ≤ s₀.

## Proof

**Step 0 (three deterministic facts for a single model T and a > 0).**
(0.i) *Variational form.* Q^{(a)}_T(Y) = min_{φ∈ℝ^T} {‖Y − X_{c,T}φ‖² + a φᵀA_Tφ/n}, the minimum attained.
Proof: J(φ) := ‖Y − X_{c,T}φ‖² + aφᵀA_Tφ/n = YᵀY − 2φᵀX_{c,T}ᵀY + φᵀK φ with K := G_T + aA_T/n ≻ 0. Completing the square,
J(φ) = (φ − K⁻¹X_{c,T}ᵀY)ᵀK(φ − K⁻¹X_{c,T}ᵀY) + YᵀY − YᵀX_{c,T}K⁻¹X_{c,T}ᵀY, whose minimum is YᵀY − YᵀM^{(a)}_TY. For T = ∅ both
sides are ‖Y‖². For a = 1, K = G_T + A_T/n = H_T/n, so M^{(1)}_T = nX_{c,T}H_T⁻¹X_{c,T}ᵀ = M_T and Q^{(1)}_T(y_c) = Q^c_T
(this is [P1] `lem:slab`'s minimum representation, `PROOF_v3.tex:68-81`).
(0.ii) *Spectrum.* With B := X_{c,T}X_{c,T}ᵀ (N × N, ⪰ 0) and K as above: X_{c,T}K = X_{c,T}((1 + a/n)G_T + (a/n)I) =
((1 + a/n)B + (a/n)I)X_{c,T}, hence X_{c,T}K⁻¹ = ((1 + a/n)B + (a/n)I)⁻¹X_{c,T} and
  M^{(a)}_T = h_a(B),  h_a(λ) := λ / ((1 + a/n)λ + a/n)  (λ ≥ 0),
the two factors commuting (functional calculus; the argument of [P1] `lem:spec`(a), `PROOF_v3.tex:101`). h_a is increasing
with h_a(0) = 0 and h_a(λ) < 1/(1 + a/n) = n/(n + a). B vanishes on (col X_{c,T})^⊥ and its nonzero eigenvalues have
eigenvectors spanning col X_{c,T}. Therefore M^{(a)}_T = 0 on (col X_{c,T})^⊥, its eigenvalues on col X_{c,T} lie in (0, n/(n+a)),
and 0 ⪯ M^{(a)}_T ⪯ (n/(n + a))P_T ⪯ P_T. Also P_T = 1{λ > 0}(B), so P_T − M^{(a)}_T = (1{λ>0} − h_a)(B) has eigenvalues in
[0, 1) on col X_{c,T} (namely 1 − h_a(λ) = a(λ + 1)/(nλ + aλ + a) ∈ (0, 1) for λ > 0) and 0 off it: 0 ⪯ P_T − M^{(a)}_T ⪯ P_T.
(0.iii) *Monotonicity.* (α) For 0 < a ≤ a′: Q^{(a)}_T(Y) ≤ Q^{(a′)}_T(Y) for all Y (the objective in (0.i) increases pointwise in
a, since φᵀA_Tφ ≥ 0), i.e. M^{(a)}_T ⪰ M^{(a′)}_T. (β) For T ⊆ T′ and a > 0: Q^{(a)}_{T′}(Y) ≤ Q^{(a)}_T(Y) for all Y, i.e.
M^{(a)}_{T′} ⪰ M^{(a)}_T. Proof of (β): for φ′ ∈ ℝ^{T′} equal to φ ∈ ℝ^T on T and 0 on T′∖T, X_{c,T′}φ′ = X_{c,T}φ and
φ′ᵀA_{T′}φ′ = φᵀA_Tφ (the T × T block of A_{T′} = G_{T′} + I is G_T + I = A_T); so the T′-minimum is over a larger set.
Both (α), (β) hold for every design (no invertibility of G is used; A ≻ 0 always).

**Step 1 (proof of (a): the split).** Young's inequality: for A ≻ 0, vectors u, w and κ > 0,
0 ≤ (√κ w ∓ u/√κ)ᵀA(√κ w ∓ u/√κ) gives −(κ wᵀAw + uᵀAu/κ) ≤ 2uᵀAw ≤ κ wᵀAw + uᵀAu/κ. Hence, for η > 0:
  (Y1) κ = η:          (u + w)ᵀA(u + w) ≤ (1 + 1/η)uᵀAu + (1 + η)wᵀAw;
  (Y2) κ = η/(1 + η):   (u + w)ᵀA(u + w) ≥ (1 − κ)wᵀAw + (1 − 1/κ)uᵀAu = wᵀAw/(1 + η) − uᵀAu/η,
using 1 − κ = 1/(1 + η) and 1 − 1/κ = −1/η.

*Upper bound for Q^c_{S₀}.* Let s₀ ≥ 1. By (0.i) with a = 1, Y = y_c = X_{c,S₀}θ* + e, and the substitution φ = θ* + ψ:
  Q^c_{S₀} = min_ψ {‖e − X_{c,S₀}ψ‖² + (θ* + ψ)ᵀA_{S₀}(θ* + ψ)/n}
        ≤ min_ψ {‖e − X_{c,S₀}ψ‖² + (1 + η)ψᵀA_{S₀}ψ/n} + (1 + 1/η)θ*ᵀA_{S₀}θ*/n      [(Y1), u = θ*, w = ψ]
        = Q^{(c)}_{S₀}(e) + (1 + 1/η)ρ′                                              [(0.i), a = c].
For s₀ = 0: Q^c_∅ = ‖y_c‖² = ‖e‖² = Q^{(c)}_∅(e) and ρ′ = 0, so the same display holds.
*Lower bound for Q^c_S.* Let θ̄ ∈ ℝ^S be θ* on S₀ and 0 on J. Then X_{c,S}θ̄ = μ_c and θ̄ᵀA_Sθ̄ = ‖X_{c,S}θ̄‖² + ‖θ̄‖² = ‖μ_c‖² + ‖θ*‖² = nρ′.
For every φ ∈ ℝ^S write φ = θ̄ + ψ; by (Y2) with u = θ̄, w = ψ:
  ‖y_c − X_{c,S}φ‖² + φᵀA_Sφ/n = ‖e − X_{c,S}ψ‖² + (θ̄ + ψ)ᵀA_S(θ̄ + ψ)/n ≥ ‖e − X_{c,S}ψ‖² + ψᵀA_Sψ/((1 + η)n) − ρ′/η.
Minimising over ψ (equivalently φ) and using (0.i) with a = 1/c: Q^c_S ≥ Q^{(1/c)}_S(e) − ρ′/η. (For S = ∅, i.e. s₀ = 0 and
J = ∅, both sides equal ‖e‖².)
*Subtract:* Q^c_{S₀} − Q^c_S ≤ Q^{(c)}_{S₀}(e) − Q^{(1/c)}_S(e) + (1 + 1/η + 1/η)ρ′ = eᵀ(M^{(1/c)}_S − M^{(c)}_{S₀})e + (1 + 2/η)ρ′. ✓
*D′ ⪰ 0:* by (0.iii)(α) with a = 1/c < c = a′, M^{(1/c)}_S ⪰ M^{(c)}_S; by (0.iii)(β) with S₀ ⊆ S, M^{(c)}_S ⪰ M^{(c)}_{S₀}.
*‖D′‖:* 0 ⪯ D′ ⪯ M^{(1/c)}_S (as M^{(c)}_{S₀} ⪰ 0), and by (0.ii) the eigenvalues of M^{(1/c)}_S are < n/(n + 1/c) = cn/(cn + 1).
So ‖D′‖ = λ_max(D′) ≤ λ_max(M^{(1/c)}_S) < cn/(cn + 1) < 1. ∎(a)

**Step 2 (proof of (b): the moment bound).**
(2.i) *Woodbury.* For every T and a > 0: I − M^{(a)}_T = (Σ^{(a)}_T)⁻¹. Proof: with W := X_{c,T}, Σ^{(a)}_T = I + W((n/a)A_T⁻¹)Wᵀ, and
the Woodbury identity (I + WCWᵀ)⁻¹ = I − W(C⁻¹ + WᵀW)⁻¹Wᵀ, valid for C ≻ 0 (here C = (n/a)A_T⁻¹, C⁻¹ = (a/n)A_T), gives
I − W((a/n)A_T + G_T)⁻¹Wᵀ = I − M^{(a)}_T. (Direct check: (I + WCWᵀ)(I − W(C⁻¹ + WᵀW)⁻¹Wᵀ) = I + W[C − (I + CWᵀW)(C⁻¹ + WᵀW)⁻¹]Wᵀ
= I + W[C − C(C⁻¹ + WᵀW)(C⁻¹ + WᵀW)⁻¹]Wᵀ = I.) In particular Σ^{(a)}_T ⪰ I and 0 ≺ I − M^{(a)}_T ⪯ I.
(2.ii) *Determinant.* By Sylvester's identity det(I_N + WCWᵀ) = det(I_{|T|} + CWᵀW):
D^{(a)}_T = det(I + (n/a)A_T⁻¹G_T) = det(A_T + (n/a)G_T)/det A_T = ∏_i g_a(λ_i), g_a(λ) := (1 + (1 + n/a)λ)/(1 + λ),
λ_i the eigenvalues of G_T (A_T and G_T commute). For a = 1, g_1(λ) = ((n+1)λ + 1)/(λ + 1) = f(λ) of [P1] `lem:spec`(e)
(`PROOF_v3.tex:97,109`), so D^{(1)}_T = D_T. Note g_a(0) = 1: zero eigenvalues (singular G, duplicated columns) contribute 1.
(2.iii) *Gaussian integral.* For z ~ N_N(0, I) and a symmetric B with λ_max(B) < 1: E exp(zᵀBz/2) = det(I − B)^{−1/2}
(diagonalise B = Σ_i β_i u_iu_iᵀ; the zᵢ := u_iᵀz are i.i.d. N(0,1) and E e^{β z²/2} = (1 − β)^{−1/2} for β < 1). With z = e/σ*
and B = D′ (λ_max(D′) < 1 by (a)): E exp(eᵀD′e/(2σ*²)) = det(I − D′)^{−1/2}.
(2.iv) *Comparison.* Put Σ₀ := Σ^{(c)}_{S₀}, Σ_S := Σ^{(1/c)}_S. By (2.i), D′ = (I − M^{(c)}_{S₀}) − (I − M^{(1/c)}_S) = Σ₀⁻¹ − Σ_S⁻¹. Hence
  I − Σ₀^{1/2}D′Σ₀^{1/2} = Σ₀^{1/2}(Σ₀⁻¹ − D′)Σ₀^{1/2} = Σ₀^{1/2}Σ_S⁻¹Σ₀^{1/2} ≻ 0,
so (α) det(I − Σ₀^{1/2}D′Σ₀^{1/2}) = det Σ₀/det Σ_S = D^{(c)}_{S₀}/D^{(1/c)}_S, and (β) every eigenvalue of Σ₀^{1/2}D′Σ₀^{1/2} is < 1.
The matrices Σ₀^{1/2}D′Σ₀^{1/2} = (Σ₀^{1/2}D′^{1/2})(D′^{1/2}Σ₀^{1/2}) and D′^{1/2}Σ₀D′^{1/2} = (D′^{1/2}Σ₀^{1/2})(Σ₀^{1/2}D′^{1/2}) are of
the form FFᵀ and FᵀF (F = Σ₀^{1/2}D′^{1/2}, both N × N), hence have the same eigenvalues (with multiplicity), all ≥ 0 and,
by (β), < 1. Since Σ₀ ⪰ I (2.i), D′^{1/2}Σ₀D′^{1/2} − D′ = D′^{1/2}(Σ₀ − I)D′^{1/2} ⪰ 0, so by Weyl's monotonicity theorem
λ_i(D′) ≤ λ_i(D′^{1/2}Σ₀D′^{1/2}) for every i (eigenvalues in decreasing order). With 0 ≤ λ_i(D′) (by (a)):
  det(I − D′) = ∏_i(1 − λ_i(D′)) ≥ ∏_i(1 − λ_i(D′^{1/2}Σ₀D′^{1/2})) = det(I − Σ₀^{1/2}D′Σ₀^{1/2}) = D^{(c)}_{S₀}/D^{(1/c)}_S > 0.
Therefore E exp(eᵀD′e/(2σ*²)) ≤ (D^{(1/c)}_S / D^{(c)}_{S₀})^{1/2}.
(2.v) *Eigenvalue-wise determinant bounds.* For λ ≥ 0 and c ≥ 1:
  g_{1/c}(λ) ≤ c·g_1(λ)  ⇔  1 + λ + cnλ ≤ c(1 + λ + nλ)  ⇔  1 + λ ≤ c(1 + λ);  true;
  g_1(λ) ≤ c·g_c(λ)     ⇔  1 + λ + nλ ≤ c(1 + λ) + nλ   ⇔  1 + λ ≤ c(1 + λ);  true.
(multiply through by 1 + λ > 0; g_c(λ) = (1 + λ + nλ/c)/(1 + λ)). Since g_a(0) = 1 for every a, zero eigenvalues contribute the
factor 1 to both sides; applying the inequalities only to the nonzero eigenvalues: D^{(1/c)}_S ≤ c^{r_S}D_S and
D_{S₀} ≤ c^{r₀}D^{(c)}_{S₀}, r_T := rank G_T; a fortiori ≤ c^{|S|}D_S and ≤ c^{s₀}D^{(c)}_{S₀}.
(2.vi) *Assembly.* (D_{S₀}/D_S)^{1/2}·E exp(eᵀD′e/(2σ*²)) ≤ (D_{S₀}/D_S)^{1/2}(D^{(1/c)}_S/D^{(c)}_{S₀})^{1/2}
= (D_{S₀}/D^{(c)}_{S₀})^{1/2}(D^{(1/c)}_S/D_S)^{1/2} ≤ c^{(r₀ + r_S)/2} ≤ c^{(s₀ + s₀ + |J|)/2} = (1 + η)^{s₀ + |J|/2}.
D_{S₀}, D_S are deterministic (fixed design), so they come out of the expectation. ∎(b)

**Step 3 (proof of (c)).** By (0.ii), M^{(1/c)}_S ⪯ P_S. Hence D′ = M^{(1/c)}_S − M^{(c)}_{S₀} ⪯ P_S − M^{(c)}_{S₀} = (P_S − P_{S₀}) + R₀,
R₀ := P_{S₀} − M^{(c)}_{S₀}, and 0 ⪯ R₀ ⪯ P_{S₀} by the last sentence of (0.ii) (T = S₀, a = c). Since col X_{c,S₀} ⊆ col X_{c,S},
P_S − P_{S₀} is the orthogonal projection onto col X_{c,S} ⊖ col X_{c,S₀}, of rank d_J = rank X_{c,S} − rank X_{c,S₀} ≤ |J|, and its range
is orthogonal to that of P_{S₀}. Thus eᵀD′e ≤ ‖(P_S − P_{S₀})e‖² + eᵀR₀e ≤ ‖(P_S − P_{S₀})e‖² + ‖P_{S₀}e‖² = ‖P_Se‖².
For e ~ N(0, σ*²I) the projections of e onto two orthogonal subspaces of dimensions d_J and r₀ are independent Gaussian
vectors, so ‖(P_S − P_{S₀})e‖²/σ*² ~ χ²_{d_J} and ‖P_{S₀}e‖²/σ*² ~ χ²_{r₀}, independent. ∎(c)

## Edge cases (Card V route V-c), all covered by the proof
- **Singular G_S / duplicated columns.** Only A_T = G_T + I ≻ 0 and K = G_T + aA_T/n ≻ 0 are inverted; Step 0 and (2.i)–(2.ii)
  hold for every G_T ⪰ 0. Zero eigenvalues give g_a(0) = 1 (no Occam factor and no MGF cost). Duplicating a column of S₀
  into J: d_J does not increase, D_S/D_{S₀} gains only through the new nonzero eigenvalue of G_S.
- **s₀ = 0.** M^{(c)}_∅ = 0, Σ₀ = I, D_∅ = D^{(c)}_∅ = 1, ρ′ = 0, R₀ = 0: (a) reads ‖e‖² − Q^c_S = eᵀM_Se ≤ eᵀM^{(1/c)}_Se (true by
  (0.iii)(α)), (b) reads E[D_S^{−1/2}e^{eᵀM^{(1/c)}_Se/(2σ*²)}] ≤ (1 + η)^{|J|/2}, (c) reads eᵀD′e ≤ ‖P_Se‖².
- **J = ∅.** D′ = M^{(1/c)}_{S₀} − M^{(c)}_{S₀} ⪰ 0, (b) gives ≤ (1 + η)^{s₀}.
- **|S| up to K (or p).** No size restriction is used anywhere. If col X_{c,S} = ℝ^N (possible only for |S| ≥ N, excluded
  by K ≤ n/2 < N for n ≥ 3, but harmless) the bounds still hold.

## Remarks (for the lead's X4; not part of the lemma)
- **V.1 (why the variance surcharge must not enter the MGF).** E exp(γ eᵀD′e/(2σ*²)) = det(I − γD′)^{−1/2} is finite only if
  γλ_max(D′) < 1. λ_max(D′) can be as large as nearly cn/(cn+1) (a new direction with a large Gram eigenvalue λ has
  h_{1/c}(λ) → cn/(cn+1) and is orthogonal to col X_{c,S₀}), so for γ = 1 + ε with ε ≫ 1/n the untruncated moment can be
  +∞. The surcharge (1 + ε_S) of X12.md Fact F6 is therefore paid pathwise, through (c): ε_S·eᵀD′e ≤ ε_S‖P_Se‖², which is
  bounded on the noise event 𝓔_t (X12.md (X1-ii)). This is what X12.md Fact F6 records.
- **V.2 (combination with the posterior ratio).** For S = S₀ ∪ J: π(S)/π(S₀) = [w(|S|)/w(s₀)](D_{S₀}/D_S)^{1/2}((2b + Q^c_{S₀})/(2b + Q^c_S))^ν
  and ((2b + Q₀)/(2b + Q_S))^ν ≤ exp(ν(Q₀ − Q_S)₊/(2b + Q_S)) (log(1 + x) ≤ x). With (a), (Q₀ − Q_S)₊ ≤ eᵀD′e + (1 + 2/η)ρ′ (the right
  side is ≥ 0). Then (b) and the prior identity C(p − s₀, j)w(s₀+j)/w(s₀) ≤ 2C(s₀+j, j)2^{−j} ([P1] `lem:prior`(e),
  `PROOF_v3.tex:119,134-136`) give the design-free superset bound E Σ_{|J|=j}[…] ≤ 2C(s₀+j, j)2^{−j}(1+η)^{s₀+j/2}·e^{(1+2/η)ρ′/(2σ*²)}
  **if the surcharge were 1**; with the surcharge one restricts to 𝓔_t and uses V.1.
- **V.3 (reference).** (a) uses the exact representation μ_c = X_{c,S₀}θ*. For an approximate reference (T, ϑ) with
  residual r = μ − X_Tϑ ≠ 0 the substitution leaves the cross term 2eᵀUᵀr-type and the residual inside both minima; (a)
  then holds with e replaced by e + Uᵀr in the quadratic forms, which is not a centred Gaussian. Not needed for DIST-1
  (strict sparsity); recorded for S-APX.
- **V.4 (numerics).** `c_checks.py` check_V: 300 designs in six families (i.i.d.; duplicated columns in S₀ and J; a
  10⁻³-collinear pair in S₀ with coefficients ±50; a J column within 10⁻⁴ of span S₀; s₀ = 0; |S| = K = n/2), η ∈
  {0.05, 0.3, 1, 3}, 20 noise draws each. Results in `c_checks_out.txt`: all four inequalities hold up to rounding. check_V_mc:
  Monte Carlo of the Gaussian identity (2.iii) in a case with λ_max(D′) < ½ (finite variance).
