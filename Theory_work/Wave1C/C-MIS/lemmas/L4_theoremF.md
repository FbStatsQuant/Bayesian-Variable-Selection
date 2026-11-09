# L4 — Theorem F (fixed design, exact sparse projection) and Corollary F

Status (per claim): Theorem F (all changed steps), Corollary F(a), cutoff remark, Lemma T, Corollary F(b) — R03 (xhigh)
VERIFIED / VERIFIED-WITH-AMENDMENTS (applied, reviews/R02_R03_disposition.md); pathwise inequalities corroborated by
numerics/check_L4.py. Sweep R06 fixes applied. Council pending.
References: [P3] = `Docs/Theory/proofs/T03_A2_selection_consistency/PROOF_v2.tex` (labels as there); T03R =
`Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/A-REV5/sources/W1-T03R/PROOF.md` (§6 steps (C1)–(C10)).
We follow T03R §6 step by step; "unchanged" means the cited text holds verbatim after the substitutions
(p, S₀, s₀, θ*) := (p_𝒞, S₀^𝒞, s₀^𝒞, θ^𝒞) and with every subset taken inside 𝒞.

## L4.0 Setting in contrast coordinates

All raw objects deterministic. U (n × N), UᵀU = I_N, UUᵀ = C. Candidate contrast design X_{c,𝒞} := UᵀX_𝒞
(X_𝒞 standardised by candidate SDs); e := Uᵀε ~ N_N(0, σ²I) under G; μ_c := UᵀX^rβ (full mean; ‖μ_c‖ = ‖Cx^rβ‖ =
‖μ_full‖, as in [P3] lem:red(b)); y_c = μ_c + e (the intercept is annihilated: Uᵀ1 = 0). For S ⊆ 𝒞: P_S, M_S, t_S,
Q^c_S, b, D_S, ℓ(S) exactly as in [P3] §2 (they depend only on the candidate columns in S and on y_c).
**(EP)** μ_c = μ^𝒞 + r with μ^𝒞 := X_{c,𝒞}θ^𝒞 = X_{c,S₀^𝒞}θ^𝒞_{S₀^𝒞} and X_{c,𝒞}ᵀr = 0. (Equivalent to STATEMENT
§4: X_𝒞ᵀr_full = 0 for r_full ∈ col(C), and Uᵀ is an isometry from col(C) onto ℝ^N with UᵀX_𝒞 = X_{c,𝒞}.)
Δ_n := ‖r‖²/N, σ²_{𝒞,n} := σ² + Δ_n. Since ‖r‖ ≤ ‖μ_c‖ (r is the residual of an orthogonal projection of μ_c) and
‖μ_c‖² ≤ Mn: Δ_n ≤ Mn/N ≤ 2M, so σ² ≤ σ²_{𝒞,n} ≤ σ² + 2M.

## L4.1 Lemma S (score identity). For every S ⊆ 𝒞:
(a) P_S r = 0 and M_S r = 0;
(b) t_S = ỹᵀM_Sỹ with ỹ := μ^𝒞 + e, and Q^c_S = Q̃_S + c_n, where Q̃_S := ‖ỹ‖² − t_S and c_n := ‖r‖² + 2rᵀe does not
depend on S;
(c) for S ⊆ T ⊆ 𝒞: (P_T − P_S)y_c = (P_T − P_S)ỹ, and t_T − t_S is the same function of ỹ as in the well-specified
problem with data ỹ.
*Proof.* (a) r ⊥ every column of X_{c,𝒞}, so r ⊥ col(X_{c,S}); P_S r = 0, and M_S = h(X_{c,S}X_{c,S}ᵀ) vanishes on
col(X_{c,S})^⊥ ([P3] lem:smoother(a)); for S = ∅ both are 0. (b) y_c = ỹ + r and M_S r = 0, M_S symmetric:
t_S = (ỹ + r)ᵀM_S(ỹ + r) = ỹᵀM_Sỹ. ‖y_c‖² = ‖ỹ‖² + 2rᵀỹ + ‖r‖² and rᵀỹ = rᵀμ^𝒞 + rᵀe = rᵀe (μ^𝒞 ∈ col X_{c,𝒞}).
(c) from (a). ∎
*Reading.* With b_y := b₀‖y_c‖²/N (the actual rate) and b̃ := b₀‖ỹ‖²/N: b_y − b̃ = b₀c_n/N, so
2b_y + Q^c_S = 2b̃ + Q̃_S + (1 + 2b₀/N)c_n exactly. Relative to the shipped posterior recomputed on ỹ, the common
denominator shift is (1 + 2b₀/N)c_n ≈ NΔ_n (a shift of Q alone is correct only with the observed rate b_y held fixed,
which is what the proof does: it keeps b_y throughout and bounds it via the full mean, L4.4(a)). Every T03 step that bounds a difference of t's
is unchanged; steps that bound 2b + Q^c_S from below get the extra −2σ² log n (at worst); steps that bound it from above
get σ²_{𝒞,n} in place of σ².

