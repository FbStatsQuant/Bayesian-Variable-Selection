# X3 — Deterministic soft-gap lemma for ϖ-approximate argmin deletions

Status: **PROVED (by this seat, unchecked)**; lemma check R03 FAILED as written on (iii) (MAJOR) → repaired as R03 proposed;
fresh re-check R03b (Codex Sol high, reviews/R03b_X3_recheck_sol.md): **VERIFIED-WITH-AMENDMENTS**, no FATAL/MAJOR, 3 MINOR
applied (reviews/R03_disposition.md). Falsification numerics: numerics/n3x_softgap.py → N3X_out.txt (random
configurations and adversarial ϖ-approximate choices; the full band containment (viii), the initial-phase bounds
(vii) and the crossing-width consequence of (iii) are checked at every step).

This lemma is purely deterministic. It replaces FACB L4.1(i) (exact gap invariant) when the deletion rule is only
approximately the argmin.

## Setting

𝒩 a finite index set with distinct reals (ξ_l)_{l∈𝒩}; constants B ∈ ℝ, κ′ > 1, ϖ ≥ 0. Kept sets
K_0 := 𝒩 ⊋ K_1 ⊋ … ⊋ K_I, K_{i+1} = K_i ∖ {j_i}, |K_i| ≥ 1 for i < I (any length I ≥ 0: every claim is a statement
about this given **prefix** and uses no step beyond I; R02 item 1). Centres
x_i := (Σ_{l∈K_i}ξ_l + B)/(|K_i| + κ′), so that (drift identity) x_{i+1} = x_i − (ξ_{j_i} − x_i)/(|K_i| − 1 + κ′).
Nondegeneracy: ξ_l ≠ x_i for all l, i. **Rule (R_ϖ):** for every i < I,
  |ξ_{j_i} − x_i| ≤ d_i + 2ϖ,  d_i := min_{l∈K_i}|ξ_l − x_i|.
Define a_i := max{ξ_l : l ∈ K_i, ξ_l < x_i} (−∞ if none), b_i := min{ξ_l : l ∈ K_i, ξ_l > x_i} (+∞ if none),
L_i := x_i − a_i, R_i := b_i − x_i, ω_i := b_i − a_i, D_i := 𝒩 ∖ K_i.
(In X4: 𝒩 = 𝒩*, B = Σ_{S₀}ξ − ϱ, κ′ = s₀ + κ, so x_i = x_{T_i}.)

## Claims

(i) K_i ∩ (a_i, b_i) = ∅ and a_i < x_i < b_i (definitions); if K_i ≠ ∅ at least one side is nonempty (if K_i = ∅,
  e.g. a fully exhausted prefix, a_i = −∞, b_i = +∞ and the hole is the whole line).
(ii) a_i − 2ϖ ≤ ξ_{j_i} ≤ b_i + 2ϖ, and ξ_{j_i} ≤ a_i or ξ_{j_i} ≥ b_i.
(iii) **Crossing.** Call step i a crossing if K_{i+1} has a point strictly between x_{i+1} and x_i. If step i is a
  crossing then both a_i, b_i are finite, d_i = min(L_i, R_i) < 2ϖ/(|K_i| − 2 + κ′) and ω_i ≤ 2d_i + 2ϖ; in particular
  ω_i < 4ϖ if |K_i| ≥ 3, and ω_i < c(κ′)ϖ, c(κ′) := 2 + 4/(κ′ − 1), for every |K_i| ≥ 1 (R03 item 1).
(iv) **Monotonicity.** If step i is not a crossing then a_{i+1} ≤ a_i and b_{i+1} ≥ b_i; in particular ω_{i+1} ≥ ω_i.
(v) If ω_{i₀} ≥ 4ϖ for some i₀ and |K_i| ≥ 3 for i₀ ≤ i < I, then no step i ≥ i₀ is a crossing and [a_i, b_i] ⊆ [a_{i′}, b_{i′}] for i₀ ≤ i ≤ i′ ≤ I.
(vi) In the situation of (v), every l deleted at a step i ∈ [i₀, i′) satisfies a_{i′} − 2ϖ ≤ ξ_l ≤ b_{i′} + 2ϖ.
(vii) **Initial phase (prefix form).** Let Q be the maximal number of points ξ_l in a closed interval of length 9ϖ,
  assume 4Qϖ/(|K_0| − Q − 1 + κ′) ≤ ϖ/10 and |K_i| ≥ 3 for i < I. Put i₀ := min{i ≤ I : ω_i ≥ 4ϖ} (i₀ := ∞ if there is
  none) and M := min(i₀, I). Then M ≤ Q, |x_i − x_0| ≤ ϖ/10 for every i ≤ M, and every point deleted at a step i < M lies
  in [x_0 − 4.1ϖ, x_0 + 4.1ϖ]. (If i₀ > I, the whole prefix is narrow; it then has I ≤ Q steps.)
