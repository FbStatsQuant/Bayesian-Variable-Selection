# A — Theorem 1-OS: (F_w) replaced by a superset Occam sum; and its deterministic converse (W3-POST2, Claim A)

Status: **PROVED (by this seat, unchecked)**. **Check record [C1B-2]:** line check K-AE (gpt-6.1-sol high, `../reviews/K_AE_check_sol.md`): VERIFIED-WITH-AMENDMENTS, all applied (`K_AE_disposition.md`); independent mid-point M01 (gpt-6-astra): A1, A2 sound; sweep S01: no analytic defect (remark fixes, `S01_disposition.md`); council C1 seats A and B re-derived A0–A2 (PASS).
Notation: `../STATEMENT.md` (v1.2). Labels of [P1], [P3], [T03R] as there. Changed steps of [T03R] §§4–6 are written in
full; unchanged steps are cited by label.

## A0. Interfaces and implications
For J ⊆ [p]∖S₀ put S_J := S₀ ∪ J, d_J := rank(X_{S_J}) − rank(X_{S₀}) and
  a_J := 2^{|J|/2} (eC_A|J| log n / max(d_J, 1))^{d_J/2}  (a_J = 2^{|J|/2} if d_J = 0),
  𝒪_n^{>i} := Σ_{j=i+1}^{min(m♯_n, p−s₀)} [w(s₀+j)/w(s₀)] Σ_{|J|=j} (D_{S₀}/D_{S_J})^{1/2} a_J,
  𝒪⁰_n := Σ_{j=1}^{K−s₀} [w(s₀+j)/w(s₀)] Σ_{|J|=j} (D_{S₀}/D_{S_J})^{1/2}.
(OS; C_OS): 𝒪_n^{>0} ≤ C_OS r_n and (2p)^{s₀}(n+1)^{s₀/2}𝒪_n^{>j₀} ≤ C_OS r_n for n ≥ n_OS.

**Lemma A0.** (i) (F_w; g₀) ⇒ (DG; g₀/(1+g₀)). (ii) (DG; c_D) ⇒ (ADG; c_D). (iii) In R1 (A ≥ 1), (ADG; c_D) ⇒ (OS; C_OS)
with n_OS, C_OS depending only on (s₀, A, c_D). (iv) a_J ≥ 1, so 𝒪⁰-type sums are dominated termwise.

*Proof.* (i) [P1] `lem:spec`(e) with g = g₀ (stated for arbitrary g > 0): D_{S_J}/D_{S₀} ≥ [(n+1)(1+1/g₀)⁻¹]^{|J|}.
(ii) An average of numbers each ≤ [c_D(n+1)]^{−j/2}.
(iii) Put x := eC_A log n (≥ 11e > e for n ≥ 3, as C_A ≥ 11 when A ≥ 1). For 1 ≤ d ≤ j the map d ↦ (xj/d)^{d/2} has
logarithm (d/2)(log(xj) − log d), with derivative ½(log(xj/d) − 1) ≥ ½(log x − 1) > 0; so it is ≤ x^{j/2} at d = j, and
for d = 0 the factor is 1 ≤ x^{j/2}. Hence a_J ≤ (2x)^{j/2} = (2eC_A log n)^{j/2}. By [P3] `lem:prior`(b) (needs
s₀ + j ≤ p) and (ADG),
  Σ_{|J|=j}[w(s₀+j)/w(s₀)](D_{S₀}/D_{S_J})^{1/2}a_J ≤ 2(j+1)^{s₀}2^{−j}(2eC_A log n)^{j/2}[c_D(n+1)]^{−j/2} = 2(j+1)^{s₀}q̃_n^j,
  q̃_n := [eC_A log n / (2c_D(n+1))]^{1/2} ≤ (eC_A/(2c_D))^{1/2} r_n.