## L4.2 Good event

𝒢_n^𝒞 := 𝒢_n ∩ (G5), where 𝒢_n = (G1)–(G4) of [P3] §`sec:good` as modified by T03R (C2) (for J ⊆ 𝒞 ∖ S₀^𝒞, sets
T ⊆ 𝒞, underfitting S ⊆ 𝒞; p := p_𝒞), and
  (G5) |rᵀe| ≤ σ‖r‖√(2 log n).
*Probability.* (G1)–(G4) concern e and deterministic candidate projections only; [P3] lem:Gprob with T03R (C2) gives
P(𝒢_n^c) ≤ 5/n for n ≥ n₀ (the union bounds use p_𝒞 ≤ n^A). rᵀe ~ N(0, σ²‖r‖²) (or ≡ 0 if r = 0), and
P(|Z| > √(2 log n)) ≤ 2e^{−log n} = 2/n (Chernoff, Z ~ N(0,1)). So P((𝒢_n^𝒞)^c) ≤ 7/n.
*Consequences of (G5).* With x := ‖r‖ and a := σ√(2 log n): c_n = x² + 2rᵀe ≥ x² − 2ax ≥ −a² = −2σ² log n, and
c_n ≤ x² + 2ax with 2ax = 2σ√(NΔ_n)·√(2 log n) ≤ (σ² + Δ_n)√(2N log n) (because 2σ√Δ_n ≤ σ² + Δ_n), i.e.
c_n ≤ NΔ_n + Nσ²_{𝒞,n}√(2 log n/N).

## L4.3 Deterministic sequences (changed)

δ_n^𝒞 := δ_n + 2 log n/N; δ''^𝒞_n := 5√(log n/N) + (12b₀ + 8)(M + σ²)/(Nσ²); ρ_n, η_n as in [P3]; υ_n^𝒞 and
ε_n^𝒞 := (υ_n^𝒞 − 1)C_A log n/2 as in [P3] lem:onesup with δ_n replaced by δ_n^𝒞. Since δ_n log n → 0
([P3] §`sec:good`, T03R (C1)) and (log n)²/N → 0: δ_n^𝒞 log n → 0, δ''^𝒞_n → 0, ε_n^𝒞 → 0; all are deterministic,
nondecreasing in m♯_n; they depend on p_𝒞 through m♯_n, but admit dominating deterministic sequences (replace m♯_n by
C_m log n) depending only on (s₀^𝒞, A, φ₀, σ², M, g₀) and n (as in [P3] §1); thresholds go into n₀. For a general
cutoff m_n ≤ C log n (L4.9) the dominating sequences and n₀ also depend on C.

