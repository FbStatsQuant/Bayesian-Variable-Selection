# L2 — The lattice at polynomial size: no-addition from the width gap, its converse, the sufficient forms, and truth removal (key lemma; claims (C3)(a)–(c), bridges (P2)–(P5))

Status: **PROVED (by this seat, unchecked)**; lemma check LC1-B (Codex gpt-6.1-sol high, blind,
`../reviews/LC1B_L2L3_check_sol.md`): Lemma 0, NA-conv, NA-W, sufficient forms (i)–(v), Lemma d, TL-W VERIFIED;
W-conv (+ corollary) VERIFIED-WITH-AMENDMENTS (1 MINOR on the wording of the "Reading" paragraph, applied [LC1B-1]);
no FATAL, no MAJOR. Independent mid-point MP1 (Codex gpt-6-astra high, blind, `../reviews/MP1_midpoint_astra.md`): CONTINUE WITH CHANGES — "the key lemma stands", no FATAL or MAJOR finding in L0–L3.
Ticket W3-RM2; statement: `../STATEMENT.md` v1.3, §1 (width
functionals), §3.1 ((W), (W-δ), (W-unif), (W-χ), (W-ref), (W-loc), (BM-W)), §4 ((C3), (P2)–(P5)).
Inputs: `L0_toolkit_b.md` (Lemma Toolkit-b, for the lattice family) and one classical fact — Gaussian concentration
for Lipschitz functions: if f : ℝⁿ → ℝ is 1-Lipschitz and g ~ N(0, I_n), then E|f(g)| < ∞ and, for t ≥ 0,
P(f(g) − Ef(g) ≥ t) ≤ e^{−t²/2} and P(f(g) − Ef(g) ≤ −t) ≤ e^{−t²/2} (Tsirelson–Ibragimov–Sudakov; Borell).
The descent lemma (C-GROW:L1.1/L1.2 through W3-RM:RM-0) is not used in this file. Templates (no conclusion of
them is used): C-GROW:L2.1–L2.3 (`Theory_work/Wave1C/C-GROW/lemmas/L2_NA_TL.md`), RM Lemma NA-F
(`Theory_work/Wave3/W3-RM/lemmas/L2_NAF.md`).

## 0. Setting, objects, standing hypotheses

Setting F and the notation of `L0_toolkit_b.md` §0. Standing hypotheses of this file:
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

## 1. Lemma NA-W — no-addition from the width gap (claim (C3)(a), bridge (P3))

**Lemma NA-conv (score conversion with a size-dependent level).** Under (F0), (FL-Q): there is n₀ depending only on
(σ², M, φ₀, A) and the sequence q log n/n such that for n ≥ n₀, on 𝓔_n ∩ 𝒵_n, F(T ∪ {l}) − F(T) ≤ −½ for every
(T, l) ∈ 𝔓; in particular NA(𝓛) holds.
*Proof.* Let (T, l) ∈ 𝔓, k := |T| ≤ K − 1 ≤ p − 1. T and T ∪ {l} are in 𝔉_lat, so by (E6) of L0 and (F3),
F(T ∪ {l}) − F(T) = log[w(k + 1)/w(k)] − ½ log(n + 1) + ν log(RSS_T/RSS_{T∪{l}}) + (R_{T∪{l}} − R_T).
Prior: w(k + 1)/w(k) ≤ (k + 1)/p (L0, prior ratios). Fit: x := (RSS_T − RSS_{T∪{l}})/RSS_T = σ²Z²_{T,l}/RSS_T; on 𝒵_n,
Z²_{T,l} ≤ c_n(k) ≤ (2A + 2) log n by (0.2), and RSS_T ≥ nσ²/2 ((T2)(a)), so x ≤ 4(A + 1) log n/n ≤ ¼ for n ≥ n₀. By
(T5)(b), ν log(RSS_T/RSS_{T∪{l}}) ≤ (1 + ϑ_n)(1 + 2x)Z²_{T,l}/2 ≤ Z²_{T,l}/2 + ½, because
(Z²_{T,l}/2)[(1 + ϑ_n)(1 + 2x) − 1] ≤ (A + 1) log n·(ϑ_n + 2x + 2xϑ_n) → 0 (ϑ_n log n → 0 by L0; x log n ≤ 4(A + 1)(log n)²/n).
Hence F(T ∪ {l}) − F(T) ≤ log(k + 1) − log p − ½ log(n + 1) + c_n(k)/2 + ½ + 2κ_E = −½. NA(𝓛) is the statement
F(T ∪ {l}) < F(T) for all T ∈ 𝓛 with |T| < K and l ∉ T, i.e. for all (T, l) ∈ 𝔓. ∎

