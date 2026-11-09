# L3 — Grid construction: exact ESS identity, pilot schedule, success criterion (deterministic)

Status: PROVED (by this seat); R03 (Codex xhigh): 3.1, 3.2, 3.2′, 3.3, 3.5(a) VERIFIED; 3.4, 3.5(b)
VERIFIED-WITH-AMENDMENTS (applied below). Code: `Scripts/SMC_BVS/core/cpp/v3_calib.h` (byte-identical to the study's
v2.2.1 copy), `cpp/v3_engine.h:274-341` (island loop), `v3_calib.R:44-82, 111-122`. Arithmetic: EX-A (exact reals);
the code's constants (0.90, 60 halvings, 1/T_e floor, 1e−12 snap) are kept literally.

## Setting
V finite, nonempty set of models (the candidate set built by `cpp_cal_V`, `v3_core.cpp:671-690`), A(S) = log γ₀(S)
(`lg0`), d(S) = log γ₁(S) − log γ₀(S). For t ∈ ℝ: ℓ_S(t) = A(S) + t d(S), F(t) = log Σ_{S∈V} e^{ℓ_S(t)} (`F_V`,
v3_calib.h:49-53), q_t(S) = e^{ℓ_S(t) − F(t)}. The code's restricted ESS is
ρ(u, v) = exp{2F(v) − F(u) − F(2v − u)} (`rho_V`, v3_calib.h:55-58). Write Δ(u, v) := F(u) − 2F(v) + F(2v − u), so
ρ = e^{−Δ}. c₀ := log(10/9), so ρ ≥ 0.90 ⟺ Δ ≤ c₀.

## Lemma 3.1 (exact identity). For every M ∈ V and all real u, v:
  ρ(u, v) = q_u(M) · q_{2v−u}(M) / q_v(M)².
*Proof.* F(t) = ℓ_M(t) − log q_t(M). ℓ_M is affine, so ℓ_M(u) − 2ℓ_M(v) + ℓ_M(2v−u) = 0 and
Δ(u,v) = −log q_u(M) + 2 log q_v(M) − log q_{2v−u}(M). ∎
*Consequences.* (i) ρ(u,v) ≥ q_u(M)·q_{2v−u}(M) for every M ∈ V (since q_v(M) ≤ 1). (ii) If some M has
q_u(M) ≥ √0.9 and q_{2v−u}(M) ≥ √0.9, the step (u, v) passes.

## Lemma 3.2 (convexity facts). F is convex and C^∞ with F′(t) = E_{q_t}d, F″(t) = Var_{q_t}(d). For u ≤ v,
  Δ(u, v) = ∫_u^{2v−u} (v − u − |t − v|) F″(t) dt,  hence 0 ≤ Δ(u, v) ≤ (v − u)² · sup_{t∈[u, 2v−u]} Var_{q_t}(d),
and v ↦ ρ(u, v) is non-increasing on [u, ∞).
*Proof.* The second difference of a C² function with the Peano kernel K(t) = (h − |t − v|)₊, h = v − u, ∫K = h².
Monotonicity: ∂_v Δ(u,v) = −2F′(v) + 2F′(2v − u) ≥ 0 because F′ is non-decreasing and 2v − u ≥ v. ∎
*Corollary 3.2′ (dominance intervals).* For c ∈ (½, 1) and M ∈ V the set {t : q_t(M) ≥ c} is a (possibly empty)
interval: q_t(M) ≥ c ⟺ Σ_{S≠M} e^{ℓ_S(t) − ℓ_M(t)} ≤ 1/c − 1, a sublevel set of a convex function of t.

## Lemma 3.3 (pilot schedule). At every tier e the pilot's temperatures 0 = φ₀ < φ₁ < … < φ_k = 1 satisfy
k ≤ T_e, and every non-final increment is ≥ 1/T_e. The tier's pilot schedule `pil$schedule` = (φ₀, …, φ_k) is the
target list of every construction at that tier.
*Proof.* Island loop (adaptive branch), v3_engine.h:303-341: the loop exits when φ_prev == 1.0 (:310); otherwise
`pilot_next_phi` (v3_calib.h:30-46) returns either 1.0 (if the step to 1 passes), or the bisection value lo with
lo − φ ≥ 1/T_e (unforced; lo < 1 since every tested mid is < hi ≤ 1), or the forced value f = min(1, φ + 1/T_e),
replaced by 1 when f ≥ 1 − 10⁻¹² (so f ≥ φ + 1/T_e or f = 1). Hence each step is a strict increase, every non-final
step increases φ by ≥ 1/T_e, and the last step lands exactly at 1 (the only values ≥ 1 − 10⁻¹² produced are 1.0, or
an unforced lo < 1, which is not final). If k steps occur, (k − 1)/T_e ≤ φ_{k−1} < 1, so k ≤ T_e; termination
follows. `cpp_cal_pilot` returns sched = (0, φ₁, …, φ_k) (v3_core.cpp:604); `v3_cal_tier` passes `pil$schedule`
to every `build` of that tier (v3_calib.R:44, :68, :79, :111). ∎

