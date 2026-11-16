# W3-MISR-R — STATEMENT v1.2 (delta over W3-MISR v1.3; 2026-11-15; lead: Claude Opus 5.5, high, Claude Third; v1.1 = statement-lock amendments [L1-#], locked by `reviews/L1_statement_lock_sol.md` (LOCK-WITH-AMENDMENTS; `reviews/L1_disposition.md`); v1.2 = lead addition [LA-1], changelog §10)

Ticket W3-MISR-R (rider T13 of `Theory_work/Wave3/API_AUDIT/sharp2/TRIAGE.md` §2, row "T13 MISR-G/H"; motivation rows
`TRIAGE.md:40-42` and §3). Tier B, NORMAL mode. Protocol: `Theory_work/Wave3/PROTOCOL_v4.md`, rider rules `RIDER_RULES.md`.

**This is a delta statement.** BASE := `Theory_work/Wave3/W3-MISR/` (recorded on main; its `STATEMENT.md` is v1.3,
registry version 1.0.0 of every W3-MISR claim, sha256 of BASE `STATEMENT.md` 797bca0e29ae2726…). This file states in
full every definition, hypothesis and claim that differs from BASE v1.3, and takes everything else from BASE by
`file:line`. It **asserts no proof status**: proofs go in `lemmas/` (plan: `PLAN.md`), statuses are recorded there and
in the checkpoints. All results are asymptotic (n → ∞) unless marked *deterministic* or *finite n*. No method change.

## 0. What changes, in one table

| # | claim (this file) | replaces / extends (BASE `STATEMENT.md`) | what is gained |
|---|---|---|---|
| 1 | **W3-MISR-R:CorG-min** (§2) | Cor-G(a), `:162-170` | the candidate design is arbitrary (any law, dependent rows, no Σ_𝒞𝒞); only the omitted part, given the candidates, must be Gaussian with linear mean on the contrast scale; Σ_𝒞𝒞 ≻ 0 dropped; necessity under Gaussian noise; a Cramér partial converse |
| 2 | **W3-MISR-R:CorGb-plus** (§3) | Cor-G(b), `:171-174` | Gaussian candidate rows plus the omitted-part condition of §2 instead of jointly Gaussian rows; floor on the correlation matrix (no variance bound C₀); beta-min may be a liminf condition; explicit finite-n bound |
| 3 | **W3-MISR-R:CorH-plus** (§4) | Cor-H, `:176-197` | clause (a) needs only (SZ), (E^σ), (F₀) and δ_n → 0 in probability (no (OS), no margin); an in-sample Kullback–Leibler clause |
| 4 | **W3-MISR-R:CorH-U** (§5) | new (no BASE counterpart) | uniform-over-class forms of Cor-H(a), (b); the conditional random-design form (as BASE §4 for MIS-R); its Gaussian-row instance (G) |

Unchanged and not restated: BASE §0 (`:17-66`, setting, configurations, (GR^c), hypotheses, classes, constants, laws),
Lemma R′ (`:68-106`), MIS-R (i), (i′), (ii) (`:108-160`), Remarks SNR, P, U (`:199-220`), BASE §9 non-claims (`:259-266`)
except where §6 below says otherwise.

## 1. Notation added to BASE §0

* **Designs.** 𝔛_n(p) := {x ∈ ℝ^{n×p} : every column non-constant} (a Borel subset of ℝ^{n×p}). A *random candidate
  design* is a random n × p matrix X^r_𝒞 (p = p_n ≥ 1 deterministic) with P(X^r_𝒞 ∈ 𝔛_n(p)) = 1.
* **Conditional laws.** For a random element Z of ℝ^k, a random design X and a probability kernel Q from ℝ^{n×p} to
  ℝ^k, "conditionally on X, Z ~ Q(X)" means: E[h(X, Z) | X] = ∫ h(X, z) Q(X, dz) almost surely, for every bounded Borel
  h on ℝ^{n×p} × ℝ^k. N_k(m, 0) := δ_m.