**Lemma NA-W.** Under (F0), (FL-Q): put s_n := −𝔴⁰_n. If s_n > 0 and (3/4)s_n√(log(n + 1)) ≥ 4κ_E + 2, then

  P(𝒵_nᶜ) ≤ exp(−s_n²/8).                                                                              (1.1)

Consequently, if **𝔴⁰_n → −∞** (condition (W)), then for n ≥ n₀:
P(NA(𝓛)ᶜ) ≤ exp(−(𝔴⁰_n)²/8) + P(𝓔_nᶜ) ≤ exp(−(𝔴⁰_n)²/8) + 2e^{−n^{1/3}} + n^{−2} + 2/n → 0, which is [NA(Q)].
Under (W-δ) (𝔴_n(δ₀) ≤ 0 for n ≥ n₀): 𝔴⁰_n ≤ −δ₀√(log n)/(2√(2A + 2)) and P(𝒵_nᶜ) ≤ n^{−c*}, c* := δ₀²/(32(2A + 2)).
*Proof.* Φ⁰_n is 1-Lipschitz: each g ↦ |u_{T,l}ᵀg| − a⁰_n(|T|) is 1-Lipschitz (‖u_{T,l}‖ = 1; the shift is a constant) and
a maximum of 1-Lipschitz functions is 1-Lipschitz. By (F3), Φ⁰_n(ε/σ) = max_𝔓(|Z_{T,l}| − a⁰_n(|T|)) and ε/σ ~ N(0, I_n). By
concentration, P(Φ⁰_n(ε/σ) > −s_n/2) = P(Φ⁰_n − EΦ⁰_n > s_n/2) ≤ exp(−s_n²/8).
Deterministically Φ⁰_n(g) ≥ −a_min, a_min := min_𝔓 a⁰_n(|T|) (take a pair attaining the minimum level and use
|u ᵀg| ≥ 0); hence −s_n = EΦ⁰_n ≥ −a_min, i.e. **s_n ≤ a⁰_n(|T|) for every pair**. On {Φ⁰_n(ε/σ) ≤ −s_n/2}, for every
(T, l) ∈ 𝔓, with a := a⁰_n(|T|): 0 ≤ |Z_{T,l}| ≤ a − s_n/2, so
Z²_{T,l} ≤ a² − as_n + s_n²/4 ≤ a² − (3/4)as_n ≤ a² − (3/4)s_n√(log(n + 1)) ≤ a² − 4κ_E − 2 = c_n(|T|),
using s_n ≤ a, a ≥ √(log(n + 1)) by (0.2), and the assumed size of s_n. This is (1.1). The consequence: when
𝔴⁰_n → −∞ the size condition holds for n ≥ n₀ (n₀ depending on the sequence 𝔴⁰_n and on κ_E), and
NA(𝓛)ᶜ ⊆ 𝒵_nᶜ ∪ 𝓔_nᶜ for n ≥ n₀ by Lemma NA-conv; P(𝓔_nᶜ) by (T1).
(W-δ): for 0 ≤ k < p and n ≥ 3, a⁰_n(k)² − a_{n,δ₀}(k)² = log(n + 1) − (1 − δ₀) log n ≥ δ₀ log n and
a⁰_n(k) + a_{n,δ₀}(k) ≤ 2a⁰_n(k) ≤ 2√((2A + 2) log n) by (0.2), so a⁰_n(k) − a_{n,δ₀}(k) ≥ δ₀√(log n)/(2√(2A + 2)) =: γ_n for
every k; then Φ⁰_n(g) ≤ max_𝔓(|u_{T,l}ᵀg| − a_{n,δ₀}(|T|)) − γ_n and 𝔴⁰_n ≤ 𝔴_n(δ₀) − γ_n ≤ −γ_n. With s_n ≥ γ_n:
exp(−s_n²/8) ≤ exp(−γ_n²/8) = n^{−δ₀²/(32(2A+2))}. ∎