For n ≥ n_OS, q̃_n ≤ ½ and, as in [P3] `prop:sup`(b), Σ_{j>i}2(j+1)^{s₀}q̃_n^j ≤ 2K_{s₀,i}q̃_n^{i+1}. With i = 0 this is
≤ 2K_{s₀,0}(eC_A/(2c_D))^{1/2}r_n. With i = j₀: (2p)^{s₀}(n+1)^{s₀/2}·2K_{s₀,j₀}q̃_n^{j₀+1} ≤ C (log n)^{(j₀+1)/2}/n ≤ C r_n
for n ≥ n_OS, by p ≤ n^A and (j₀+1)/2 ≥ s₀(A + ½) + 1 exactly as in [P3] `lem:assemble`. (iv) the base is ≥ 2 > 1 when d ≥ 1. ∎

Remark (compatibility, not a proved example) [K-AE-3]. If the last column u of S_J lies in the span of the others,
u = X_{S}a with a of minimal norm, the Schur factor is [1 + (n+1)aᵀG(I+(n+1)G)⁻¹a]/[1 + aᵀG(I+G)⁻¹a] ≤ 1 + ‖a‖²; so
exact rank loss at |J| = j is not *excluded* by (DG) as long as c_D^j(n+1) ≤ 1 + ‖a‖² (whether (DG) then holds depends on
the other factors; no explicit design is claimed). (ADG) allows a vanishing fraction of dependent J at
every j; (OS) appears to allow, at fixed p, e.g. an exactly duplicated null pair: finite-n evidence only (numerics N2); no
asymptotic proof is given for this example.

## A1. Sufficiency (Theorem 1-OS)

**Statement.** In R1 under G, (E), (F_λ) and (OS) (for all large n, with a common onset in item 6): conclusions 1–6 of
[W3P] Theorem 1, **each with its beta-min qualification unchanged** (items 1–4 under (BM); 5(a), 5(b) without) [K-AE-4]. Conclusion 5(a) holds under
G, (E), (F₀), (OS) in R1.

**Where (F_w) enters [T03R].** Only through Lemma B(B1) ([T03R] lines 139, 143): full column rank of X_{S_J}, the exact
law χ²_J ~ χ²_{|J|}, and the determinant bound. B1 is used in (C2) for (G3), in (C4), in (C5)(b), and in T02(ii♯)
([T03R] §5 items 2, 4). [T03R] §7 Remark 1 and (C6)(a), (C8) confirm that no other step uses (F_w). We replace these.

