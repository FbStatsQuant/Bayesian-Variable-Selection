# BRIDGE B3.8 — the fully orthogonal witness satisfies Theorem 1 and Theorem 3(b) (W3-PSHARP-R, post-CP3, for READER_DELTA v0.4)

Status: **PROVED (by this seat, unchecked)**. Purpose: name the cases in which the reader's Theorem 3 may say "the rate
of Theorem 1 is exact in expectation". Reader texts: W3-READER `READER_VERSIONS.md` @e20d287f, Theorem 1 (row 1.1,
§1, lines 89-112: assumptions (A1)–(A6), expectation display) and Theorem 3 (row 1.3, §3); notation
`NOTATION.md` @e20d287f line 46 (R̂_S := G_S/(n − 1), G_S := X_SᵀX_S). Master of the lower bound: `W3-PSHARP-R:AE`,
Corollary A1-E (`../../STATEMENT.md` v1.1 §3.2, lines 74-84), council R2 PASS (MANIFEST fdfd4562…). The interface-level
version of part (1) for p = min(n − 1, ⌊n^a⌋) is PARENT `Theory_work/Wave3/W3-PSHARP/lemmas/A_log_factor.md:135-137`
(Remark 2(i), inside `W3-PSHARP:A`@1.0.0, a remark, not a claim); this file states it in the reader's assumptions and
for every p.

**Setting (the fully orthogonal witness).** Fixed s₀ ≥ 1, a fixed index set S₀ of size s₀, and fixed real numbers
θ*_j ≠ 0 (j ∈ S₀), all independent of n; θ*_j = 0 for j ∉ S₀. For each n, p = p_n is any integer with
s₀ + 1 ≤ p ≤ n − 1 (bounded or growing), S₀ ⊆ [p], and X is a standardised design (centred columns, ‖x_j‖² = n − 1) with
XᵀX = (n − 1)I_p. The truth is the model (S1) with these X and θ*. (Such X exists because p ≤ n − 1: take p orthonormal
vectors of 1^⊥, of dimension n − 1, scaled by √(n − 1).)

**Claim.** For n ≥ 2s₀ + 2:
1. Theorem 1's assumptions (A1)–(A6) hold with A := 1, θ̄ := max_{j∈S₀}|θ*_j|, φ₀ := 1, g₀ := 1, and (A6) in its second form.
2. Theorem 3(b)'s assumptions hold: s₀ fixed, (N-orth), ‖Xθ*‖² ≤ nM and ‖θ*‖² ≤ nM′ with M := M′ := ‖θ*‖², and
   s₀ + 1 ≤ K := min(p, ⌊n/2⌋).
3. Consequently there are constants 0 < c ≤ C < ∞ (depending only on s₀ and θ*) and n₀ with
   c(s₀ + 1)√(log n/n) ≤ E[1 − π(S₀ | y)] ≤ C√(log n/n) for n ≥ n₀, for every such sequence p_n,
   the upper bound being Theorem 1's expectation display (with its master's status) and the lower bound Corollary A1-E.

**Proof.**
1. (A1): (S1) holds by the setting; (S2) asks 2 ≤ p ≤ n^A with A ≥ 1 fixed: p ≥ s₀ + 1 ≥ 2 and p ≤ n − 1 < n = n^1.
   (A2): s₀ ≥ 1 fixed. (A3): max_j |θ*_j| = θ̄ < ∞, fixed. (A4): for every S ⊆ [p], R̂_S = X_SᵀX_S/(n − 1) = I_{|S|}, so
   λ_min(R̂_S) = 1 ≥ φ₀² = 1, in particular for |S| ≤ 2(A + 1)s₀ + 2. (A5): for every nonempty S ⊆ [p],
   λ_min(X_SᵀX_S) = n − 1 ≥ 2 > g₀ = 1, in particular for |S| ≤ 3(A + 1)(s₀ + 1) log n. (A6), second form:
   θ*_min := min_{j∈S₀}|θ*_j| > 0 is fixed, so θ*_min√(n/log n) → ∞.
2. (N-orth): all columns are mutually orthogonal, so the columns outside S₀ are mutually orthogonal and orthogonal to
   those in S₀. ‖Xθ*‖² = θ*ᵀXᵀXθ* = (n − 1)‖θ*‖² ≤ n‖θ*‖². ‖θ*‖² ≤ n‖θ*‖² (n ≥ 1). K ≥ s₀ + 1: p ≥ s₀ + 1, and
   ⌊n/2⌋ ≥ s₀ + 1 for n ≥ 2s₀ + 2.
3. Upper bound: by 1, Theorem 1 applies at every n ≥ its n₀ (its constants depend only on (s₀, A, σ*², θ̄, φ₀, g₀) and,
   for the second form of (A6), on the divergence of θ*_min√(n/log n), here fixed by θ*). Lower bound: by 2 and bridge
   B3.3 ((N-orth) with all nulls gives the orthogonal witness hypothesis with (log p)² = o(n), since p ≤ n), Corollary
   A1-E applies with N = p − s₀ ≥ 1: liminf E[1 − π(S₀ | y)]/Λ^E_n ≥ 1, where
   Λ^E_n = (s₀ + 1)f_p√(ℓ_n/(πn)), f_p := 2(p − s₀)/(2p − 1 − s₀), ℓ_n := log(p√n/(s₀ + 1)) ≥ ½ log n (as s₀ + 1 ≤ p).
   For s₀ ≥ 1 and p ≥ s₀ + 1, (s₀ + 1)f_p ≥ 2, because (s₀ + 1)(p − s₀) − (2p − 1 − s₀) = (s₀ − 1)(p − s₀ − 1) ≥ 0. Hence
   Λ^E_n ≥ 2√(log n/(2πn)) = (2/√(2π))√(log n/n), and for n large E[1 − π(S₀ | y)] ≥ (1/√(2π))√(log n/n)
   = c(s₀ + 1)√(log n/n) with c := 1/((s₀ + 1)√(2π)). If moreover s₀ ≤ p/2, then f_p ≥ p/(2p) = ½, so Λ^E_n ≥ ½(s₀ + 1)√(log n/(2πn)), and for n large
   E[1 − π(S₀ | y)] ≥ c(s₀ + 1)√(log n/n) with c := 1/(4√(2π)), not depending on s₀. ∎

**Remarks.** (i) Every p with s₀ + 1 ≤ p ≤ n − 1 is covered, bounded p included; p is capped at n − 1 by the existence
of the design. (ii) The Gaussian witness (raw i.i.d. N(0, 1) columns) is **not** covered in expectation: the reader's
random-design theorem (Theorem 2) has an in-probability conclusion only. In probability the two named sequences of the
current reader text (fully orthogonal with p = min(n − 1, ⌊n^a⌋); raw Gaussian with p = ⌊n^a⌋; fixed nonzero
coefficients) keep their reading "exact when log p ≍ log n, conditional on Theorems 1 and 2" (PARENT STATEMENT :79-85).
(iii) Statuses are not changed by this bridge: the upper half carries Theorem 1's master status (row 1.1).
