# Walk T8-Thm5 — Theorem 5, the start law concentrates (card row 3.3)

Walker: Fable-CT-D (Fable 5.2, Claude Third). Depth: standard walk. Snapshot: origin/main at branch creation
(`theory/PRE-LEAN-walkD`). Master: `W3-START2-R:START-R@1.0.0` (`W3-START2-R/STATEMENT.md:226-240`), bridge
`W3-START2-R:BR@1.0.0` (`:217-225`), floor `W3-START:FLOOR@1.0.0` (`W3-START/STATEMENT.md:241-243`).
Paths below are relative to `Theory_work/Wave3/`.

## Findings

| # | Severity | file:line | Claim | Why |
|---|---|---|---|---|
| F1 | NOTE | `W3-START2-R/lemmas/R3_RATE.md:125-127`; `W3-START2/lemmas/P4_BR.md:59-67`; `W3-START/lemmas/L6_COROLLARIES.md:11-26` | START-R (i) ("probability → 1" with the explicit envelope) is proved from Corollary L6.0′, i.e. (T1)(d) run at ε_n = 4/log n | L6.0′ needs how (C, c₀, n₀) of (T1)(d) depend on ε (Lemma L6.0 and the explicit λ = 4c_L/ε of L5.2). The **statement** of (T1)(d) only says "there are C, c₀, n₀ depending on (ε, κ)". The registry row for START-R lists `W3-START2:START-F@stmt`; the dependency actually used is proof-level (`W3-START:START-F@proof`: L5.2, L6.0, L6.0′), and ERRATA #6 does not add it. No mathematical gap (L6.0′ is proved; a diagonal choice of ε_n would also do from the statement alone). For Lean: L5.2 with its explicit constants and L6.0′ must be exported as lemmas, not kept inside the START-F proof. |
| F2 | NOTE | `W3-START2-R/lemmas/R3_RATE.md:41-63`, `:89-105`, `:122-141` | "BASE L9.1–L9.6 hold verbatim with the changed lines [R-1]–[R-9]" | The proof of START-R is three layers of "as before, with these lines replaced" (BASE L9, PARENT P4, this file). I checked every replaced line against the line it replaces and found each substitution sound (sections below). A formalization needs one consolidated statement of L9.5 with the shift bound d̄ as a parameter (it is used twice: d̄ = √2s₀C_L/c_Σ^{3/2} and d̄⁰_n = √2s₀C₀/(c_Σ^{3/2}√log n)) and of L9.6 with the reference count as a parameter. Not a flaw. |

No FATAL, MAJOR or MINOR finding. Already on the T8 card and re-confirmed here, not re-counted: T8-2 (`STATEMENT.md:237`,
"on every data set" needs s₀ < K) and T8-3 (`R3_RATE.md:87`, "=" should be "≤" on a probability-zero event).

## 0. Presented statement against the master

Reader Theorem 5 (`W3-READER/READER_VERSIONS.md:574-605`) and card row 3.3.

* (A1)–(A3) with (S1)–(S3) = Setting R with p > s₀, p ≤ n^A, ε independent of the design, exact arithmetic, (FL-R16).
  (A4) = (V-R). (A5) = (L-R⁺⁺) with Q = S₀, H̄_n = e^{κ√log n}. (A6) ⇒ (L-gain-0) with C₀ = 0
  (Σ_{lU} = 0 for U ⊆ S₀; Σ_UU invertible by (A3)). Each matches the master clause word for word.
* First display = START-R (i) at Q = S₀: an unconditional statement under the joint law of (X^r, ε), "probability
  → 1" (not "for every n"), every c < ½. ✓
* (A6) display = START-R (iii): O_P in the sense of `W3-START2-R/STATEMENT.md:45-47` (limsup_n P(· > C·a_n) ≤ ε),
  joint law. ✓
* Leakage remark = START-R (i) with general Q; |Q| ≤ K is stated; for |Q| ≤ n^{1/2−ε} the bound |Q| ≤ K is automatic
  once n ≥ 4 (|Q| ≤ p, and n^{1/2} ≤ n/2). ✓
* Floor sentence = (T0), with "n ≥ 4 and s₀ < K" stated. ✓
* Card wording "with probability tending to one" for both displays [R1-S5] agrees with the master. ✓

