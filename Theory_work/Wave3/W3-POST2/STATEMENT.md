# W3-POST2 — STATEMENT (v1.2.1, 2026-11-09; v1.2.1 = post-council C1 wording/bookkeeping; v1.2 = sharpness-gate adoptions from R03b [C+, D+, E ridge margin]; lead: Claude Opus 5.5, claudeAgent, high; v1.1 = statement-lock amendments [L01-#] + lead corrections [LC-#])

Ticket W3-POST2 (HQ decision 2026-11-09, `Theory_work/Wave3/HQ_DECISIONS.md`). Brief numbering [C1B-3]: "brief item k"
below is the order of the delegation brief; in W3-POST REPORT §4 numbering (used by `Theory_work/Wave3/HQ_DECISIONS.md:8`):
A = §4.1, B = §4.3, C = §4.4, D = PROGRAM 1b / §4.11, E = §4.2 (stretch). Improvements to W3-POST's posterior theorem.
Input: `Theory_work/Wave3/W3-POST/` (STATEMENT v1.4, council-passed C3). Five claims A–E, one per brief item, each with its
own checks. Statuses are verbatim. Each new result carries the status of its proof file (`lemmas/A_occam.md`,
`B_tail_approx.md`, `C_expectation.md`, `D_hellinger.md`, `E_visibility.md`): **PROVED (by this seat, unchecked)** until
the check record in that file says otherwise [L01-1]. Inherited statuses (W3-POST and earlier) are unchanged.

**Aliases.** As W3-POST STATEMENT: [P1] (locked T01/T02, `PROOF_v3.tex`), [P3] (locked T03, `PROOF_v2.tex`), [T03R]
(`ARC/W1-T03R/PROOF.md`), [SL], [POST]; **[W3P]** = `Theory_work/Wave3/W3-POST/STATEMENT.md` (v1.4), **[L1a′]** =
`W3-POST/lemmas/L1a_size_tail.md`, **[LB]** = `W3-POST/lemmas/LB_rate_lower_bound.md`.

**Notation.** The coded target π, data conventions, X (standardised retained columns), y, Ω, K = min(p, ⌊n/2⌋), G_S, H_S,
D_S, Q_S, ν, w(k), q_k, R_m, m♯_n, r_n = √(log n/n), δ_n = 1 − π(S₀), PIP, HPM, MPM: exactly [W3P] §0. Contrast coordinates
of [P1]/[P3]: N = n − 1, U, y_c = Uᵀy^r, X_c = UᵀX, e = Uᵀε, μ_c = Uᵀμ, P_S (projection onto col X_{c,S}), M_S, Q^c_S,
b = b₀s_y². Events [L01-2]: 𝒢^sup_n := (G1) ∩ (G2*) ∩ (G3) of [P3] §`sec:good` (with (G3) for all J, any rank; (G2*) := ‖P_Te‖² ≤ σ*²C_A|T| log n
for every T with 1 ≤ |T| ≤ m♯_n + s₀ — the per-size bound that [P3] line 190 actually proves, which implies (G2) [K-D-1];
P((𝒢^sup_n)ᶜ) ≤ 4/n for n ≥ n₀); 𝒢^sel_n := 𝒢^sup_n ∩ (G4) (P((𝒢^sel_n)ᶜ) ≤ 5/n; (G4)'s proof uses only
rank(P_{S∪S₀} − P_S) ≤ s₀, [P3] line 194); 𝒢⁵_n := the cross-term event of `lemmas/E_visibility.md` (P((𝒢⁵_n)ᶜ) ≤ 1/n) [M01-2]. j₀ := ⌈(2A + 1)s₀⌉ + 1,
C_A := 8 + 3A, τ_j := C_A j log n. For J ⊆ [p]∖S₀: d_J := rank(X_{S₀∪J}) − rank(X_{S₀}) ∈ {0, …, |J|} (the rank gain).
For S ⊆ [p]: Δ_S := ‖(I − P^{(n)}_S)μ‖² with P^{(n)}_S the projection in ℝⁿ onto col X_S (= ‖(I − P_S)μ_c‖²).
Regime R1 and (E), (F_λ), (F_w), (BM) as in [W3P] §2. Additionally:
- **(F₀)** λ_min(X_{S₀}ᵀX_{S₀}/(n − 1)) ≥ φ₀² (the S₀ part of R; implied by (F_λ)).