* **Parameter posterior and distances.** Π(· | x, y^r) is the parameter posterior of BASE R′(a′) (`:75-77`) on
  (S, θ, v′); for a configuration κ = (x, β, v): μ̂ := X_Sθ (X the standardised x),
    h̄_n²(κ) := n⁻¹ Σ_i H²(N(μ̂_i, v′), N(μ_i(κ), v))   (as BASE `:180`),
    k̄_n(κ) := n⁻¹ Σ_i KL(N(μ̂_i, v′) ‖ N(μ_i(κ), v)),   KL(P‖Q) := ∫ log(dP/dQ) dP.
* **Bad sets** (sets of (S, θ, v′), depending on κ, n and a sequence M_n; θ zero-padded to ℝ^p; C_H = C_H(s, A) is
  the constant of BASE Cor-H(b), `:181`, i.e. that of [POST2] Claim D(b) at σ*² = 1):
    B^a_n(κ) := {‖μ̂ − μ(κ)‖² > M_n v} ∪ {|v′/v − 1| > M_n n^{−1/2}} ∪ {S ≠ S₀(κ)} ∪ {‖θ − θ(κ)‖ > M_n √(v/n)},
    H^a_n(κ) := {h̄_n(κ) > M_n n^{−1/2}},  K^a_n(κ) := {k̄_n(κ) > M_n/n};
    B^b_n(κ) := {‖μ̂ − μ(κ)‖² > C_H v log n} ∪ {|v′/v − 1| > M_n n^{−1/2}},
    H^b_n(κ) := {h̄_n²(κ) > (1 + C_H/4) log n/n},  K^b_n(κ) := {k̄_n(κ) > (1 + C_H/2) log n/n}.
  For s̄ ≥ 1, C̄_H := max_{s≤s̄} C_H(s, A), and B^b, H^b, K^b with C̄_H in place of C_H are written B̄^b, H̄^b, K̄^b.
* **Floor-only class.** 𝒦^F_n(s, A, M, φ₀) := {κ : s(κ) = s, (SZ), (E^σ; M), (F₀; φ₀)} (BASE `:46-48`); so
  𝒦⁰_n(s, A, M, φ₀, C_OS) = 𝒦^F_n ∩ {(OS; C_OS)} (BASE `:60`). Unions over s ≤ s̄ are written with s̄ in place of s:
  𝒦^F_n(≤s̄, A, M, φ₀) := ∪_{s=1}^{s̄} 𝒦^F_n(s, A, M, φ₀), likewise 𝒦⁰_n(≤s̄, …). sup ∅ := 0.
* δ(κ) := 1 − π_𝒞(S₀(κ) | x, y^r) (BASE `:118`).

## 2. Corollary G-min (W3-MISR-R:CorG-min) — replaces BASE Cor-G(a), `:162-170`

**Setting (at each n).** On (Ω*, 𝒢*, P): a random candidate design X^r_𝒞 (§1; **no other assumption on its law**: the
rows need not be independent, identically distributed or Gaussian, and no moment or covariance is assumed); a random
n × q matrix X^r_𝓜 of omitted columns (q = q_n ≥ 0); deterministic β_𝒞 ∈ ℝ^p, β_𝓜 ∈ ℝ^q; a real random variable α
(any dependence on everything); a random vector ε ∈ ℝⁿ; and
  y^r = α1 + X^r_𝒞β_𝒞 + X^r_𝓜β_𝓜 + ε.
Hypotheses:
- **(N)** ε ~ N_n(0, σ²I_n) with deterministic σ² ≥ 0, and ε is independent of (X^r_𝒞, X^r_𝓜).
- **(OV^c)** there are Borel maps γ : ℝ^{n×p} → ℝ^p and τ² : ℝ^{n×p} → [0, ∞) such that, conditionally on X^r_𝒞,
    Uᵀ(X^r_𝓜β_𝓜 − X^r_𝒞γ(X^r_𝒞)) ~ N_N(0, τ²(X^r_𝒞) I_N);
  and σ²_𝒞(x) := σ² + τ²(x) > 0 for every x.