## 2. Lemma W-conv — the width gap is forced by the route (claim (C3)(b), bridge (P5))

**Lemma W-conv.** Under (F0), (FL-Q): put s_n := 𝔴⁰_n. There is n₀ depending only on (σ², M, φ₀, A) and the sequence
q log n/n such that for n ≥ n₀: if s_n√(log(n + 1)) ≥ 8κ_E + 8, then

  P(NA(𝓛)) ≤ exp(−s_n²/8) + P(𝓔_nᶜ).                                                                    (2.1)

In particular **if 𝔴⁰_n → +∞ then P(NA(𝓛)) → 0**.
*Proof.* By concentration (lower tail), P(Φ⁰_n(ε/σ) < s_n/2) ≤ exp(−s_n²/8). On {Φ⁰_n(ε/σ) ≥ s_n/2} ∩ 𝓔_n there is
(T, l) ∈ 𝔓 with |Z_{T,l}| ≥ a + s_n/2, a := a⁰_n(k), k := |T| < K; so Z²_{T,l} ≥ a² + as_n. T ∪ {l} ∈ Ω (|T| < K), and by
(E6) and (F3),
F(T ∪ {l}) − F(T) = log[w(k + 1)/w(k)] − ½ log(n + 1) + ν log(RSS_T/RSS_{T∪{l}}) + (R_{T∪{l}} − R_T)
  ≥ log((k + 1)/(2p)) − ½ log(n + 1) + (1 − 4n^{−1/3})Z²_{T,l}/2 − 2κ_E
(prior ratio ≥ (k + 1)/(2p); (T5)(c) with Λ_T = 0, (F1); remainders bounded by 2κ_E). By the definition of a,
log((k + 1)/(2p)) − ½ log(n + 1) = −a²/2 − log 2, and Z²_{T,l} ≥ a² + as_n, so
F(T ∪ {l}) − F(T) ≥ ½as_n(1 − 4n^{−1/3}) − 2n^{−1/3}a² − log 2 − 2κ_E ≥ ¼as_n − 1 − log 2 − 2κ_E > 0
for n ≥ n₀ (4n^{−1/3} ≤ ½ and 2n^{−1/3}a² ≤ 2n^{−1/3}(2A + 2) log n ≤ 1), because as_n ≥ s_n√(log(n + 1)) ≥ 8κ_E + 8.
So NA(𝓛) fails on that event, which gives (2.1). ∎

