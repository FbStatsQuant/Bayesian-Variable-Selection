# L3 — The probability event E_n

Status: **PROVED (by this seat, unchecked)**; lemma check R03 (Codex Sol high): VERIFIED-WITH-AMENDMENTS (items 4–8),
applied. Falsification numerics: the event components are standard Gaussian
bounds; the consequences used in L4 are monitored along simulated paths in numerics/n5_invariants.py → N5_raw.jsonl.

Setting: STATEMENT §1–2 and L1 (Υ_n = I). Deterministic objects: S₀, the partition, N₀, S* = [p] ∖ N₀,
𝒩* := S* ∖ S₀, m₀ := |𝒩*| = p − s₀ − |N₀| ≥ p − s₀ − 15. Random inputs (L1.1): η ~ N(0,1), ξ ~ N(0, I_p),
r ~ χ²_{n−1−p}, independent; (ξ_j)_{j∈𝒩*} iid N(0,1).

**Notation.** L_n := log log n. H := √(2 log(2m₀ + 2)). 𝒩*± := {j ∈ 𝒩* : ±ξ_j > 0}, m₀± := |𝒩*±|.
ζ_(i) := i-th largest of {|ξ_j| : j ∈ 𝒩*}; ζ±_(i) := i-th largest of {|ξ_j| : j ∈ 𝒩*±}. Top(j) := the j elements
of 𝒩* with the largest |ξ| (a.s. unique), D_j := Σ_{i∈Top(j)}ξ_i, P_j := #(Top(j) ∩ 𝒩*₊). Fixed constants
ε_bal := 1/50 (renamed from η, which denotes the Gaussian factor; R03 item 4), K₁ := 100/ε_bal² = 250 000; m₁ := ⌈K₁L_n⌉; δ_e := 2 log(25 m₁ H)/H; g_max := L_n + δ_e.

**Regimes.** (S) p ≤ n^{1/200}; (L) p > n^{1/200} (then m₀ ≥ n^{1/200} − s₀ − 15 → ∞ and H² ≥ (1/100)log n).
**Conventions** (R03 item 6): max over ∅ is 0; if m₀ = 0, E4 is vacuous; E5–E7 are the sure event outside regime (L);
in regime (L), E6 asserts in particular that each sign has at least m₁ observations (nonexistent order statistics := −∞).

## The event E_n := E1 ∩ … ∩ E7

* **E1** |η| ≤ L_n and |ξ_j| ≤ L_n for every j ∈ S₀ ∪ N₀.
* **E2** r ≥ (n − 1 − p)(1 − n^{−1/3}); |gᵀΣ⁻¹g + r − (n − 1)| ≤ n^{2/3}; |θ*ᵀg| ≤ L_n(θ*ᵀΣθ*)^{1/2}.
* **E3** max_{j∈𝒩*}|ξ_j| ≤ H̄ := (H² + 2L_n)^{1/2} (note H̄ − H ≤ L_n/H, and in regime (L), for n ≥ n₀, L_n/H ≤ δ_e — R03 item 5).
* **E4** ζ_(i)² ≤ Z_i² := 2 log(2m₀/i) + 4 log log n for every 1 ≤ i ≤ m₀.
* **E5** (regime (L)) for every 1 ≤ j ≤ m₀, with x_j := 2 log(j + 1) + L_n: |D_j| ≤ H̄√(2j x_j) and
  |P_j − j/2| ≤ √(j x_j/2); and m₀± ≥ m₀/3.
* **E6** (regime (L)) ζ₊_(m₁) ≥ H − δ_e and ζ₋_(m₁) ≥ H − δ_e.
* **E7** (regime (L)) every interval of length L_n/2 contained in [0, H − δ_e] contains |ξ_j| for some j ∈ 𝒩*₊ and
  for some j ∈ 𝒩*₋.

**Consequences used in L4** (on E_n, n ≥ n₀):
(c1) ‖e‖²/σ² ∈ [n − 1 − n^{2/3}, n − 1 + n^{2/3}], s² = θ*ᵀΣθ* + σ² + O(n^{−1/3}); |ϱ| ≤ C_ρ(L_n + 1), where ϱ is the
centre offset of L4.0.
(c2) (regime (L)) consecutive values of {|ξ_j| : j ∈ 𝒩*₊} below H − δ_e differ by ≤ L_n; the top m₁ values of each
sign lie in [H − δ_e, H̄] ⊆ [H̄ − 2δ_e, H̄]; so **all** consecutive gaps of each one-signed sample, and the gap across 0 (smallest
positive plus smallest negative magnitude), are ≤ g_max.
(c3) In regime (L), δ_e = O(L_n/H) and m₁δ_e = O(L_n²/H) → 0; H δ_e = O(L_n).

**Lemma L3.1.** P(E_n) → 1.