Put β^𝒞(x) := β_𝒞 + γ(x) and κ_n := (X^r_𝒞, β^𝒞(X^r_𝒞), σ²_𝒞(X^r_𝒞)) on {X^r_𝒞 ∈ 𝔛_n(p)}, κ_n := a fixed reference
configuration off it (a null event).
**(a) Sufficiency.** Under (N) and (OV^c), (GR^c | σ(X^r_𝒞)) of BASE §4 (`:147`) holds for κ_n. Hence BASE MIS-R (ii)
(`:150-160`) applies with 𝓕_n := σ(X^r_𝒞) and target S₀(κ_n) = supp(β_𝒞 + γ(X^r_𝒞)) (random when γ depends on the
design; BASE §4(b) slices cover a random size in {1, …, s̄}; the class/event hypotheses of MIS-R (ii) are still to be
verified).
**(b) Full-vector sufficient form.** (OV^c) holds if there is moreover a Borel a : ℝ^{n×p} → ℝ such that, conditionally on
X^r_𝒞, X^r_𝓜β_𝓜 ~ N_n(a(X^r_𝒞)1 + X^r_𝒞γ(X^r_𝒞), τ²(X^r_𝒞)I_n)   **(OV)**.
If (N), (OV) hold and α = α(X^r_𝒞) is a Borel function of the design, then conditionally on X^r_𝒞,
y^r ~ N_n((α + a)(X^r_𝒞)1 + X^r_𝒞β^𝒞(X^r_𝒞), σ²_𝒞(X^r_𝒞)I_n).
**(c) Necessity under Gaussian noise.** Assume (N) and let γ, v : ℝ^{n×p} → ℝ^p × (0, ∞) be Borel. If (GR^c | σ(X^r_𝒞))
holds for κ_n := (X^r_𝒞, β_𝒞 + γ(X^r_𝒞), v(X^r_𝒞)) (reference configuration off 𝔛_n(p)), then v(X^r_𝒞) ≥ σ² almost
surely and (OV^c) holds with this γ and τ² := (v − σ²)₊ (conditionally on X^r_𝒞, almost surely). So under (N), (OV^c)
is equivalent to (GR^c | σ(X^r_𝒞)) at κ_n.
**(d) Cramér partial converse (noise law unknown).** Assume only that ε is independent of (X^r_𝒞, X^r_𝓜), with any law.
If (GR^c | σ(X^r_𝒞)) holds for κ_n as in (c), then Uᵀε ~ N_N(b, Σ_ε) for some deterministic b ∈ ℝ^N, Σ_ε ⪰ 0, and,
conditionally on X^r_𝒞, Uᵀ(X^r_𝓜β_𝓜 − X^r_𝒞γ(X^r_𝒞)) ~ N_N(−b, v(X^r_𝒞)I_N − Σ_ε) (in particular v(X^r_𝒞)I_N ⪰ Σ_ε a.s.).
The noise contrasts are Gaussian, and the centred omitted-part contrasts are Gaussian **conditionally on the candidate
design**; their conditional covariances add to v(X^r_𝒞)I_N [L1-2].
**(e) Examples (each a one-line check of (OV)).**
  (E1) *Jointly Gaussian rows* (BASE `:164-165`): rows (x^r_{𝒞,i}, x^r_{𝓜,i}) iid N(m, Σ) with Σ_jj > 0 for j ∈ 𝒞 and n ≥ 2;
  **Σ_𝒞𝒞 may be singular.** (OV) holds with deterministic γ := Σ_𝒞𝒞⁺Σ_𝒞𝓜β_𝓜 (Moore–Penrose inverse),
  a := (m_𝓜 − Σ_𝓜𝒞Σ_𝒞𝒞⁺m_𝒞)ᵀβ_𝓜, τ² := β_𝓜ᵀ(Σ_𝓜𝓜 − Σ_𝓜𝒞Σ_𝒞𝒞⁺Σ_𝒞𝓜)β_𝓜. With Σ_𝒞𝒞 ≻ 0 these are BASE's γ, β^𝒞, τ², σ²_𝒞.
  (E2) *Omitted columns linear in the candidates plus Gaussian noise*: X^r_𝓜 = 1m′ᵀ + X^r_𝒞Γ + Z, deterministic m′, Γ,
  Z with iid N_q(0, Σ_Z) rows independent of X^r_𝒞; X^r_𝒞 of any law (binary, heavy-tailed, dependent rows). (OV) holds
  with γ := Γβ_𝓜, a := m′ᵀβ_𝓜, τ² := β_𝓜ᵀΣ_Zβ_𝓜.
  (E3) *Fixed design*: X^r_𝒞 ≡ x deterministic. Then (N) + (OV^c) is BASE's (GR^c) (`:36-43`) with β = β_𝒞 + γ(x),
  v = σ² + τ²(x).
