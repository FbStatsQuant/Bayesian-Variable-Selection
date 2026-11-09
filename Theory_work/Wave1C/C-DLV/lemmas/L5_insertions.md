# L5 — How many points does the construction insert? Two-model transition lemma (deterministic)

Status: PROVED (by this seat); R03 (Codex xhigh): Lemmas 5.0, 5.1, 5.2, 5.2′ VERIFIED / VERIFIED-WITH-AMENDMENTS,
Corollary 5.3 ERROR as first written → corrected below (v2). Notation of L3 (ℓ_S, F, q_t, ρ, Δ). EX-A.
A *trial* of the construction is one pass of the loop at a point u; it is *bisection-limited* if ρ(u, b) < 0.90 at its
current target b (L3 Lemma 3.4(a)). N_b^try counts bisection-limited trials; N_b^app ≤ N_b^try counts those that
append an interval. The interval identity of L3 Lemma 3.4(b) uses N_b^app. (R03 #3.) A bisection-limited trial that
appends never appends a snapped point: if lo were snapped to 1 then ρ(u, 1) ≤ ρ(u, b) < 0.90 (monotonicity) and
validation fails, so such a trial ends the construction (event (γ)).

## Lemma 5.0 (bisection step length). If a trial from u is bisection-limited and some mid passes, the raw passing point
v_raw := lo and the last failing tested point w = u + h (= hi) satisfy v_raw − u ≥ h/2, ρ(u, w) < 0.90, and
ρ(u, v_raw) ≥ 0.90 (before any snap; R03 #5).
*Proof.* With lo = u, hi = b and 60 halvings (v3_calib.h:83-85), at the end hi − lo = (b − u)2⁻⁶⁰; hi has failed
(either hi = b, which failed, or hi was set at a failing mid) and lo = v passed. Progress means some mid passed, so
lo − u = jδ with δ = (b − u)2⁻⁶⁰ and an integer j ≥ 1, so h = hi − u = (j + 1)δ ≤ 2jδ = 2(lo − u). ∎

## Lemma 5.1 (two-model closed form). For M₁, M₂ with d(M₂) − d(M₁) = D > 0, let x(t) := ℓ_{M₂}(t) − ℓ_{M₁}(t) = x₀ + tD
and, for the two-point family on {M₁, M₂}, ρ⁽²⁾(u, v) = 1 − a(c − 1)²/((1 + a)(1 + ac²)) with a = e^{x(u)}, c = e^{(v−u)D}.
Moreover, for all a > 0 and c ≥ 1: (i) 1 − ρ⁽²⁾ ≤ tanh²((v − u)D/2); (ii) 1 − ρ⁽²⁾ ≤ 1/(1 + a);
(iii) 1 − ρ⁽²⁾ ≤ ac²/(1 + ac²).
*Proof.* By Lemma 3.1 with M = M₂ on the two-point family, ρ⁽²⁾ = σ(x)σ(x+2s)/σ(x+s)² with σ(z) = e^z/(1+e^z),
s = (v − u)D; simplifying gives (1 + ac)²/((1 + a)(1 + ac²)), and (1 + ac)² − (1 + a)(1 + ac²) = −a(c − 1)².
(i) a/((1 + a)(1 + ac²)) is maximised over a > 0 at a = 1/c with value 1/(1 + c)², and (c − 1)²/(c + 1)² =
tanh²(s/2). (ii) a(c−1)² ≤ ac² ≤ 1 + ac². (iii) (c − 1)² ≤ c² and 1 + a ≥ 1. ∎

## Lemma 5.2 (insertions on a two-model family with an ε-remainder). Let V ∋ M₁, M₂ with D = d(M₂) − d(M₁) > 0 and
suppose r_t := 1 − q_t(M₁) − q_t(M₂) ≤ ε for all t ∈ [0, 2], with ε ∈ [0, 0.02]. Put θ := 0.90/(1 − ε)² (< 0.94),
x₀ := ℓ_{M₂}(0) − ℓ_{M₁}(0) = log γ₀(M₂)/γ₀(M₁), s_θ := 2 artanh √(1 − θ), λ_θ := log(θ/(1 − θ)). Then the number of
bisection-limited steps of any construction on V (any pilot targets in [0, 1]) satisfies
  N_b^try ≤ N̄_b := 1 + ⌈(2λ_θ + 2s_θ)/(s_θ/2)⌉ + ⌈log_{4/3} max{1, (−x₀ − λ_θ)/(2s_θ)}⌉
(counting the starting coordinates of the trials, so a final unappended trial is included; R03 #3, #6).
With ε = 0.01 the exact constants are θ = 0.918273…, s_θ = 0.588143…, λ_θ = 2.419118…,
(2λ_θ + 2s_θ)/(s_θ/2) = 20.4525…, so N̄_b = 22 + ⌈log_{4/3} max{1, (−x₀ − λ_θ)/(2s_θ)}⌉ = O(1 + log(1 + |x₀|)).
(The rounded form 22 + ⌈log_{4/3} max{1, (−x₀ − 2.42)/1.18}⌉ is NOT a direct substitution; use the exact form.)
*Proof.* Let q⁽²⁾ be the two-point family on {M₁, M₂} (same lines). Then q_t(M₂) = (1 − r_t) q⁽²⁾_t(M₂), so by Lemma
3.1 (with M = M₂) applied to both families,
  ρ(u, v) = ρ⁽²⁾(u, v) · (1 − r_u)(1 − r_{2v−u})/(1 − r_v)²,  hence (1 − ε)² ρ⁽²⁾ ≤ ρ ≤ ρ⁽²⁾/(1 − ε)²
for 0 ≤ u ≤ v ≤ 1 (all three points lie in [0, 2]). So ρ⁽²⁾(u, v) ≥ θ ⇒ ρ(u, v) ≥ 0.90, and ρ(u, w) < 0.90 ⇒
ρ⁽²⁾(u, w) < 0.90/(1 − ε)² = θ.
Work in the coordinate x = x(u). By Lemma 5.1, ρ⁽²⁾(u, v) ≥ θ whenever (A) a/(1 + a) ≥ θ, i.e. x ≥ λ_θ (any v); or
(B) tanh²(sD/2) ≤ 1 − θ, i.e. sD ≤ s_θ (s = v − u); or (C) ac² ≤ (1 − θ)/θ, i.e. x + 2sD ≤ −λ_θ.
Take a bisection-limited step from u with x = x(u), failing w = u + h, accepted v (Lemma 5.0). Since ρ⁽²⁾(u, w) < θ:
by (A), x < λ_θ; by (B), hD > s_θ; by (C), x + 2hD > −λ_θ. With v − u ≥ h/2, the next coordinate x′ = x(v) satisfies
  x′ − x ≥ hD/2 > max{ s_θ/2, (−λ_θ − x)/4 }.
Phase 1 (x < −λ_θ − 2s_θ): put y = −λ_θ − x > 2s_θ; then y′ ≤ y − y/4 = (3/4)y. The number of Phase-1 steps is at most
⌈log_{4/3} max{1, (−x₀ − λ_θ)/(2s_θ)}⌉ (the coordinate only increases between steps, also along non-bisection steps,
since D > 0 and u increases). Phase 2 (−λ_θ − 2s_θ ≤ x < λ_θ): each step increases x by > s_θ/2, so at most ⌈(2λ_θ + 2s_θ)/(s_θ/2)⌉ steps
Phase 3 (x ≥ λ_θ): no bisection-limited step by (A). Summing gives
the bound; for ε = 0.01, (2λ_θ + 2s_θ)/(s_θ/2) = 20.45 → 21.
Indexing (R05 #3). Every bisection-limited trial either appends an interval (then some mid passed and Lemma 5.0 applies)
or ends the construction (terminal `non_progress`, or terminal failed validation after a snap — no mid-passing
conclusion is used for it). There is at most one terminal trial. For the appended trials, count by starting coordinate:
those starting in Phase 1 have starting values y > 2s_θ with y_{j+1} < (3/4)y_j, so there are at most
⌈log_{4/3} max{1, y₀/(2s_θ)}⌉ of them (y₀ = −λ_θ − x₀); those starting in Phase 2 have starting coordinates in an
interval of width 2λ_θ + 2s_θ, consecutive ones more than s_θ/2 apart, so at most ⌈(2λ_θ + 2s_θ)/(s_θ/2)⌉ of them; none
starts in Phase 3. The additive 1 in N̄_b is reserved for the terminal trial. ∎

## Lemma 5.2′ (the remainder needs control only on [0, 1 + η]). Let η ∈ (0, 1] and replace the hypothesis of Lemma
5.2 by r_t ≤ ε for t ∈ [0, 1 + η] (ε ∈ [0, 0.02]). Then
  N_b^try ≤ N̄_b′ := N̄_b + ⌈log_{4/3}((1 + η)/η)⌉   (N̄_b as in Lemma 5.2).
(For η = 1/4, the last term is ⌈log_{4/3} 5⌉ = 6.)
*Proof.* Classify each bisection-limited step from u by its last failing test w (Lemma 5.0). Type I: 2w − u ≤ 1 + η.
Then u, w, 2w − u ∈ [0, 1 + η], the perturbation inequality of Lemma 5.2 applies at (u, w), and the step obeys
x < λ_θ and x′ − x > max{s_θ/2, (−λ_θ − x)/4} exactly as there. Type II: 2w − u > 1 + η. Then w − u > (1 + η − u)/2,
so v − u ≥ (w − u)/2 > z/4 with z := 1 + η − u, i.e. z′ < (3/4)z. Along every step of the construction u increases,
so x(u) is non-decreasing and z(u) decreasing; hence the Phase-1 contraction and the Phase-2 increments of Lemma 5.2
hold for appended Type-I trials whatever steps lie in between, and their count is bounded by the two phase terms of
Lemma 5.2. Appended Type-II trials, counted by their starting value z = 1 + η − u: inside the loop u < 1, so each
starts at z > η, and each appended Type-II step multiplies z by < 3/4 (other steps only decrease z); so k of them
satisfy η < z_k < (3/4)^{k−1}(1 + η), giving k ≤ ⌈log_{4/3}((1 + η)/η)⌉. The type classification uses the last failing
test w only for appended trials (Lemma 5.0); the single possible terminal trial (non_progress or failed post-snap
validation) is covered by the additive 1 of N̄_b, as in Lemma 5.2. Add the counts. ∎
*Why this matters.* For t > 1 the tilted family γ₀^{1−t}γ₁^{t} over-rewards models the start under-weights relative to
the target (e.g. S₀ ∪ {j} for noise j with a large partial score); with p = n^{a} these can overtake S₀ only beyond a
t_c > 1 (heuristic, orthogonal-block approximation for LH with p = n^{1/3}: t_c ≈ 1.5–1.6; not proved). Lemma 5.2′ needs control only up to
1 + η.

## Corollary 5.3 (what the two-model hypothesis buys; corrected after R03 #1, #2, #7). Let N̄ be the bound of the
applicable lemma: N̄ = N̄_b under the hypothesis of Lemma 5.2 (remainder ≤ ε on [0, 2]), N̄ = N̄_b′ under Lemma 5.2′
(remainder ≤ ε on [0, 1 + η]). For a construction at tier e with pilot count k:
(a) if k + N̄ ≤ T_e, the construction cannot fail through `too_many_intervals` (#intervals ≤ k + N_b^app ≤ k + N̄);
(b) `non_progress` is impossible at a trial from u with target b whenever (b − u)2⁻⁶⁰ ≤ s_θ/D: the smallest mid
    m = u + (b − u)2⁻⁶⁰ has 2m − u = u + 2⁻⁵⁹(b − u) ≤ b ≤ 1, so the remainder bound applies at u, m, 2m − u, and
    (m − u)D ≤ s_θ gives ρ⁽²⁾ ≥ θ by (B), hence ρ(u, m) ≥ 0.90; by the bisection semantics (L3 Lemma 3.4(c)) some mid then
    passes. A sufficient uniform condition is D ≤ s_θ2⁶⁰;
(c) validation after a snap (event (γ)) is NOT excluded by the hypothesis: R03 exhibits a two-model family with
    modest D (D = log 2/(1 − 2⁻⁴²), targets {0, 1}) whose exact passing boundary 1 − 2⁻⁴² lies in the snap band and
    fails validation at 1.
So, under the hypothesis, the construction fails only if k > T_e − N̄, or (β) at a trial with (b − u)2⁻⁶⁰ > s_θ/D, or
(γ). Using N̄_b instead of N̄_b′ under the shorter-range hypothesis is FALSE: R03 #1 gives a three-model family with the
remainder < 0.005 on [0, 1 + 2⁻⁴⁰] and k = 978 that overflows at interval 1001 although 978 + 22 ≤ 1000.

## Remark 5.4 (scope; what is not proved; MEASURED: the hypothesis fails at the sizes run).
(0) Numerics N3 (numerics/N3_SUMMARY.md, N3_twomodel.csv; 51 constructions from 16 production fits, masked and
favourable designs, (n,p) = (800,108), (1600,135)): replaying `build_grid` on the saved V and pilot schedule
reproduces the code's grid in 51/51 constructions (max abs diff 9.8·10⁻¹³), which validates L3's reading of the
constructor; but with the selected pair M₁ = argmax_V log γ₀, M₂ = argmax_V log γ₁ the sampled remainder maximum r_max
is ≥ 0.129 on [0, 2] and ≥ 0.08 on
[0, 1.25] in every construction (median 0.50 and 0.18). So Lemmas 5.2/5.2′ do NOT apply to the realised candidate
sets with the selected pair (in 7/51 constructions M₁ = M₂, so no admissible pair was tested there; other pairs were not
searched — R06 #7): the observed small insertion counts (max 10) are not explained by the lemmas at these sizes. Whether
an asymptotic two-model regime exists on the classes is CONJECTURAL (open: the data-only remainder bound and the
candidate-inclusion event below). (a) The hypothesis r_t ≤ ε on [0, 1 + η] (Lemma 5.2′) is a structural
property of the realised candidate set V: one "start-side" model and one "target-side" model carry all but ε of the
tilted mass along the path, including part of the extrapolated range t > 1 used by ρ(u, v) through F(2v − u). If
M₁, M₂ ∈ V, then r_t^V ≤ R_t := Σ_{S ∈ Ω∖{M₁,M₂}} γ_t(S)/max{γ_t(M₁), γ_t(M₂)}, a function of the data only, uniformly
over such V; so the hypothesis splits into an algorithmic event (M₁, M₂ ∈ V at every construction) and a data event
(sup_{[0,1+η]} R_t ≤ ε). Heuristically (not proved), masked LH has
this shape on [0, 1] (M₁ = S* = start mode, M₂ = S₀; x₀ = log γ₀(S₀)/γ₀(S*) ≈ −log(2p) − ½ log n + O(1)), giving
N̄_b = 22 + O(log log n) (if the remainder is controlled on [0, 2]; with Lemma 5.2′ add ⌈log_{4/3}((1+η)/η)⌉). It is NOT proved here that r_t ≤ ε holds w.p. → 1 for the random V of the method; nor for
t ∈ (1, 2] when p grows fast (noise models S₀ ∪ {j} can carry tilted mass at t near 2 when the start under-weights them
relative to the target; see N1 design F). A chain of m transitions gives, by the same argument applied
transition-by-transition, O(m(1 + log|x₀|)) insertions provided the transitions are separated; this is stated, not
proved. (b) The pilot count k is a random functional of the pilot particle system (adaptive ESS on H_e particles with
moves between stages); bounding P(k > T_e − N̄_b) is the as-coded stage-count question of CJ06 (Conjecture P, OPEN) and
is not attempted here.