**Corollary (the v1.2 form).** Let a⁺_{n,δ}(k) := √(2 log(2p/(k + 1)) + (1 + δ) log n). If, for a fixed δ₁ ∈ (0, 1],
E max_𝔓(|u_{T,l}ᵀg| − a⁺_{n,δ₁}(|T|)) ≥ 0 for all large n, then 𝔴⁰_n ≥ δ₁√(log n)/(2√(2A + 4)) → ∞ and P(NA(𝓛)) → 0.
*Proof.* For n ≥ 2 and k < p: a⁺² − a⁰² = 2 log 2 + (1 + δ₁) log n − log(n + 1) ≥ δ₁ log n (2 log 2 ≥ log(1 + 1/n)), and
a⁺ + a⁰ ≤ 2a⁺ ≤ 2√((2A + 4) log n) (2 log(2p) + (1 + δ₁) log n ≤ 2 log 2 + (2A + 2) log n ≤ (2A + 4) log n). So
a⁺ − a⁰ ≥ δ₁√(log n)/(2√(2A + 4)) uniformly in k, Φ⁰_n(g) ≥ max_𝔓(|u_{T,l}ᵀg| − a⁺_{n,δ₁}(|T|)) + δ₁√(log n)/(2√(2A + 4)), and
taking expectations gives the bound on 𝔴⁰_n; then Lemma W-conv. ∎

**Reading.** With the gap 𝔴⁰_n = E max over the lattice of (Gaussian projection − level): gap → −∞ ⇒ whole-lattice
no-addition w.p. → 1; gap → +∞ ⇒ it fails w.p. → 1. [LC1B-1] When the gap stays bounded, neither divergence
conclusion applies; the finite-n bounds remain available whenever their respective size conditions hold. Nothing here
concerns the conclusion Ŝ⁺ = S₀: an improving addition at some lattice set need not be met by the search.

## 3. Sufficient forms (claim (C3)(c), bridge (P4))

Throughout, g ~ N(0, I_n), b ∈ (0, ½) fixed, q ≤ n^b.

**(i) (W-δ) ⇒ (W).** Proved in Lemma NA-W: 𝔴⁰_n ≤ −δ₀√(log n)/(2√(2A + 2)) → −∞.

**(ii) (W-unif) with parameter δ ∈ (0, (1 − 2b)/2) ⇒ (W-δ) with δ₀ = δ.** For (T, l) ∈ 𝔓, k = |T| ≤ q ≤ n^b, so
a_{n,δ}(k)² ≥ 2 log p − 2 log(n^b + 1) + (1 − δ) log n ≥ 2 log p + (1 − 2b − δ) log n − 2 log 2 ≥ 2 log p + (1 − 2b − 2δ) log n
as soon as δ log n ≥ 2 log 2. Hence, for such n,
𝔴_n(δ) ≤ E max_𝔓|u_{T,l}ᵀg| − min_𝔓 a_{n,δ}(|T|) ≤ √(2 log p + (1 − 2b − 2δ) log n) − min_𝔓 a_{n,δ}(|T|) ≤ 0. ∎

**(iii) (W-χ) ⇒ (W-δ) for every δ₀ < δ₁.** Assume |Q ∖ S₀| ≤ (1 − δ₁) log n. Fix (T, l) ∈ 𝔓 and put Q_l := Q ∖ {l}
(so T ⊆ Q_l, l ∉ Q_l, and Q_l ∪ {l} = Q ∪ {l}). Write (I − P_T)x_l = a + c with a := (I − P_{Q_l})x_l ≠ 0 ((F2)) and
c := (P_{Q_l} − P_T)x_l; a ⊥ c because P_{Q_l} − P_T is the projector on span X_{Q_l} ⊖ span X_T. For any g, by
Cauchy–Schwarz in ℝ², (aᵀg + cᵀg)² ≤ (‖a‖² + ‖c‖²)[(aᵀg)²/‖a‖² + (cᵀg)²/‖c‖²] (second term 0 if c = 0), and
(cᵀg)²/‖c‖² ≤ ‖(P_{Q_l} − P_T)g‖² ≤ ‖(P_Q − P_{S₀})g‖² (range(P_{Q_l} − P_T) ⊆ range(P_Q − P_{S₀}) since S₀ ⊆ T ⊆ Q_l ⊆ Q).
As ‖(I − P_T)x_l‖² = ‖a‖² + ‖c‖²:

  (u_{T,l}ᵀg)² ≤ (u_{Q_l,l}ᵀg)² + ‖(P_Q − P_{S₀})g‖²   for every (T, l) ∈ 𝔓.                                (3.1)

