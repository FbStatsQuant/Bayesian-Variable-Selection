# W3-SAMP · ASSUMPTION_MAP (sharpness gate, PROTOCOL Wave 3 rule 3)

Numerics: `numerics/samp_sim.py` (exact T12 island on small Ω, arbitrary γ₀ > 0 and d), `numerics/run_checks.py`
→ `numerics/RESULTS_v1.txt` (seed 20261109); NC probes re-run → `numerics/RESULTS_v1_sec4b.txt` (`sec4.py`, seed 4).

| Id | Where it enters (proof sketch, PLAN.md) | Necessary? | Boundary numerics / evidence | Flag |
|---|---|---|---|---|
| EX-A, H-U, START, KERNEL, CAL, SI, MEAS, POT | Exact identities (MR), iid draws (D), kernel bounds (ST) | KERNEL's invariance is necessary for MR (N1 control NC1 breaks it, W1-N1 RESULTS §4); the rest are idealisations of the code | MR identities: max |z| = 2.70 over 76 tests (RESULTS_v1 §1) | standard (inherited) |
| s₀ ≤ K | S₀ ∈ Ω | yes (else π(S₀) = 0) | — | sharp |
| B ≤ 16 (coded) | constant 19 = B + 3 in ST-c / LT-b | no: λ₀ is far below (B+3)o₁ (1.37 vs 13.6; 1.12 vs 13.2; 4.87 vs 100) | RESULTS_v1 §1 "ST-c" | constant loose, harmless |
| P-CONC (δ → 0) | LT: Markov term δ/(εη), κ₀ ≤ o₁, λ₀ ≤ 19o₁ | κ₀ is attained: a measured path staying at S₀ throughout has RB error exactly κ₀ (ST-b; deterministic); RB PIPs need κ₀ → 0, which needs the posterior Gibbs conditionals at S₀ to degenerate | RESULTS_v1 §3 case dbar = 0.90: P(RB err > .1) ≈ 1 although W ≈ 1 | sharp in form (κ₀ term needed) |
| NC_r | LT: P(W_r < η) term | finite-n illustration only (not an asymptotic witness, LC1 issue 3) of failure without NC: trap example with δ = 0.0099, π₀(S₀) = 1.5e-8: W < 0.01 in 100% of islands, RB error ≥ ½ and MPM wrong in 100% | RESULTS_v1_sec4b "trap" | necessity open |
| NC_r | same | finite-n illustration only of success without NC: "near" example, δ = 0.0039, median W = 3.6e-4 (P(W < .01) = 0.76) yet RB error ≥ .1 in 0.9% of islands with L = 20 terminal rounds (23.5% with L = 5) | RESULTS_v1_sec4b "near" | improvable in form (TR replaces it by a (π, π₀) premise) |
| P-START(T) / T·δ̄ → 0 | C: stagewise Markov + stopping-time sum over T + 1 stages | the factor T is **not** needed in the numerics: at fixed δ̄, E|W − 1| *decreases* in T (δ̄ = 0.168: 0.114, 0.068, 0.035, 0.018 for T = 1, 4, 16, 64; Tδ̄ up to 58 in the δ̄ = 0.90 case with E|W−1| = 0.029) | RESULTS_v1 §3 | **improvable** (T-dependence is a proof artefact) |
| P-START (some start condition) | C | some condition tying the start to S₀ is necessary for the conclusion with fixed small L: the trap example (π₀(S₀) tiny, P-CONC holds) fails | RESULTS_v1_sec4b "trap" | necessary in kind, not in form |
| P-OVL (D_rπ₀(S₀) → ∞) | D: (1 − π₀(S₀))^{D_r} | the draw-miss probability is an **equality** (MC: 0.3754 vs 0.3728, 0.7876 vs 0.7861); for the reported HPM it is only sufficient: S₀ is reached as a particle endpoint in 94–97% of islands where no draw hit it | RESULTS_v1 §5 | sharp for the draw mechanism; improvable for the method (other mechanisms) |
| IND-T | D-ii only (exponent 4D_r) | not needed for D-i or any other claim | — | optional |

## Candidate strengthenings (for HQ; not adopted before the "better theorem" review)

1. **C with min(T, D⁺) instead of T.** With D⁺ := max(0, d(S₀) − min_Ω d), log-concavity gives the per-stage bound
   (1/N)Σ_i e^{Δ_t d(X_i)} ≥ e^{Δ_t d(S₀)}·(1 − c_t x_{t−1}), c_t := min(1, Δ_t D⁺) (x = fraction away from S₀), so the
   stopping-time argument runs with Σ_t c_t ≤ min(T, D⁺) in place of T + 1. Cost: a data quantity D⁺ (not a condition on
   (X, θ*) in closed form). Cheap to add as (C-ii′).
2. **T-free C.** The numerics suggest δ̄ → 0 alone suffices (for every N_e). A proof would need the non-S₀ particles'
   contribution to Ẑ (a two-sided, not one-sided, stage bound); not attempted unless HQ asks.
3. **Terminal-repair route for LT** (replaces NC_r): every round has one independence step at φ = 1; a particle away
   from S₀ jumps there w.p. ≥ π₀(S₀)·min(1, w(S₀)/max w) per round and, by ST, stays w.p. ≥ 1 − λ₀. This gives PIP
   consistency without NC under L·π₀(S₀)/M̃ → ∞ and λ₀M̃/π₀(S₀) → 0, M̃ := max_S [π(S)/π₀(S)]/[π(S₀)/π₀(S₀)] (cf.
   BLIND_astra2 Thm 5's M_n). M̃ is a max over all of Ω and is not controlled by P-CONC/P-START; L = Θ(log n) forces
   π₀(S₀) ≫ 1/log n. Judged weaker in practice than C; recorded only.

## Gate outcome (2026-11-09, after BT1 — `reviews/BT1_better_theorem_astra.md`, `reviews/BT1_disposition.md`)

- **T·δ̄ (C) → removed.** BT1's telescoping proof gives E|W_r − 1| ≤ 2max(δ, (1−δ)o₀) ≤ 2δ̄ for every grid and N_e;
  re-derived (`lemmas/C_theorem.md` Step 4) and falsified (`numerics/RESULTS_v3.txt`, 0 violations). P-START is now
  "π₀(S₀) → 1", no rate. The flag `improvable` is resolved: the remaining δ̄ dependence is linear and natural (N_e = 1).
- **NC_r (LT♯) → complemented** by Theorem TR, whose premise L/M → ∞ concerns (π, π₀) only. TR is sufficient, not
  necessary: in the "near" example M = 1.3e6 (TR vacuous) while the local moves repair the PIPs (RESULTS_v3 TR block).
  NC_r also weakened to a vanishing threshold (LT-e′).
- **D → premise weakened** from δ < ½ to the MAP condition S† = S₀ (exact for the ledger argument).
- Not adopted (recorded for HQ): Gibbs/swap-neighbour discovery bound (BT1 §3.2), pooled secondary estimator (BT1 §4.3,
  not a reported field), ST constant 18.
