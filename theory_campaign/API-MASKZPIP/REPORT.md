# API-MASKZPIP REPORT — two-sided evidence and PIP accuracy in the masked regime

Run API-MASKZPIP (Opus 5.5), branch `theory/API-MASKZPIP`, 2026-11-02, Owls (all compute through `owls_run -j 2`).
Everything here is a **candidate**: not reviewed, not adopted. Proofs are in `PROOF.md`; scripts in `scripts/`,
outputs in `results/` (`python3 scripts/summarise.py` prints all tables). Status words follow `PROTOCOL.md`.

## 1. Headline

1. **Evidence: the lower tail is decided by one number, the temperature at which the population first reaches the
   truth's basin (PROVED, Theorems E1 and E2).** For any kernel, grid and N:
   P(Ẑ_r/Z > (T/η)·[π₀(Aᶜ)/π₀(x_m)]·e^{−φ_{τ_A}D_A}) ≤ η + Nπ₀(A). Here A is the truth's basin, τ_A is the first
   stage with a particle in A, and D_A is the d-gap between the best model and the best model outside A. On a frozen
   path the matching identity log Ẑ_r/Z = (a+Λ)(φ* − φ_τ) + O(1) holds, where φ* is the crossing temperature. So
   **Ẑ underestimates by exactly the log-odds overshoot of a late switch.** This extends F-MASKPIP (N-c) from T = 1 to
   every grid.