## L4.4 Lemma ongood^𝒞 (changes [P3] lem:ongood; T03R (C3)). For n ≥ n₀, on 𝒢_n^𝒞:
(a) ‖y_c‖² ≤ 4n(M + σ²) and 0 < b ≤ 6b₀(M + σ²). — **unchanged** (uses only ‖μ_c‖² ≤ Mn, which R^𝒞 states for the
full mean, and (G1)).
(b) δ_n^𝒞 ≤ ½, and for every S ⊇ S₀^𝒞, S ⊆ 𝒞, |S| ≤ m♯_n + s₀^𝒞: Q^c_S ≥ Nσ²(1 − δ_n^𝒞).
*Proof.* Q^c_S ≥ y_cᵀ(I − P_S)y_c ([P3] lem:smoother(b)) = ‖(I − P_S)y_c‖². (I − P_S)μ^𝒞 = 0 (S ⊇ S₀^𝒞) and
(I − P_S)r = r (L4.1(a)), so (I − P_S)y_c = r + (I − P_S)e and ‖·‖² = ‖r‖² + 2rᵀ(I − P_S)e + ‖(I − P_S)e‖²
= ‖r‖² + 2rᵀe + ‖(I − P_S)e‖² (rᵀP_Se = (P_Sr)ᵀe = 0). By (G5), ‖r‖² + 2rᵀe ≥ −2σ² log n; by (G1)–(G2) as in
[P3], ‖(I − P_S)e‖² ≥ Nσ²(1 − δ_n). Sum: ≥ Nσ²(1 − δ_n^𝒞). ∎
(c) For every underfitting S ⊆ 𝒞 (S ⊉ S₀^𝒞) with |S| ≤ m♯_n and |J′(S)| ≤ j₀, with S′ := S ∪ S₀^𝒞 and
V_S := ‖(P_{S′} − P_S)y_c‖²: 2b + Q^c_S ≤ E_n^𝒞 + V_S, where E_n^𝒞 := 2b + ‖r + e‖² + (2/(n+1))‖y_c‖² satisfies
Nσ²(1 − δ_n^𝒞) ≤ E_n^𝒞 ≤ Nσ²_{𝒞,n}(1 + δ''^𝒞_n).
*Proof.* As in [P3] lem:ongood(c) (with the eigenvalue condition on S supplied by T03R (B2), anchored at S₀^𝒞):
Q^c_S ≤ ‖(I − P_S)y_c‖² + (2/(n+1))‖y_c‖² (uses λ_min(G_S) ≥ Nφ₀² and Nφ₀² ≥ 1; trivial for S = ∅).
‖(I − P_S)y_c‖² = ‖(I − P_{S′})y_c‖² + V_S (nested column spaces). (I − P_{S′})y_c = r + (I − P_{S′})e (S′ ⊇ S₀^𝒞,
L4.1(a)), so ‖(I − P_{S′})y_c‖² = ‖r‖² + 2rᵀe + ‖(I − P_{S′})e‖² ≤ ‖r‖² + 2rᵀe + ‖e‖² = ‖r + e‖². This gives the
first claim. Lower bound: E_n^𝒞 ≥ ‖r + e‖² = ‖r‖² + 2rᵀe + ‖e‖² ≥ −2σ² log n + Nσ²(1 − 3√(log n/N)) ≥
Nσ²(1 − δ_n^𝒞) by (G5), (G1) and δ_n ≥ 3√(log n/N). Upper bound: by (a), (G1), (G5) and L4.2,
E_n^𝒞 ≤ 12b₀(M + σ²) + NΔ_n + Nσ²_{𝒞,n}√(2 log n/N) + Nσ²(1 + 3√(log n/N)) + 8(M + σ²)
≤ Nσ²_{𝒞,n}[1 + (3 + √2)√(log n/N) + (12b₀ + 8)(M + σ²)/(Nσ²)] ≤ Nσ²_{𝒞,n}(1 + δ''^𝒞_n),
using NΔ_n + Nσ² = Nσ²_{𝒞,n} and σ² ≤ σ²_{𝒞,n} in the remaining terms. ∎
(d) If B ≥ Nσ²(1 − δ_n^𝒞) then ν(n/(n+1))η_n‖y_c‖²/B ≤ ρ_n. — **unchanged** ([P3] lem:ongood(d); it uses B ≥ Nσ²/2,
true as δ_n^𝒞 ≤ ½).

