# L0 — Toolkit: GEN L1 on families with logarithmically growing set sizes

Status: **PROVED (by this seat, unchecked)**; lemma check R03 (Codex Sol high, reviews/R03_L0L1L2_check_sol.md): VERIFIED (a re-statement of GEN L1 with one constant changed; GEN L1 has check
record GEN/reviews/R02 Sol VERIFIED-WITH-AMENDMENTS, applied).
Source: `Theory_work/Wave1/W1-GEN/lemmas/L1_lemmaE.md` (cited as [GEN-L1]). Notation of STATEMENT.md §1 and [GEN-L1]:
Y := Cy^r = μ + Cε, RSS_A := ‖(I − P_A)Y‖², r_A := (I − P_A)μ, Λ_A := ‖r_A‖², and

  RSS_A = Λ_A + 2⟨r_A, ε⟩ + ‖Cε‖² − ‖P_Aε‖²   ([GEN-L1] (1.1)).

## L0.1 What changes

[GEN-L1] assumes a deterministic family 𝔉 with |A| ≤ J for a **fixed** J, |𝔉| ≤ C_F n^D, a Gram floor
λ_min(R̂_A) ≥ φ₀² on nonempty A ∈ 𝔉, ‖μ‖² ≤ Mn, and a vector set 𝒱𝒱 with |𝒱𝒱| ≤ C_V n^{D_V}. Here we allow

  |A| ≤ J_n ≤ C_J log n for A ∈ 𝔉   (C_J fixed),

and replace t_n := 4(D + 2) log n by t_n := 4(D + 2 + C_J) log n. Everything else is unchanged.

**Lemma L0.1.** With this change, Lemmas L1.1–L1.4 of [GEN-L1] hold verbatim (same events 𝒟₁, 𝒟₂, 𝒟₃, same
constants C_R = 3(M + σ²), c_E = σ²/(12(M + σ²)), κ_E = 0.52/c_E + 1), with n₀ depending also on C_J.

*Proof.* Only two places use J.
(i) 𝒟₂ in L1.1: for a deterministic projection of rank d ≤ J_n, P(‖Pε‖²/σ² > t) ≤ 2^{d/2}e^{−t/4}
≤ n^{C_J (log 2)/2}e^{−t/4} ≤ n^{C_J}e^{−t/4}; at t = t_n this is n^{C_J}·n^{−(D+2+C_J)} = n^{−(D+2)}; the union over
≤ C_F n^D sets gives P(𝒟₂ᶜ) ≤ C_F n^{−2}. t_n is still O(log n), which is all L1.2–L1.4 use.
(ii) L1.3 needs (n − 1)φ₀² ≥ max(J, 100) (for x_i ≤ 0.01 in (E1)) and uses J/((n − 1)φ₀²) ≤ 1 in the remainder bound;
both hold with J_n = O(log n) for n ≥ n₀(C_J, φ₀). ∎

## L0.2 Three consequences (used in L2, L3)

On 𝒟₁ ∩ 𝒟₂ ∩ 𝒟₃ (with 𝒱𝒱 ⊇ {r_A : A ∈ 𝔉}) and n ≥ n₀:

(a) **RSS floor, sharp form.** For every A ∈ 𝔉: RSS_A ≥ σ²n(1 − ω_n), ω_n := 4n^{−1/3} + (h_n² + t_n + 1)/n → 0.
*Proof.* As in [GEN-L1] L1.2(a): RSS_A ≥ Λ_A − 2σh_n√Λ_A + σ²(n − 1 − 2√((n−1)n^{1/3}) − 2n^{1/3}) − σ²t_n and
Λ − 2σh_n√Λ ≥ −σ²h_n²; 2√((n − 1)n^{1/3}) + 2n^{1/3} ≤ 4n^{2/3}. ∎

(b) **One-step likelihood ratio for nested sets.** If A, A ∪ {l} ∈ 𝔉, x := (RSS_A − RSS_{A∪{l}})/RSS_A ∈ [0, 1) and
x ≤ ¼, then
  ν log(RSS_A/RSS_{A∪{l}}) = −ν log(1 − x) ≤ (RSS_A − RSS_{A∪{l}})/(2σ²)·(1 + ϑ_n)·(1 + 2x),
with ϑ_n := (1 + 0.02/n)/(1 − ω_n) − 1 → 0; and for any nested A ⊆ A′ in 𝔉,
  ν log(RSS_A/RSS_{A′}) ≤ ν(RSS_A − RSS_{A′})/RSS_{A′} ≤ (RSS_A − RSS_{A′})(1 + ϑ_n)/(2σ²).
*Proof.* −log(1 − x) ≤ x + x² ≤ x(1 + 2x) for x ∈ [0, ½]; ν = n/2 + 0.01; RSS_A ≥ σ²n(1 − ω_n) by (a). The second
display: log u ≤ u − 1 with u = RSS_A/RSS_{A′}, and RSS_{A′} ≥ σ²n(1 − ω_n). ∎

(c) **Score differences** ([GEN-L1] (E6)). For A, A′ ∈ 𝔉,
  F(A) − F(A′) = log[w(|A|)/w(|A′|)] − ½(|A| − |A′|) log(n + 1) − ν log(RSS_A/RSS_{A′}) + (R_A − R_{A′}),
  |R_A − R_{A′}| ≤ 2κ_E,
and for block tables (A ⊆ A′ ⊆ C_b, both in 𝔉): log r_b(A′) − log r_b(A) = −½(|A′| − |A|) log(n + 1)
− ν log(RSS_{A′}/RSS_A) + (R_{A′} − R_A). (Immediate from (E4); r_b(U) = m(U)/m(∅).)

Prior ratios used throughout (w(k) = 1/(2C(2p − 1, k))): w(k + 1)/w(k) = (k + 1)/(2p − 1 − k); for k ≤ p − 1,
2p − 1 − k ≥ p, so log[w(k + 1)/w(k)] ≤ log(k + 1) − log p, and log[w(k − 1)/w(k)] = log((2p − k)/k) ∈ [0, log(2p)]
for 1 ≤ k ≤ p.