**(G3′) Ranks and laws.** For J ⊆ [p]∖S₀ with 1 ≤ |J| ≤ m♯_n and s₀ + |J| ≤ p, put χ²_J := σ*⁻²‖(P_{S_J} − P_{S₀})e‖².
Since col X_{c,S₀} ⊆ col X_{c,S_J}, P_{S_J} − P_{S₀} is the orthogonal projection onto their orthogonal difference, of
rank d_J (rank X_{c,T} = rank X_T because X_T = UX_{c,T} and U is an isometry). Under G, e ~ N_N(0, σ*²I), so
χ²_J ~ χ²_{d_J} (χ²_0 ≡ 0), stochastically smaller than χ²_{|J|} ([P3] `lem:chi`(a), last claim). The union bound of
[P3] `lem:Gprob` (G3) therefore holds verbatim: P(some χ²_J > τ_{|J|}) ≤ 1/n. (G1), (G2), (G2*) use no eigenvalue condition.
(G4) — needed below only in (C10)/5(b), via [P3] `lem:signalgain` — is unchanged: its proof uses only
rank(P_{S'} − P_S) ≤ |J(S)| ≤ s₀ ([P3] line 194). With 𝒢^sup_n := (G1)∩(G2*)∩(G3) ((G2*) ⊆ (G2), the per-size form proved at [P3] line 190; STATEMENT v1.1) and 𝒢^sel_n := 𝒢^sup_n ∩ (G4)
(STATEMENT v1.1 [L01-2]): P((𝒢^sup_n)ᶜ) ≤ 4/n and P((𝒢^sel_n)ᶜ) ≤ 5/n for n ≥ n₀, under G, (E) and R1 alone.

**(C4′) One superset, without the determinant bound.** For n ≥ n₀, on 𝒢^sup_n, every J ⊆ [p]∖S₀ with 1 ≤ |J| = j ≤ m♯_n
(s₀ + j ≤ p) and S = S_J:
  m(S)/m(S₀) ≤ (D_{S₀}/D_S)^{1/2} exp{υ_nχ²_J/2 + ρ_n}  (υ_n, ρ_n, ε_n of [P3] `lem:onesup`, unchanged).
*Proof.* [T03R] (C4) with its "Determinant" sentence deleted (the factor (D_{S₀}/D_S)^{1/2} is kept exactly). Numerator:
t_S − t_{S₀} ≥ 0 ([P3] `lem:smoother`(d)); [T03R] (B3) with (S, T) = (S₀, S) needs λ_min(G_{S₀}) ≥ Nφ₀², i.e. (F₀), and no
condition on S; with u = y_c and (P_S − P_{S₀})μ_c = 0 it gives t_S − t_{S₀} ≤ (n/(n+1))[σ*²χ²_J + η_n‖y_c‖²], where now
‖(P_S − P_{S₀})y_c‖² = σ*²χ²_J by definition (whatever the rank). Denominator: [P3] `lem:ongood`(b) (|S| ≤ m♯_n + s₀;
uses (G1), (G2), (E) only). The remaining algebra is verbatim. ∎

**(C5′) Superset sums.** Define
  Υ′_n := Σ_{j=1}^{min(m♯_n, p−s₀)} Σ_{|J|=j} [w(s₀+j)/w(s₀)] (D_{S₀}/D_{S_J})^{1/2} e^{jε_n} e^{χ²_J/2} 1{χ²_J ≤ τ_j},
and Υ′^{>j₁}_n its part with j > j₁. For n ≥ n₀: (a) on 𝒢^sup_n, Σ_{j=j₁+1}^{min(m♯_n, p−s₀)}Ξ_j ≤ e^{ρ_n}Υ′^{>j₁}_n for every integer j₁ ≥ 0 [K-AE-1];
(b) E Υ′^{>j₁}_n ≤ 𝒪_n^{>j₁}; (c) under (OS), Υ′_n = O_P(r_n), (2p)^{s₀}(n+1)^{s₀/2}Υ′^{>j₀}_n = O_P(r_n), and
Σ_{j ≤ m♯_n}Ξ_j1_{𝒢^sup_n} = O_P(r_n).
*Proof.* (a) As [P3] `prop:sup`(a): on 𝒢^sup_n every indicator is 1 by (G3′), and e^{υ_nχ²_J/2} ≤ e^{χ²_J/2}e^{jε_n} for
χ²_J ≤ τ_j; insert into (C4′), multiply by the prior ratio, sum. (Ξ_j = 0 for s₀ + j > p.)
(b) **Lemma M.** For integers 0 ≤ d ≤ j, j ≥ 1, and τ = τ_j (n ≥ 3, A ≥ 1):
  E[e^{χ²_d/2}1{χ²_d ≤ τ}] ≤ (eτ/max(d, 1))^{d/2} (= 1 for d = 0).
*Proof.* d = 0: χ²_0 ≡ 0. d ≥ 1: [P3] `lem:chi`(b). ∎ Hence each term of Υ′ has expectation ≤ weight × e^{jε_n} ×
(eC_A j log n/max(d_J,1))^{d_J/2} ≤ weight × a_J once e^{2ε_n} ≤ 2 (n ≥ n₀, ε_n → 0 by [P3] `lem:onesup`). Sum.
(c) Markov's inequality with (b) and (OS); then (a) with j₁ = 0. ∎

**(C8′) Underfitting mass.** [T03R] (C8) holds with Υ_n replaced by Υ′_n; its rate clause becomes
(2p)^{s₀}(n+1)^{s₀/2}Υ′^{>j₀}_n = O_P(r_n) by (C5′)(c). *Proof:* verbatim; for |J′| ≤ j₀ it uses (C5′)(a) with j₁ = 0,
for |J′| > j₀ it uses (C6)(a) (no eigenvalue condition) and (C5′)(a) with j₁ = j₀. ∎

**Assembly.** (i), **under (BM)**: [T03R] Assembly with (C5′), (C8′) in place of (C5), (C8), on 𝒢^sel_n: the superset term is O_P(r_n) by (C5′)(c);
the underfit term is O_P(n^{−2} + r_n) by (C8′) and (C10) (unchanged: (C10) uses (B2), i.e. (F_λ), and [P3]
`lem:signalgain`, which uses (C6)(b), (C3) and (G4) — none uses (F_w)); Step 0 (C9) is T02(i♯) (uses (F₀), (E)).
Items 2–4 follow from item 1 by [SL] (deterministic). 5(b): [T03R] (iv) with the same replacements. 7 is [LB].
**5(a) under (F₀), (OS) only:** π(S ⊋ S₀) ≤ π(|S| > m♯_n) + Σ_{j≤m♯_n}Ξ_j (eq. (`eq:supsum`)); the first term is
O_P(n^{−1/2}) by T02(i♯), the second O_P(r_n) on 𝒢^sup_n by (C5′)(c), and P((𝒢^sup_n)ᶜ) ≤ 4/n. Neither step uses (F_λ).
**6:** the diagonal transfer of [POST] step (5) applies verbatim once (OS) holds on the events with a common (C_OS, n_OS).

## A2. Converse (deterministic)

**Proposition A2.** For every n ≥ 3, design, data set and S₀ with s₀ ≤ K: δ_n ≥ 𝒪⁰_n/(1 + 𝒪⁰_n).
*Proof.* For S = S_J ∈ Ω (1 ≤ |J| ≤ K − s₀), with the common factors cancelled,
π(S)/π(S₀) = [w(|S|)/w(s₀)](D_{S₀}/D_S)^{1/2}((2b₀ + Q_{S₀})/(2b₀ + Q_S))^ν ≥ [w(|S|)/w(s₀)](D_{S₀}/D_S)^{1/2},
since Q_S ≤ Q_{S₀} ([P1] `lem:spec`(d)). The models S_J are distinct and ≠ S₀, so δ_n ≥ Σ_J π(S_J) ≥ (1 − δ_n)𝒪⁰_n. ∎

Remarks. (1) [LB] is the j = 1 part with D_{S_J}/D_{S₀} ≤ n + 1 ([P3] `lem:det`) and the prior multiplicity bound.
(2) Gap to (OS) [S01-6]: on j ≤ min(K − s₀, m♯_n), 𝒪_n^{>0} dominates 𝒪⁰_n termwise, the ratio per term being the weight
1 ≤ a_J ≤ (2eC_A log n)^{|J|/2} (Lemma A0(iii)) [K-AE-2]; in addition (ii) 𝒪⁰_n contains feasible supersets with j > m♯_n,
which the proof controls by the size tail instead; (iii) 𝒪_n^{>0} contains comparison unions S₀ ∪ J ∉ Ω (K − s₀ < j), with no
counterpart in A2; (iv) the amplified (2p)^{s₀}(n+1)^{s₀/2}𝒪_n^{>j₀} inequality has no counterpart in A2.
(3) Sharpness example (numerics N1, exact case) [S01-7]: a null column x_k = X_{S₀}a ∈ col X_{S₀} with a **bounded
minimal-norm representation** ‖a‖ ≤ C (as in N1, x₃ ∝ x₁ + x₂) gives d_{{k}} = 0 and, by the Schur bound of the Remark
after Lemma A0, D_{S_{{k}}}/D_{S₀} ≤ 1 + C², so 𝒪⁰_n ≥ (s₀+1)(2p − 1 − s₀)⁻¹(1 + C²)^{−1/2} and, by A2, δ_n does not tend
to 0 at fixed p. Span membership alone is not enough: a column in the span with an unbounded representation (e.g. the
normalised difference of two truths with correlation 1 − n⁻²) can have D_{S_{{k}}}/D_{S₀} ≍ n. (For s₀ ≥ 2 the N1 column
also breaks (ID).)