## L4.5 Supersets (T03R (C4)–(C5)). **Unchanged up to δ_n → δ_n^𝒞.**
(C4) For J ⊆ 𝒞 ∖ S₀^𝒞, 1 ≤ |J| = j ≤ m♯_n, S = S₀^𝒞 ∪ J, on 𝒢_n^𝒞:
m(S)/m(S₀^𝒞) ≤ (n+1)^{−j/2}(1 + 1/g₀)^{j/2}exp{(υ_n^𝒞/2)χ²_J + ρ_n}, χ²_J := σ^{−2}‖(P_S − P_{S₀^𝒞})e‖² ~ χ²_j.
*Check of each ingredient.* Exact ratio ([P3] eq:score): (D_{S₀^𝒞}/D_S)^{1/2}(1 + (t_S − t_{S₀^𝒞})/(2b + Q^c_S))^ν.
Determinant: (B1) — design only. Numerator: (B3) with (S, T) = (S₀^𝒞, S), u = y_c: t_S − t_{S₀^𝒞} ≤
(n/(n+1))[‖(P_S − P_{S₀^𝒞})y_c‖² + η_n‖P_{S₀^𝒞}y_c‖²], and (P_S − P_{S₀^𝒞})y_c = (P_S − P_{S₀^𝒞})e because
(P_S − P_{S₀^𝒞})μ^𝒞 = 0 and (P_S − P_{S₀^𝒞})r = 0 (L4.1(a)); ‖P_{S₀^𝒞}y_c‖ ≤ ‖y_c‖. Denominator: 2b + Q^c_S ≥
Nσ²(1 − δ_n^𝒞) (L4.4(b)). Then the [P3] algebra with δ_n^𝒞. (C5): verbatim (it uses only (C4), the exact χ²_j laws,
deterministic weights, [P3] lem:chi(b), lem:prior(b)); in particular Υ_n = O_P(r_n) and
(2p_𝒞)^{s₀^𝒞}(n+1)^{s₀^𝒞/2}Υ_n^{>j₀} = O_P((log n)^{(j₀+1)/2}/n).

## L4.6 Underfitting models (T03R (C6)–(C8), (C10))