*Proof.* **E1**: s₀ + 16 standard normals; P(|N(0,1)| > L_n) ≤ 2e^{−L_n²/2}.
**E2**: Laurent–Massart: P(χ²_N − N ≤ −2√(Nt)) ≤ e^{−t}, P(|χ²_N − N| ≥ 2√(Nt) + 2t) ≤ 2e^{−t}. With N = n − 1 − p ≥ n/2 − 1
(p ≤ n/2) and t = log n, 2√(N log n) ≤ N n^{−1/3} for large n; gᵀΣ⁻¹g + r ~ χ²_{n−1} and 2√(n log n) + 2 log n ≤ n^{2/3}.
θ*ᵀg ~ N(0, θ*ᵀΣθ*).
**E3**: P(max > H̄) ≤ m₀ · 2Φ̄(H̄) ≤ 2m₀φ(H̄)/H̄ = 2m₀e^{−H²/2}e^{−L_n}/(H̄√(2π)) ≤ e^{−L_n} → 0 (any p).
**E4**: {ζ_(i) > z} = {#{j : |ξ_j| ≥ z} ≥ i}; the count has mean 2m₀Φ̄(z) ≤ m₀e^{−z²/2} (z ≥ 1). With
z_i := (2 log(m₀ log²n / i))^{1/2}, Markov gives P(ζ_(i) > z_i) ≤ 1/log² n. For 2^h ≤ i < 2^{h+1},
ζ_(i) ≤ ζ_(2^h) ≤ z_{2^h} and z_{2^h}² ≤ 2 log(2m₀ log² n/i) = Z_i². The union over 0 ≤ h ≤ log₂ m₀ ≤ log₂ n has
probability ≤ (log₂ n + 1)/log² n → 0.
**E5**: conditional on (|ξ_j|)_{j∈𝒩*} the signs are iid Rademacher (ξ_j symmetric), so Top(j) is fixed and
D_j = Σ_{Top(j)} sign_i|ξ_i|; Hoeffding: P(|D_j| ≥ √(2V_jx)) ≤ 2e^{−x}, V_j = Σ_{Top(j)}ξ² ≤ jH̄² on E3; likewise
P(|P_j − j/2| ≥ √(jx/2)) ≤ 2e^{−x}. With x = x_j the union over j costs ≤ 4e^{−L_n}Σ_j(j + 1)^{−2} → 0. m₀₊ ~ Bin(m₀, ½):
Hoeffding with t = m₀/6.
**E6**: let t₀ := Φ̄⁻¹(2m₁/m₀) (in regime (L), 2m₁/m₀ → 0, so t₀ ≥ 1 for n ≥ n₀). #{j ∈ 𝒩* : ξ_j ≥ t₀} ~
Bin(m₀, Φ̄(t₀)) has mean 2m₁, so P(ζ₊_(m₁) < t₀) = P(Bin < m₁) ≤ e^{−m₁/4} → 0 (Chernoff); this also gives at least m₁
positive observations. t₀ ≤ H because Φ̄(H) ≤ e^{−H²/2} = 1/(2m₀ + 2) < 2m₁/m₀. Lower bound: for t ≥ 1,
Φ̄(t) ≥ φ(t)/(2t), so 2m₁/m₀ ≥ e^{−t₀²/2}/(2t₀√(2π)), i.e. t₀² ≥ 2 log m₀ − 2 log(4√(2π) m₁ t₀). For m₀ ≥ 5,
2 log(2m₀ + 2) − 2 log m₀ = 2 log(2 + 2/m₀) ≤ 2 log 2.4 and 4√(2π)·2.4 < 25, so with t₀ ≤ H:
t₀² ≥ H² − 2 log(25 m₁ H). Hence H − t₀ = (H² − t₀²)/(H + t₀) ≤ 2 log(25 m₁ H)/H = δ_e. Same for ζ₋ (R03 item 7).
**E7** (R03 item 8): put b := H − δ_e (≥ 1 eventually; b ≤ t₀ by E6's computation), h := L_n/4, and use the full grid
cells I_r := [rh, (r + 1)h] ⊆ [0, b], r = 0, 1, …: there are ≤ b/h ≤ 4H/L_n of them, and every subinterval of [0, b] of
length 2h = L_n/2 contains a full cell. For each cell and each sign, P(no j ∈ 𝒩* with ξ_j ∈ I_r) ≤ exp(−m₀ h φ(b)) and
φ(b) ≥ Φ̄(b) ≥ Φ̄(t₀) = 2m₁/m₀ (b ≥ 1, b ≤ t₀), so each probability is ≤ exp(−L_n m₁/2); the union over the cells and
both signs (reflection for the negative sample) is ≤ 2(4H/L_n + 1)exp(−L_n m₁/2) → 0, since log H ≤ L_n/2 + O(1) and
m₁ ≥ K₁L_n. ∎

**Remark (regime (S)).** In regime (S) L4 uses only E1, E2, E3.
