# W3-RM2 — STATEMENT (Theorem 3 at polynomial leakage: the reported model under visibility, leakage of size n^b, and a lattice-width condition)

Ticket W3-RM2, Theory Wave 3 (follow-up of PROGRAM item 3; W3-RM REPORT §6 item 1). Lead: Claude Fable 5.2 (Claude
Work, effort high). Status of this file: **v1.1 (target statement — nothing in it is proved yet)** = v1.0 with all
six required changes and the four optional suggestions of statement-lock review SL1 applied
(`reviews/SL1_statement_lock_sol.md`: LOCK WITH CHANGES; `reviews/SL1_disposition.md`; markers [SL1-#]).
Protocol: `Theory_work/Wave3/PROTOCOL.md`. All results are asymptotic (n → ∞). Method = production core as on `main`
(pins in §1). **No method change is requested.**

Abbreviations. RM = `Theory_work/Wave3/W3-RM/`; GROW = `Theory_work/Wave1C/C-GROW/`; GEN = `Theory_work/Wave1/W1-GEN/`;
LOC2 = `Theory_work/Wave2/W2-LOC2/`; UNI = `Theory_work/Wave2/W2-UNI/`; APP = `Theory_work/Wave2/W2-APP/`;
CORE = `Scripts/SMC_BVS/core/`. Registry = `Theory_work/INFRA/registry/claims.tsv`; a claim is cited as `id@version`.

## 0. What is claimed, in one paragraph

W3-RM proved Theorem 3 for leakage sets of polylogarithmic size. Here the leakage set may have **polynomial** size
|Q| ≤ n^b. **Form F (fixed design):** under Theorem 1's conditions, the eigenvalue floors, visibility (V), leakage
(L) with |Q| ≤ n^b and leak level η, where **b < β(η, A) := ½ − η/2 − √(2Aη)** (so b < ½ when nothing leaks outside
Q), a signal floor at the lattice scale (BM-Q), and a **lattice-width condition (W)** on (X, Q), every output run of
the coded method reports Ŝ⁺ = S₀ on one data event of probability → 1. (W) replaces RM's lattice condition (N): it
is a bound on the expected maximum of a Gaussian process indexed by the residual directions of the lattice [S₀, Q];
it contains RM's (N-χ) and (N-D)(i), it follows from a primitive localisation condition (W-loc), and it is
**necessary for the whole-lattice no-addition event up to the slack in its constant** (Lemma W-conv). **Form R
(Gaussian rows):** the same from population visibility and localised leakage with |Q| ≤ n^b and reference
neighbourhoods |H_l| ≤ n^ρ, 15ρ + b < ½, and (W) holding on the realised design with probability → 1 (sufficient:
the population reference/atom conditions of LOC2's Lemma NA-R). RM-F and RM-R are special cases. **Not claimed:**
the theorem without any lattice condition (path-level control of LS0 — a separate ticket), and any b ≥ ½.

## 1. Settings, method objects, events (imported)

Everything in RM `STATEMENT.md` §1 (`Theory_work/Wave3/W3-RM/STATEMENT.md:32-68`) is used unchanged and is not
restated: **Setting F** (fixed raw design, y^r = α1 + X^rβ + ε, ε ~ N_n(0, σ²I), X centred and standardised, μ = Xθ*,
S₀ = supp θ*, s₀ ≥ 1 fixed, p ≤ n^A, A ≥ 1 fixed, K = min(p, ⌊n/2⌋), Ω = {|S| ≤ K}, D0 score, capped BB(1, p) prior
w, F(S) = log w(|S|) + log m(S), block tables r_b, start law γ₀, start mode S̃₀); **Setting R** (raw rows iid
N(m_n, Σ_n), unit diagonal, sample-standardised X, |θ*_j| ∈ [θ_lo, θ_hi] on S₀, s₀ fixed, p ≤ n^A); the move cap
ℓ_n = ⌈log₂(n + p + 1)⌉ and LS0's shipped cap ℓ_n + |S̃₀|; the method's partition (an X-measurable partition with
blocks of size ≤ 16; nothing else about it is used); the notation P_T, R̂_T, u_{T,l}, δ_{T,l}, Z_{T,l}, θ*_min,
τ²_U := σ² + ‖(I − P_U)μ‖²/(n − 1); the events Sand_n(Q), NA(𝓛), TL(𝓛), 𝒦_n, 𝒪, U_n and the reported model Ŝ⁺; the
implementation premises (EX-A, EX-S, SR, GUARD-W, OP-LS0, complete scans) and the configuration (`ls0 = TRUE`,
`ls0_ell = ℓ_n`, `ls0_cap = "ell_n_plus_mode"`, `ls0_tie_dp = TRUE`); "admissible run".

**Code pins** (the facts about the method used here; commit `9700e17` of this branch; the three files were last
changed at `0638af9`):
* LS0's centre is the returned start mode, unmodified, and its move cap is ℓ_n + |centre| in the shipped
  configuration: CORE `cpp/v3_core.cpp:465-476` (cap at `:473`, option parsing `:394-404`).
* One LS0 scan scores every single flip (deletion of a member; addition of a non-member when |C| < K) and every swap
  (one member out, one non-member in): CORE `cpp/v3_engine.h:394-406`. It moves to the best neighbour only on a strict
  F improvement, ties broken lexicographically (`:392`, `:408`), and stops with `local_certified = true` when a
  completed scan finds no strict improvement (`:413-414`), or with `local_limit = true` at the cap (`:409-410`).
* Lemma E4 (W3-RM:E4@1.0.0) identifies the centre as a maximiser of γ₀ on Ω.

**Additional notation.** For a deterministic Q ⊇ S₀ with |Q| ≤ K: q := |Q|; 𝓛 := {T : S₀ ⊆ T ⊆ Q};
**𝔓 := {(T, l) : T ∈ 𝓛, |T| < K, l ∈ [p] ∖ T}** (the pairs that NA(𝓛) quantifies over). [SL1-2] For l ∈ [p] and
any B ⊆ Q ∖ {l} with X_BᵀX_B invertible, β_{B,l} := (X_BᵀX_B)⁻¹X_Bᵀx_l ∈ ℝ^B is the sample regression coefficient of
x_l on X_B (β_{∅,l} := 0, P_∅ := 0); a bar (β̄) denotes zero-padding to ℝ^Q. Under (FL-Q) every such inverse exists.
* **Leak budget.** β(η, A) := ½ − η/2 − √(2Aη) for η ≥ 0. β(0, A) = ½; β(η, A) > 0 ⇔ η < η_A := (√(2A + 1) − √(2A))²
  (RM's leak threshold); β is decreasing in η.
* **Lattice width.** For δ ∈ (0, 1) and integers 0 ≤ k < p put a_{n,δ}(k) := √(2 log(p/(k + 1)) + (1 − δ) log n) and
  a⁺_{n,δ}(k) := √(2 log(2p/(k + 1)) + (1 + δ) log n). When every u_{T,l}, (T, l) ∈ 𝔓, is defined, let g ~ N(0, I_n) and

    𝔴_n(δ) := E max_{(T,l)∈𝔓} ( |u_{T,l}ᵀg| − a_{n,δ}(|T|) ),   𝔴⁺_n(δ) := E max_{(T,l)∈𝔓} ( |u_{T,l}ᵀg| − a⁺_{n,δ}(|T|) )

  (both := −∞ if 𝔓 = ∅; then (W) below holds vacuously and no reference family is needed [SL1-opt3]). They are
  deterministic functions of (X, S₀, Q): the expected maximum of shifted absolute Gaussian projections [SL1-opt1] —
  the projections of one Gaussian vector on the lattice's unit residual directions, each compared with the
  size-dependent level that the prior and the score assign to one more variable. For (T, l) ∈ 𝔓, |T| < K ≤ p, so
  p/(|T| + 1) ≥ 1 and the levels are real. g is an auxiliary vector; with g = ε/σ, u_{T,l}ᵀg = Z_{T,l}.

## 2. Interface properties (PROTOCOL item 5) — unchanged from RM

| id | property | consumed by |
|---|---|---|
| [POST] | E[1 − π(S₀)] → 0 | RM-0 |
| [SAND(Q)] | P(Sand_n(Q)) → 1 | RM-0 |
| [TL(Q)] | P(TL(𝓛)) → 1 | RM-0 |
| [NA(Q)] | P(NA(𝓛)) → 1 | RM-0 |
| [E4] | the emitted LS0 centre is a maximiser of γ₀ on Ω | RM-0 |

The assembly is **W3-RM:RM-0@1.0.0** (RM `STATEMENT.md:160-176`), which holds for any design and any deterministic
Q ⊇ S₀ with |Q| ≤ K — no size bound on Q enters it — together with W3-RM:E4@1.0.0. This ticket supplies [SAND(Q)],
[TL(Q)], [NA(Q)] at polynomial size; [POST] is inherited (§5).

## 3. Assumptions (ids for the registry)

Fixed constants [SL1-1: the two forms have separate constants]. Common: A ≥ 1, s₀, δ₀ ∈ (0, 1).
**Form F:** M, φ₀ ∈ (0, 1], g₀ > 0, η ∈ [0, η_A), **b ∈ (0, β(η, A))**; for the sufficient forms h ≥ 0 with
**h + b < ½**, m₀ ∈ ℕ, δ₁ ∈ (0, 1). **Form R:** c > 0, θ_lo, θ_hi, a₀ > 0, C_L, **b ∈ (0, ½)** (no η; not tied to
β(η, A)), ρ ≥ 0 with **15ρ + b < ½**.

### 3.1 Fixed design (conditions on (X, θ*) and the deterministic set Q only)

* **(T1-F)**, **(FL)** = (FL-16) and (FL-Q), **(V)**: exactly as in RM `STATEMENT.md:91-96`
  ((T1-F) = Theorem 1's hypotheses (H0) of GROW; (FL-16): λ_min(R̂_T) ≥ φ₀² for 1 ≤ |T| ≤ 16; (FL-Q):
  λ_min(R̂_{Q∪{l}}) ≥ φ₀² for every l ∈ [p]; (V): δ²_{U,j} ≥ M_n log n for every j ∈ S₀ and U ⊆ [p] ∖ {j}, |U| ≤ 15,
  with a deterministic M_n → ∞).
* **(L^b) Polynomial leakage.** A deterministic Q = Q_n with S₀ ⊆ Q ⊆ [p] such that
  (L-size^b) **|Q| ≤ n^b**;
  (L-feas) |Q| ≤ K, and Q = [p] or K ≥ 2|Q| + 32s₀ + 1, for n ≥ n₀ (as RM);
  (L-gain) for every l ∉ Q and every U ⊆ [p] ∖ {l} with |U| ≤ 15: δ²_{U,l} ≤ η τ²_U log n (as RM, τ-form).
  The constants are tied by b < β(η, A): a larger leak level outside Q leaves room for a smaller Q only.
* **(BM-Q) Signal floor at the lattice scale.** θ*²_min nφ₀²/(σ²(|Q| + log n)) → ∞ (as RM's (N-D)(ii)).
* **(W) Lattice width.** 𝔴_n(δ₀) ≤ 0 for n ≥ n₀ (every u_{T,l}, (T, l) ∈ 𝔓, is defined under (FL-Q)).
  In words: over the whole lattice, the expected largest standardised projection of a Gaussian vector on a residual
  direction u_{T,l} does not exceed the level √(2 log(p/(|T| + 1)) + (1 − δ₀) log n) attached to its set size.
  A cruder sufficient form — **(W-unif)** with parameter δ ∈ (0, (1 − 2b)/2) [SL1-1: the radicand is then positive]:
  E max_𝔓 |u_{T,l}ᵀg| ≤ √(2 log p + (1 − 2b − 2δ) log n) for n ≥ n₀; it implies (W) with δ₀ = δ.
* **Sufficient forms for (W)** (each implies (W) for a suitable δ₀; claim (C3)):
  **(W-χ)** |Q ∖ S₀| ≤ (1 − δ₁) log n — nothing else (this is RM's (N-χ); it forces |Q| = O(log n)).
  **(W-ref) References, atoms, remainder.** There are deterministic objects — a finite family 𝒱_n of linear
  subspaces of ℝⁿ, each of dimension ≤ m₀, with log|𝒱_n| ≤ log p + h log n; a finite set 𝒜_n of unit vectors of ℝⁿ
  and L_n ≥ 0 with L_n² log(|𝒜_n| + 1) = o(log n); ρ_n ≥ 0 with ρ_n²(|Q| + log n) = o(log n); η_n → 0 — such that
  every u_{T,l}, (T, l) ∈ 𝔓, can be written

    u_{T,l} = v + Σ_{a∈𝒜_n} λ_a a + w,  v ∈ V for some V ∈ 𝒱_n, ‖v‖ ≤ 1 + η_n,  Σ_a |λ_a| ≤ L_n,
                                          w ∈ span(X_{Q∪{l}}), ‖w‖ ≤ ρ_n.

  (RM's (N-D)(i) is the case m₀ = 1, 𝒜_n = ∅, v a unit vector of span(X_{Q∪{l}}); there h < ½ and Q polylogarithmic,
  so h + b < ½ for a small b.)
  **(W-loc) Local regressions.** For every l ∈ [p] a deterministic N_l ⊆ Q ∖ {l} with |N_l| ≤ ν_n,
  ν_n log 2 ≤ h log n, and a deterministic L_n ≥ 0 with L_n² log(|Q| + 1) = o(log n), such that

    ‖β̄_{T,l} − β̄_{T∩N_l,l}‖₁ ≤ L_n  and  ‖(I − P_{T∩N_l})x_l‖² ≤ (1 + η_n)‖(I − P_T)x_l‖²  for every (T, l) ∈ 𝔓,

  with a deterministic η_n → 0 (under (FL-Q) the second inequality follows from the first with η_n = L_n²/φ₀²
  whenever L_n → 0). T ∩ N_l need not contain S₀ and may be empty; β_{T∩N_l,l} is the regression of §1 [SL1-2]. In
  words: the regression of any column on any lattice set is carried, up to a small ℓ¹ coefficient error, by at most
  ν_n ≤ h log n/log 2 lattice members attached to that column, h < ½ − b [SL1-opt2]. (When |Q| has genuine polynomial
  order, |Q| ≥ n^{b′} for a fixed b′ > 0, log(|Q| + 1) ≍ log n and L_n → 0 is required; N_l = ∅ is allowed.)
* **Block-relative forms** (weaker; what the sandwich proof consumes): (V_b), (L_b), (FL_b) exactly as in RM
  `STATEMENT.md:118-125`, on the method's actual partition.

### 3.2 Gaussian rows (conditions on (Σ_n, θ*) and Q only)

* **(T1-R)**, **(FL-R)**, **(V-R)**: exactly as in RM `STATEMENT.md:129-136` ((FL-R): λ_min(Σ_{n,S}) ≥ c for
  |S| ≤ 16 + s₀ and for S = Q ∪ {l}, l ∈ [p]; (V-R) = PTV(a₀)).
* **(L-R^b) Polynomial leakage, localised.** A deterministic Q ⊇ S₀ with (L-size^b) |Q| ≤ n^b and (L-feas); for
  every l ∉ Q a deterministic H_l ⊇ {l} ∪ S₀ with **|H_l| ≤ n^ρ**, such that for every U ⊆ [p] ∖ {l} with |U| ≤ 15,
  writing U₀ := U ∩ H_l: (L-gain-R) and (L-loc-R) exactly as in RM `STATEMENT.md:140-142`
  (|Cov(W_l, W_j | W_{U₀})| ≤ C_L n^{−1/2} for j ∈ S₀ ∖ U₀; |Cov(W_l, W_v | W_{U₀})| ≤ r_n and
  |Cov(W_j, W_v | W_{U₀})| ≤ r_n for v ∈ U ∖ H_l, j ∈ S₀ ∖ U₀, with r_n(n log n)^{1/4} → 0). Budget: 15ρ + b < ½.
* **(W-R) Lattice width on the realised design.** Let 𝒲⁰_n := {λ_min(R̂_{Q∪{l}}) ≥ c/2 for every l ∈ [p]} (on it
  every u_{T,l}, (T, l) ∈ 𝔓, is defined, so 𝔴_n(δ₀) is defined for the realised X) and
  𝒲_n := 𝒲⁰_n ∩ {𝔴_n(δ₀) ≤ 0} [SL1-opt3]. (W-R): P(𝒲_n) → 1, for the fixed δ₀ ∈ (0, 1) of the theorem.
  Sufficient, **for every fixed δ₀ ∈ (0, 1 − 2b)** [SL1-1] — **(D-R^b)**: hypotheses (N1), (R1)–(R3) of LOC2 Lemma NA-R (`Theory_work/Wave2/W2-LOC2/lemmas/L2_NAR.md:23-36`)
  for (Σ_n, Q), with its deterministic latent-extension contract (`L2_NAR.md:15-20`), where (N0)'s size bound is
  replaced by |Q| ≤ n^b, b < ½ (frames: log N_n ≤ log p + o(log n); atoms: L_n² log(|𝒜_n| + 1) = o(log n); variance
  ratio η_n → 0). Sufficient for (D-R^b) — **(D-loc^b)**: RM's (D-loc) (`STATEMENT.md:154-156`) with
  L_n² log(|Q| + 1) = o(log n) (so L_n → 0 at polynomial size).

## 4. Claims

**(C1) Theorem RM2-F (fixed design, polynomial leakage).** Setting F, the method as coded, premises and
configuration of §1. Assume (T1-F), (FL), (V), (L^b) with b < β(η, A), (BM-Q) and (W). Then [SAND(Q)], [TL(Q)],
[NA(Q)] and [POST] hold, hence all conclusions of RM-0: there is a data event 𝒢_n with P(𝒢_n) → 1 on which every
admissible output run — every seed, N_e, R′ and calibration outcome — reports Ŝ⁺ = S₀; in particular
P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 and P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − P(U_n) − o(1). On Sand_n(Q) ∩ NA(𝓛) ∩ TL(𝓛) LS0 makes exactly
|S̃₀ ∖ S₀| ≤ |Q ∖ S₀| ≤ n^b moves, all deletions of extras, and its archive has `returned` = S₀, `local_certified` =
true, `local_limit` = false (RM-0(a)); the shipped cap ℓ_n + |S̃₀| is never binding (the old cap `ell_n` is not
covered beyond (W-χ)). The same holds with (V), (L-gain), (FL-16) replaced by the block-relative (V_b), (L_b), (FL_b)
on the method's partition. No delivery claim (P(U_n) → 0 is not asserted).

**(C2) Theorem RM2-R (Gaussian rows, polynomial leakage).** Setting R, the method as coded, any X-measurable
partition with blocks ≤ 16. Assume (T1-R), (FL-R), (V-R), (L-R^b) with 15ρ + b < ½, and (W-R). Then, under the joint
law of (X, ε): [SAND(Q)], [TL(Q)], [NA(Q)], [POST], hence all conclusions of RM-0 as in (C1).

**(C3) Lattice-width lemmas.** Setting F, ‖μ‖² ≤ Mn, p ≤ n^A, deterministic Q ⊇ S₀ with |Q| ≤ K and |Q| ≤ n^b
(any fixed b < 1 for (a), (b)), (FL-Q).
(a) **Lemma NA-W.** (W) ⇒ with c_n(k) := log(n + 1) + 2 log p − 2 log(k + 1) − 4κ_E − 2 (κ_E the score-expansion
constant of the toolkit), P(Z²_{T,l} ≤ c_n(|T|) for all (T, l) ∈ 𝔓) → 1, and [NA(Q)].
(b) **Lemma W-conv (the width condition is forced by the route).** If 𝔴⁺_n(δ₁) ≥ 0 for all large n, then
P(NA(𝓛)) → 0. So, up to the factors (1 ∓ δ) on log n and the factor 2 on p in the levels, (W) is equivalent to the
whole-lattice no-addition event having probability → 1.
(c) **Sufficient forms.** (W-χ) ⇒ (W) for every δ₀ < δ₁; (W-ref) with h + b < ½ ⇒ (W-unif) with
δ = (1 − 2b − 2h)/4 ⇒ (W) with δ₀ = (1 − 2b − 2h)/4; (W-loc) ⇒ (W-ref) with the same h, m₀ = 1, ρ_n = 0, 𝒜_n = the normalised columns of Q,
𝒱_n = {span(u_{T∩N_l,l})}, atom coefficient bound L_n/φ₀ and (1 + η_n)^{1/2} − 1 in place of η_n.

**(C4) Containment.** RM-F is the special case of (C1) in which |Q| ≤ (log n)^κ and (W) is supplied by (W-χ) or by
(N-D)(i) [⊂ (W-ref)] (take b < min(β(η, A), ½ − h)); RM-R is the special case of (C2) with |H_l| ≤ (log n)^κ and
(W-R) supplied by (D-R) (for a δ₀ < 1 − 2b, with b and ρ small) [SL1-1]. So W3-RM2:RM2-F ⇒ W3-RM:RM-F and
W3-RM2:RM2-R ⇒ W3-RM:RM-R at the level of hypotheses and conclusions.

**Bridge lemmas** (each delivers one interface property; "delta" = the source proof is re-run and every use of the
size of Q is re-proved here, not cited outside its stated range):

| id | statement | source engine | new in this ticket |
|---|---|---|---|
| (P0) Toolkit-b | Setting F, ‖μ‖² ≤ Mn, a deterministic family 𝔉 ∋ ∅ of sets of size ≤ J_n with a Gram floor φ₀² on its nonempty members, a deterministic nonempty finite vector set 𝒱𝒱 ⊇ {r_A : A ∈ 𝔉} ∪ {r_A − r_{A′} : A, A′ ∈ 𝔉}, r_A := (I − P_A)μ [SL1-3], and (log\|𝔉\| + log\|𝒱𝒱\| + J_n) log n/n → 0: the events 𝒟₁, 𝒟₂, 𝒟₃ of the GEN-L1 toolkit, defined with t_n := 4(log\|𝔉\| + 2 log n + J_n) and h_n² := 2(log\|𝒱𝒱\| + log n) in place of the source's fixed-cardinality expressions, have P(𝒟₂ᶜ) ≤ n^{−2}, P(𝒟₃ᶜ) ≤ 2/n, and on them the score/contrast conclusions of GEN-L1 L1.2–L1.4 and GROW L0.2(a)–(c) hold with the same κ_E and ω_n log n → 0 | C-GROW:L0.1, L0.2 (sets of size O(log n)); LOC2 L0′ (polylog) | polynomial sizes: for the lattice family J_n = q + 1, t_n + h_n² = O(q + log n) |
| (P1) SAND-F^b | Setting F, ‖μ‖² ≤ Mn, p ≤ n^A, a partition with blocks ≤ 16 that is a function of X, (G3a), (V_b), (L_b) with η, (L-feas), \|Q\| ≤ n^b, b < β(η, A) ⇒ [SAND(Q)] | C-GROW:L3; RM Lemma B2τ (log\|Q\| = o(log n)) | the junk-exclusion margin [½ − η/2 − √(2Aη) − b] log n − o(log n) > 0; ladder unchanged |
| (P2) TL-F^b | (P0) for the lattice family, (FL-Q), (BM-Q), \|Q\| ≤ K ⇒ [TL(Q)] | C-GROW:L2.1; RM Lemma B3 (polylog) | toolkit at polynomial size |
| (P3) NA-W | claim (C3)(a) | C-GROW:L2.2 (uniform level, \|Q\| = O(log n)) | size-dependent level c_n(k); Gaussian concentration of the lattice maximum |
| (P4) W-suff | claim (C3)(c) | C-GROW:L2.3; RM Lemmas NA-F, N-loc | frames of dimension ≤ m₀, ℓ¹ atoms, (W-loc) |
| (P5) W-conv | claim (C3)(b) | — | new |
| (P6) POST-F | (T1-F) ⇒ [POST] | SOP:TH09 (T03♯) | none (inherited, §5) |
| (P7) SAND-R^b | Setting R, (FL-R) on sets ≤ 16 + s₀, (V-R), (L-R^b), 15ρ + b < ½ ⇒ [SAND(Q)] for any X-measurable partition with blocks ≤ 16 | RM Lemmas SAND-R, SAND-R′ (polylog H_l, Q); LOC2 `lemmas/L6_poly.md` §§4–5 (a design family) | reference count n^{15ρ}; ladder needs 15ρ < ½, junk exclusion 15ρ + b < ½; the spherical tail C-GROW:L6.4 is used for all 0 ≤ t ≤ (2A + 3) log n (its proof gives this; re-proved) |
| (P8) F→R | Setting R, (FL-R) on Q ∪ {l}, \|Q\| ≤ n^b, b < ½, (W-R) ⇒ [NA(Q)], [TL(Q)] under the joint law | (P0), (P2), (P3) conditional on X | sample floors on Q ∪ {l} from the entrywise Gram event (q√(log n/n) → 0); energy and (BM-Q) from the fixed θ_lo, θ_hi |
| (P9) D→W | (D-R^b) ⇒ (W-R) for every fixed δ₀ ∈ (0, 1 − 2b) [SL1-1]; (D-loc^b) ⇒ (D-R^b) | W2-LOC2:NA-R (polylog); LOC2 `lemmas/L6_poly.md` §6 (a design family) | polynomial lattice: sample/population errors O((q + log n)/√n) → 0; passage from a joint-law bound on max\|Z_{T,l}\| to the conditional mean (median–mean for a Lipschitz functional) |
| (P10) POST-R | (T1-R) ⇒ [POST] | W2-APP:POST (through RM Lemma B9) | none (inherited, §5) |

**(C5) Examples table** (families verifying the assumptions; verification is a proof obligation of the last leg; no
family appears in (C1)–(C4)). Form F: every example of RM-F (by (C4)); exact-Gram designs whose Gram matrix has
spectrum in [c, C] and polynomial off-diagonal decay of exponent α > 2 on a line (leakage radius
≍ (n/log n)^{1/(2α)}, so any b > 1/(2α) works for large n, b < ¼ available; (W-loc) from the inverse-decay bound
W2-LOC2:Lemma-IR applied to the Gram matrix; the truth-separation and coefficient conditions are to be specified with
the verification [SL1-opt4]); **candidate, not verified**: exact-Gram designs with one equicorrelated leak group of
size ≍ n^b around one truth ((W) by a direct width computation; heuristic range 8b < 2A + 1). Form R: UNI-0's class
and LOC-BF's class (by (C4)); polynomial covariance decay α > 17/2 (the class of W2-LOC2:Thm-Poly). There the
construction gives |Q| = O(n^{1/(2α)}) and |H_l| = O(n^{ρ*}) with multiplicative constants, for any ρ* > 1/(4α); take
b > 1/(2α) and ρ > ρ* with 15ρ + b < ½ — possible exactly because α > 17/2 leaves strict slack [SL1-5]; (D-R^b) by
its (P16)–(P17).

**(C6) Sharpness record** — `SHARPNESS.md` (written with the proofs; `ASSUMPTION_MAP.md` now): per assumption, what
is proved, what is observed, what is open. In particular: b < ½ is where the size penalty log(p/k) + ½ log n of one
more variable stops dominating the best of p pure-noise gains (≈ log p) at model sizes k ≈ √n — the level at which
both the sandwich in a deterministic Q and whole-lattice no-addition are expected to fail; whether the *conclusion*
fails there is open (path-level).

## 5. Dependencies (registry id@version; statuses verbatim; PROTOCOL rule 11)

Consumed as proved results (ACTIVE, "PROVED-CHECKED"): W3-RM:RM-0@1.0.0, W3-RM:E4@1.0.0 (assembly and centre);
C-GROW:L0.1@1.0.0, C-GROW:L0.2@1.0.0, C-GROW:L1.1@1.0.0, C-GROW:L1.2@1.0.0, C-GROW:L2.1@1.0.0, C-GROW:L2.2@1.0.0,
C-GROW:L3@1.0.0, C-GROW:L6.4@1.0.0 (engines whose proofs are re-run at polynomial size: each step that uses the size
of Q or of a reference family is re-proved in this ticket); W3-RM:RM-F@1.0.0, W3-RM:RM-R@1.0.0 (containment (C4)
only); W2-UNI:UNI-0@1.1.0 (examples only).
Consumed below PROVED-CHECKED — **explicit conditions of (C1)/(C2), carried into their status** ("conditional on …"):
* SOP:TH09@1.0.0 (Theorem 1, T03♯; full registry status [SL1-6]: "T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED
  (A-REV2). T02(i♯), T02(ii♯): PROVED; SF/XF VERIFIED. T01–T03: PROVED-LOCKED (wave 3; external review queued),
  SAME-FAMILY-ONLY") — gives [POST] under (T1-F); (C1) is conditional on it.
* W2-APP:POST@1.0.1 (full registry status [SL1-6]: "PROVED (by this seat, unchecked); R02 VERIFIED-WITH-AMENDMENTS,
  applied") — gives [POST] under (T1-R); (C2) is conditional on it.
* W1-GEN:L1@1.0.0 (score toolkit, status "PROVED (by this seat, unchecked)") — (P0) re-runs its proof at general
  cardinalities; its statements at fixed set size are used through C-GROW:L0.1/L0.2. (C1)–(C3) are conditional on it
  unless (P0) is written self-contained (planned).
* W2-LOC2:NA-R@1.0.0, W2-LOC2:Thm-Poly@1.0.1, W2-LOC2:Lemma-IR@1.0.0, the RM lemma rows W3-RM:B2tau, B3, NA-F,
  SAND-R, SAND-Rp@1.0.0 (statuses "PROVED (by this seat, unchecked)"; each inside a PROVED-CHECKED ticket): used as
  **templates** for delta proofs and for the examples; no conclusion of them is consumed outside its stated range.
Implementation premises as RM §1 (named, not proved).

## 6. Not claimed

* **The theorem without a lattice condition**: (V) + (L^b) + floors alone, for any b > 0 (or for |Q| ≤ C log n with
  arbitrary C). The route needs whole-lattice no-addition, and by (C3)(b) that event is equivalent to (W) up to
  constants; a statement without (W) needs path-level control of LS0 (separate ticket; PROTOCOL rule 14).
* **b ≥ ½**, or b ≥ β(η, A) in Form F; leakage sets that are not deterministic (data-dependent envelopes).
* (W) from (V), (L) and the floors; necessity of (W), (BM-Q), (V), the floors or the constant β(η, A) for the
  *conclusion* Ŝ⁺ = S₀ (only the route statement (C3)(b) is claimed).
* An improvement of W2-LOC2:Thm-Poly's cutoff α > 17/2 (Form R reproduces it: 15ρ + b < ½ with ρ > 1/(4α),
  b = 1/(2α)); removing the localisation clause (L-loc-R).
* Non-Gaussian rows or errors; growing s₀; θ*_min → 0 in Form R; masked truths; delivery P(U_n) → 0; finite-n
  statements; a binary64 theorem (everything is under EX-A); runs outside the configuration of §1; any change to
  shipped components.

## 7. Registry block (draft; statuses are targets, nothing is proved) [SL1-4]

Headline rows list only the hypotheses the theorem assumes; the sufficient forms are registered as separate
implication lemmas (W-suff, D-to-W). Every bridge is an explicit `depends_on` edge (PROTOCOL rule 16). The size
budgets are recorded as sufficient budgets of the present arguments (ARTEFACT), not as necessary conditions.

```
REGISTRY
claim: W3-RM2:RM2-F | kind: theorem | statement: STATEMENT.md:(C1) | premises: STATEMENT.md:§1,§3.1
status: TARGET (not proved); when proved: conditional on SOP:TH09@1.0.0 and on W1-GEN:L1@1.0.0 unless (P0) is self-contained | status_source: STATEMENT.md:4
assumptions: A:T1-F ; A:FL-16 ; A:FL-Q ; A:V ; A:L-gain ; A:L-feas ; A:BM-Q ; A:L-size-b (new | polynomial leakage size | |Q| <= n^b, b < beta(eta,A) | STATEMENT.md §3.1 | shared yes | P1 SAND-F^b) ; A:W (new | lattice width | w_n(delta0) <= 0 | STATEMENT.md §1,§3.1 | shared yes | P3 NA-W)
consumes: P:POST ; P:SAND(Q) ; P:TL(Q) ; P:NA(Q) ; P:E4
conclusion: reported-model: one data event of probability -> 1 on which every admissible output run reports S0 | rate: none claimed | scope: fixed design; s0 fixed; p <= n^A (p >> n allowed); |Q| <= n^b
depends_on: W3-RM:RM-0@stmt ; W3-RM:E4@stmt ; SOP:TH09@hyp ; W1-GEN:L1@hyp ; W3-RM2:Toolkit-b@stmt ; W3-RM2:SAND-F-b@stmt ; W3-RM2:TL-F-b@stmt ; W3-RM2:NA-W@stmt
implies: W3-RM:RM-F (special case |Q| polylog, (W) from (N-chi) or (N-D)(i) through W3-RM2:W-suff; claim (C4))
sharpness: A:W = NECESSARY-FOR-ROUTE up to the slack delta (target: Lemma W-conv; for whole-lattice no-addition, not for reporting) ; A:L-size-b = ARTEFACT (sufficient budget of the junk-exclusion argument; necessity open) ; A:BM-Q = WEAKENABLE (target) ; A:V, A:L-gain, A:FL = as W3-RM
binding: A:W forced by P:NA(Q) via Lemma W-conv [whole-lattice route only] ; A:L-size-b enters P:SAND(Q) via the junk-exclusion margin [artefact-threshold]
gates: correct:PENDING ; lit:PENDING ; necessity:PENDING ; better:PENDING
council: none yet

claim: W3-RM2:RM2-R | kind: theorem | statement: STATEMENT.md:(C2) | premises: STATEMENT.md:§1,§3.2
status: TARGET (not proved); when proved: conditional on W2-APP:POST@1.0.1 and on W1-GEN:L1@1.0.0 unless (P0) is self-contained | status_source: STATEMENT.md:4
assumptions: A:T1-R ; A:FL-R ; A:V-R ; A:L-gain-R ; A:L-loc-R ; A:L-feas ; A:L-size-b-R (new | polynomial leakage size, Gaussian rows | |Q| <= n^b, b < 1/2 | STATEMENT.md §3.2 | shared no | P7 SAND-R^b) ; A:H-size-rho (new | reference neighbourhood size | |H_l| <= n^rho, 15 rho + b < 1/2 | STATEMENT.md §3.2 | shared no | P7 SAND-R^b) ; A:W-R (new | lattice width on the realised design | P(W_n) -> 1 | STATEMENT.md §3.2 | shared yes | P8 F-to-R)
consumes: P:POST ; P:SAND(Q) ; P:TL(Q) ; P:NA(Q) ; P:E4
conclusion: reported-model: as RM2-F under the joint law of (X, eps) | rate: none claimed | scope: Gaussian rows; s0 fixed; p <= n^A (p >> n allowed); |Q| <= n^b, |H_l| <= n^rho
depends_on: W3-RM:RM-0@stmt ; W3-RM:E4@stmt ; W2-APP:POST@hyp ; W1-GEN:L1@hyp ; W3-RM2:Toolkit-b@stmt ; W3-RM2:SAND-R-b@stmt ; W3-RM2:F-to-R@stmt ; W3-RM2:TL-F-b@stmt ; W3-RM2:NA-W@stmt
implies: W3-RM:RM-R (special case, (W-R) from (D-R) through W3-RM2:D-to-W; claim (C4))
sharpness: A:W-R = NECESSARY-FOR-ROUTE up to slack (target; whole-lattice route only) ; A:H-size-rho = ARTEFACT (reference counting; 17/2-type threshold) ; A:L-size-b-R = ARTEFACT (sufficient budget; necessity open)
binding: A:H-size-rho enters P:SAND(Q) via the reference count n^{15 rho} [artefact-threshold]
gates: correct:PENDING ; lit:PENDING ; necessity:PENDING ; better:PENDING
council: none yet

claim: W3-RM2:Toolkit-b | kind: lemma | statement: STATEMENT.md:(P0) | premises: STATEMENT.md:§1
status: TARGET (not proved) | status_source: STATEMENT.md:4
depends_on: W1-GEN:L1@hyp ; C-GROW:L0.1@proof ; C-GROW:L0.2@proof
claim: W3-RM2:SAND-F-b | kind: lemma | statement: STATEMENT.md:(P1) | premises: STATEMENT.md:§1,§3.1
status: TARGET (not proved) | status_source: STATEMENT.md:4
depends_on: C-GROW:L3@proof ; W3-RM2:Toolkit-b@stmt
claim: W3-RM2:TL-F-b | kind: lemma | statement: STATEMENT.md:(P2) | premises: STATEMENT.md:§1,§3.1
status: TARGET (not proved) | status_source: STATEMENT.md:4
depends_on: C-GROW:L2.1@proof ; W3-RM2:Toolkit-b@stmt
claim: W3-RM2:NA-W | kind: lemma | statement: STATEMENT.md:(C3)(a) | premises: STATEMENT.md:§1,§3.1
status: TARGET (not proved) | status_source: STATEMENT.md:4
depends_on: C-GROW:L2.2@proof ; W3-RM2:Toolkit-b@stmt
claim: W3-RM2:W-conv | kind: lemma | statement: STATEMENT.md:(C3)(b) | premises: STATEMENT.md:§1,§3.1
status: TARGET (not proved) | status_source: STATEMENT.md:4
depends_on: W3-RM2:Toolkit-b@stmt
claim: W3-RM2:W-suff | kind: lemma | statement: STATEMENT.md:(C3)(c) | premises: STATEMENT.md:§1,§3.1
status: TARGET (not proved) | status_source: STATEMENT.md:4
assumptions: A:W-chi ; A:W-ref (new) ; A:W-loc (new)  [alternatives, not a conjunction: each implies A:W]
implies: A:W-chi => A:W ; A:W-ref => A:W ; A:W-loc => A:W-ref
claim: W3-RM2:SAND-R-b | kind: lemma | statement: STATEMENT.md:(P7) | premises: STATEMENT.md:§1,§3.2
status: TARGET (not proved) | status_source: STATEMENT.md:4
depends_on: C-GROW:L6.4@proof ; W3-RM2:Toolkit-b@stmt
claim: W3-RM2:F-to-R | kind: lemma | statement: STATEMENT.md:(P8) | premises: STATEMENT.md:§1,§3.2
status: TARGET (not proved) | status_source: STATEMENT.md:4
depends_on: W3-RM2:Toolkit-b@stmt ; W3-RM2:TL-F-b@stmt ; W3-RM2:NA-W@stmt
claim: W3-RM2:D-to-W | kind: lemma | statement: STATEMENT.md:(P9) | premises: STATEMENT.md:§1,§3.2
status: TARGET (not proved) | status_source: STATEMENT.md:4
assumptions: A:D-R-b (new) ; A:D-loc-b (new)  [alternatives: A:D-loc-b => A:D-R-b => A:W-R for every delta0 in (0, 1 - 2b)]
```
