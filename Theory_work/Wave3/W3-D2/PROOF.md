# W3-D2 — PROOF of Theorem 2X and Corollary 2X (v1.0, 2026-11-17)

Status: **PROVED (by this seat, unchecked)**, conditional as carried from `W3-MISR-R:CorGb-plus@1.0.1` (STATEMENT §5).
Statement: `STATEMENT.md` v1.1 (locked) §§0–3; clause (E) is the explicit form of §1. Aliases as there. Every step is either a citation (file:line, id@version) or
elementary; no new estimate.

## P0. Deterministic facts (STATEMENT §3)

Fix a data set with y^r non-constant; write π for π(· | X^r, y^r) and δ := 1 − π(S₀) (δ = 1 if S₀ ∉ Ω).
1. *PIP error.* For j ∈ S₀: 1 − PIP_j = π(S ∌ j) ≤ π(S ≠ S₀) = δ. For j ∉ S₀: PIP_j = π(S ∋ j) ≤ π(S ≠ S₀) = δ.
   So max_j |PIP_j − 1{j ∈ S₀}| ≤ δ.
2. *HPM.* If HPM = T ≠ S₀, then π(T) ≥ π(S₀) = 1 − δ (T maximises π) and π(T) ≤ π(S ≠ S₀) = δ; so δ ≥ ½.
3. *MPM.* MPM = {j : PIP_j > ½}. If MPM ≠ S₀, either some j ∈ S₀ has PIP_j ≤ ½, so δ ≥ 1 − PIP_j ≥ ½ by 1, or some
   j ∉ S₀ has PIP_j > ½, so δ ≥ PIP_j > ½ by 1. Either way δ ≥ ½.
(Item 1 is [MISR] MIS-R (i) consequence 1, `:118-119`, "for every data set".) Under the model of STATEMENT §0, y^r is
non-constant almost surely (σ² > 0, n ≥ 2), so P0 holds almost surely.

## P1. Theorem 2X is an instance of CorGb-plus

Map STATEMENT §0 to the setting of [MISR-R] §3 (`:96-100`) with candidate set 𝒞 := [p] and **no omitted columns**:
- q := 0, X^r_𝓜 the n × 0 matrix, β_𝓜 ∈ ℝ⁰, so X^r_𝓜β_𝓜 = 0 ∈ ℝⁿ; X^r_𝒞 := X^r, β_𝒞 := β, m_𝒞 := m, Σ_𝒞𝒞 := Σ;
  α as in §0 (deterministic; [MISR-R] §2 allows any real random variable, `:51-54`).
- **(N)** ([MISR-R] `:56`): ε ~ N_n(0, σ²I_n), σ² deterministic, independent of (X^r_𝒞, X^r_𝓜) = (X^r, empty) — this is §0.
- **(OV)** ([MISR-R] `:67-68`) with the deterministic choices a := 0, γ := 0, τ² := 0: conditionally on X^r,
  X^r_𝓜β_𝓜 = 0 has law δ₀ = N_n(0·1 + X^r·0, 0·I_n) (N_k(m, 0) := δ_m, [MISR-R] `:31`). So (OV) holds; a, γ, τ² are
  deterministic as [MISR-R] `:97-98` requires.
- Then β^𝒞 = β_𝒞 + γ = β, σ²_𝒞 = σ² + τ² = σ² > 0, supp β^𝒞 = S₀, s = s₀, and
  π_𝒞(· | X^r_𝒞, y^r) = π(· | X^r, y^r): both are the coded target of [W3P] §0 computed from the same (X^r, y^r)
  ([MISR] §0 `:20-22`: "π_𝒞(· | x, y^r) is the coded target of [W3P] §0 (lines 16-29) computed from (x, y^r)").
  So CorGb-plus's δ_n = 1 − π_𝒞(supp β^𝒞 | X^r_𝒞, y^r) is STATEMENT's δ_n, and its HPM is STATEMENT's HPM.
- Rows: i.i.d. N_p(m, Σ) with Σ_jj > 0 ([MISR-R] `:96`) — §0. "Everything may depend on n" ([MISR-R] `:99`) — §0.

Hypotheses of CorGb-plus ([MISR-R] `:100-104`), with c_R := c:
- 2 ≤ p ≤ n^A: (A1). s := |supp β^𝒞| = s₀ ≥ 1 fixed: (A1) and the fixed s₀ of STATEMENT §1.
- *Floor.* CorGb-plus asks λ_min(R_TT) ≥ c_R for every T ⊆ 𝒞 with |T| ≤ k_n := s + max(j₀, m♯_n). For n ≥ max(3, 2s₀)
  we have s₀ ≤ K = min(p, ⌊n/2⌋) (p ≥ s₀ because S₀ ⊆ [p]), so `W3-READER:R1@1.0.2` B4.1 ([R1] `:43-45`, valid for
  s ≤ K, n ≥ 3, A ≥ 1, s ≥ 1, with p = |𝒞| = p) gives k_n ≤ 3(A + 1)(s₀ + 1) log n. Every non-empty T with |T| ≤ k_n is
  therefore covered by (A2). (Empty T does not arise: CorGb-plus's proof uses non-empty T only, `lemmas/G2_corr.md`
  step 2; if the floor is read for T = ∅ it is vacuous.)