(viii) **Conclusion.** Under the assumptions of (vii): for every i ≤ I,
  𝒩 ∩ (a_i, b_i) ⊆ D_i ⊆ 𝒩 ∩ (a_i − 4.3ϖ, b_i + 4.3ϖ),
  i.e. D_i is the interval part 𝒩 ∩ (a_i, b_i) plus a subset of the band (a_i − 4.3ϖ, a_i] ∪ [b_i, b_i + 4.3ϖ).
(ix) **Sparse case.** If every two distinct ξ_l differ by more than max(9, c(κ′))ϖ, then for every i ≤ I (any |K_i| ≥ 1),
  no step is a crossing and D_i = 𝒩 ∩ (a_i, b_i) exactly (FACB L4.1(i)).

## Proofs

(i) By definition no kept point lies in (a_i, x_i) ∪ (x_i, b_i), and ξ_l ≠ x_i. If K_i ≠ ∅, nondegeneracy places at least
one kept point on one side of x_i; if K_i = ∅, a_i = −∞, b_i = +∞ and the claims hold trivially (R03b item 1).

(ii) If ξ_{j_i} > x_i then ξ_{j_i} ≥ b_i (b_i is the smallest kept point above x_i) and, as d_i ≤ R_i,
ξ_{j_i} − x_i ≤ R_i + 2ϖ, i.e. ξ_{j_i} ≤ b_i + 2ϖ. Symmetrically if ξ_{j_i} < x_i.

(iii) Suppose ξ_{j_i} > x_i (then x_{i+1} < x_i by the drift identity); write m := |K_i| − 1 + κ′ (> 1) and
h := ξ_{j_i} − x_i = m(x_i − x_{i+1}). A crossing means some kept l ∈ K_{i+1} has x_{i+1} < ξ_l < x_i; then a_i is finite and
a_i ≥ ξ_l > x_{i+1}, so L_i < h/m; and b_i ≤ ξ_{j_i} is finite with R_i ≤ h. By (R_ϖ), h ≤ d_i + 2ϖ.
*Case d_i = L_i:* L_i < (L_i + 2ϖ)/m gives L_i(m − 1) < 2ϖ; and R_i ≤ h ≤ L_i + 2ϖ gives ω_i ≤ 2d_i + 2ϖ.
*Case d_i = R_i < L_i:* R_i < L_i < (R_i + 2ϖ)/m gives R_i(m − 1) < 2ϖ; and L_i < (R_i + 2ϖ)/m < R_i + 2ϖ gives
ω_i < 2d_i + 2ϖ.
In both cases d_i < 2ϖ/(m − 1) = 2ϖ/(|K_i| − 2 + κ′) and ω_i ≤ 2d_i + 2ϖ. If |K_i| ≥ 3 then m − 1 > 2, d_i < ϖ and
ω_i < 4ϖ; in general m − 1 ≥ κ′ − 1, d_i < 2ϖ/(κ′ − 1) and ω_i < c(κ′)ϖ. The case ξ_{j_i} < x_i is the mirror image
(L ↔ R). (The bound is on d_i, not on the side opposite to the deletion: R03's configurations {0.1, −2.1, −10}, B = 12,
κ′ = 2, ϖ = 1, deleting −2.1 (d = R = 0.1, L = 2.1) and its reflection show that a direction-specific bound on L, or a
strict inequality ω < 2d + 2ϖ, would be false.)

(iv) Let ξ_{j_i} > x_i (so x_{i+1} < x_i), no crossing. Kept points of K_{i+1} below x_{i+1}: they are the kept points of K_i
below x_i other than those in [x_{i+1}, x_i) — of which there are none (no crossing; ξ_l ≠ x_{i+1}) — so a_{i+1} = a_i.
Kept points above x_{i+1}: those of K_i above x_i, minus j_i, plus none from (x_{i+1}, x_i]; so b_{i+1} ≥ b_i. The case
ξ_{j_i} < x_i is symmetric (b_{i+1} = b_i, a_{i+1} ≤ a_i).