## New interfaces on (X, θ*) (all design-agnostic; families appear only as examples)

**Superset Occam sums.** For i ≥ 0 and n with s₀ ≤ K:
  𝒪⁰_n := Σ_{j=1}^{K−s₀} [w(s₀+j)/w(s₀)] Σ_{J⊆[p]∖S₀, |J|=j} (D_{S₀}/D_{S₀∪J})^{1/2}             (no weights),
  𝒪_n^{>i} := Σ_{j=i+1}^{min(m♯_n, p−s₀)} [w(s₀+j)/w(s₀)] Σ_{|J|=j} (D_{S₀}/D_{S₀∪J})^{1/2} a_J,
  a_J := 2^{|J|/2}(eC_A|J| log n / max(d_J, 1))^{d_J/2}            (a_J = 2^{|J|/2} if d_J = 0) [LC-1].
The sum 𝒪_n^{>i} runs over j ≤ min(m♯_n, p − s₀) (unions S ∪ S₀ used in [T03R] (C8) may leave Ω) [LC-2]; i ≥ 0 an
integer; empty sums are 0.
- **(OS; C_OS)** at a given n: 𝒪_n^{>0} ≤ C_OS r_n and (2p)^{s₀}(n + 1)^{s₀/2} 𝒪_n^{>j₀} ≤ C_OS r_n. (Asymptotic
  statements assume it for all large n; finite-n bounds assume it at that n [L01-3].)
- **(ADG; c_D)** for every 1 ≤ j ≤ min(m♯_n, p − s₀): C(p−s₀, j)⁻¹ Σ_{|J|=j} (D_{S₀}/D_{S₀∪J})^{1/2} ≤ [c_D(n + 1)]^{−j/2}.
- **(DG; c_D)** D_{S₀∪J}/D_{S₀} ≥ [c_D(n + 1)]^{|J|} for every J ⊆ [p]∖S₀ with 1 ≤ |J| ≤ m♯_n.

**Identifiability margin.** **(ID; c)**: Δ_S ≥ c σ*² log n for every S ∈ Ω with S₀ ⊄ S and |S∖S₀| ≤ j₀. Ridge form
**(ID^M; c)**: the same with L_S := μ_cᵀ(I − M_S)μ_c = min_ϑ B_S(ϑ) ≥ Δ_S in place of Δ_S (weaker).
(ID_j; c), (ID^M_j; c) for j ∈ S₀: the same for every S ∈ Ω with j ∉ S and |S∖S₀| ≤ j₀.

**Approximate reference.** For T ∈ Ω and ϑ ∈ ℝ^T: the reference cost B_T(ϑ) := ‖μ − X_Tϑ‖² + (‖X_Tϑ‖² + ‖ϑ‖²)/n.

**Implications (`lemmas/A_occam.md` Lemma A0, `E_visibility.md` E3.1; R1, so A ≥ 1):** (F_w; g₀) ⇒ (DG; g₀/(1 + g₀)) ⇒ (ADG; same c_D) ⇒ (OS; C_OS(c_D, s₀, A))
for n ≥ n₀; (F_λ) ⇒ (F₀); (F_λ) ∧ (BM(c)) ⇒ (ID; c(1 − 1/n)) ([P3] `lem:signal`); (F₀) ∧ (E) ⇒ the coefficient bound
‖θ*‖² ≤ 1.5M/φ₀² ([L1a′] Remark 1); exact representation μ = X_Tθ ⇒ B_T(θ) = (‖μ‖² + ‖θ‖²)/n.

