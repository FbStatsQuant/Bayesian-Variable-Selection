# W3-PSHARP-R — PLAN (v1.1, 2026-11-15; v1.1 = L01 amendments)

Targets: BRIEF.md §Targets 1–2 (T12 of `API_AUDIT/sharp2/TRIAGE.md`). Delta statement: `STATEMENT.md` v1.0. Tier B,
NORMAL mode. No new key lemma: the route is the one named in the brief (truncate at T = ϵ/c_n; Var ≤ T·E), on top of
PARENT's checked steps. Kill budget 3 per lemma.

## 1. Files
- `lemmas/AE_expectation.md` (new) — Proposition A-E, Corollaries A1-E, A2-E.
- `lemmas/A2C_critical.md` (new) — Proposition A2C.
- PARENT steps consumed unchanged are cited by `file:line` (STATEMENT §6); no PARENT lemma is copied unless a step
  changes (then `[R-#]` marks).

## 2. Proof routes

### 2.1 Lemma T (abstract truncated-expectation inequality; new, ~10 lines)
Let odds ≥ Y := c Σ_{j=1}^N U_j 1_{G_j}·e^{−e} with c, e ≥ 0 deterministic, 0 ≤ U_j ≤ T, the U_j independent and
identically distributed, and U_j independent of G_j [orth] (or all U_j jointly independent of one event G = G_j [sph]).
Then, with δ = odds/(1 + odds) and x/(1+x) ≥ x − x²:
  E δ ≥ E Y − E Y²,  E Y = e^{−e}·c E U·Σ_j P(G_j) ≥ e^{−e}·c N E U·min_j P(G_j),
  E Y² ≤ c²(N·T·E U + N²(E U)²)   (drop the indicators; U² ≤ T U; the U_j independent)  [L01-F2].
With c > 0, T := ϵ/c > 0: E δ ≥ L·(e^{−e}·min P(G_j) − ϵ − L), L := cN E U.

### 2.2 (W-orth)
PARENT §3 (`A_log_factor.md:53-63`): νγ_j = κ_n g_j²/2, κ_n ≥ (n−1)σ*²/V, V ≤ σ*²E(1 + 0.04/(n−1)) + 1.06M + M′,
E = ‖Cε‖²/σ*². **Decoupling:** E = g_j² + R_j with R_j := ‖(C − u_ju_jᵀ)ε‖²/σ*² ~ χ²_{n−2} independent of g_j.
U_j := e^{g_j²/2}1{g_j² ≤ 2 log T}, G_j := {R_j ≤ (n−2) + x√(2(n−2))} (Chebyshev: P(G_jᶜ) ≤ x⁻²). On
{U_j > 0} ∩ G_j: 1 − κ_n ≤ e_n := x√(2/(n−1)) + 2.1 log T/(n−1) + O((1 + (M+M′)/σ*²)/n), so
e^{νγ_j} ≥ e^{−e_n log T}U_j. Lemma S(4) ⇒ odds ≥ c_n Σ_{j∈𝒩} e^{νγ_j} ≥ Y. E U = 2√(log T/π) exactly (Lemma W(i),
`:22-23`, with N replaced by T). Cross terms: g_j ⟂ g_k. Choose x = x_n → ∞ with x_n log T/√n → 0, possible as
log T ≤ log p + ½ log n + log 2 = o(√n).

### 2.3 (W-sph)
PARENT §4 (`:75-99`): conditionally on ε the ζ_j are iid with a fixed law ⇒ (ζ_j)_j independent of ε. The ε-event
G := {E ≤ 2(n−1)} ∩ {E₂ ≥ m/2} ∩ {E₁ ≤ x(r₀+1)}, P(Gᶜ) ≤ 2/(n−1) + 16/n + 1/x; on G, 1 − κ′_n ≤ (C₀ + 2x(r₀+1))/n.
U_j := e^{ζ_j/2}1{ζ_j ≤ 2 log T}. Sphere law (Lemma W(ii)(a)-(b), `:26-37`, with τ := 2 log T ≤ d/2):
2√(log T/π)(1 − 1/d)e^{−2(log T)²/d} ≤ E U ≤ 2√(log T/π)e^{3 log T/d}, d = n − 1. Need (log T)² = o(n) and
(r₀+1) log T = o(n): from (W-sph-E).

### 2.4 From L to Λ^E
log T = ℓ_n + log(ϵ′(2p − 1 − s₀)/p), (2p − 1 − s₀)/p ∈ [1, 2), ℓ_n ≥ ½ log n ⇒ L = (1 + o(1))Λ^E_n uniformly
(both witnesses). Absorb: if Λ^E ≥ 1 − ϵ the claim is trivial; otherwise take ϵ′ = ϵ/2 and n ≥ n₀ so that all (1 + o(1))
factors sit inside the slack ϵ/2. Random (X_{S₀}, θ*): condition, multiply by P(𝒜_n).

### 2.5 Corollaries
- A1-E: s₀ fixed, N = p − s₀; Λ^E → 0 (ℓ_n = o(n)); constants: ℓ_n = (a + ½)log n + O(1) for p = n^a; ℓ_n = ½ log n + O(1)
  for fixed p.