**Remark (what β^𝒞 is; no claim).** Under (OV^c), the mean of the regular conditional law of UᵀX^r_𝓜β_𝓜 given
X^r_𝒞 = x is Uᵀxγ(x) (no integrability of UᵀX^r_𝓜β_𝓜 itself is assumed or needed) [L1-3]: β^𝒞 is the candidate
coefficient of the conditional mean of the response contrasts given the candidates. As in BASE `:41-42`, β^𝒞 need
not be unique when UᵀX^r_𝒞 has deficient column rank; statements are about the chosen γ.

## 3. Corollary G(b)⁺ (W3-MISR-R:CorGb-plus) — replaces BASE Cor-G(b), `:171-174`

Setting: rows x^r_{𝒞,i}, i ≤ n, iid N_p(m_𝒞, Σ_𝒞𝒞) with Σ_jj > 0 (j ∈ 𝒞; Σ_𝒞𝒞 ≻ 0 is not assumed beyond the floor
below); (N) and (OV) of §2 with **deterministic**
a, γ, τ² (e.g. (E1) with Σ_𝒞𝒞 ≻ 0, or (E2) with Gaussian candidate rows); β^𝒞 := β_𝒞 + γ, σ²_𝒞 := σ² + τ² > 0.
Everything (m_𝒞, Σ_𝒞𝒞, β, γ, σ², τ², p) may depend on n. R := D_Σ^{−1/2}Σ_𝒞𝒞D_Σ^{−1/2}, D_Σ := diag(Σ_𝒞𝒞), is the
correlation matrix of a candidate row. Assume: 2 ≤ p ≤ n^A; s := |supp β^𝒞| ≥ 1 fixed; with k_n := s + max(j₀, m♯_n)
(m♯_n of BASE `:34` with p = |𝒞|),
  λ_min(R_TT) ≥ c_R > 0 for every T ⊆ 𝒞 with |T| ≤ k_n;  β^𝒞ᵀΣ_𝒞𝒞β^𝒞 ≤ M₀σ²_𝒞;
  ρ_n^{BM} := n·min_{j∈supp β^𝒞} Σ_jj(β^𝒞_j)²/(σ²_𝒞 log n) satisfies liminf_n ρ_n^{BM} > 16c₀(s, A)/c_R
