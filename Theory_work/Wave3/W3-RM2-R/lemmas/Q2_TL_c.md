# Q2 — Lemma TL-F-c: truth removal under the additive constant-level floor (BM-W⁺); and the posterior/mode input under (T1-F♭) (bridges (Q2), (Q3); claims W3-RM2-R:TL-F-c, and the [POST]/[MODE] step of RM2-F-plus)

Status: **PROVED (by this seat, unchecked)** — 2026-11-16, lead Claude Opus 5.5. Ticket W3-RM2-R; statement:
`../STATEMENT.md` v1.0 §2 ((BM-W⁺), (T1-F♭), 𝓜_n, [MODE]), §4 bridges (Q2), (Q3).
**This file is a partial copy** of PARENT `Theory_work/Wave3/W3-RM2/lemmas/L2_width.md` (claims W3-RM2:TL-F-b@1.0.0,
NA-W@1.0.0, "PROVED-CHECKED; council R1, …"; sha256 prefix 0fa63729eeac8c28 in `../DEPS.tsv`): its §0 (setting,
facts, Lemma 0) and §4 (Lemma TL-W) are copied; **changed lines are marked [R-#]**; unmarked lines are the parent's
text. §§1–3 of the parent (Lemma NA-conv, Lemma NA-W, Lemma W-conv, the sufficient forms) are **not changed and are
cited**, not copied: PARENT `lemmas/L2_width.md:56-180`. §6 (new, [R-6]) is the posterior/mode input (Q3).
PARENT := `Theory_work/Wave3/W3-RM2/`. Inputs: PARENT `lemmas/L0_toolkit_b.md` (Lemma Toolkit-b, W3-RM2:Toolkit-b@1.0.0),
PARENT `lemmas/L2_width.md` §1 (Lemma NA-W, W3-RM2:NA-W@1.0.0), Gaussian concentration as quoted in the parent header
(`L2_width.md:9-11`), and SOP:TH09@1.0.0 for §6 (status below).

## 0. Setting, objects, standing hypotheses

Setting F and the notation of PARENT `lemmas/L0_toolkit_b.md` [R-0] §0. Standing hypotheses of this file:
(F0) ‖μ‖² ≤ Mn; p ≤ n^A (A ≥ 1); S₀ = supp θ*, s₀ = |S₀| ≥ 1 fixed; Q = Q_n ⊇ S₀ deterministic, q := |Q| ≤ K =
     min(p, ⌊n/2⌋), and **q log n/n → 0** (true if q ≤ n^b with a fixed b < 1).
(FL-Q) λ_min(R̂_{Q∪{l}}) ≥ φ₀² for every l ∈ [p].
𝓛 := {T : S₀ ⊆ T ⊆ Q}; 𝔓 := {(T, l) : T ∈ 𝓛, |T| < K, l ∈ [p] ∖ T}; 𝔓⁺ := {(T, l) : T ∈ 𝓛, l ∈ [p] ∖ T} ⊇ 𝔓.
𝔉_lat, 𝒱𝒱_lat: the lattice family of L0 §4(ii); 𝓔_n: its toolkit event. By L0 §4(ii) the hypotheses of Lemma Toolkit-b
hold for it, so (T1)–(T5) are available with t_n + h_n² = O(q + log n), ω_n log n → 0, ϑ_n log n → 0, and
P(𝓔_nᶜ) ≤ 2e^{−n^{1/3}} + n^{−2} + 2/n.

**Facts.** (F1) For T ∈ 𝓛: μ ∈ span X_{S₀} ⊆ span X_T, so r_T = 0, Λ_T = 0.
(F2) For B ⊆ [p] and j ∉ B with B ∪ {j} ⊆ Q ∪ {l} for some l ∈ [p]: X_{B∪{j}} has full column rank ((FL-Q), interlacing),
(I − P_B)x_j ≠ 0, u_{B,j} := (I − P_B)x_j/‖(I − P_B)x_j‖ is defined, u_{B,j} ⊥ span X_B and u_{B,j} ⊥ 1, and
  ‖(I − P_B)x_j‖² = 1/[(X_{B∪{j}}ᵀX_{B∪{j}})⁻¹]_{jj} ≥ λ_min(X_{B∪{j}}ᵀX_{B∪{j}}) ≥ (n − 1)φ₀²;
  RSS_B − RSS_{B∪{j}} = (u_{B,j}ᵀY)².                                                                    (0.1)
(F3) For (T, l) ∈ 𝔓⁺: u_{T,l}ᵀY = u_{T,l}ᵀCε = u_{T,l}ᵀε (u ⊥ μ by (F1), u ⊥ 1), so with Z_{T,l} := u_{T,l}ᵀε/σ:
RSS_T − RSS_{T∪{l}} = σ²Z²_{T,l}. The vector ε/σ is N(0, I_n).

Levels and functionals (STATEMENT §1): a⁰_n(k) := √(log(n + 1) + 2 log(p/(k + 1))),
a_{n,δ}(k) := √(2 log(p/(k + 1)) + (1 − δ) log n) (0 ≤ k < p); for g ∈ ℝⁿ,
Φ⁰_n(g) := max_{(T,l)∈𝔓}(|u_{T,l}ᵀg| − a⁰_n(|T|)); 𝔴⁰_n := EΦ⁰_n(g), 𝔴_n(δ) := E max_𝔓(|u_{T,l}ᵀg| − a_{n,δ}(|T|)), g ~ N(0, I_n).
If 𝔓 = ∅ every statement about 𝔓 below is vacuous; assume 𝔓 ≠ ∅ where a maximum over 𝔓 is written.
c_n(k) := log(n + 1) + 2 log p − 2 log(k + 1) − 4κ_E − 2 = a⁰_n(k)² − 4κ_E − 2;
𝒵_n := {Z²_{T,l} ≤ c_n(|T|) for all (T, l) ∈ 𝔓}. For (T, l) ∈ 𝔓, k = |T| ≤ K − 1 ≤ p − 1, so
  log(n + 1) ≤ a⁰_n(k)² ≤ log(n + 1) + 2 log p ≤ (2A + 2) log n   (n ≥ 2).                                (0.2)

**Lemma 0 (three elementary Gaussian bounds).** Let g ~ N(0, I_n).
(G1) For unit vectors v₁, …, v_N (N ≥ 1): E max_i |v_iᵀg| ≤ √(2 log(2N)).
(G2) For linear subspaces V₁, …, V_N of dimension ≤ d, with projectors Π_i: E max_i ‖Π_ig‖ ≤ √d + √(2 log N).
(G3) For unit vectors v₁, …, v_N, N ≥ 2: E max_i (v_iᵀg)² ≤ 2 log N + 2 log(1 + 2 log N) + 1.
*Proof.* (G1): for λ > 0, exp(λE max|v_iᵀg|) ≤ E exp(λ max|v_iᵀg|) ≤ Σ_i E(e^{λv_iᵀg} + e^{−λv_iᵀg}) = 2Ne^{λ²/2}; take
λ = √(2 log(2N)). (G2): g ↦ ‖Π_ig‖ is 1-Lipschitz with mean ≤ (E‖Π_ig‖²)^{1/2} ≤ √d, so by concentration
E exp(λ(‖Π_ig‖ − E‖Π_ig‖)) ≤ e^{λ²/2} (a 1-Lipschitz function of g is sub-Gaussian with variance proxy 1), and as in
(G1) E max_i(‖Π_ig‖ − E‖Π_ig‖) ≤ √(2 log N). (G3): for λ ∈ (0, ½), E max_i(v_iᵀg)² ≤ λ⁻¹ log(N(1 − 2λ)^{−1/2}); with
m := 1 + 2 log N and λ := (1 − 1/m)/2 this is (m/(2 log N))(2 log N + log m) = m + m log m/(2 log N)
= 1 + 2 log N + (1 + 1/(2 log N)) log m ≤ 1 + 2 log N + 2 log m (2 log N ≥ 1 for N ≥ 2). ∎
(The sub-Gaussian moment bound used in (G2): for 1-Lipschitz f, E exp(λ(f(g) − Ef(g))) ≤ exp(λ²/2) for all real λ —
the standard form of Gaussian concentration; the tail bounds quoted in the header follow from it by Chernoff.)

**Cited unchanged from the parent (not copied):** Lemma NA-conv, Lemma NA-W (with (1.1): under (W), P(𝒵_nᶜ) ≤
exp(−(𝔴⁰_n)²/8) for n ≥ n₀), Lemma W-conv, sufficient forms (i)–(v): PARENT `lemmas/L2_width.md:56-180`.

## 4. Lemma TL-F-c — truth removal under (BM-W⁺) (bridge (Q2)) [R-1]

𝒟ᵀ_n := {u_{A,i} : T ∈ 𝓛, i ∈ S₀, A = T ∖ {i} or A = (T ∖ {i}) ∪ {l} with l ∈ [p] ∖ T} (defined by (F2): A ∪ {i} ⊆ Q ∪ {l});
d_n := E max_{v∈𝒟ᵀ_n}|vᵀg|; λ_n := (n − 1)φ₀²θ*²_min/σ². (BM-W): λ_n/(d_n² + log n) → ∞.
[R-1] **(BM-W⁺)** (STATEMENT §2): for n ≥ n₀, (i) √λ_n ≥ 2(d_n + √(2 log n)) and (ii) λ_n ≥ c_TL log n, for a fixed
c_TL > c_TL⁰ := 8(A + 1) + 4(2A + 1)C_R/σ², C_R = 3(M + σ²) (PARENT `lemmas/L0_toolkit_b.md:38`).

**Lemma d (size of the truth-removal width).** d_n ≤ √(q + 1) + √(2 log p) ≤ √(q + 1) + √(2 log(2p)), hence
d_n² ≤ 2(q + 1) + 4 log(2p), and (BM-Q) [θ*²_min nφ₀²/(σ²(q + log n)) → ∞] implies (BM-W).
*Proof.* u_{A,i} ∈ span(X_{A∪{i}}) ⊆ span(X_{Q∪{l}}) (for a deletion any l will do, e.g. l ∈ Q), a subspace of
dimension ≤ q + 1; there are at most p such subspaces. So max_{𝒟ᵀ_n}|vᵀg| ≤ max_l‖Π_lg‖ and (G2) applies. Then
d_n² + log n ≤ 2(q + 1) + 4 log(2p) + log n ≤ C(A)(q + log n). ∎
[R-2] **Implications into (BM-W⁺).** (a) (BM-W) ⇒ (BM-W⁺): (2(d_n + √(2 log n)))² ≤ 8d_n² + 16 log n ≤ 16(d_n² + log n),
so λ_n/(d_n² + log n) → ∞ gives (i) and, since d_n² + log n ≥ log n, (ii) for n ≥ n₀. (b) (BM-Q♭) ⇒ (BM-W⁺), where
(BM-Q♭): λ_n ≥ 32(q + 1) + 64 log(2p) + max{c_TL, 16} log n: by Lemma d, 16(d_n² + log n) ≤ 32(q + 1) + 64 log(2p) + 16 log n
≤ λ_n, which gives (i) by the display in (a), and λ_n ≥ c_TL log n is (ii). (c) If d_n² ≤ D log n for a fixed D, then
4(d_n + √(2 log n))² ≤ 4(√D + √2)² log n = 8(1 + √(D/2))² log n, so λ_n ≥ max{c_TL, 8(1 + √(D/2))²} log n gives (BM-W⁺).

**Lemma TL-F-c** [R-3]. Under (F0), (FL-Q), (BM-W⁺): let
𝒵⁺_n := {Z²_{T,l} ≤ (2A + 2) log n for all (T, l) ∈ 𝔓⁺} and ℬ_n := {max_{v∈𝒟ᵀ_n}|vᵀε|/σ ≤ d_n + √(2 log n)}.
Then P(ℬ_nᶜ) ≤ 1/n; P(𝒵⁺_nᶜ) ≤ P(𝒵_nᶜ) + 2/n; and there is n₀ (depending on A, M, σ², φ₀, c_TL, the n₀ of (BM-W⁺) and the
sequence q log n/n) [R-3]
such that for n ≥ n₀, on 𝓔_n ∩ 𝒵⁺_n ∩ ℬ_n, TL(𝓛) holds: F(A) < F(T) for every T ∈ 𝓛 and every feasible neighbour A of T
with S₀ ⊄ A. Hence, if also P(𝒵_n) → 1 (in particular under (W), Lemma NA-W), then P(TL(𝓛)) → 1: [TL(Q)].
*Proof.* *Probabilities.* g ↦ max_{v∈𝒟ᵀ_n}|vᵀg| is 1-Lipschitz with mean d_n, and ε/σ ~ N(0, I_n): by concentration
P(ℬ_nᶜ) ≤ exp(−(√(2 log n))²/2) = 1/n. For (T, l) ∈ 𝔓,
c_n(|T|) ≤ (2A + 2) log n by (0.2), so on 𝒵_n the bound holds on 𝔓. A pair of 𝔓⁺ ∖ 𝔓 has |T| = K, hence T = Q with
q = K, and l ∉ Q: at most p standard normals Z_{Q,l}, and P(max_l Z²_{Q,l} > (2A + 2) log n) ≤ 2p·n^{−(A+1)} ≤ 2/n.
*Which neighbours remove a truth.* A neighbour of T (one flip or one swap) with S₀ ⊄ A is A = T ∖ {i} or
A = (T ∖ {i}) ∪ {l} with i ∈ S₀, l ∉ T; both have |A| ≤ |T| ≤ K (feasible) and belong to 𝔉_lat.
*The identity.* Put B := A ∪ {i}; B = T for a deletion and B = T ∪ {l} for a swap. By (0.1),
RSS_A − RSS_B = (u_{A,i}ᵀY)². Now μ − θ*_ix_i ∈ span X_{S₀∖{i}} ⊆ span X_A, u_{A,i} ⊥ span X_A and u_{A,i} ⊥ 1, so
u_{A,i}ᵀY = θ*_iu_{A,i}ᵀx_i + u_{A,i}ᵀε = θ*_i‖(I − P_A)x_i‖ + σZ_{A,i}, Z_{A,i} := u_{A,i}ᵀε/σ. For a swap, RSS_T − RSS_B = σ²Z²_{T,l}
by (F3). Therefore

  RSS_A − RSS_T = (θ*_i‖(I − P_A)x_i‖ + σZ_{A,i})² − σ²Z²_{T,l}·1{A is a swap}.                              (4.1)

*Size.* [R-4] By (F2), θ*_i²‖(I − P_A)x_i‖²/σ² ≥ λ_n, i.e. |θ*_i|‖(I − P_A)x_i‖ ≥ σ√λ_n. On ℬ_n,
|Z_{A,i}| ≤ d_n + √(2 log n) ≤ ½√λ_n by (BM-W⁺)(i), so |θ*_i‖(I − P_A)x_i‖ + σZ_{A,i}| ≥ σ√λ_n − σ|Z_{A,i}| ≥ ½σ√λ_n
and the first square is ≥ σ²λ_n/4. On 𝒵⁺_n the subtracted term is ≤ σ²(2A + 2) log n ((T, l) ∈ 𝔓⁺). So
  RSS_A − RSS_T ≥ σ²(λ_n/4 − (2A + 2) log n) ≥ σ²(c_TL/4 − 2A − 2) log n > 0
by (BM-W⁺)(ii), since c_TL > c_TL⁰ > 8(A + 1).
*Score.* By (E6) for A, T ∈ 𝔉_lat, with |A| − |T| ∈ {−1, 0}:
F(A) − F(T) = log[w(|A|)/w(|T|)] − ½(|A| − |T|) log(n + 1) − ν log(RSS_A/RSS_T) + (R_A − R_T)
  ≤ log(2p) + ½ log(n + 1) + 2κ_E − (RSS_A − RSS_T)/(2C_R)
  ≤ (A + ½) log n + (3/2) log 2 + 2κ_E − σ²(λ_n/4 − (2A + 2) log n)/(2C_R)
  ≤ −γ log n + (3/2) log 2 + 2κ_E,   γ := σ²(c_TL/4 − 2A − 2)/(2C_R) − (A + ½) > 0,
which is < 0 for n ≥ n₀ [R-5] (prior ratio w(k − 1)/w(k) ≤ 2p, or 1 for a swap, and the Occam term is absent for a
swap, so the first line bounds both kinds; (T4)(b) applies because RSS_A > RSS_T; log(2p) ≤ A log n + log 2 and
½ log(n + 1) ≤ ½ log n + ½ log 2; (BM-W⁺)(ii)). γ > 0 ⇔ c_TL/4 − 2A − 2 > 2C_R(A + ½)/σ² ⇔ c_TL > 8(A + 1) + 4(2A + 1)C_R/σ²
= c_TL⁰. ∎

**Remarks.** (1) Both kinds of direction are needed in 𝒟ᵀ_n: after a swap the truth is regressed on (T ∖ {i}) ∪ {l}, not
on T ∖ {i}. (2) The toolkit's contrast bound (T4)(a), whose cost t_n + h_n² = O(q + log n) made RM's Lemma B3 require
(BM-Q), is not used: (4.1) is exact. (3) Lemma TL-W uses (W) only through 𝒵⁺_n, a bound of order log n on the
addition statistics at lattice sets; without any such bound the subtracted term in (4.1) could only be bounded by
‖Π_lε‖²/σ² = O(q + log n), which is (BM-Q) again. (4) [R-5] The constant c_TL⁰ is a proof artefact (C_R comes from
the crude bound RSS_A ≤ ‖Y‖² ≤ C_R n of the toolkit); the order λ_n ≍ d_n² + log n is what identity (4.1) needs.

## 6. The posterior and mode input under (T1-F♭) (bridge (Q3)) [R-6]

**Lemma POST/MODE-F.** In Setting F, under (T1-F♭) (STATEMENT §2: (H0) of GROW with "BM-∞, or BM(c) with a fixed
c > c₀(s₀, A)"), [POST] E[1 − π(S₀)] → 0 and [MODE] P(𝓜_n) → 1 hold, where 𝓜_n := {S₀ is the unique maximiser of F on Ω}
(for n with s₀ ≤ K; s₀ ≤ K holds eventually under (H0)).
*Proof.* (T1-F♭) is the hypothesis list of SOP:TH09@1.0.0 with either beta-min branch: the card
`Theory_work/State_of_Project/sections/04_theory.tex:784` ("BM-∞ … Alternatively BM(c) uses a fixed c > c₀(s₀, A)") and
the final statement `:788` ("Under R1, G, R, SE_λ(j₀), SE_w(m♯_n; g₀), and BM-∞ or BM(c > c₀), 1 − π(S₀) = O_P(√(log n/n))");
restated as Theorem 1 item 1 at `Theory_work/Wave3/W3-POST/STATEMENT.md:64-82`. So 1 − π(S₀) → 0 in probability, and as
0 ≤ 1 − π(S₀) ≤ 1, E[1 − π(S₀)] ≤ ε + P(1 − π(S₀) > ε) for every ε > 0; let n → ∞, then ε → 0 (as PARENT
`lemmas/L3_assemblyF.md:22-24`). [MODE]: π(S) = exp F(S)/Σ_{S′∈Ω} exp F(S′) on Ω, so on {π(S₀) > ½} every S ∈ Ω ∖ {S₀}
has π(S) ≤ 1 − π(S₀) < π(S₀), i.e. F(S) < F(S₀): {π(S₀) > ½} ⊆ 𝓜_n. By Markov, P(𝓜_nᶜ) ≤ P(1 − π(S₀) ≥ ½) ≤ 2E[1 − π(S₀)] → 0. ∎
Status of the input (verbatim, registry): SOP:TH09@1.0.0 "T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2).
T02(i♯), T02(ii♯): PROVED; SF/XF VERIFIED. T01–T03: PROVED-LOCKED (wave 3; external review queued), SAME-FAMILY-ONLY" —
below PROVED-CHECKED: claims using this lemma are **conditional on SOP:TH09**.
(The identity π ∝ exp F on Ω: F(S) = log w(|S|) + log m(S) and π(S) ∝ ϖ(S)m(S) with ϖ(S) = w(|S|)/W_K, POST
`STATEMENT.md:23-24`.)