(C6)(a) [no eigenvalue condition]: ℓ(S)/ℓ(S′) ≤ (2p_𝒞)^{|J(S)|}(n+1)^{|J(S)|/2} — **unchanged** (prior ratio,
lem:det, and Q^c_{S′} ≤ Q^c_S from t monotonicity; L4.1(b) shifts both Q's by the same c_n, and 2b + Q^c_{S′} > 0).
(C6)(b) For underfitting S ⊆ 𝒞 with |S| ≤ m♯_n, |J′(S)| ≤ j₀, on 𝒢_n^𝒞, n ≥ n₀:
  ℓ(S)/ℓ(S′) ≤ (2p_𝒞)^{|J|}(n+1)^{|J|/2}exp{−ν(n/(n+1))V_S/(E_n^𝒞 + V_S) + ρ_n}
            ≤ (2p_𝒞)^{|J|}(n+1)^{|J|/2}exp{−min(V_S/(8σ²_{𝒞,n}), n/5) + ρ_n}.
*Proof.* [P3] lem:SvsSp verbatim for the first line, with: cor:diff lower half for the pair S ⊆ S′ (eigenvalue
condition on S′ from (B2)) and u = y_c, giving t_{S′} − t_S ≥ (n/(n+1))[V_S − η_n‖y_c‖²]; 2b + Q^c_S ≤ E_n^𝒞 + V_S
(L4.4(c)); L4.4(d) with B = E_n^𝒞 ≥ Nσ²(1 − δ_n^𝒞). Second line: V/(E + V) ≥ min(V/(2E), ½); ν ≥ n/2,
E_n^𝒞 ≤ Nσ²_{𝒞,n}(1 + δ''^𝒞_n), δ''^𝒞_n ≤ 1 (n ≥ n₀): ν(n/(n+1))V_S/(2E_n^𝒞) ≥ (n²/(n² − 1))V_S/(4σ²_{𝒞,n}(1 +
δ''^𝒞_n)) ≥ V_S/(8σ²_{𝒞,n}); the n/5 branch as in [P3]. ∎
(C7) **lem:signal^𝒞.** For underfitting S ⊆ 𝒞 with λ_min(G_{S′}) ≥ Nφ₀² (from (B2) when |J′(S)| ≤ j₀):
Δ_S := ‖(I − P_S)μ^𝒞‖² ≥ Nφ₀²‖θ^𝒞_{J(S)}‖², J(S) := S₀^𝒞 ∖ S. — [P3] lem:signal verbatim with μ_c := μ^𝒞 (its proof
uses only μ^𝒞 ∈ col X_{c,S₀^𝒞} with coefficients θ^𝒞).
**lem:signalgain^𝒞.** On 𝒢_n^𝒞, n ≥ n₀, for underfitting S ⊆ 𝒞 with |S| ≤ m♯_n (the domain of (C6)(b), (G4) and
L4.4(c)), if |J′(S)| ≤ j₀ and Δ_S ≥ Lσ²_{𝒞,n} log n with L ≥ 4C_*, then
ℓ(S)/ℓ(S′) ≤ exp{s₀^𝒞(A + 1)log n + ρ_n − min(L log n/32, n/5)}.
*Proof.* (P_{S′} − P_S)y_c = (P_{S′} − P_S)(μ^𝒞 + e) (L4.1(c)) = (I − P_S)μ^𝒞 + (P_{S′} − P_S)e, since
P_{S′}μ^𝒞 = μ^𝒞. So √V_S ≥ √Δ_S − √N_S, N_S := ‖(P_{S′} − P_S)e‖². (G4): N_S ≤ σ²C_* log n ≤ σ²_{𝒞,n}C_* log n ≤
(C_*/L)Δ_S ≤ Δ_S/4, so V_S ≥ Δ_S/4 ≥ (L/4)σ²_{𝒞,n} log n and V_S/(8σ²_{𝒞,n}) ≥ L log n/32. Prefactor as in [P3]
(|J| ≤ s₀^𝒞, p_𝒞 ≤ n^A). Apply (C6)(b). ∎
(C8) lem:assemble — **unchanged** (algebra over (C5)(a) and (C6)(a)/(b)).
(C10) **Step 1 with σ²_{𝒞,n}.** Let 𝒰 := underfitting S ∈ Ω_𝒞 with |S| ≤ m♯_n. For |J′(S)| ≤ j₀, (C7) and BM^𝒞(c),
θ^𝒞²_min ≥ cσ²_{𝒞,n} log n/(nφ₀²), c > c₀ = L_*, give Δ_S ≥ Nφ₀²θ^𝒞²_min ≥ (1 − 1/n)cσ²_{𝒞,n} log n ≥
L_*σ²_{𝒞,n} log n (n ≥ c/(c − L_*)); lem:signalgain^𝒞 with L = L_* gives κ_n(𝒰) ≤ e^{ρ_n}n^{−2} on 𝒢_n^𝒞. Under BM-∞
(θ^𝒞²_min nφ₀²/log n → ∞): as σ²_{𝒞,n} ≤ σ² + 2M, BM^𝒞(L_* + 1) holds eventually. Inclusion version (iv): the same with
𝒰_j, j ∈ J_n^𝒞(c) := {j ∈ S₀^𝒞 : θ^𝒞_j² ≥ cσ²_{𝒞,n} log n/(nφ₀²)}.

## L4.7 Step 0 and assembly

Step 0 (T03R (C9), via T02(i♯)) is **replaced by TAIL^𝒞**: π_𝒞(|S| > m♯_n | y) = O_P(r_n). (T02(i♯)'s proof is not
available here: L5 §2.) Assembly: every S ∈ Ω_𝒞 ∖ {S₀^𝒞} has |S| > m♯_n, or is a superset of S₀^𝒞 with |S| ≤ m♯_n, or
lies in 𝒰. The three masses are O_P(r_n) by TAIL^𝒞, (C5) on 𝒢_n^𝒞, and (C8)+(C10) on 𝒢_n^𝒞; P((𝒢_n^𝒞)^c) ≤ 7/n.
Hence 1 − π_𝒞(S₀^𝒞 | y) = O_P(r_n). (ii)–(iv) of T03R (`PROOF.md:168`) then follow verbatim ((ii), (iii) are
deterministic consequences of (i); (iv) uses (C10)'s inclusion version and TAIL^𝒞). ∎ **(Theorem F)**

**Where σ² vs σ²_{𝒞,n} enter.** Exact χ² laws, (G1)–(G4), (C4)–(C5), lower bounds on denominators: σ² (the true noise).
Upper bound E_n^𝒞, (C6)(b), signalgain, beta-min: σ²_{𝒞,n}. So the *established bounds* for supersets are those of the
well-specified case (up to δ_n → δ_n^𝒞) — an asymptotic comparison of bounds, not a pointwise ordering of posteriors
(for r ≠ 0, c_n < 0 has probability Φ(−‖r‖/(2σ)) > 0 — for r = 0, c_n ≡ 0 — and then extensions gain relative to the posterior on ỹ) — while the sufficient beta-min condition established here uses θ^𝒞²_min ≳ σ²_{𝒞,n} log n/n (dilution, as an interpretation of
the sufficient bound — no lower bound or necessity is proved; c₀ is a proof artefact, T03R `PROOF.md:164`; numerics N3).

## L4.8 Corollary F (bounded candidate set)

If p_𝒞 ≤ P̄ for all n (and n ≥ 2P̄), then m♯_n = K = p_𝒞 eventually, so π_𝒞(|S| > m♯_n | y) = 0 and TAIL^𝒞 holds;
Theorem F holds without TAIL^𝒞.
*Proof.* For n ≥ 2P̄, K = min(p_𝒞, ⌊n/2⌋) = p_𝒞. R_m = Σ_{k=m+1}^{K}C(p_𝒞,k)w(k)/w(s₀^𝒞) depends only on
(p_𝒞, s₀^𝒞, m); for s₀^𝒞 ≤ m ≤ K − 1 it is > 0 (positive terms, m + 1 ≤ K). Over the finitely many triples with
p_𝒞 ≤ P̄ let r_min > 0 be the least such value (if that family is empty, i.e. s₀^𝒞 = K, then m♯_n = K = s₀^𝒞
directly). Once n^{−(s₀^𝒞+2)/2} < r_min no m < K satisfies R_m ≤
n^{−(s₀^𝒞+2)/2}, while R_K = 0; hence m♯_n = K and {|S| > m♯_n} ∩ Ω_𝒞 = ∅. ∎
(With p_𝒞 bounded, SE_w(m♯_n = K; g₀) reads λ_min(X_𝒞ᵀX_𝒞) ≥ g₀, which requires p_𝒞 ≤ N.)

## L4.9 General cutoff, and Lemma T (TAIL^𝒞 under a large omitted residual)

**Cutoff remark.** In L4.0–L4.7, m♯_n may be replaced by any deterministic m_n with s₀^𝒞 ≤ m_n ≤ min(K, C log n)
(fixed C): T03R (C1) uses only these properties of m♯_n (`PROOF.md:172`), and m♯_n enters elsewhere only through Step 0
(C9), which Theorem F replaces by TAIL^𝒞. So Theorem F holds in the form: *if SE_w(m_n; g₀) and
TAIL^𝒞(m_n): π_𝒞(|S| > m_n | y) = O_P(r_n), then 1 − π_𝒞(S₀^𝒞 | y) = O_P(r_n)* (plus (ii)–(iv)). Qualifications
(R03): n₀ and the dominating sequences may depend on C; and this is not an arbitrary-cutoff version of T03R (C9), which
uses the defining prior-tail inequality of m♯_n — its replacement here is the separately assumed (or Lemma-T-proved)
TAIL^𝒞(m_n). SE_λ(j₀) still supplies the bounded-extension eigenvalue bounds, also when m_n < j₀.

**Lemma T.** Assume EP, G, R^𝒞, s := s₀^𝒞 ≥ 1 fixed, p_𝒞 ≤ n^A, d_n := rank X_{c,𝒞}, and, for a fixed κ ∈ (0, 1),
  (TL)  ϑ_n := σ²/(Δ_n + σ²(1 − d_n/N)) ≤ (3/4)(1 − κ)   for all large n.
Put t̄ := (3/8)(1 − κ/2), ρ := ½(1 − 2t̄)^{−1/2} = ½(¼ + 3κ/8)^{−1/2} ∈ (0, 1), and
m^T_n := s + ⌈(s(A + ½) + 1)log n / log(1/ρ)⌉. Then π_𝒞(|S| > m^T_n | y) = O_P((log n)^s/n) = o_P(r_n).
(No eigenvalue condition on any set other than S₀^𝒞 is used.)

*Proof.* Write S₀ := S₀^𝒞, V := col X_{c,𝒞}, W_n := Δ_n + σ²(1 − d_n/N) (so (TL) gives W_n ≥ (4/3)σ²).
*Event.* E_T := (G1) ∩ (G5) ∩ {‖P_Ve‖² ≤ σ²(d_n + 2√(d_n log n) + 2 log n)}; P(E_T^c) ≤ 2/n + 2/n + 1/n
([P3] lem:chi(a) for (G1) and for ‖P_Ve‖²/σ² ~ χ²_{d_n}; L4.2 for (G5)). On E_T, ‖y_c‖² ≤ 4n(M + σ²) (L4.4(a)).
*Denominators, uniformly.* For every S′ with S₀ ⊆ S′ ⊆ 𝒞: 2b + Q^c_{S′} ≥ ‖(I − P_{S′})y_c‖² = ‖r‖² + 2rᵀe +
‖(I − P_{S′})e‖² (proof of L4.4(b)) ≥ ‖r‖² + 2rᵀe + ‖e‖² − ‖P_Ve‖² (P_{S′} ⪯ P_V). On E_T, using
2σ‖r‖√(2 log n) ≤ (σ² + Δ_n)√(2N log n) ≤ (σ² + 2M)√(2N log n) and d_n ≤ N:
  2b + Q^c_{S′} ≥ NW_n − (σ² + 2M)√(2N log n) − 5σ²√(N log n) − 2σ² log n ≥ NW_n(1 − ζ_n),
ζ_n := (3/(4σ²))[((σ² + 2M)√2 + 5σ²)√(log n/N) + 2σ² log n/N] → 0 (deterministic; W_n ≥ 4σ²/3).
*One superset.* For J ⊆ 𝒞 ∖ S₀, |J| = j ≥ 1, S′ = S₀ ∪ J: ℓ(S′)/ℓ(S₀) = [w(s + j)/w(s)](D_{S₀}/D_{S′})^{1/2}(1 + X/B)^ν
with X := t_{S′} − t_{S₀} ≥ 0, B := 2b + Q^c_{S′}. D_{S′}/D_{S₀} ≥ 1 ([P3] lem:det proof: D_T/D_S ≥ ∏_{i≤j}f(λ_i(G_T))
and f ≥ 1). (B3) (eigenvalue condition on S₀ only, from R) with u = y_c and L4.1(c):
X ≤ (n/(n+1))[σ²χ̃²_J + η_n‖y_c‖²], χ̃²_J := σ^{−2}‖(P_{S′} − P_{S₀})e‖² ~ χ²_{r_J}, r_J := rank(P_{S′} − P_{S₀}) ≤ j.
With log(1 + x) ≤ x, νn/((n+1)N) = ½υ⁰_n, υ⁰_n := 1 + (0.02n + 1)/(n² − 1):
  ν log(1 + X/B) ≤ t_nχ̃²_J + ρ̃_n,  t_n := υ⁰_nϑ_n/(2(1 − ζ_n)) ≤ t̄ (n ≥ n₀),
  ρ̃_n := ½υ⁰_nη_n·4n(M + σ²)/(W_n(1 − ζ_n)) ≤ (3/2)υ⁰_nη_nn(M + σ²)/(σ²(1 − ζ_n)) → 0
(t_n ≤ (3/8)(1 − κ)υ⁰_n/(1 − ζ_n) ≤ (3/8)(1 − κ/2) once υ⁰_n/(1 − ζ_n) ≤ (1 − κ/2)/(1 − κ)).
So on E_T: ℓ(S′)/ℓ(S₀) ≤ [w(s + j)/w(s)]e^{t̄χ̃²_J + ρ̃_n}.
*Expectation.* E e^{t̄χ²_r} = (1 − 2t̄)^{−r/2} ≤ (1 − 2t̄)^{−j/2} for r ≤ j (1 − 2t̄ < 1). With [P3] lem:prior(b),
  E Σ_{|J|=j}[w(s + j)/w(s)]e^{t̄χ̃²_J} ≤ 2(j + 1)^s2^{−j}(1 − 2t̄)^{−j/2} = 2(j + 1)^sρ^j.
Let Ψ_n := Σ_{j > m^T_n − s}Σ_{|J|=j}[w(s + j)/w(s)]e^{t̄χ̃²_J} (sum over J ⊆ 𝒞 ∖ S₀ with s + j ≤ p_𝒞). Then
EΨ_n ≤ 2Σ_{j>m^T−s}(j + 1)^sρ^j ≤ 2ρ^{m^T−s}·Σ_{i≥1}(m^T − s + 1 + i)^sρ^i ≤ C_{ρ,s}(m^T_n + 2)^sρ^{m^T_n−s}.
*Tail.* Every S ∈ Ω_𝒞 with |S| > m := m^T_n has S′ := S ∪ S₀ = S₀ ∪ J with j = |S ∖ S₀| ≥ |S| − (s − 1) > m − s
when S ⊉ S₀, and j = |S| − s > m − s when S ⊇ S₀. By eq:ratio, ℓ(S)/ℓ(S₀) = [ℓ(S)/ℓ(S′)]·[ℓ(S′)/ℓ(S₀)] with
ℓ(S)/ℓ(S′) ≤ (2p_𝒞)^s(n + 1)^{s/2} (T03R (C6)(a), no condition; = 1 if S = S′), and each S′ arises from at most 2^s
sets S. Hence on E_T:
  π_𝒞(|S| > m | y) ≤ 2^s(2p_𝒞)^s(n + 1)^{s/2}e^{ρ̃_n}Ψ_n.
E of the right side without the event: ≤ 2^s(2n^A)^s(2n)^{s/2}e^{ρ̃_n}C_{ρ,s}(m + 2)^sρ^{m−s} and
ρ^{m−s} ≤ n^{−(s(A+½)+1)}, so it is O((log n)^s/n). Markov plus P(E_T^c) ≤ 5/n give the claim. ∎

**Corollary F(b).** Under EP, G, R^𝒞, (TL), SE_λ(j₀), SE_w(m_n; g₀) with m_n := min(K, max(m♯_n, m^T_n)), and BM^𝒞:
Theorem F holds without TAIL^𝒞 (cutoff remark + Lemma T; π(|S| > m_n) ≤ π(|S| > m^T_n), and = 0 if m_n = K).
*Reading of (TL).* With d_n/N → 0 (e.g. p_𝒞 = o(n)) and κ small, (TL) asks Δ_n ≳ σ²/3: the omitted residual energy
per observation is at least about a third of the noise variance. The window 0 < Δ_n < σ²(1/3 + d_n/N) with growing p_𝒞
remains open (L5 §2–3).