- A2-E: sub-block argument. Any 𝒩′ ⊆ 𝒩 satisfies the same witness hypotheses (stated through p, not N). Per-column
  increment of Λ^E is Δ_n = 2c_n√(ℓ_n/π) ≤ 2√(ℓ_n/(πn)) → 0 (s₀ ≤ p/2 ⇒ (s₀+1)/(2p−1−s₀) ≤ 1). Pick |𝒩′| with
  Λ^E(𝒩′) ∈ [min(Λ^E, ¼) − Δ_n, min(Λ^E, ¼)]; Prop A-E with ϵ = ½ ⇒ E δ_n ≥ ¼(min(Λ^E_n, ¼) − Δ_n) (if only |𝒩′| = 0
  fits, the right side is ≤ 0 and δ_n ≥ 0 suffices [L01]). (W-sph) without the rank condition: E δ_n → 0 and PARENT B1
  (δ_n ≥ (s₀+1)/(3√n + s₀ + 1) surely) give s₀ = o(√n), hence (r₀+1) log(pn) = o(n), then apply A-E [L01-F3]. (i) follows; (ii):
  then liminf E δ_n/Λ^E_n ≥ 1, 2N/(2p−1−s₀) ≥ ½, ℓ_n ≥ ½ log n ⇒ s₀ + 1 = O(1).

### 2.6 A2C (W-orth, multi-step; new, ~1 page)
For J ⊆ 𝒩, |J| = j, s₀ + j ≤ K: every added column is ⟂ col X_{S₀∪J′}, so by Lemma S(1) (equality case) and S(2)
D_{S₀∪J}/D_{S₀} = n^j and Q_{S₀} − Q_{S₀∪J} = Σ_{k∈J}(x_kᵀy)²/n (additive). Hence
π(S₀∪J)/π(S₀) = [w(s₀+j)/w(s₀)] n^{−j/2}(1 − Σ_J γ_k)^{−ν} ≥ (c_n)^j Π_{k∈J} e^{νγ_k}  (prior ratio = Π_{i<j}(s₀+1+i)/(2p−1−s₀−i) ≥ P_n^j).
So odds ≥ Σ_{j=1}^{J₀} c_n^j e_j(e^{νγ}). On PARENT's κ-event (Lemma R proof `:46`): e^{νγ_k} ≥ e^{−ϵ/2}W_k, W_k ≤ N.
Newton-type bound j! e_j ≥ A^j − C(j,2)B A^{j−2} with A = c_nΣW, B = c_n²ΣW² ≤ (c_nN)A, c_nN ≤ (s₀+1)/√n → 0 when Λ_n
bounded. Lemma W: P(A ≥ (1−ϵ)Λ_n) → 1, E A = Λ_n. Fix J₀ large for the given η, then ϵ small, n large: odds ≥
e^λ − 1 − η w.p. → 1 (no growing-j estimate needed [L01]); expectation consequence by boundedness [L01-F4]. Needs
K − s₀ → ∞ (s₀ = O(√n) from Λ_n bounded, p − s₀ → ∞).

## 3. Numerics
- N1 (done, lead): `numerics/ae_fixed_p.py` — exact orthogonal design, p ∈ {2, 3, 5}, n ≤ 10⁶: E δ_n/Λ^E_n → 0.99–1.03.
  This is the boundary experiment for the dropped hypothesis N_n → ∞ (bounded N) and the end-to-end check of A1-E(b).
- N2 (optional, ≤ 30 min, Sonnet helper or lead): A1-E(a) on the orthogonal design with p = n − 1 (exact odds via the
  PARENT DP `numerics/a_orth.py:36`, importance sampling over the null scores), constant √(1.5/π).
- N3 (optional): A2C — π(S₀) against e^{−λ} at s₀ ≈ λ√(πn/log p) on the orthogonal design (PARENT `a_orth.py` E2).

## 4. Reviews (NORMAL mode; Sol = codex gpt-6.1-sol, high)
1. L01 statement lock (Sol, fresh, blind) — now.
2. CP1 → manager.
3. L02 line check (Sol, new agent): `AE_expectation.md` + `A2C_critical.md` in one batch (2 lemmas).
4. Citecheck (copy of PARENT `citecheck.py`, pointed at this folder), 0 MISS.
5. Council R1: Sol seat + Opus 5.5 high seat (Claude Third), fresh, blind; manifest frozen when DEPS all OK.
6. CP3.

## 5. Hours and dates (cut-off CP3 Wed 2026-11-18 18:00 CT)
| step | hours | when |
|---|---|---|
| PLAN, STATEMENT, TARGET, READER_DELTA, N1, L01 lock, CP1 | 1.5 | Sun 11-15 evening |
| AE_expectation.md | 1.0 | after CP1 go (Mon 11-16) |
| A2C_critical.md (droppable to a named open item if it stops being a restatement) | 0.75 | Mon 11-16 |
| L02 line check + repairs | 0.5 (+ wait) | Mon 11-16 |
| REPORT, DEPS, citecheck, council R1 (+ diff round if needed) | 1.0 (+ wait) | Tue 11-17 |
| CP3 | 0.25 | Tue 11-17, latest Wed 11-18 18:00 |
Total lead time ≈ 4–5 h; within the brief's 3–4 h for the claims, plus review waits.