- *Energy.* β^𝒞ᵀΣ_𝒞𝒞β^𝒞 = βᵀΣβ ≤ M₀σ² = M₀σ²_𝒞: (A3).
- *Beta-min.* ρ_n^{BM} = n·min_{j∈S₀} Σ_jjβ_j²/(σ² log n) = ρ_n → ∞ by (A3); this is the "→ ∞" branch named at
  [MISR-R] `:104` ("in particular if ρ_n^{BM} → ∞"), which satisfies liminf ρ_n^{BM} > 16c₀(s, A)/c_R.

Conclusion of CorGb-plus ([MISR-R] `:104-107`): there are n* and C such that for every n ≥ n*,
  E δ_n ≤ C r_n + (2 + 2k_n)n^{−2} + n^{−1} = b_n,  P(HPM ≠ S₀) ≤ 2C r_n + (2 + 2k_n)n^{−2} + n^{−1} ≤ 2b_n.
C is the constant of MIS-R (i) on 𝒦^λ_n(s, A, 2M₀ + 1, (c_R/8)^{1/2}, C_OS, c′), C_OS = C_OS(s, A) from the bridge
(F_w; 1) ⇒ (OS) and c′ = c₀(s, A) + 1 on the → ∞ branch (`lemmas/G2_corr.md`, [R-3]): it depends only on (s₀, A, M₀, c).
n* depends on the sequence. (Take n* ≥ max(3, 2s₀) as well, for the floor step above.)

## P2. The remaining displays of Theorem 2X

By P0.1, E max_j |PIP_j − 1{j ∈ S₀}| ≤ E δ_n ≤ b_n. By P0.3 and Markov, P(MPM ≠ S₀) ≤ P(δ_n ≥ ½) ≤ 2E δ_n ≤ 2b_n
(P0.2 gives the same bound for the HPM, consistent with P1). Finally k_n ≤ 3(A + 1)(s₀ + 1) log n (P1), so
(2 + 2k_n)n^{−2} = O(log n/n²) and n^{−1} = o(r_n); hence b_n = O(r_n). ∎ (Theorem 2X)

## P3. Corollary 2X

Assume the recorded hypotheses (STATEMENT §2). Then the §0 setting holds with m := m_n, Σ := Σ_n (Σ_jj = 1 > 0),
σ² := σ*² > 0, α := α*, β := β* (deterministic: the model of `Theory_work/Wave3/W3-READER/NOTATION.md:15-20`).
- (A1): (S2) and s₀ ≥ 1.
- (A2) with c := φ²: R = Σ_n (unit diagonal), and every T with 1 ≤ |T| ≤ 3(A + 1)(s₀ + 1) log n also has
  |T| ≤ 5(A + 1)(s₀ + 1) log n, where the recorded floor gives λ_min(Σ_{n,T}) ≥ φ². (If the recorded floor is asked only on
  |S| ≤ 3(A + 1)(s₀ + 1) log n, this is (A2) directly.)
- (A3), energy: βᵀΣ_nβ = β_{S₀}ᵀ(Σ_n)_{S₀S₀}β_{S₀} ≤ λ_max((Σ_n)_{S₀S₀})‖β_{S₀}‖² ≤ tr((Σ_n)_{S₀S₀})·s₀b_hi² = s₀²b_hi²
  (a positive semidefinite matrix has λ_max ≤ trace; the trace of an s₀ × s₀ correlation block is s₀). So
  βᵀΣ_nβ ≤ M₀σ*² with M₀ := s₀²b_hi²/σ*², fixed.
- (A3), beta-min: ρ_n = n·min_{j∈S₀}β_j²/(σ*² log n) ≥ n b_lo²/(σ*² log n) → ∞.
So Theorem 2X applies. Its displays give the recorded conclusions: δ_n ≥ 0 and E δ_n = O(r_n) give δ_n = O_P(r_n)
(Markov: P(δ_n > L r_n) ≤ E δ_n/(L r_n)); P(HPM ≠ S₀) + P(MPM ≠ S₀) = O(r_n) → 0 gives P(HPM = MPM = S₀) → 1; the PIP
error is ≥ 0 with expectation O(r_n), hence O_P(r_n). ∎ (Corollary 2X)

## P4. What the proof does not use

No upper eigenvalue bound on Σ; no condition on m or α; no fixed σ², Σ or β (only the fixed constants A, s₀, c, M₀ and
ρ_n → ∞); no Gaussianity beyond the rows and the noise (both used only through CorGb-plus).