2. **Positive side: CONJECTURE, with the idealised case PROVED (E3, Lemma J).** A full-space ESS ≥ 0.9 grid cannot
   make the blind step (Lemma J, PROVED). With exact pair refresh, E(W−1)² = ∏(1+χ²_t/N) − 1 (PROVED; O-PW2 for the
   general exact refresh). "log Ẑ − log Z = O_P(√(T/N)) when V contains the competing pair" (METHODOLOGY §6.7's V11)
   remains a PROOF SKETCH. At p = 18, the engine's log W equals an *exact-refresh* SMC's log W on the same grid in
   every setting: **the evidence loss is a grid effect, not a kernel effect.**
3. **Two-sided consistent evidence exists for a different reported quantity: the top-store sum Z_𝒯 (PROVED,
   deterministic, Prop. P3).** 1 − δ₁ ≤ Z_𝒯/Z ≤ 1 and |PIP^𝒯_j − PIP_j| ≤ δ₁ whenever S₀ ∈ 𝒯. With T03 and discovery
   (O-BGIBBS BG3), Z_𝒯/Z → 1 at rate δ₁ on the masked family. This needs no grid, mixing or second-moment hypothesis.
   The split from Ẑ is Prop W4 made concrete: Z_𝒯 and the PIPs are first-moment / occupancy objects, while Ẑ is a
   product of importance-sampling steps that is χ²-sensitive at the crossing.
4. **PIPs: the bias of the RB PIPs is at most the TV distance of the delivered population from π (PROVED, Thm P1).**
   This bound has no L, B or ρ̄ term. After locking (all particles at S₀) the bias is ≤ δ₁, and the L¹ error is
   ≤ (L+4)ρ̄ + u_π + δ₁ = O_P(log n·√(log n/n)) under T03 (PROVED as a composition, Thm P2). Locking itself is
   O-BGIBBS BG3 (candidate, LH with p fixed).
5. **Per-fit (finite n): one new deterministic item (PROVED, Prop C1).** Ẑ/Z ≤ Ẑ/Z_𝒯 on every run, so Ẑ < Z_𝒯
   *certifies* underestimation. In the 4 study fits re-scored by O-CERT, Ẑ/Z_𝒯 = e^{0.18…0.59}, so no
   underestimation is certified. Island agreement certifies nothing (Cor. E1b, PROVED).

## 2. Statements (full hypotheses in PROOF.md §0)

Common setting: fixed data, successful frozen 𝓒 (EX-A, EX-S, CAL, START), one island, N particles, any frozen grid,
v3 round kernels (q_t-invariant). W := Ẑ_r/Z. The bridge is γ_φ = γ₀e^{φd}, with d = log γ₁ − log γ₀.

- **E1 (two-phase sandwich), PROVED.** If the stage-k populations lie in M for k < t and in M′ for k ≥ t, then
  |log W − Ψ_t| ≤ φ_tη + (1−φ_t)η′, where Ψ_t = log[q_t(x°)/π₀(x°)] + log[π(x*)/q_t(x*)]
  = (a+Λ)(φ* − φ_t) + log π(x*) − log π₀(x°). The terms are a = log π₀(x°)/π₀(x*), Λ = log π(x*)/π(x°) and
  φ* = a/(a+Λ). Corollaries: E1a (late switch ⇒ underestimation e^{(a+Λ)(φ_t−φ*)}), E1b (island agreement is
  uninformative), E1c (one-sided relaxation).
- **E2 (miss bound), PROVED.** (a) E[W·1{no stage-(t−1) particle in A}] ≤ κ_t(A) := q_{t−1}(1_{Aᶜ}h_{t−1,T})
  ≤ [π₀(Aᶜ)/π₀(x_m)]e^{−φ_tD_A}. (b) Markov form. (c) Arrival-temperature form (headline 1). This uses the
  Feynman–Kac martingale of O-PW2 Thm A1 (candidate; standard).
- **Lemma J, PROVED.** χ²(q_t‖q_{t−1}) ≤ χ̄ ⇒ q_t(A)² ≤ (1+χ̄)q_{t−1}(A) for every A.
- **E3, PROVED in the idealisation, PROOF SKETCH beyond it.** Exact refresh gives E(W−1)² = ∏(1+χ²_t/N) − 1. A pure
  pair differing in one coordinate is exactly refreshed by the v3 round. The pair-dominated perturbation is a PROOF
  SKETCH.
- **E4 (dichotomy), PARTLY PROVED.** The upper tail is always O_P(1) (T31(i)). The lower tail is
  −φ_{τ_A}D_A + O_P(log T + log 1/π₀(x_m)) if blind (PROVED), and O_P(√(T/N)) if the grid resolves the crossing
  (CONJECTURE).
- **P1 (bias ≤ TV), PROVED.** |E PIP̂_rj − PIP_j| ≤ TV(ν̄_rP^L, π) ≤ E f_{r,0} + δ₁. Conditionally on the locked event,
  the bias is ≤ δ₁.
- **P2 (L¹ error after delivery), PROVED as a composition** of locked T23(ii) and T12 (R3).
  E[max_j|PIP̂_rj − PIP_j| | 𝓕_T] ≤ f_{r,0} + (L+4)ρ̄ + u_π + δ₁.
- **P3 (top store), PROVED.** Z_𝒯/Z = π(𝒯) and |PIP^𝒯_j − PIP_j| ≤ π(𝒯ᶜ). **P3′**, CONDITIONAL on T03 + discovery:
  consistency at rate δ₁.
- **C1–C3 (per-fit), PROVED.** W ≤ Ẑ/Z_𝒯 surely. The band is log Z ≥ max(log Z_𝒯, log Ẑ − log 20) w.p. ≥ 0.95, with
  no upper bound available. The PIP gap is |PIP̂ − PIP| ≤ |PIP̂ − PIP^𝒯| + π(𝒯ᶜ).

## 3. Proofs

All are in `PROOF.md`. The cruxes:
- E1 is algebra: on a frozen phase every increment is e^{Δd(x)}, and the products telescope to tempered-mass ratios.
- E2 uses one Feynman–Kac step. Condition on 𝓕_{t−1}; on the miss event the future-weight function is integrated
  only over Aᶜ; then bound h by e^{(1−φ_t)d_max}Z̄_t/Z.
- P1 holds because the terminal rounds are π-invariant and use fresh randomness, so the TV distance of the path laws
  equals that of the start laws.
- P3 is a two-line ratio inequality.

## 4. Evidence (p = 18, exact enumeration, engine-faithful simulator from F-MASKPIP/W2-T26)

Script `scripts/maskz_check.py` (designs `masked`, `masked8` of F-MASKPIP; data seed 0; N = 500; 40 islands per
grid; fixed seeds). Grids: the jump grids (0, φ_a, 1) for 18 values of φ_a, G1 = (0,1), G2 = full-space ESS 0.9,
and G3 = the blind V0-restricted grid. "iid" = the same grid run with exact refresh (iid draws from q_{t−1}).

RESULTS_TABLES_PLACEHOLDER

## 5. What fails and why

- **Upgrading the sandwich to a probabilistic two-sided theorem.** E1 is exact but needs a near-frozen path. When the
  populations are diffuse (δ₁ ≈ 0.05–0.1 at p = 18), the visited sets have a d-spread of 20+ nats and the sandwich
  is uninformative (median width ≈ 24 nats in the masked8/n=640 jump grids). The rigorous content in the diffuse case
  is the one-sided E2.
- **A method-level evidence collapse on LH.** My first draft claimed that on LH the method's Ẑ underestimates by
  e^{−Θ(n)/T_e} via the floor φ₁ ≥ 1/T_e. That is **wrong for the method**, for two reasons. The floor 1/T_e belongs
  to the *pilot* (METHODOLOGY §6.6), not to the final grid. And the final grid is built on V, which contains the top
  20p *scored* models by γ₁. O-BGIBBS BG1 says the pilot scores S₀ at stage 1 on LH, so V ∋ S₀ and the grid is
  expected to resolve the crossing. The collapse statement survives only for a blind grid (E4 blind case). The same
  caveat applies to F-MASKPIP's G3 proxy (V0 = distinct π₀ draws), which is blinder than the method's V.
- **A conditional evidence theorem from first moments.** It is impossible (F-MASKPIP M3), and E2 does not change that:
  E2 bounds W from above on the miss event and gives no lower bound on the hit event.
- **Lower-bounding W by a second-moment route in the masked regime.** O-PW2's Theorem C needs an L² mixing defect
  λ_t < 1 and sup-norm control of h. In the masked regime h is of order 1/q_t(S₀) before the crossing, so the route
  is vacuous unless the crossing is resolved, and that is the V11 conjecture.

## 6. Needs escalation

- **V11 / E3(c):** the pair-dominated perturbation, i.e. leakage control of the coupling to the pure-pair island,
  uniformly over the stages near φ*. This is the missing positive half of E4. It needs an independent prover; the
  obstruction is the same sup-norm control of h_{s,T} that O-PW2 flags.
- **E2's use of the FK martingale (O-PW2 A1):** standard, but O-PW2 is itself a candidate. An independent check that
  A1 holds for v3's exact stage order (resample → mutate → record) is worthwhile.
- **(XM) on LH:** log 1/π₀(x_m) = O_P(log n) for x_m = argmax d. At p = 18, x_m ≠ S₀ in every setting. The quantity
  only enters the blind-case bound.

## 7. Outside scope

- At n = 200 the posterior itself is far from 0/1: O-CERT's sure bound π(Ŝ) ≤ e^{F(Ŝ)}/Z_𝒯 gives π(S₀) ≤ 0.37 even
  on exactly correct fits. So δ₁ ≥ 0.63 and every bound involving u_π is vacuous at the study's n. This touches T26
  and T03's relevance, not only this task.
- METHODOLOGY §6.7 already states the evidence failure modes ("off by n^{−1/2} or e^{−Θ(n)} while every self-check
  passes"). E1b gives the reason the self-checks pass: collapsed islands agree.

## 8. Confidence card

| Target | Refined statement | True? | Provable at reasonable cost? | Crux | Method change? |
|---|---|---|---|---|---|
| T26(i) masked, PIPs | E1–P2: the RB PIP bias is ≤ TV(ν̄,π) ≤ E f_{r,0} + δ₁. After locking, the bias is ≤ δ₁ and the L¹ error is ≤ (L+4)ρ̄+u_π+δ₁. | high (PROVED given inputs) | high for the bounds. Locking on LH is BG3 (candidate); general DELIV-POP is OPEN (medium) | population delivery/locking | no |
| T26(ii) masked, evidence via Ẑ | Dichotomy E4: blind ⇒ log W ≤ −φ_{τ_A}D_A + O_P(log T) (PROVED); resolved ⇒ log W = O_P(√(T/N)) | blind half: high; resolved half: medium | blind: done; resolved: medium-low (V11 leakage, sup-norm of h) | does V contain the competing pair; pair-refresh perturbation | no (the rebuild loop already targets it) |
| Evidence via the top store | P3/P3′: Z_𝒯/Z ∈ [1−δ₁, 1] and |PIP^𝒯−PIP| ≤ δ₁ once S₀ ∈ 𝒯 | high (PROVED) | high (composition with T03 + BG3) | discovery (BG3) and T03 | reporting only (report log Z_𝒯 next to log Ẑ) |
| T12/T31 (Prop 2) per fit | C1–C3: W ≤ Ẑ/Z_𝒯 surely; log Z ≥ max(log Z_𝒯, log Ẑ − log 20) w.p. ≥ 0.95; island agreement uninformative | high (PROVED) | done | — | no |
| p ≫ n transfer | E1, E2, Lemma J, E3(a,b), P1, P3, C1–C3 are data-free statements given 𝓒 and hold for any p. LH-specific rates (D_A = Θ(n), locking, discovery) are proved only for exact-Gram p < n / p fixed | high for the generic parts | LH-iid rates: low-medium (O-BGIBBS lists them as CONJECTURE) | uniform gaps over supersets as p → ∞ | no |

## 9. What the paper can claim about the reported Ẑ and PIPs at n = 200

N200_PLACEHOLDER