---

## Claim A (brief item 1) — Theorem 1-OS: the logarithmic-size floor (F_w) replaced by a superset Occam sum

**A1 (sufficiency).** In R1 under G, (E), (F_λ) and (OS) — in place of (F_w) — all conclusions 1–6 of [W3P] Theorem 1 hold
(item 6 with a common C_OS in place of g₀; item 7 is unchanged). Conclusion 5(a) needs only G, (E), (F₀), (OS) in R1.
In particular (ADG) or (DG) may replace (F_w).

**A2 (necessity of the Occam sum, deterministic).** For every n ≥ 3, design, data set and S₀ with s₀ ≤ K:
  δ_n ≥ 𝒪⁰_n / (1 + 𝒪⁰_n).
Hence, for fixed designs, δ_n → 0 in probability requires 𝒪⁰_n → 0 and δ_n = O_P(r_n) requires 𝒪⁰_n = O(r_n) (for random
designs: 𝒪⁰_n = O_P(r_n)) [L01-4]. (OS) is a **sufficient envelope used by this proof**, not a characterisation. Compared on j ≤ min(K − s₀, m♯_n), (OS)'s first sum differs from 𝒪⁰_n by (i) the weights a_J ≥ 1 (bounds on truncated χ² moments); outside that range (ii) 𝒪⁰_n also contains feasible supersets with j > m♯_n (controlled in the proof by the size tail instead), and (iii) (OS) also contains comparison unions S₀ ∪ J ∉ Ω (j > K − s₀), which have no counterpart in A2; and (iv) the amplified second inequality on j > j₀ has no counterpart in A2 [S01-6]. [LB] is the j = 1 term of A2 with
D_{S₀∪{j}}/D_{S₀} ≤ n + 1, on LB's domain.

Relation: A1 **implies** [W3P] Theorem 1 (since (F_w) ⇒ (OS)); A2 **implies** [LB] (supersedes it as a statement about the
superset mass). Item 1 of the brief asked for (DG) "or the weakest condition the proof actually uses": the proof uses
(F_w) only through (OS) (with (G3) by rank domination), and (DG) ⇒ (ADG) ⇒ (OS) are the clean sufficient forms [L01-4].

## Claim B (brief item 2) — Lemma 1a″: size tail with an approximate reference and the exact determinant

Truth with an arbitrary mean: y^r = α*1 + f + ε, ε ~ N_n(0, σ*²I) (**G′**; f ∈ ℝⁿ any vector, μ := Cf; G is the case
f = X^rβ*), ‖μ‖² ≤ nM, n ≥ 3, any standardised design X with p ≥ 2. Let T ∈ Ω (t := |T|) and ϑ ∈ ℝ^T be deterministic
with B_T(ϑ) ≤ B. Put A^T_m := R^T_m √(D_T) √n with R^T_m := Σ_{k=max(m+1,0)}^{K} q_k / w(t), and define Θ″_{n,m} ≥ 0 by
π(|S| > m) = A^T_m Θ″_{n,m} (Θ″ := 0 if R^T_m = 0). Then for every L > c♯² (c♯ of [T03R] line 77):
  sup_m P(Θ″_{n,m} > L) ≤ (8 + 24M/σ*²)/(n − 1) + L^{−1/2} + C″_Λ(B)/log(√L/c♯),
  C″_Λ(B) := 1/√2 + 1/2 + B/(2σ*²) + √(2B/π)/σ*.
The bound is uniform over all designs, references and means with these (M, B). Consequently π(|S| > m_n) = O_P(e^{−ω_n})
for every deterministic m_n with A^T_{m_n} ≤ e^{−ω_n}. Since D_T ≤ (n + 1)^t, A^T_m ≤ R^T_m (n+1)^{t/2}√n.