## 1. (T0) FLOOR — `W3-START/lemmas/L1_AGG_FLOOR.md:111-137`

Deterministic; valid data, n ≥ 4, EX-A, |S| < K.
* (i) Q_S = yᵀy/(n+1) + (n/(n+1))ρ_S with ρ_S the ridge minimum at λ = 1/(n+1): checked from H_S = (n+1)(G_S + λI).
  Monotone in S. ✓
* (ii) D_{S∪l}/D_S = (n+1)·s(1/(n+1))/s(1) ≤ n+1, s the Schur complement, nondecreasing in λ. ✓ No rank condition.
* (iii) one-step ratio ≥ (n+1)^{−1/2} (ν > 0). ✓
* (iv) w(k+1)/w(k) = (k+1)/(2p−1−k) from w(k) = ½/C(2p−1,k) ✓; sum over p − k columns gives f_n(k);
  2(k+1)(p−k) − (2p−1−k) = k(2(p−k)−1) + 1 > 0 for k < p ✓; f/(1+f) ≥ (2/3)f as f < ½ ✓.
* (v) with S = S₀ and s₀ < K the sum is T₁, so o₀ ≥ T₁ ≥ ½(n+1)^{−1/2}. ✓
Assumptions used: |S| < K (so S ∪ {l} ∈ Ω), block size ≤ K (table fully scored). Nothing else.

## 2. Bridge (B-R⁺⁺)(i) — BASE `W3-START/lemmas/L9_BR.md` with [R-1]–[R-5] of `R3_RATE.md:39-63`

* **L9.1 (covariance event).** Rows of OᵀW are N iid N(0, Σ); polarisation and Laurent–Massart give
  |Ŝ_jk − Σ_jk| ≤ 2√(x/N) + 2x/N with probability ≥ 1 − 4e^{−x}; union over p² ≤ n^{2A} pairs at x = (2A+2) log n:
  P(E_covᶜ) ≤ 4n^{−2}. ✓ Uses Gaussian rows, unit diagonal, p ≤ n^A.
* **(c1)–(c4).** |R̂ − Σ| ≤ 2h/(1−h) ≤ 3h ✓; λ_min(R̂_T) ≥ c_Σ/2 for |T| ≤ 16 + s₀ ✓ ((FL-R16)); Schur perturbation
  constant C_S = 1 + 45/c_Σ + 450/c_Σ² recomputed ✓; |U ∪ {j,k}| ≤ 17 ≤ 16 + s₀ uses s₀ ≥ 1 ✓.
* **L9.2.** ‖μ‖² ≤ s₀²θ_hi²N deterministically ✓; (GF-16) with g_* = c_Σ/2 ✓; (V-c): |N⁻¹x_jᵀ(I−P_U)μ| ≥ a_V/2 from
  (V-R) and (c3), so δ²_{U,j} ≥ N a_V²/4, τ²_U ≤ σ² + Δ_hi ✓. This is the only use of (V-R). "(V-c) for every fixed c_V"
  holds on E_cov for n ≥ a threshold that depends on c_V; the proof fixes c_V = 2A + 4. ✓
* **L9.3.** J_n(δ_{U,l}, τ_U) = F(g_{U,l}, a_U) with √(1−a_U) = √Δ_U/τ_U ✓; (F1) ✓; (F2) ✓. Δ_U ≥ Δ_lo uses θ_lo and (c4).
* **L9.4 (localisation).** Partial-correlation recursion ✓; ‖a‖ ≤ c_aε_n, ‖d‖ ≤ c_dε_n from (c3), (c4), (L-loc-R) ✓
  (both parts of (L-loc-R) are used; S₀ ⊆ H_l is used to get S₀ ∩ U = S₀ ∩ U₀); C₄, C₅ recomputed ✓;
  ι_n√log n → 0 from r_n(n log n)^{1/4} → 0 and h′_n² = O(log n/n) ✓. Independent of |H_l|. ✓
