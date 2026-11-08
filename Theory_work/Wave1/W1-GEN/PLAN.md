# W1-GEN — PLAN

## Route (one paragraph)
M5(0) reduces reported-HPM consistency to D_n → 0 given S-T. Under OP-LS0 + GUARD-W, D_n ≤ P(LS0 from S̃₀ does not
score S₀). Split: (C1) S̃₀ = S* w.p. → 1 (start-mode law for a general reference S*, by re-running the locked T22(iii)
proof with S₀ → S* and with EXP′ proved by a uniform score expansion, Lemma E); (C2) from every centre inside a bounded
relevance set 𝒱 the production local search reaches S₀ inside 2^𝒱 (Λ-descent via the best-truth-addition lemma under
SE + BM-∞ for states missing a truth; extra deletion beats every outside move for supersets of S₀; SEP keeps the path
inside 𝒱; strict monotonicity of F bounds the number of moves by 2^{v̄}). Assemble with (M5-0) and T03♯.

Why this is not a dead route (05_history.tex table): it does **not** use PGD/region form of Theorem W (RF176) — no
margin between progress and non-progress moves is required inside 𝒱; it does not lock LH (RF208) or use STAB-LH (no-LS0
route); it keeps SE/R/BM (CE169: barrier designs violate fixed SE/fixed-ratio signals and are excluded); it does not use
the common-σ² start (RF150); it does not use literal TD (Prop 1 of W1-T37R); it does not claim PD/repair from the HPM
centre (Lemma 0(b)) — only LS0 from the start mode.

## Lemmas (one file each in lemmas/)
- L1 `L1_lemmaE.md` — uniform score expansion on polynomial families of bounded-size sets with a Gram floor
  (EXP′ on within-block additions, and the two-set comparison (E6)). Adapted from BS/API-PXNGAP/PROOF.md §4 (candidate),
  re-proved.
- L2 `L2_centre.md` — (C1): T22(iii) with reference S*; NL_C + NL_avg(κ) in place of NL_η; EXP′ from L1; T22(i) cited.
- L3 `L3_descent.md` — (C2) probabilistic part: events on which (a) every m ≥ 1 state S ⊆ 𝒱 has an improving
  in-𝒱 neighbour that beats every out-of-𝒱 neighbour; (b) every superset T ⊆ 𝒱 of S₀, T ≠ S₀, has an improving extra
  deletion that beats every out-of-𝒱 neighbour; (c) (L) at S₀.
- L4 `L4_search.md` — (C2) deterministic part: production search semantics on those events (path in 2^𝒱, F strictly
  increasing, ≤ 2^{v̄} − 1 moves, scoring vs certification).
- L5 `L5_assembly.md` — (C3), (C3-fav), (C4) (de-randomisation lemma).
- L6 `L6_instances.md` — (C5) LH, LH-iid, W, study generator.
- L7 `L7_counterexample.md` — (C6).

## Numerics (numerics/, local, small)
- N1 exact scorer + partition + start mode + production local search (Python), unit-checked against formulas.
- N2 falsification of L3/L4: random designs in the class (block-separable signal clusters with masking, AR(1), LH
  exact Gram, LH-iid, random correlated clusters), n ∈ {200, 800, 3200}, ≤ 20 seeds: measure S̃₀ = S*, path ⊆ 𝒱,
  S₀ scored, moves; plus adversarial designs near the boundary (small θ, large ζ).
- N3 population checks of (H1)–(H2) on LH, W, study scenarios S1–S6 (exact Σ computations), VIS-onset estimate.
- N4 counterexample (C6): proxy-flood design, LS0 path length vs ℓ_n.

## Reviews (per protocol)
Statement lock (Codex gpt-6.1-sol high) → per-lemma Sol checks + numerics → mid-point independent Sol review after L3/L4
→ exhaustive sweep (Sol) → council (Sol high + Claude Opus 5.5 high), ≤ 3 rounds.

## Risks
- L2's reuse of T22(iii) with S* ≠ S₀: verify no step uses μ ∈ span X_{S₀} or "l ∉ S₀ ⇒ null".
- L3 uniformity: union bounds over 2^{v̄}·(1 + p + v̄p) sets (polynomial) — fine; the extras-deletion step needs a finite
  family (that is what SEP buys).
- (C5)(b) depends on candidate inputs (W7-B, API-PXNGAP Beta laws) — will be labelled as such.
- (C5)(d): S5 (between-group 0.3) is expected to be outside; at n = 200 nothing is claimed.
