# B3w — the events of W3-POST Theorem 1 item 6 under (A1)–(A4) of Theorem 2SG

**Status: PROVED (by this seat, unchecked).** Ticket W3-D3 (Tier B rider). Target: `STATEMENT.md` §2 (v1.0).
This file is a copy of `Theory_work/Wave3/W3-DIST/work/E_bridges/B3.md` (`W3-DIST:B3@1.0.1`, "PROVED-CHECKED, conditional
on W3-POST:Thm-1 (for its last sentence); council R2, …"; its amendments A-1, A-2 included) with the window changed.
Changed or new lines are marked **[R-#]**; unmarked steps are B3's argument specialised to the present setting.
Numerical check of the size arithmetic: `numerics/N1_window.py` → `numerics/N1_out.txt`.

Aliases: [EB] = `Theory_work/Wave3/W3-DIST/work/E_bridges/`; [W3P] = `Theory_work/Wave3/W3-POST/STATEMENT.md`;
[R1] = `Theory_work/Wave3/W3-READER/lemmas/R1_set_sizes.md`.

## Statement

Assume (A1)–(A4) of `STATEMENT.md` §1: rows x_1, …, x_n of X^r i.i.d. copies of x ∈ ℝ^p with E x = m_n, Cov(x) = Σ_n a
correlation matrix; (S1), (S2); s₀ ≥ 1 fixed, b_lo ≤ |β*_j| ≤ b_hi on S₀ = supp β*; λ_min(Σ_{n,S}) ≥ φ² for |S| ≤ W̄_n;
E exp(λuᵀ(x − m_n)) ≤ exp(K²λ²uᵀΣ_nu/2) for all λ and all u with at most W̄_n nonzero entries, where
  **[R-1]** W̄_n := 5(A + 1)(s₀ + 1) log n,  q_n := ⌊W̄_n⌋,  w_n := min{p, q_n}  (replaces B3's q_n = min{p, ⌈C_q log n⌉}).
By [EB]`B0.md` work in the unit-noise model (α* = 0, σ* = 1, coefficients β̃* := β*/σ*; S₀ unchanged; all interface
constants in units of σ*²). Let 𝒜_n := 𝓔₁ ∩ 𝓔₂(q_n) ([EB]`B1.md`, [EB]`B2core.md`). Put
  **[R-2]** M_E := 2s₀²b_hi²/σ*²,  φ₀² := φ²/4,  g₀ := φ²/8,  M_n := b_lo²nφ²/(8σ*² log n),  j₀ := ⌈(2A + 1)s₀⌉ + 1,
and m♯_n as in [W3P] `:36-37` (computed with p_ret and s₀). **[R-3]** Let n₁ = n₁(s₀, A, K) be the least integer
n₁ ≥ max(3, 2s₀) such that W̄_n(1 + A log n) ≤ c₂n/K⁴ for every n ≥ n₁ (c₂ = 10⁻⁵; n₁ is finite because the left side
is O((log n)²)). For n ≥ n₁, on 𝒜_n:
(i) p_ret = p ≥ 2 (no column of X^r is constant in the sample), |supp θ̃*| = s₀ and s₀ ≤ K = min(p, ⌊n/2⌋).
(ii) (E; M_E): ‖μ̃‖² ≤ nM_E.
(iii) (F_λ; φ₀) of [W3P] `:68-70`: λ_min(X_{S₀∪J}ᵀX_{S₀∪J}/(n − 1)) ≥ φ₀² for every J ⊆ [p]∖S₀ with |J| ≤ j₀; 0 < φ₀ ≤ ½.
(iv) (F_w; g₀) of [W3P] `:71-73`: λ_min(X_{S₀∪J}ᵀX_{S₀∪J}) ≥ g₀ for every J ⊆ [p]∖S₀ with |J| ≤ m♯_n.
(v) BM-∞ with a common deterministic envelope: θ̃*²_min nφ₀²/log n ≥ M_n, and M_n → ∞.
(vi) P(𝒜_nᶜ) ≤ 4p·e^{−c₁n/K⁴} + e^{−c₂n/K⁴} ≤ 5n^A e^{−c₂n/K⁴} → 0 (c₁ = 1/576).
Consequently the hypotheses of [W3P] Theorem 1 item 6 (`:95-100`) hold for the unit-noise model with the
(X, θ̃*)-measurable events 𝒜′_n ⊇ 𝒜_n of Step 6, common constants (M_E, φ₀, g₀) and the common envelope M_n.

## Inherited results used (statuses verbatim; registry at main 029bb748)
- [EB]`B0.md` (`W3-DIST:B0@1.0.1`), [EB]`B1.md` (`W3-DIST:B1@1.0.1`), [EB]`B2core.md` (`W3-DIST:B2core@1.0.1`),
  [EB]`B2.md` part (a) (`W3-DIST:B2@1.0.1`): each "PROVED-CHECKED; council R2, MANIFEST 9719c817… (= R2 c5cd9cdd re-frozen
  CITATION-ONLY as R2r), astra=9.3 PASS, opus=9.2 PASS". Statements used verbatim:
  B1: "(SG₁) E exp(λz_j) ≤ exp(K²λ²/2) … (a) K ≥ 1, and for n ≥ 3: P(𝓔₁ᶜ) ≤ 4p·exp(−c₁n/K⁴) with c₁ = 1/576. (b) On 𝓔₁ no
  column is constant in the sample: p_ret = p, … S₀ = supp β* … (c) Suppose in addition |supp β*| ≤ s and
  |β*_j|·sd(x_j) ≤ b̄σ* for every j … On 𝓔₁: ‖μ‖² ≤ … n·(2s²b̄²)σ*²", with 𝓔₁ := {½ ≤ ŝ_j²/Var(x_j) ≤ 2 for every j ≤ p}.
  B2-core: "(SG_q) … 𝓔₂(q) := {n⁻¹Σ_i(a + uᵀz_i)² ≥ ½(a² + Var(uᵀz)) for all a ∈ ℝ and all u with at most q nonzero
  entries}. If q′·log(ep/q′) ≤ c₂n/K⁴ with c₂ = 10⁻⁵, then P(𝓔₂(q)) ≥ 1 − exp(−c₂n/K⁴). On 𝓔₂(q), for every u with at most
  q nonzero entries, uᵀΣ̂^z u ≥ ½uᵀΓu" (q′ := min(q, p); z_i := x_i − m_n here, Γ = Σ_n).
  B2 (a): under (SG_q) and "(A4_q) λ_min(Corr(x_T)) ≥ c_ψ/n for every T ⊆ [p] with 1 ≤ |T| ≤ q", "on 𝓔₁ ∩ 𝓔₂(q):
  (a) λ_min(G_T) ≥ c_ψ/4 ≥ g₀ for every T with 1 ≤ |T| ≤ q", g₀ := c_ψ/8; and its proof identity G_T = n·Λ_TΣ̂^z_TΛ_T,
  Λ_T = diag(sd(x_j)/ŝ_j : j ∈ T) ([EB]`B2.md:45-55`).
- [R1] (`W3-READER:R1@1.0.2`, "PROVED-CHECKED; council R3, …"): **[R-4]** B1.2 "s + j₀ ≤ (2A + 2)s + 2" (`:15-17`) and
  B1.3 "For s ≤ K: s + m♯_n ≤ 3(A + 1)(s + 1) log n" (`:19-31`), both for n ≥ 3, A ≥ 1, s = s₀ ≥ 1, p ≤ n^A.
- Definitions of (E), (F_λ), (F_w), (BM), R1, item 6: [W3P] `:63-75, 95-100` (definitions only); the consumed theorem
  `W3-POST:Thm-1@1.0.1` is applied in `ASSEMBLY.md`, not here.

## Proof

**Step 0 [R-5] (sizes covered by the window).** Let n ≥ 3. *Claim:* every set S₀ ∪ J ⊆ [p] with |J| ≤ j₀, and every set
S₀ ∪ J ⊆ [p] with |J| ≤ m♯_n when s₀ ≤ K and p_ret = p, has size ≤ w_n.
(1) By [R1] B1.2, |S₀ ∪ J| ≤ s₀ + j₀ ≤ (2A + 2)s₀ + 2. And (2A + 2)s₀ + 2 ≤ W̄_n: since log n ≥ log 3 > 1.0986,
W̄_n ≥ 5.49(As₀ + A + s₀ + 1) ≥ 2As₀ + 2s₀ + 2 (coefficient by coefficient; A ≥ 0). The left side is an integer, so it
is ≤ ⌊W̄_n⌋ = q_n; and |S₀ ∪ J| ≤ p as a subset of [p]. Hence |S₀ ∪ J| ≤ w_n.
(2) By [R1] B1.3 (its hypotheses: s₀ ≥ 1, s₀ ≤ K, p ≤ n^A for the dimension p = p_ret in which m♯_n is computed),
s₀ + m♯_n ≤ 3(A + 1)(s₀ + 1) log n ≤ W̄_n, so s₀ + m♯_n ≤ q_n (integer), and |S₀ ∪ J| ≤ min{p, s₀ + m♯_n} ≤ w_n. ∎
Also W̄_n ≥ 1, so (A4) contains every u = e_j, and W̄_n ≥ |S₀| = s₀.

**Step 1 [R-6] (the hypotheses of B1 and B2-core).** Put z := x − m_n, z_i := x_i − m_n. Then E z = 0, Var(z_j) = Σ_{n,jj} = 1,
Γ := E zzᵀ = Σ_n, Var(uᵀz) = uᵀΣ_nu, and z_j = (x_j − E x_j)/sd(x_j). (A4) with u = e_j (one nonzero entry ≤ W̄_n) is (SG₁) of
B1 with the same K. (A4) restricted to u with at most q_n ≤ W̄_n nonzero entries is (SG_{q_n}) of B2-core. For n ≥ n₁:
q′ := min(q_n, p) = w_n ≥ 1, and log(ep/w_n) ≤ 1 + log p ≤ 1 + A log n (w_n ≥ 1, p ≤ n^A), so
w_n log(ep/w_n) ≤ W̄_n(1 + A log n) ≤ c₂n/K⁴, which is B2-core's size condition. ∎

**Step 2 ((i) and (ii)).** On 𝓔₁ ([EB]`B1.md` (b)): p_ret = p ≥ 2 by (S2), and θ̃*_j = ŝ_jβ̃*_j with ŝ_j > 0, so
supp θ̃* = supp β* and |supp θ̃*| = s₀. K = min(p, ⌊n/2⌋) ≥ s₀ because p ≥ s₀ and ⌊n/2⌋ ≥ s₀ for n ≥ 2s₀ (n ≥ n₁).
(ii) [R-7]: (A5) of B1 (c), |β̃*_j|·sd(x_j) ≤ b̄·1, holds with b̄ := b_hi/σ* (sd(x_j) = 1; β̃*_j = 0 off S₀); with
|supp β̃*| ≤ s₀, B1 (c) gives ‖μ̃‖² ≤ n·2s₀²b̄² = nM_E. ∎

**Step 3 [R-8] ((iii)).** Let T = S₀ ∪ J, J ⊆ [p]∖S₀, |J| ≤ j₀. By Step 0 (1), |T| ≤ w_n ≤ W̄_n, so (A3) gives
λ_min(Σ_{n,T}) ≥ φ². As in [EB]`B2.md` (a), G_T = n·Λ_TΣ̂^z_TΛ_T with Λ_T = diag(1/ŝ_j : j ∈ T) (sd(x_j) = 1). For u ∈ ℝ^T put
ũ := Λ_Tu, which (padded by zeros) has at most |T| ≤ q_n nonzero entries. On 𝓔₂(q_n) and 𝓔₁ (ŝ_j² ≤ 2):
  uᵀG_Tu = n·ũᵀΣ̂^z_Tũ ≥ (n/2)ũᵀΣ_{n,T}ũ ≥ (n/2)φ²‖ũ‖² = (nφ²/2)Σ_{j∈T}u_j²/ŝ_j² ≥ (nφ²/4)‖u‖².
So λ_min(G_T/(n − 1)) ≥ nφ²/(4(n − 1)) ≥ φ²/4 = φ₀² (T = S₀ included). φ ∈ (0, 1] gives φ₀ ∈ (0, ½]. ∎

**Step 4 [R-9] ((iv)).** (A4_{q_n}) of B2 holds with c_ψ := φ²: for 1 ≤ |T| ≤ q_n ≤ W̄_n, (A3) gives
λ_min(Corr(x_T)) = λ_min(Σ_{n,T}) ≥ φ² ≥ φ²/n. B2's other hypotheses: 2 ≤ p, Var(x_j) = 1 ∈ (0, ∞), (SG_{q_n}) (Step 1).
For J ⊆ [p]∖S₀ with |J| ≤ m♯_n, on 𝒜_n (where s₀ ≤ K and p_ret = p, Step 2), |S₀ ∪ J| ≤ w_n ≤ q_n (Step 0 (2)) and
|S₀ ∪ J| ≥ s₀ ≥ 1, so B2 (a) gives λ_min(G_{S₀∪J}) ≥ c_ψ/4 = φ²/4 ≥ φ²/8 = g₀. ∎
*Remark.* m♯_n depends on (n, p_ret, s₀) only ([W3P] `:36-37`: "data-free"), so (F_w; g₀) is a statement about X alone.

**Step 5 [R-10] ((v)).** In the unit-noise model θ̃*_j = ŝ_jβ*_j/σ* ([EB]`B0.md` (f)). On 𝓔₁, ŝ_j² ≥ Var(x_j)/2 = ½, so for
j ∈ S₀, by (A2), θ̃*_j² ≥ b_lo²/(2σ*²). Hence θ̃*²_min nφ₀²/log n ≥ (b_lo²/(2σ*²))·n·(φ²/4)/log n = M_n, a deterministic
sequence, and M_n → ∞ because b_lo, φ, σ*² are fixed and positive. (In the unit-noise model σ*² = 1 in item 6's (BM).) ∎

**Step 6 (item 6's events; (vi)).** [W3P] `:95-98` asks for "(X, θ*)-measurable events 𝒜_n with P(𝒜_n) → 1 on which
|supp θ*| = s₀ and (E), (F_λ), (F_w) hold with common constants (M, φ₀, g₀) and (BM) holds with … a common deterministic
envelope M_n → ∞", in regime R1 (`:63-64`: s₀ ≥ 1 fixed, 2 ≤ p ≤ n^A, s₀ ≤ K eventually, σ*² > 0 fixed, G) with ε
independent of (X, θ*). Define 𝒜′_n as the set of outcomes on which p_ret = p and (X, θ̃*) satisfies: |supp θ̃*| = s₀,
‖Xθ̃*‖² ≤ nM_E, (F_λ; φ₀), (F_w; g₀) (m♯_n computed from (n, p, s₀)), and θ̃*²_min nφ₀²/log n ≥ M_n. Each condition is a
finite collection of inequalities between Borel functions (norms, smallest eigenvalues of Gram submatrices, the indicator
of a column being constant) of the raw design, indexed by the finitely many subsets of [p]; so 𝒜′_n is measurable with
respect to the raw design. By Steps 2–5, 𝒜_n ⊆ 𝒜′_n (μ̃ = Xθ̃*) for n ≥ n₁. R1 holds: s₀ ≥ 1 fixed by (A2); 2 ≤ p ≤ n^A by
(S2); s₀ ≤ K for n ≥ 2s₀ on {p_ret = p}; σ*² = 1 ([EB]`B0.md` (e)); G: ε/σ* ~ N(0, I_n) independent of the raw design
(S1), and θ̃* = D_xβ̃* is raw-design-measurable. *Dimension (B3 amendment A-2, unchanged):* to apply the consumed theorem in
the fixed dimension p, outside {p_ret = p} the retained standardised design and truth are replaced by a fixed admissible
n × p design and truth (a function of the raw design only, hence independent of the noise); the replacement agrees with
the actual objects on {p_ret = p} ⊇ 𝓔₁, so conclusions transfer to the actual posterior with an added error at most
P(p_ret ≠ p) ≤ P(𝓔₁ᶜ) → 0 (used in `ASSEMBLY.md` Step 3).
*(vi).* For n ≥ n₁ (≥ 3), Step 1 and B1 (a), B2-core give P(𝒜_nᶜ) ≤ P(𝓔₁ᶜ) + P(𝓔₂(q_n)ᶜ) ≤ 4pe^{−c₁n/K⁴} + e^{−c₂n/K⁴} ≤
5n^Ae^{−c₂n/K⁴} → 0 (c₂ ≤ c₁, p ≤ n^A, K fixed). Hence P(𝒜′_n) ≥ P(𝒜_n) → 1. ∎

## Remarks
1. Against `B3.md`: [R-1] the window is Theorem 2's 5(A + 1)(s₀ + 1) log n instead of C_q log n
   (C_q = 2(s₀(A + 2) + 4)/log 2); at s₀ = A = 1, C_q = 20.198… > 20 = 5(A + 1)(s₀ + 1), so B3's window would ask (A3), (A4)
   on slightly larger sets than Theorem 2 does. [R-5] Step 0 uses [R1] B1.2, B1.3 in place of `B2.md` (d). [R-8], [R-9]
   use the single fixed floor φ² of (A3) for both (F_λ) and (F_w) (B3 used ψ on small sets and c_ψ/n on the window).
   [R-6], [R-3] check B2-core's size condition directly for q_n. The probability argument (B1, B2-core) is unchanged.
2. Nothing here uses the last sentence of `W3-DIST:B3` (δ_n → 0), which is the part conditional on W3-POST:Thm-1.
3. The multiplicative form of B2-core would allow the floor on the window to be of order 1/n (option o2 of the plan);
   that option is OFF (HQ), and Theorem 2SG keeps (A3) as recorded.