Relation: **implies** [L1a′] (take ϑ = θ with μ = X_Tθ: B = (‖μ‖² + ‖θ‖²)/n ≤ M + M′) and [W3P] Lemma 1a (T = S₀, ϑ = θ*:
B ≤ M + M/(2φ₀²), Θ♯ ≤ Θ″) [C1B-7]. New uses: references that drop weak coefficients (t < s₀), T = ∅ when ‖μ‖² = O(1), effective rank through D_T,
and means outside col X (G′).

## Claim C (brief item 3) — Proposition ER: an expectation rate (v1.2: O(r_n), adopting R03b C+)

Fix s₀, A and constants (σ*², M, φ₀, c, and g₀ or C_OS). There are n₀ and C depending only on these such that, for every
n ≥ n₀ and every fixed design and θ* for which, **at that n** [L01-3], R1's size conditions (s₀ ≤ K, 2 ≤ p ≤ n^A), G,
(E), (F₀) and one of (i) [W3P] Theorem 1's (F_λ), (F_w), BM(c), c > c₀; (ii) (F_λ), (OS), BM(c), c > c₀;
(iii) (OS), (ID^M; c), c > c₁ hold:
  **E δ_n ≤ C r_n = C√(log n/n).**
Hence (the brief's target) E δ_n = O(n^{−q/2}) for every q < 1, uniformly over such designs; P(HPM ≠ S₀) ≤ 2Eδ_n,
P(MPM ≠ S₀) ≤ 2Eδ_n, P(ξ_q ≠ S₀) ≤ Eδ_n/min(q, 1 − q), E max_j|PIP_j − 1{j ∈ S₀}| ≤ Eδ_n. Under BM-∞ the same holds
with n₀ depending on the envelope. For random designs on events 𝒜_n: E δ_n ≤ C r_n + P(𝒜_nᶜ) [L01-3]. With [LB] (when
s₀ + 1 ≤ K, s₀ < p): E δ_n ≥ (1 + √(n+1))⁻¹, so E δ_n is between order n^{−1/2} and order √(log n/n). By-product
(Lemma C2): E π(|S| > m) ≤ C R_m√(D_{S₀})√n + O(1/n) for every deterministic m.

Relation: **new conclusion**; implies item 1's O_P(r_n) (Markov) and strengthens [W3P] item 3's "E max_j|…| → 0, no
expectation rate claimed". (v1.1 had C n^{−1/2}e^{2√(2 log n)}; superseded.)

## Claim D (brief item 4, PROGRAM 1b) — Corollary H: in-sample predictive / Hellinger contraction

Parameter posterior: the exact joint posterior of (S, θ_S, v) under the working model, transformed to the original
response scale (θ = s_yβ, v = s_y²σ²) — by [P1] `thm:T01i` it is the contrast model Π_b, b = b₀s_y², with
v | S, y ~ IG(ν, b + Q^c_S/2) and θ_S | v, S, y ~ N(nH_S⁻¹z^c_S, nvH_S⁻¹). Fitted in-sample mean μ̂ := X_Sθ ∈ ℝⁿ (centred
scale), truth μ. Average Hellinger distance of the one-observation laws:
  h̄_n² := n⁻¹ Σ_i H²(N(μ̂_i, v), N(μ_i, σ*²)),  H²(P, Q) := 1 − ∫√(dP dQ);
then deterministically h̄_n² ≤ (v/σ*² − 1)² + ‖μ̂ − μ‖²/(4nσ*²).
**D(a) (with selection: oracle rate).** In R1 under G, (E), (F₀), if δ_n → 0 in probability (e.g. under the hypotheses of
[W3P] Theorem 1, Claim A1 or Claim E, with BM), then for every M_n → ∞:
  Π(‖μ̂ − μ‖² > M_n or |v/σ*² − 1| > M_n n^{−1/2} or S ≠ S₀ or ‖θ − θ*‖ > M_n n^{−1/2} | y) → 0 in probability
(θ zero-padded to ℝ^p) [L01-5],
hence Π(h̄_n > M_n n^{−1/2} | y) → 0 in probability.
**D(b) (no beta-min, no floor away from S₀: rate log n / n; v1.2 adopting R03b D+).** In R1 under G, (E), (F₀), (OS):
there is C_H depending only on (s₀, A, σ*²) such that for every M_n → ∞,
Π(‖μ̂ − μ‖² > C_H log n or |v/σ*² − 1| > M_n n^{−1/2} | y) → 0 in probability; hence
Π(h̄_n² > C_H′ log n / n | y) → 0 in probability, C_H′ := 1 + C_H/(4σ*²). (v1.1 assumed (F_λ) and gave the variance at
rate √(log n/n); superseded.)
Random designs: as [W3P] item 6 (events with common constants; ε independent of (X, θ*)).
h̄_n is the centred (intercept-free) distance; with the plug-in intercept the distance gains ε̄²/(4σ*²) = O_P(1/n)
and D(a), D(b) hold verbatim (`lemmas/D_hellinger.md` D4 Remark 0) [C1B-4].

Relation: **new** (PROGRAM item 1b; an in-sample marginal Hellinger analog, not an out-of-sample predictive theorem [L01-6]). Analog of Song–Liang (2015) Theorems 1–2 (posterior Hellinger consistency at rate
ε_n), with differences recorded in ASSUMPTION_MAP: fixed-design in-sample average instead of an integrated (x, y)
Hellinger distance; convergence in probability instead of exponential bounds; D(b) needs no beta-min and no floor
away from S₀.

## Claim E (brief item 5, stretch) — Theorem 1-VIS: (F_λ) away from S₀ replaced by an identifiability margin

In R1 under G, (E), (F₀), (OS) and (ID^M; c) with c > c₁(s₀, A) — (ID^M; c): L_S := μ_cᵀ(I − M_S)μ_c ≥ cσ*² log n for every
S ∈ Ω with S₀ ⊄ S, |S∖S₀| ≤ j₀; L_S = min_ϑ B_S(ϑ) ≥ Δ_S, so (ID; c) ⇒ (ID^M; c) (v1.2, R03b §D) — where
  c₁ := (√(2C_x) + √(2C_x + C_A j₀ + (2/log 2)(s₀(A + 1) + 2)))²,  C_x := Aj₀ + s₀ + log(j₀ + 1) + 2,
conclusions 1–4 of [W3P] Theorem 1 hold (δ_n = O_P(r_n); exact HPM = MPM = S₀ w.p. → 1; ξ_{q_n} = S₀ w.p. → 1 for
deterministic q_n with r_n = o(min(q_n, 1 − q_n)); PIPs; size and functionals), and Claim C applies [L01-6]. Without (ID^M), (ID^M_j; c) gives π(S ∌ j) = O_P(r_n) (5(b) analog). Item 6
(random design) as in [W3P]. No eigenvalue condition is imposed on any set other than S₀; (OS) holds e.g. under (DG).

Relation: **supersedes [W3P] Theorem 1 items 1–4 and Claim A1 items 1–4 for beta-min constants c > c₁** (since
(F_λ) ∧ BM(c) ⇒ (ID; c(1 − 1/n)) ⇒ (ID^M; c′) for any fixed c₁ < c′ < c and n ≥ c/(c − c′)) [L01-6]; for c₀ < c ≤ c₁ they **coexist** (c₁ ≈ 161 vs c₀ = 128 at s₀ = A = 1; c₀ < c₁ checked numerically on s₀ ≤ 20, A ∈ [1, 10], min c₁/c₀ = 1.23 [C1B-8]; both are proof
artefacts). Answers "is the floor set size improvable": yes — the bounded-size normalised floor on S₀ ∪ J is not needed;
only the floor on S₀, a superset Occam sum, and an identifiability margin on bounded-excess underfits.

## Kill/stop rules for this ticket
Each item is a separate claim; any item exceeding ~1/3 of the ticket's effort is stopped with the reason recorded.
Claim E has a kill budget: statement lock + one proof attempt.
