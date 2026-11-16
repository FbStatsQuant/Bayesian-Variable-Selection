# R5 — Examples table (T7⁺⁺): the changed rows

Status: **PROVED (by this seat)**. The check record is kept outside this file (the ticket's final checkpoint file and `reviews/`).
Citations: BASE = `Theory_work/Wave3/W3-START/` (v1.3.4); `STATEMENT.md` without prefix is this ticket's v1.5.
Statement proved: `STATEMENT.md` §3.1 [EX] (`:199-211`): the rows F-1, F-3, F-2, G-1, G-2 as changed there; every other row
is BASE (T7) and BASE `lemmas/L11_EXAMPLES.md` unchanged. Uses: BASE `lemmas/L11_EXAMPLES.md` (frames, designs and the
verifications cited by line), (T1⁺⁺), F2⁺⁺, F4⁺⁺ (`lemmas/R1_VIS.md`, `lemmas/R4_TRANSFER_COR.md`, `lemmas/R2_NEC.md`),
(T3⁺⁺)(b)(ii)–(iii) (`lemmas/R3_RATE.md`), PARENT `STATEMENT.md:57-61` (𝔏^♯_n(h) ≤ 𝔏_n(S₀; h)).

## R5.1 F-1 (orthogonal) and F-3 (near-duplicate nulls): exact order without a growth condition on p

Designs: BASE `lemmas/L11_EXAMPLES.md:17-18` (F-1; the frame of `:10-12` exists for every p ≤ n − 1) and `:29-31` (F-3,
1 + 2m_n ≤ p ≤ n − 1). In both, s₀ ≥ 1 fixed, θ_lo ≤ |θ*_j| ≤ θ_hi on S₀, p > s₀ for all large n.
* (E), (GF-16): BASE `:19` (F-1; g_* = 1), `:32-34` (F-3; g_* = d²/2).
* Null gains δ_{U,l} = 0 for every null l and every U: BASE `:20` (F-1), `:35-36` (F-3). So η′ = 0 in F2⁺⁺, and
  𝔏_n(S₀) ≤ √(2/π)z̄_n (BASE `lemmas/L6_COROLLARIES.md:42-45`), hence n^{−1/2}𝔏_n(S₀)² = O(log n/√n) → 0.
* (V-cp) for every fixed c_V > 1: δ²_{U,j} = Nθ*_j² for j ∈ S₀ and U ∌ j (F-1: BASE `:21`; F-3: `:37`, where S₀ = {1}) and
  τ²_U ≤ σ² + s₀θ_hi², so δ²_{U,j}/τ²_U ≥ Nθ_lo²/(σ² + s₀θ_hi²) ≥ (c_V + 2A) log n ≥ c_V log n + 2 log p for n large. So
  κ_V = (c_V − 1)/2 can be taken > ½.
* λ_min(R̂_{S₀}) = 1 (F-1: X_{S₀}ᵀX_{S₀} = N·I; F-3: S₀ = {1}, R̂ = 1): F2⁺⁺ with φ₀ = 1.
By F2⁺⁺ (STATEMENT [F2]; proof `lemmas/R4_TRANSFER_COR.md` R4.2 with PARENT `lemmas/P1_LEADING.md:128-144`): o₀ is of exact
order n^{−1/2}, with no condition on p beyond p > s₀ (and the design constraints p ≤ n − 1, 1 + 2m_n ≤ p). ∎

## R5.2 F-2 (one truth, fifteen correlated nulls): (V-mp) with every c_m < 1 + 2A; rate; first-order form for A > 3/4

Design: BASE `lemmas/L11_EXAMPLES.md:43-50`: A ∈ [0.1, 1], p := min(⌊n^A⌋, n − 1), ρ² = 0.4, c := 2(1 + 2A), S₀ = {1},
μ = θ*₁e₁ with ‖μ‖² = cσ² log n, Λ_N = cσ² log n·q_k (k := |N ∩ {2, …, 16}|, q₀ = 1, q₁ = 0.6, q_k ≥ q₁₅ = 1/11),
σ² ≤ τ²_N ≤ σ²(1 + c log n/N). (E), (GF-16): BASE `:51-53`. Note log p/log n → A.

**(V-mp) with Q = S₀, any c_m ∈ (0, 1 + 2A) and any ε₀ > 0, for n large.** Q = S₀ forces R = ∅ and c_Q = 16; V = D = {1};
N ⊆ [p] ∖ {1}, a := |N| ≤ 15, d = 1; U = N, T = {1}, W = N ∪ {1}. Since μ ∈ span x₁, Λ_T = Λ_W = 0, and (V-mp) reads
  Λ_N/τ²_N ≥ π_n(1, a; S₀) + c_m log n.
* a = 0: π_n = log n + 2 log p ≤ (1 + 2A) log n (p ≤ n^A). LHS = c log n/(τ²_∅/σ²) ≥ 2(1 + 2A) log n/(1 + c log n/N). This is
  ≥ (1 + 2A + c_m) log n as soon as 2(1 + 2A)/(1 + c log n/N) ≥ 1 + 2A + c_m, true for n large because c_m < 1 + 2A.
* a = 1: π_n = 0. LHS ≥ cq₁ log n/(1 + c log n/N) = 1.2(1 + 2A) log n/(1 + o(1)) ≥ c_m log n for n large (c_m < 1 + 2A).
* 2 ≤ a ≤ 15: π_n = −(a − 1)(log n + 2 log(p/16)). For n large p ≥ 16, so π_n ≤ −(log n + 2 log(p/16)), and since
  log p/log n → A, π_n + c_m log n ≤ (c_m − 1 − 2A + o(1)) log n < 0 ≤ LHS for n large.
The term (1 + ε₀)(Λ_T − Λ_W)/τ²_W is 0, so ε₀ > 0 is arbitrary. Hence κ_V = c_m/2 can be any number in (0, (1 + 2A)/2).
(Version 1.3.4 had c_m = (1 + 2A)/6, BASE `:54-58`; the gain comes from the negative price for a ≥ 2 and from the a = 0
instance being asked only at log n + 2 log p.)

**F4⁺⁺ levels.** I_n := {2, …, 16}, ī = 15. For l ∈ I_n and every U ∌ l, |U| ≤ 15: δ²_{U,l} ≤ 0.4cσ² log n ≤ 0.8(1 + 2A)τ²_U log n
(BASE `:61-63`). Write 0.8(1 + 2A) log n = c_n log n + 2 log p with c_n := 0.8(1 + 2A) − 2 log p/log n → 0.8 − 0.4A ≤ 0.76;
so c_n ≤ 1 for n large and the premise of F4⁺⁺ holds. For l ≥ 17, δ_{U,l} = 0 (BASE `:64`), and ϱ^{−I}_n(S₀) ≤ 2n^{−1/2}√(2/π)z_n
(BASE `:64-65`). By F4⁺⁺ (STATEMENT [F4]; `lemmas/R2_NEC.md`) with the levels h of F4, b_n(h) → 0 and
  ϱ_n(S₀; h) ≤ 2n^{−1/2}√(2/π)z_n + 2·15·n^{−(1−c_n)/2}e^{C_A√(log n log log n)} = n^{−(1+2A)/10+o(1)},
because (1 − c_n)/2 → (0.2 + 0.4A)/2 = (1 + 2A)/10 and (1 + 2A)/10 ≤ 0.3 < ½. So (AL) holds with h.

**Conclusions.** (T1⁺⁺)(a), (b), (d) apply with (V-mp) and this h. Since ϱ_n(S₀; h) = 2n^{−1/2}𝔏_n(S₀; h):
n^{−1/2}𝔏_n(S₀; h) ≤ n^{−(1+2A)/10+o(1)} and, by 𝔏^♯_n(h) ≤ 𝔏_n(S₀; h) (PARENT `STATEMENT.md:59`), n^{−1/2}𝔏^♯_n(h) ≤
n^{−(1+2A)/10+o(1)}; n^{−1}𝔏_n(S₀; h)² ≤ n^{−(1+2A)/5+o(1)}. Take c_m ∈ ((1 + 2A)/5, 1 + 2A), so that κ_V = c_m/2 > (1 + 2A)/10,
and κ ∈ ((1 + 2A)/10, κ_V). (T1⁺⁺)(b) gives o₀ = O_P(n^{−(1+2A)/10+o(1)}) + o_P(n^{−κ}), i.e. **o₀ = O_P(n^{−(1+2A)/10+η})
for every η > 0** (the o(1) is deterministic).
*First-order form.* Take c_m ∈ (1, 1 + 2A), so κ_V > ½. Then n^{−1/2}𝔏_n(S₀; h)² = n^{1/2}·(n^{−1/2}𝔏_n(S₀; h))²
≤ n^{1/2−(1+2A)/5+o(1)} = n^{3/10−2A/5+o(1)} → 0 iff A > 3/4. So for **A ∈ (3/4, 1]**, (T1⁺⁺)(c) applies: o₀/T₁ → 1 in
probability. (For A ≤ 3/4 this upper bound does not give (c); nothing is claimed.) ∎

## R5.3 G-1 (Gaussian rows, Σ_n = I_p): o₀ = O_P(√(log n/n))

Setting R with Σ_n = I_p, s₀ ≥ 1, s₀ < p ≤ n^A (p ≫ n allowed), |θ*_j| ∈ [θ_lo, θ_hi] on S₀. (FL-R16) with c_Σ = 1 and (V-R) with
a_V = θ_lo: BASE `lemmas/L11_EXAMPLES.md:80`. (L-R⁺⁺) with Q = S₀, H_l := {l} ∪ S₀, C_L = 0, r_n = 0: the covariance identities
of BASE `:81-83`; |H_l| = s₀ + 1 =: H̄_n, and log(s₀ + 1) ≤ κ_H√log n for all large n, for any κ_H > 0. (L-gain-0) with C₀ = 0:
Cov(W_l, W_j) = 0 for l ≠ j (`STATEMENT.md` (D5), C₀ = 0 form). By (T3⁺⁺)(b)(iii) (`lemmas/R3_RATE.md` R3.6):
**o₀ = O_P(√(log n/n))**, hence 1 − π₀(S₀) = O_P(√(log n/n)), for every p ≤ n^A. (BASE `:85-86` noted this sharper rate
and did not claim it.) ∎

## R5.4 G-2 (block-diagonal Σ_n, one truth per group): 1 − π₀(𝓛(Q)) = O_P(√(log n/n))

Design and verification of (FL-R16), (V-R), (L-gain-R) with C_L = 0 and (L-loc-R) with r_n = 0: BASE
`lemmas/L11_EXAMPLES.md:90-98`, with Q := ∪_{j∈S₀}G(j) (|Q| ≤ s₀ḡ ≤ K for n large) and H_l := G(l) ∪ Q, |H_l| ≤ (s₀ + 1)ḡ =: H̄_n
(bounded, so log H̄_n ≤ κ_H√log n for large n and any κ_H > 0). This is (L-R⁺⁺) with C_L = 0, and N̄_n = (1 + H̄_n)^{15} is a
constant. By (T3⁺⁺)(b)(ii) (`lemmas/R3_RATE.md` R3.5): 1 − π₀(𝓛(Q)) = O_P((|Q| + 1)N̄_n√(log n/n)) = **O_P(√(log n/n))**. Nothing
is claimed about π₀(S₀) itself (BASE `:100`). ∎