## Lemma 3.4 (what the construction does). `build_grid(lg0, d, targets, T_e)` (v3_calib.h:68-98) with the pilot
schedule as targets:
(a) every appended point is either the current target b (the smallest pilot temperature > u) or, if ρ(u,b) < 0.90, the
    bisection value lo ∈ (u, b) (60 halvings with lo = u, hi = b); a point ≥ 1 − 10⁻¹² is snapped to 1;
(b) consequently: an unsnapped step never skips its current target; every pilot temperature strictly below the first
    raw candidate that is snapped to 1 is reached; that candidate is replaced by 1 and later targets are skipped
    (R03 #5). Hence #intervals = N_p′ + N_b^app, where N_b^app counts appended bisection steps (L5) and N_p′ ≤ k ≤ T_e
    counts the steps that end on a pilot temperature or on the snapped value 1;
(c) failure reasons under EX-A: `no_target_above_u` never occurs (1 is a target and u < 1 inside the loop);
    `validation_failed` never occurs for an unsnapped point (ρ(u,v) ≥ 0.90 was tested at that exact v) and for a
    snapped point v = 1 it fails iff ρ(u, 1) < 0.90; `non_progress` occurs iff no tested mid passes. If no mid passes,
    every update is hi = mid, so the 60th test is exactly the smallest dyadic point u + (b − u)2⁻⁶⁰; if some mid passes,
    it is ≥ that point, which therefore passes too (monotonicity, Lemma 3.2). So `non_progress` ⟺
    ρ(u, u + (b − u)2⁻⁶⁰) < 0.90; and once a mid passed, the second progress check (:90) cannot fail (lo > u) (R03 #4).
    `too_many_intervals` occurs iff the interval count exceeds T_e (checked after appending, :93-94).
*Proof.* Direct reading of v3_calib.h:68-98; the monotonicity of ρ(u, ·) is Lemma 3.2. For (b): the target b is the
smallest pilot temperature > u and unsnapped appended points satisfy v ≤ b, so the next u is ≤ b and b remains the
next target until it is appended or a snap to 1 ends the construction. ∎

## Proposition 3.5 (success criterion; grid ⊆ pilot ∪ {1}). Let (φ_i) be the tier's pilot schedule and V the candidate set.
(a) If ρ(u, v) ≥ 0.90 for every pair 0 ≤ u < v ≤ 1 with u ∈ {φ_i} ∪ {snap points} — in particular if
    sup_{t∈[0,2]} Var_{q_t}(d) < c₀, or if some M ∈ V has q_t(M) ≥ √0.9 for t = 0 and t = 2 (hence, by Cor. 3.2′, for
    all t ∈ [0, 2]) — then the construction succeeds; it never bisects, its points are the pilot temperatures up to
    the first one in [1 − 10⁻¹², 1], which is replaced by 1 (later targets are skipped), so its interval count is
    ≤ k ≤ T_e. (It is NOT always exactly the pilot schedule: R01 #2.)
(b) In general the construction succeeds iff no `non_progress`, no failed validation at a snapped point, and
    N_p′ + N_b^app ≤ T_e (appended intervals).
*Proof.* (a) At u = φ_{i−1} the target is b = φ_i and ρ(u, b) ≥ 0.90, so v = b, or v = 1 if b ≥ 1 − 10⁻¹² (then
ρ(u, 1) ≥ 0.90 by the hypothesis, which covers every pair 0 ≤ u < v ≤ 1), validation passes and no bisection happens;
after a snap u = 1 and the loop ends. So N_b = 0, every interval ends at a distinct pilot temperature or at 1, and the
interval count is ≤ k ≤ T_e by Lemma 3.3. The variance version: for 0 ≤ u < v ≤ 1, [u, 2v−u] ⊆ [0, 2] and Lemma 3.2 gives Δ ≤ (v−u)²·sup Var < c₀.
The dominance version: by Cor. 3.2′ the set {q_t(M) ≥ √0.9} is an interval containing 0 and 2, so it contains u and
2v − u ∈ [0, 2]; Lemma 3.1(i) gives ρ ≥ 0.9. (b) is Lemma 3.4(c). ∎

## Remark 3.6 (why (a) is rarely enough; measured). Numerics N1 (`numerics/psi_enum.py`, outputs `N1_psi_F.txt`,
`N1_psi_M.txt`; LH-type p = 27, oracle V = top-20p by γ₀ ∪ top-20p by γ₁ ∪ {∅} over all models of size ≤ 5): the start mode
differs from S₀ (masked design M, at every tested n ≥ 400: start mode {0} vs S₀ = {0, 9}; design F, from n = 1600: the linked proxy
9 enters the start mode {0, 9, 18} vs S₀ = {0, 18}), the sampled maximum of Var over 2001 points of [0, 2] on the oracle V is ≈ 22.98–57,135 (a lower bound on the
supremum, ≫ c₀), yet the
construction with a one-jump pilot (targets {1}) succeeds with only 8–15 intervals (F) and 10 (M), and with a 10-step
pilot 14–21 intervals, against T_e = 1000. So bisection insertions are the normal case; their number is small.