(c₀ of BASE `:63`; in particular if ρ_n^{BM} → ∞, BASE's condition). Then there are n* and C such that for every n ≥ n*, with δ_n := 1 − π_𝒞(supp β^𝒞 | X^r_𝒞, y^r):
  E δ_n ≤ C r_n + (2 + 2k_n)n^{−2} + n^{−1},  P(HPM ≠ supp β^𝒞) ≤ 2C r_n + (2 + 2k_n)n^{−2} + n^{−1};
so both are O(r_n). (C is the constant of BASE MIS-R (i) on 𝒦^λ_n for (s, A, 2M₀ + 1, φ₀ = (c_R/8)^{1/2}, C_OS, c), with
C_OS of the bridge (F_w; 1) ⇒ (OS) and c > c₀(s, A) fixed by the beta-min branch; n* depends on the sequence.)
With m_𝒞 = 0 and jointly Gaussian rows, supp β^𝒞 is SL's s̃ (BASE `:174`).

## 4. Corollary H⁺ (W3-MISR-R:CorH-plus) — replaces BASE Cor-H, `:176-197`

Fixed designs; s ≥ 1, A ≥ 1, M ≥ 0, 0 < φ₀ ≤ 1 fixed; a sequence of configurations κ_n ∈ 𝒦^F_n(s, A, M, φ₀) for all
large n, laws P_{κ_n} (BASE `:65`); Π, μ̂, h̄_n, k̄_n as in §1; δ_n := δ(κ_n).
**(a′) (selection premise only).** If δ_n → 0 in P_{κ_n}-probability, then for every M_n → ∞,
  Π(B^a_n(κ_n) | x_n, y^r) → 0, Π(H^a_n(κ_n) | x_n, y^r) → 0 and Π(K^a_n(κ_n) | x_n, y^r) → 0 in probability.
  ((OS) and the margin are not assumed; δ_n → 0 may come from any source, e.g. BASE MIS-R (i) on 𝒦_n, c > c₁(s, A),
  or on 𝒦^λ_n, c > c₀(s, A), via Markov.)
**(b) (no margin, no beta-min; = BASE Cor-H(b), `:181-183`).** If moreover κ_n ∈ 𝒦⁰_n(s, A, M, φ₀, C_OS) for all large n,
then for every M_n → ∞, Π(B^b_n(κ_n) | x_n, y^r) → 0, Π(H^b_n(κ_n) | x_n, y^r) → 0 and Π(K^b_n(κ_n) | x_n, y^r) → 0 in
probability.
**(KL) (deterministic).** k̄_n(κ) = ½(v′/v − 1 − log(v′/v)) + ‖μ̂ − μ(κ)‖²/(2nv), and on {|v′/v − 1| ≤ ½}:
  k̄_n(κ) ≤ (v′/v − 1)² + ‖μ̂ − μ(κ)‖²/(2nv).
**The reference law** is BASE's (`:187-191`, unchanged). **Kullback–Leibler reading (replaces BASE `:191-195`).**
(i) Fixed design, contrast scale: under (GR^c) at κ the law of Uᵀy^r is N_N(Uᵀxβ, vI_N), a member of the working
contrast family {N_N(UᵀX b, wI_N) : b ∈ ℝ^p, w > 0}; so it is its own Kullback–Leibler projection onto that family
(divergence 0). (ii) In the setting of §2(b) (with α a function of the design): the conditional law of y^r given the
candidate design is N_n((α + a)1 + X^r_𝒞β^𝒞, σ²_𝒞I_n), a member of the candidate linear-Gaussian family, hence the
Kullback–Leibler minimiser over it (divergence 0). For jointly Gaussian rows as in (E1), with a deterministic intercept
α (and the deterministic parameters of that example), this also gives BASE's row-wise reading (SL's f₀, centred rows)
[L1-1]. k̄_n is the in-sample average divergence from the posterior's one-observation laws to the reference.
No statement about the projection given the realised omitted columns ([MIS1] `L1_reduction.md:69-74`).
Differences from SL's Theorem 4 as BASE `:196-197`.

## 5. Corollary H-U (W3-MISR-R:CorH-U) — uniform and conditional random-design forms (new)

Fix s̄ ≥ 1, A ≥ 1, M ≥ 0, 0 < φ₀ ≤ 1, C_OS < ∞, a sequence M_n → ∞ and η > 0. For every n and κ, write
P_κ(Π(B) > η) for P_κ(Π(B | x, y^r) > η) (well defined, and the same for every law satisfying (GR^c) at κ).
**(U-b) Uniform no-margin form.** lim_{n→∞} sup_{κ∈𝒦⁰_n(≤s̄, A, M, φ₀, C_OS)} P_κ(Π(B) > η) = 0 for B ∈ {B̄^b_n(κ), H̄^b_n(κ), K̄^b_n(κ)}.
**(U-a) Uniform selection form.** Let 𝒦^♭_n ⊆ 𝒦^F_n(≤s̄, A, M, φ₀) be any classes with
  lim_{n→∞} sup_{κ∈𝒦^♭_n} P_κ(δ(κ) > η′) = 0 for every η′ > 0   **(UP)**