The vectors u_{Q_l,l}, l ∈ [p] ∖ S₀, are at most p unit vectors; P_Q − P_{S₀} has rank |Q ∖ S₀|. If p ≥ 2, by Jensen,
(G3) and E‖(P_Q − P_{S₀})g‖² = |Q ∖ S₀|:
(E max_𝔓|u_{T,l}ᵀg|)² ≤ E max_l (u_{Q_l,l}ᵀg)² + |Q ∖ S₀| ≤ 2 log p + 2 log(1 + 2 log p) + 1 + (1 − δ₁) log n.
(If p = 1 then 𝔓 = ∅.) On the other hand k ≤ q ≤ s₀ + (1 − δ₁) log n, so
min_𝔓 a_{n,δ₀}(|T|)² ≥ 2 log p − 2 log(s₀ + 1 + log n) + (1 − δ₀) log n. The difference of the two right sides is
(δ₁ − δ₀) log n − O(log log n) > 0 for n ≥ n₀; hence 𝔴_n(δ₀) ≤ E max_𝔓|u ᵀg| − min_𝔓 a_{n,δ₀} ≤ 0. ∎
((W-χ) forces q ≤ s₀ + log n ≤ n^b for large n, so it is compatible with every b > 0.)

**(iv) (W-ref) with h + b < ½ ⇒ (W-unif) with δ = (1 − 2b − 2h)/4.** Let (𝒱_n, m₀, h), (𝒜_n, L_n), ρ_n, η_n be as in
(W-ref): every u_{T,l}, (T, l) ∈ 𝔓, is v + Σ_{a∈𝒜_n}λ_aa + w with v ∈ V ∈ 𝒱_n, ‖v‖ ≤ 1 + η_n, Σ|λ_a| ≤ L_n,
w ∈ span(X_{Q∪{l}}), ‖w‖ ≤ ρ_n. With Π_V the projector on V and Π_l the projector on span(X_{Q∪{l}}):
|u_{T,l}ᵀg| ≤ (1 + η_n)‖Π_Vg‖ + L_n max_{a∈𝒜_n}|aᵀg| + ρ_n‖Π_lg‖ (the middle term absent if 𝒜_n = ∅). By (G2) (dimension
≤ m₀, |𝒱_n| subspaces; dimension ≤ q + 1, at most p subspaces) and (G1):
E max_𝔓|u_{T,l}ᵀg| ≤ (1 + η_n)(√m₀ + √(2 log|𝒱_n|)) + L_n√(2 log(2|𝒜_n|)) + ρ_n(√(q + 1) + √(2 log p))
  ≤ √(2 log p + 2h log n) + e_n,