* **L9.5 (conditional law).** Population regression of W_l on W_D, D = U₀ ∪ S₀; τ_e² ∈ [c_Σ, 1] ((FL-R16) on
  |D ∪ {l}| ≤ 16 + s₀); γ² by Frisch–Waugh, ‖γ²‖ ≤ √s₀C_L/(c_Σ√n) from (L-gain-R) at U = U₀ ✓. Given 𝒲 = σ(W_D):
  ξ ~ N(0,1), R noncentral χ²_{ν₀−1}, independent ✓; (9.1) ✓; |d₀| ≤ d̄ on CN (𝒲-measurable) ✓. The Gaussian integral:
  1 − s′² ≥ a̲/2, coefficients η_n/a̲, 2/a̲, 1/a̲ recomputed ✓. The conditioning is on W_D only; nothing is asserted
  given E_cov. ✓ The expectation carries 1_{E_R}1_{CN} only (E_ξ is not needed here, and is not used).
* **L9.6 with [R-1]–[R-5].** [R-1] |I_l| ≤ N̄_n = (1 + H̄_n)^{15} ✓ (Σ_{k≤15}C(m,k) ≤ (1+m)^{15}). [R-2]
  P(Eᶜ) ≤ (4 + 3N̄_n)n^{−2} → 0 since N̄_n ≤ 2^{15}e^{15κ_H√log n} for n ≥ n_H ✓ (H̄_n ≥ 2 because |H_l| ≥ 2). E_ξ enters E to
  bound |g| ≤ G_n for (F2) ✓. [R-3] EΨ_n ≤ N̄_nΦ_n ✓. [R-4] Markov with e^{ς′_n} ≤ e ✓. [R-5] λ = log n,
  C_B = 2d̄√(2A+1)/a̲ + 15κ_H + 1 ✓; (R3.2) ✓.
* (V-c) at level c_V + 2A gives (V-cp) at c_V (2 log p ≤ 2A log n) ✓ (not needed by START-R, which uses (V-c)).
Events: all under the joint design law; (i) is "probability → 1". Thresholds depend on the fixed constants, the
sequence r_n and n_H; no uniformity over these is claimed. ✓

## 3. Bridge (B-R⁺⁺)(ii), C_L = 0 — `R3_RATE.md:65-72`

d̄ = 0; Φ_n ≤ 2√(2/a̲)√(2/π)z̄_n; C₇ = 9√((2A+1)/a̲) (1 + 2e√2 < 9, a̲ ≤ 1) ✓; (R3.3) for every λ ≥ 1 ✓. Tightness
only, as stated. ✓

## 4. Bridge (B-R⁺⁺)(iii), sharp leading functional — `R3_RATE.md:74-118`

Hypotheses (FL-R16), (L-gain-0); neither (V-R) nor (L-R⁺⁺) nor E_cov is used — checked: the reference sets are
U ⊊ S₀, so no localisation and no (F2) step (hence no need for a_U ≤ ā, θ_lo, or E_ξ).
* Step 1: representation is algebra; a_U ≥ a̲ deterministically ✓. Probability-zero event: T8-3 (known).
* Step 2: L9.5 at U₀ = U, D = S₀; ‖γ²‖ ≤ √s₀C₀/(c_Σ√(n log n)) from (L-gain-0) (its quantifiers l ∉ S₀, U ⊊ S₀,
  |U| ≤ 15, j ∈ S₀ ∖ U are exactly those needed) ✓; d̄⁰_n; C₈, C₉ recomputed ✓. L9.5's proof uses only a ≥ a̲, (F1),
  (9.1), η_n ≤ a̲/2, |d₀| ≤ d̄ on CN ✓.
* Step 3: P(‖CW_j‖² > 2N) ≤ e^{−N/8} (Laurent–Massart at x = N/8) ✓; ≤ 2^{s₀} sets U; max ≤ sum; Markov gives
  (R3.4) ✓. 𝔏^♯_n as in PARENT (D1) (`W3-START2/STATEMENT.md:52-55`) ✓.

## 5. START-R (i) — `R3_RATE.md:120-131`, PARENT `W3-START2/lemmas/P4_BR.md:47-74`, BASE `L8_TRANSFER.md`

* Design set 𝒳_n: (c1)–(c4), (V-c) at c_V = 2A + 4 (κ_V = 3/2 > κ = 1), 𝔏_n(Q) ≤ e^{C_B√log n}; P(X^r ∉ 𝒳_n) → 0 by
  L9.1, L9.2, (R3.2) ✓. Every design of 𝒳_n is admissible (p ≤ n^A, s₀ < p, S₀ ⊆ Q, |Q| ≤ K from (D4), ‖μ‖² ≤ Mn,
  (GF-16), (V-c); θ*, Q, h do not depend on the response) ✓.