(e.g. 𝒦^♭_n = 𝒦_n(s, A, M, φ₀, C_OS, c) with c > c₁(s, A), or 𝒦^λ_n with c > c₀(s, A), by BASE §2 and Markov; unions of
finitely many such). Then lim_{n→∞} sup_{κ∈𝒦^♭_n} P_κ(Π(B) > η) = 0 for B ∈ {B^a_n(κ), H^a_n(κ), K^a_n(κ)}.
**(RD) Conditional random-design form.** In the setting of BASE §4 (`:144-149`: σ-fields 𝓕_n, 𝓕_n-measurable random
configurations κ_n = (X^r_𝒞, β^𝒞, σ²_𝒞), response y^r with (GR^c | 𝓕_n)), let 𝒦♯_n be either 𝒦⁰_n(≤s̄, A, M, φ₀, C_OS)
with B_n := any of B̄^b_n, H̄^b_n, K̄^b_n, or a class 𝒦^♭_n with (UP) with B_n := any of B^a_n, H^a_n, K^a_n; put
ε_n := sup_{κ∈𝒦♯_n} P_κ(Π(B_n(κ)) > η) (→ 0 by (U-b), (U-a)). Then for every event 𝒜_n ∈ 𝓕_n with 𝒜_n ⊆ {κ_n ∈ 𝒦♯_n}:
  P(Π(B_n(κ_n) | X^r_𝒞, y^r) > η | 𝓕_n) ≤ ε_n almost surely on 𝒜_n,  hence  P(Π(B_n(κ_n) | X^r_𝒞, y^r) > η) ≤ ε_n + P(𝒜_nᶜ).