(v) Induction on i ≥ i₀: ω_i ≥ 4ϖ ⇒ step i is not a crossing (iii) ⇒ [a_i, b_i] ⊆ [a_{i+1}, b_{i+1}] and ω_{i+1} ≥ ω_i ≥ 4ϖ (iv).

(vi) By (ii) at step i, a_i − 2ϖ ≤ ξ_l ≤ b_i + 2ϖ, and [a_i, b_i] ⊆ [a_{i′}, b_{i′}] by (v).

(vii) For a narrow step i (ω_i < 4ϖ, i < I): both a_i, b_i are finite, d_i = min(L_i, R_i) ≤ ω_i/2 < 2ϖ and, by (R_ϖ),
|ξ_{j_i} − x_i| < 4ϖ; by the drift identity |x_{i+1} − x_i| < 4ϖ/(|K_i| − 1 + κ′). Suppose M ≥ Q + 1. Then steps
0, …, Q are all narrow and belong to the prefix (Q < M ≤ I), and |K_i| = |K_0| − i ≥ |K_0| − Q for i ≤ Q. By induction,
for i = 0, …, Q: |x_i − x_0| ≤ i·4ϖ/(|K_0| − Q − 1 + κ′) ≤ 4Qϖ/(|K_0| − Q − 1 + κ′) ≤ ϖ/10 (only the Q increments
x_1 − x_0, …, x_Q − x_{Q−1} are used, R02 item 1). So the Q + 1 deleted points ξ_{j_0}, …, ξ_{j_Q} are distinct and lie in
[x_0 − 4.1ϖ, x_0 + 4.1ϖ], an interval of length 8.2ϖ ≤ 9ϖ — contradicting the definition of Q. Hence M ≤ Q. Repeating
the induction for i = 0, …, M (now M ≤ Q, all steps i < M narrow and in the prefix) gives |x_i − x_0| ≤ ϖ/10 for i ≤ M
and ξ_{j_i} ∈ [x_0 − 4.1ϖ, x_0 + 4.1ϖ] for i < M.

(viii) For i ≤ M: D_i ⊆ [x_0 − 4.1ϖ, x_0 + 4.1ϖ] by (vii); and a_i < x_i ≤ x_0 + ϖ/10, b_i > x_i ≥ x_0 − ϖ/10, so
x_0 − 4.1ϖ > a_i − 4.3ϖ and x_0 + 4.1ϖ < b_i + 4.3ϖ. For M < i ≤ I (then i₀ = M ≤ I): points deleted before i₀ lie in
[x_0 − 4.1ϖ, x_0 + 4.1ϖ] ⊆ (a_{i₀} − 4.3ϖ, b_{i₀} + 4.3ϖ) ⊆ (a_i − 4.3ϖ, b_i + 4.3ϖ) by (v); points deleted at steps in
[i₀, i) lie in [a_i − 2ϖ, b_i + 2ϖ] by (vi). The left inclusion is (i).

(ix) A crossing at step i requires both sides nonempty (iii), hence ω_i ≥ (minimal spacing) > c(κ′)ϖ, contradicting (iii).
So no step is a crossing, and by (iv) the intervals [a_i, b_i] are nested increasing (no |K| restriction is needed for
(iv)). By (ii) and nesting every deleted point lies in [a_i − 2ϖ, b_i + 2ϖ]; the only point of 𝒩 in [b_i, b_i + 2ϖ] is b_i
itself (spacing > 2ϖ) and it is kept, similarly at a_i; so D_i ⊆ (a_i, b_i); the reverse inclusion is (i). ∎

(Zero tolerance, R03b item 2: when ϖ = 0 every finite a_i or b_i is the coordinate of a kept index; distinctness
excludes a deleted point from either finite endpoint, so the closed bound of (vi) gives strict open containment; here
i₀ = M = 0, and for I = 0 the conclusion is immediate from D_0 = ∅.)

**Remark.** For steps with |K_i| ≥ 3, (iii)–(v) are the whole mechanism: a kept point can be overtaken by the centre
only when the hole around the centre is narrower than 4ϖ; once the hole is ≥ 4ϖ wide it only grows, as in FACB L4.1,
and each new deletion overshoots the current kept edge by at most 2ϖ. With fewer kept points the threshold is c(κ′)ϖ
instead (R03b item 3: e.g. {−3/2, 7/2}, B = −2, κ′ = 11/10, ϖ = 1, deleting 7/2 crosses although the hole is 5 ≥ 4ϖ
wide; (iii) with c(11/10) = 42 is not violated).