* Transfer L8.1–L8.2: the conditional law given X^r is Setting F at the fixed design, because ε is independent of
  X^r; the constants of (T1)(d) do not depend on the design, so no union over designs is taken ✓.
* Two cases at each n ≥ n_R: a_n ≥ 1 (event empty) or a_n < 1 (then ϱ̄ = a_ne^{−√log n} ≤ c_{0,n}, and
  C_nϱ̄ + n^{−1} ≤ a_n since a_n ≥ n^{−1/2}) ✓. Result: P(1 − π₀(𝓛(Q)) > a_n) ≤ 4/log n + 1/(32 log n) + P(X^r ∉ 𝒳_n) → 0,
  a_n = (|Q|+1)n^{−1/2}e^{C_R√log n}, C_R = C_B + 1 ✓. Default levels: b_n ≤ 1/(32 log n) ✓.
* Consequences for Q = S₀ (every c < ½) and |Q| ≤ n^{1/2−ε_Q} (every c < ε_Q) ✓.
* Input used: BASE Corollary L6.0′ / Proposition L5.2 — see F1.

## 6. START-R (ii) — `R3_RATE.md:133-141`, PARENT `P4_BR.md:78-90`

[R-9] b^Q_n with N̄_n; D_ε = C₇·4/ε; limsup P(X^r ∉ 𝒳_n^ε) ≤ ε/4 ✓; T_ε = max(D_ε/c₀, CD_ε + 1); two cases ✓;
limsup ≤ ε/2 ✓. O_P with a rate that need not tend to zero, as the statement says. ✓ (Not on the card.)

## 7. START-R (iii) — `R3_RATE.md:143-167`, PARENT `P1_LEADING.md:82-110, 147-151`

* 𝒳⁰_n adds 𝔏^♯_n ≤ D⁰_ε√log n; limsup P(X^r ∉ 𝒳⁰_n) ≤ ε/8 by (R3.2) at Q = S₀ and (R3.4) with λ = 8/ε ✓.
* On 𝒳⁰_n: ϱ_n(S₀) ≤ ϱ̄_n → 0 and n^{−1/2}𝔏^♯_n + n^{−1}𝔏_n(S₀)² ≤ (D⁰_ε + 1)√(log n/n) for n large ✓.
* PARENT P1.4(ii) / P1.7 at (ε/8, κ = 1): P(o₀ > C^♯r̄_n + n^{−1}) ≤ ε/8 + 1/(32 log n) + P(X^r ∉ 𝒳⁰_n); limsup ≤ ε/4 ✓.
  P1.4's delta over BASE L5.2 (event 𝓜^♯ from (1.2), λ = 2^{17}e_κ/ε, 451ε/2^{17} ≤ ε/4) checked ✓.
* 1 − π₀(S₀) = o₀/(1 + o₀) ≤ o₀ ✓.
* Where each hypothesis is used (`:165-167`) agrees with what I found: (L-gain-0) only in (R3.4); (L-R⁺⁺) at Q = S₀
  only for 𝔏_n(S₀) ≤ e^{C_B√log n} (second-order term and ϱ ≤ c₀); (V-R) for (V-c); (FL-R16) for floors, τ_e², ‖γ²‖.
* Optimality up to √log n: (T0) with s₀ < K, true for all large n since p > s₀ (T8-2, known). ✓

## 8. Boundary of this walk

Walked: FLOOR; BASE L9.1–L9.6; R3.0–R3.6; PARENT P4.2–P4.3, P1.4, P1.7; BASE L8.0–L8.2; BASE L6.0–L6.0′ (statement and
its one-line proof). **Not opened below the statement:** BASE Proposition L5.2 = (T1)(d) (`W3-START:START-F`,
PROVED-CHECKED) and its chain (AGG-a/b, TK, LEAK, VIS, ASM), and PARENT Lemma LEAK-0 ((1.2)); these are recorded
inputs. IF-START⁺⁺ (`R3_RATE.md:169-178`) belongs to row 3.6 and was read but is not part of row 3.3.

**WALK COMPLETE** (to recorded inputs; boundary as in §8).