In particular Π(B_n(κ_n) | X^r_𝒞, y^r) → 0 in P-probability if P(𝒜_n) → 1; and, for the (a)-type sets B^a, H^a, K^a,
also when for every η″ > 0 there are constants (s̄, A, M, φ₀)_{η″}, classes 𝒦^{♭,η″}_n with (UP) and events
𝒜^{η″}_n ∈ 𝓕_n, 𝒜^{η″}_n ⊆ {κ_n ∈ 𝒦^{♭,η″}_n}, with limsup_n P((𝒜^{η″}_n)ᶜ) ≤ η″ (the form of BASE §4(c), `:157-160`).
With §2 this applies to omitted-variable models with an arbitrary candidate design (𝓕_n = σ(X^r_𝒞)).
**(G) Gaussian-row instance [LA-1].** In the setting and under the hypotheses of §3, with κ_n := (X^r_𝒞, β^𝒞, σ²_𝒞)
(reference configuration off the null event of §2): for every M_n → ∞, Π(B | X^r_𝒞, y^r) → 0 in P-probability for
B ∈ {B^a_n(κ_n), H^a_n(κ_n), K^a_n(κ_n)}. (By (RD) with 𝓕_n = σ(X^r_𝒞), 𝒦^♭_n := 𝒦^λ_n(s, A, 2M₀ + 1, (c_R/8)^{1/2}, C_OS, c)
of §3 — (UP) by BASE MIS-R (i) and Markov — and the design events of §3's proof, whose probability tends to one.)

## 6. Not claimed (additions to BASE §9, `:259-266`)

An expectation rate for Cor-H(b) (posterior expectations of unbounded losses: BASE `D_hellinger.md` D4.3); a
Bernstein–von Mises statement; Cor-G(b)⁺ with non-Gaussian (e.g. sub-Gaussian) candidate rows; anything about W3-DIST
(the observation that a candidate run under §2(b) is an (RD) instance of W3-DIST is recorded in `REPORT.md` as
HEURISTIC/OPEN only); the BASE `ASSUMPTION_MAP.md:27` cross-cite (editorial ticket W3-EDIT).

## 7. Inputs (registry id @ version, ACTIVE on origin/main; statuses verbatim, in full)

- W3-MISR:R'@1.0.0, W3-MISR:MIS(i)@1.0.0, W3-MISR:MIS(ii)@1.0.0, W3-MISR:Cor-G(b)@1.0.0, W3-MISR:Cor-H@1.0.0, by
  statement; BASE `lemmas/G_corollaries.md` G.1–G.3 and `lemmas/M_misr.md` M.3 by line in the proofs. Statuses:
  - W3-MISR:R' — "PROVED-CHECKED; council R2, MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103, sol=9.2 PASS, opus=8.9 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT)";
  - W3-MISR:MIS(i) — "PROVED-CHECKED, conditional on W3-POST2:C; council R2, MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103, sol=9.2 PASS, opus=8.9 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT)";
  - W3-MISR:MIS(ii) — "PROVED-CHECKED, conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1, SOP:TH09, SOP:TH128; input versions SOP:TH09@1.0.0, SOP:TH128@1.0.0; council R2, MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103, sol=9.2 PASS, opus=8.9 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT)";
  - W3-MISR:Cor-G(b) — "PROVED-CHECKED, conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1, W3-POST2:A0, C-MIS:Prop-P, SOP:TH09, SOP:TH128, C-MIS:GDb; input versions C-MIS:Prop-P@1.0.0, SOP:TH09@1.0.0, SOP:TH128@1.0.0, C-MIS:GD(b)@1.0.0 (C-MIS:GDb = alias of C-MIS:GD(b)); council R2, MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103, sol=9.2 PASS, opus=8.9 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT)";
  - W3-MISR:Cor-H — "PROVED-CHECKED, conditional on W3-POST2:D, W3-POST2:C; council R2, MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103, sol=9.2 PASS, opus=8.9 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT)".
- W3-POST2:D@1.1.0 (Claim D(a), D(b), by statement, `W3-POST2/STATEMENT.md:99-119`), W3-POST2:A0@1.0.0 (bridge
  (F_w; g₀) ⇒ (OS), `:46-47`; `lemmas/A_occam.md` Lemma A0, `:14-15`), W3-POST2:C@1.0.0 (through MIS(i)) — each
  "PROVED (by this seat, unchecked)": carried as declared hypotheses ("conditional on …") per BASE `:225-228`.
- SOP:TH09@1.0.0 — "T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2). T02(i♯), T02(ii♯): PROVED; SF/XF VERIFIED. T01–T03: PROVED-LOCKED (wave 3; external review queued), SAME-FAMILY-ONLY";
  SOP:TH128@1.0.0 — "PROVED (candidate) (W1-T03R); SF VERIFIED (W2-VT03R, no GAP/ERROR in the mathematics); XF VERIFIED under exactly its hypotheses (A-REV2); VERIFIED core (A-REV5, onset gloss ERROR); LIT-STAT: modest extension of Rossell 2022, clause (iii) known; final card: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)"
  (through Cor-G(b) and MIS(ii); quoted in full, absorbing erratum W3-EDIT I4-F2 for this delta).
- C-MIS:Prop-P@1.0.0 — "R02 VERIFIED; R04 wording fixes checked in R05; council PASS"; C-MIS:GD(b)@1.0.0 — "R02
  VERIFIED-WITH-AMENDMENTS (applied); council PASS" (through Cor-G(b)).
- Code: as BASE `:15` (commit 16a7f85). Code fact used: the standardisation of the retained candidate columns
  X = CxD_x⁻¹ (BASE `:22`; [W3P] `Theory_work/Wave3/W3-POST/STATEMENT.md:18-22`, with the code lines cited there)
  [L1-Q5], which makes π_𝒞 invariant under positive rescaling of candidate columns (used in §3).
- External classical input: Cramér's decomposition theorem (H. Cramér, Math. Z. 41 (1936), 405–414: if the sum of two
  independent real random variables is Gaussian, each is Gaussian, degenerate laws included), used in §2(d) only [L1-Q5].

