# W3-SAMP · ASSUMPTION_MAP (sharpness gate, PROTOCOL Wave 3 rule 3) — live registry for STATEMENT v3

Revised 2026-11-09 after SW1 (#7, #8, #11, #24, #25): the table below is the **current** registry for STATEMENT v3; the
gate history (v1/v2 candidates, now superseded) is kept at the end, dated. Numerical evidence = falsification attempts
with no violation detected, on finite targets (`numerics/README.md`); finite targets cannot witness sequence-level
properties.

## Current registry (STATEMENT v3)

| Id | Where it enters | Necessary? / sharpness | Evidence | Flag |
|---|---|---|---|---|
| EX-A, H-U, START, KERNEL, CAL, SI, MEAS, POT | exact identities (MR), iid draws (D), kernel bounds (ST, TR), completed records (PC) | KERNEL's invariance is necessary for MR (W1-N1 control NC1); the rest idealise the code | MR identities max |z| = 2.70 over 76 tests (RESULTS_v1 §1) | inherited |
| IND-T | D-ii only (exponent 4D_r) | not used elsewhere | — | optional |
| s₀ ≤ K | S₀ ∈ Ω | yes | — | sharp |
| B ≤ 16 (coded) | constant 19 = B + 3 in ST-c / LT-b | constant loose (λ₀ ≪ (B+3)o₁ in all tests) | RESULTS_v1 §1 | harmless |
| P-CONC (δ → 0), localised 1_𝒜o₁ → 0 where stated | LT (Markov term, κ₀ ≤ o₁, λ₀ ≤ 19o₁, g ≤ 21o₁); C; TR | the κ₀ term of the **pathwise** bound is attained: a measured path staying at S₀ throughout has RB error exactly κ₀ (ST-b; numerically 7.062579e-02 = κ₀ on 93 good-path islands). This is sharpness of the bound, not a proof that consistent RB PIPs require κ₀ → 0 (SW1 #7) | RESULTS_v1 §2 | sharp in form |
| P-MAP (S† = S₀) | D-iii/iv | implied by P-CONC; strictly weaker | — | — |
| P-OVL (Q_D → ∞, Q_D = D_rπ₀(S₀) on 𝒜, ∞ off 𝒜) | D | the draw-miss probability is an **equality** for the draw mechanism; only sufficient for the method. Conditional on no draw hitting S₀, S₀ was still a terminal particle endpoint in 13773/15015 and 30559/31505 islands (two targets) — other mechanisms discover it (SW1 #8) | RESULTS_v1 §5 | sharp for draws; improvable for the method |
| P-START (1_𝒜o₀ → 0, no rate) | C | some start/transport condition is needed for C's conclusions with fixed L: the finite "trap" target (π₀(S₀) = 1.5e-8) has collapsed W and wrong outputs (illustration only) | RESULTS_v1_sec4b | input (item-2 ticket) |
| NC_r | LT♯ (P(W_r < η) term) | **open** (sequence-level). Finite illustrations only: "trap" (collapsed W, wrong outputs) and "near" (collapsed W, RB error ≥ .1 in 23.5% of islands at L = 5, 0.9% at L = 20) | RESULTS_v1_sec4b | computational premise; discharged by C, replaced by TR |
| P-OVL∞ (P(𝒜 ∩ {L/M ≤ c}) → 0) | TR | sufficient, not necessary at finite size: "near" has M = 1.3e6 (TR vacuous) yet the local moves repair the PIPs | RESULTS_v3 TR block | global overlap relative to L |
| Linear δ̄ in C | C-iii, C-iv | possible but no lower-bound family proved (SW1 #15) | RESULTS_v3/v4 | — |

Implications (localised to 𝒜 where the premises are): P-CONC ⇒ P-MAP; 1_𝒜o₁ → 0 and P-START ⇒ NC_r (Theorem C);
P-START is implied by the item-2 rate π₀(S₀) ≥ 1 − n^{−c} on 𝒜; under P-CONC, P-OVL∞ implies π₀(S₀)·L → ∞ **on 𝒜** (SW1 #11).

## Gate history (dated; superseded items are kept for the record)

- 2026-11-09, v1/v2 gate (before BT1): flagged `improvable` — the factor T in C (then E|W − 1| ≤ 18Tδ̄ under T·δ̄ → 0;
  numerics showed E|W − 1| decreasing in T) and NC_r. Candidates then listed: (1) a min(T, D⁺) version of C; (2) a T-free
  C, "not attempted"; (3) a terminal-repair route.
- 2026-11-09, BT1 (`reviews/BT1_better_theorem_astra.md`, disposition `reviews/BT1_disposition.md`): (2) **proved**
  (telescoping; C-iii in v3, no T, no start-mass rate) — supersedes (1); (3) **proved** as Theorem TR (without the
  candidate's extra escape/entry condition); D's premise weakened to P-MAP; LT-b′, LT-e′ added. The T-free bound was
  subjected to falsification attempts with no violation detected (RESULTS_v3, v4) (SW1 #25).
- Not adopted (HQ: skip for now): Gibbs/swap-neighbour discovery bound (BT1 §3.2), pooled secondary estimator, ST
  constant 18.