e_n := η_n√(2 log p + 2h log n) + (1 + η_n)√m₀ + L_n√(2 log(2|𝒜_n|)) + ρ_n(√(q + 1) + √(2 log p)) = o(√log n)
(η_n → 0 and log p + h log n = O(log n); L_n² log(|𝒜_n| + 1) = o(log n); ρ_n²(q + log n) = o(log n), p ≤ n^A).
With δ = (1 − 2b − 2h)/4 > 0: 1 − 2b − 2δ = 2h + 2δ, δ < (1 − 2b)/2, and
√(2 log p + (2h + 2δ) log n) − √(2 log p + 2h log n) ≥ 2δ log n/(2√((2A + 1) log n)) = δ√(log n)/√(2A + 1)
(the larger radicand is ≤ (2A + 1) log n because 2h + 2δ < 1). For n ≥ n₀, e_n ≤ δ√(log n)/√(2A + 1), which is
(W-unif) with parameter δ. ∎
(RM's (N-D)(i) is the case m₀ = 1, 𝒜_n = ∅, η_n = 0, 𝒱_n = {span(v) : v ∈ 𝒰_n}, w = u_{T,l} − v ∈ span(X_{Q∪{l}}).)

**(v) (W-loc) ⇒ (W-ref)** with the same h, m₀ = 1, ρ_n = 0. Let N_l, ν_n, L_n, η_n be as in (W-loc). Fix (T, l) ∈ 𝔓,
B := T ∩ N_l ⊆ Q ∖ {l}. By (F2), a := (I − P_T)x_l ≠ 0 with ‖a‖² ≥ (n − 1)φ₀², and (I − P_B)x_l ≠ 0 (B ∪ {l} ⊆ Q ∪ {l}).
With the regressions of STATEMENT §1 (P_Bx_l = X_Bβ_{B,l}, P_Tx_l = X_Tβ_{T,l}, zero-padded to ℝ^Q),
a = x_l − X_Qβ̄_{T,l} = (I − P_B)x_l − X_Qλ, λ := β̄_{T,l} − β̄_{B,l}, ‖λ‖₁ ≤ L_n. Dividing by ‖a‖:

  u_{T,l} = v − Σ_{t∈Q}(λ_t‖x_t‖/‖a‖)·(x_t/‖x_t‖),   v := (I − P_B)x_l/‖a‖ ∈ span(u_{B,l}).

‖v‖ = ‖(I − P_B)x_l‖/‖a‖ ≤ (1 + η_n)^{1/2} by the second inequality of (W-loc); the atoms x_t/‖x_t‖, t ∈ Q, are |Q| unit
vectors with coefficients of total absolute value ≤ L_n√(n − 1)/(φ₀√(n − 1)) = L_n/φ₀, and (L_n/φ₀)² log(|Q| + 1) = o(log n).
The lines span(u_{B,l}), l ∈ [p], B ⊆ N_l, number at most p·2^{ν_n}, and log(p·2^{ν_n}) ≤ log p + h log n. So (W-ref)
holds with 𝒱_n := {span(u_{B,l})}, 𝒜_n := {x_t/‖x_t‖ : t ∈ Q}, atom bound L_n/φ₀, remainder 0 and (1 + η_n)^{1/2} − 1 → 0 in
place of η_n. ∎
*The parenthetical remark of (W-loc).* X_Qλ = (I − P_B)x_l − a = (P_T − P_B)x_l lies in span X_T, hence is orthogonal to
a; so ‖(I − P_B)x_l‖² = ‖a‖² + ‖X_Qλ‖² ≤ ‖a‖² + (L_n√(n − 1))² ≤ (1 + L_n²/φ₀²)‖a‖². Thus the first inequality of (W-loc)
implies the second with η_n = L_n²/φ₀² whenever L_n → 0. ∎

## 4. Lemma TL-W — truth removal under (BM-W) (bridge (P2))

𝒟ᵀ_n := {u_{A,i} : T ∈ 𝓛, i ∈ S₀, A = T ∖ {i} or A = (T ∖ {i}) ∪ {l} with l ∈ [p] ∖ T} (defined by (F2): A ∪ {i} ⊆ Q ∪ {l});
d_n := E max_{v∈𝒟ᵀ_n}|vᵀg|; λ_n := (n − 1)φ₀²θ*²_min/σ². (BM-W): λ_n/(d_n² + log n) → ∞.

**Lemma d (size of the truth-removal width).** d_n ≤ √(q + 1) + √(2 log p) ≤ √(q + 1) + √(2 log(2p)), hence
d_n² ≤ 2(q + 1) + 4 log(2p), and (BM-Q) [θ*²_min nφ₀²/(σ²(q + log n)) → ∞] implies (BM-W).
*Proof.* u_{A,i} ∈ span(X_{A∪{i}}) ⊆ span(X_{Q∪{l}}) (for a deletion any l will do, e.g. l ∈ Q), a subspace of
dimension ≤ q + 1; there are at most p such subspaces. So max_{𝒟ᵀ_n}|vᵀg| ≤ max_l‖Π_lg‖ and (G2) applies. Then
d_n² + log n ≤ 2(q + 1) + 4 log(2p) + log n ≤ C(A)(q + log n). ∎

**Lemma TL-W.** Under (F0), (FL-Q), (BM-W): let
𝒵⁺_n := {Z²_{T,l} ≤ (2A + 2) log n for all (T, l) ∈ 𝔓⁺} and ℬ_n := {max_{v∈𝒟ᵀ_n}|vᵀε|/σ ≤ d_n + √(2 log n)}.
Then P(ℬ_nᶜ) ≤ 1/n; P(𝒵⁺_nᶜ) ≤ P(𝒵_nᶜ) + 2/n; and there is n₀ (depending on the constants and on the rate in (BM-W))
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

*Size.* By (F2), θ*_i²‖(I − P_A)x_i‖²/σ² ≥ λ_n. On ℬ_n, |Z_{A,i}| ≤ d_n + √(2 log n) ≤ √(2d_n² + 4 log n) ≤ ½√λ_n for
n ≥ n₀ (BM-W), so the first square is ≥ σ²λ_n/4. On 𝒵⁺_n the subtracted term is ≤ σ²(2A + 2) log n ≤ σ²λ_n/8 for n ≥ n₀
(λ_n/log n → ∞). So RSS_A − RSS_T ≥ σ²λ_n/8 > 0.
*Score.* By (E6) for A, T ∈ 𝔉_lat, with |A| − |T| ∈ {−1, 0}:
F(A) − F(T) = log[w(|A|)/w(|T|)] − ½(|A| − |T|) log(n + 1) − ν log(RSS_A/RSS_T) + (R_A − R_T)
  ≤ log(2p) + ½ log(n + 1) + 2κ_E − (RSS_A − RSS_T)/(2C_R) ≤ (A + 1) log n + 2 + 2κ_E − σ²λ_n/(16C_R) < 0
for n ≥ n₀ (prior ratio w(k − 1)/w(k) ≤ 2p, or 1 for a swap; (T4)(b); λ_n/log n → ∞). ∎

**Remarks.** (1) Both kinds of direction are needed in 𝒟ᵀ_n: after a swap the truth is regressed on (T ∖ {i}) ∪ {l}, not
on T ∖ {i}. (2) The toolkit's contrast bound (T4)(a), whose cost t_n + h_n² = O(q + log n) made RM's Lemma B3 require
(BM-Q), is not used: (4.1) is exact. (3) Lemma TL-W uses (W) only through 𝒵⁺_n, a bound of order log n on the
addition statistics at lattice sets; without any such bound the subtracted term in (4.1) could only be bounded by
‖Π_lε‖²/σ² = O(q + log n), which is (BM-Q) again.

## 5. Summary of what this file delivers

| claim | where | hypotheses beyond (F0), (FL-Q) | conclusion |
|---|---|---|---|
| (C3)(a) / (P3) | §1 | (W): 𝔴⁰_n → −∞ | P(NA(𝓛)ᶜ) ≤ exp(−(𝔴⁰_n)²/8) + P(𝓔_nᶜ) for n ≥ n₀; under (W-δ) the first term is n^{−c*} |
| (C3)(b) / (P5) | §2 | 𝔴⁰_n → +∞ | P(NA(𝓛)) ≤ exp(−(𝔴⁰_n)²/8) + P(𝓔_nᶜ) for n ≥ n₀ |
| (C3)(c) / (P4) | §3 | each sufficient form | (W-loc) ⇒ (W-ref) ⇒ (W-unif) ⇒ (W-δ) ⇒ (W); (W-χ) ⇒ (W-δ) |
| (P2) | §4 | (BM-W), P(𝒵_n) → 1 | P(TL(𝓛)) → 1; (BM-Q) ⇒ (BM-W) |