## 8. Dependencies and supersession (each new claim implies the BASE claim it replaces)

| new claim | implies | why (one line) |
|---|---|---|
| W3-MISR-R:CorG-min | W3-MISR:Cor-G(a)@1.0.0 | BASE's Gaussian rows with Σ_𝒞𝒞 ≻ 0 are (E1), which gives (N) + (OV) with BASE's (γ, τ²); (a) then gives (GR^c | σ(X^r_𝒞)) with BASE's (β^𝒞, σ²_𝒞) |
| W3-MISR-R:CorGb-plus | W3-MISR:Cor-G(b)@1.0.0 | jointly Gaussian rows ⇒ Gaussian candidate rows + (OV) (E1); λ_min(Σ_TT) ≥ c_pop and Σ_jj ≤ C₀ ⇒ λ_min(R_TT) ≥ c_pop/C₀; ρ_n^{BM} → ∞ is one branch; the explicit bound is O(r_n) |
| W3-MISR-R:CorH-plus | W3-MISR:Cor-H@1.0.0 | 𝒦⁰_n ⊆ 𝒦^F_n; on 𝒦_n (c > c₁) or 𝒦^λ_n (c > c₀) BASE MIS-R (i) gives δ_n → 0, so (a′) gives BASE (a); (b) is BASE (b) |
| W3-MISR-R:CorH-U | W3-MISR-R:CorH-plus (a′), (b) | a single sequence is the singleton classes 𝒦^♭_n := {κ_n} (then (UP) is δ_n → 0 in probability) and 𝒦⁰_n ∋ κ_n |

Supersession of the BASE rows (the headline row Cor-G(b) included) is HQ's decision with the HQ consultant (v4 H5); the
lead proposes it in `REPORT.md`. Consumers of BASE Cor-G(a), Cor-G(b), Cor-H: W3-READER row thm4 (via `READER_DELTA.md`).

## 9. Assumption ids (for the registry block)

A:MISR-OVC (new: (N) + (OV^c); implies A:MISR-GRC conditionally on σ(X^r_𝒞), equivalent to it under (N)); A:MISR-OV
(new: full-vector (OV)); A:GAUSS-CAND-ROWS (new: iid Gaussian candidate rows; CorGb-plus only); A:CORR-FLOOR (new:
correlation-matrix sparse floor; CorGb-plus); A:MISR-ESNR, A:POST2-F0, A:POST2-OS, A:FIXED-S0, A:P-POLY (BASE `:269-272`);
A:SEL-P (new: premise δ_n → 0 in probability, resp. its uniform form (UP); CorH-plus (a′), CorH-U (U-a)).

## 10. Changelog (v4 §4.2; rows after the lock)

| version | clause | STRONGER / WEAKER / EQUAL / NEW-CLAIM | reason | trigger | check |
|---|---|---|---|---|---|
| 1.1a | §4 KL reading (ii), row-wise sentence | WEAKER (an interpretive assertion restricted to a deterministic intercept; no displayed hypothesis or conclusion changed; not a target-clause display; reported at CP3 per v4 §4.2) | L1-1 (MAJOR) | `reviews/L1_statement_lock_sol.md` | `reviews/K1_linecheck_sol.md` (K1-1: tag corrected from EQUAL) |
| 1.1b | §2(d) sentence; §2 remark; §2(a) parenthesis; §7 code/Cramér citations | EQUAL (wording, conditional-law convention, citations) | L1-2, L1-3, Q1/Q5 | `reviews/L1_statement_lock_sol.md` | `reviews/K1_linecheck_sol.md` (confirmed) |
| 1.2 | §5 CorH-U clause (G) | NEW-CLAIM (clause; a composition of (RD), §3 and MIS-R (i)) | needed by the reader-version remark (`READER_DELTA.md` B4.4) | lead [LA-1] | `reviews/K1_linecheck_sol.md` (NEW-CLAIM confirmed; clause correct) |
